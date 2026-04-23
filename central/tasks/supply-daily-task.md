# 供应站 Agent 每日任务卡

## 部署方式
Cloudflare Pages API（wrangler）

## 当前状态
- 生成器：`/root/.openclaw/workspace-crm/notebooklm_seo/supply_generator.py`
- 输出：`/root/.openclaw/workspace-crm/notebooklm_seo/output/supply-chain/`
- 站点：uscompliance-team.com
- 现有：78 个 HTML

## 今日任务

### 任务 1：扩展子类页面
```bash
cd /root/.openclaw/workspace-crm/notebooklm_seo

python3 << 'PYEOF'
import supply_generator
from pathlib import Path

OUT = Path("output/supply-chain")
OUT.mkdir(parents=True, exist_ok=True)

SUBCLASSES = [
    ("dresses", "Dresses Sourcing from China"),
    ("jackets", "Jackets & Outerwear Sourcing"),
    ("pants", "Pants & Trousers Manufacturing"),
    ("activewear", "Activewear & Sportswear Sourcing"),
    ("smartphones", "Smartphone Sourcing from China"),
    ("tablets", "Tablet & iPad Sourcing"),
]

for slug, h1 in SUBCLASSES:
    html = supply_generator.generate_product(slug, f"https://uscompliance-team.com/product/{slug}/", h1=h1)
    (OUT / f"{slug}.html").write_text(html)
    print(f"Generated: {slug}.html")

print(f"Done: {len(SUBCLASSES)} pages")
PYEOF
```

### 任务 2：发布到 Cloudflare Pages
```bash
cd /root/.openclaw/workspace-crm/notebooklm_seo
CLOUDFLARE_API_TOKEN="cfut_mArL0iV51oigP7gsU8Nt74TOz0sL6G7Va74TPJzJce964ba8" wrangler pages deploy output/supply-chain --project-name=suppler-geo 2>&1
```

### 任务 3：写日报
```bash
REPORT_DIR="/root/.openclaw/workspace-crm/central/reports"
TODAY=$(date +%Y-%m-%d)
TOTAL=$(find /root/.openclaw/workspace-crm/notebooklm_seo/output/supply-chain -name "*.html" | wc -l)

cat > $REPORT_DIR/supply_$TODAY.json << EOF
{
  "agent": "supply",
  "workspace": "workspace-geo-suppler",
  "date": "$TODAY",
  "status": "ok",
  "pages_total": $TOTAL,
  "deploy_method": "cloudflare_pages",
  "errors": [],
  "blockers": [],
  "needs_attention": false
}
EOF
```

## 验收标准
- 页面生成成功
- wrangler deploy 成功
- 日报写入 `/root/.openclaw/workspace-crm/central/reports/supply_日期.json`
