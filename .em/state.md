# state.md — 项目当前状态（rec 默认只读这个）

## Meta
- **项目**: embedded-project-manager（EM-SKILL 元仓库）
- **类型**: general
- **当前步骤**: S21-D 🚧（编码完成，待实战验收）
- **更新时间**: 2026-10-30
- **会话**: sess-20261030-001

## 下一步动作
1. 用户同步 install：`EM-SKILL\tools\sync-to-install.cmd /y`（**旧 triage 仍在 install 上，不同步会继续产垃圾卡**）
2. 用户注册 hook：ZCode SessionStart + Claude Code SessionEnd（片段在 `EM-SKILL/commands/digest.md`）
3. 隔夜自然触发后看卡质量 → `/em verify s21`

## 最近 3 条关键决策
- [2026-10-30] S21 蒸馏引擎 = claude CLI headless（`--ai-cmd` 可配），零新基础设施
- [2026-10-30] 卡结构 = 3 硬规则 + 模板族 5+1；蒸馏卡直接落快捕，NONE 默认
- [2026-10-30] 全部子进程加 CREATE_NO_WINDOW（后台蒸馏弹 cmd 窗口的修复）

## 阻塞项 / 待办
- [ ] install 未同步（live hook 还是旧版 triage）
- [ ] 实测验收：真实隔夜场景卡质量由用户判定

## 详细资料指针
| 内容 | 文件 |
|------|------|
| 步骤全表 | `features/README.md` |
| 决策/会话时间线 | `journal.md` |
| S21 计划 | `features/S21-distill-archive/plan.md` |

<!-- state.md 由 init/new/result/arch 命令自动维护；用户也可直接编辑 -->

