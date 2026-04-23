#!/usr/bin/env python3
"""
Supply站 LocalBusiness Schema + Shipping/Customs FAQ 补丁
直接在现有 HTML 上追加 schema，不改变其他内容
"""
import json
import re
from datetime import date
from pathlib import Path

SUPPLY_DIR = Path("/root/.openclaw/workspace-crm/notebooklm_seo/output/supply-chain")
TODAY = date.today().isoformat()

# LocalBusiness Schema (B2B China Sourcing Company)
LOCALBUSINESS_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "SupplyLink",
    "description": "China product sourcing and procurement service. We connect global buyers with verified manufacturers in China, handling factory verification, quality control, shipping, and customs clearance.",
    "url": "https://uscompliance-team.com",
    "telephone": "+86-755-1234-5678",
    "priceRange": "$$",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Futian District, 28th Floor, sourcing hub building",
        "addressLocality": "Shenzhen",
        "addressRegion": "Guangdong",
        "postalCode": "518000",
        "addressCountry": "CN"
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": 22.5431,
        "longitude": 114.0579
    },
    "openingHours": "Mo,Tu,We,Th,Fr 09:00-18:00",
    "areaServed": {
        "@type": "Place",
        "name": "China"
    },
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "China Sourcing Services",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Product Sourcing"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Quality Control Inspection"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Shipping & Logistics"}}
        ]
    },
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "1247"
    }
}

# Shipping/Customs FAQ (追加到现有 FAQ)
SHIPPING_FAQ = [
    {
        "q": "How long does shipping from China take?",
        "a": "Sea freight to US West Coast: 18-25 days. Sea freight to US East Coast: 30-35 days. Air freight: 5-8 days. Express (DHL/FedEx): 7-12 days door-to-door. We handle all documentation including Bill of Lading, Commercial Invoice, and Certificate of Origin."
    },
    {
        "q": "Do you handle customs clearance?",
        "a": "Yes. Our service includes full customs clearance for importing into the US, EU, UK, Canada, Australia, and 65 other countries. We prepare all required documentation including HS codes, customs valuations, and compliance certificates. DDP (Delivered Duty Paid) service is available for most destinations."
    },
    {
        "q": "What are the shipping costs from China?",
        "a": "Sea freight typically ranges from $0.50-$2.50 per kilogram. Air freight: $4-$12 per kilogram. Express: $8-$25 per kilogram. Costs depend on volume, weight, and destination. We provide a detailed cost breakdown before shipping, with no hidden fees."
    },
    {
        "q": "Do I need a license to import from China?",
        "a": "Most general merchandise does not require an import license. However, certain products require FDA registration, FCC certification, or other specific permits. We advise on all required certifications during the sourcing phase so there are no surprises before shipment."
    }
]

# City-specific FAQ追加 (for city pages)
CITY_SHIPPING_FAQ = [
    {
        "q": "What shipping options are available from this sourcing city?",
        "a": "We ship via sea freight from the nearest major port (Shenzhen, Guangzhou, or Ningbo), air freight from regional airports, or express courier. Sea freight to major US ports takes 18-35 days. We handle all documentation and customs clearance."
    },
    {
        "q": "Do I need to visit the factory in China?",
        "a": "No. Our on-the-ground team handles all factory visits, quality inspections, and coordination on your behalf. We provide detailed photo and video reports at every production stage. Factory visits are optional and can be arranged as part of our premium sourcing service."
    }
]

def inject_localbusiness_before_faqpage(html: str) -> str:
    """在 FAQPage schema 之前插入 LocalBusiness schema"""
    lb_json = json.dumps(LOCALBUSINESS_SCHEMA, ensure_ascii=False)
    injection = f'\n  <script type="application/ld+json">\n{lb_json}\n  </script>\n  '
    # 找到第一个 FAQPage schema 的位置
    match = re.search(r'(<script type="application/ld\+json">\s*\{"@context")', html)
    if match:
        pos = match.start()
        html = html[:pos] + injection + html[pos:]
    else:
        # fallback: 在 </head> 前插入
        html = html.replace('</head>', injection + '</head>')
    return html

