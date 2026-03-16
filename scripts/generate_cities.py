#!/usr/bin/env python3
"""
US City Data Generator & AI Content Enhancer
This script can:
1. Generate expanded city data with realistic values
2. Use OpenAI API to generate unique 150-word introductions for each city

Usage:
    python generate_cities.py              # Generate data
    OPENAI_API_KEY=your_key python generate_cities.py  # Generate + AI intros
"""

import json
import os
import time
import random

# Expanded city list with realistic US city data
CITIES_DATA = [
    # Major metros (Tier 1 - population > 1M)
    {"city": "New York", "state": "New York", "state_abbr": "NY", "county": "New York", "population": 8336817, "lat": 40.7128, "lng": -74.006, "tier": 1},
    {"city": "Los Angeles", "state": "California", "state_abbr": "CA", "county": "Los Angeles", "population": 3979576, "lat": 34.0522, "lng": -118.2437, "tier": 1},
    {"city": "Chicago", "state": "Illinois", "state_abbr": "IL", "county": "Cook", "population": 2746388, "lat": 41.8781, "lng": -87.6298, "tier": 1},
    {"city": "Houston", "state": "Texas", "state_abbr": "TX", "county": "Harris", "population": 2320268, "lat": 29.7604, "lng": -95.3698, "tier": 1},
    {"city": "Phoenix", "state": "Arizona", "state_abbr": "AZ", "county": "Maricopa", "population": 1680992, "lat": 33.4484, "lng": -112.074, "tier": 1},
    {"city": "Philadelphia", "state": "Pennsylvania", "state_abbr": "PA", "county": "Philadelphia", "population": 1584064, "lat": 39.9526, "lng": -75.1652, "tier": 1},
    {"city": "San Antonio", "state": "Texas", "state_abbr": "TX", "county": "Bexar", "population": 1547253, "lat": 29.4241, "lng": -98.4936, "tier": 1},
    {"city": "San Diego", "state": "California", "state_abbr": "CA", "county": "San Diego", "population": 1423851, "lat": 32.7157, "lng": -117.1611, "tier": 1},
    {"city": "Dallas", "state": "Texas", "state_abbr": "TX", "county": "Dallas", "population": 1343573, "lat": 32.7767, "lng": -96.797, "tier": 1},
    {"city": "San Jose", "state": "California", "state_abbr": "CA", "county": "Santa Clara", "population": 1021795, "lat": 37.3382, "lng": -121.8863, "tier": 1},
    
    # Large metros (Tier 2 - 500K-1M)
    {"city": "Austin", "state": "Texas", "state_abbr": "TX", "county": "Travis", "population": 974580, "lat": 30.2672, "lng": -97.7431, "tier": 2},
    {"city": "Jacksonville", "state": "Florida", "state_abbr": "FL", "county": "Duval", "population": 911507, "lat": 30.3322, "lng": -81.6557, "tier": 2},
    {"city": "San Francisco", "state": "California", "state_abbr": "CA", "county": "San Francisco", "population": 873965, "lat": 37.7749, "lng": -122.4194, "tier": 2},
    {"city": "Columbus", "state": "Ohio", "state_abbr": "OH", "county": "Franklin", "population": 898553, "lat": 39.9612, "lng": -82.9988, "tier": 2},
    {"city": "Fort Worth", "state": "Texas", "state_abbr": "TX", "county": "Tarrant", "population": 909585, "lat": 32.7555, "lng": -97.3308, "tier": 2},
    {"city": "Indianapolis", "state": "Indiana", "state_abbr": "IN", "county": "Marion", "population": 876862, "lat": 39.7684, "lng": -86.1581, "tier": 2},
    {"city": "Charlotte", "state": "North Carolina", "state_abbr": "NC", "county": "Mecklenburg", "population": 885708, "lat": 35.2271, "lng": -80.8431, "tier": 2},
    {"city": "Seattle", "state": "Washington", "state_abbr": "WA", "county": "King", "population": 753675, "lat": 47.6062, "lng": -122.3321, "tier": 2},
    {"city": "Denver", "state": "Colorado", "state_abbr": "CO", "county": "Denver", "population": 727211, "lat": 39.7392, "lng": -104.9903, "tier": 2},
    {"city": "Washington", "state": "District of Columbia", "state_abbr": "DC", "county": "District of Columbia", "population": 705749, "lat": 38.9072, "lng": -77.0369, "tier": 2},
    {"city": "Boston", "state": "Massachusetts", "state_abbr": "MA", "county": "Suffolk", "population": 692600, "lat": 42.3601, "lng": -71.0589, "tier": 2},
    {"city": "Nashville", "state": "Tennessee", "state_abbr": "TN", "county": "Davidson", "population": 670820, "lat": 36.1627, "lng": -86.7816, "tier": 2},
    {"city": "Detroit", "state": "Michigan", "state_abbr": "MI", "county": "Wayne", "population": 670031, "lat": 42.3314, "lng": -83.0458, "tier": 2},
    {"city": "Portland", "state": "Oregon", "state_abbr": "OR", "county": "Multnomah", "population": 654741, "lat": 45.5155, "lng": -122.6789, "tier": 2},
    {"city": "Las Vegas", "state": "Nevada", "state_abbr": "NV", "county": "Clark", "population": 651319, "lat": 36.1699, "lng": -115.1398, "tier": 2},
    {"city": "Memphis", "state": "Tennessee", "state_abbr": "TN", "county": "Shelby", "population": 650910, "lat": 35.1495, "lng": -90.049, "tier": 2},
    {"city": "Louisville", "state": "Kentucky", "state_abbr": "KY", "county": "Jefferson", "population": 617638, "lat": 38.2527, "lng": -85.7585, "tier": 2},
    {"city": "Baltimore", "state": "Maryland", "state_abbr": "MD", "county": "Baltimore", "population": 593490, "lat": 39.2904, "lng": -76.6122, "tier": 2},
    {"city": "Milwaukee", "state": "Wisconsin", "state_abbr": "WI", "county": "Milwaukee", "population": 577222, "lat": 43.0389, "lng": -87.9065, "tier": 2},
    
    # Mid-size cities (Tier 3 - 200K-500K)
    {"city": "Tucson", "state": "Arizona", "state_abbr": "AZ", "county": "Pima", "population": 548073, "lat": 32.2226, "lng": -110.9747, "tier": 3},
    {"city": "Fresno", "state": "California", "state_abbr": "CA", "county": "Fresno", "population": 531576, "lat": 36.7378, "lng": -119.7871, "tier": 3},
    {"city": "Sacramento", "state": "California", "state_abbr": "CA", "county": "Sacramento", "population": 513624, "lat": 38.5816, "lng": -121.4944, "tier": 3},
    {"city": "Mesa", "state": "Arizona", "state_abbr": "AZ", "county": "Maricopa", "population": 508958, "lat": 33.4152, "lng": -111.8315, "tier": 3},
    {"city": "Kansas City", "state": "Missouri", "state_abbr": "MO", "county": "Jackson", "population": 495327, "lat": 39.0997, "lng": -94.5786, "tier": 3},
    {"city": "Atlanta", "state": "Georgia", "state_abbr": "GA", "county": "Fulton", "population": 498715, "lat": 33.749, "lng": -84.388, "tier": 3},
    {"city": "Miami", "state": "Florida", "state_abbr": "FL", "county": "Miami-Dade", "population": 467963, "lat": 25.7617, "lng": -80.1918, "tier": 3},
    {"city": "Cleveland", "state": "Ohio", "state_abbr": "OH", "county": "Cuyahoga", "population": 381009, "lat": 41.4993, "lng": -81.6944, "tier": 3},
    {"city": "Minneapolis", "state": "Minnesota", "state_abbr": "MN", "county": "Hennepin", "population": 425403, "lat": 44.9778, "lng": -93.265, "tier": 3},
    {"city": "New Orleans", "state": "Louisiana", "state_abbr": "LA", "county": "Orleans", "population": 390144, "lat": 29.9511, "lng": -90.0715, "tier": 3},
    {"city": "Tampa", "state": "Florida", "state_abbr": "FL", "county": "Hillsborough", "population": 384959, "lat": 27.9506, "lng": -82.4572, "tier": 3},
    {"city": "Pittsburgh", "state": "Pennsylvania", "state_abbr": "PA", "county": "Allegheny", "population": 300286, "lat": 40.4406, "lng": -79.9959, "tier": 3},
    {"city": "Cincinnati", "state": "Ohio", "state_abbr": "OH", "county": "Hamilton", "population": 309317, "lat": 39.1031, "lng": -84.512, "tier": 3},
    {"city": "St. Louis", "state": "Missouri", "state_abbr": "MO", "county": "St. Louis City", "population": 300576, "lat": 38.627, "lng": -90.1994, "tier": 3},
    {"city": "Buffalo", "state": "New York", "state_abbr": "NY", "county": "Erie", "population": 255284, "lat": 42.8864, "lng": -78.8784, "tier": 3},
    {"city": "Riverside", "state": "California", "state_abbr": "CA", "county": "Riverside", "population": 330063, "lat": 33.9806, "lng": -117.3755, "tier": 3},
    {"city": "Santa Ana", "state": "California", "state_abbr": "CA", "county": "Orange", "population": 332318, "lat": 33.7455, "lng": -117.8677, "tier": 3},
    {"city": "Anaheim", "state": "California", "state_abbr": "CA", "county": "Orange", "population": 350365, "lat": 33.8366, "lng": -117.9143, "tier": 3},
    {"city": "Honolulu", "state": "Hawaii", "state_abbr": "HI", "county": "Honolulu", "population": 345064, "lat": 21.3069, "lng": -157.8583, "tier": 3},
    {"city": "Tulsa", "state": "Oklahoma", "state_abbr": "OK", "county": "Tulsa", "population": 413066, "lat": 36.154, "lng": -95.9928, "tier": 3},
    {"city": "Oklahoma City", "state": "Oklahoma", "state_abbr": "OK", "county": "Oklahoma", "population": 655057, "lat": 35.4676, "lng": -97.5164, "tier": 3},
    {"city": "Newark", "state": "New Jersey", "state_abbr": "NJ", "county": "Essex", "population": 282011, "lat": 40.7357, "lng": -74.1724, "tier": 3},
    {"city": "Lincoln", "state": "Nebraska", "state_abbr": "NE", "county": "Lancaster", "population": 291082, "lat": 40.8136, "lng": -96.7026, "tier": 3},
    {"city": "Plano", "state": "Texas", "state_abbr": "TX", "county": "Collin", "population": 287677, "lat": 33.0198, "lng": -96.6989, "tier": 3},
    {"city": "Raleigh", "state": "North Carolina", "state_abbr": "NC", "county": "Wake", "population": 474169, "lat": 35.7796, "lng": -78.6382, "tier": 3},
    {"city": "Scottsdale", "state": "Arizona", "state_abbr": "AZ", "county": "Maricopa", "population": 258069, "lat": 33.4942, "lng": -111.9261, "tier": 3},
    {"city": "Salt Lake City", "state": "Utah", "state_abbr": "UT", "county": "Salt Lake", "population": 200564, "lat": 40.7608, "lng": -111.891, "tier": 3},
    {"city": "Des Moines", "state": "Iowa", "state_abbr": "IA", "county": "Polk", "population": 214237, "lat": 41.5868, "lng": -93.625, "tier": 3},
    {"city": "Madison", "state": "Wisconsin", "state_abbr": "WI", "county": "Dane", "population": 269840, "lat": 43.0731, "lng": -89.4012, "tier": 3},
    {"city": "Wichita", "state": "Kansas", "state_abbr": "KS", "county": "Sedgwick", "population": 389877, "lat": 37.6872, "lng": -97.3301, "tier": 3},
    {"city": "Charleston", "state": "South Carolina", "state_abbr": "SC", "county": "Charleston", "population": 150388, "lat": 32.7765, "lng": -79.9311, "tier": 3},
    {"city": "Omaha", "state": "Nebraska", "state_abbr": "NE", "county": "Douglas", "population": 486051, "lat": 41.2565, "lng": -95.9345, "tier": 3},
    {"city": "Colorado Springs", "state": "Colorado", "state_abbr": "CO", "county": "El Paso", "population": 472688, "lat": 38.8339, "lng": -104.8214, "tier": 3},
    {"city": "Eugene", "state": "Oregon", "state_abbr": "OR", "county": "Lane", "population": 170245, "lat": 44.0521, "lng": -123.0868, "tier": 4},
    {"city": "Boise", "state": "Idaho", "state_abbr": "ID", "county": "Ada", "population": 235684, "lat": 43.615, "lng": -116.2023, "tier": 4},
    {"city": "Spokane", "state": "Washington", "state_abbr": "WA", "county": "Spokane", "population": 228989, "lat": 47.6588, "lng": -117.426, "tier": 4},
    {"city": "Reno", "state": "Nevada", "state_abbr": "NV", "county": "Washoe", "population": 264165, "lat": 39.5296, "lng": -119.8138, "tier": 4},
    {"city": "Ann Arbor", "state": "Michigan", "state_abbr": "MI", "county": "Washtenaw", "population": 121536, "lat": 42.2808, "lng": -83.743, "tier": 4},
    {"city": "Rochester", "state": "New York", "state_abbr": "NY", "county": "Monroe", "population": 205257, "lat": 43.1566, "lng": -77.6088, "tier": 4},
    {"city": "Knoxville", "state": "Tennessee", "state_abbr": "TN", "county": "Knox", "population": 190223, "lat": 35.9606, "lng": -83.9207, "tier": 4},
    {"city": "Shreveport", "state": "Louisiana", "state_abbr": "LA", "county": "Caddo", "population": 192036, "lat": 32.5252, "lng": -93.7502, "tier": 4},
    {"city": "Worcester", "state": "Massachusetts", "state_abbr": "MA", "county": "Worcester", "population": 185174, "lat": 42.2626, "lng": -71.8023, "tier": 4},
    {"city": "Tempe", "state": "Arizona", "state_abbr": "AZ", "county": "Maricopa", "population": 195805, "lat": 33.4255, "lng": -111.94, "tier": 4},
    {"city": "Santa Clarita", "state": "California", "state_abbr": "CA", "county": "Los Angeles", "population": 228673, "lat": 34.3917, "lng": -118.5426, "tier": 4},
    {"city": "Huntsville", "state": "Alabama", "state_abbr": "AL", "county": "Madison", "population": 215006, "lat": 34.7304, "lng": -86.5861, "tier": 4},
    {"city": "Fort Wayne", "state": "Indiana", "state_abbr": "IN", "county": "Allen", "population": 264488, "lat": 41.0793, "lng": -85.1394, "tier": 4},
    {"city": "Fayetteville", "state": "North Carolina", "state_abbr": "NC", "county": "Cumberland", "population": 211657, "lat": 35.0527, "lng": -78.8784, "tier": 4},
    {"city": "Birmingham", "state": "Alabama", "state_abbr": "AL", "county": "Jefferson", "population": 198218, "lat": 33.5186, "lng": -86.8104, "tier": 4},
    {"city": "Lubbock", "state": "Texas", "state_abbr": "TX", "county": "Lubbock", "population": 266878, "lat": 33.5779, "lng": -101.8552, "tier": 4},
    {"city": "Modesto", "state": "California", "state_abbr": "CA", "county": "Stanislaus", "population": 214221, "lat": 37.6391, "lng": -120.9969, "tier": 4},
    {"city": "Yonkers", "state": "New York", "state_abbr": "NY", "county": "Westchester", "population": 200807, "lat": 40.9312, "lng": -73.8988, "tier": 4},
    {"city": "St. George", "state": "Utah", "state_abbr": "UT", "county": "Washington", "population": 171923, "lat": 37.0965, "lng": -113.5684, "tier": 4},
    {"city": "Springfield", "state": "Missouri", "state_abbr": "MO", "county": "Greene", "population": 167882, "lat": 37.209, "lng": -93.2923, "tier": 4},
    {"city": "Laredo", "state": "Texas", "state_abbr": "TX", "county": "Webb", "population": 262495, "lat": 27.5306, "lng": -99.4803, "tier": 4},
    {"city": "Jersey City", "state": "New Jersey", "state_abbr": "NJ", "county": "Hudson", "population": 264152, "lat": 40.7178, "lng": -74.0431, "tier": 4},
    {"city": "Chandler", "state": "Arizona", "state_abbr": "AZ", "county": "Maricopa", "population": 257165, "lat": 33.3062, "lng": -111.8413, "tier": 4},
    {"city": "Irving", "state": "Texas", "state_abbr": "TX", "county": "Dallas", "population": 239798, "lat": 32.814, "lng": -96.9489, "tier": 4},
    {"city": "North Las Vegas", "state": "Nevada", "state_abbr": "NV", "county": "Clark", "population": 251974, "lat": 36.1989, "lng": -115.1175, "tier": 4},
    {"city": "Winston-Salem", "state": "North Carolina", "state_abbr": "NC", "county": "Forsyth", "population": 247945, "lat": 36.0999, "lng": -80.2442, "tier": 4},
    {"city": "Glendale", "state": "Arizona", "state_abbr": "AZ", "county": "Maricopa", "population": 249630, "lat": 33.5387, "lng": -112.186, "tier": 4},
    {"city": "Gilbert", "state": "Arizona", "state_abbr": "AZ", "county": "Maricopa", "population": 248279, "lat": 33.3528, "lng": -111.789, "tier": 4},
    {"city": "Hialeah", "state": "Florida", "state_abbr": "FL", "county": "Miami-Dade", "population": 238942, "lat": 25.8576, "lng": -80.2781, "tier": 4},
    {"city": "Garland", "state": "Texas", "state_abbr": "TX", "county": "Dallas", "population": 239928, "lat": 32.9126, "lng": -96.6389, "tier": 4},
    {"city": "Peoria", "state": "Arizona", "state_abbr": "AZ", "county": "Maricopa", "population": 175961, "lat": 33.5806, "lng": -112.2374, "tier": 4},
    {"city": "Cedar Rapids", "state": "Iowa", "state_abbr": "IA", "county": "Linn", "population": 134856, "lat": 41.9779, "lng": -91.6656, "tier": 4},
    {"city": "Davenport", "state": "Iowa", "state_abbr": "IA", "county": "Scott", "population": 101724, "lat": 41.5236, "lng": -90.5776, "tier": 4},
    {"city": "Fort Lauderdale", "state": "Florida", "state_abbr": "FL", "county": "Broward", "population": 182437, "lat": 26.1224, "lng": -80.1373, "tier": 4},
    {"city": "St. Petersburg", "state": "Florida", "state_abbr": "FL", "county": "Pinellas", "population": 265351, "lat": 27.7676, "lng": -82.6403, "tier": 4},
    {"city": "Corpus Christi", "state": "Texas", "state_abbr": "TX", "county": "Nueces", "population": 326554, "lat": 27.8006, "lng": -97.3964, "tier": 4},
    {"city": "Newport News", "state": "Virginia", "state_abbr": "VA", "county": "Newport News", "population": 179225, "lat": 37.0871, "lng": -76.473, "tier": 4},
    {"city": "Chesapeake", "state": "Virginia", "state_abbr": "VA", "county": "Chesapeake", "population": 249822, "lat": 36.7682, "lng": -76.2875, "tier": 4},
    {"city": "Akron", "state": "Ohio", "state_abbr": "OH", "county": "Summit", "population": 197882, "lat": 41.0814, "lng": -81.519, "tier": 4},
    {"city": "Albuquerque", "state": "New Mexico", "state_abbr": "NM", "county": "Bernalillo", "population": 560218, "lat": 35.0844, "lng": -106.6504, "tier": 3},
    {"city": "Bridgeport", "state": "Connecticut", "state_abbr": "CT", "county": "Fairfield", "population": 144399, "lat": 41.1865, "lng": -73.1952, "tier": 4},
    {"city": "Springfield", "state": "Massachusetts", "state_abbr": "MA", "county": "Hampden", "population": 155929, "lat": 42.1015, "lng": -72.5898, "tier": 4},
    {"city": "Salem", "state": "Oregon", "state_abbr": "OR", "county": "Marion", "population": 177219, "lat": 44.9429, "lng": -123.0351, "tier": 4},
    {"city": "El Paso", "state": "Texas", "state_abbr": "TX", "county": "El Paso", "population": 682669, "lat": 31.7619, "lng": -106.485, "tier": 3},
    {"city": "Anchorage", "state": "Alaska", "state_abbr": "AK", "county": "Anchorage", "population": 291247, "lat": 61.2181, "lng": -149.9003, "tier": 4},
    {"city": "Fremont", "state": "California", "state_abbr": "CA", "county": "Alameda", "population": 237238, "lat": 37.5485, "lng": -121.9886, "tier": 4},
    {"city": "Santa Rosa", "state": "California", "state_abbr": "CA", "county": "Sonoma", "population": 177586, "lat": 38.4404, "lng": -122.7141, "tier": 4},
    {"city": "Ontario", "state": "California", "state_abbr": "CA", "county": "San Bernardino", "population": 175265, "lat": 34.0633, "lng": -117.6509, "tier": 4},
    {"city": "Vancouver", "state": "Washington", "state_abbr": "WA", "county": "Clark", "population": 186192, "lat": 45.6387, "lng": -122.6615, "tier": 4},
    {"city": "Cape Coral", "state": "Florida", "state_abbr": "FL", "county": "Lee", "population": 194016, "lat": 26.5629, "lng": -81.9495, "tier": 4},
    {"city": "Sioux Falls", "state": "South Dakota", "state_abbr": "SD", "county": "Minnehaha", "population": 192517, "lat": 43.546, "lng": -96.7313, "tier": 4},
    {"city": "Port St. Lucie", "state": "Florida", "state_abbr": "FL", "county": "St. Lucie", "population": 201846, "lat": 27.273, "lng": -80.3582, "tier": 4},
    {"city": "Providence", "state": "Rhode Island", "state_abbr": "RI", "county": "Providence", "population": 190934, "lat": 41.824, "lng": -71.4128, "tier": 4},
    {"city": "Chattanooga", "state": "Tennessee", "state_abbr": "TN", "county": "Hamilton", "population": 180557, "lat": 35.0458, "lng": -85.3097, "tier": 4},
    {"city": "New Orleans", "state": "Louisiana", "state_abbr": "LA", "county": "Orleans", "population": 390144, "lat": 29.9511, "lng": -90.0715, "tier": 3},
]

