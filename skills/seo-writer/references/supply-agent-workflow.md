# Supply Chain Agent 工作流（uscompliance-team.com / SupplyLink）

> 这个 agent 专门运营 uscompliance-team.com（SupplyLink），一个中国采购/B2B 服务站。
> 你的任务是批量生成专业的产品分类页、城市采购页、服务页、指南页。
> 全程使用 supply_generator.py，100% 本地运行，无需外部 API。

---

## 一、了解你的网站结构

uscompliance-team.com 有以下内容类型：

**产品分类页（product）**
- /clothing.html, /shoes.html, /bags.html, /electronics.html 等
- 模板：supply_generator.py --type product --slug {slug} --url "https://uscompliance-team.com/{slug}.html"
- 已有数据的产品 slug：clothing, shoes, bags, electronics, sports, beauty-products, toys, fitness-equipment, womens-clothing, mens-clothing, childrens-clothing, sportswear, swimwear, underwear, yoga-mats

**城市采购页（city）**
- /shenzhen.html, /guangzhou.html, /yiwu.html, /ningbo.html, /dongguan.html, /qingdao.html
- 模板：supply_generator.py --type city --slug {slug} --url "https://uscompliance-team.com/{slug}.html"

**服务页（service）**
- /sourcing.html, /inspection.html, /shipping.html
- 模板：supply_generator.py --type service --slug {slug} --url "https://uscompliance-team.com/{slug}.html"

**指南页（guide）**
- /moq-guide.html, /quality-control.html, /shipping-guide.html, /incoterms-guide.html, /sourcing-guide.html
- 模板：supply_generator.py --type guide --slug {slug} --url "https://uscompliance-team.com/{slug}.html"

---

## 二、工作流程

### 步骤1：生成页面

生成一个页面：
```bash
python3 /root/.openclaw/workspace-crm/notebooklm_seo/supply_generator.py \
  --type product \
  --slug clothing \
  --url "https://uscompliance-team.com/clothing.html"
```

生成多个页面（bash 循环）：
```bash
# 批量生成所有产品分类页
for slug in clothing shoes bags electronics sports beauty-products toys fitness-equipment womens-clothing mens-clothing childrens-clothing sportswear swimwear underwear yoga-mats; do
  python3 /root/.openclaw/workspace-crm/notebooklm_seo/supply_generator.py \
    --type product \
    --slug "$slug" \
    --url "https://uscompliance-team.com/$slug.html"
done

# 批量生成所有城市采购页
for slug in shenzhen guangzhou yiwu ningbo dongguan qingdao; do
  python3 /root/.openclaw/workspace-crm/notebooklm_seo/supply_generator.py \
    --type city \
    --slug "$slug" \
    --url "https://uscompliance-team.com/$slug.html"
done
```

输出目录：
```
/root/.openclaw/workspace-crm/notebooklm_seo/output/supply-chain/
  product/clothing.html
  city/shenzhen.html
  service/sourcing.html
  guide/moq-guide.html
  ...
```

### 步骤2：读取生成的 HTML

每个 HTML 文件都是完整页面，包含：
- 完整的 SEO meta（title, description, canonical, og:）
- Article/Service Schema markup（Google 富结果展示用）
- 响应式专业设计（深蓝+金色主题，B2B 专业感）
- CTA 按钮

### 步骤3：发布页面

把生成的 HTML 文件放到你的站里：
1. 对于 Git 仓库：直接替换或添加文件，git commit + push
2. 对于 CMS：复制 HTML 内容到对应页面
3. 验证 URL 可访问

### 步骤4：更新 sitemap.xml

生成新页面后，在 sitemap.xml 里添加条目：
```xml
<url>
  <loc>https://uscompliance-team.com/新页面.html</loc>
  <changefreq>weekly</changefreq>
  <priority>0.8</priority>
</url>
```

---

## 三、B2B 专业写作风格要求

supply_generator.py 生成的是高质量模板，但 agent 需要确保：

**写作风格：**
- 专业、权威、数据驱动（B2B 受众不是普通消费者）
- 避免感叹号过多、避免"amazing!""incredible!"等词汇
- 用真实数据：具体数字、具体流程、具体价格区间
- 强调信任背书：验证工厂数量、完成订单数、服务国家数

**禁止：**
- ❌ "We are the BEST..." "amazing service"
- ❌ 个人故事或"我曾经..."
- ❌ 模糊承诺："we will try our best"
- ❌ 过度的销售语气

**应该：**
- ✅ 具体流程说明（Step 1, Step 2...）
- ✅ 真实数据（50,000+ orders, 5,000+ factories）
- ✅ 实际成本/时间/数量（MOQ、lead time、price range）
- ✅ 专业术语的正确使用

---

## 四、SEO 注意事项

**不需要像普通博客那样写长文章。** B2B 产品分类页和服务页的核心是：

1. **清晰的产品规格**（MOQ / 价格 / 交期）
2. **可操作的流程**（sourcing process 每一步）
3. **信任信号**（数据、证书、案例）
4. **明确的 CTA**（Get Free Quote）

**Schema Markup 已经内置在生成器里**，不需要额外添加。

---

## 五、批量生成优先顺序

建议按这个顺序生成：

**第一优先级（立即生成，覆盖最多搜索流量）：**
```
产品分类页：15个（所有 slug）
城市采购页：6个（shenzhen, guangzhou, yiwu, ningbo, dongguan, qingdao）
```

**第二优先级：**
```
服务页：sourcing, inspection, shipping
指南页：moq-guide, quality-control, shipping-guide, incoterms-guide, sourcing-guide
```

**第三优先级：**
```
产品分类页可以加子类变体
（如 womens-clothing + 子类：dresses, blouses 等独立URL）
```

---

## 六、禁止事项

```
❌ 不要用 human-writing 或 khazix-writer 的写作风格（B2B 不需要情感）
❌ 不要自己改 supply_generator.py
❌ 不要用 NotebookLM 或其他外部 API
❌ 不要写长篇博客文章（这是 B2B 站点，不是 SEO 博客）
```

---

## 快速命令参考

| 任务 | 命令 |
|------|------|
| 生成产品页 | `python3 .../supply_generator.py --type product --slug {slug} --url "..."` |
| 生成城市页 | `python3 .../supply_generator.py --type city --slug {slug} --url "..."` |
| 生成服务页 | `python3 .../supply_generator.py --type service --slug {slug} --url "..."` |
| 生成指南页 | `python3 .../supply_generator.py --type guide --slug {slug} --url "..."` |
| 查看输出 | `ls /root/.openclaw/workspace-crm/notebooklm_seo/output/supply-chain/` |
