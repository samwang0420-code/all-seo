#!/usr/bin/env python3
"""
错误码站 - 生成 Brand/Category 索引页 + 修复内链
错误码页 → /brand/X/ 和 /category/Y/ 的链接改为真实存在的页
"""
import json, re
from pathlib import Path
from collections import defaultdict

DIR = Path("/root/.openclaw/workspace-crm/notebooklm_seo/output/error-codes")
BRANDS = ["amana","bosch","electrolux","frigidaire","ge","haier","hisense","kenmore","kitchenaid","lg","maytag","samsung","whirlpool"]
BRAND_NAMES = {
    "kitchenaid":"KitchenAid","whirlpool":"Whirlpool","maytag":"Maytag","ge":"General Electric",
    "bosch":"Bosch","samsung":"Samsung","lg":"LG Electronics","frigidaire":"Frigidaire",
    "electrolux":"Electrolux","amana":"Amana","kenmore":"Kenmore","haier":"Haier","hisense":"Hisense"
}
CATEGORIES = ["dishwasher","dryer","microwave","oven","refrigerator","washer"]
CAT_NAMES = {"dishwasher":"Dishwasher","dryer":"Clothes Dryer","microwave":"Microwave Oven","oven":"Wall Oven","refrigerator":"Refrigerator","washer":"Washing Machine"}

BASE_URL = "https://uscomplianceguard.com"

