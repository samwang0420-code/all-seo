#!/bin/bash
cd /root/.openclaw/workspace-crm/notebooklm_seo

BRANDS="whirlpool GE Samsung LG Frigidaire KitchenAid Maytag Haier Amana Bosch Electrolux"
CATEGORY="dishwasher"
CODES="E1 E2 E3 E4 E5 F1 F2 F3 F6 H1 H2 OE LE1 LE2"

count=0
for brand in $BRANDS; do
  for code in $CODES; do
    python3 error_code_generator.py \
      --brand "$(echo $brand | tr '[:upper:]' '[:lower:]')" \
      --category $CATEGORY \
      --code $code \
      --model "$brand $CATEGORY" \
      --url "https://uscomplianceguard.com/error/$(echo $brand | tr '[:upper:]' '[:lower:]')/$CATEGORY/$code/" \
      --format html 2>&1
    count=$((count + 1))
  done
done
echo "Total generated: $count"
