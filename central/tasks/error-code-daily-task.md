# 错误码站 Agent 每日任务卡

## 部署方式
GitHub → Cloudflare Pages（Next.js 构建）

## 当前状态
- 站点：uscomplianceguard.com
- 输出：`/root/.openclaw/workspace-crm/notebooklm_seo/output/error-codes/`
- 现有：1082 个 HTML 错误码页面
- 新增：13 个品牌索引页（/brand/kitchenaid/ 等）+ 6 个品类索引页

## 今日任务

### 任务 1：检查文件是否就绪
brand 索引页：`notebooklm_seo/output/brand/*/index.html`（13 个）
category 索引页：`notebooklm_seo/output/category/*.html`（6 个）

### 任务 2：触发部署
推送到 GitHub，Cloudflare Pages 自动构建。

### 任务 3：验证内链
部署后抽检 3 个错误码页，确认 /brand/X/ 和 /category/Y/ 不再 404。
