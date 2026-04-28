<!-- 归档内容见 .emv2/history/2026/04/19/project-spec.md -->

# 项目规格单：embedded-project-manager-v2

## Meta
- **创建日期**: 2026-02-25
- **项目类型**: Claude Skill 元仓库
- **当前步骤**: S7-A(开发中)
- **整体状态**: S1-S6 全部完成 ✅ / S7 EM-SKILL GUI 开发中 🚧
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
| S7 | EM-SKILL GUI桌面应用 | 🚧 讨论完成 | 2026-04-28 |
| S8 | 优化项目文件模板 | 🚧 讨论中 | 2026-04-28 |

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

## S7 EM-SKILL GUI 桌面应用

### 核心定位
**S7 = Tauri桌面应用 + Vue3 UI + Claude CLI管道双向通信**

EM-SKILL的GUI前端，替代命令行操作，提供可视化项目管理界面。

### 子流程

| 子步骤 | 名称 | 状态 | 优先级 | 说明 |
|--------|------|------|--------|------|
| S7-A | 技术验证 | 🔲 待开发 | P0 | 验证Claude CLI管道通信可行性 |
| S7-B | 项目脚手架 | 🔲 待开发 | P0 | 初始化Tauri+Vue3+Vite+Element Plus项目框架 |
| S7-C | Claude Code桥接 | 🔲 待开发 | P0 | 常驻子进程管理、命令发送、流式输出接收 |
| S7-D | 项目管理面板 | 🔲 待开发 | P0 | 项目信息读取、步骤状态展示、待办事项 |
| S7-E | 命令快捷操作区 | 🔲 待开发 | P0 | 一键按钮面板、命令历史/收藏 |
| S7-F | 日志与输出面板 | 🔲 待开发 | P0 | Markdown渲染、日志搜索/导出 |
| S7-G | 串口工具(Vue版) | 🔲 待开发 | P1 | 重写串口面板，保留原tkinter工具 |
| S7-H | VS Code Extension | 🔲 待开发 | P2 | 轻量Extension嵌入VS Code侧栏 |
| S7-I | 技能整合框架 | 🔲 待开发 | P2 | 插件式架构，后续整合embed-ai-tool |

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

---

## 参考文档
- Skill 安装路径: C:\Users\23393\.claude\skills\EM-SKILL
- chips.json 路径: C:\Users\23393\.claude\chips.json
- embed-ai-tool 路径: D:\DeskTop\WorkSpace\Code\embed-ai-tool
- 归档索引: .emv2/history/index.md
