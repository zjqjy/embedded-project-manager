---
name: em-skill
description: 项目开发管家 - 通用核（HVR 工作流 + state.md 瘦身 + new 三档分流）+ 双插件架构（embedded 嵌入式 + learning 学习模式）。支持通用/嵌入式/学习三类项目。
version: 3.1.0
---

# EM-SKILL

> 项目开发管家 | 通用核 + 嵌入式插件 | superpower 风格 new 三档分流

你接收到的参数：`$ARGUMENTS`

---

## 快速开始

```
1. /em help              # 看所有命令
2. /em rec               # 恢复当前项目（只读 state.md，≤50 行）
3. /em new <描述>        # 新功能开发（AI 推荐档位）
```

**首次进入项目**：

| 场景 | 命令 |
|------|------|
| 全新项目 | `/em init <name>` |
| 存量项目（无 `.em/`）| `/em si <path>` |
| 恢复已有项目 | `/em rec` |
| 旧版 `.emv2/` 升级 | `/em migrate` |
| 老项目体感瘦身 | `/em migrate-state` |

---

## 通用命令（16 个）

| 命令 | 用途 |
|------|------|
| `/em rec` | **恢复项目**（只读 state.md ≤50 行） |
| `/em stat` | 查看状态（默认极简；`-v` 全景） |
| `/em sessions` | 浏览会话历史（按需） |
| `/em init` | 初始化项目（自动识别类型） |
| `/em si` | 存量接入 |
| `/em new` | **新功能开发**（三档分流：轻/中/重） |
| `/em disc` | 进入讨论模式（重档独立触发） |
| `/em verify` | 步骤验证 + HVR + commit 提议 |
| `/em result` | 记录验证结果 |
| `/em sw` | 跨项目切换 |
| `/em arch` | 归档已完成步骤 |
| `/em sum` | 生成上下文摘要 |
| `/em pi` | 项目索引 |
| `/em gi` | 全局索引 |
| `/em help` | 帮助 |
| `/em migrate` | `.emv2/` → `.em/` 深度迁移 |
| `/em migrate-state` | 一键生成 state.md（瘦身） |

> **子命令路由约定**：AI 执行任一通用命令时，读取 `commands/<cmd>.md`。
> 通用核不维护命令-文件路由表，约定即可（统一前缀 `commands/`）。

### 插件命令（lazy load — S15）

> 插件命令**不**走 `project.json.type` 检测；用户敲命令时按需加载。
> 路由由 `plugins/_loader.py` 启动时一次性构建 + mtime 缓存（O(1) 查表）。
> 通用核不维护插件命令清单；**新增插件无需改 SKILL.md**，只需在 `plugins/<name>/PLUGIN.md` 声明 `provides.commands` 即可。

| 插件 | 用户前缀 | Manifest |
|------|----------|----------|
| embedded | (空，顶层命令) | [`plugins/embedded/PLUGIN.md`](plugins/embedded/PLUGIN.md) |
| learning | `learn` | [`plugins/learning/PLUGIN.md`](plugins/learning/PLUGIN.md) |

**解析规则**（`em-loader --resolve <inv>`）：
- 直接匹配：`hello` 命中命令名 → 加载
- 前缀拼接：`learn new` 命中 `learn-new` → 加载

详见 [`plugins/_loader.py`](plugins/_loader.py) 与 [`plugins/INDEX.md`](plugins/INDEX.md)。

---

## 项目类型

EM-SKILL 提供三类项目支持：

### 通用项目（默认）

适用任何软件开发（Web、App、CLI、库等）。

- **HVR 工作流**：需求 → 设计 → 验证 → 归档
- **状态文件瘦身**：`state.md` ≤ 50 行作单一恢复源；会话独立成文件
- **new 三档分流**（superpower 风格）：
  - 轻档 → `quick-plan.md`（5 min）
  - 中档（默认） → `brainstorm.md` + `milestones.md`（15 min）
  - 重档 → 5 阶段 disc（45 min）
- **Git 集成**：verify 时提议 commit；归档时打 tag

### 嵌入式项目（按需加载插件）

触发方式：用户敲 `/em initem` 或 `/em build/flash/serial` 时 lazy-load，无需 `type=embedded`。
- `tools/` 含 `serial-mcp` / `serial-monitor` / `build-keil` / `flash-openocd`
- `/em verify` 注入编译→烧录→串口三连子流程
- `/em init` / `/em si` 注入芯片选择 + 学习

详见：[`plugins/embedded/PLUGIN.md`](plugins/embedded/PLUGIN.md)

通用项目**不**加载此插件，零负担。

### 学习模式项目（按需加载插件）⭐ S14 + S15

触发方式：用户敲 `/em learn new/verify/status` 时 lazy-load，无需 `type=learning`。
- `/em learn new <slug> [title]` — 创建新主题（LPR 闭环起点）
- `/em learn verify [slug] [l<N>]` — 阶段验证 + 推进 L1→L5
- `/em learn status [slug] [-v]` — 查看学习状态
- **LPR 5 阶段**：Learn → Pack → Practice → Verify → Surface
- **唯一硬交付物**：主题 README 卡片（5 段式：钩子 → 总结 → 概念图 → 架构 → 踩坑）
- **多格式分发**：`tools/build-html.py` / `generate-script.py` / `generate-poster.py` / `package-skill.py`

详见：[`plugins/learning/PLUGIN.md`](plugins/learning/PLUGIN.md)

通用项目**不**加载此插件，零负担。

---

## 状态目录布局

```
<STATE_DIR>/   ← .em/ (优先) 或 .emv2/ (兼容)
├── state.md           # ⭐ 最小状态（≤50 行，rec 默认只读）
├── project.json       # { type, name, plugins, ... }
├── project-spec.md    # 项目规格单（步骤表）
├── decisions.md       # 决策日志
├── problem-log.md     # 问题追踪
├── sessions/          # 每会话一文件
│   └── sess-<id>.md
├── discussion/        # 讨论目录
│   └── <YYYYMMDD>-<slug>/
│       ├── quick-plan.md   (轻档)
│       ├── brainstorm.md   (中档/重档)
│       ├── milestones.md   (中档/重档)
│       ├── split.md / requirements.md / hardware.md  (重档)
│       └── status.json
├── checkpoints/       # HVR 文件
├── history/           # 归档
└── logs/              # 日志（嵌入式串口/编译日志等）
```

## 详细文档

- `commands/` — 各命令完整定义
- `workflows/` — 工作流细则（discussion-flow / hvr-workflow / new-light / new-standard）
- `templates/` — 模板（state / session / project / project-spec / decisions / problem-log / hvr / global-index / history-index / em-migration）
- `plugins/embedded/` — 嵌入式插件（独立可拆）
- `tools/git-changelog/` — 通用 CHANGELOG 生成工具

---

查看详细: `/em help <命令>`
