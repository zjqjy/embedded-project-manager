---
name: em-skill
description: 嵌入式项目开发管家 - 人机协作测试、存量项目审计、新功能开发。提供 rec/init/new/disc/verify 等命令，通过 HVR 工作流管理嵌入式项目从需求到验证全流程。
version: 2.0.0
---

# EM-SKILL

> 嵌入式项目开发管家 | HVR（需求→设计→验证）工作流 | 通用项目 + 嵌入式双场景

你接收到的参数：`$ARGUMENTS`

---

## 快速开始

3 步上手 EM-SKILL：

```
1. /em help              # 查看所有命令
2. /em stat              # 查看当前项目状态（如已初始化）
3. /em help verify       # 查看核心命令 verify 详情
```

**首次使用**（存量项目）：

```
/em si <path>            # 存量接入 - 扫描并建立 .emv2/
/em rec                  # 恢复项目状态（任意时刻可执行）
```

**新项目**：

```
/em init <name>          # 初始化（自动识别嵌入式特征）
/em new <功能描述>       # 进入新功能开发流程
```

---

## 通用命令

EM-SKILL 提供 14 个 `/em` 命令（外加 `si` 用于存量接入），覆盖项目全生命周期：

| 命令 | 用途 |
|------|------|
| `/em rec` | 恢复项目状态（按 path 加载 `.emv2/`） |
| `/em init` | 初始化新项目（智能识别嵌入式特征） |
| `/em new` | 进入新功能开发流程 |
| `/em disc` | 进入需求讨论模式 |
| `/em verify` | 执行步骤验证（如 `/em verify s7`） |
| `/em result` | 记录验证结果 |
| `/em stat` | 查看当前项目状态 |
| `/em sw` | 跨项目切换 |
| `/em arch` | 归档已完成步骤 |
| `/em sum` | 生成上下文摘要 |
| `/em pi` | 查看项目索引 |
| `/em gi` | 查看全局索引 |
| `/em help` | 帮助（`/em help <cmd>` 查看命令详情） |
| `/em initem` | 工具初始化（检查/更新 `~/.claude/settings.json`） |
| `/em migrate` | 迁移 `.emv2/` → `.em/`（S10-C，存量项目按需） |

> 注：`/em initem` 也是嵌入式场景入口（详见下文）。

### 子命令路由（执行前必须先读取对应命令文件）

如果 `$0` 是 `si`：
- **立即读取** `commands/si.md`
- 严格按照该文件执行存量接入，路径为 `$1`（空时使用当前目录 `.`）

如果 `$0` 是 `init`：
- **立即读取** `commands/init.md`
- 严格按照该文件执行项目初始化，名称为 `$1`

如果 `$0` 是 `new`：
- **立即读取** `commands/new.md`
- 严格按照该文件执行新功能开发流程，功能描述为 `$1`

如果 `$0` 是 `disc`：
- **立即读取** `commands/disc.md`
- 严格按照该文件进入讨论流程模式

如果 `$0` 是 `verify`：
- **立即读取** `commands/verify.md`
- 严格按照该文件内的流程执行验证步骤 `$1`（s<编号>，如 s7）
- **不要跳过文件中的任何检查项或模板**

如果 `$0` 是 `result`：
- **立即读取** `commands/result.md`
- 严格按照该文件记录验证结果 `$1`

如果 `$0` 是 `stat`：
- **立即读取** `commands/stat.md`
- 严格按照该文件查看当前项目状态

如果 `$0` 是 `rec`：
- **立即读取** `commands/rec.md`
- 严格按照该文件恢复项目，可选路径 `$1`

如果 `$0` 是 `sw`：
- **立即读取** `commands/sw.md`
- 严格按照该文件跨项目切换，名称/路径为 `$1`

如果 `$0` 是 `arch`：
- **立即读取** `commands/arch.md`
- 严格按照该文件执行归档

如果 `$0` 是 `sum`：
- **立即读取** `commands/sum.md`
- 严格按照该文件生成上下文摘要

如果 `$0` 是 `pi`：
- **立即读取** `commands/pi.md`
- 严格按照该文件查看项目索引

如果 `$0` 是 `gi`：
- **立即读取** `commands/gi.md`
- 严格按照该文件查看全局索引

如果 `$0` 是 `help`：
- **立即读取** `commands/help.md`
- 如果有 `$1`，显示 `commands/$1.md` 内容
- 如果无 `$1`，显示所有命令列表

如果 `$0` 是 `initem`：
- **立即读取** `commands/initem.md`
- 严格按照该文件执行工具初始化，检查并更新 `~/.claude/settings.json` 配置

如果 `$0` 是 `migrate`：
- **立即读取** `commands/migrate.md`
- 严格按照该文件执行 `.emv2/` → `.em/` 迁移，可选路径 `$1`

---

## 项目类型

EM-SKILL 双轨制：通用项目（默认）+ 嵌入式场景（⭐ 原生场景）。

### 通用项目

适用于任何软件开发项目（Web、App、CLI、库等）。EM 核心能力：

