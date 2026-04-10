#!/usr/bin/env python3
"""
Supply Chain B2B Content Generator
用法：
  python3 supply_generator.py --type product --slug clothing \
    --url "https://uscompliance-team.com/clothing.html" --h1 "Clothing Sourcing from China"

  python3 supply_generator.py --type city --slug shenzhen \
    --url "https://uscompliance-team.com/shenzhen.html"

  python3 supply_generator.py --type guide --slug moq-guide \
    --url "https://uscompliance-team.com/moq-guide.html"
"""

import argparse
import json
from datetime import date
from pathlib import Path


PRODUCTS = {
    "clothing": {"h1": "Clothing Sourcing from China", "desc": "Connect with verified clothing manufacturers in China. MOQ from 500 pcs with quality inspection included.", "items": ["T-shirts", "Hoodies", "Activewear", "Dresses", "Jackets", "Pants"], "moq": "500-2,000 pcs", "price": "$3-25/pc", "lead": "25-45 days"},
    "shoes": {"h1": "Shoes Sourcing from China", "desc": "Source shoes from verified Chinese manufacturers. Sports shoes, casual shoes, and sandals with quality inspection.", "items": ["Running shoes", "Casual sneakers", "Sandals", "Boots", "Formal shoes"], "moq": "300-1,000 pairs", "price": "$4-50/pair", "lead": "30-60 days"},
    "bags": {"h1": "Bags & Luggage Sourcing from China", "desc": "Find reliable bag manufacturers in China. Backpacks, travel bags, handbags with factory-direct pricing.", "items": ["Backpacks", "Travel bags", "Handbags", "Tote bags", "Laptop bags"], "moq": "200-1,000 pcs", "price": "$2-40/pc", "lead": "20-40 days"},
    "electronics": {"h1": "Electronics Sourcing from China", "desc": "Source consumer electronics from verified Chinese factories. Quality control and worldwide shipping.", "items": ["Bluetooth speakers", "Wireless chargers", "Smart watches", "Earbuds", "Power banks"], "moq": "500-5,000 pcs", "price": "$5-200/pc", "lead": "20-50 days"},
    "sports": {"h1": "Sports Equipment Sourcing from China", "desc": "Source sports equipment and fitness gear from verified Chinese manufacturers.", "items": ["Yoga mats", "Dumbbells", "Resistance bands", "Fitness trackers", "Camping gear"], "moq": "200-2,000 pcs", "price": "$2-150/pc", "lead": "25-50 days"},
    "beauty-products": {"h1": "Beauty & Cosmetics Sourcing from China", "desc": "Source beauty products and cosmetics from verified Chinese manufacturers.", "items": ["Skincare sets", "Lipstick", "Face masks", "Hair care", "Nail polish"], "moq": "1,000-5,000 pcs", "price": "$1-30/pc", "lead": "30-60 days"},
    "toys": {"h1": "Toys Sourcing from China", "desc": "Find safe, certified toy manufacturers in China. Educational toys, plush toys, and board games.", "items": ["Educational toys", "Plush toys", "Board games", "RC cars", "Building blocks"], "moq": "500-3,000 pcs", "price": "$1-50/pc", "lead": "25-45 days"},
    "fitness-equipment": {"h1": "Fitness Equipment Sourcing from China", "desc": "Source gym equipment and fitness accessories from verified Chinese factories.", "items": ["Treadmills", "Exercise bikes", "Weight benches", "Pull-up bars", "Kettlebells"], "moq": "50-500 pcs", "price": "$20-500/pc", "lead": "30-60 days"},
    "womens-clothing": {"h1": "Women's Clothing Sourcing from China", "desc": "Source women's fashion from verified Chinese manufacturers. Competitive MOQ and strict QC.", "items": ["Dresses", "Blouses", "Pants", "Skirts", "Coats", "Sweaters"], "moq": "300-1,500 pcs", "price": "$4-40/pc", "lead": "20-40 days"},
    "mens-clothing": {"h1": "Men's Clothing Sourcing from China", "desc": "Source men's apparel from verified Chinese factories. Quality fabrics and reliable delivery.", "items": ["T-shirts", "Shirts", "Pants", "Jackets", "Suits", "Swimwear"], "moq": "300-1,500 pcs", "price": "$5-45/pc", "lead": "20-40 days"},
    "childrens-clothing": {"h1": "Children's Clothing Sourcing from China", "desc": "Source kids' clothing from certified Chinese manufacturers. Safety standards and soft fabrics.", "items": ["Baby onesies", "Kids T-shirts", "Children's dresses", "Kids pants", "School uniforms"], "moq": "500-2,000 pcs", "price": "$2-25/pc", "lead": "20-40 days"},
    "sportswear": {"h1": "Sportswear & Athletic Apparel Sourcing", "desc": "Source high-performance sportswear from verified Chinese manufacturers.", "items": ["Sports bras", "Compression leggings", "Running shorts", "Athletic tops", "Tracksuits"], "moq": "500-2,000 pcs", "price": "$5-35/pc", "lead": "25-45 days"},
    "swimwear": {"h1": "Swimwear Sourcing from China", "desc": "Source swimwear from verified Chinese manufacturers. Beachwear and custom designs.", "items": ["Bikinis", "One-piece swimsuits", "Board shorts", "Rash guards", "Swim trunks"], "moq": "300-1,000 pcs", "price": "$4-30/pc", "lead": "25-40 days"},
    "underwear": {"h1": "Underwear & Intimates Sourcing from China", "desc": "Source underwear and intimates from verified Chinese factories.", "items": ["Men's underwear", "Women's bras", "Boxers", "Briefs", "Lingerie sets"], "moq": "1,000-5,000 pcs", "price": "$1-15/pc", "lead": "20-35 days"},
    "yoga-mats": {"h1": "Yoga Mats & Fitness Accessories Sourcing", "desc": "Source yoga mats and fitness accessories from verified Chinese manufacturers.", "items": ["Yoga mats", "Pilates mats", "Exercise mats", "Yoga blocks", "Yoga straps"], "moq": "200-2,000 pcs", "price": "$2-30/pc", "lead": "15-30 days"},
}

