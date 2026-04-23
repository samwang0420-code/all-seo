#!/usr/bin/env python3
"""
便捷脚本：SEO agent 一行命令添加任务到队列

用法：
  python3 queue_task.py --url "https://..." --notebook "SEO-科技" --title "文章标题"
  python3 queue_task.py --url "https://..." --notebook "SEO-科技" --generate audio,flashcards
"""
import argparse
import os
import sys
from pathlib import Path

QUEUE_DIR = Path("/root/.openclaw/workspace-crm/notebooklm_seo/queue")


def get_default_notebook():
    """从文件名推断 notebook 名称"""
    import os
    return os.environ.get("SEO_NOTEBOOK", "SEO默认")


def add_task(url: str, notebook: str, title: str = None, generate: str = "audio,flashcards,quiz,report", file_path: str = None):
    """将任务追加到队列
    
    file_path: 本地文章文件路径（Markdown/PDF），会直接上传到 NotebookLM（不依赖 URL 抓取）
    """
    # 自动为 notebook 创建队列文件
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in notebook)
    queue_file = QUEUE_DIR / f"{safe_name}.txt"

    # 第5列：@文件路径 或留空
    extra = f"@{file_path}" if file_path else ""
    line = f"{url}|{notebook}|{title or ''}|{generate}|{extra}"
    with open(queue_file, "a") as f:
        f.write(line + "\n")

    print(f"✅ 任务已添加到队列: {queue_file}")
    print(f"   URL: {url}")
    print(f"   Notebook: {notebook}")
    print(f"   生成: {generate}")
    print(f"\n📋 当前队列 ({queue_file}):")
    with open(queue_file) as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        print(f"   共 {len(lines)} 个任务")

    return queue_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="添加 NotebookLM SEO 任务到队列")
    parser.add_argument("--url", required=True, help="文章 URL")
    parser.add_argument("--notebook", default=get_default_notebook(), help="Notebook 名称")
    parser.add_argument("--title", help="文章标题（用于文件名）")
    parser.add_argument("--generate", default="audio,flashcards,quiz,report",
                        help="生成类型: audio,flashcards,quiz,report,infographic,video")
    parser.add_argument("--file", help="本地文章文件路径（Markdown/PDF），优先上传此文件而非抓取URL")
    args = parser.parse_args()

    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    add_task(args.url, args.notebook, args.title, args.generate, args.file)
