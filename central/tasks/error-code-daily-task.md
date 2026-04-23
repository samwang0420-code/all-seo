# 错误码站 Agent 每日任务卡

## 部署方式
GitHub（Cloudflare Pages 的 Next.js 构建会处理）

## 当前状态
- 站点：uscomplianceguard.com
- 现有：3036 个 TSX 页面（已全部修复格式）

## 今日任务

### 任务 1：生成 + 推送（一条命令搞定）
```bash
cd /root/.openclaw/workspace-geo-arch/error-code-hub
bash scripts/daily-error-pages.sh
```

这个脚本会：
1. 生成所有 brand × category × code 组合（3036 页）
2. 修复 TSX 格式（每行分开，TypeScript 编译器能识别）
3. 更新 sitemap.xml
4. Git push 到 GitHub（触发 Cloudflare Pages 自动构建）
5. 写入日报到 `/root/.openclaw/workspace-crm/central/reports/error-code_日期.json`

## 验收标准
- GitHub push 成功（Cloudflare Pages 自动构建完成）
- 日报写入 `/root/.openclaw/workspace-crm/central/reports/error-code_日期.json`
