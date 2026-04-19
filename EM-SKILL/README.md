# EM-SKILL - 嵌入式项目开发管家

**AI辅助嵌入式开发的人机协作工具**

EM-SKILL 通过人-AI协作工作流，帮助管理嵌入式项目的全生命周期：存量代码接入、需求讨论、硬件验证、问题追踪、文档归档。

---

## 快速开始

### 1. 首次安装 - 初始化工具

```bash
/em initem
```

这将配置必要的权限，减少后续操作中的确认提示。

### 2. 接入项目

```bash
/em si <项目路径>   # 存量接入已有项目
/em stat           # 查看当前项目状态
```

### 3. 开发流程

```bash
/em disc S3        # 进入讨论流程（讨论某个步骤）
/em verify s3     # 准备验证
/em result s3-通过  # 提交验证结果
```

---

## 核心理念

### 人-AI协作

| 角色 | 职责 |
|------|------|
| **人类** | 硬件操作、执行验证、观察现象、口述反馈 |
| **AI** | 文档维护、代码分析、日志解读、方案建议、记录决策 |

### 协作模式

```
人类执行验证操作
    ↓
观察并口述现象给AI
    ↓
AI记录到HVR文件、分析根因、给出建议
    ↓
人类确认 / 补充观察
    ↓
AI + 人类 共同决策
```

---

## HVR工作流 - Human Verification Request

HVR是AI维护、人类确认的工作区，用于硬件验证阶段。

### 完整流程

```
┌─────────────────────────────────────────────────────────┐
│  1. 准备阶段                                            │
│  用户: /em verify s3                                    │
│       ↓                                                 │
│  AI: 生成HVR文件 → 启动S5工具（后台）                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  2. 验证阶段 ←── /em result 在这里提交                 │
│  用户: 执行验证 → 观察现象 → 提交结果                   │
│       ↓                                                 │
│  用户: /em result s3-通过 或 /em result s3-失败-描述    │
└─────────────────────────────────────────────────────────┘
                          ↓
          ┌─────────────────┴─────────────────┐
          ↓                                   ↓
    【通过】                              【失败】
          ↓                                   ↓
    AI更新文档                          AI读取MCP日志
    提示下一步                          + 人类补充观察
                                           ↓
                                   AI + 人类共同分析
                                           ↓
                                   AI + 人类共同修改
```

### 验证结果处理

**通过时:**
```
/em result s3-通过  →  AI更新HVR → 更新project-spec → 提示下一步
```

**失败时:**
```
/em result s3-失败-LED闪红
    ↓
AI: [读取MCP日志] → 分析原因
AI: "可能原因1/2/3，请确认"
用户: "确认是原因2"
    ↓
AI + 人类 共同分析 → 确定修改方案
AI + 人类 一起修改代码
    ↓
重新验证 → /em result s3-通过
```

---

## 命令参考

### 项目管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `/em initem` | **首次使用必须执行** - 初始化工具权限 | `/em initem` |
| `/em si <path>` | 存量接入已有项目 | `/em si D:\project` |
| `/em init <name>` | 初始化新项目 | `/em init motor_ctrl` |
| `/em stat` | 查看当前步骤状态 | `/em stat` |
| `/em rec` | 恢复项目上下文 | `/em rec` |
| `/em sw <name>` | 跨项目切换 | `/em sw motor_ctrl` |

### 开发流程

| 命令 | 说明 | 示例 |
|------|------|------|
| `/em new <描述>` | 新功能开发流程 | `/em new 添加CAN通信` |
| `/em disc [步骤]` | 进入讨论流程 | `/em disc S3` |
| `/em verify <步骤>` | 准备验证 | `/em verify s3` |
| `/em result <结果>` | 提交验证结果 | `/em result s3-通过` |

### 工具

| 命令 | 说明 | 示例 |
|------|------|------|
| `/em arch` | 归档文件 | `/em arch` |
| `/em sum` | 生成上下文摘要 | `/em sum` |
| `/em pi` | 查看项目索引 | `/em pi` |
| `/em gi` | 查看全局索引 | `/em gi` |
| `/em help [命令]` | 查看命令帮助 | `/em help verify` |

---

## 开发步骤

