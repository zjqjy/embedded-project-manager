# state.md — 项目当前状态（rec 默认只读这个）

## Meta
- **项目**: embedded-project-manager（EM-SKILL 元仓库）
- **类型**: general
- **当前步骤**: S22-A 🚧
- **更新时间**: 2026-10-30
- **会话**: sess-20261030-001

## 下一步动作
1. 编码 S22-A（setup.py 框架 + 基础检查组 + --guide）→ 完成后 `/em verify s22-a`
2. 依据：`features/S22-setup-onboarding/plan.md`

## 最近 3 条关键决策
- [2026-10-30] S22 架构 = 检查项注册表+插件追加（A），交互 = --guide 向导（C 混入）
- [2026-10-30] /em initem 废弃为 /em setup --embedded 别名，职责经 provides.setup_checks 由 embedded 插件注册
- [2026-10-30] 蒸馏引擎自动发现链 claude → codex exec → 手动降级；hook 注册改前必备份

## 阻塞项 / 待办
- [ ] S21 隔夜实战验收（用户侧）
- [ ] github 推送时好时坏，提交后注意补推

## 详细资料指针
| 内容 | 文件 |
|------|------|
| 步骤全表 | `features/README.md` |
| 决策/会话时间线 | `journal.md` |
| S21 计划 | `features/S21-distill-archive/plan.md` |
| S22 计划 | `features/S22-setup-onboarding/plan.md` |

<!-- state.md 由 init/new/result/arch 命令自动维护；用户也可直接编辑 -->

