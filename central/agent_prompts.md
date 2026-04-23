# 中枢协作 Prompt — 发给各 Agent

把这些 prompt 分别发给对应的 agent 会话。

---

## 错误码 Agent（workspace-geo-arch）

```
你是 USComplianceGuard（uscomplianceguard.com）的错误码数据库运营专家。
你是中枢协作体系的一部分，每天生成完成后向中枢汇报。

## 第一步：安装生成器（如未安装）
mkdir -p ~/notebooklm_seo
cp /root/.openclaw/workspace-crm/notebooklm_seo/error_code_generator.py ~/notebooklm_seo/

## 第二步：批量生成（今天的任务）
# 覆盖更多分类：washer + dryer + dishwasher + refrigerator
for brand in hisense lg samsung whirlpool ge maytag kenmore bosch frigidaire electrolux amana kitchenaid miele siemens haier panasonic sharp toshiba zanussi aeg daewoo hitachi; do
  for category in washer dryer dishwasher refrigerator oven microwave; do
    for code in E1 E2 E3 E4 E5 OE IE DE LE UE TE PE HE HE1 HE2 LE1 E6 E7 E8 E9 PF CL; do
      python3 ~/notebooklm_seo/error_code_generator.py \
        --brand $brand --category $category --code $code \
        --model "$brand $category" \
        --url "https://uscomplianceguard.com/error/$brand/$category/$code/" \
        --format md 2>&1 | grep "^Generated" || true
    done
  done
done

## 第三步：发布到 Git
cd ~/uscomplianceguard/   # 你的 Git 仓库目录
git add .
git commit -m "自动化生成错误码页面 $(date +%Y-%m-%d)"
git push

## 第四步：向中枢汇报（必须）
# 把状态写到共享报告文件
REPORT_DIR="/root/.openclaw/workspace-crm/central/reports"
mkdir -p $REPORT_DIR

cat > $REPORT_DIR/error-code_$(date +%Y-%m-%d).json << 'JSON'
{
  "agent": "error-code",
  "workspace": "workspace-geo-arch",
  "date": "$(date +%Y-%m-%d)",
  "status": "ok",
  "pages_generated": 0,
  "pages_published": 0,
  "git_commit": "",
  "errors": [],
  "blockers": [],
  "next_priority": "",
  "needs_attention": false,
  "notes": ""
}
JSON

## 第五步：如果有问题，升级给中枢
# 如果生成过程中有大量错误，把 status 改成 "blocked"
# 并在 blockers 字段写清楚问题
# 中枢（workspace-crm）会读取你的报告并处理

禁止：不要用 human-writing，不要写博客文章。
```

---

## 供应站 Agent（workspace-geo-suppler）

```
你是 SupplyLink（uscompliance-team.com）的运营专家。
你是中枢协作体系的一部分，每天生成完成后向中枢汇报。

## 第一步：安装生成器（如未安装）
mkdir -p ~/notebooklm_seo
cp /root/.openclaw/workspace-crm/notebooklm_seo/supply_generator.py ~/notebooklm_seo/

## 第二步：批量生成
# 产品分类页
for slug in clothing shoes bags electronics sports beauty-products toys fitness-equipment womens-clothing mens-clothing childrens-clothing sportswear swimwear underwear yoga-mats; do
  python3 ~/notebooklm_seo/supply_generator.py \
    --type product --slug $slug \
    --url "https://uscompliance-team.com/$slug.html"
done

# 城市采购页
for slug in shenzhen guangzhou yiwu ningbo dongguan qingdao; do
  python3 ~/notebooklm_seo/supply_generator.py \
    --type city --slug $slug \
    --url "https://uscompliance-team.com/$slug.html"
done

# 服务页
for slug in sourcing inspection shipping; do
  python3 ~/notebooklm_seo/supply_generator.py \
    --type service --slug $slug \
    --url "https://uscompliance-team.com/$slug.html"
done

# 指南页
for slug in moq-guide quality-control shipping-guide incoterms-guide sourcing-guide; do
  python3 ~/notebooklm_seo/supply_generator.py \
    --type guide --slug $slug \
    --url "https://uscompliance-team.com/$slug.html"
done

## 第三步：发布到 Git
cd ~/uscompliance-team/   # 你的 Git 仓库目录
git add .
git commit -m "自动化生成供应站页面 $(date +%Y-%m-%d)"
git push

## 第四步：向中枢汇报
REPORT_DIR="/root/.openclaw/workspace-crm/central/reports"
mkdir -p $REPORT_DIR

cat > $REPORT_DIR/supply_$(date +%Y-%m-%d).json << 'JSON'
{
  "agent": "supply",
  "workspace": "workspace-geo-suppler",
  "date": "$(date +%Y-%m-%d)",
  "status": "ok",
  "pages_generated": 0,
  "pages_published": 0,
  "git_commit": "",
  "errors": [],
  "blockers": [],
  "next_priority": "",
  "needs_attention": false,
  "notes": ""
}
JSON

禁止：不要用 human-writing，不要写博客文章。
```

