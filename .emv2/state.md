# state.md — embedded-project-manager-v2

## Meta
- **项目**: embedded-project-manager-v2 (EM-SKILL 元仓库)
- **类型**: learning ⚠️ 试用模式（meta-skill 本质保留在 project.json.is_meta）
- **当前步骤**: S14 ✅ 完成 + learning 插件试用（主题 `iic` 已启动）
- **更新时间**: 2026-07-13
- **会话**: sess-20260713-001

## 下一步动作
1. /em learn status — 查看 iic 主题进度
2. /em learn verify iic l2 — 进入 L2 Pack 阶段（需先完成 L1 调研：bib.json ≥ 3 条 + knowledge.md ≥ 50 行）
3. （试用完成后）还原 project.json.type = "general"

## 最近 3 条关键决策
- [2026-07-13] S14: 学习模式作为 plugins/learning/ 物理解耦，遵循 v3.0 通用核零业务原则
- [2026-07-13] S14: 学习状态目录归用户项目（.em/learning/state.md），插件只提供 schema
- [2026-06-03] EM-SKILL v3.0：通用核 + plugins/embedded/ 物理解耦

## 阻塞项 / 待办
- [ ] S10-E L2 用户端到端验证（沿用 S10）
- [ ] S12: 串口监控+initem 优化（原 S11，被本轮重构顺延）

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
