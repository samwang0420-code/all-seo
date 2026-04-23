#!/usr/bin/env python3
"""城市站 Place+GeoCoordinates+TouristDestination 补丁 v5"""
import json, re
from pathlib import Path

DIR = Path("/root/.openclaw/workspace-crm/notebooklm_seo/output/city-data")

STATE_COORDS = {
    "AL":(32.8067,-86.7911),"AK":(61.3707,-152.4044),"AZ":(33.7298,-111.4312),
    "AR":(34.9697,-92.3731),"CA":(36.1162,-119.6816),"CO":(39.0598,-105.3111),
    "CT":(41.5978,-72.7554),"DE":(39.3185,-75.5071),"FL":(27.7663,-81.6868),
    "GA":(33.0406,-83.6431),"HI":(21.0943,-157.4983),"ID":(44.2405,-114.4788),
    "IL":(40.3495,-88.9861),"IN":(39.8494,-86.2583),"IA":(42.0115,-93.2105),
    "KS":(38.5266,-96.7265),"KY":(37.6681,-84.6701),"LA":(31.1695,-91.8678),
    "ME":(44.6939,-69.3819),"MD":(39.0639,-76.8021),"MA":(42.2302,-71.5301),
    "MI":(43.3266,-84.5361),"MN":(45.6945,-93.9002),"MS":(32.7416,-89.6787),
    "MO":(38.4561,-92.2884),"MT":(46.9219,-110.4544),"NE":(41.1254,-98.2681),
    "NV":(38.3135,-117.0554),"NH":(43.4525,-71.5639),"NJ":(40.2989,-74.5210),
    "NM":(34.8405,-106.2485),"NY":(42.1657,-74.9481),"NC":(35.6301,-79.8064),
    "ND":(47.5289,-99.7840),"OH":(40.3888,-82.7649),"OK":(35.5653,-96.9289),
    "OR":(44.5720,-122.0709),"PA":(39.9526,-75.1652),"RI":(41.6809,-71.5118),
    "SC":(33.8569,-80.9450),"SD":(45.2730,-99.9017),"TN":(35.7478,-86.6923),
    "TX":(31.0545,-97.5635),"UT":(40.1500,-111.8624),"VT":(44.0459,-72.7107),
    "VA":(37.7693,-78.1700),"WA":(47.4009,-121.4905),"WV":(38.4912,-80.9545),
    "WI":(44.2685,-89.6165),"WY":(42.7560,-107.3025),"DC":(38.9072,-77.0369),
    "PR":(18.2208,-66.5901),"VI":(18.3358,-64.8963),"GU":(13.4443,144.7937),
}

