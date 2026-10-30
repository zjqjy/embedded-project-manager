# 命令: /em initem（已合并入 /em setup）

> **S22 起废弃为别名**：本命令 = `/em setup --embedded`。
> 原「工具初始化」职责（Claude 权限配置 / 工具路径探测 / OpenOCD 检测 / CLAUDE.md 触发器注册）
> 已迁为 embedded 插件的 setup 检查组（`plugins/embedded/setup_checks.py`），由 `/em setup` 统一驱动。
> 本文件保留为兼容指针；历史版本职责细节见 git log（S13-S17 时代）。

## 触发
```
/em initem        # 等价于 /em setup --embedded
```

## 执行流程
1. 跑 `python "<SKILL_DIR>/tools/setup.py" --embedded`
2. 通用组 + 嵌入式组一起体检（✅就绪 / 🔧已自动修 / 📋需人工）
3. 芯片工具组合锁定（原 initem 步骤5）**不在自检范围**——项目级一次性动作，走 `/em init` / `/em si`

## 迁移说明
- 检查项实现：`plugins/embedded/setup_checks.py`（`register_checks(apply)`）
- 重量级脚本仍复用既有资产：`tools/lib/register_claude_md.py`、`commands/scripts/detect_tools.py`
- OpenOCD 自动下载不再内联：setup 只检测并给下载指引（重量级操作不静默）
