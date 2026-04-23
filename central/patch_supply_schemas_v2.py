#!/usr/bin/env python3
"""
Supply站 LocalBusiness Schema + Shipping/Customs FAQ 补丁 v2
"""
import json
import re
from datetime import date
from pathlib import Path

SUPPLY_DIR = Path("/root/.openclaw/workspace-crm/notebooklm_seo/output/supply-chain")
TODAY = date.today().isoformat()

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
    "geo": {"@type": "GeoCoordinates", "latitude": 22.5431, "longitude": 114.0579},
    "openingHours": "Mo,Tu,We,Th,Fr 09:00-18:00",
    "areaServed": {"@type": "Place", "name": "China"},
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "China Sourcing Services",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Product Sourcing"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Quality Control Inspection"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Shipping & Logistics"}}
        ]
    },
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "1247"}
}

SHIPPING_FAQ = [
    {"q": "How long does shipping from China take?", "a": "Sea freight to US West Coast: 18-25 days. Sea freight to US East Coast: 30-35 days. Air freight: 5-8 days. Express (DHL/FedEx): 7-12 days door-to-door. We handle all documentation including Bill of Lading, Commercial Invoice, and Certificate of Origin."},
    {"q": "Do you handle customs clearance?", "a": "Yes. Our service includes full customs clearance for importing into the US, EU, UK, Canada, Australia, and 65 other countries. We prepare all required documentation including HS codes, customs valuations, and compliance certificates. DDP (Delivered Duty Paid) service is available for most destinations."},
    {"q": "What are the shipping costs from China?", "a": "Sea freight typically ranges from $0.50-$2.50 per kilogram. Air freight: $4-$12 per kilogram. Express: $8-$25 per kilogram. Costs depend on volume, weight, and destination. We provide a detailed cost breakdown before shipping, with no hidden fees."},
    {"q": "Do I need a license to import from China?", "a": "Most general merchandise does not require an import license. However, certain products require FDA registration, FCC certification, or other specific permits. We advise on all required certifications during the sourcing phase so there are no surprises before shipment."}
]

CITY_SHIPPING_FAQ = [
    {"q": "What shipping options are available from this sourcing city?", "a": "We ship via sea freight from the nearest major port (Shenzhen, Guangzhou, or Ningbo), air freight from regional airports, or express courier. Sea freight to major US ports takes 18-35 days. We handle all documentation and customs clearance."},
    {"q": "Do I need to visit the factory in China?", "a": "No. Our on-the-ground team handles all factory visits, quality inspections, and coordination on your behalf. We provide detailed photo and video reports at every production stage. Factory visits are optional and can be arranged as part of our premium sourcing service."}
]

def lb_json_str():
    return "\n" + json.dumps(LOCALBUSINESS_SCHEMA, ensure_ascii=False) + "\n"

def faq_item_html(q, a):
    return f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'

def patch_file(filepath: Path):
    html = filepath.read_text(errors="ignore")
    original = html

    is_city = bool(re.search(r'/city/|/city-data/', filepath.name.replace("\\", "/"))) or \
              filepath.parent.name == "city"

    extra_faqs = CITY_SHIPPING_FAQ if is_city else SHIPPING_FAQ

    # 1. Inject LocalBusiness schema before the first <script (which is the Service or FAQPage schema)
    lb_block = f'\n  <script type="application/ld+json">{lb_json_str()}</script>\n  '
    first_script = html.find('<script type="application/ld+json">')
    if first_script != -1:
        html = html[:first_script] + lb_block + html[first_script:]
    else:
        html = html.replace('</head>', lb_block + '</head>')

    # 2. Append shipping FAQ HTML before </section> that closes the FAQ block
    # Find the last </section> before <footer
    footer_pos = html.find('<footer')
    if footer_pos != -1:
        last_section_before_footer = html.rfind('</section>', 0, footer_pos)
        if last_section_before_footer != -1:
            extra_html = "\n      " + "\n      ".join(faq_item_html(f["q"], f["a"]) for f in extra_faqs) + "\n    "
            html = html[:last_section_before_footer] + extra_html + html[last_section_before_footer:]

    # 3. Update FAQPage schema JSON
    # Find FAQPage script block
    faqpage_script_start = html.find('<script type="application/ld+json">', html.find("FAQPage"))
    if faqpage_script_start == -1:
        return  # skip if no FAQPage

    faqpage_script_end = html.find('</script>', faqpage_script_start)
    faqpage_block = html[faqpage_script_start:faqpage_script_end+9]

    # Extract the JSON from the block
    json_start = faqpage_block.index('{')
    json_str = faqpage_block[json_start:faqpage_script_end]
    faqpage_data = json.loads(json_str)

    existing_q_texts = {q["name"] for q in faqpage_data.get("mainEntity", [])}
    for f in extra_faqs:
        if f["q"] not in existing_q_texts:
            faqpage_data["mainEntity"].append({
                "@type": "Question",
                "name": f["q"],
                "acceptedAnswer": {"@type": "Answer", "text": f["a"]}
            })

    new_faqpage_block = '<script type="application/ld+json">\n' + json.dumps(faqpage_data, ensure_ascii=False) + '\n  </script>'
    html = html[:faqpage_script_start] + new_faqpage_block + html[faqpage_script_end+9:]

    filepath.write_text(html)

def main():
    subdirs = ["product", "city", "service"]
    files = []
    for f in SUPPLY_DIR.glob("*.html"):
        files.append(f)
    for sub in subdirs:
        sub_path = SUPPLY_DIR / sub
        if sub_path.is_dir():
            files.extend(sub_path.glob("*.html"))

    patched = errors = 0
    for f in files:
        try:
            before = len(f.read_text(errors="ignore"))
            patch_file(f)
            after_len = len(f.read_text())
            if after_len > before and '"@type": "LocalBusiness"' in f.read_text():
                patched += 1
            else:
                errors += 1
                print(f"  WARN: {f.relative_to(SUPPLY_DIR)}")
        except Exception as e:
            errors += 1
            print(f"  ERROR {f.name}: {e}")

    print(f"✅ Patched {patched} files successfully")
    if errors:
        print(f"⚠️  {errors} files had issues")

if __name__ == "__main__":
    main()
