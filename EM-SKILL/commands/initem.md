# 命令: /em initem (工具初始化)

## 功能
初始化 EM-SKILL 开发环境，包含：
1. 更新 Claude 权限配置
2. 探测并注册工具路径
3. 自动下载 OpenOCD（如果未安装）

## 触发
```
/em initem
```

## 执行流程

### 步骤 1: 更新权限配置

自动更新 `~/.claude/settings.json`，添加脚本执行权限：

```json
"permissions": {
  "allow": [
    "Read",
    "Glob",
    "Grep",
    "Search",
    "Bash(git:status)",
    "Bash(git:diff)",
    "Bash(npm:test)",
    "Bash(npm run:build)",
    "Bash(ls:*)",
    "Edit(**/.emv2/**/*.md)",
    "Write(**/.emv2/**/*.md)",
    "Bash(python:*)",
    "Bash(python */EM-SKILL/tools/build-keil/*.py)",
    "Bash(python */EM-SKILL/tools/flash-openocd/*.py)",
    "Bash(python */EM-SKILL/tools/serial-monitor/*.py)"
  ],
  "ask": [
    "Write(**/.emv2/discussion/**/*.md)",
    "Edit(**/.emv2/discussion/**/*.md)"
  ],
  "deny": [
    "Bash(rm:*)",
    "Bash(sudo:*)",
    "Bash(git push:*)"
  ]
}
```

### 步骤 2: 探测工具路径

```bash
python EM-SKILL/tools/shared/detect_tools.py
```

找到的工具自动注册到 `%APPDATA%/em_skill/config.json`。

### 步骤 3: 注册工具

| 工具 | config key | 必须 | 说明 |
|------|-----------|------|------|
| OpenOCD | `openocd` | ✅ 必须 | 烧录工具（未安装则自动下载） |
| Keil UV4 | `uv4` | 必须 | 编译工具（用户手动指定） |
| J-Link | `jlink` | 可选 | 烧录工具 |

未找到的工具：
- OpenOCD → 自动下载
- Keil UV4 → 提示用户手动指定
- 其他 → 提示用户手动指定

### 步骤 4: 自动下载 OpenOCD

OpenOCD 是烧录的必须工具。如果未安装，自动下载：

```bash
# 下载地址
https://github.com/xpack-dev-tools/openocd-xpack/releases

# 选择版本（如 xpack-openocd-0.12.0-7-win32-x64.zip）
# 解压到常用目录
```

## 完整输出示例

```
🔧 EM-SKILL 工具初始化

[1/4] 更新权限配置...
  ✅ permissions 已更新

[2/4] 探测工具...
  ✅ openocd: D:/OpenOCD/xpack-openocd-0.12.0-7/bin/openocd.exe
  ⚠️ uv4: 未找到（可选）
  ⚠️ jlink: 未找到（可选）

[3/4] 注册工具路径...
  ✅ openocd 已注册

[4/4] 检查 OpenOCD...
  ✅ OpenOCD 可用

━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 初始化完成！

已注册工具：
  - openocd: D:/OpenOCD/xpack-openocd-0.12.0-7/bin/openocd.exe
```

---

## Python 环境检查

### 检查流程
```
1. 检查 Python 是否安装（python --version）
   └─→ 无 → 显示安装指南，终止
   └─→ 有 → 继续

2. 检查依赖是否安装（pip show）
   ├─→ pyserial
   └─→ mcp

3. 未安装 → pip install
   ├─→ 成功 → ✅
   └─→ 失败 → 提示手动安装
```

### 依赖列表
| 依赖 | 用途 |
|------|------|
| pyserial | S5 串口工具 |
| mcp | MCP SDK |

### 输出示例

#### 情况1: 无 Python
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

#### 情况2: 有 Python，依赖已安装
```
🔍 检查 Python 安装...
✅ Python 3.12.3 已安装

🔍 检查 MCP 工具依赖...
✅ pyserial 已安装
✅ mcp 已安装

✅ 环境就绪！
```

#### 情况3: 有 Python，依赖未安装
```
🔍 检查 Python 安装...
✅ Python 3.12.3 已安装

🔍 检查 MCP 工具依赖...
❌ pyserial 未安装
❌ mcp 未安装

📦 正在安装依赖...
✅ pyserial 安装成功
✅ mcp 安装成功

✅ 环境就绪！
```

#### 情况4: pip 安装失败
```
🔍 检查 Python 安装...
✅ Python 3.12.3 已安装

🔍 检查 MCP 工具依赖...
❌ pyserial 未安装
❌ mcp 未安装

📦 正在安装依赖...
❌ pyserial 安装失败

⚠️ 手动安装提示:
请在命令行执行:
  pip install pyserial mcp

或使用国内镜像:
  pip install pyserial mcp -i https://pypi.tuna.tsinghua.edu.cn/simple
```
