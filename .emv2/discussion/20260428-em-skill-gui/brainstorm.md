# 头脑风暴 - EM-SKILL GUI

**需求ID**: 20260428-em-skill-gui
**日期**: 2026-04-28

## 技术难点与方案

### 难点1: Claude Code CLI 管道通信
- **需要做技术验证**: Claude CLI是否支持 `--print` 非交互式模式
- 验证方法: 写测试代码，尝试 stdin/stdout 方式与 Claude 子进程通信

### 难点2: 输出实时流式显示
- **方案**: 从Claude子进程stdout按行/按块读取 → Tauri IPC推送 → Vue响应式逐字渲染

### 难点3: S5串口工具整合
- **决策**: 直接重写串口面板为Vue组件（不修改原tkinter工具）
- 原工具保留独立运行能力

### 难点4: 多平台支持
- **决策**: 第一期只做Windows，代码架构按跨平台写
- 后续用GitHub Actions CI编译多平台

### 难点5: 扩展性架构
- EM-GUI作为统一入口，后续整合embed-ai-tool各技能
- 采用模块化/插件式架构设计
