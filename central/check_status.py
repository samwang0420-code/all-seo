#!/usr/bin/env python3
"""快速检查三个 agent 状态的脚本"""
import subprocess, json
from pathlib import Path
from datetime import datetime

REPORTS = Path("/root/.openclaw/workspace-crm/central/reports")
TODAY = datetime.now().strftime("%Y-%m-%d")
YESTERDAY = datetime.fromisoformat(
    (datetime.now().replace(hour=0, minute=0, second=0)).isoformat()
).strftime("%Y-%m-%d")

def get_latest_report():
    """找到最新的报告"""
    files = sorted(REPORTS.glob("2*.json"), reverse=True)
    if files:
        return files[0]
    return None

def count_pages_by_site():
    """统计各站总页面数"""
    total = {"error-code": 0, "supply": 0, "city": 0}
    for f in sorted(REPORTS.glob("2*.json")):
        try:
            d = json.loads(f.read_text())
            for a in d.get("agents", []):
                total[a["agent"]] = total.get(a["agent"], 0) + a.get("total_generated", 0)
        except:
            pass
    return total

def main():
    print("=" * 50)
    print("📊 SEO 中枢状态检查")
    print("=" * 50)
    print()

    # 最新报告
    latest = get_latest_report()
    if latest:
        d = json.loads(latest.read_text())
        date = d.get("date", "unknown")
        summary = d.get("summary", {})
        print(f"📅 最新报告: {date}")
        print(f"   文件: {latest.name}")
        print()

        names = {"error-code": "错误码站", "supply": "供应站", "city": "城市站"}
        icons = {"OK": "✅", "ERROR": "❌", "CRASH": "💥"}
        for a in d.get("agents", []):
            nm = names.get(a["agent"], a["agent"])
            icon = icons.get(a.get("status", "?"), "⚠️")
            gen = a.get("total_generated", 0)
            err = a.get("total_errors", 0)
            site = a.get("site", "")
            print(f"  {icon} {nm} ({site})")
            print(f"     生成: {gen} 页 | 错误: {err}")

        print()
        print(f"  总计: {summary.get('total_pages', 0)} 页, {summary.get('total_errors', 0)} 错误")
        if summary.get("needs_attention"):
            print(f"  ⚠️  需要关注")
        else:
            print(f"  ✅ 全部正常")
    else:
        print("  无报告文件")

    print()
    print("-" * 50)
    print("📈 累计总页面数（所有报告）:")
    totals = count_pages_by_site()
    for k, v in totals.items():
        nm = {"error-code": "错误码站", "supply": "供应站", "city": "城市站"}.get(k, k)
        print(f"  • {nm}: {v} 页")
    print()
    print(f"  总计: {sum(totals.values())} 页")
    print()
    print(f"📁 报告目录: {REPORTS}")
    print(f"🕐 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
