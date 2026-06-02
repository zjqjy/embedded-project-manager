# 命令: /em rec (恢复项目)

## 功能
加载项目状态

## 触发
```
/em rec [项目名称]
```

## 无参数时
使用 `get_state_dir()` 检测当前目录的状态目录（`.em/` 优先，回退 `.emv2/`）

## 有参数时
从全局索引查找并恢复项目

## 状态目录检测（S10-B 通用化）

EM 启动恢复流程时，调用统一的目录检测函数：

```python
def get_state_dir(project_root: str) -> str | None:
    """优先读 .em/，缺失时回退 .emv2/。"""
    em_dir   = os.path.join(project_root, '.em')
    emv2_dir = os.path.join(project_root, '.emv2')
    if os.path.isdir(em_dir):
        return em_dir
    elif os.path.isdir(emv2_dir):
        return emv2_dir
    return None
```

**检测结果输出示例**：

```
[EM] 检测到状态目录：.em/        # 新格式
[EM] 检测到状态目录：.emv2/      # 旧格式回退（向后兼容）
[EM] 未找到状态目录，请先运行 /em init   # 未初始化
```

## 执行流程

1. **【状态目录检测】** 调用 `get_state_dir()` 确定 `<STATE_DIR>`
   - `.em/` 优先 → 使用
   - 回退 `.emv2/` → 使用并提示「建议运行 `/em migrate` 升级到 `.em/`」
   - 都不存在 → 提示「请先运行 `/em init` 初始化项目」
2. **读取 `<STATE_DIR>/project-spec.md` 与 `<STATE_DIR>/memory-log.md`**
3. 或从全局索引查找项目信息
4. 工作空间切换至项目路径
5. 读取项目状态
6. **检测旧版格式，提供迁移选项**（详见下方「旧版迁移」）
7. 生成恢复摘要
8. 提示用户选择操作

> 📌 **目录兼容性说明**：所有读取路径用 `<STATE_DIR>/...` 表达，实际由 `get_state_dir()` 解析。
> 新项目统一使用 `.em/`，旧 `.emv2/` 项目零配置兼容。

## 旧版迁移

### 检测标准
如 `<STATE_DIR>/project-spec.md` 包含以下内容，判定为旧版：
- `### S1:` 或 `### S2:` 等独立区段
- `## 代码片段索引` 区段

### 迁移步骤

如果是旧版，在恢复摘要后询问用户是否迁移：

**用户确认后**，AI 执行：

```
1. project-spec.md:
   - 保留：Meta、问题追踪、参考文档
   - 删除：代码片段索引、HVR记录、S1-S4独立区段
   - 新增：开发步骤状态表（从S1-S4区段提取信息）

2. memory-log.md:
   - 保留：会话指纹、快速恢复信息、关键决策、会话历史
   - 删除：当前状态（重复project-spec）、待办事项、代码变更记录、调试记录

3. 迁移完成提示
```

### 迁移格式对照

| 旧版 | 新版 |
|------|------|
| `## 开发步骤` + `### S1:` 独立区段 | `## 开发步骤状态` + 表格 |
| `## 人工验证记录` | 无（移至 checkpoints/） |
| `## 代码片段索引` | 删除 |
| memory: `## 当前状态` | 删除（project-spec Meta 已有） |
| memory: `## 待办事项` | 删除 |
| memory: `## 代码变更记录` | 删除 |

## 相关文件
- commands/init.md - 初始化命令（含动态检测逻辑）
- S10-C（`em migrate`）- 旧版 `.emv2/` → `.em/` 完整迁移工具