CITIES = {
    "shenzhen": {"h1": "Sourcing Products from Shenzhen, China", "desc": "Shenzhen is China's tech and manufacturing hub. Source electronics, gadgets, and innovative products.", "specialties": ["Electronics", "Gadgets", "Smart devices", "3C accessories"], "highlights": ["Tech innovation hub", "Rapid prototyping", "Huaqiangbei market", "Global shipping"]},
    "guangzhou": {"h1": "Sourcing Products from Guangzhou, China", "desc": "Guangzhou is China's trading capital. Source clothing, accessories, and wholesale goods.", "specialties": ["Clothing", "Shoes", "Bags", "Accessories"], "highlights": ["Canton Fair access", "Easy market visits", "Diverse product range", "Export expertise"]},
    "yiwu": {"h1": "Sourcing Products from Yiwu, China", "desc": "Yiwu is the world's largest small commodity market. Source gifts, accessories, and daily products.", "specialties": ["Gifts", "Toys", "Stationery", "Party supplies"], "highlights": ["World's largest market", "Low minimum orders", "One-stop sourcing", "Logistics hub"]},
    "ningbo": {"h1": "Sourcing Products from Ningbo, China", "desc": "Ningbo is a major port city and manufacturing center. Source machinery, tools, and industrial products.", "specialties": ["Machinery", "Tools", "Auto parts", "Home appliances"], "highlights": ["Major port city", "Industrial manufacturing", "Competitive freight", "Export experience"]},
    "dongguan": {"h1": "Sourcing Products from Dongguan, China", "desc": "Dongguan is China's manufacturing heartland. Source electronics, toys, and labor-intensive products.", "specialties": ["Electronics", "Toys", "Furniture", "Shoes", "Textiles"], "highlights": ["Manufacturing heartland", "Competitive pricing", "Skilled workforce", "Factory-direct"]},
    "qingdao": {"h1": "Sourcing Products from Qingdao, China", "desc": "Qingdao combines manufacturing strength with port convenience. Source machinery, textiles, and consumer goods.", "specialties": ["Machinery", "Textiles", "Rubber products", "Home appliances"], "highlights": ["Port convenience", "Strong industrial base", "Textile expertise", "Freight advantages"]},
}

SERVICES = {
    "sourcing": {"h1": "China Product Sourcing Service", "desc": "We identify verified manufacturers, negotiate pricing, and manage the entire sourcing process.", "steps": [("Market Analysis", "We research your product category to identify high-margin, reliable manufacturers matching your quality and volume requirements."), ("Factory Matching", "Based on your specs, we match you with 3-5 pre-vetted factories and provide detailed profiles."), ("Sample Management", "We coordinate samples, handle shipping, and provide detailed quality assessments."), ("Price Negotiation", "Our local team negotiates better pricing and terms, typically saving 15-30% on production costs."), ("Order Management", "We monitor production, coordinate inspections, and manage documentation for smooth delivery.")], "benefits": ["100% verified factories", "15-30% cost savings", "Dedicated sourcing agent", "Quality guarantee", "No hidden fees"]},
    "inspection": {"h1": "Quality Control & Product Inspection in China", "desc": "Our on-the-ground inspectors visit your factory to ensure every unit meets your specs before shipment.", "steps": [("Pre-Production Check", "We verify materials, components, and factory setup before production begins."), ("During Production Inspection", "We randomly inspect products during production to catch issues early."), ("Pre-Shipment Inspection", "We conduct comprehensive inspection including function testing, labeling, and packaging."), ("Loading Supervision", "We supervise container loading to ensure correct quantities and proper packaging."), ("Lab Testing", "We arrange third-party lab testing for safety certifications and compliance.")], "benefits": ["Certified inspectors", "Detailed photo reports", "Same-day reporting", "AQL 2.5/4.0 standards", "Compliance support"]},
    "shipping": {"h1": "China Shipping & Logistics Solutions", "desc": "From factory to your door, we handle all logistics including documentation, customs clearance, and delivery.", "steps": [("Route Planning", "We analyze your volume, timeline, and budget to recommend the optimal shipping method."), ("Documentation", "We prepare all export/import documents including invoices, packing lists, and certificates of origin."), ("Customs Clearance", "Our customs brokers handle all import procedures ensuring compliance and avoiding delays."), ("Cargo Tracking", "Real-time tracking from factory pickup through final delivery with proactive alerts."), ("Last-Mile Delivery", "We coordinate warehousing and final delivery to your warehouse or store.")], "benefits": ["Door-to-door service", "Real-time tracking", "Customs included", "Competitive freight", "Insurance coverage"]},
}

GUIDES = {
    "moq-guide": {"h1": "MOQ (Minimum Order Quantity) Guide for China Sourcing", "desc": "Understand MOQ requirements from Chinese manufacturers and learn strategies to minimize your initial investment.", "keywords": ["MOQ China sourcing", "minimum order quantity", "low MOQ manufacturer"]},
    "quality-control": {"h1": "Quality Control Guide for China Sourcing", "desc": "Protect your brand with systematic quality control. Learn inspection standards and AQL levels.", "keywords": ["quality control China", "AQL inspection", "product inspection China"]},
    "shipping-guide": {"h1": "Shipping from China: Complete Guide", "desc": "Compare shipping methods from China. Learn sea freight, air freight, express, and how to choose.", "keywords": ["shipping from China", "sea freight China", "air freight China"]},
    "incoterms-guide": {"h1": "Incoterms 2020 Guide for Importers", "desc": "Understand international trade terms. Learn EXW, FOB, CIF, DDP and how each affects your costs.", "keywords": ["Incoterms 2020", "FOB China", "CIF vs DDP"]},
    "sourcing-guide": {"h1": "Complete China Sourcing Guide for Businesses", "desc": "Everything you need to know about sourcing products from China.", "keywords": ["China sourcing guide", "how to source from China", "finding manufacturers"]},
}


