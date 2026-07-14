# state.md — embedded-project-manager-v2

## Meta
- **项目**: embedded-project-manager-v2 (EM-SKILL 元仓库)
- **类型**: learning ⚠️ 试用模式（meta-skill 本质保留在 project.json.is_meta）
- **当前步骤**: S16-A 🚧 改写 `workflows/new-standard.md` 为 R1/R2/R3 渐进
- **更新时间**: 2026-07-14
- **会话**: sess-20260714-001
- **分支**: `feature/s16-new-flow-optimization`

## 下一步动作
1. 改写 `workflows/new-standard.md`（brainstorm/milestones 阶段拆 R1/R2/R3；阶段 3 拆 3 个落盘点）
2. 完成后 `/em verify s16-a` 验证 + HVR 提议 commit
3. S15-A 已编码完成（待 verify + commit），与 S16 并行推进

## 最近 3 条关键决策
- [2026-07-14] S16: 中档流程改为 R1/R2/R3 渐进对话流，**落盘前必须确认**
- [2026-07-14] S16: 阶段 3「同步状态」拆 3 个落盘点（brainstorm.md / milestones.md / state+spec+decisions）
- [2026-07-14] S16: 新分支 `feature/s16-new-flow-optimization` 隔离 EM-SKILL 元仓库改动

## 阻塞项 / 待办
- [ ] S16-A: 改写 `workflows/new-standard.md`（**当前**）
- [ ] S16-B: 用 S16 当样本回归验证
- [x] S15-A: ✅ 编码 + verify + commit (183e7c3)
- [x] S15-B: ✅ SKILL.md 路由表指针化 (9b5b70c)
- [x] S15-C: ✅ `project.json.type` 降级 + trial_mode 清理 (9b5b70c)
- [x] S15-D: ✅ 嵌入式 `enabled_when` 多文件探测移除 (9b5b70c)
- [x] S15-E: ✅ 端到端验证 + 性能对比 (9b5b70c)
- [ ] S10-E L2 用户端到端验证（沿用 S10）
- [ ] S12: 串口监控+initem 优化（原 S11，被本轮重构顺延）

## S16 计划文件
- `discussion/20260714-s16-new-flow-optimize/brainstorm.md`
- `discussion/20260714-s16-new-flow-optimize/milestones.md`

## S14 计划文件
- `discussion/20260713-integrate-learning-v4/brainstorm.md`
- `discussion/20260713-integrate-learning-v4/milestones.md`

## 已完成步骤（S14）
- [x] S14-A：学习模式插件骨架
- [x] S14-B：模板层迁入
- [x] S14-C：脚本层迁入
- [x] S14-D：插件注册与通用核文档
- [x] S14-E：S10 设计产物归档与状态收尾

## S13 计划文件
- `discussion/20260709-claude-md-initem-register/quick-plan.md`

## 详细资料指针
| 内容 | 文件 |
|------|------|
| 步骤全表 | `project-spec.md` |
| 会话历史 | `memory-log.md`（旧版兼容；建议 /em migrate-state 升级到 sessions/）|
| 决策全集 | `memory-log.md` 关键决策段 |
| 问题追踪 | `problem-log.md` |
| HVR 记录 | `checkpoints/` |
| S11 HVR | `checkpoints/HVR-S11-001.md` |
| 双场景验收 | `../test-runs/{general-cli,embedded-blink}/ACCEPT-*.md` |
| S10 学习模式 v4.1 设计档案 | `history/2026/07/13/S10-learning-v4-design/` |
| S10 学习模式 v4.1 原型 | `../em-skill-v4.1/.em/learning/`（S14-B/C 时迁入）|