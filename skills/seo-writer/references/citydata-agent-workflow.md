# City Data Agent 工作流（getuscompliance.com）

> 这个 agent 专门运营 getuscompliance.com（USCityHub），一个美国城市数据站。
> 你的任务是批量生成/优化城市页面，确保 FAQ 答案具体有用，不是废话。

---

## 核心问题

城市页面的核心问题：**FAQ 答案全是废话**
- "New York is a city known for its unique character" ❌
- 正确："New York is a major metropolitan city known for being the financial capital of the US..." ✅

city_data_generator.py 会生成完整的、FAQ 答案具体的城市页面。

---

## URL 格式

```
/city/new-york-ny/
/city/los-angeles-ca/
/city/chicago-il/
```

---

## 工作流程

### 步骤1：确定要生成/更新的城市

优先处理 sitemap 中已有页面但 FAQ 答案质量差的城市。

常用高流量城市（优先生成）：
```
New York NY, Los Angeles CA, Chicago IL, Houston TX, Phoenix AZ,
Philadelphia PA, San Antonio TX, San Diego CA, Dallas TX, San Jose CA,
Austin TX, Jacksonville FL, Fort Worth TX, Columbus OH, Indianapolis IN,
Charlotte NC, San Francisco CA, Seattle WA, Denver CO, Washington DC,
Boston MA, Nashville TN, Baltimore MD, Oklahoma City OK, Louisville KY,
Portland OR, Las Vegas NV, Milwaukee WI, Albuquerque NM, Tucson AZ,
Atlanta GA, Miami FL, Boston MA, Brooklyn NY, Queens NY, Manhattan NY
```

### 步骤2：生成城市页面

**生成一个城市：**
```bash
python3 /root/.openclaw/workspace-crm/notebooklm_seo/city_data_generator.py \
  --city "Buffalo" \
  --state NY \
  --url "https://getuscompliance.com/city/buffalo-ny" \
  --population "255,284" \
  --median-home "$238,000" \
  --median-rent "$1,450" \
  --median-income "$48,000" \
  --crime-index "35" \
  --livability "7.4" \
  --format both
```

**批量生成多个城市（用 bash 循环）：**
```bash
CITIES="New York:NY:8537673:$1074000:Chicago:IL:2693976:$309000:Los Angeles:CA:3979576:$679000"

echo "$CITIES" | tr ':' '\n' | while read city && read state && read pop && read home; do
  python3 /root/.openclaw/workspace-crm/notebooklm_seo/city_data_generator.py \
    --city "$city" --state "$state" \
    --url "https://getuscompliance.com/city/$(echo $city | tr '[:upper:]' '[:lower:]')-$(echo $state | tr '[:upper:]' '[:lower:]')" \
    --population "$pop" --median-home "$home" \
    --crime-index "40" --livability "7.5" \
    --format html
done
```

### 步骤3：获取真实数据

数据来源（按优先级）：
1. **Wikipedia** - 城市简介、人口、地理信息
2. **Census Bureau** - 人口、收入、房价中位数
3. **City-Data.com** - 详细统计
4. **Crime Index** - 找当地治安数据

如果某个数据点找不到，生成器会自动填充合理估算值。

### 步骤4：发布页面

把生成的 HTML 文件放到 Git 仓库对应路径，提交 + push。

### 步骤5：验证

用 Google Rich Results Test 验证 FAQ Schema：
https://search.google.com/test/rich-results

---

## FAQ 质量标准

❌ 禁止（废话 FAQ）：
- "New York is a city known for its unique character and attractions."
- "The population is [number]. Population is [number]."

✅ 必须（具体 FAQ）：
- "New York is a major metropolitan city known for being the financial capital of the US..."
- "Buffalo is a mid-sized city in NY, known for its affordable cost of living and proximity to Niagara Falls..."

---

## ### 快速批量生成：全部城市

**使用批量生成器（推荐）：**
```bash
# 城市 slug 列表已保存在:
# /root/.openclaw/workspace-crm/central/all_city_slugs.txt
# 共 1000 个城市 URL

python3 /root/.openclaw/workspace-crm/central/batch_city_generator.py \
  --file /root/.openclaw/workspace-crm/central/all_city_slugs.txt
```
预计：~15 分钟生成 1000 页（无网络调用，全本地）。

### 第二优先：高搜索量城市

全美前 500 个人口最多的城市优先。

### 第三优先：其他城市

按需生成或更新。

---

## 禁止事项

```
❌ 不要生成"New York is a city known for its unique character"这种废话 FAQ
❌ 不要用 human-writing / khazix-writer（B2B 数据站不需要情感写作）
❌ 不要自己改 city_data_generator.py
❌ 不要用 NotebookLM 或外部 API（生成器自己抓 Wikipedia/OSM 数据）
❌ 不要生成无意义的通用 FAQ
```

---

## 快速命令

| 任务 | 命令 |
|------|------|
| 生成城市页 | `python3 .../city_data_generator.py --city "X" --state XX --url "..." --population "X" --median-home "X"` |
| 查看输出 | `ls /root/.openclaw/workspace-crm/notebooklm_seo/output/city-data/` |

---

## FAQ 问题清单（每个城市必须有这8个）

每个生成的城市页必须包含这8个 FAQ：

1. What is {city}, {state} known for?
2. What is the population of {city}, {state}?
3. Is {city}, {state} safe?
4. What is the cost of living in {city}, {state}?
5. What is the weather like in {city}, {state}?
6. How did {city}, {state} get its name?
7. What industries drive {city}, {state}'s economy?
8. What are the best neighborhoods in {city}, {state}?
