# state.md — 项目当前状态（rec 默认只读这个）

## Meta
- **项目**: embedded-project-manager（EM-SKILL 元仓库）
- **类型**: general
- **当前步骤**: S21-A 🚧
- **更新时间**: 2026-10-30
- **会话**: sess-20261030-001

## 下一步动作
1. 编码 S21-A（triage.py 砍落卡改写 pending_lines.jsonl 队列）→ 完成后 `/em verify s21-a`
2. 实现依据：`docs/research/2026-10-30-conversation-knowledge-capture.md` + `features/S21-distill-archive/plan.md`

## 最近 3 条关键决策
- [2026-10-30] S21 蒸馏引擎 = claude CLI headless（`--ai-cmd` 可配），零新基础设施
- [2026-10-30] 卡结构 = 3 硬规则 + 模板族 5+1；蒸馏卡直接落快捕，NONE 默认
- [2026-10-30] 触发 = SessionStart 后台补跑（6h 门控）；多源 = push hook + pull sweep

## 阻塞项 / 待办
- [ ] S21-C 需用户在 ZCode / Claude Code 注册 hook（注册片段 C 步骤交付）
- [ ] 存量 17 张 hook 垃圾卡待 S21-D 清理

## 详细资料指针
| 内容 | 文件 |
|------|------|
| 步骤全表 | `features/README.md` |
| 决策/会话时间线 | `journal.md` |
| S21 计划 | `features/S21-distill-archive/plan.md` |

<!-- state.md 由 init/new/result/arch 命令自动维护；用户也可直接编辑 -->
