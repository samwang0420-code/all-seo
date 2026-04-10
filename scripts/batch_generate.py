#!/usr/bin/env python3
"""
Batch City Generator
Usage: python batch_generate.py --target 12000
"""

import json
import random
import argparse
import os

def generate_cities(target_count):
    """Generate cities to reach target count"""
    
    # Load existing
    try:
        with open('src/data/cities.json', 'r') as f:
            existing = json.load(f)
    except:
        existing = []
    
    current = len(existing)
    if current >= target_count:
        print(f"Already have {current} cities, target is {target_count}. Nothing to do.")
        return
    
    need = target_count - current
    print(f"Current: {current}, Target: {target_count}, Need: {need}")
    
    # State data
    states = [
        ("Alabama", "AL", 0.78), ("Alaska", "AK", 1.3), ("Arizona", "AZ", 1.2), ("Arkansas", "AR", 0.80),
        ("California", "CA", 2.0), ("Colorado", "CO", 1.5), ("Connecticut", "CT", 1.5), ("Delaware", "DE", 1.1),
        ("Florida", "FL", 1.3), ("Georgia", "GA", 1.0), ("Hawaii", "HI", 1.8), ("Idaho", "ID", 1.1),
        ("Illinois", "IL", 1.0), ("Indiana", "IN", 0.88), ("Iowa", "IA", 0.85), ("Kansas", "KS", 0.85),
        ("Kentucky", "KY", 0.80), ("Louisiana", "LA", 0.85), ("Maine", "ME", 0.85), ("Maryland", "MD", 1.4),
        ("Massachusetts", "MA", 1.6), ("Michigan", "MI", 0.95), ("Minnesota", "MN", 0.95), ("Mississippi", "MS", 0.75),
        ("Missouri", "MO", 0.90), ("Montana", "MT", 0.80), ("Nebraska", "NE", 0.85), ("Nevada", "NV", 1.1),
        ("New Hampshire", "NH", 0.95), ("New Jersey", "NJ", 1.6), ("New Mexico", "NM", 0.95), ("New York", "NY", 1.9),
        ("North Carolina", "NC", 1.0), ("North Dakota", "ND", 0.80), ("Ohio", "OH", 0.90), ("Oklahoma", "OK", 0.82),
        ("Oregon", "OR", 1.3), ("Pennsylvania", "PA", 1.0), ("Rhode Island", "RI", 1.2), ("South Carolina", "SC", 0.95),
        ("South Dakota", "SD", 0.80), ("Tennessee", "TN", 0.90), ("Texas", "TX", 1.2), ("Utah", "UT", 1.1),
        ("Vermont", "VT", 0.90), ("Virginia", "VA", 1.3), ("Washington", "WA", 1.7), ("West Virginia", "WV", 0.75),
        ("Wisconsin", "WI", 0.87), ("Wyoming", "WY", 0.80),
    ]
    
    name_patterns = [
        "Springfield", "Franklin", "Clinton", "Madison", "Washington", "Georgetown", "Manchester",
        "Bristol", "Greenville", "Salem", "Fairview", "Chester", "Oak Grove", "Riverdale",
        "Highland", "Midway", "Jackson", "Marion", "Clayton", "Porter", "Lebanon", "Ashland",
        "Winchester", "Burlington", "Newport", "Auburn", "Hudson", "Kingston", "Milton",
    ]
    
    suffixes = ["City", "Town", "Village", "Heights", "Park", "Valley", "Springs", "Fields", "Gardens"]
    
    # Track used names per state
    used = {}
    for c in existing:
        key = (c['city'], c['state_abbr'])
        used[key] = True
    
    new_cities = []
    state_idx = 0
    
    while len(new_cities) < need:
        state_name, state_abbr, cost_mult = states[state_idx % len(states)]
        
        # Generate unique name
        for attempt in range(100):
            base = random.choice(name_patterns)
            suf = random.choice(suffixes)
            
            if attempt % 3 == 0:
                name = base
            elif attempt % 3 == 1:
                name = f"{base} {suf}"
            else:
                name = f"New {base}"
            
            key = (name, state_abbr)
            if key not in used:
                break
        
        used[key] = True
        
        # Generate data
        pop = random.randint(500, 50000)
        tier = 5 if pop < 2500 else 4 if pop < 10000 else 3
        
        mult2 = {1: 2.0, 2: 1.4, 3: 1.0, 4: 0.7, 5: 0.5}.get(tier, 1)
        
        median_rent = int(1000 * mult2 * cost_mult * (max(pop,100)/10000)**0.15)
        median_home = int(250000 * mult2 * cost_mult * (max(pop,100)/10000)**0.15)
        median_income = int(median_rent * 28 + random.randint(3000, 15000))
        crime_index = random.randint(15, 80)
        median_age = random.randint(28, 55)
        livability = round(10 - crime_index/20 + cost_mult*0.15 + random.uniform(-0.3, 0.3), 1)
        livability = max(4.0, min(9.5, livability))
        
        lat = random.uniform(25, 48)
        lng = random.uniform(-125, -66)
        
        city = {
            "city": name, "state": state_name, "state_abbr": state_abbr,
            "county": f"{state_name} County", "population": pop, "lat": round(lat, 4),
            "lng": round(lng, 4), "median_rent": median_rent, "median_home_value": median_home,
            "median_income": median_income, "crime_index": crime_index, "median_age": median_age,
            "livability_score": livability, "type": "city",
            "zip_codes": str(random.randint(10000, 99999)), "tier": tier,
            "ai_introduction": f"{name} is a charming community in {state_name}."
        }
        
        new_cities.append(city)
        
        if len(new_cities) % 1000 == 0:
            print(f"  Generated {len(new_cities)}/{need}...")
        
        state_idx += 1
    
    # Merge
    all_cities = existing + new_cities
    
    # Save
    with open('src/data/cities.json', 'w') as f:
        json.dump(all_cities, f, indent=2)
    
    print(f"\nDone! Total cities: {len(all_cities)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, required=True, help="Target total cities")
    args = parser.parse_args()
    
    generate_cities(args.target)
