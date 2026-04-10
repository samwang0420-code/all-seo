#!/usr/bin/env node
/**
 * Generate neighborhood pages for major cities
 */

import fs from 'fs';
import path from 'path';

const neighborhoodsFile = '../data/neighborhoods/usneighborhoods.csv';
const outputDir = './src/pages/neighborhood';

// Read neighborhoods CSV
const content = fs.readFileSync(neighborhoodsFile, 'utf-8');
const lines = content.trim().split('\n');
const headers = lines[0].split(',').map(h => h.replace(/"/g, ''));

// Group neighborhoods by city
const neighborhoodsByCity = {};

for (let i = 1; i < lines.length; i++) {
  const values = lines[i].split(',').map(v => v.replace(/"/g, ''));
  const row = {};
  headers.forEach((h, idx) => row[h] = values[idx] || '');
  
  const cityKey = `${row.city_name}-${row.state_name}`;
  if (!neighborhoodsByCity[cityKey]) {
    neighborhoodsByCity[cityKey] = {
      city: row.city_name,
      state: row.state_name,
      neighborhoods: []
    };
  }
  
  // Sanitize name for URL - replace / with -, remove other problematic chars
  const sanitizedName = row.neighborhood.replace(/\//g, '-').replace(/[^a-zA-Z0-9\s-]/g, '');
  
  neighborhoodsByCity[cityKey].neighborhoods.push({
    name: row.neighborhood,
    url_name: sanitizedName.toLowerCase().replace(/\s+/g, '-'),
    lat: parseFloat(row.lat),
    lng: parseFloat(row.lng),
    zips: row.zips,
    county: row.county_name,
    id: row.id
  });
}

console.log(`Found ${Object.keys(neighborhoodsByCity).length} cities with neighborhoods`);

// Generate neighborhoods data JSON
const neighborhoodsData = {
  cities: neighborhoodsByCity,
  generated: new Date().toISOString()
};

fs.writeFileSync('./src/data/neighborhoods.json', JSON.stringify(neighborhoodsData, null, 2));
console.log('Written src/data/neighborhoods.json');

// Show breakdown
Object.entries(neighborhoodsByCity).forEach(([key, data]) => {
  console.log(`  ${key}: ${data.neighborhoods.length} neighborhoods`);
});
