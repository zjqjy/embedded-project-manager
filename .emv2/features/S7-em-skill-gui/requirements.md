# 需求确认 - EM-SKILL GUI

**需求ID**: 20260428-em-skill-gui
**日期**: 2026-04-28

## M1: GUI框架选型
- **方案**: Tauri桌面应用（独立窗口）
- **前端框架**: Vue3 + Vite
- **UI组件库**: Element Plus
- **CLI用户兼容**: 可额外提供VS Code Extension

## M2: 命令后端引擎
- **调用方式**: GUI通过CLI管道向常驻Claude子进程发送`/em xxx`命令
- **命令模板**: 常用命令设置预制模板
- **命令历史**: ✅ 支持（最近使用命令可快速复用）
- **收藏功能**: ✅ 支持

## M3: Claude Code桥接
- **方案**: `claude -p` 单次调用（非持久会话）
- **进程管理**: 每次操作新建子进程，完成后销毁；串行执行
- **消息展示**: Markdown渲染 + 流式逐字显示（stream-json）
- **权限模式**: 用户可选三种模式，**默认C（交互模式）**
  - **A: 静默模式** → `--permission-mode acceptEdits`，自动允许，无提示
  - **B: 通知模式** → `--permission-mode acceptEdits`，自动允许，日志区显示操作记录
  - **C: 交互模式（默认）** → `--permission-mode default`，GUI弹窗让用户确认/拒绝
- **tool_use事件展示**: stream-json中的工具调用事件（Read/Write/Bash等）显示在日志区
- **与initem关系**: initem配置settings.json权限（交互模式），GUI权限模式（-p模式）独立控制，互补不冲突

## M4: 项目管理面板
- 项目名称 & 路径展示
- 当前步骤状态（进度条/S1-S6状态灯）
- 快速操作（一键执行常用命令）
- 待办事项列表（从memory-log读取）

## M5: 命令快捷操作区
- 一键按钮覆盖：stat / si / disc / new / verify / result / arch / sum / help

## M6: 串口工具整合
- S5串口监控器嵌入GUI（保留独立运行能力）

## M7: 日志与输出面板
- 日志格式: Markdown渲染 + 纯文本切换
- 日志来源: Claude回复 + 本地日志文件
- 日志搜索: 关键词过滤
- 日志导出: 保存为.md/.txt文件

## M8: MCP工具管理（P2）

## M9: 外部技能整合平台（P1）

## 架构定位
- **EM-SKILL**: 仍然是Claude Code技能（核心逻辑不变）
- **GUI**: 桌面启动器/仪表盘（可视化操作入口）
- **触发方式**: 桌面快捷方式为主，VS Code Extension + `/em gui` 命令为辅
