#!/usr/bin/env python3
"""
NotebookLM SEO Pipeline
自动处理 SEO 文章 URL → 上传 → 生成内容包

用法:
  python pipeline.py --url "https://..." --notebook "SEO-科技" --generate audio,quiz,flashcards
  python pipeline.py --watch          # 监听 queue 目录，自动处理新任务
  python pipeline.py --batch urls.txt # 批量处理文件中的所有 URL
"""

import argparse
import asyncio
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
from typing import Optional
import httpx

# ── 路径配置 ──────────────────────────────────────────────
ROOT = Path("/root/.openclaw/workspace-crm/notebooklm_seo")
QUEUE_DIR = ROOT / "queue"
OUTPUT_DIR = ROOT / "output"
LOGS_DIR = ROOT / "logs"

# 确保目录存在
for d in [QUEUE_DIR, OUTPUT_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

AUTH_PATH = Path("/root/.notebooklm/storage_state.json")

# ── 日志 ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("nbseo")


# ── NotebookLM SDK ─────────────────────────────────────────
sys.path.insert(0, "/usr/local/lib/python3.10/dist-packages")
from notebooklm import NotebookLMClient, AuthTokens, QuizQuantity, QuizDifficulty


async def get_client() -> NotebookLMClient:
    auth = await AuthTokens.from_storage(AUTH_PATH)
    return NotebookLMClient(auth)


# ── 数据模型 ───────────────────────────────────────────────
@dataclass
class SEOTask:
    url: str
    notebook_name: str
    article_title: Optional[str] = None
    generate: list[str] = field(default_factory=lambda: ["audio", "quiz", "flashcards", "report"])
    output_subdir: Optional[str] = None
    content: Optional[str] = None   # 直接传文章正文
    file_path: Optional[str] = None  # 或传文件路径

    @classmethod
    def from_line(cls, line: str) -> "SEOTask":
        """从 queue 文件的一行解析任务
        格式：URL|notebook|title|生成类型|content或@filepath
        最后一项以@开头表示文件路径，以content:开头表示直接传正文
        """
        line = line.strip()
        if not line or line.startswith("#"):
            return None
        parts = line.split("|")
        url = parts[0].strip()
        notebook = parts[1].strip() if len(parts) > 1 else "SEO默认"
        title = parts[2].strip() if len(parts) > 2 else None
        gens = (parts[3].strip().split(",") if len(parts) > 3 else ["audio", "quiz", "flashcards", "report"])

        # content 或 file_path
        content = None
        file_path = None
        if len(parts) > 4:
            extra = parts[4].strip()
            if extra.startswith("@"):
                file_path = extra[1:]
            elif extra.startswith("content:"):
                content = extra[8:]

        return cls(
            url=url,
            notebook_name=notebook,
            article_title=title,
            generate=gens,
            content=content,
            file_path=file_path,
        )


# ── Notebook 管理 ──────────────────────────────────────────
async def get_or_create_notebook(client: NotebookLMClient, name: str) -> str:
    """获取或创建一个 notebook，返回其 ID"""
    notebooks = await client.notebooks.list()
    for nb in notebooks:
        if nb.title == name:
            log.info(f"  使用已有 notebook: {name} ({nb.id[:12]}...)")
            return nb.id
    # 创建新的
    nb = await client.notebooks.create(name)
    log.info(f"  创建新 notebook: {name} ({nb.id[:12]}...)")
    return nb.id


# ── 内容上传 ───────────────────────────────────────────────
async def add_source(
    client: NotebookLMClient,
    notebook_id: str,
    url: str,
    content: Optional[str] = None,
    file_path: Optional[str] = None,
) -> bool:
    """添加内容到 notebook，优先级：content > file_path > url"""

    # 方式1：直接传文本内容
    if content:
        title = url or "Article Content"
        try:
            await client.sources.add_text(notebook_id, title, content, wait=True, wait_timeout=120)
            log.info(f"  ✅ 文本内容上传成功: {title}")
            return True
        except Exception as e:
            log.error(f"  ❌ 文本上传失败: {e}")
            return False

    # 方式2：传文件
    if file_path:
        path = Path(file_path).resolve()  # 转为绝对路径
        if not path.exists():
            log.error(f"  ❌ 文件不存在: {path}")
            return False
        try:
            await client.sources.add_file(notebook_id, str(path), wait=True, wait_timeout=120)
            log.info(f"  ✅ 文件上传成功: {file_path}")
            return True
        except Exception as e:
            log.error(f"  ❌ 文件上传失败: {e}")
            return False

    # 方式3：URL（自动降级为文本）
    try:
        await client.sources.add_url(notebook_id, url, wait=True, wait_timeout=120)
        log.info(f"  ✅ URL 上传成功: {url}")
        return True
    except Exception as e:
        log.warning(f"  ⚠️ URL 上传失败，尝试下载内容: {e}")

    # URL 失败 → 下载页面内容，用 add_text 上传
    try:
        text = await download_page_text(url)
        if text:
            await client.sources.add_text(notebook_id, url, text, wait=True, wait_timeout=120)
            log.info(f"  ✅ 页面下载+文本上传成功: {url}")
            return True
        else:
            log.error(f"  ❌ 无法获取页面内容: {url}")
            return False
    except Exception as e2:
        log.error(f"  ❌ 文本上传也失败: {e2}")
        return False


async def download_page_text(url: str, timeout: float = 15.0) -> Optional[str]:
    """下载页面正文文本，用于 NotebookLM add_text 上传"""
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as c:
            resp = await c.get(url)
            resp.raise_for_status()
            html = resp.text

        # 简单提取 <p> 文本
        import re
        # 移除 <script> <style> 等
        html = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', html)
        html = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', html)
        # 提取纯文本
        text = re.sub(r'<[^>]+>', ' ', html)
        # 清理多余空白
        text = re.sub(r'\s+', ' ', text).strip()

        if len(text) < 200:
            log.warning(f"  下载内容过少（{len(text)} chars），可能需要人工处理")
        else:
            log.info(f"  页面下载成功，提取 {len(text)} chars 文本")
        return text

    except Exception as e:
        log.error(f"  下载失败: {url} — {e}")
        return None


# ── 内容生成 ───────────────────────────────────────────────
GENERATE_MAP = {
    "audio": ("generate_audio", "audio.mp3", "download_audio"),
    "flashcards": ("generate_flashcards", "flashcards.json", "download_flashcards"),
    "quiz": ("generate_quiz", "quiz.json", "download_quiz"),
    "infographic": ("generate_infographic", "infographic.png", "download_infographic"),
    "report": ("generate_report", "report.md", "download_report"),
    "video": ("generate_video", "video.mp4", "download_video"),
}


async def generate_and_download(
    client: NotebookLMClient, notebook_id: str, task: SEOTask, output_path: Path
) -> dict:
    """并行生成所有内容，返回结果摘要"""
    log.info(f"  开始生成内容: {', '.join(task.generate)}")

    async def one_task(gen_key: str, out_filename: str, dl_func_name: str, dl_extra_args=()):
        if gen_key not in GENERATE_MAP:
            log.warning(f"  未知生成类型: {gen_key}")
            return gen_key, False, None
        gen_func_name, _, dl_func_name = GENERATE_MAP[gen_key]

        try:
            # 生成
            gen_func = getattr(client.artifacts, gen_func_name)
            dl_func = getattr(client.artifacts, dl_func_name)
            status = await gen_func(notebook_id, **dl_extra_args)
            # 等待完成（超时5分钟）
            final = await client.artifacts.wait_for_completion(notebook_id, status.task_id, timeout=300)
            if final.is_failed:
                log.error(f"  ❌ {gen_key} 生成失败: {final.error}")
                return gen_key, False, None
            # 下载
            out_file = output_path / out_filename
            await dl_func(notebook_id, str(out_file), status.task_id)
            size = out_file.stat().st_size
            log.info(f"  ✅ {gen_key}: {out_filename} ({size/1024:.1f} KB)")
            return gen_key, True, str(out_file)
        except Exception as e:
            log.error(f"  ❌ {gen_key} 出错: {e}")
            return gen_key, False, None

    # 构造生成参数
    gen_params = {
        "audio": (),
        "flashcards": ({"quantity": QuizQuantity.STANDARD}),
        "quiz": ({"quantity": QuizQuantity.STANDARD}),
        "infographic": ({"orientation": 2, "detail_level": 2}),  # PORTRAIT, DETAILED
        "report": ({}),
        "video": ({}),
    }

    # 并行生成所有内容
    tasks = []
    for key in task.generate:
        if key not in GENERATE_MAP:
            continue
        _, out_file, _ = GENERATE_MAP[key]
        params = gen_params.get(key, {})
        tasks.append(one_task(key, out_file, None, params))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    summary = {}
    for r in results:
        if isinstance(r, Exception):
            log.error(f"  任务异常: {r}")
            continue
        key, ok, path = r
        summary[key] = {"ok": ok, "path": path}

    return summary


# ── 处理单个任务 ───────────────────────────────────────────
async def process_task(task: SEOTask) -> dict:
    """处理一个 SEO 任务，返回结果"""
    start = time.time()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r"[^\w\-_. ]", "_", task.article_title or task.url)[:50]
    output_path = OUTPUT_DIR / (task.output_subdir or "default")
    output_path.mkdir(parents=True, exist_ok=True)
    output_path = output_path / f"{safe_name}_{ts}"
    output_path.mkdir(parents=True, exist_ok=True)

    result = {
        "task": task.url,
        "notebook": task.notebook_name,
        "output": str(output_path),
        "generate_results": {},
        "success": False,
    }

    try:
        async with await get_client() as client:

            # 获取或创建 notebook
            notebook_id = await get_or_create_notebook(client, task.notebook_name)

            # 添加内容（URL / 文件 / 正文）
            ok = await add_source(
                client, notebook_id,
                url=task.url,
                content=task.content,
                file_path=task.file_path,
            )
            if not ok:
                return result

            # 生成所有内容
            summary = await generate_and_download(client, notebook_id, task, output_path)
            result["generate_results"] = summary
            result["success"] = all(v["ok"] for v in summary.values() if v["path"] is not None)

            elapsed = time.time() - start
            log.info(f"✅ 任务完成: {task.url} ({elapsed:.0f}s)")

    except Exception as e:
        log.error(f"❌ 任务失败: {task.url} — {e}")
        result["error"] = str(e)

    # 保存结果 JSON
    result_file = output_path / "_result.json"
    result_file.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    return result


