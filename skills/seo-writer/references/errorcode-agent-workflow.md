# Error Code Agent 工作流（uscomplianceguard.com）

> 这个 agent 专门运营 uscomplianceguard.com，一个错误码数据库站。
> 你的任务是批量生成 4000+ 错误码详情页。
> 全程使用 error_code_generator.py，100% 本地运行，无需外部 API。

---

## 你的网站结构

uscomplianceguard.com 有以下 URL 格式：

```
错误码详情页：/error/{brand}/{category}/{code}/
品牌索引页：  /brand/{brand}/
分类索引页：  /category/{category}/
品牌列表：   /brand/{brand}/
```

**支持的品牌（30+）：**
hisense, lg, samsung, whirlpool, ge, maytag, kenmore, bosch, frigidaire, electrolux, amana, kitchenaid, miele, siemens, haier, panasonic, sharp, toshiba, zanussi, aeg, daewoo, hitachi, viking, Jenn-air, westinghouse, paykel, fisher, blomberg, candy, etc.

**支持的分类：**
washer, dryer, dishwasher, refrigerator, oven, microwave, hvac, car, electric-vehicle, plc, cnc, robotics

---

## 核心工作流

### 步骤1：批量生成错误码页面

**生成一个页面：**
```bash
python3 /root/.openclaw/workspace-crm/notebooklm_seo/error_code_generator.py \
  --brand hisense \
  --category washer \
  --code E3 \
  --model "Hisense Front Load Washer" \
  --url "https://uscomplianceguard.com/error/hisense/washer/e3/" \
  --difficulty medium \
  --diy false \
  --format both
```

**批量生成某个品牌+分类的所有代码：**
```bash
# Hisense Washer 全部错误码
for code in E1 E2 E3 E4 E5 OE IE DE LE UE tE PE HE HE1 HE2 LE1 E6 E7 E8 E9 PF CL 0E FE DE1; do
  python3 /root/.openclaw/workspace-crm/notebooklm_seo/error_code_generator.py \
    --brand hisense \
    --category washer \
    --code $code \
    --model "Hisense Washer" \
    --url "https://uscomplianceguard.com/error/hisense/washer/$code/" \
    --format both 2>&1 | grep -v "^$"
done
```

**批量生成某个品牌所有分类：**
```bash
# LG 全部分类
for category in washer dryer dishwasher refrigerator oven microwave; do
  for code in E1 E2 E3 E4 E5 OE IE DE LE UE tE PE HE HE1 HE2 LE1 E6 E7 E8 E9 PF CL 0E FE DE1; do
    python3 /root/.openclaw/workspace-crm/notebooklm_seo/error_code_generator.py \
      --brand lg --category $category --code $code \
      --model "LG $category" \
      --url "https://uscomplianceguard.com/error/lg/$category/$code/" \
      --format md 2>&1 | grep -v "^$"
  done
done
```

### 步骤2：发布页面

把生成的 HTML/Markdown 文件放到你的 Git 仓库里。

**每个品牌+分类输出目录：**
```
/root/.openclaw/workspace-crm/notebooklm_seo/output/error-codes/{brand}/{category}/
  E1.html, E1.md, E1_manifest.json
  E2.html, E2.md, E2_manifest.json
  ...
```

### 步骤3：更新 sitemap.xml

每个新页面在 sitemap.xml 加一条：
```xml
<url>
  <loc>https://uscomplianceguard.com/error/{brand}/{category}/{code}/</loc>
  <changefreq>weekly</changefreq>
  <priority>0.7</priority>
</url>
```

---

## 批量生成策略

### 第一优先级：覆盖已有品牌

sitemap 显示已经有以下品牌分类页，先把主要品牌的 washer/dryer 填满：
```
brand/hisense/        ← 45 codes
brand/lg/             ← 已有
brand/samsung/         ← 已有
brand/whirlpool/       ← 已有
brand/ge/             ← 已有
brand/bosch/          ← 已有
brand/maytag/         ← 已有
brand/kenmore/        ← 已有
```

每个品牌 washer + dryer = ~25 个错误码 × 8 品牌 = 200 个页面

### 第二优先级：扩展到 dishwasher/refrigerator

每个分类 × 所有品牌 = 大量页面

### 第三优先级：处理 404 错误码 URL

sitemap.xml 显示有 `/error/hisense/washer/e3/` 格式，
但实际页面 404。需要生成这些页面填上。

---

## 错误码自动识别规则

error_code_generator.py 内置了 30+ 标准错误码含义。
如果某个 code 不在内置库里，生成器会自动用通用模板。

**常见错误码速查（不用搜，生成器自动处理）：**

| Code | 含义 | DIY? |
|------|------|------|
| E1 / IE | 水位/进水错误 | 简单 |
| E2 / OE / 0E | 排水错误 | 简单 |
| E3 | 水位传感器错误 | 需专业 |
| E4 / DE | 门锁错误 | 简单 |
| E5 / tE | 温度传感器错误 | 需专业 |
| F1 | 电机错误 | 需专业 |
| F2 | 控制板错误 | 需专业 |
| LE / LE1 | 电机锁死错误 | 需专业 |
| UE | 不平衡负载 | 简单 |
| HE / HE1 / HE2 | 加热错误 | 需专业 |
| PF | 电源故障 | 简单 |
| CL | 儿童锁 | 简单 |

---

## 禁止事项

```
❌ 不要用 human-writing / khazix-writer（错误码页不需要情感写作）
❌ 不要写长篇博客文章（这是数据库，每个错误码只需结构化内容）
❌ 不要自己改 error_code_generator.py
❌ 不要用 NotebookLM 或外部 API
❌ 不要生成无意义的 FAQ（FAQ 要围绕这个具体的错误码）
```

---

## 快速批量命令

**全部品牌 × washer × 25个代码：**
```bash
BRANDS="hisense lg samsung whirlpool ge maytag kenmore bosch frigidaire electrolux amana kitchenaid miele siemens haier panasonic sharp toshiba zanussi aeg daewoo hitachi"
CODES="E1 E2 E3 E4 E5 OE IE DE LE UE tE PE HE HE1 HE2 LE1 E6 E7 E8 E9 PF CL 0E FE DE1"

for brand in $BRANDS; do
  for code in $CODES; do
    python3 /root/.openclaw/workspace-crm/notebooklm_seo/error_code_generator.py \
      --brand $brand --category washer --code $code \
      --model "$brand washer" \
      --url "https://uscomplianceguard.com/error/$brand/washer/$code/" \
      --format md 2>&1 | grep "^Generated"
  done
done
```

---

## 输出路径

所有生成文件：
```
/root/.openclaw/workspace-crm/notebooklm_seo/output/error-codes/{brand}/{category}/
```
