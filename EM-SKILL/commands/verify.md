# 命令: /em verify (准备验证)

## 功能
生成人工验证请求 (HVR)，并启动S5串口工具

## 触发
```
/em verify s<编号>    # 如 /em verify s7
```

**步骤参数使用 new 命令分配的 S 编号**（如 S7），详见 new.md。

## 执行流程

1. 读取项目当前步骤
2. 🔄 **更新状态**：当前子步骤 🚧 开发中 → 🔄 验证中
3. 🔄 **更新 Meta**：当前步骤: S7-A(验证中)
4. 生成 HVR 文件（增强版）
5. 保存到 `.emv2/checkpoints/HVR-<步骤>-<序号>.md`
6. 启动S5串口工具
7. 输出验证清单

## HVR 文件

- 生成到 `.emv2/checkpoints/HVR-<步骤>-<序号>.md`
- HVR 模板和工作流细则详见 `workflows/hvr-workflow.md`

## S5工具启动（串口调试）

```bash
start "" "EM-SKILL\tools\serial-mcp\start.bat"
```
GUI程序启动后独立运行，AI继续其他工作。

## 相关文件
- workflows/hvr-workflow.md - HVR工作流细则（含模板和流程图）
