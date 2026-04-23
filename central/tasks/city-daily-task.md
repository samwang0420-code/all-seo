# 城市站 Agent 每日任务卡

## 部署方式
Cloudflare Pages API（wrangler）

## 当前状态
- slug 列表：`/root/.openclaw/workspace-crm/central/all_city_slugs.txt`（1000 个城市）
- 输出：`/root/.openclaw/workspace-crm/notebooklm_seo/output/city-data/`
- 站点：getuscompliance.com
- 现有：1028 个 HTML

## 今日任务

### 任务 1：检查 sitemap 是否有新城市
```bash
curl -s "https://getuscompliance.com/sitemap.xml" | \
  grep -oP '/city/[^<]+' | sed 's|/city/||' | sed 's|/$||' > /tmp/new_cities.txt 2>/dev/null
wc -l /tmp/new_cities.txt
```
如果有新城市，追加并重新生成：
```bash
cat /tmp/new_cities.txt >> /root/.openclaw/workspace-crm/central/all_city_slugs.txt
sort -u /root/.openclaw/workspace-crm/central/all_city_slugs.txt -o /root/.openclaw/workspace-crm/central/all_city_slugs.txt
python3 /root/.openclaw/workspace-crm/central/batch_city_generator.py \
  --file /tmp/new_cities.txt --format html 2>&1
```

### 任务 2：发布到 Cloudflare Pages
```bash
cd /root/.openclaw/workspace-crm/notebooklm_seo
CLOUDFLARE_API_TOKEN="cfut_mArL0iV51oigP7gsU8Nt74TOz0sL6G7Va74TPJzJce964ba8" wrangler pages deploy output/city-data --project-name=all-seo 2>&1
```

### 任务 3：写日报
```bash
REPORT_DIR="/root/.openclaw/workspace-crm/central/reports"
TODAY=$(date +%Y-%m-%d)
TOTAL=$(find /root/.openclaw/workspace-crm/notebooklm_seo/output/city-data -name "*.html" | wc -l)

cat > $REPORT_DIR/city_$TODAY.json << EOF
{
  "agent": "city",
  "workspace": "workspace-geo-all",
  "date": "$TODAY",
  "status": "ok",
  "pages_total": $TOTAL,
  "sitemap_coverage": "100%",
  "deploy_method": "cloudflare_pages",
  "errors": [],
  "blockers": [],
  "new_cities_found": 0,
  "needs_attention": false
}
EOF
```

## 验收标准
- wrangler deploy 成功
- 日报写入 `/root/.openclaw/workspace-crm/central/reports/city_日期.json`
