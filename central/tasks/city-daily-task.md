# 城市站 Agent 每日任务卡

## 部署方式
Cloudflare Pages API

## 当前状态
- 输出：`/root/.openclaw/workspace-crm/notebooklm_seo/output/city-data/`
- 站点：getuscompliance.com
- 现有：26 州，1028 个城市页
- Schema：Place + TouristDestination + GeoCoordinates（全量注入）

## 今日任务

### 任务 1：检查 city-data 是否就绪
文件已在 `/root/.openclaw/workspace-crm/notebooklm_seo/output/city-data/`，包含：
- 26 个州目录（ak, al, ar, ... wy）
- 每个城市：.html + .md + _manifest.json
- Schema 已注入（Place/TouristDestination/GeoCoordinates）

### 任务 2：触发部署
使用 Cloudflare Pages API 或 wrangler 部署更新内容。

### 任务 3：验证
部署后抽检 3 个城市页，确认 Schema 完整。
