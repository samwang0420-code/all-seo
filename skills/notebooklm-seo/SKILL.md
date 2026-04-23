---
name: notebooklm-seo
description: |
  将 SEO 文章 URL 自动上传到 NotebookLM，生成 Audio Overview / Quiz / 闪卡 / 信息图 / 报告，
  打包成完整内容包。用于 SEO agent 写完文章后自动触发内容生成流水线。
  触发方式：将任务写入 queue 目录，由 pipeline 自动执行。
---

# NotebookLM SEO Pipeline Skill

SEO agent 使用此 skill 将文章上传到 NotebookLM 并生成配套内容。

## 触发方式

### 方式一：直接调用（立即执行）

```bash
python3 /root/.openclaw/workspace-crm/notebooklm_seo/pipeline.py \
  --url "https://example.com/seo-article" \
  --notebook "SEO-科技" \
  --title "文章标题" \
  --generate audio,flashcards,quiz,report,infographic
```

### 方式二：写入队列（Pipeline 监听模式）

将任务写入队列文件，pipeline 每 30 秒自动检查并执行：

```bash
echo "https://example.com/seo-article|SEO-科技|文章标题|audio,flashcards,quiz" \
  >> /root/.openclaw/workspace-crm/notebooklm_seo/queue/agent1.txt
```

## 队列文件格式

```
URL|notebook名称|文章标题|生成类型
```

- `|` 分隔，空格不影响
- `#` 开头为注释
- 生成类型：audio / flashcards / quiz / report / infographic / video（逗号分隔）
- 同一 notebook 下的所有 URL 会累积，适合持续添加内容

## 输出结构

```
output/
└── {notebook名称}/
    └── {文章标题}_{时间戳}/
        ├── audio.mp3            # AI 播客音频
        ├── flashcards.json      # 闪卡（导入 Anki）
        ├── flashcards.md        # 闪卡（Markdown）
        ├── quiz.json           # Quiz
        ├── quiz.md              # Quiz（Markdown）
        ├── report.md           # 结构化报告
        ├── infographic.png      # 信息图
        ├── video.mp4           # 视频概览
        └── _result.json        # 任务执行结果
```

## Pipeline 管理命令

```bash
# 查看队列内容
cat /root/.openclaw/workspace-crm/notebooklm_seo/queue/*.txt

# 查看处理日志
tail -f /root/.openclaw/workspace-crm/notebooklm_seo/logs/pipeline_*.log

# 手动触发队列处理（一次性）
python3 /root/.openclaw/workspace-crm/notebooklm_seo/pipeline.py --watch --interval 5

# 批量处理 URL 文件
python3 /root/.openclaw/workspace-crm/notebooklm_seo/pipeline.py --batch urls.txt --notebook "SEO-科技"
```

## 自动触发配置

在 OpenClaw 中设置 cron job，持续监听队列：

```
# 每分钟检查一次队列（用 --interval 1 快速响应）
openclaw cron add --name "nbseo-pipeline" \
  --command "python3 /root/.openclaw/workspace-crm/notebooklm_seo/pipeline.py --watch --interval 60" \
  --detach
```

## NotebookLM 内容类型说明

| 类型 | 格式 | 用途 |
|------|------|------|
| audio | MP3 | AI 播客音频，适合通勤听 |
| flashcards | JSON/MD | 导入 Anki 生成学习卡 |
| quiz | JSON/MD | 配套文章做成测验题 |
| report | MD | 自动摘要报告 |
| infographic | PNG | 信息图，适合社交媒体 |
| video | MP4 | 视频概览 |

## 注意事项

- NotebookLM API 不稳定，同一 notebook 短时间内生成任务不要超过 3 个
- Audio Overview 生成较慢（约 1-3 分钟），infographic 较快（约 30s）
- 建议顺序：先 quiz/flashcards/report（快），再 audio/video（慢）
- cookies 有效期约 7 天，过期需重新导入