- **HVR 工作流**：需求（Human-Verify-Result）→ 设计 → 验证 → 归档
- **状态管理**：`memory-log.md`（必读）、`problem-log.md`、`decision-log.md`
- **讨论机制**：`/em disc` 进入结构化讨论，产出 `requirements/rules/hardware/milestones`
- **验证闭环**：`/em verify s<N>` + `/em result` + HVR 文件

通用项目 init 时不加载嵌入式工具。

### 嵌入式场景 ⭐

EM 起源于嵌入式，通用化是叠加层。嵌入式项目自动启用以下能力：

#### 嵌入式专属命令

`/em initem` — 工具初始化命令，嵌入式场景的核心入口：

- 检查并安装 `serial-mcp`、`serial-monitor`、`build-keil`、`flash-openocd` 工具
- 更新 `~/.claude/settings.json` 配置
- 含 **OpenOCD 下载指引**（嵌入式烧录首选方案）

#### 工具索引

EM-SKILL 集成 4 个嵌入式工具（位于 `EM-SKILL/tools/`）：

| 工具 | 路径 | 用途 | 步骤 |
|------|------|------|------|
| `serial-mcp` | `EM-SKILL/tools/serial-mcp/` | 串口 GUI 工具（图形化监控） | S5 |
| `serial-monitor` | `EM-SKILL/tools/serial-monitor/` | 串口 CLI 工具（自动化） | S9 |
| `build-keil` | `EM-SKILL/tools/build-keil/` | Keil 编译脚本 | S9 |
| `flash-openocd` | `EM-SKILL/tools/flash-openocd/` | OpenOCD 烧录脚本 | S9 |

调用方式：通过 `~/.claude/settings.json` 中配置的 MCP/CLI 工具直接调用。

#### 嵌入式项目快速开始

```
1. /em si <path>            # 存量接入（Keil/CubeMX/ESP-IDF/PlatformIO 项目）
   - 自动检测嵌入式特征 → 启用嵌入式工具集
2. /em initem               # 初始化工具（首次使用）
3. /em rec                  # 恢复项目状态
4. 编译 → 烧录 → 串口 流程：
   - build-keil/keil_build.sh
   - flash-openocd/openocd_flash.sh
   - serial-mcp 或 serial-monitor 监控
```

#### S5/S7/S9 已完成能力

| 步骤 | 能力 | 说明 |
|------|------|------|
| **S5** | 串口 GUI 工具（`serial-mcp`） | 图形化监控串口输出 |
| **S7** | 测试结果记录 | `/em result` + HVR 文件 |
| **S9** | 嵌入式三件套 | `serial-monitor`（CLI）+ `build-keil`（编译）+ `flash-openocd`（烧录） |

#### 详细使用场景

完整的嵌入式使用场景（智能识别逻辑、工具详细说明、典型工作流、`.emv2/` → `.em/` 迁移指南）见：

- [`templates/em-migration.md`](templates/em-migration.md) — 嵌入式使用场景与迁移指南
- [`commands/migrate.md`](commands/migrate.md) — `/em migrate` 命令完整定义

---

## 详细命令文档

各命令的完整定义见 `commands/` 目录：

```
commands/
├── si.md        # /em si - 存量接入
├── init.md      # /em init - 项目初始化
├── new.md       # /em new - 新功能开发
├── disc.md      # /em disc - 讨论模式
├── verify.md    # /em verify - 步骤验证
├── result.md    # /em result - 记录结果
├── stat.md      # /em stat - 查看状态
├── rec.md       # /em rec - 恢复项目
├── sw.md        # /em sw - 切换项目
├── arch.md      # /em arch - 归档
├── sum.md       # /em sum - 上下文摘要
├── pi.md        # /em pi - 项目索引
├── gi.md        # /em gi - 全局索引
├── help.md      # /em help - 帮助
├── initem.md    # /em initem - 工具初始化
└── migrate.md   # /em migrate - 迁移 .emv2/ → .em/（S10-C）
```

辅助目录：

- **workflows/** - 工作流细则
- **templates/** - 模板文件
- **tools/** - 嵌入式工具集（serial-mcp / serial-monitor / build-keil / flash-openocd）

---

## 文件结构

EM-SKILL 在项目中生成 `.emv2/` 目录（v2.0+ 新项目将使用 `.em/`，`.emv2/` 仍兼容）：

```
.emv2/
├── project-spec.md      # 项目规格单
├── memory-log.md        # 记忆日志（必读）
├── problem-log.md       # 问题追踪
├── decision-log.md      # 决策记录
├── discussion/          # 讨论结果
│   └── <需求ID>/
│       ├── requirements.md
│       ├── rules.md
│       ├── hardware.md
│       └── milestones.md
├── checkpoints/         # HVR文件
│   └── HVR-S<X>-<N>.md
├── history/             # 归档
│   └── index.md
└── logs/                # 串口日志
    └── serial_<步骤>_<问题>.log
```

---

查看详细: `/em help verify`
