#!/usr/bin/env python3
"""
每日报告发送脚本 - 由 cron 调用
运行 orchestrator，读取报告，通过 Telegram 发给 wei
"""
import subprocess, json, sys
from pathlib import Path
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")
REPORT_FILE = Path("/root/.openclaw/workspace-crm/central/reports") / (TODAY + ".json")
ORCHESTRATOR = Path("/root/.openclaw/workspace-crm/central/orchestrator.py")

def send_telegram(msg):
    """通过本地 OpenClaw CLI 发 Telegram"""
    import urllib.request
    # 直接调用 openclaw message send
    cmd = [
        "openclaw", "message", "send",
        "--channel", "telegram",
        "--target", "wei",
        "--message", msg
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=15)
    except Exception as e:
        print("Telegram send failed:", e)

def main():
    # 1. 运行 orchestrator
    print("Running orchestrator...")
    r = subprocess.run(
        ["python3", str(ORCHESTRATOR)],
        capture_output=True, text=True, timeout=600,
        cwd="/root/.openclaw/workspace-crm"
    )
    print(r.stdout[-500:] if r.stdout else "(no stdout)")

    # 2. 读取报告
    if not REPORT_FILE.exists():
        msg = "⚠️ 今日报告文件不存在，请检查。"
        send_telegram(msg)
        print(msg)
        return 1

    report = json.loads(REPORT_FILE.read_text())
    summary = report.get("summary", {})
    agents = report.get("agents", [])

    # 3. 构造成 Telegram 消息
    date_str = TODAY
    total_pages = summary.get("total_pages", 0)
    total_errors = summary.get("total_errors", 0)
    problems = summary.get("problem_agents", [])

    lines = [
        f"📊 *每日生成报告 - {date_str}*",
        "",
    ]

    names = {"error-code": "错误码站", "supply": "供应站", "city": "城市站"}
    icons = {"OK": "✅", "ERROR": "❌", "CRASH": "💥"}

    for a in agents:
        nm = names.get(a["agent"], a["agent"])
        icon = icons.get(a.get("status", "?"), "⚠️")
        gen = a.get("total_generated", 0)
        err = a.get("total_errors", 0)
        lines.append(f"{icon} *{nm}*: {gen} 页生成, {err} 错误")

    lines.append("")
    lines.append(f"总计: {total_pages} 页, {total_errors} 错误")

    if problems or total_errors > 0:
        lines.append("")
        lines.append("⚠️ *需要关注 - 详情请查看报告*")
        for a in agents:
            if a.get("status") not in ("OK", None):
                lines.append(f"  • {a['agent']}: {a.get('error', '未知错误')[:100]}")
    else:
        lines.append("")
        lines.append("✅ *全部正常*")

    lines.append("")
    lines.append(f"报告: /root/.openclaw/workspace-crm/central/reports/{TODAY}.json")

    msg = "\n".join(lines)

    # 4. 发送
    send_telegram(msg)
    print(msg)
    return 0

if __name__ == "__main__":
    sys.exit(main())
