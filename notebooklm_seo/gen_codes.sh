#!/bin/bash
cd /root/.openclaw/workspace-crm/notebooklm_seo
for category in refrigerator oven microwave; do
  for brand in whirlpool GE Samsung LG Frigidaire KitchenAid Maytag Haier Amana Bosch Electrolux; do
    for code in E1 E2 E3 E4 E5 F1 F2 F3 H1 H2 OE1 OE2; do
      python3 error_code_generator.py \
        --brand "$(echo $brand | tr '[:upper:]' '[:lower:]')" \
        --category $category \
        --code $code \
        --model "$brand $category" \
        --url "https://uscomplianceguard.com/error/$(echo $brand | tr '[:upper:]' '[:lower:]')/$category/$code/" \
        --format html 2>&1
    done
  done
done
