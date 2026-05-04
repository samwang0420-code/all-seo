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

### 任务 2：部署
```bash
cd /root/.openclaw/workspace-geo-suppler/suppler-geo
export CLOUDFLARE_API_TOKEN="X-3jRM7vU05v4XKinPscNTaq66haXS_kXVm6dsaD"
export CLOUDFLARE_ACCOUNT_ID="5d298b12fa6d0f4da3cd751fed7ab2e1"
npx wrangler pages deploy . --project-name=suppler-geo --commit-dirty=true
```

### 任务 3：验证
部署后抽检 2 个产品页，确认 LocalBusiness Schema + 8 条 FAQ 完整。