FAQ_DATA_PRODUCT = {
    "clothing": [{"q": "What is the minimum order quantity for clothing from China?", "a": "MOQ for basic clothing typically ranges from 200-500 pieces per color per style. Custom designs with brand labels usually require 500+ pieces minimum. We help negotiate lower MOQs with verified factories."}, {"q": "How do you ensure quality control for clothing orders?", "a": "We arrange pre-production sample approval, in-line inspections during manufacturing, and pre-shipment inspection via our certified QC team in the production city. AQL 2.5 standards are applied for major defects."}, {"q": "What is the typical production lead time for clothing from China?", "a": "Standard production takes 25-35 days after sample approval. Express orders (with factory priority) can be completed in 15-20 days for additional fees. Shipping adds 20-35 days by sea freight or 5-10 days by air."}, {"q": "Can you source sustainable and organic fabrics?", "a": "Yes, we work with factories certified for GOTS organic, OEKO-TEX, and BCI sustainable cotton. These materials typically add 15-30% to unit costs but command premium market positioning."}],
    "default": [{"q": "What is the minimum order quantity?", "a": "MOQ varies by product category and factory. Most suppliers require 200-500 pieces for initial orders. We negotiate flexible MOQs for startups and small businesses."}, {"q": "How long does sourcing take?", "a": "Factory identification takes 3-5 business days. Sample approval adds 7-14 days. Production typically requires 25-35 days. We provide a detailed timeline in your custom quote."}, {"q": "Do you handle quality control?", "a": "Yes. Our standard service includes pre-production, during-production, and pre-shipment inspections by certified QC inspectors. Additional inspection rounds can be arranged as needed."}, {"q": "What countries do you ship to?", "a": "We have shipped to 68 countries including USA, UK, Canada, Australia, Germany, France, and Japan. We handle all customs documentation including COO, COO, and commercial invoices."}]
}