CITY_COORDS = {
    "new-york":(40.7128,-74.0060),"los-angeles":(34.0522,-118.2437),
    "chicago":(41.8781,-87.6298),"houston":(29.7604,-95.3698),
    "phoenix":(33.4484,-112.0740),"philadelphia":(39.9526,-75.1652),
    "san-antonio":(29.4241,-98.4936),"san-diego":(32.7157,-117.1611),
    "dallas":(32.7767,-96.7970),"san-jose":(37.3382,-121.8863),
    "austin":(30.2672,-97.7431),"jacksonville":(30.3322,-81.6557),
    "fort-worth":(32.7555,-97.3308),"columbus":(39.9612,-82.9988),
    "charlotte":(35.2271,-80.8431),"san-francisco":(37.7749,-122.4194),
    "indianapolis":(39.7684,-86.1581),"seattle":(47.6062,-122.3321),
    "denver":(39.7392,-104.9903),"washington":(38.9072,-77.0369),
    "boston":(42.3601,-71.0589),"nashville":(36.1627,-86.7816),
    "detroit":(42.3314,-83.0458),"portland":(45.5152,-122.6784),
    "las-vegas":(36.1699,-115.1398),"memphis":(35.1495,-90.0490),
    "louisville":(38.2527,-85.7585),"baltimore":(39.2904,-76.6122),
    "milwaukee":(43.0389,-87.9065),"albuquerque":(35.0844,-106.6504),
    "tucson":(32.2226,-110.9747),"fresno":(36.7378,-119.7871),
    "sacramento":(38.5816,-121.4944),"mesa":(33.4152,-111.8315),
    "kansas-city":(39.0997,-94.5786),"atlanta":(33.7490,-84.3880),
    "colorado-springs":(38.8339,-104.8214),"miami":(25.7617,-80.1918),
    "raleigh":(35.7796,-78.6382),"omaha":(41.2565,-95.9345),
    "long-beach":(33.7701,-118.1937),"virginia-beach":(36.8529,-75.9780),
    "oakland":(37.8044,-122.2712),"minneapolis":(44.9778,-93.2650),
    "tulsa":(36.1540,-95.9928),"tampa":(27.9506,-82.4572),
    "new-orleans":(29.9511,-90.0715),"wichita":(37.6872,-97.3301),
    "cleveland":(41.4993,-81.6944),"bakersfield":(35.3733,-119.0187),
    "stockton":(37.9577,-121.2908),"corpus-christi":(27.8006,-97.3964),
    "anchorage":(61.2181,-149.9003),"reno":(39.5296,-119.8138),
    "scottsdale":(33.4942,-111.9261),"chandler":(33.3063,-111.8413),
    "tacoma":(47.2529,-122.4453),"santa-clarita":(34.3917,-118.5426),
    "lubbock":(33.5779,-101.8552),"madison":(43.0731,-89.4012),
    "durham":(36.0010,-78.9382),"orlando":(28.5383,-81.3792),
    "richmond":(37.5407,-77.4360),"fort-lauderdale":(26.1224,-80.1373),
    "jersey-city":(40.7178,-74.0431),"st-petersburg":(27.7676,-82.6403),
    "laredo":(27.5306,-99.4805),"boise":(43.6150,-116.2023),
    "birmingham":(33.5207,-86.8025),"norfolk":(36.8508,-76.2859),
    "san-bernardino":(34.1083,-117.2898),"spokane":(47.6588,-117.4260),
    "baton-rouge":(30.4515,-91.1871),"modesto":(37.6391,-120.9969),
    "des-moines":(41.5868,-93.6250),"port-st-lucie":(27.2730,-80.3582),
    "huntsville":(34.7304,-86.5861),"chattanooga":(35.0456,-85.3097),
    "tempe":(33.4255,-111.9400),"arlington-ca":(33.8031,-118.0817),
    "arlington-27-tx":(32.7357,-97.1081),"arlington-tx":(32.7357,-97.1081),
    "arlington-va":(38.8786,-77.1043),"glendale-az":(33.5387,-112.1859),
    "fayetteville-nc":(35.0527,-78.8784),"arlington":(38.8786,-77.1043),
}

STATE_NAME_TO_POSTAL = {
    "alabama":"AL","alaska":"AK","arizona":"AZ","arkansas":"AR","california":"CA",
    "colorado":"CO","connecticut":"CT","delaware":"DE","florida":"FL","georgia":"GA",
    "hawaii":"HI","idaho":"ID","illinois":"IL","indiana":"IN","iowa":"IA",
    "kansas":"KS","kentucky":"KY","louisiana":"LA","maine":"ME","maryland":"MD",
    "massachusetts":"MA","michigan":"MI","minnesota":"MN","mississippi":"MS","missouri":"MO",
    "montana":"MT","nebraska":"NE","nevada":"NV","new-hampshire":"NH","new-jersey":"NJ",
    "new-mexico":"NM","new-york":"NY","north-carolina":"NC","north-dakota":"ND","ohio":"OH",
    "oklahoma":"OK","oregon":"OR","pennsylvania":"PA","rhode-island":"RI","south-carolina":"SC",
    "south-dakota":"SD","tennessee":"TN","texas":"TX","utah":"UT","vermont":"VT",
    "virginia":"VA","washington":"WA","west-virginia":"WV","wisconsin":"WI","wyoming":"WY",
    "dc":"DC","puerto-rico":"PR","guam":"GU","virgin-islands":"VI",
}

def slug_to_coords(slug: str) -> tuple:
    slug_dash = slug.lower()
    if slug_dash in CITY_COORDS:
        return CITY_COORDS[slug_dash]
    for state in STATE_COORDS:
        for sep in ['-', '_']:
            suffix = sep + state.lower()
            if slug_dash.endswith(suffix):
                prefix = slug_dash[:-len(suffix)]
                if prefix in CITY_COORDS:
                    return CITY_COORDS[prefix]
    for state, sc in STATE_COORDS.items():
        for sep in ['-', '_']:
            if slug_dash.endswith(sep + state.lower()):
                return sc
    return STATE_COORDS["KS"]

