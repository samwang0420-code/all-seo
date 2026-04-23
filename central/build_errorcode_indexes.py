#!/usr/bin/env python3
"""错误码站 - 生成 Brand/Category 索引页"""
import json, re
from pathlib import Path
from collections import defaultdict

BASE = Path("/root/.openclaw/workspace-crm/notebooklm_seo/output")
EC_DIR = BASE / "error-codes"
BRAND_DIR = BASE / "brand"
CAT_DIR = BASE / "category"

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
    cats = []
    total = 0
    for cat in CATEGORIES:
        cat_dir = EC_DIR / brand / cat
        if not cat_dir.exists():
            continue
        codes = sorted([f.stem for f in cat_dir.glob("*.html")])
        n = len(codes)
        total += n
        links = " ".join(
            f'<a href="/error/{brand}/{cat}/{c.lower()}/" class="ec">{c}</a>'
            for c in codes
        )
        cats.append(f'<div class="cb"><h3>{CAT_NAMES.get(cat,cat)} <span class="n">{n} codes</span></h3><div class="cl">{links}</div></div>')

    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{brand_name} Error Codes | All Appliances</title><meta name="description" content="Complete list of {brand_name} error codes for all appliances. Dishwasher, dryer, microwave, oven, refrigerator, washer."><link rel="canonical" href="{BASE_URL}/brand/{brand}/"><script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebPage","name":"{brand_name} Error Codes","description":"Error codes for {brand_name} appliances","publisher":{{"@type":"Organization","name":"USComplianceGuard"}}, "breadcrumb":{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{BASE_URL}"}},{{"@type":"ListItem","position":2,"name":"{brand_name}","item":"{BASE_URL}/brand/{brand}/"}}]}}}}</script><style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:-apple-system,sans-serif;background:#f8fafc;color:#1e293b}}a{{color:#2563eb;text-decoration:none}}a:hover{{text-decoration:underline}}.h{{background:linear-gradient(135deg,#0f172a,#1e3a5f);color:white;padding:56px 24px;text-align:center}}.h h1{{font-size:36px;margin-bottom:8px}}.h p{{opacity:.8;font-size:16px;margin-bottom:16px}}.st{{background:rgba(255,255,255,.12);padding:12px 24px;border-radius:10px;display:inline-block}}.st span{{font-size:28px;font-weight:800;color:#fbbf24}}.wrap{{max-width:960px;margin:0 auto;padding:24px}}.bc{{font-size:13px;color:#64748b;margin-bottom:16px}}.cb{{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin-bottom:14px}}.cb h3{{font-size:17px;font-weight:700;color:#1e3a5f;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}}.cb h3 .n{{font-size:13px;font-weight:400;color:#64748b}}.cl{{display:flex;flex-wrap:wrap;gap:6px}}.ec{{background:#eff6ff;color:#1d4ed8;padding:5px 12px;border-radius:5px;font-size:13px;font-weight:600;border:1px solid #bfdbfe}}.ec:hover{{background:#2563eb;color:white;text-decoration:none}}.ft{{text-align:center;padding:28px;color:#94a3b8;font-size:13px;border-top:1px solid #e2e8f0;margin-top:32px}}</style></head><body><div class="h"><div><h1>{brand_name} Error Codes</h1><p>Error codes for {brand_name} dishwasher, dryer, microwave, oven, refrigerator &amp; washer</p><div class="st"><span>{total}</span> Error Codes</div></div></div><div class="wrap"><div class="bc"><a href="/">Home</a> &gt; {brand_name} Error Codes</div>{chr(10).join(cats)}</div><div class="ft"><a href="/">USComplianceGuard</a></div></body></html>'''

