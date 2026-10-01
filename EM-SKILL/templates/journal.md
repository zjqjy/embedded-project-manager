# journal.md — <项目名> 时间线

> **append-only**：只追加条目，不修改历史；旧条目由 `/em arch` 截出到 history。
> v4 起合并 sessions/ + decisions.md + memory-log.md 三个职责。
> 恢复上下文：读 state.md；翻近期历史：读本文件**尾部 30 条**。

## 使用规则

- 每条 = 一个事件（会话收尾 / 决策 / 问题闭环 / 步骤通过 / 归档）
- 格式：`## [YYYY-MM-DD HH:MM] <类型>: <一句话>` + ≤5 行正文
- 类型：`会话` / `决策` / `问题` / `步骤` / `维护`
- > 500 行 → `/em arch` 把头部截出到 `history/journal-<date>.md`

## 条目模板

```markdown
## [YYYY-MM-DD HH:MM] 会话: <本次干了什么>
- 产出: <文件/commit>
- 下一步: <一句话>

## [YYYY-MM-DD HH:MM] 决策: <决策一句话>
- 理由: <一句话>（详见 features/S<N>-<slug>/plan.md）

## [YYYY-MM-DD HH:MM] 问题: <problem 摘要> → <闭环结论>

## [YYYY-MM-DD HH:MM] 步骤: S<N> ✅ <一句话>（HVR: features/S<N>-<slug>/hvr.md）

## [YYYY-MM-DD HH:MM] 维护: <logs-clean / journal 截出 / 归档>
```

---

<!-- 正文从下方开始追加， newest 在最下 -->
