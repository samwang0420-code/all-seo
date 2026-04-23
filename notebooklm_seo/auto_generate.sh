#!/bin/bash
# Auto Article Generator - Runs daily at 9:00 UTC
# Generates 2 SEO-optimized articles per day

DATE=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/root/.openclaw/workspace-crm/notebooklm_seo/logs/auto_gen_$(date +%Y%m%d).log"

echo "[$(date)] Starting auto article generation..." >> $LOG_FILE

# Topics to cycle through (medical aesthetics + local services)
TOPICS=(
  "Dental Implants Cost Guide 2026"
  "Invisalign vs Braces Comparison 2026"
  "Emergency HVAC Service Guide 2026"
  "CoolSculpting vs Liposuction 2026"
  "Best Med Spa Near Me Guide 2026"
  "Teeth Whitening Options 2026"
  "PRP Therapy Benefits 2026"
  "Emergency Electrician Guide 2026"
  "Dermal Fillers Lip Guide 2026"
  "HVAC Maintenance Tips 2026"
)

BLOG_DIR="/root/.openclaw/workspace/blog"
MANUSCRIPT_DIR="/root/.openclaw/workspace-crm/notebooklm_seo/manuscripts"
OUTPUT_DIR="/root/.openclaw/workspace-crm/notebooklm_seo/output"

# Get 2 random topics
for i in 1 2; do
  RANDOM_TOPIC=${TOPICS[$((RANDOM % ${#TOPICS[@]}))]}
  SLUG=$(echo "$RANDOM_TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr '/' '-')
  NOTEBOOK_NAME="${SLUG}-$(date +%Y%m%d)"
  
  echo "[$(date)] Generating article $i: $RANDOM_TOPIC" >> $LOG_FILE
  
  # Generate article markdown (template-based for now)
  mkdir -p "$MANUSCRIPT_DIR/$NOTEBOOK_NAME"
  
  # Run pipeline
  cd /root/.openclaw/workspace-crm/notebooklm_seo
  python3 content_generator.py \
    --file "$MANUSCRIPT_DIR/$NOTEBOOK_NAME/article.md" \
    --url "https://stackmatrices.com/blog/$SLUG/" \
    --notebook "$NOTEBOOK_NAME" \
    --title "$RANDOM_TOPIC" 2>&1 | tee -a $LOG_FILE
  
  # Copy to blog if generated
  OUTPUT_PATH=$(ls -td "$OUTPUT_DIR/$NOTEBOOK_NAME"*/ 2>/dev/null | head -1)
  if [ -n "$OUTPUT_PATH" ]; then
    cp "$MANUSCRIPT_DIR/$NOTEBOOK_NAME/article.md" "$BLOG_DIR/content/blog/$SLUG.md" 2>/dev/null
    cp "$OUTPUT_PATH"*.png "$BLOG_DIR/public/blog/$SLUG/" 2>/dev/null
    echo "[$(date)] Copied to blog: $SLUG.md" >> $LOG_FILE
  fi
done

# Push to GitHub
cd $BLOG_DIR
git add -A >> $LOG_FILE 2>&1
git commit -m "Auto: Daily articles $(date +%Y%m%d)" >> $LOG_FILE 2>&1
git push origin main >> $LOG_FILE 2>&1

echo "[$(date)] Completed. Pushed to GitHub." >> $LOG_FILE
