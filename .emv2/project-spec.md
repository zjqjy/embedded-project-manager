<!-- 归档内容见 .emv2/history/2026/04/19/project-spec.md -->

# 项目规格单：embedded-project-manager-v2

## Meta
- **创建日期**: 2026-02-25
- **项目类型**: Claude Skill 元仓库
- **当前步骤**: S10 ✅ 完成
- **整体状态**: S1-S6 全部完成 ✅ / S7 EM-SKILL GUI ⏸️ 暂停 / S8 模板优化 ✅ 完成 / S9 embed-ai-tool 整合 ✅ 完成 / S10 工具使用说明 ✅ 完成
- **项目路径**: D:\DeskTop\WorkSpace\Code\embedded-project-manager

## 全局检查点（Gates）
- [x] G1: S2-S6 全部开发完成
- [x] G2: 全流程验证通过
- [x] G3: 文档更新完成
- [ ] G4: 用户验收通过

---

## 开发步骤状态

| 步骤 | 名称 | 状态 | 日期 |
|------|------|------|------|
| S1 | 存量接入 | ✅ 完成 | 2026-02-25 |
| S2 | 需求对齐讨论流程 | ✅ 规划完成 | 2026-03-27 |
| S3 | HVR工作流增强 | ✅ 完成 | 2026-04-16 |
| S4 | 芯片学习机制 | ✅ 完成 | 2026-04-16 |
| S5 | 串口调试工具 | ✅ 完成 | 2026-04-19 |
| S6 | 文件归档机制 | ✅ 完成 | 2026-04-17 |
| S7 | EM-SKILL GUI桌面应用 | ⏸️ 暂停（延后开发） | 2026-04-28 |
| S8 | 优化项目文件模板 | ✅ 完成 | 2026-04-28 |
| S9 | embed-ai-tool 整合 | ✅ 完成 | 2026-04-30 |
| S10 | 工具使用说明 | ✅ 完成 | 2026-05-09 |

---

## S5 串口调试工具（Serial Monitor & AI Assistant）

### 核心定位
**S5 = MCP工具 + GUI + 人-AI协作验证流程**

### 子流程

| 子步骤 | 名称 | 状态 | 说明 |
|--------|------|------|------|
| S5-A | MCP工具开发 | ✅ 完成 | tkinter UI + pyserial + MCP Server |
| S5-B | EM流程集成 | ✅ 完成 | `/em verify` → 打开工具 |
| S5-C | 实际验证测试 | ✅ 完成 | 2026-04-19 MCP测试通过 |

### 技术方案

| 项目 | 选择 |
|------|------|
| GUI框架 | tkinter |
| 串口库 | pyserial |
| MCP SDK | Python版MCP SDK |
| 日志格式 | `.emv2/logs/serial_<步骤>_<时间>.log` |

### 功能清单

| 功能 | 优先级 |
|------|--------|
| 串口配置（端口、波特率） | P0 |
| 实时显示 | P0 |
| 发送命令 | P0 |
| 日志保存 | P0 |
| MCP接口 | P0 |
| 时间戳 | P1 |
| AI分析区 | P1 |

### 讨论记录
- 讨论目录: `.emv2/discussion/20260419-s5-serial-debug/`

---

## /em initem 增强（2026-04-19）

### 新增功能
- Python 自检（检测版本 3.12）
- MCP 工具依赖自动安装
- pip 失败时提供手动安装提示

### 依赖列表
| 依赖 | 用途 | 状态 |
|------|------|------|
| pyserial | S5 串口工具 | ✅ 已安装 |
| mcp | MCP SDK | ✅ 已安装 |

### 讨论记录
- 讨论目录: `.emv2/discussion/20260419-initem-python-check/`

---

## README 完善（2026-04-19）

### 更新内容
- 添加完整开发流程说明（方式A存量接入、方式B空项目）
- 明确两种方式的操作步骤

### 讨论记录
- 讨论目录: `.emv2/discussion/20260419-readme-update/`

---

## S7 EM-SKILL GUI 桌面应用

### 核心定位
**S7 = Tauri桌面应用 + Vue3 UI + Claude CLI管道双向通信**

EM-SKILL的GUI前端，替代命令行操作，提供可视化项目管理界面。

### 子流程

| 子步骤 | 名称 | 状态 | 优先级 | 说明 |
|--------|------|------|--------|------|
| S7-A | 技术验证 | ✅ 完成 | P0 | 验证Claude CLI管道通信可行性 |
| S7-B | 项目脚手架 | ✅ 完成 | P0 | 初始化Tauri+Vue3+Vite+Element Plus项目框架 |
| S7-C | Claude Code桥接 | ⏸️ 暂停 | P0 | Rust后端进程管理 + Tauri IPC事件流 + 权限交互UI（Windows兼容性问题待后续修复） |
| S7-D | 项目管理面板 | ✅ 完成 | P0 | 项目状态显示、操作记录、刷新功能 |
| S7-E | 命令快捷操作区 | ✅ 完成 | P0 | 一键按钮面板、自定义命令输入 |
| S7-F | 日志与输出面板 | ✅ 完成 | P0 | Markdown实时输出、操作记录侧栏 |
| S7-G | 串口工具(Vue版) | ✅ 完成 | P1 | 串口配置/连接/终端界面（待后端实现） |
| S7-H | VS Code Extension | ⏸️ 暂停 | P2 | 轻量Extension嵌入VS Code侧栏 |
| S7-I | 技能整合框架 | ⏸️ 暂停 | P2 | 插件式架构，后续整合embed-ai-tool |