def build_brand_index(brand: str) -> str:
    brand_name = BRAND_NAMES.get(brand, brand.title())
    categories_data = []
    for cat in CATEGORIES:
        cat_dir = DIR / brand / cat
        if not cat_dir.exists():
            continue
        codes = sorted([f.stem for f in cat_dir.glob("*.html")])
        if not codes:
            continue
        codes_links = " | ".join(
            f'<a href="/error/{brand}/{cat}/{c.lower()}/" class="code-link">{c}</a>'
            for c in codes
        )
        categories_data.append(f'''
        <div class="cat-block">
          <h2>{CAT_NAMES.get(cat, cat.title())}</h2>
          <div class="codes">{codes_links}</div>
        </div>''')

    codes_total = sum(len(list((DIR/brand/cat).glob("*.html"))) for cat in CATEGORIES if (DIR/brand/cat).exists())
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{brand_name} Error Codes | Complete List & Fix Guide</title>
  <meta name="description" content="Complete list of {brand_name} error codes for all appliances. Find your error code and get step-by-step repair instructions.">
  <link rel="canonical" href="{BASE_URL}/brand/{brand}/">
  <script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebPage","name":"{brand_name} Error Codes","description":"Complete error code reference for {brand_name} appliances","publisher":{{"@type":"Organization","name":"USComplianceGuard"}}}}
  </script>
  <style>
    :root{{--p:#1a365d;--a:#2563eb;--bg:#f8fafc;--d:#0f172a}}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.6;color:#1e293b;background:var(--bg)}}
    .c{{max-width:1000px;margin:0 auto;padding:0 20px}}
    .hero{{background:linear-gradient(135deg,#0f172a 0%,#1a365d 100%);color:white;padding:60px 0;text-align:center}}
    .hero h1{{font-size:38px;font-weight:800;margin-bottom:10px}}
    .hero p{{opacity:.85;font-size:16px}}
    .stat{{background:rgba(255,255,255,.12);padding:16px 28px;border-radius:12px;display:inline-block;text-align:center;margin-top:20px}}
    .stat .n{{font-size:32px;font-weight:800;color:#fbbf24}}
    .cat-block{{background:white;border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid #e2e8f0}}
    .cat-block h2{{font-size:20px;font-weight:700;color:var(--p);margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid #e2e8f0}}
    .codes{{display:flex;flex-wrap:wrap;gap:8px}}
    .code-link{{background:#eff6ff;color:#1d4ed8;padding:6px 14px;border-radius:6px;font-size:14px;font-weight:600;text-decoration:none;border:1px solid #bfdbfe}}
    .code-link:hover{{background:#2563eb;color:white}}
    .breadcrumb{{padding:16px 0;font-size:14px;color:#64748b}}
    .breadcrumb a{{color:var(--a);text-decoration:none}}
    .footer{{text-align:center;padding:32px;color:#64748b;font-size:13px;border-top:1px solid #e2e8f0;margin-top:40px}}
  </style>
</head>
<body>
  <div class="hero">
    <div class="c">
      <h1>{brand_name} Error Codes</h1>
      <p>Complete error code reference for {brand_name} appliances — dishwasher, dryer, microwave, oven, refrigerator, washer</p>
      <div class="stat"><div class="n">{codes_total}</div><div style="font-size:13px;opacity:.8">Error Codes</div></div>
    </div>
  </div>
  <div class="c">
    <div class="breadcrumb"><a href="/">Home</a> &gt; <a href="/brand/{brand}/">{brand_name} Error Codes</a></div>
    {''.join(categories_data)}
  </div>
  <div class="footer">
    <p><a href="/">USComplianceGuard</a> | Error code data for reference purposes</p>
  </div>
</body>
</html>'''

def build_category_index(cat: str) -> str:
    cat_name = CAT_NAMES.get(cat, cat.title())
    brands_data = []
    for brand in BRANDS:
        cat_dir = DIR / brand / cat
        if not cat_dir.exists():
            continue
        codes = sorted([f.stem for f in cat_dir.glob("*.html")])
        if not codes:
            continue
        codes_links = " | ".join(
            f'<a href="/error/{brand}/{cat}/{c.lower()}/" class="code-link">{c}</a>'
            for c in codes
        )
        brands_data.append(f'''
        <div class="brand-block">
          <h3>{BRAND_NAMES.get(brand, brand.title())}</h3>
          <div class="codes">{codes_links}</div>
        </div>''')

    codes_total = sum(len(list((DIR/b/cat).glob("*.html"))) for b in BRANDS if (DIR/b/cat).exists())
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{cat_name} Error Codes | All Brands</title>
  <meta name="description" content="Complete list of {cat_name} error codes across all major brands. Find your error code and get step-by-step repair instructions.">
  <link rel="canonical" href="{BASE_URL}/category/{cat}/">
  <script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebPage","name":"{cat_name} Error Codes - All Brands","description":"Error codes for {cat_name} across all brands","publisher":{{"@type":"Organization","name":"USComplianceGuard"}}}}
  </script>
  <style>
    :root{{--p:#1a365d;--a:#2563eb;--bg:#f8fafc;--d:#0f172a}}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.6;color:#1e293b;background:var(--bg)}}
    .c{{max-width:1000px;margin:0 auto;padding:0 20px}}
    .hero{{background:linear-gradient(135deg,#0f172a 0%,#1a365d 100%);color:white;padding:60px 0;text-align:center}}
    .hero h1{{font-size:38px;font-weight:800;margin-bottom:10px}}
    .hero p{{opacity:.85;font-size:16px}}
    .stat{{background:rgba(255,255,255,.12);padding:16px 28px;border-radius:12px;display:inline-block;text-align:center;margin-top:20px}}
    .stat .n{{font-size:32px;font-weight:800;color:#fbbf24}}
    .brand-block{{background:white;border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid #e2e8f0}}
    .brand-block h3{{font-size:18px;font-weight:700;color:var(--p);margin-bottom:14px}}
    .codes{{display:flex;flex-wrap:wrap;gap:8px}}
    .code-link{{background:#eff6ff;color:#1d4ed8;padding:6px 14px;border-radius:6px;font-size:14px;font-weight:600;text-decoration:none;border:1px solid #bfdbfe}}
    .code-link:hover{{background:#2563eb;color:white}}
    .breadcrumb{{padding:16px 0;font-size:14px;color:#64748b}}
    .breadcrumb a{{color:var(--a);text-decoration:none}}
    .footer{{text-align:center;padding:32px;color:#64748b;font-size:13px;border-top:1px solid #e2e8f0;margin-top:40px}}
  </style>
</head>
<body>
  <div class="hero">
    <div class="c">
      <h1>{cat_name} Error Codes</h1>
      <p>Error codes for {cat_name} across all major appliance brands</p>
      <div class="stat"><div class="n">{codes_total}</div><div style="font-size:13px;opacity:.8">Error Codes</div></div>
    </div>
  </div>
  <div class="c">
    <div class="breadcrumb"><a href="/">Home</a> &gt; <a href="/category/{cat}/">{cat_name} Error Codes</a></div>
    {''.join(brands_data)}
  </div>
  <div class="footer">
    <p><a href="/">USComplianceGuard</a> | Error code data for reference purposes</p>
  </div>
</body>
</html>'''

def generate_indexes():
    """生成所有 brand 和 category 索引页"""
    out = []
    for brand in BRANDS:
        content = build_brand_index(brand)
        # Save at the brand level: error-codes/kitchenaid/index.html
        out_path = DIR / brand / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content)
        out.append(str(out_path.relative_to(DIR)))

    for cat in CATEGORIES:
        content = build_category_index(cat)
        # Save at a categories dir
        cat_dir = DIR / "categories"
        cat_dir.mkdir(exist_ok=True)
        out_path = cat_dir / f"{cat}.html"
        out_path.write_text(content)
        out.append(str(out_path.relative_to(DIR)))

    return out

if __name__ == "__main__":
    files = generate_indexes()
    print(f"✅ Generated {len(files)} index pages:")
    for f in files:
        print(f"  {f}")
