# 命令: /em migrate-state (一键生成 state.md)

## 功能
从旧版 `memory-log.md` + `project-spec.md` 提取关键信息，生成 ≤50 行的 `state.md`，让 `/em rec` 体感瘦身。

## 触发
```
/em migrate-state
```

## 何时用
- 第一次升级到瘦身版 rec 时（一次性操作）
- 当前 `state.md` 与实际状态偏离严重，想重新生成时

## 执行流程

1. **【检测】** 必须存在 `<STATE_DIR>/memory-log.md` 或 `<STATE_DIR>/project-spec.md`，否则提示先 `/em init`
2. **【提取】** 按以下规则填模板：

| state.md 字段 | 来源 |
|---|---|
| 项目名 | `project-spec.md` 标题 |
| 类型 | `project.json.type`，无则按检测：有 `tools/build-keil` 或芯片关键字 → `embedded`，否则 `general` |
| 当前步骤 | `project-spec.md` Meta 的「当前步骤」 |
| 更新时间 | `memory-log.md` 快速恢复信息 |
| 会话 | `memory-log.md` 当前会话 |
| 下一步动作 | `memory-log.md` 会话历史 → 最近一条会话的 `下一步` |
| 最近 3 条决策 | `memory-log.md` 关键决策 → 倒序取前 3 |
| 阻塞项 | `problem-log.md` 状态为 `open` 的 P0/P1 → 取标题前 3 行 |

3. **【写入】** 生成 `<STATE_DIR>/state.md`（如已存在询问覆盖）
4. **【生成 project.json】** 如不存在则按检测结果生成（用户可改）
5. **【报告】** 输出生成的 state.md 内容（让用户检查）

## 安全性
- ✅ **只读取，不修改** 旧文件（memory-log/project-spec/problem-log 原样保留）
- ✅ 生成失败不留半成品（先写到 `state.md.tmp` 再 rename）
- ✅ 已存在 state.md 时询问：覆盖 / 备份后覆盖（`state.md.bak`）/ 取消

## 输出格式

```
🔁 state.md 已生成 — <STATE_DIR>/state.md

────── 内容预览 ──────
<state.md 全文>
──────────────────────

✅ 项目类型: <general|embedded>
✅ 当前步骤: S<N>
✅ 提取决策: 3 条
✅ 阻塞项: <N> 条

下次 /em rec 将直接读这个文件（≤50 行）。

如发现遗漏，可用 /em stat -v 查询完整历史后手动补充 state.md。
```

## 相关文件
- `commands/rec.md` — 瘦身版 rec
- `templates/state.md` — state.md 模板
- `commands/migrate.md` — 旧版深度迁移（独立流程）
