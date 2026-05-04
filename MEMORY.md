# MEMORY.md — Long-term memory

## Who I Am
- **Name:** 小p 🦞
- **Role:** 多站点 SEO 内容引擎中枢 agent（Openclaw）
- **Manager:** Wei (@SamuelDenk, Telegram)

## The Three Sites
| 站 | Domain | Content | Agent |
|---|---|---|---|
| 错误码站 | uscomplianceguard.com | ErrorCodeHub — 家电错误码数据库 | geo-arch |
| 供应站 | uscompliance-team.com | SupplyLink — 中国采购/B2B | geo-suppler |
| 城市站 | getuscompliance.com | USCityHub — 美国城市数据 | geo-all |

## Deployment
- 所有站点通过 Cloudflare Pages 部署（非 git push）
- 各 agent 独立运行，中枢（我）只管文件层
- CF API token 藏在 `all-seo/scripts/auto_update.sh`（`X-3jRM7vU05v4XKinPscNTaq66haXS_kXVm6dsaD`）
- CF Account ID：`5d298b12fa6d0f4da3cd751fed7ab2e1`
- 部署命令：`CLOUDFLARE_API_TOKEN=X TOKEN CLOUDFLARE_ACCOUNT_ID=ID npx wrangler pages deploy dist --project-name=NAME --commit-dirty=true`
- 文件同步路径：
  - 城市站 GEO → `workspace-geo-all/all-seo/`（Astro rebuild 后 CF deploy）
  - 供应站 GEO → `workspace-geo-suppler/suppler-geo/`
  - 错误码站内链 → `workspace-geo-arch/notebooklm_seo/output/brand/`, `category/`

## SEO Pipeline
- Generator: `notebooklm_seo/` — NotebookLM API 驱动
- Batch: `bash` → Git commit
- Output dirs: `notebooklm_seo/output/{error-codes,supply-chain,city-data}/`
- 每个 site 有一个独立 workspace（geo-all/arch/suppler）

## Key Scripts (workspace-crm/central/)
- `patch_supply_final.py` — 供应站 LocalBusiness + Shipping FAQ
- `patch_city_schemas_v5.py` — 城市站 Place + TouristDestination + GeoCoordinates
- `build_errorcode_indexes.py` — 错误码站品牌+品类索引页

## Lessons Learned
- 城市坐标匹配：不能只匹配城市名，要精确到 "city-state" slug（Arlington-CA/TX bug）
- JSON Schema 截断：括号匹配比简单找 `}` 更可靠
- FAQ 答案截断：流式生成需等完整 body 再解析
- Cloudflare Pages：无 git remote 时直接 API 部署，不本地 build
