# SEO Agent 完整工作流（v2 - 本地 Pipeline，无需外部 API）

> **核心变化：完全放弃 NotebookLM，不再有认证过期问题。**
> 所有内容由 `content_generator.py` 本地生成，100% 稳定。

---

## 完整工作流（8步）

### 第0步：填品牌信息卡（只做一次）
```
在 workspace 创建 BRAND.md：
- 站点名称
- 目标读者
- 品牌调性
- 核心话题方向
- 禁止词汇
```

### 第1步：写文章

```
规则（按顺序执行）：
1. /root/.openclaw/skills/seo-writer/SKILL.md
2. /root/.openclaw/skills/seo-writer/references/seo-writing-guide.md
3. /root/.openclaw/skills/human-writing/references/anti-ai-patterns.md
4. /root/.openclaw/skills/khazix-writer/SKILL.md

要求：1500-3000字，60%真实案例/数据，禁止AI词汇，禁止堆砌bullet list
```

### 第2步：发布文章
```
用你自己的方式发布（git push / API / CMS）
获得正式 URL：https://你的站.com/blog/文章slug/
```

### 第3步：保存 Markdown
```
路径：/root/.openclaw/workspace-crm/notebooklm_seo/manuscripts/{你的notebook名}/article.md

示例：
mkdir -p /root/.openclaw/workspace-crm/notebooklm_seo/manuscripts/jianfacv-interviews
把文章内容写入 article.md
```

### 第4步：运行本地 Pipeline

```bash
python3 /root/.openclaw/workspace-crm/notebooklm_seo/content_generator.py \
  --file "/root/.openclaw/workspace-crm/notebooklm_seo/manuscripts/{notebook名}/article.md" \
  --url "https://你的站.com/blog/文章slug/" \
  --notebook "{notebook名}" \
  --title "文章标题"
```

**这次不需要 NotebookLM，不需要 cookies，不需要任何外部认证。**

### 第5步：等待生成完成
```
预计 10-30 秒，全部在本地生成：
✅ schema-article.jsonld（Article 结构化数据）
✅ schema-faq.jsonld（FAQ 结构化数据）
✅ schema-breadcrumb.jsonld（面包屑结构化数据）
✅ chart-comparison.png（对比图表）
✅ infographic.png（信息图）
✅ quiz.html（可交互 Quiz）
✅ internal-links.json（内链建议）
```

### 第6步：读取输出清单
```
路径：/root/.openclaw/workspace-crm/notebooklm_seo/output/{notebook名}/{文章标题}_{时间戳}/
manifest 文件：_manifest.json（包含所有生成文件的路径）
```

### 第7步：把内容嵌回文章

#### 7a. Schema Markup（最重要，必须做）
把以下 JSON-LD 嵌入文章页面 `<head>` 或 `<body>` 的 `<script type="application/ld+json">` 标签内：

```html
<!-- 从输出目录读取这三个文件，合并到一个 <script type="application/ld+json"> 标签 -->
<script type="application/ld+json">
// schema-article.jsonld 的内容
</script>
<script type="application/ld+json">
// schema-faq.jsonld 的内容
</script>
<script type="application/ld+json">
// schema-breadcrumb.jsonld 的内容
</script>
```

#### 7b. 信息图
把 `infographic.png` 嵌入文章内容里（`<figure>` 或 `<img>` 标签）：

```html
<figure>
  <img src="/images/infographic.png" alt="Article Infographic" loading="lazy">
  <figcaption>Key insights from this guide</figcaption>
</figure>
```

#### 7c. Quiz（可选但推荐）
把 `quiz.html` 的全部内容嵌入文章里（在 `</article>` 标签之前）：

```html
<!-- 直接把 quiz.html 的内容复制进去 -->
```

#### 7d. 对比图表
把 `chart-comparison.png` 也嵌入文章：

```html
<figure>
  <img src="/images/chart-comparison.png" alt="Comparison Chart" loading="lazy">
  <figcaption>Performance comparison</figcaption>
</figure>
```

### 第8步：提交
```
1. 提交所有文件到 Git 仓库
2. 等待 Cloudflare Pages 部署
3. 用 Google Rich Results Test 验证 Schema 是否生效：
   https://search.google.com/test/rich-results
```

---

## 禁止事项

```
❌ 不要运行 notebooklm_seo/pipeline.py（已废弃）
❌ 不要运行 notebooklm_seo/queue_task.py（已废弃）
❌ 不要尝试登录 NotebookLM
❌ 不要用 @generate quiz 之类的 NotebookLM 参数
```

---

## 常见问题

**Q: content_generator.py 报 matplotlib 错误**
A: matplotlib 已安装，无需额外操作。图表警告可以忽略。

**Q: 生成的 Quiz 题目不够准确**
A: 这是正常的。Quiz 是从文章内容自动提取关键词生成的，不是 AI 智能出题。价值在于互动性，不在于题目精准度。

**Q: Schema 怎么验证？**
A: 用 Google Rich Results Test: https://search.google.com/test/rich-results
输入文章 URL，看有没有 Article 和 FAQ 的富卡片。

---

## 文件路径速查

| 用途 | 路径 |
|------|------|
| 本地 Pipeline | `/root/.openclaw/workspace-crm/notebooklm_seo/content_generator.py` |
| 保存文章 | `/root/.openclaw/workspace-crm/notebooklm_seo/manuscripts/{notebook}/` |
| 读取输出 | `/root/.openclaw/workspace-crm/notebooklm_seo/output/{notebook}/{标题}_{时间戳}/` |
| Schema 文件 | `schema-article.jsonld` + `schema-faq.jsonld` + `schema-breadcrumb.jsonld` |
| 图表文件 | `chart-comparison.png` + `infographic.png` |
| Quiz | `quiz.html` |
| 内链建议 | `internal-links.json` |
