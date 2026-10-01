<!-- 本文件由 v4 迁移（2026-10-01）从 project-spec.md 转换；原件：history/2026/10/01/project-spec.md -->

# features/ — 步骤索引

> 每个主步骤一个目录（`S<N>-<slug>/`），入口是各目录 README 状态卡；历史步骤整目录归档至 history/。
> 无步骤号的早期一次性讨论在 `_orphan/`。

## 步骤总表

| 步骤 | 名称 | 状态 | 日期 | 目录 |
|------|------|------|------|------|
| S1 | 存量接入 | ✅ 完成 | 2026-02-25 | —（无产物目录） |
| S2 | 需求对齐讨论流程 | ✅ 完成 | 2026-03-27 | [S2-practical-fix](S2-practical-fix/) |
| S3 | HVR 工作流增强 | ✅ 完成 | 2026-04-16 | [S3](S3/) |
| S4 | 芯片学习机制 | ✅ 完成 | 2026-04-16 | [S4](S4/) |
| S5 | 串口调试工具 | ✅ 完成 | 2026-04-19 | [S5-serial-debug](S5-serial-debug/) |
| S6 | 文件归档机制 | ✅ 完成 | 2026-04-17 | [S6-arch-review](S6-arch-review/) |
| S7 | EM-SKILL GUI 桌面应用 | ⏸️ 暂停 | 2026-04-28 | [S7-em-skill-gui](S7-em-skill-gui/) |
| S8 | 优化项目文件模板 | ✅ 完成 | 2026-04-28 | [S8-optimize-templates](S8-optimize-templates/) |
| S9 | embed-ai-tool 整合 | ✅ 完成 | 2026-04-30 | [S9-embed-ai-tool-integration](S9-embed-ai-tool-integration/) |
| S10 | 标准化+通用化+Git集成 | ✅ 完成（L2 待用户） | 2026-06-02 | [S10-skill-standardize-universal-git](S10-skill-standardize-universal-git/) |
| S11 | v3.0 重构（通用核解耦+三档+瘦身） | ✅ 完成 | 2026-06-03 | [S11](S11/) |
| S12 | 串口监控+initem 优化（顺延） | 📋 待开发 | — | — |
| S13 | initem 注册 CLAUDE.md 触发器 | ⏸️ 暂停 | 2026-07-09 | [S13-claude-md-initem-register](S13-claude-md-initem-register/) |
| S14 | 整合学习模式 v4.1 | ✅ 完成（有 P3-1，S15 解） | 2026-07-13 | [S14-integrate-learning-v4](S14-integrate-learning-v4/) |
| S15 | 插件 lazy-load 重构 | ✅ 完成 | 2026-07-14 | [S15-plugin-lazy-load](S15-plugin-lazy-load/) |
| S16 | 中档 R1/R2/R3 渐进确认 | ⏸️ 并入 S17-A | 2026-07-14 | [S16-new-flow-optimize](S16-new-flow-optimize/) |
| S17 | 瘦身 + 工具注册表（两步走） | ✅ 开发完成（L2 收口） | 2026-10-01 | [S17-slim-tools-registry](S17-slim-tools-registry/) |

## 全局检查点（Gates）
- [x] G1: S2-S6 全部开发完成
- [x] G2: 全流程验证通过
- [x] G3: 文档更新完成
- [ ] G4: 用户验收通过（S17 L2 收口中）

## _orphan（无步骤号的一次性讨论）

`20260416-auto-read-emv2` / `20260416-initem-optimization` / `20260416-skill-tab-completion` / `20260419-initem-python-check` / `20260428-new-step-id` / `20260428-step-state-machine` / `20260509-usage-guide`

## 参考文档
- Skill 安装路径: `~/.claude/skills/EM-SKILL`（占位符约定见 CLAUDE.md）
- 生命周期总表: `EM-SKILL/docs/LIFECYCLE.md`
- 工具能力矩阵: `EM-SKILL/plugins/embedded/tools/registry.json`
- 归档索引: history/index.md