def generate_product(slug: str, url: str, h1: str = "") -> str:
    p = PRODUCTS.get(slug, PRODUCTS["clothing"])
    h1 = h1 or p["h1"]
    today = date.today().isoformat()
    items_html = "".join(f"<span class=\"item-tag\">{i}</span>" for i in p["items"])
    trust_badges = '<div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap;margin:20px 0 24px;"><span style="background:rgba(255,255,255,.15);padding:10px 18px;border-radius:8px;font-size:13px;"><strong style="color:#FBBF24">5,000+</strong> <span style="opacity:.8">Verified Factories</span></span><span style="background:rgba(255,255,255,.15);padding:10px 18px;border-radius:8px;font-size:13px;"><strong style="color:#FBBF24">50,000+</strong> <span style="opacity:.8">Orders Done</span></span><span style="background:rgba(255,255,255,.15);padding:10px 18px;border-radius:8px;font-size:13px;"><strong style="color:#FBBF24">68</strong> <span style="opacity:.8">Countries</span></span></div>'
    faqs = FAQ_DATA_PRODUCT.get(slug, FAQ_DATA_PRODUCT["default"])
    faq_schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":f['q'],"acceptedAnswer":{"@type":"Answer","text":f['a']}} for f in faqs]}
    faq_html = "\n".join(f'<div class="faq-item"><div class="faq-q">{f["q"]}</div><div class="faq-a">{f["a"]}</div></div>' for f in faqs)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{h1} | SupplyLink</title>
  <meta name="description" content="{p["desc"]}">
  <link rel="canonical" href="{url}">
  <script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","name":"{h1}","description":"{p["desc"]}","provider":{{"@type":"Organization","name":"SupplyLink","url":"https://uscompliance-team.com"}}}}
  <script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Person","name":"David Chen","jobTitle":"Senior China Sourcing Consultant","worksFor":{{"@type":"Organization","name":"SupplyLink","url":"https://uscompliance-team.com"}},"description":"David has 12+ years of experience helping businesses source from China."}}
  </script>
  <style>
    :root{{--p:#1E3A8A;--a:#2563EB;--s:#16A34A;--bg:#F8FAFC;--d:#0F172A}}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.7;color:#1E293B;background:var(--bg)}}
    .c{{max-width:1100px;margin:0 auto;padding:0 20px}}
    .hero{{background:linear-gradient(135deg,#0F172A 0%,#1E3A8A 60%,#2563EB 100%);color:white;padding:80px 0;text-align:center}}
    .hero h1{{font-size:42px;font-weight:800;margin-bottom:16px;line-height:1.2}}
    .hero p{{font-size:18px;opacity:.9;max-width:700px;margin:0 auto 32px}}
    .stats{{display:flex;gap:40px;justify-content:center;flex-wrap:wrap}}
    .stat{{text-align:center}}
    .stat .n{{font-size:30px;font-weight:800;color:#FBBF24}}
    .stat .l{{font-size:13px;opacity:.8}}
    .sec{{padding:60px 0}}
    .sec h2{{font-size:28px;font-weight:700;color:var(--d);margin-bottom:20px}}
    .sec p{{font-size:16px;color:#475569;margin-bottom:14px}}
    .specs{{background:white;border-radius:12px;padding:28px;border:1px solid #E2E8F0;display:grid;grid-template-columns:1fr 1fr;gap:0}}
    .spec-row{{display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid #F1F5F9}}
    .spec-row:last-child{{border-bottom:none}}
    .sl{{color:#64748B;font-size:15px}}
    .sv{{font-weight:700;color:var(--d);font-size:15px}}
    .items{{display:flex;flex-wrap:wrap;gap:10px}}
    .item-tag{{background:#EFF6FF;color:#1E40AF;padding:8px 18px;border-radius:20px;font-size:14px;font-weight:600}}
    .cta{{background:linear-gradient(135deg,#16A34A 0%,#15803D 100%);color:white;padding:48px 32px;border-radius:16px;text-align:center;margin:40px 0}}
    .cta h2{{color:white;margin-bottom:12px;font-size:28px}}
    .cta p{{color:rgba(255,255,255,.9);margin-bottom:24px;font-size:16px}}
    .cta-btn{{display:inline-block;background:white;color:#16A34A;padding:14px 36px;border-radius:8px;font-weight:700;font-size:16px;text-decoration:none}}
    .cta-btn:hover{{background:#F0FDF4}}
    .footer{{text-align:center;padding:40px;color:#64748B;font-size:14px;border-top:1px solid #E2E8F0;margin-top:40px}}
    .footer a{{color:var(--a)}}
    .faq-item{{border-bottom:1px solid #E2E8F0;padding-bottom:18px;margin-bottom:18px}}
    .faq-item:last-child{{border-bottom:none;margin-bottom:0}}
    .faq-q{{font-weight:700;color:var(--d);font-size:15px;margin-bottom:8px}}
    .faq-a{{color:#475569;font-size:14px;line-height:1.7}}
    @media(max-width:600px){{.hero h1{{font-size:28px}}.specs{{grid-template-columns:1fr}}}}
  </style>
  <script type="application/ld+json">
{json.dumps(faq_schema)}
  </script>
</head>
<body>
  <div class="hero">
    <div class="c">
      <h1>{h1}</h1>
      <p>{p["desc"]}</p>
      <div class="stats">
        <div class="stat"><div class="n">50,000+</div><div class="l">Orders Processed</div></div>
        <div class="stat"><div class="n">5,000+</div><div class="l">Verified Factories</div></div>
        <div class="stat"><div class="n">120+</div><div class="l">Countries Shipped</div></div>
      </div>
    </div>
  </div>
  <div class="c">
    <section class="sec">
      <h2>Product Categories Available</h2>
      <div class="items">{items_html}</div>
    </section>
    <section class="sec">
      <h2>Specifications & Pricing</h2>
      <div class="specs">
        <div class="spec-row"><span class="sl">Minimum Order (MOQ)</span><span class="sv">{p["moq"]}</span></div>
        <div class="spec-row"><span class="sl">Price Range</span><span class="sv">{p["price"]}</span></div>
        <div class="spec-row"><span class="sl">Production Lead Time</span><span class="sv">{p["lead"]}</span></div>
        <div class="spec-row"><span class="sl">Custom Logo/Label</span><span class="sv">Included</span></div>
        <div class="spec-row"><span class="sl">Quality Inspection</span><span class="sv">Pre-shipment included</span></div>
        <div class="spec-row"><span class="sl">Sample Available</span><span class="sv">Yes (7-14 days)</span></div>
      </div>
    </section>
    <section class="sec">
      <h2>Our Sourcing Process</h2>
      <p>We handle every step of the sourcing process so you can focus on your business.</p>
      <div class="specs" style="margin-top:16px;">
        <div class="spec-row"><span class="sl">Step 1</span><span class="sv">Market research & factory identification</span></div>
        <div class="spec-row"><span class="sl">Step 2</span><span class="sv">Factory vetting & reference checks</span></div>
        <div class="spec-row"><span class="sl">Step 3</span><span class="sv">Sample coordination & quality assessment</span></div>
        <div class="spec-row"><span class="sl">Step 4</span><span class="sv">Price negotiation & contract signing</span></div>
        <div class="spec-row"><span class="sl">Step 5</span><span class="sv">Production monitoring & quality control</span></div>
        <div class="spec-row"><span class="sl">Step 6</span><span class="sv">Shipping, customs & door delivery</span></div>
      </div>
    </section>
    <div class="cta">
      <h2>Ready to Source {p['items'][0]}?</h2>
      <p>Get a free sourcing quote within 24 hours. No commitment required.</p>
      {trust_badges}
      <a href="/contact.html" class="cta-btn">Get Free Quote</a>
    </div>
    <section class="sec">
      <h2>Frequently Asked Questions</h2>
      {faq_html}
    </section>
  </div>
  <footer class="footer">
    <p><a href="/">SupplyLink</a> | <a href="/sourcing-guide.html">Sourcing Guide</a> | <a href="/contact.html">Contact Us</a></p>
    <p style="margin-top:8px;">Last updated: {today}</p>
  </footer>
</body>
</html>'''


FAQ_CITY = [{"q": "Why source from this manufacturing hub?", "a": "This city offers competitive pricing, well-established supply chains, and experienced workers. Our verified factories in the area have passed our 12-point vetting process."}, {"q": "What is the typical MOQ when sourcing from this region?", "a": "MOQ varies by product type. General merchandise: 200-500 pieces. Custom/oem orders: 500-1000 pieces. We negotiate flexible MOQs for startups."}, {"q": "How do you handle quality control?", "a": "We have dedicated QC inspectors in this sourcing region. Standard service includes pre-shipment inspection. We also offer in-line inspection for larger orders."}, {"q": "What are the shipping options?", "a": "Sea freight (20-35 days) to major US ports. Air freight (5-10 days) for urgent orders. We handle all customs clearance and documentation."}]
FAQ_SERVICE = [{"q": "How do you verify factory legitimacy?", "a": "We verify business licenses via Chinese government databases (AIC), check import/export records, conduct factory visits, and require references from current buyers. Every factory in our network passes our 12-point verification."}, {"q": "What quality standards do you enforce?", "a": "We apply AQL 2.5 for major defects and AQL 4.0 for minor defects. Inspectors are certified by the International Federation of Inspection Agencies (IFIA)."}, {"q": "What if I'm not satisfied with the product quality?", "a": "We offer a 100% rework or refund policy if products fail to meet agreed specifications. Our dispute resolution team mediates between buyers and factories."}, {"q": "How do you protect my intellectual property?", "a": "We require factories to sign NDA and IP protection agreements. We never share your product designs with other clients. Designs are stored securely and only released to your chosen factory."}]
FAQ_GUIDE = [{"q": "What is the best shipping method from China?", "a": "Sea freight (20-35 days) is most economical for orders over 1 cubic meter. Air freight (5-10 days) for samples and urgent orders under 100kg. Express (7-15 days) for small packages under 30kg."}, {"q": "How do Incoterms work?", "a": "Incoterms define who pays for shipping, insurance, and customs duties. FOB (Free on Board) means you pay from the destination port. CIF includes insurance. DDP (Delivered Duty Paid) means we handle everything to your door."}, {"q": "What is a reasonable production lead time?", "a": "Standard production: 25-35 days after sample approval. Complex products or custom tooling: 45-60 days. Rush orders with factory premium: 15-20 days."}]

def generate_city(slug: str, url: str, h1: str = "") -> str:
    c = CITIES.get(slug, CITIES["shenzhen"])
    h1 = h1 or c["h1"]
    today = date.today().isoformat()
    specs_html = "".join(f"<span class=\"item-tag\">{s}</span>" for s in c["specialties"])
    trust_badges = '<div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap;margin:20px 0 24px;"><span style="background:rgba(255,255,255,.15);padding:10px 18px;border-radius:8px;font-size:13px;"><strong style="color:#FBBF24">5,000+</strong> <span style="opacity:.8">Verified Factories</span></span><span style="background:rgba(255,255,255,.15);padding:10px 18px;border-radius:8px;font-size:13px;"><strong style="color:#FBBF24">50,000+</strong> <span style="opacity:.8">Orders Done</span></span><span style="background:rgba(255,255,255,.15);padding:10px 18px;border-radius:8px;font-size:13px;"><strong style="color:#FBBF24">68</strong> <span style="opacity:.8">Countries</span></span></div>'
    city_faqs = FAQ_CITY
    faq_schema_city = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":f['q'],"acceptedAnswer":{"@type":"Answer","text":f['a']}} for f in city_faqs]}
    faq_html_city = "\n".join(f'<div class="faq-item"><div class="faq-q">{f["q"]}</div><div class="faq-a">{f["a"]}</div></div>' for f in city_faqs)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{h1} | SupplyLink</title>
  <meta name="description" content="{c["desc"]}">
  <link rel="canonical" href="{url}">
  <script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","name":"{h1}","description":"{c["desc"]}","provider":{{"@type":"Organization","name":"SupplyLink","url":"https://uscompliance-team.com"}}}}
  <script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Person","name":"David Chen","jobTitle":"Senior China Sourcing Consultant","worksFor":{{"@type":"Organization","name":"SupplyLink","url":"https://uscompliance-team.com"}},"description":"David has 12+ years of experience helping businesses source from China."}}
  </script>
  <script type="application/ld+json">
{json.dumps(faq_schema_city)}
  </script>
  <style>
    :root{{--p:#1E3A8A;--a:#2563EB;--s:#16A34A;--bg:#F8FAFC;--d:#0F172A}}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.7;color:#1E293B;background:var(--bg)}}
    .c{{max-width:1100px;margin:0 auto;padding:0 20px}}
    .hero{{background:linear-gradient(135deg,#0F172A 0%,#1E3A8A 60%,#2563EB 100%);color:white;padding:80px 0;text-align:center}}
    .hero h1{{font-size:40px;font-weight:800;margin-bottom:16px}}
    .hero p{{font-size:18px;opacity:.9;max-width:700px;margin:0 auto 32px}}
    .stats{{display:flex;gap:40px;justify-content:center;flex-wrap:wrap}}
    .stat{{text-align:center}}
    .stat .n{{font-size:30px;font-weight:800;color:#FBBF24}}
    .stat .l{{font-size:13px;opacity:.8}}
    .sec{{padding:60px 0}}
    .sec h2{{font-size:28px;font-weight:700;color:var(--d);margin-bottom:20px}}
    .sec p{{font-size:16px;color:#475569;margin-bottom:14px}}
    .specs{{background:white;border-radius:12px;padding:28px;border:1px solid #E2E8F0}}
    .row{{display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid #F1F5F9;font-size:15px}}
    .row:last-child{{border-bottom:none}}
    .items{{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}}
    .item-tag{{background:#EFF6FF;color:#1E40AF;padding:8px 18px;border-radius:20px;font-size:14px;font-weight:600}}
    .cta{{background:linear-gradient(135deg,#16A34A 0%,#15803D 100%);color:white;padding:48px 32px;border-radius:16px;text-align:center;margin:40px 0}}
    .cta h2{{color:white;margin-bottom:12px;font-size:28px}}
    .cta p{{color:rgba(255,255,255,.9);margin-bottom:24px}}
    .cta-btn{{display:inline-block;background:white;color:#16A34A;padding:14px 36px;border-radius:8px;font-weight:700;font-size:16px;text-decoration:none}}
    .footer{{text-align:center;padding:40px;color:#64748B;font-size:14px;border-top:1px solid #E2E8F0;margin-top:40px}}
    .footer a{{color:var(--a)}}
  </style>
</head>
<body>
  <div class="hero">
    <div class="c">
      <h1>{h1}</h1>
      <p>{c["desc"]}</p>
      <div class="stats">
        <div class="stat"><div class="n">50,000+</div><div class="l">Orders Processed</div></div>
        <div class="stat"><div class="n">5,000+</div><div class="l">Verified Factories</div></div>
        <div class="stat"><div class="n">120+</div><div class="l">Countries Shipped</div></div>
      </div>
    </div>
  </div>
  <div class="c">
    <section class="sec">
      <h2>Specialized Product Categories</h2>
      <div class="items">{specs_html}</div>
    </section>
    <section class="sec">
      <h2>Why Source from {slug.title()}?</h2>
      <div class="specs">
        {''.join(f'<div class="row"><span style="color:#64748B">Key Advantage</span><span style="font-weight:700;color:#0F172A">{h}</span></div>' for h in c["highlights"])}
      </div>
    </section>
    <section class="sec">
      <h2>Our {slug.title()} Sourcing Services</h2>
      <div class="specs">
        <div class="row"><span style="color:#64748B">Factory Identification</span><span style="font-weight:700;color:#0F172A">Pre-vetted manufacturers matched to your needs</span></div>
        <div class="row"><span style="color:#64748B">Quality Control</span><span style="font-weight:700;color:#0F172A">On-site inspections by certified QC professionals</span></div>
        <div class="row"><span style="color:#64748B">Price Negotiation</span><span style="font-weight:700;color:#0F172A">Local team secures competitive pricing</span></div>
        <div class="row"><span style="color:#64748B">Shipping & Logistics</span><span style="font-weight:700;color:#0F172A">End-to-end logistics including customs clearance</span></div>
        <div class="row"><span style="color:#64748B">Ongoing Support</span><span style="font-weight:700;color:#0F172A">Dedicated agent for repeat orders</span></div>
      </div>
    </section>
    <div class="cta">
      <h2>Source Products from {slug.title()}?</h2>
      <p>Get matched with verified factories within 48 hours.</p>
      {trust_badges}
      <a href="/contact.html" class="cta-btn">Get Free Quote</a>
    </div>
    <section class="sec">
      <h2>Frequently Asked Questions</h2>
      {faq_html_city}
    </section>
  </div>
  <footer class="footer">
    <p><a href="/">SupplyLink</a> | <a href="/sourcing-guide.html">Sourcing Guide</a> | <a href="/contact.html">Contact</a></p>
    <p style="margin-top:8px;">{today}</p>
  </footer>
</body>
</html>'''


def generate_service(slug: str, url: str, h1: str = "") -> str:
    s = SERVICES.get(slug, SERVICES["sourcing"])
    h1 = h1 or s["h1"]
    today = date.today().isoformat()
    steps_html = "".join(f'<div style="margin-bottom:24px;padding:20px;background:#F8FAFC;border-radius:10px;"><div style="font-weight:700;color:#1E3A8A;margin-bottom:6px;">Step {i+1}: {step[0]}</div><p style="color:#475569;font-size:15px;margin:0">{step[1]}</p></div>' for i, step in enumerate(s["steps"]))
    benefits_html = "".join(f'<span style="display:inline-block;background:#DCFCE7;color:#16A34A;padding:8px 16px;border-radius:20px;font-size:14px;font-weight:600;margin:4px;">{b}</span>' for b in s["benefits"])
    trust_badges = '<div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap;margin:20px 0 24px;"><span style="background:rgba(255,255,255,.15);padding:10px 18px;border-radius:8px;font-size:13px;"><strong style="color:#FBBF24">5,000+</strong> <span style="opacity:.8">Verified Factories</span></span><span style="background:rgba(255,255,255,.15);padding:10px 18px;border-radius:8px;font-size:13px;"><strong style="color:#FBBF24">50,000+</strong> <span style="opacity:.8">Orders Done</span></span><span style="background:rgba(255,255,255,.15);padding:10px 18px;border-radius:8px;font-size:13px;"><strong style="color:#FBBF24">68</strong> <span style="opacity:.8">Countries</span></span></div>'
    svc_faqs = FAQ_SERVICE
    faq_schema_svc = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":f['q'],"acceptedAnswer":{"@type":"Answer","text":f['a']}} for f in svc_faqs]}
    faq_html_svc = "\n".join(f'<div class="faq-item"><div class="faq-q">{f["q"]}</div><div class="faq-a">{f["a"]}</div></div>' for f in svc_faqs)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{h1} | SupplyLink</title>
  <meta name="description" content="{s["desc"]}">
  <link rel="canonical" href="{url}">
  <script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","name":"{h1}","description":"{s["desc"]}","provider":{{"@type":"Organization","name":"SupplyLink","url":"https://uscompliance-team.com"}}}}
  <script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Person","name":"David Chen","jobTitle":"Senior China Sourcing Consultant","worksFor":{{"@type":"Organization","name":"SupplyLink","url":"https://uscompliance-team.com"}},"description":"David has 12+ years of experience helping businesses source from China."}}
  </script>
  <script type="application/ld+json">
{json.dumps(faq_schema_svc)}
  </script>
  <style>
    :root{{--p:#1E3A8A;--a:#2563EB;--s:#16A34A;--bg:#F8FAFC;--d:#0F172A}}
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.7;color:#1E293B;background:var(--bg)}}
    .c{{max-width:1100px;margin:0 auto;padding:0 20px}}
    .hero{{background:linear-gradient(135deg,#0F172A 0%,#1E3A8A 60%,#2563EB 100%);color:white;padding:80px 0;text-align:center}}
    .hero h1{{font-size:40px;font-weight:800;margin-bottom:16px}}
    .hero p{{font-size:18px;opacity:.9;max-width:700px;margin:0 auto 32px}}
    .stats{{display:flex;gap:40px;justify-content:center;flex-wrap:wrap}}
    .stat{{text-align:center}}
    .stat .n{{font-size:30px;font-weight:800;color:#FBBF24}}
    .stat .l{{font-size:13px;opacity:.8}}
    .sec{{padding:60px 0}}
    .sec h2{{font-size:28px;font-weight:700;color:var(--d);margin-bottom:24px}}
    .sec p{{font-size:16px;color:#475569;margin-bottom:14px}}
    .benefits{{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0}}
    .cta{{background:linear-gradient(135deg,#16A34A 0%,#15803D 100%);color:white;padding:48px 32px;border-radius:16px;text-align:center;margin:40px 0}}
    .cta h2{{color:white;margin-bottom:12px;font-size:28px}}
    .cta p{{color:rgba(255,255,255,.9);margin-bottom:24px}}
    .cta-btn{{display:inline-block;background:white;color:#16A34A;padding:14px 36px;border-radius:8px;font-weight:700;font-size:16px;text-decoration:none}}
    .footer{{text-align:center;padding:40px;color:#64748B;font-size:14px;border-top:1px solid #E2E8F0;margin-top:40px}}
    .footer a{{color:var(--a)}}
  </style>
</head>
<body>
  <div class="hero">
    <div class="c">
      <h1>{h1}</h1>
      <p>{s["desc"]}</p>
      <div class="stats">
        <div class="stat"><div class="n">50,000+</div><div class="l">Orders Processed</div></div>
        <div class="stat"><div class="n">5,000+</div><div class="l">Verified Factories</div></div>
        <div class="stat"><div class="n">120+</div><div class="l">Countries Shipped</div></div>
      </div>
    </div>
  </div>
  <div class="c">
    <section class="sec">
      <h2>How It Works</h2>
      {steps_html}
    </section>
    <section class="sec">
      <h2>What's Included</h2>
      <div class="benefits">{benefits_html}</div>
    </section>
    <div class="cta">
      <h2>Ready to Get Started?</h2>
      <p>Contact us for a free consultation and custom quote.</p>
      {trust_badges}
      <a href="/contact.html" class="cta-btn">Get Free Quote</a>
    </div>
    <section class="sec">
      <h2>Frequently Asked Questions</h2>
      {faq_html_svc}
    </section>
  </div>
  <footer class="footer">
    <p><a href="/">SupplyLink</a> | <a href="/how-it-works.html">How It Works</a> | <a href="/contact.html">Contact</a></p>
    <p style="margin-top:8px;">{today}</p>
  </footer>
</body>
</html>'''


def generate_guide(slug: str, url: str, h1: str = "") -> str:
    g = GUIDES.get(slug, GUIDES["sourcing-guide"])
    title = h1 or g["h1"]
    today = date.today().isoformat()

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>""" + title + """ | SupplyLink</title>
  <meta name="description" content=""" + json.dumps(g["desc"]) + """>
  <link rel="canonical" href=""" + json.dumps(url) + """>
  <script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":""" + json.dumps(title) + ""","description":""" + json.dumps(g["desc"]) + ""","author":{"@context":"https://schema.org","@type":"Person","name":"David Chen","jobTitle":"Senior China Sourcing Consultant","worksFor":{"@type":"Organization","name":"SupplyLink","url":"https://uscompliance-team.com"},"description":"David has 12+ years of experience helping businesses source from China, with expertise in manufacturing, quality control, and international logistics."},"publisher":{"@type":"Organization","name":"SupplyLink","url":"https://uscompliance-team.com"},"datePublished":""" + today + ""","dateModified":""" + today + """}
  </script>
  <script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://uscompliance-team.com"},{"@type":"ListItem","position":2,"name":"Sourcing Guide","item":"https://uscompliance-team.com/sourcing-guide.html"},{"@type":"ListItem","position":3,"name":""" + json.dumps(title) + """}]}
  </script>
  <style>
    :root {--p:#1E3A8A;--a:#2563EB;--s:#16A34A;--bg:#F8FAFC;--d:#0F172A}
    * {box-sizing:border-box;margin:0;padding:0}
    body {font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.7;color:#1E293B;background:var(--bg)}
    .c {max-width:1100px;margin:0 auto;padding:0 20px}
    .hero {background:linear-gradient(135deg,#0F172A 0%,#1E3A8A 100%);color:white;padding:60px 0;text-align:center}
    .hero h1 {font-size:38px;font-weight:800;margin-bottom:16px}
    .hero p {font-size:17px;opacity:.9;max-width:650px;margin:0 auto}
    .article {max-width:750px;margin:0 auto;padding:40px 20px}
    .article h2 {font-size:24px;font-weight:700;color:#0F172A;margin:32px 0 16px}
    .article p {font-size:16px;color:#334155;margin-bottom:16px;line-height:1.8}
    .article ul {margin:0 0 16px 24px;font-size:16px;color:#334155;line-height:1.8}
    .toc {background:#EFF6FF;border-radius:12px;padding:24px;margin:32px 0}
    .toc h3 {font-size:16px;font-weight:700;color:#1E3A8A;margin-bottom:12px}
    .toc a {display:block;color:#2563EB;text-decoration:none;padding:4px 0;font-size:14px}
    .toc a:hover {text-decoration:underline}
    .cta {background:linear-gradient(135deg,#16A34A 0%,#15803D 100%);color:white;padding:40px 32px;border-radius:16px;text-align:center;margin:40px 0}
    .cta h2 {color:white;margin-bottom:12px;font-size:26px}
    .cta p {color:rgba(255,255,255,.9);margin-bottom:20px}
    .cta-btn {display:inline-block;background:white;color:#16A34A;padding:12px 32px;border-radius:8px;font-weight:700;text-decoration:none}
    .footer {text-align:center;padding:40px;color:#64748B;font-size:14px;border-top:1px solid #E2E8F0;margin-top:40px}
    .footer a {color:#2563EB}
  </style>
  <script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What is the best shipping method from China?","acceptedAnswer":{"@type":"Answer","text":"Sea freight (20-35 days) is most economical for orders over 1 cubic meter. Air freight (5-10 days) for samples and urgent orders under 100kg. Express (7-15 days) for small packages under 30kg."}},{"@type":"Question","name":"How do Incoterms work?","acceptedAnswer":{"@type":"Answer","text":"Incoterms define who pays for shipping, insurance, and customs duties. FOB (Free on Board) means you pay from the destination port. CIF includes insurance. DDP (Delivered Duty Paid) means we handle everything to your door."}},{"@type":"Question","name":"What is a reasonable production lead time?","acceptedAnswer":{"@type":"Answer","text":"Standard production: 25-35 days after sample approval. Complex products or custom tooling: 45-60 days. Rush orders with factory premium: 15-20 days."}}]}
  </script>
</head>
<body>
  <div class="hero"><div class="c"><h1>""" + title + """</h1><p>""" + g["desc"] + """</p></div></div>
  <div class="article">
    <nav class="toc">
      <h3>In This Guide</h3>
      <a href="#section1">What is China Sourcing?</a>
      <a href="#section2">Why Source from China?</a>
      <a href="#section3">How to Find Factories</a>
      <a href="#section4">Quality Control Basics</a>
      <a href="#section5">Shipping and Logistics</a>
    </nav>
    <h2 id="section1">What is China Sourcing?</h2>
    <p>China sourcing means finding and working with manufacturers based in China to produce products for your business. Whether you are launching a new product, looking for competitive pricing, or need specific manufacturing capabilities, China offers the most diverse and developed manufacturing ecosystem in the world.</p>
    <h2 id="section2">Why Source from China?</h2>
    <p>For most product categories, China remains the most competitive manufacturing destination. The advantages go beyond labor costs:</p>
    <ul>
      <li><strong>Supplier depth:</strong> Thousands of factories in each product category, from small workshops to massive modern facilities</li>
      <li><strong>Speed and flexibility:</strong> Fast production runs, rapid tooling, and low minimum order quantities available</li>
      <li><strong>Export infrastructure:</strong> Well-established logistics, customs, and trade finance networks</li>
      <li><strong>Supply chain ecosystems:</strong> Component suppliers, raw material providers, and packaging specialists clustered together</li>
    </ul>
    <h2 id="section3">How to Find Reliable Factories</h2>
    <p>Finding a genuine factory requires diligence. Request factory floor videos, verify business licenses on Chinese government databases, check import/export records, and insist on references from current buyers. Our sourcing team handles all of this verification for you.</p>
    <h2 id="section4">Quality Control Basics</h2>
    <p>Never skip quality control when sourcing from China. The cost of inspection ($150-300 per day) is always less than the cost of receiving defective goods. Use AQL (Acceptable Quality Limit) standards: AQL 2.5 for major defects, AQL 4.0 for minor defects. We provide certified inspectors in all major manufacturing cities.</p>
    <h2 id="section5">Shipping and Logistics</h2>
    <p>Choose your shipping method based on volume, urgency, and budget. Sea freight (20-35 days) is most economical for large orders. Air freight (5-10 days) for urgent or high-value shipments. Express (7-15 days, door-to-door) for samples and small orders. We handle all logistics including customs clearance.</p>
    <div class="cta">
      <h2>Need Help Sourcing from China?</h2>
      <p>Our sourcing team has verified 5,000+ factories across China. Get a free consultation.</p>
      <div style="display:flex;gap:24px;justify-content:center;flex-wrap:wrap;margin:20px 0 24px;">
        <div style="text-align:center"><div style="font-size:28px;font-weight:800;color:#FBBF24;">5,000+</div><div style="font-size:12px;opacity:.8;">Verified Factories</div></div>
        <div style="text-align:center"><div style="font-size:28px;font-weight:800;color:#FBBF24;">50,000+</div><div style="font-size:12px;opacity:.8;">Orders Completed</div></div>
        <div style="text-align:center"><div style="font-size:28px;font-weight:800;color:#FBBF24;">68</div><div style="font-size:12px;opacity:.8;">Countries Served</div></div>
        <div style="text-align:center"><div style="font-size:28px;font-weight:800;color:#FBBF24;">12+</div><div style="font-size:12px;opacity:.8;">Years Experience</div></div>
      </div>
      <a href="/contact.html" class="cta-btn">Get Free Quote</a>
    </div>
    <section style="max-width:750px;margin:0 auto;padding:40px 20px 0;">
      <h2 style="font-size:24px;font-weight:700;color:#0F172A;margin-bottom:24px;">Frequently Asked Questions</h2>
      <div style="border-bottom:1px solid #E2E8F0;padding-bottom:18px;margin-bottom:18px;"><div style="font-weight:700;color:#0F172A;font-size:15px;margin-bottom:8px;">What is the best shipping method from China?</div><div style="color:#475569;font-size:14px;line-height:1.7;">Sea freight (20-35 days) is most economical for orders over 1 cubic meter. Air freight (5-10 days) for samples and urgent orders under 100kg.</div></div>
      <div style="border-bottom:1px solid #E2E8F0;padding-bottom:18px;margin-bottom:18px;"><div style="font-weight:700;color:#0F172A;font-size:15px;margin-bottom:8px;">How do Incoterms work?</div><div style="color:#475569;font-size:14px;line-height:1.7;">Incoterms define who pays for shipping, insurance, and customs duties. FOB means you pay from destination port. DDP means we handle everything to your door.</div></div>
      <div><div style="font-weight:700;color:#0F172A;font-size:15px;margin-bottom:8px;">What is a reasonable production lead time?</div><div style="color:#475569;font-size:14px;line-height:1.7;">Standard: 25-35 days. Complex/custom tooling: 45-60 days. Rush orders: 15-20 days.</div></div>
    </section>
  </div>
  <footer class="footer">
    <p><a href="/">SupplyLink</a> | <a href="/sourcing-guide.html">Sourcing Guide</a> | <a href="/contact.html">Contact</a></p>
    <p style="margin-top:8px;">""" + today + """</p>
  </footer>
</body>
</html>"""
    return html

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Supply Chain B2B Content Generator")
    parser.add_argument("--type", required=True, choices=["product", "city", "service", "guide"])
    parser.add_argument("--slug", required=True, help="Content slug (e.g., clothing, shenzhen, sourcing)")
    parser.add_argument("--url", required=True, help="Canonical URL")
    parser.add_argument("--h1", default="", help="H1 title override")
    parser.add_argument("--output-dir", default="/root/.openclaw/workspace-crm/notebooklm_seo/output/supply-chain")
    args = parser.parse_args()

    slug = args.slug
    url = args.url
    h1 = args.h1

    generators = {
        "product": generate_product,
        "city": generate_city,
        "service": generate_service,
        "guide": generate_guide,
    }
    html = generators[args.type](slug, url, h1)

    out_dir = Path(args.output_dir) / args.type
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{slug}.html"
    out_file.write_text(html)

    manifest = {
        "type": args.type,
        "slug": slug,
        "url": url,
        "h1": h1,
        "output": str(out_file),
        "size_kb": len(html) // 1024,
    }
    manifest_file = out_dir / f"{slug}_manifest.json"
    manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    print(f"Generated: {args.type}/{slug}.html ({len(html)//1024} KB)")
    print(f"Output: {out_file}")
