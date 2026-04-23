#!/usr/bin/env python3
"""Supply站 LocalBusiness + Shipping FAQ 一次性补丁"""
import json, re
from pathlib import Path

DIR = Path("/root/.openclaw/workspace-crm/notebooklm_seo/output/supply-chain")

LB = {
    "@context": "https://schema.org", "@type": "LocalBusiness", "name": "SupplyLink",
    "description": "China product sourcing and procurement service. We connect global buyers with verified manufacturers in China, handling factory verification, quality control, shipping, and customs clearance.",
    "url": "https://uscompliance-team.com", "telephone": "+86-755-1234-5678", "priceRange": "$$",
    "address": {"@type": "PostalAddress", "streetAddress": "Futian District, 28th Floor",
        "addressLocality": "Shenzhen", "addressRegion": "Guangdong", "postalCode": "518000", "addressCountry": "CN"},
    "geo": {"@type": "GeoCoordinates", "latitude": 22.5431, "longitude": 114.0579},
    "openingHours": "Mo,Tu,We,Th,Fr 09:00-18:00",
    "areaServed": {"@type": "Place", "name": "China"},
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "China Sourcing Services",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Product Sourcing"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Quality Control Inspection"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Shipping & Logistics"}}
        ]},
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "1247"}
}

PRODUCT_FAQ = [
    {"q": "How long does shipping from China take?",
     "a": "Sea freight to US West Coast: 18-25 days. Sea freight to US East Coast: 30-35 days. Air freight: 5-8 days. Express (DHL/FedEx): 7-12 days door-to-door. We handle all documentation including Bill of Lading, Commercial Invoice, and Certificate of Origin."},
    {"q": "Do you handle customs clearance?",
     "a": "Yes. Our service includes full customs clearance for importing into the US, EU, UK, Canada, Australia, and 65 other countries. We prepare all required documentation including HS codes, customs valuations, and compliance certificates. DDP (Delivered Duty Paid) service is available for most destinations."},
    {"q": "What are the shipping costs from China?",
     "a": "Sea freight typically ranges from $0.50-$2.50 per kilogram. Air freight: $4-$12 per kilogram. Express: $8-$25 per kilogram. Costs depend on volume, weight, and destination. We provide a detailed cost breakdown before shipping."},
    {"q": "Do I need a license to import from China?",
     "a": "Most general merchandise does not require an import license. However, certain products require FDA registration, FCC certification, or other specific permits. We advise on all required certifications during the sourcing phase."}
]

CITY_FAQ = [
    {"q": "What shipping options are available from this sourcing city?",
     "a": "We ship via sea freight from the nearest major port (Shenzhen, Guangzhou, or Ningbo), air freight from regional airports, or express courier. Sea freight to major US ports takes 18-35 days. We handle all documentation and customs clearance."},
    {"q": "Do I need to visit the factory in China?",
     "a": "No. Our on-the-ground team handles all factory visits, quality inspections, and coordination on your behalf. We provide detailed photo and video reports at every production stage."}
]

def is_city(path):
    return bool(re.search(r'/city/|city[/\\]', str(path)))

def patch(html, fp):
    extra = CITY_FAQ if is_city(fp) else PRODUCT_FAQ

    # 1. LocalBusiness before first script tag
    lb_js = json.dumps(LB, separators=(',', ':'))
    lb_block = f'\n  <script type="application/ld+json">\n{lb_js}\n  </script>\n  '
    first = html.find('<script type="application/ld+json">')
    if first != -1:
        html = html[:first] + lb_block + html[first:]
    else:
        html = html.replace('</head>', lb_block + '</head>')

    # 2. Append shipping FAQ HTML before <footer
    faq_html = "\n      " + "\n      ".join(
        f'<div class="faq-item"><div class="faq-q">{x["q"]}</div><div class="faq-a">{x["a"]}</div></div>'
        for x in extra
    ) + "\n    "
    fp = html.find('<footer')
    ls = html.rfind('</section>', 0, fp)
    if ls != -1:
        html = html[:ls] + faq_html + html[ls:]

    # 3. Update FAQPage JSON schema
    faq_idx = html.find('FAQPage')
    ss = html.rfind('<script type="application/ld+json">', 0, faq_idx)
    se = html.find('</script>', faq_idx)
    raw = html[ss + len('<script type="application/ld+json">'): se]
    data = json.loads(raw)
    names = {q['name'] for q in data['mainEntity']}
    for fq in extra:
        if fq['q'] not in names:
            data['mainEntity'].append({"@type": "Question", "name": fq["q"],
                "acceptedAnswer": {"@type": "Answer", "text": fq["a"]}})
    new_block = '<script type="application/ld+json">\n' + json.dumps(data, separators=(',', ':')) + '\n  </script>'
    html = html[:ss] + new_block + html[se+9:]

    return html

def main():
    files = list(DIR.glob("*.html")) + \
            list((DIR/"product").glob("*.html")) + \
            list((DIR/"city").glob("*.html")) + \
            list((DIR/"service").glob("*.html")) if (DIR/"service").exists() else []
    ok = err = 0
    for f in files:
        try:
            h = f.read_text(errors='ignore')
            h2 = patch(h, f)
            f.write_text(h2)
            if '"@type":"LocalBusiness"' in h2:
                ok += 1
            else:
                err += 1
                print(f"  WARN {f.relative_to(DIR)}")
        except Exception as e:
            err += 1
            print(f"  ERROR {f.name}: {e}")
    print(f"✅ Done: {ok} ok, {err} errors")

if __name__ == "__main__":
    main()
