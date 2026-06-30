# 讨论：initem Python 自检与环境依赖安装

## 基本信息
- **日期**: 2026-04-19
- **需求ID**: 20260419-initem-python-check
- **当前状态**: 讨论中

## 功能需求

### 背景
当前 `/em initem` 只检查 settings.json permissions 配置，不涉及 Python 环境。

### 期望功能
1. **Python 自检**: 检查系统是否安装 Python
2. **无 Python 处理**: 给出安装链接、方法、注意事项
3. **有 Python 处理**: 自动安装 MCP 工具的环境依赖

---

## 决策结果

| 问题 | 决策 |
|------|------|
| Q1: Python 版本 | Python 3.12 |
| Q2: 依赖列表 | pyserial, mcp（只有这两个） |
| Q3: 安装方式 | A - pip 直接安装 |
| Q4: 错误处理 | 手动安装提示 |
| Q5: 安装链接 | 需要（官网+注意事项） |

---

## 预期输出示例

### 情况1: 无 Python
```
🔍 检查 Python 安装...
❌ 未检测到 Python

📥 Python 安装指南:
- 下载: https://www.python.org/downloads/
- 版本: Python 3.12
- 注意事项:
  1. 勾选 "Add Python to PATH"
  2. 选择 Customized Installation
  3. 勾选 pip

安装后请重新运行 /em initem
```

### 情况2: 有 Python，依赖已安装
```
🔍 检查 Python 安装...
✅ Python 3.10.11 已安装

🔍 检查 MCP 工具依赖...
✅ pyserial 已安装
✅ mcp 已安装

✅ 环境就绪！
```

### 情况3: 有 Python，依赖未安装
```
🔍 检查 Python 安装...
✅ Python 3.10.11 已安装

🔍 检查 MCP 工具依赖...
❌ pyserial 未安装
❌ mcp 未安装

📦 正在安装依赖...
✅ pyserial 安装成功
✅ mcp 安装成功

✅ 环境就绪！
```
