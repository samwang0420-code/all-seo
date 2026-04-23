# Agent 协作协议

## 角色定义

| 角色 | Workspace | 职责 |
|---|---|---|
| **中枢** | workspace-crm | 监控、汇总、修复、汇报 |
| **错误码 Agent** | workspace-geo-arch | 生成错误码页面 |
| **供应站 Agent** | workspace-geo-suppler | 生成供应站页面 |
| **城市站 Agent** | workspace-geo-all | 生成城市页面 |

---

## 每日工作流程

### Agent 侧（每天自动跑）

每个 agent 跑完后，在 `/root/.openclaw/workspace-crm/central/reports/` 写一个状态文件：

```
# 格式：{agent-name}_{date}.json
# 例：error-code_2026-04-10.json

{
  "agent": "error-code",
  "workspace": "workspace-geo-arch",
  "date": "2026-04-10",
  "status": "ok" | "error" | "blocked",
  "pages_generated": 528,
  "pages_published": 528,
  "errors": [],
  "blockers": [],
  "needs_attention": false,
  "notes": "昨天计划覆盖 12 brands，今天追加了 dishwawer 分类"
}
```

### 中枢侧（我，每天汇总）

1. **每天 10:00 UTC**（北京 18:00）：读取三个 agent 的最新状态文件
2. **如果有问题**：自动尝试修复，记录到 `central/repair_log.md`
3. **如果修不了**：向 wei 报告具体问题
4. **汇总报告**：给 wei 发一份简洁的今日摘要

---

## 报告文件路径

```
/root/.openclaw/workspace-crm/central/reports/
├── 2026-04-10.json          ← orchestrator 主报告
├── error-code_2026-04-10.json   ← 错误码 agent 状态
├── supply_2026-04-10.json      ← 供应站 agent 状态
├── city_2026-04-10.json        ← 城市站 agent 状态
└── repair_log.md               ← 修复操作日志
```

---

## Agent → 中枢 汇报格式

每个 agent 每天向 `central/reports/{agent}_{date}.json` 写状态。格式：

```json
{
  "agent": "error-code",
  "workspace": "workspace-geo-arch",
  "date": "2026-04-10",
  "status": "ok",
  "pages_generated": 528,
  "pages_published": 528,
  "git_commit": "abc1234",
  "errors": [],
  "blockers": [],
  "next_priority": "补全 dishwasher 分类剩余错误码",
  "needs_attention": false,
  "notes": ""
}
```

`status` 含义：
- `ok` — 顺利完成，不需要关注
- `error` — 有生成错误，已记录
- `blocked` — 无法继续，等我介入

---

## 错误升级流程

```
Agent 发现问题
    ↓
尝试自己修复（2次）
    ↓
失败 → status=blocked + 写清楚错误详情
    ↓
我（中枢）读取
    ↓
能修 → 修复 + 通知 Agent 重跑
不能修 → 向 wei 报告
```

---

## 中枢 → Agent 指令格式

如果需要 agent 做额外任务，我写：

```
/root/.openclaw/workspace-crm/central/instructions/{agent}_{date}.txt

例：
error-code_2026-04-10.txt

今天请追加生成：
- dishwasher 分类：bosch, lg, samsung 各 15 个错误码
- 完成后更新 sitemap.xml
```

Agent 下次运行时读取这个文件执行。

---

## 禁止事项（Agent 不要自己做）

- ❌ 删除大量已有页面
- ❌ 修改生成器核心逻辑
- ❌ 改变 URL 结构
- ❌ 停掉定时任务
- ❌ 用 human-writing / NotebookLM 覆盖生成器输出

如有以上需求 → 向中枢（我）报告 → 我向 wei 确认。

---

## 共享资源（只读）

三个 agent 都可以读取，不许修改：

```
/root/.openclaw/workspace-crm/notebooklm_seo/       ← 生成器（只读）
/root/.openclaw/workspace-crm/central/all_city_slugs.txt   ← 城市列表
/root/.openclaw/workspace-crm/central/orchestrator.py     ← 中枢逻辑
```

生成器如有 bug → 向中枢报告 → 我修复 → 通知所有 agent 更新。