# ── 批量处理 ───────────────────────────────────────────────
async def process_batch(urls: list[str], notebook: str, generate: list[str]):
    """批量处理多个 URL"""
    tasks = [
        SEOTask(url=url, notebook_name=notebook, generate=generate)
        for url in urls if url.strip()
    ]
    log.info(f"📦 批量任务: {len(tasks)} 个 URL")
    results = []
    for task in tasks:
        r = await process_task(task)
        results.append(r)
    return results


# ── 监听队列 ───────────────────────────────────────────────
async def watch_queue(interval: int = 30):
    """定期扫描 queue 目录，处理新任务"""
    log.info(f"👁️  开始监听 queue 目录: {QUEUE_DIR} (每 {interval}s 检查一次)")
    processed_file = QUEUE_DIR / ".processed"

    # 读取已处理记录
    processed = set()
    if processed_file.exists():
        processed = set(processed_file.read_text().splitlines())

    while True:
        try:
            for queue_file in sorted(QUEUE_DIR.glob("*.txt")):
                lines = queue_file.read_text().splitlines()
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("#") or line in processed:
                        continue
                    task = SEOTask.from_line(line)
                    if not task:
                        continue
                    log.info(f"📥 发现新任务: {line[:80]}")
                    await process_task(task)
                    processed.add(line)
                    # 记录已处理
                    processed_file.write_text("\n".join(processed))

            await asyncio.sleep(interval)
        except KeyboardInterrupt:
            log.info("👋 监听停止")
            break
        except Exception as e:
            log.error(f"监听异常: {e}")
            await asyncio.sleep(interval)


