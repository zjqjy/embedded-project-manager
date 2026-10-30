# S22-setup-onboarding — 一条命令的环境自检+修复（给外部用户/AI agent）

> 状态卡：feature 目录的入口，`/em pi` 与 `/em stat -v` 扫描本行

| 字段 | 值 |
|------|-----|
| 状态 | 🚧 开发中 |
| 档位 | 中 |
| 日期 | 2026-10-30 |
| HVR | `hvr.md`（verify 后存在） |

## 一句话目标
别人（人或 AI agent）拿到 EM-SKILL 跑一条 `/em setup`，环境从零到达"可直接用"：能自动修的自动修，不能修的给精确到命令的指引。

## 关键决策（≤3 条）
- [2026-10-30] 架构 = 检查项注册表 + 插件追加（A），交互 = `--guide` 向导模式（C 混入）；默认非交互 agent 友好
- [2026-10-30] `/em initem` 废弃为 `/em setup --embedded` 别名；嵌入式检查组由 embedded 插件经 `provides.setup_checks` 注册
- [2026-10-30] 蒸馏引擎自动发现链：claude CLI → codex exec → 手动模式降级；hook 注册改前必备份

## 产物清单
- `plan.md` — 方案 + 拆分
- `hvr.md` — 验证请求与结果（待 verify）

<!-- feature 完成时：整个目录由 /em result 提示 mv 到 history/（LIFECYCLE #8） -->
