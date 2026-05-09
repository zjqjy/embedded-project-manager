# 需求确认 - 20260509-usage-guide

## 日期
2026-05-09

## 1. 项目 CLAUDE.md - 使用说明索引

### 内容
```markdown
## 工具使用说明

当提到以下关键词时，AI 自动查看对应命令文件：

| 关键词 | 查看文件 |
|--------|----------|
| 编译/build/编译固件 | `EM-SKILL/commands/build.md` |
| 烧录/下载/flash | `EM-SKILL/commands/flash.md` |
| 串口/监控/debug | `EM-SKILL/commands/serial.md` |
```

## 2. EM-SKILL/commands/build.md

### 内容
- 功能概述
- 调用方式（参考 verify.md）
- 参数来源
- 检测工程方法
- 结果处理
- 自动决策
- 常见错误

## 3. EM-SKILL/commands/flash.md

### 内容
- 功能概述
- 探测环境方法
- 调用方式（参考 verify.md）
- 参数来源
- 结果处理
- 自动决策
- 常见错误

## 4. EM-SKILL/commands/serial.md

### 内容
- 功能概述
- 两个工具对比（serial-mcp GUI / serial-monitor CLI）
- 完整参数示例（参考 verify.md）
- 参数说明
- 注意事项
- 常见错误

## 5. 修改 si.md 和 init.md

### 内容
在项目初始化流程中增加：
- 检查项目是否有 CLAUDE.md
- 如果没有，创建并写入使用说明索引

## 结论
✅ 确认需求内容
