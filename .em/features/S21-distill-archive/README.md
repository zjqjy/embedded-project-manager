# S21-distill-archive — 对话知识自动蒸馏入库 + 快捕区自维护

> 状态卡：feature 目录的入口，`/em pi` 与 `/em stat -v` 扫描本行

| 字段 | 值 |
|------|-----|
| 状态 | 🚧 开发中 |
| 档位 | 中 |
| 日期 | 2026-10-30 |
| HVR | `hvr.md`（verify 后存在） |

## 一句话目标
聊天只管聊，vault 自己长出 LX 卡质量的结构化卡：垃圾不再产生、过程卡不重复、冷卡自动归档、转正只出建议。

## 关键决策（≤3 条）
- [2026-10-30] 蒸馏引擎 = claude CLI headless（`--ai-cmd` 可配），零新基础设施
- [2026-10-30] 卡结构 = 3 硬规则 + 模板族 5+1；蒸馏卡直接落快捕，NONE 默认
- [2026-10-30] 触发 = SessionStart 后台补跑（6h 门控）；多源 = push hook + pull sweep

## 产物清单
- `plan.md` — 方案 + 拆分
- `hvr.md` — 验证请求与结果（待 verify）

<!-- feature 完成时：整个目录由 /em result 提示 mv 到 history/（LIFECYCLE #8） -->
