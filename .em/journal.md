# journal.md — embedded-project-manager 时间线

> **append-only**：只追加条目，不修改历史；旧条目由 `/em arch` 截出到 history。
> 恢复上下文：读 state.md；翻近期历史：读本文件尾部 30 条。

## [2026-10-30 14:50] 决策: S21 立项——对话知识自动蒸馏入库 + 快捕区自维护（中档）
- 痛点：triage.py 纯启发式，17 张待确认卡 0 张可用
- 选定方案 A：headless CLI 蒸馏（claude -p，`--ai-cmd` 可配）；否决直连 API（密钥面）、会话内软约定（不可靠）
- 拆分：A 队列 → B 蒸馏器 → C 接线+多源 → D 存量清理+验收，线性依赖

## [2026-10-30 14:55] 会话: R0-R3 完成 + GitHub 调研归档 + .em/ 骨架首次建立
- 调研：claude-mem（机制 + prompt 全文）+ mem0 #4573 垃圾率审计；15 项借鉴、6 项明确不借
- 产出：`features/S21-distill-archive/plan.md`、`docs/research/2026-10-30-conversation-knowledge-capture.md`、`.em/` 骨架
- 下一步：编码 S21-A

## [2026-10-30 16:00] 步骤: S21 A-D 编码完成，存量清理完毕
- A: triage.py 重写为入队器（书签+指针+角色，model_io 只取新增轮次）；B: distill.py 蒸馏器（sweep/门控/三合一prompt/NEW-UPDATE-NONE协议/need_context扩窗/过程卡快照覆盖/日志+熔断）；C: hook_session_start.py + /em digest + SKILL.md 挂表；D: 19 张存量 hook 卡重蒸判定后删除（df84d58）
- 实测：无用材料 NONE、决策卡达 LX 标准、过程卡同主题合并稳定（2 次 UPDATE 0 新建）、门控跳过/放行正确、后台无窗口（CREATE_NO_WINDOW 修复弹窗 bug）
- 下一步：用户 sync install + 注册 hook + 隔夜验收 → /em verify s21