def get_state(fp: Path) -> str:
    parts = fp.parts
    if len(parts) >= 2:
        st = parts[-2].lower()
        if st.upper() in STATE_COORDS:
            return st.upper()
        if st in STATE_NAME_TO_POSTAL:
            return STATE_NAME_TO_POSTAL[st]
    return "CA"

def extract_city_name(slug: str) -> str:
    name = slug.replace("-", " ").replace("_", " ").title()
    for state in STATE_COORDS:
        for sep in [' ', '-', '_']:
            suf = sep + state
            if name.endswith(suf):
                name = name[:-len(suf)].strip()
                break
    return name

def find_matching_brace(text: str, start: int) -> int:
    """Given text starting with '{', find the index of the matching '}'"""
    depth = 0
    i = start
    while i < len(text):
        c = text[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i
        elif c == '"':
            # Skip string
            i += 1
            while i < len(text):
                if text[i] == '\\':
                    i += 2
                elif text[i] == '"':
                    break
                i += 1
        i += 1
    return -1

def get_schema_types_in_block(script_content: str) -> list:
    """Extract all @type values from a JSON-LD script block content using string search"""
    types = []
    content = script_content.strip()
    # Find all "@type": "Value" occurrences
    for m in re.finditer(r'"@type"\s*:\s*"([^"]+)"', content):
        types.append(m.group(1))
    return types

def remove_old_place_schemas(html: str) -> str:
    """Remove all <script type="application/ld+json"> blocks containing Place or TouristDestination"""
    result = []
    pos = 0
    while True:
        start_tag = html.find('<script type="application/ld+json">', pos)
        if start_tag == -1:
            result.append(html[pos:])
            break
        result.append(html[pos:start_tag])
        end_tag = html.find('</script>', start_tag)
        if end_tag == -1:
            result.append(html[start_tag:])
            break
        script_block = html[start_tag:end_tag + 9]
        script_content = html[start_tag + len('<script type="application/ld+json">'):end_tag]
        types = get_schema_types_in_block(script_content)
        if not any(t in ('Place', 'TouristDestination') for t in types):
            result.append(script_block)
        pos = end_tag + 9
    return ''.join(result)

def build_injection(city_name: str, state: str, lat: float, lng: float) -> str:
    place = {
        "@context": "https://schema.org", "@type": "Place",
        "name": f"{city_name}, {state.upper()}",
        "address": {"@type": "PostalAddress", "addressLocality": city_name,
                    "addressRegion": state.upper(), "addressCountry": {"@type": "Country", "name": "US"}},
        "geo": {"@type": "GeoCoordinates", "latitude": round(lat, 4), "longitude": round(lng, 4)}
    }
    tourist = {
        "@context": "https://schema.org", "@type": "TouristDestination",
        "name": f"{city_name}, {state.upper()}",
        "description": f"Travel guide and local information for {city_name}, {state.upper()}. Discover attractions, cost of living, and visitor resources.",
        "geo": {"@type": "GeoCoordinates", "latitude": round(lat, 4), "longitude": round(lng, 4)}
    }
    def j(s): return json.dumps(s, separators=(',', ':'))
    return (f'\n  <script type="application/ld+json">\n{j(place)}\n  </script>\n'
            f'  <script type="application/ld+json">\n{j(tourist)}\n  </script>\n  ')

def patch_file(fp: Path) -> bool:
    html = fp.read_text(errors='ignore')
    slug = fp.stem
    city_name = extract_city_name(slug)
    state = get_state(fp)
    lat, lng = slug_to_coords(slug)

    # Step 1: remove existing Place/TouristDestination schemas
    html = remove_old_place_schemas(html)

    # Step 2: inject new schemas before FAQPage
    injection = build_injection(city_name, state, lat, lng)
    faqpage_pos = html.find('FAQPage')
    if faqpage_pos == -1:
        return False
    script_start = html.rfind('<script type="application/ld+json">', 0, faqpage_pos)
    if script_start == -1:
        return False

    html = html[:script_start] + injection + html[script_start:]
    fp.write_text(html)
    return True

def main():
    files = list(DIR.glob("**/*.html"))
    print(f"Found {len(files)} HTML files")
    ok = err = skip = 0
    for fp in files:
        try:
            if patch_file(fp):
                ok += 1
            else:
                skip += 1
        except Exception as e:
            err += 1
            print(f"  ERROR {fp.relative_to(DIR)}: {e}")
    print(f"✅ Done: {ok} patched, {skip} skipped (no FAQPage), {err} errors")

if __name__ == "__main__":
    main()
