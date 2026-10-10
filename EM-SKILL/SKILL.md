---
name: em
description: 项目开发管家 - 通用核（HVR 工作流 + state.md 瘦身 + new 三档分流）+ 双插件架构（embedded 嵌入式 + learning 学习模式）。支持通用/嵌入式/学习三类项目。
version: 4.0.0
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

## 通用命令（19 个）

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
| `/em pro` | **跨项目记录**（追加到管家项目 problem-log，集中处理） |
| `/em migrate` | `.emv2/` → `.em/` 深度迁移 |
| `/em migrate-state` | 一键生成 state.md（瘦身） |
| `/em logs-clean` | **日志滚动清理**（保留最新 N 份，S17-A） |

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
- **new 三档分流**（superpower 风格，S18 起追问先行、落盘最后）：
  - 三档必经 **R0 追问轮**（`workflows/new-clarify.md`）：一次一问澄清需求（轻 ≤2 / 中 ≤5 / 重每子系统 ≤3），理解摘要经用户确认才继续
  - 轻档 → R0 + 对话内 quick-plan，**不落盘**（5 min）
  - 中档（默认） → R0 + R1/R2 对话 → R3 统一落盘 `features/S<N>-<slug>/plan.md`（15 min）
  - 重档 → R0 + 5 阶段 disc（45 min）
  - **硬闸门**：理解未确认禁止出方案；写文档永远是流程最后一步
- **Git 集成**：verify 时提议 commit；归档时打 tag

### 嵌入式项目（按需加载插件）

触发方式：用户敲 `/em initem` 或 `/em build/flash/serial` 时 lazy-load，无需 `type=embedded`。
- `tools/adapters/{build,flash,observe}/` adapter 集 + `tools/registry.json` 能力矩阵（S17-B：芯片×动词×adapter 数据驱动）+ `serial-mcp` GUI
- `/em verify` 注入编译→烧录→串口三连子流程
- `/em init` / `/em si` 注入芯片选择 + 学习

详见：[`plugins/embedded/PLUGIN.md`](plugins/embedded/PLUGIN.md)

通用项目**不**加载此插件，零负担。

### 学习模式项目（按需加载插件）⭐ S14 + S15

触发方式：用户敲 `/em learn new/verify/status` 时 lazy-load，无需 `type=learning`。
- `/em learn new <slug> [title]` — 创建新主题（LPR 闭环起点）
- `/em learn verify [slug] [l<N>]` — 阶段验证 + 推进 L1→L5
- `/em learn status [slug] [-v]` — 查看学习状态
- `/em learn humanize [slug]` — 去 AI 味检查（L5 定稿工序）
- **LPR 5 阶段**：Learn → Pack → Practice → Verify → Surface
- **唯一硬交付物**：主题 README 卡片（5 段式：钩子 → 总结 → 概念图 → 架构 → 踩坑）
- **风格硬约束**：所有讲解产物遵守 [plugins/learning/STYLE.md](plugins/learning/STYLE.md) —— 行业术语当主语、禁自造拟人名词、类比 ≤1 个/篇、结论先行、标题即结论
- **多格式分发**：`tools/build-html.py` / `generate-script.py` / `generate-poster.py` / `package-skill.py`

详见：[`plugins/learning/PLUGIN.md`](plugins/learning/PLUGIN.md)

通用项目**不**加载此插件，零负担。

---

## 状态目录布局（v4，S17-D 收敛：11 类 → 6 类，活文件 2 个）

```
<STATE_DIR>/   ← .em/
├── state.md           # ⭐ 唯一活状态（≤50 行，rec 硬闸门）
├── project.json       # { type, name, embedded?, plugins, ... }
├── journal.md         # append-only 时间线（会话/决策/问题闭环/维护）
├── problem-log.md     # 只留 open 问题（closed > 30 天归档）
├── features/          # ⭐ 每主步骤一目录：README 状态卡 + plan.md + hvr.md
│   ├── README.md      # 步骤索引总表
│   └── S<N>-<slug>/
├── history/           # 完成步骤整目录 + 各类归档（最终归宿）
└── logs/              # 日志（/em logs-clean 滚动保留 N 份）
```

> 生命周期规则见 [`docs/LIFECYCLE.md`](docs/LIFECYCLE.md)；v3 结构迁移见 `commands/migrate.md` §v4。

## 详细文档

- `commands/` — 各命令完整定义
- `workflows/` — 工作流细则（new-clarify / discussion-flow / hvr-workflow / new-light / new-standard）
- `templates/` — 模板（state / session / project / project-spec / decisions / problem-log / hvr / global-index / history-index / em-migration）
- `plugins/embedded/` — 嵌入式插件（独立可拆）
- `tools/git-changelog/` — 通用 CHANGELOG 生成工具

---

查看详细: `/em help <命令>`