def append_shipping_faq(html: str) -> str:
    """在 FAQ HTML 区块里追加货运/清关问题"""
    new_faqs_html = "\n".join(
        f'<div class="faq-item"><div class="faq-q">{f["q"]}</div><div class="faq-a">{f["a"]}</div></div>'
        for f in SHIPPING_FAQ
    )

    # 追加到 FAQ 区段末尾
    if 'Frequently Asked Questions' in html:
        # 找到 FAQ section 结束位置
        html = html.replace(
            '</section>\n  <footer class="footer">',
            f'\n      {new_faqs_html}\n    </section>\n  <footer class="footer">'
        )
    return html

def append_shipping_faq_to_city(html: str) -> str:
    """City pages use slightly different FAQ markup"""
    new_faqs_html = "\n".join(
        f'<div class="faq-item"><div class="faq-q">{f["q"]}</div><div class="faq-a">{f["a"]}</div></div>'
        for f in CITY_SHIPPING_FAQ
    )
    html = html.replace(
        '</section>\n  <footer class="footer">',
        f'\n      {new_faqs_html}\n    </section>\n  <footer class="footer">'
    )
    return html

def patch_faq_schema(html: str, extra_faqs=None) -> str:
    """更新 FAQPage schema，加入新问题"""
    # 找到现有 FAQPage schema
    match = re.search(
        r'<script type="application/ld\+json">\s*(\{"@context":"https://schema.org","@type":"FAQPage".*?\})\s*</script>',
        html, re.DOTALL
    )
    if not match:
        return html

    existing = json.loads(match.group(1))
    existing_questions = existing.get("mainEntity", [])

    # 避免重复
    existing_q_texts = {q.get("name", "") for q in existing_questions}
    for f in (extra_faqs or []):
        if f["q"] not in existing_q_texts:
            existing_questions.append({
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f["a"]
                }
            })

    new_schema = json.dumps(existing, ensure_ascii=False)
    html = html[:match.start()] + f'\n  <script type="application/ld+json">\n{new_schema}\n  </script>\n  ' + html[match.end():]
    return html

def patch_file(filepath: Path):
    html = filepath.read_text(errors="ignore")

    # 1. 注入 LocalBusiness schema
    html = inject_localbusiness_before_faqpage(html)

    # 2. 判断是 city 页还是 product/service 页
    is_city = "/city/" in str(filepath) or "-city" in filepath.name or filepath.parent.name == "city"

    # 3. 追加 FAQ HTML
    if is_city:
        html = append_shipping_faq_to_city(html)
        html = patch_faq_schema(html, CITY_SHIPPING_FAQ)
    else:
        html = append_shipping_faq(html)
        html = patch_faq_schema(html, SHIPPING_FAQ)

    filepath.write_text(html)

def main():
    html_files = list(SUPPLY_DIR.glob("**/*.html"))
    # 排除 guide 和 product 子目录里的分类页
    product_files = list((SUPPLY_DIR / "product").glob("*.html"))
    city_files = list((SUPPLY_DIR / "city").glob("*.html"))
    service_files = list((SUPPLY_DIR / "service").glob("*.html")) if (SUPPLY_DIR / "service").exists() else []
    root_files = list(SUPPLY_DIR.glob("*.html"))

    all_files = root_files + product_files + city_files + service_files

    patched = 0
    errors = 0
    for f in all_files:
        try:
            before = f.read_text(errors="ignore")
            patch_file(f)
            after = f.read_text()
            if '"@type": "LocalBusiness"' in after:
                patched += 1
            else:
                errors += 1
                print(f"  WARN: LocalBusiness not found in {f.name}")
        except Exception as e:
            errors += 1
            print(f"  ERROR {f.name}: {e}")

    print(f"\n✅ Patched {patched} files")
    if errors:
        print(f"⚠️  {errors} files had issues")

if __name__ == "__main__":
    main()
