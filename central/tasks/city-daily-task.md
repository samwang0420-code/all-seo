# 城市站 Agent 每日任务卡

## 部署方式
Cloudflare Pages API（wrangler）

## 当前状态
- Astro 源：`/root/.openclaw/workspace-geo-all/all-seo/`
- city-data：`/root/.openclaw/workspace-crm/notebooklm_seo/output/city-data/`
- 站点：getuscompliance.com
- 现有：Astro 动态生成 7000+ 城市页，JSON-LD 含 City + GeoCoordinates + FAQPage + HowTo

## 今日任务

### 任务 1：增强城市页 Schema（已更新 [city].astro）
Astro [city].astro 中的 jsonLd 现在输出 `@type: ["City", "Place", "TouristDestination"]`
运行 Astro build：
```bash
cd /root/.openclaw/workspace-geo-all/all-seo && npm run build
```

### 任务 2：部署
```bash
export CLOUDFLARE_API_TOKEN="X-3jRM7vU05v4XKinPscNTaq66haXS_kXVm6dsaD"
export CLOUDFLARE_ACCOUNT_ID="5d298b12fa6d0f4da3cd751fed7ab2e1"
npx wrangler pages deploy dist --project-name=all-seo --commit-dirty=true
```

### 任务 3：验证
curl -s https://getuscompliance.com/city/los-angeles-ca | grep -o '"@type":"[^"]*"' | sort -u
确认输出包含 City, Place, TouristDestination
