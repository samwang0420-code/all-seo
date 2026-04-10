#!/usr/bin/env python3
"""
SEO/GEO 中枢监控系统
主动检查三个站的 SEO 健康度，不只是等错误报告
"""
import subprocess, json, re
from datetime import datetime
from pathlib import Path

OUTPUT = Path("/root/.openclaw/workspace-crm/central/reports")
OUTPUT.mkdir(parents=True, exist_ok=True)
TODAY = datetime.now().strftime("%Y-%m-%d")

def check_site(name, html_dir):
    """检查一个站点的 SEO 健康度"""
    issues = []
    warnings = []
    health = {"name": name, "html_count": 0, "schema_count": 0,
              "faq_count": 0, "author_count": 0, "issues": [], "warnings": []}

    html_files = list(Path(html_dir).glob("**/*.html"))
    health["html_count"] = len(html_files)

    if len(html_files) == 0:
        health["issues"].append("无 HTML 文件")
        return health

    sample = html_files[:20]  # 抽查前20个

    for f in sample:
        try:
            content = f.read_text(errors="ignore")

            # Schema 检测
            if '"@type": "FAQPage"' in content or '"@type":"FAQPage"' in content:
                health["schema_count"] += 1
            if '"@type": "Person"' in content or '"@type":"Person"' in content:
                health["author_count"] += 1
            if '"@type": "HowTo"' in content or '"@type":"HowTo"' in content:
                health["faq_count"] += 1

            # 常见 SEO 问题
            if "lorem ipsum" in content.lower() or "placeholder" in content.lower():
                issues.append(f"{f.name}: 含占位符文本")

            if content.count("<h1") > 3:
                warnings.append(f"{f.name}: 超过 3 个 H1 标签")

            if len(content) < 3000 and "error-code" in str(html_dir):
                warnings.append(f"{f.name}: 内容过短 (<3KB)，可能被判断为薄页")

            # 检测 AI 内容模式
            ai_patterns = ["in conclusion", "in summary", "overall,"]
            for p in ai_patterns:
                if content.lower().count(p) > 2:
                    warnings.append(f"{f.name}: 过度使用 {p}（AI 内容特征）")

        except Exception as e:
            issues.append(f"{f.name}: 读取失败 {e}")

    health["schema_pct"] = round(health["schema_count"] / len(sample) * 100) if sample else 0
    health["author_pct"] = round(health["author_count"] / len(sample) * 100) if sample else 0
    health["issues"] = issues
    health["warnings"] = warnings
    return health

def check_internal_links(html_dir, site_url):
    """检查内链结构"""
    results = {"links_found": 0, "broken_suspicious": []}
    html_files = list(Path(html_dir).glob("**/*.html"))[:10]  # 抽查

    for f in html_files:
        content = f.read_text(errors="ignore")
        # 找相对路径链接
        links = re.findall(r'href="(/\w[^"]*)"', content)
        results["links_found"] += len(links)
        # 检查有没有指向不存在的页面
        for link in links:
            if "sitemap" in link or "contact" in link:
                pass  # 正常
            # 截断链接检查
            target = Path(html_dir + link)
            if not target.exists() and link.endswith("/"):
                results["broken_suspicious"].append(f"{f.name} -> {link}")

    return results

def geo_analysis(html_dir, site_type):
    """GEO（地理 SEO）分析"""
    results = {"geo_signals": [], "missing": []}

    if site_type == "city":
        html_files = list(Path(html_dir).glob("**/*.html"))[:10]
        for f in html_files:
            content = f.read_text(errors="ignore")
            if '"@type": "City"' in content or '"@type":"City"' in content:
                results["geo_signals"].append(f"{f.name}: 有 City Schema")
            if "coordinates" in content.lower() or "lat" in content.lower():
                results["geo_signals"].append(f"{f.name}: 有坐标数据")
            if "area-code" in content or "area_codes" in content:
                results["geo_signals"].append(f"{f.name}: 有区号信息")

        results["missing"].append("Place Schema（替代 City Schema）")
        results["missing"].append("GeoCoordinates（经纬度）")
        results["missing"].append("TouristDestination Schema（旅游城市）")

    elif site_type == "supply":
        results["missing"].append("LocalBusiness Schema（中文采购服务）")
        results["missing"].append("FAQ on shipping/to customs")
        results["missing"].append("City-specific content（新塘/广州等中国城市详情）")

    return results

def main():
    print("=" * 60)
    print("🩺 SEO/GEO 健康检查")
    print("=" * 60)

    sites = [
        ("错误码站", "/root/.openclaw/workspace-crm/notebooklm_seo/output/error-codes", "error-code"),
        ("供应站",   "/root/.openclaw/workspace-crm/notebooklm_seo/output/supply-chain", "supply"),
        ("城市站",   "/root/.openclaw/workspace-crm/notebooklm_seo/output/city-data", "city"),
    ]

    all_results = {"date": TODAY, "timestamp": datetime.now().isoformat(), "sites": []}
    total_issues = 0

    for name, path, stype in sites:
        print(f"\n📋 {name} ({path})")
        health = check_site(name, path)
        links = check_internal_links(path, stype)
        geo = geo_analysis(path, stype)

        result = {**health, "links": links, "geo": geo}
        all_results["sites"].append(result)

        print(f"  HTML 文件: {health['html_count']}")
        print(f"  FAQ Schema 覆盖率: {health.get('schema_pct', 0)}%")
        print(f"  Author Schema 覆盖率: {health.get('author_pct', 0)}%")
        print(f"  内链数量: {links['links_found']} (抽查10个)")

        if health["issues"]:
            print(f"  ❌ 问题: {health['issues']}")
            total_issues += len(health["issues"])
        if health["warnings"]:
            print(f"  ⚠️  警告: {len(health['warnings'])} 项")
        if geo["missing"]:
            print(f"  📍 GEO 缺失: {geo['missing']}")

    # 保存报告
    report_file = OUTPUT / f"seo_health_{TODAY}.json"
    report_file.write_text(json.dumps(all_results, indent=2, ensure_ascii=False))
    print(f"\n📁 报告: {report_file}")

    # 优先修复项
    print("\n" + "=" * 60)
    print("🔧 优先修复项")
    print("=" * 60)
    for site in all_results["sites"]:
        if site["issues"] or site["warnings"] or site["geo"]["missing"]:
            print(f"\n【{site['name']}】")
            for issue in site["issues"]:
                print(f"  ❌ {issue}")
            for warn in site["warnings"][:3]:
                print(f"  ⚠️  {warn}")
            for miss in site["geo"]["missing"][:3]:
                print(f"  📍 GEO: {miss}")

    return 0 if total_issues == 0 else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
