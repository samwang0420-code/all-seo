#!/usr/bin/env python3
"""
AI City Content Generator
============================
This script generates unique 150-word introductions for US cities using OpenAI API.
This helps overcome Google's "thin content" penalty by creating high-quality, 
unique content for each city page.

Usage:
    1. Set your OpenAI API key:
       export OPENAI_API_KEY="your-api-key-here"
    
    2. Run the generator:
       python ai_content_generator.py

The script will:
1. Read cities from src/data/cities.json
2. Filter cities with population >= 10,000
3. Generate unique 150-word introductions using GPT
4. Save to src/data/cities_with_ai_content.json
5. Output a JSON patch file for integration
"""

import os
import json
import time
import random
from datetime import datetime

# Try to import openai, install if needed
try:
    import openai
except ImportError:
    print("Installing openai...")
    os.system("pip install openai")
    import openai

# Configuration
INPUT_FILE = "src/data/cities.json"
OUTPUT_FILE = "src/data/cities_with_ai_content.json"
LOG_FILE = "ai_generation_log.json"
BATCH_SIZE = 10  # Cities per batch
DELAY_BETWEEN_calls = 1.5  # Seconds between API calls (rate limiting)

# City introduction prompt template
PROMPT_TEMPLATE = """Write a 150-word unique SEO-optimized introduction for {city}, {state}.

Requirements:
- Include: history, geography, economy, culture, and what makes this city special
- Make it engaging and natural, like a professional travel guide
- Include specific local details based on: Population {pop}, County {county}, Type: {city_type}
- Start with an interesting fact or hook
- Do NOT use bullet points or lists
- Do NOT repeat the same generic phrases

Write in English, engaging tone:"""

def load_cities():
    """Load cities from JSON file"""
    with open(INPUT_FILE, 'r') as f:
        cities = json.load(f)
    print(f"Loaded {len(cities)} cities")
    return cities

def filter_cities(cities, min_population=10000):
    """Filter cities by minimum population"""
    filtered = [c for c in cities if c.get('population', 0) >= min_population]
    print(f"Cities with population >= {min_population}: {len(filtered)}")
    return filtered

def generate_intro(city, api_key):
    """Generate unique introduction for a city using OpenAI API"""
    openai.api_key = api_key
    
    prompt = PROMPT_TEMPLATE.format(
        city=city['city'],
        state=city['state'],
        pop=city.get('population', 'N/A'),
        county=city.get('county', 'N/A'),
        city_type=city.get('type', 'city')
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional travel writer and SEO content expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7,
            top_p=0.9
        )
        
        intro = response.choices[0].message.content.strip()
        
        # Ensure roughly 150 words
        word_count = len(intro.split())
        if word_count < 120:
            # Too short, try again with more detail
            return None
            
        return intro
        
    except Exception as e:
        print(f"Error generating intro for {city['city']}, {city['state']}: {e}")
        return None

def generate_batch(cities, api_key, start_idx=0):
    """Generate introductions for a batch of cities"""
    results = []
    
    for i, city in enumerate(cities[start_idx:start_idx + BATCH_SIZE]):
        print(f"  [{start_idx + i + 1}] Generating for {city['city']}, {city['state']}...")
        
        intro = generate_intro(city, api_key)
        
        if intro:
            city_copy = city.copy()
            city_copy['ai_introduction'] = intro
            city_copy['intro_word_count'] = len(intro.split())
            city_copy['intro_generated_at'] = datetime.now().isoformat()
            results.append(city_copy)
            print(f"      ✓ ({len(intro.split())} words)")
        else:
            # Use fallback
            city_copy = city.copy()
            city_copy['ai_introduction'] = generate_fallback_intro(city)
            city_copy['intro_word_count'] = len(city_copy['ai_introduction'].split())
            city_copy['intro_generated_at'] = datetime.now().isoformat()
            results.append(city_copy)
            print(f"      ✗ (fallback used)")
        
        # Rate limiting
        time.sleep(DELAY_BETWEEN_calls)
    
    return results

def generate_fallback_intro(city):
    """Generate a basic fallback introduction"""
    return f"{city['city']}, {city.get('state', '')} is a {city.get('type', 'city')} located in {city.get('county', '')} County. " + \
           f"With a population of {city.get('population', 'N/A')}, " + \
           f"the city offers a unique blend of history, culture, and modern amenities. " + \
           f"Residents enjoy access to local schools, parks, and community events. " + \
           f"The city's location provides easy access to major transportation routes, " + \
           f"making it convenient for commuters and families alike."

def save_results(results, total_cities):
    """Save results to output file"""
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {len(results)} cities with AI content to {OUTPUT_FILE}")

def create_json_patch(original_file, ai_content_file):
    """Create a JSON patch to merge AI content into original data"""
    with open(original_file, 'r') as f:
        original = json.load(f)
    
    with open(ai_content_file, 'r') as f:
        ai_content = json.load(f)
    
    # Create a lookup
    ai_lookup = {
        (c['city'], c['state_abbr']): c.get('ai_introduction', '')
        for c in ai_content
    }
    
    # Add AI content to original
    for city in original:
        key = (city['city'], city['state_abbr'])
        if key in ai_lookup:
            city['ai_introduction'] = ai_lookup[key]
    
    # Save merged file
    with open(original_file, 'w') as f:
        json.dump(original, f, indent=2)
    
    print(f"Updated {original_file} with AI introductions")

def main():
    """Main function"""
    # Check for API key
    api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        print("=" * 60)
        print("OpenAI API Key Required")
        print("=" * 60)
        print("""
To generate AI content, you need an OpenAI API key:

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Set it as an environment variable:
   
   export OPENAI_API_KEY="your-key-here"

4. Run this script again

Cost estimate: ~$0.002 per city for GPT-3.5
For 3000 cities: approximately $6-10
        """)
        return
    
    print("=" * 60)
    print("AI City Content Generator")
    print("=" * 60)
    
    # Load and filter cities
    cities = load_cities()
    target_cities = filter_cities(cities, min_population=10000)
    
    print(f"\nWill generate introductions for {len(target_cities)} cities")
    print(f"Estimated cost: ~${len(target_cities) * 0.002:.2f}")
    
    # Generate in batches
    all_results = []
    for start in range(0, len(target_cities), BATCH_SIZE):
        print(f"\n--- Batch {start // BATCH_SIZE + 1} ---")
        batch_results = generate_batch(target_cities, api_key, start)
        all_results.extend(batch_results)
        
        # Save intermediate results
        save_results(all_results, len(target_cities))
    
    print("\n" + "=" * 60)
    print("Generation Complete!")
    print("=" * 60)
    print(f"Generated {len(all_results)} city introductions")
    print(f"Output: {OUTPUT_FILE}")
    
    # Ask to merge
    merge = input("\nMerge AI content into original cities.json? (y/n): ")
    if merge.lower() == 'y':
        create_json_patch(INPUT_FILE, OUTPUT_FILE)
        print(f"Updated {INPUT_FILE}")

if __name__ == "__main__":
    main()
