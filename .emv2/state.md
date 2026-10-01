# state.md — embedded-project-manager-v2

## Meta
- **项目**: embedded-project-manager-v2 (EM-SKILL 元仓库)
- **类型**: learning ⚠️ 试用模式（meta-skill 本质保留在 project.json.is_meta）
- **当前步骤**: S17 ✅ 开发完成 + L2 收口（v4 演练进行中，分支 feature/s17-v4）
- **更新时间**: 2026-10-01
- **会话**: sess-20261001-001
- **分支**: feature/s17-v4（v4 演练）；master 停在 v3.2 + S17 全量提交

## 下一步动作
1. v4 演练 Phase 4：命令文档切 v4 路径（new/verify/result/init/SKILL 布局）+ 版本 4.0.0
2. 用户 review 本分支 → merge master → 手动 `git push`（EM 规则禁自动 push）
3. L2 余项（CCS 机器）：slack_app `/em build` → `/em flash`（命令见 features/S17-slim-tools-registry/hvr.md L2 表）
4. install 副本同步（sync-to-install.cmd /y，交互 bug 已修）

## 最近 3 条关键决策
- [2026-10-01] v4 迁移演练执行（本分支三段式 commit：move artifacts 28edd20 → consolidate journal a85dc26 → slim state）；15 个 feature 目录 + journal.md 生成，原件入 history/2026/10/01/
- [2026-10-01] S17-两步走落地: v3.2 止血包（SKILL 3.2.0）+ v4 能力交付（LIFECYCLE/migrate/journal/feature 模板）
- [2026-10-01] S17-工具组织: adapters/{build,flash,observe} + registry.json（st/gd/ti）；initem 锁定组合、verify 数据驱动；外部工具不集成

## 阻塞项 / 待办
- [ ] v4 Phase 4 命令切换（**当前**）
- [ ] 用户 review/merge feature/s17-v4；push 手动
- [ ] S17-L2 余项：CCS 机器 slack_app build/flash 实测
- [x] v4 Phase 1-3: ✅ 搬移/合并/瘦身完成（28edd20 / a85dc26）

## 详细资料指针（v4）
| 内容 | 文件 |
|------|------|
| 步骤索引 | `features/README.md`（原 project-spec.md） |
| 时间线/决策 | `journal.md`（原 memory-log.md / decisions） |
| 问题追踪 | `problem-log.md`（臃肿条目 closed-by-S17） |
| S17 全套 | `features/S17-slim-tools-registry/`（plan/research/hvr） |