### 技术方案

| 项目 | 选择 |
|------|------|
| 桌面框架 | Tauri (Rust + Web前端) |
| 前端框架 | Vue3 + Vite |
| UI组件库 | Element Plus |
| Claude通信 | CLI管道（常驻子进程，stdin/stdout实时双向） |
| 串口工具 | Vue重写（保留原tkinter工具） |

### 讨论记录
- 讨论目录: `.emv2/discussion/20260428-em-skill-gui/`

---

## S9 embed-ai-tool 整合

### 核心定位
**EM = 流程控制（verify 命令），embed-ai-tool = 具体执行（编译/烧录/监控）**

embed-ai-tool 的脚本已合并到 `EM-SKILL/tools/` 目录，EM-SKILL 实现自包含。

### 子流程

| 子步骤 | 名称 | 状态 | 说明 |
|--------|------|------|------|
| S9-A | 工具初始化+权限配置 | ✅ 完成 | initem.md 新增工具路径自动探测/注册流程 |
| S9-B | build-keil 脚本整合 | ✅ 完成 | 合并到 EM-SKILL/tools/build-keil/ |
| S9-C | flash-openocd 脚本整合 | ✅ 完成 | 合并到 EM-SKILL/tools/flash-openocd/ + 修复硬编码bug |
| S9-D | serial-monitor 脚本整合 | ✅ 完成 | 合并到 EM-SKILL/tools/serial-monitor/ |
| S9-E | HVR 工作流更新 | ✅ 完成 | hvr-workflow.md 新增技能声明+AI执行记录 |
| S9-F | 全流程验证 | ✅ 完成 | OTA 项目验证通过，编译→烧录→串口全流程OK |

### 技术方案

| 项目 | 选择 |
|------|------|
| 脚本位置 | EM-SKILL/tools/ 内自包含 |
| 配置读取 | tool_config.py（EM-SKILL/tools/shared/） |
| 串口工具 | S5 serial-mcp (GUI) + serial-monitor (CLI) 并存 |

### 讨论记录
- 讨论目录: `.emv2/discussion/20260420-embed-ai-tool-integration/`

---

## S10 工具使用说明

### 核心定位
**为编译/烧录/串口工具建立使用说明和触发机制**

### 子流程

| 子步骤 | 名称 | 状态 | 说明 |
|--------|------|------|------|
| S10-A | 修改 si.md | ✅ 完成 | 增加创建 CLAUDE.md 步骤 |
| S10-B | 修改 init.md | ✅ 完成 | 增加创建 CLAUDE.md 步骤 |
| S10-C | 新建 build.md | ✅ 完成 | 编译详细说明命令文件 |
| S10-D | 新建 flash.md | ✅ 完成 | 烧录详细说明命令文件 |
| S10-E | 新建 serial.md | ✅ 完成 | 串口监控详细说明命令文件 |

### 文件结构

```
EM-SKILL/
├── commands/
│   ├── build.md      # 编译详细说明
│   ├── flash.md      # 烧录详细说明
│   └── serial.md     # 串口监控详细说明
└── tools/
    ├── build-keil/
    ├── flash-openocd/
    ├── serial-monitor/
    └── serial-mcp/
```

### 触发机制

在项目 CLAUDE.md 中增加"工具使用说明索引"，当用户提到关键词时自动查看对应命令文件：

| 关键词 | 查看文件 |
|--------|----------|
| 编译/build/编译固件 | `EM-SKILL/commands/build.md` |
| 烧录/下载/flash | `EM-SKILL/commands/flash.md` |
| 串口/监控/debug | `EM-SKILL/commands/serial.md` |

### 讨论记录
- 讨论目录: `.emv2/discussion/20260509-usage-guide/`

## 归档文件类型

| 文件 | 触发条件 | 说明 |
|------|----------|------|
| memory-log.md | > 600行 | 记忆日志，按会话归档 |
| project-spec.md | S完成后 | 项目规格单，按里程碑归档 |
| problem-log.md | > 300行 | 问题追踪记录 |
| decision-log.md | > 300行 | 关键决策记录 |

---

## 问题追踪

### 待解决问题
（无）

### 已解决问题
1. 基本功能搭建完成 - 2026-02-25
2. S4芯片学习机制 - 2026-04-16
3. S8 .emv2文件自动读取 - 2026-04-16
4. S6文件归档机制 - 2026-04-17
5. S5串口调试工具 - 2026-04-19

---

## 讨论索引

| 讨论 | 目录 |
|------|------|
| S5 串口调试讨论 | `.emv2/discussion/20260419-s5-serial-debug/` |
| embed-ai-tool 整合讨论 | `.emv2/discussion/20260420-embed-ai-tool-integration/` |
| S7 GUI 讨论 | `.emv2/discussion/20260428-em-skill-gui/` |
| new 命令步骤编号讨论 | `.emv2/discussion/20260428-new-step-id/` |
| 步骤状态自动推进讨论 | `.emv2/discussion/20260428-step-state-machine/` |
| S8 优化模板讨论 | `.emv2/discussion/20260428-optimize-templates/` |
| S10 工具使用说明讨论 | `.emv2/discussion/20260509-usage-guide/` |

---

## 参考文档
- Skill 安装路径: C:\Users\23393\.claude\skills\EM-SKILL
- chips.json 路径: C:\Users\23393\.claude\chips.json
- embed-ai-tool 路径: D:\DeskTop\WorkSpace\Code\embed-ai-tool
- 归档索引: .emv2/history/index.md
