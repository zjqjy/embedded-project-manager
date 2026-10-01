# 子流程拆分 - EM-SKILL GUI

**需求ID**: 20260428-em-skill-gui
**日期**: 2026-04-28

## S7 - EM-SKILL GUI 桌面应用

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

## 验证方式

| 子步骤 | 验证方法 |
|--------|---------|
| S7-A | 编写测试脚本，确认Claude CLI能通过stdin/stdout正常交互 |
| S7-B | `cargo tauri dev` 能正常启动空白窗口 |
| S7-C | 在GUI中输入命令，能看到Claude实时回复 |
| S7-D | 打开项目后正确显示步骤状态 |
| S7-E | 点击按钮等效于输入对应命令 |
| S7-F | Claude返回的Markdown格式正确渲染 |
| S7-G | 串口收发功能正常工作 |
| S7-H | VS Code侧栏显示GUI面板 |
| S7-I | 能注册/加载外部技能模块 |