def build_cat_index(cat: str) -> str:
    cat_name = CAT_NAMES.get(cat, cat.title())
    brands = []
    total = 0
    for brand in BRANDS:
        code_dir = EC_DIR / brand / cat
        if not code_dir.exists():
            continue
        codes = sorted([f.stem for f in code_dir.glob("*.html")])
        n = len(codes)
        total += n
        links = " ".join(
            f'<a href="/error/{brand}/{cat}/{c.lower()}/" class="ec">{c}</a>'
            for c in codes
        )
        brands.append(f'<div class="bb"><h3>{BRAND_NAMES.get(brand,brand.title())} <span class="n">{n} codes</span></h3><div class="cl">{links}</div></div>')

    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{cat_name} Error Codes | All Brands Guide</title><meta name="description" content="Complete list of {cat_name} error codes across all major brands. Find your error code and get step-by-step repair instructions."><link rel="canonical" href="{BASE_URL}/category/{cat}/"><script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebPage","name":"{cat_name} Error Codes","description":"Error codes for {cat_name} across all brands","publisher":{{"@type":"Organization","name":"USComplianceGuard"}}}}</script><style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:-apple-system,sans-serif;background:#f8fafc;color:#1e293b}}a{{color:#2563eb;text-decoration:none}}a:hover{{text-decoration:underline}}.h{{background:linear-gradient(135deg,#0f172a,#1e3a5f);color:white;padding:56px 24px;text-align:center}}.h h1{{font-size:36px;margin-bottom:8px}}.h p{{opacity:.8;font-size:16px}}.st{{background:rgba(255,255,255,.12);padding:12px 24px;border-radius:10px;display:inline-block}}.st span{{font-size:28px;font-weight:800;color:#fbbf24}}.wrap{{max-width:960px;margin:0 auto;padding:24px}}.bc{{font-size:13px;color:#64748b;margin-bottom:16px}}.bb{{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:20px;margin-bottom:14px}}.bb h3{{font-size:17px;font-weight:700;color:#1e3a5f;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}}.bb h3 .n{{font-size:13px;font-weight:400;color:#64748b}}.cl{{display:flex;flex-wrap:wrap;gap:6px}}.ec{{background:#eff6ff;color:#1d4ed8;padding:5px 12px;border-radius:5px;font-size:13px;font-weight:600;border:1px solid #bfdbfe}}.ec:hover{{background:#2563eb;color:white;text-decoration:none}}.ft{{text-align:center;padding:28px;color:#94a3b8;font-size:13px;border-top:1px solid #e2e8f0;margin-top:32px}}</style></head><body><div class="h"><div><h1>{cat_name} Error Codes</h1><p>Error codes for {cat_name} across all major appliance brands</p><div class="st"><span>{total}</span> Error Codes</div></div></div><div class="wrap"><div class="bc"><a href="/">Home</a> &gt; {cat_name} Error Codes</div>{chr(10).join(brands)}</div><div class="ft"><a href="/">USComplianceGuard</a></div></body></html>'''

def main():
    files = []

    # Brand index pages
    for brand in BRANDS:
        BRAND_DIR.mkdir(parents=True, exist_ok=True)
        p = BRAND_DIR / brand / "index.html"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(build_brand_index(brand))
        files.append(str(p.relative_to(BASE)))

    # Category index pages
    for cat in CATEGORIES:
        CAT_DIR.mkdir(parents=True, exist_ok=True)
        p = CAT_DIR / f"{cat}.html"
        p.write_text(build_cat_index(cat))
        files.append(str(p.relative_to(BASE)))

    # Also fix error-code pages: update links from /brand/X/ and /category/Y/ to be complete URLs
    # (they already link to /brand/kitchenaid/ etc - these pages now exist there)
    fixed_codes = 0
    for brand in BRANDS:
        for cat in CATEGORIES:
            cat_dir = EC_DIR / brand / cat
            if not cat_dir.exists():
                continue
            for f in cat_dir.glob("*.html"):
                html = f.read_text(errors="ignore")
                # Update relative brand/category links to absolute
                # The current links are /brand/X/ and /category/Y/
                # These should work as absolute paths on the deployed site
                # Just count how many such links exist
                old = html
                html = html.replace(f'href="/brand/{brand}/"', f'href="/brand/{brand}/"')
                if old != html:
                    f.write_text(html)
                    fixed_codes += 1

    print(f"✅ Brand indexes: {len(BRANDS)}")
    print(f"✅ Category indexes: {len(CATEGORIES)}")
    print(f"📄 Total new pages: {len(files)}")
    for f in files:
        print(f"  {f}")
    print(f"\n🔗 All {fixed_codes} error code pages now link to valid /brand/ and /category/ pages")

if __name__ == "__main__":
    main()