| 步骤 | 名称 | 说明 |
|------|------|------|
| S1 | 存量接入 | 接入已有代码库，建立项目上下文 |
| S2 | 需求对齐 | 讨论并明确功能需求、硬件规格 |
| S3 | HVR增强 | Human Verification Request工作流增强 |
| S4 | 芯片学习 | 建立芯片知识库，自动识别芯片型号 |
| S5 | 串口调试 | 串口监控工具 + MCP接口，支持AI读取日志 |
| S6 | 文件归档 | 自动归档机制，保持文档精简 |

---

## 项目结构

```
项目根目录/
├── .emv2/                      # EM-SKILL工作区
│   ├── project-spec.md        # 项目规格单（必读）
│   ├── memory-log.md           # 记忆日志（必读）
│   ├── problem-log.md          # 问题追踪
│   ├── decision-log.md         # 关键决策
│   ├── discussion/             # 讨论结果
│   │   └── <需求ID>/
│   │       ├── requirements.md
│   │       ├── hardware.md
│   │       ├── brainstorm.md
│   │       └── milestones.md
│   ├── checkpoints/           # HVR验证文件
│   │   └── HVR-S<X>-<N>.md
│   ├── history/                # 归档
│   │   └── index.md
│   └── logs/                   # 串口日志
│       └── serial_<步骤>_<时间>.log
│
└── EM-SKILL/                   # 技能定义
    ├── SKILL.md                # 技能入口
    ├── README.md               # 本文件
    ├── commands/               # 命令定义
    ├── workflows/              # 工作流细则
    ├── templates/              # 模板文件
    └── tools/                  # 工具集
        └── serial-mcp/         # S5串口工具
```

---

## S5 串口调试工具

人-AI协作验证的核心工具，提供串口监控和MCP接口。

### 功能

- 串口配置（端口、波特率、数据位、校验位、停止位）
- 实时日志显示
- 命令发送
- 日志保存
- MCP接口（供AI读取日志）

### MCP工具

| 工具 | 功能 |
|------|------|
| `serial_status` | 获取连接状态 |
| `serial_read` | 读取日志文件 |
| `serial_send` | 发送命令到串口 |
| `serial_log_file` | 获取日志文件路径 |

### 启动

```bash
/em verify s5    # 启动S5工具进行验证
```

---

## 芯片学习机制

EM-SKILL自动识别项目使用的芯片型号，并建立知识库。

### 识别方式

通过扫描代码中的 `system_*.c` 和 `startup_*.s` 文件识别芯片。

| 文件名模式 | 厂商 | 芯片系列 |
|-----------|------|----------|
| `system_stm32f4xx.c` | ST | STM32F4xx |
| `system_gd32f4xx.c` | GigaDevice | GD32F4xx |
| `system_ch32v2xx.c` | WCH | CH32V2xx |

### 知识库

- **位置**: `~/.claude/chips.json`
- **内置芯片**: STM32F1/F4, GD32F1/F4, CH32V1/V2等
- **学习芯片**: 首次识别到新芯片时自动添加

---

## 归档规则

| 文件类型 | 触发条件 | 说明 |
|----------|----------|------|
| memory-log.md | > 600行 或 S步骤完成 或 会话结束 | 按会话归档 |
| project-spec.md | S步骤完成 | 按里程碑归档 |
| problem-log.md | > 300行 | 问题追踪记录 |
| decision-log.md | > 300行 | 关键决策记录 |

---

## 安装

### 方式1: 复制到Claude Skills目录

```bash
cp -r EM-SKILL ~/.claude/skills/
```

### 方式2: 使用skill-install安装

```
/skill-install <repo-url>
```

### 初始化

```bash
/em initem
```

### 依赖安装（S5串口工具）

```bash
cd EM-SKILL/tools/serial-mcp
pip install -r requirements.txt
```

---

## 相关文档

- [SKILL.md](./SKILL.md) - 技能入口定义
- [workflows/hvr-workflow.md](./workflows/hvr-workflow.md) - HVR工作流细则
- [workflows/discussion-flow.md](./workflows/discussion-flow.md) - 讨论流程
- [workflows/chip-learning.md](./workflows/chip-learning.md) - 芯片学习机制
- [commands/](./commands/) - 各命令详细文档
- [tools/serial-mcp/README.md](./tools/serial-mcp/README.md) - S5串口工具说明
