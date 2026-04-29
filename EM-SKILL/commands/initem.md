# 命令: /em initem (工具初始化)

## 功能
检查并更新 `~/.claude/settings.json` 配置，确保 EM 工具的基础 permissions 配置完整。

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

## embed-ai-tool 工具路径注册

首次使用 embed-ai-tool 整合功能前，需要注册工具路径。AI 会尝试自动探测，未找到的工具需要用户手动指定。

### 自动探测

```bash
python EM-SKILL/commands/scripts/detect_tools.py
```

AI 执行此命令后：
- 找到的工具 → 自动注册到全局配置（`%APPDATA%/em_skill/config.json`）
- 未找到的工具 → 提示用户手动指定路径

### 手动注册（自动探测失败时）

如果某个工具未自动找到，用户可提供路径，AI 执行注册：

```bash
python -c "
import sys; sys.path.insert(0, r'embed-ai-tool')
from shared.tool_config import set_tool_path
set_tool_path('<工具名>', r'<完整路径>', global_=True)
print('✅ 已注册')
"
```

### 验证注册

```bash
python -c "
import sys; sys.path.insert(0, r'embed-ai-tool')
from shared.tool_config import list_tools
for name, info in list_tools().items():
    print(f'  {name}: {info[\"path\"]} ({info[\"source\"]})')
"
```

### 新增 permissions 配置

同时需要在 `~/.claude/settings.json` 的 `permissions.allow` 中添加脚本执行权限：

```json
"Bash(python *)"
```

### 注册的工具

| 工具 | config key | 说明 |
|------|-----------|------|
| Keil UV4 | `uv4` | UV4.exe 路径 |
| OpenOCD | `openocd` | openocd.exe 路径 |
| J-Link | `jlink` | JLink.exe 路径 |