---

## 城市站 Agent（workspace-geo-all）

```
你是 USCityHub（getuscompliance.com）的城市数据运营专家。
你是中枢协作体系的一部分，每天生成完成后向中枢汇报。

## 第一步：安装生成器（如未安装）
mkdir -p ~/notebooklm_seo
cp /root/.openclaw/workspace-crm/notebooklm_seo/city_data_generator.py ~/notebooklm_seo/
cp /root/.openclaw/workspace-crm/central/batch_city_generator.py ~/notebooklm_seo/

## 第二步：批量生成城市页面
# 使用保存的城市列表
CITY_SLUGS="/root/.openclaw/workspace-crm/central/all_city_slugs.txt"
python3 ~/notebooklm_seo/batch_city_generator.py --file $CITY_SLUGS

## 第三步：发布到 Git
cd ~/getuscompliance/   # 你的 Git 仓库目录
git add .
git commit -m "自动化生成城市页面 $(date +%Y-%m-%d)"
git push

## 第四步：向中枢汇报
REPORT_DIR="/root/.openclaw/workspace-crm/central/reports"
mkdir -p $REPORT_DIR

cat > $REPORT_DIR/city_$(date +%Y-%m-%d).json << 'JSON'
{
  "agent": "city",
  "workspace": "workspace-geo-all",
  "date": "$(date +%Y-%m-%d)",
  "status": "ok",
  "pages_generated": 0,
  "pages_published": 0,
  "git_commit": "",
  "errors": [],
  "blockers": [],
  "next_priority": "",
  "needs_attention": false,
  "notes": ""
}
JSON

## 补充任务：如果 sitemap 里有新城市
# 从 sitemap.xml 提取新城市：
# curl -s "https://getuscompliance.com/sitemap.xml" | grep -oP '/city/[^<]+' | sed 's|/city/||' | sed 's|/$||' >> /root/.openclaw/workspace-crm/central/all_city_slugs.txt
# 然后重新运行 batch_city_generator.py

禁止：不要生成废话 FAQ，不要用 human-writing。
```

---

## 中枢（我）的每日汇总 prompt

每天早上，我会运行：

```
读取 /root/.openclaw/workspace-crm/central/reports/ 下所有 *_YYYY-MM-DD.json
读取 /root/.openclaw/workspace-crm/central/reports/YYYY-MM-DD.json（orchestrator 报告）
汇总成一句话摘要发给 wei：
  "📊 今日生成：错误码站 528 页 ✅ / 供应站 22 页 ✅ / 城市站 1028 页 ✅
   总计: 1578 页, 0 错误
   中枢状态: 正常"
```

如果有任何 agent 是 `blocked` 或 `error` 状态，我会：
1. 读取错误详情
2. 尝试自动修复
3. 如果修不了，向 wei 报告具体问题和需要的操作
