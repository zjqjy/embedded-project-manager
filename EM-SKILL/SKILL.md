---
name: em
description: 嵌入式项目开发管家 - 人机协作测试、存量项目审计、新功能开发
argument-hint: "<si|init|new|disc|verify|result|stat|rec|sw|arch|sum|pi|gi|help> [args]"
---

# EM - 嵌入式项目开发管家

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