# ── CLI 入口 ───────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="NotebookLM SEO Pipeline")
    parser.add_argument("--url", help="单个 URL")
    parser.add_argument("--batch", type=argparse.FileType("r"), help="批量文件（每行一个 URL）")
    parser.add_argument("--notebook", default="SEO默认", help="Notebook 名称")
    parser.add_argument(
        "--generate",
        default="audio,flashcards,quiz,report",
        help="生成内容类型（逗号分隔）: audio,flashcards,quiz,infographic,report,video",
    )
    parser.add_argument("--title", help="文章标题（用于文件名）")
    parser.add_argument("--file", help="本地文章文件路径（Markdown/PDF），优先上传此文件而非抓取URL")
    parser.add_argument("--watch", action="store_true", help="监听 queue 目录")
    parser.add_argument("--interval", type=int, default=30, help="监听检查间隔（秒）")

    args = parser.parse_args()

    if args.watch:
        asyncio.run(watch_queue(args.interval))
        return

    # 单个 URL
    if args.url:
        task = SEOTask(
            url=args.url,
            notebook_name=args.notebook,
            article_title=args.title,
            generate=args.generate.split(","),
            file_path=args.file,
        )
        asyncio.run(process_task(task))
        return

    # 批量文件
    if args.batch:
        urls = [line.strip() for line in args.batch if line.strip() and not line.startswith("#")]
        results = asyncio.run(process_batch(urls, args.notebook, args.generate.split(",")))
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