def generate_realistic_data(city):
    """Generate realistic economic/demographic data based on city tier and location"""
    pop = city['population']
    state = city['state_abbr']
    tier = city['tier']
    
    # Base values
    base_rent = 1200
    base_home = 300000
    
    # Adjust by population tier
    if tier == 1:
        multiplier = random.uniform(1.8, 2.5)
    elif tier == 2:
        multiplier = random.uniform(1.2, 1.8)
    elif tier == 3:
        multiplier = random.uniform(0.9, 1.2)
    else:
        multiplier = random.uniform(0.6, 0.9)
    
    # Adjust by state
    state_multipliers = {
        'CA': 2.0, 'NY': 1.9, 'WA': 1.7, 'MA': 1.6, 'CO': 1.5,
        'FL': 1.3, 'TX': 1.2, 'AZ': 1.2, 'NV': 1.1, 'UT': 1.1,
        'GA': 1.0, 'NC': 1.0, 'IL': 1.0, 'OH': 0.9, 'MO': 0.9,
        'TN': 0.9, 'IN': 0.88, 'WI': 0.87, 'IA': 0.85, 'KS': 0.85,
        'NE': 0.85, 'OK': 0.82, 'AR': 0.80, 'KY': 0.80, 'AL': 0.78,
        'HI': 1.8, 'NJ': 1.6, 'CT': 1.5, 'MD': 1.4, 'VA': 1.3,
        'OR': 1.3, 'ID': 1.1, 'NM': 0.95, 'SC': 0.95, 'LA': 0.85,
        'SD': 0.8, 'ND': 0.8, 'WV': 0.75, 'MS': 0.75, 'MT': 0.8,
        'WY': 0.8, 'ME': 0.85, 'NH': 0.95, 'VT': 0.9, 'RI': 1.2,
        'DE': 1.1, 'PA': 1.0,
    }
    state_mult = state_multipliers.get(state, 1.0)
    
    median_rent = int(base_rent * multiplier * state_mult * (pop / 500000) ** 0.3)
    median_home = int(base_home * multiplier * state_mult * (pop / 500000) ** 0.3)
    median_income = int(median_rent * 32 + random.randint(10000, 30000))
    crime_index = random.randint(20, 85)
    median_age = random.randint(28, 45)
    livability_score = round(10 - (crime_index / 25) + (multiplier * 0.3), 1)
    livability_score = max(5.0, min(9.5, livability_score))
    
    # City type
    city_types = {
        'CA': 'tech hub', 'WA': 'tech hub', 'NY': 'metropolis', 'MA': 'historic city',
        'FL': 'coastal city', 'TX': 'major city