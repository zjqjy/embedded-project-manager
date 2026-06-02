---
name: em-skill
description: 项目开发管家 - 通用核（HVR 工作流 + state.md 瘦身 + new 三档分流）+ 可插拔嵌入式插件。支持通用软件项目（默认）与嵌入式项目（按需加载 plugins/embedded/）。
version: 3.0.0
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

### 子命令路由（执行前必须先读取对应命令文件）

| `$0` | 读取的文件 | 说明 |
|------|-----------|------|
| `si` | `commands/si.md` | 路径 `$1`（空则当前目录） |
| `init` | `commands/init.md` | 名称 `$1` |
| `new` | `commands/new.md` | 功能描述 `$1` |
| `disc` | `commands/disc.md` | — |
| `verify` | `commands/verify.md` | 步骤 `$1`（如 s7） |
| `result` | `commands/result.md` | 结果 `$1` |
| `stat` | `commands/stat.md` | 可选 `-v` / `steps` / `next` |
| `rec` | `commands/rec.md` | 可选 `$1` |
| `sessions` | `commands/sessions.md` | 可选 ID 或 `latest` / `search <kw>` |
| `sw` | `commands/sw.md` | 名称/路径 `$1` |
| `arch` | `commands/arch.md` | — |
| `sum` | `commands/sum.md` | — |
| `pi` | `commands/pi.md` | — |
| `gi` | `commands/gi.md` | — |
| `help` | `commands/help.md` | 可选命令名 `$1` |
| `migrate` | `commands/migrate.md` | — |
| `migrate-state` | `commands/migrate-state.md` | — |

### 嵌入式插件命令（按需加载）

如 `<STATE_DIR>/project.json.type == "embedded"`，路由表追加：

| `$0` | 读取的文件 |
|------|-----------|
| `initem` | `plugins/embedded/commands/initem.md` |

---

## 项目类型

EM-SKILL 提供两类项目支持：

### 通用项目（默认）

适用任何软件开发（Web、App、CLI、库等）。

- **HVR 工作流**：需求 → 设计 → 验证 → 归档
- **状态文件瘦身**：`state.md` ≤ 50 行作单一恢复源；会话独立成文件
- **new 三档分流**（superpower 风格）：
  - 轻档 → `quick-plan.md`（5 min）
  - 中档（默认） → `brainstorm.md` + `milestones.md`（15 min）
  - 重档 → 5 阶段 disc（45 min）
- **Git 集成**：verify 时提议 commit；归档时打 tag

### 嵌入式项目（可拆插件）

`<STATE_DIR>/project.json.type == "embedded"` 时自动加载 `plugins/embedded/`：

- `/em initem` — 工具初始化（OpenOCD/Keil/串口工具路径注册）
- `/em verify` 注入编译→烧录→串口三连子流程
- `/em init` / `/em si` 注入芯片选择 + 学习
- `tools/` 含 `serial-mcp` / `serial-monitor` / `build-keil` / `flash-openocd`

详见：[`plugins/embedded/PLUGIN.md`](plugins/embedded/PLUGIN.md)

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
