# 命令: /em initem (工具初始化)

## 功能
1. 检查并更新 `~/.claude/settings.json` 配置
2. 检查 Python 环境
3. 安装 MCP 工具依赖（pyserial, mcp）

## 触发
```
/em initem
```

## 为什么需要执行这个？

执行 `/em initem` 后，EM 工具将获得以下基础权限：

| 权限 | 效果 |
|------|------|
| `Read` | 读取文件 |
| `Glob` | 查找文件 |
| `Grep` | 搜索内容 |
| `Search` | 网络搜索 |
| `Bash(git:status)` | 查看 Git 状态 |
| `Bash(git:diff)` | 查看 Git 差异 |

**好处**：
- ✅ 减少交互确认，提升效率
- ✅ 工具能正常使用基础功能
- ✅ 防止权限不足导致的操作失败

## 需要确保的 permissions 配置

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
      "Bash(ls *)",
      "Edit(**/.emv2/**/*.md)",
      "Write(**/.emv2/**/*.md)"
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

## 输出示例

### 首次运行（无配置）
```
🔧 工具初始化

检查 ~/.claude/settings.json...
- 文件不存在，创建中...
- 备份: ~/.claude/settings.json.bak
- 添加基础权限配置...

✅ 配置完成！

效果：
  - 基础权限配置 ✓
  - 减少确认交互，提升效率 ✓
```

### 已配置
```
🔧 工具初始化

检查 ~/.claude/settings.json...
✅ 已有完整权限配置，无需重复配置
```

### 配置异常
```
🔧 工具初始化

检查 ~/.claude/settings.json...
⚠️ 检测到权限配置不完整
- 缺少: npm:test, npm run:build
- 是否修复？[是] [否]
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
