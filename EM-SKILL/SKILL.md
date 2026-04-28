---
name: em
description: 嵌入式项目开发管家 - 人机协作测试、存量项目审计、新功能开发
argument-hint: "si|init|new|disc|verify|result|stat|rec|sw|arch|sum|pi|gi|initem|help [command]"
---

# EM - 嵌入式项目开发管家

你接收到的参数：`$ARGUMENTS`

请根据第一个参数执行对应功能：

## 子命令路由（执行前必须先读取对应命令文件）

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

## 快速开始

```
/em help           # 查看帮助
/em si <path>     # 存量接入
/em stat          # 当前步骤
```

## 命令列表

### 项目管理
| 命令 | 说明 | 示例 |
|------|------|------|
| `/em si` | 存量接入 | `/em si D:\project` |
| `/em init` | 项目初始化 | `/em init myproject` |
| `/em stat` | 当前步骤 | `/em stat` |
| `/em rec` | 恢复项目 | `/em rec` |

### 开发流程
| 命令 | 说明 | 示例 |
|------|------|------|
| `/em new` | 新功能开发 | `/em new 添加CAN通信` |
| `/em disc` | 讨论流程 | `/em disc` |
| `/em verify` | 准备验证 | `/em verify s3` |
| `/em result` | 提交结果 | `/em result s3-通过` |

### 工具
| 命令 | 说明 | 示例 |
|------|------|------|
| `/em arch` | 归档 | `/em arch` |
| `/em help` | 帮助 | `/em help verify` |
| `/em sum` | 上下文摘要 | `/em sum` |
| `/em pi` | 项目索引 | `/em pi` |
| `/em gi` | 全局索引 | `/em gi` |
| `/em sw` | 跨项目切换 | `/em sw myproject` |
| `/em initem` | 工具初始化 | `/em initem` |

## 文件结构

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

## 详细文档

- **commands/** - 各命令详细定义
- **workflows/** - 工作流细则
- **templates/** - 模板文件

---
查看详细: /em help verify
