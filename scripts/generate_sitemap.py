#!/usr/bin/env python3
"""
Generate sitemap for all-seo project
"""
import json
import os

def generate_sitemap():
    domain = "https://getuscompliance.com"
    
    # Load cities
    try:
        with open('src/data/cities.json') as f:
            cities = json.load(f)
    except:
        print("No cities data found")
        return
    
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
    
    # Homepage
    sitemap += f'''
  <url>
    <loc>{domain}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>'''
    
    # Add states
    states = set(c['state'] for c in cities)
    for state in sorted(states):
        state_slug = state.lower().replace(' ', '-')
        sitemap += f'''
  <url>
    <loc>{domain}/state/{state_slug}/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>'''
    
    # Add cities (limit to 1000 to keep file size reasonable)
    for city in cities[:2000]:
        city_name = city['city'].lower().replace(' ', '-')
        state_abbr = city['state_abbr'].lower()
        sitemap += f'''
  <url>
    <loc>{domain}/city/{city_name}-{state_abbr}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>'''
    
    sitemap += '''
</urlset>'''
    
    with open('public/sitemap.xml', 'w') as f:
        f.write(sitemap)
    
    print(f"Sitemap generated with {len(states)} states and {min(len(cities), 2000)} cities")

if __name__ == "__main__":
    generate_sitemap()
