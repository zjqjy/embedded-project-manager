# 命令: /em rec (恢复项目)

## 功能
最小代价加载项目当前状态。**只读 `state.md`** 一个文件（≤50 行），按需查询详情。

## 触发
```
/em rec [项目名称|路径]
```

## 加载策略（瘦身设计）

| 加载层 | 文件 | 何时读 |
|--------|------|--------|
| L0 默认 | `<STATE_DIR>/state.md` | 总是（≤50 行） |
| L1 类型 | `<STATE_DIR>/project.json` | 总是（< 20 行） |
| L2 详情 | `project-spec.md` / `memory-log.md` / `problem-log.md` / `sessions/<id>.md` | **按需**（用户问到才读） |

> 旧版项目（无 state.md）→ 自动回退读 `memory-log.md`（兼容路径），并提示运行 `/em migrate-state` 一键生成 state.md。

## 执行流程

1. **【状态目录】** 调用 `get_state_dir()` → `<STATE_DIR>`
   - `.em/` 优先 → 使用
   - 回退 `.emv2/` → 使用并提示「建议运行 `/em migrate` 升级到 `.em/`」
   - 都无 → 提示「请先 `/em init`」
2. **【最小加载】** 读 `<STATE_DIR>/state.md`（若存在）+ `<STATE_DIR>/project.json`（若存在）
3. **【旧版兼容】** state.md 不存在 → 读 `memory-log.md` 前 ~30 行（会话指纹+快速恢复信息+当前状态），跳过会话历史
4. **【嵌入式插件】** 若 `project.json.type == "embedded"` 或检测到 `.emv2/embedded/` → 加载 `plugins/embedded/PLUGIN.md`（仅文件名提示，不展开内容）
5. **【生成摘要】** 输出 5 行内的恢复摘要
6. **【交互】** 提示下一步可选动作；用户问详情时再加载 L2

## 摘要输出格式

```
📂 项目恢复完成 — <项目名>
状态目录: <STATE_DIR>  (general | embedded)
当前步骤: S<N> — <状态>
下一步:   <state.md 中第 1 条 next-action>
详情命令: /em stat -v   /em sessions   /em pi
```

## 旧版项目迁移提示（一次性，不强制）

如检测到旧版（无 state.md），输出：

```
ℹ️  检测到旧版结构（无 state.md，已回退读 memory-log.md）
   建议运行  /em migrate-state   一键生成 state.md（瘦身后体感更快）
   也可继续用旧文件，不影响任何命令。
```

## 旧版格式深度迁移（独立子命令）

如 `project-spec.md` 含 `### S1:` 或 `## 代码片段索引` → 提示运行 `/em migrate`（已存在）。

## 设计原则
- ❌ rec 不再一次性灌入 memory-log/project-spec/problem-log 全部内容
- ❌ rec 不再尝试解析会话历史（移到 `/em sessions`）
- ✅ rec 只回答「我现在该做什么」，详情按需查
- ✅ 旧项目零破坏，新项目立即体感

## 相关文件
- `templates/state.md` — state.md 模板
- `commands/stat.md` — 详细状态查询（含 `-v` 详情模式）
- `commands/sessions.md` — 会话历史浏览（新增）
- `commands/migrate-state.md` — 一键生成 state.md（新增）
- `commands/migrate.md` — 旧版深度迁移（已有）
