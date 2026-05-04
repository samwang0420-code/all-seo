# 供应站 Agent 每日任务卡

## 部署方式
Cloudflare Pages API

## 当前状态
- 输出：`/root/.openclaw/workspace-crm/notebooklm_seo/output/supply-chain/`
- 站点：uscompliance-team.com
- 现有：73 个产品页 + 6 个中国城市页
- Schema：LocalBusiness + Shipping FAQ（全量注入）

## 今日任务

### 任务 1：检查文件是否就绪
- 73 个产品页（LocalBusiness + Shipping FAQ）
- 6 个城市页（深圳/广州/义乌/宁波/东莞/青岛）

### 任务 2：触发部署
同步到 `workspace-geo-suppler/suppler-geo/`，使用 Cloudflare Pages API 部署。

### 任务 3：验证
部署后抽检 2 个产品页，确认 LocalBusiness Schema + 8 条 FAQ 完整。
