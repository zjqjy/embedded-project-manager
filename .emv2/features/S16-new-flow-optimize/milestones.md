# milestones: S16-new-flow-optimize

## 选定方案
**R1/R2/R3 渐进对话流**：
- brainstorm 阶段：R1 需求复述（2-3 句）→ R2 方案发散（2-3 候选，各 1 句）→ R3 落盘 brainstorm.md
- milestones 阶段：R1 子步骤草案（1-3 个）→ R2 验证+决策 → R3 落盘 milestones.md
- 阶段 3「同步状态」拆 3 个落盘点：R1 写 brainstorm.md → R2 写 milestones.md → R3 同步 state/spec/decisions

## 子步骤

### S16-A: 改写 `workflows/new-standard.md`
- **内容**：brainstorm 阶段拆 R1/R2/R3；milestones 阶段拆 R1/R2/R3；阶段 3 同步状态拆 3 个落盘点；每轮标注「只输出 X」约束
- **依赖**：无
- **验证**：grep `R1` `R2` `R3` 标记 ≥ 6 处；每轮输出格式有明确"只输出 X"约束；阶段 3 拆 3 个落盘点
- **预估**：S

### S16-B: 用 S16 当样本回归验证
- **内容**：用当前 S16 这次讨论作为样本，对照新流程复盘每个 R 是否有确认闸门、每轮输出是否克制
- **依赖**：S16-A
- **验证**：能列出"哪一步原本要甩 / 现在分了几轮 / 用户注意力曲线"
- **预估**：S

## 关键决策
- [2026-07-14] S16: 中档流程改为 R1/R2/R3 渐进对话流，**落盘前必须确认**
- [2026-07-14] S16: 阶段 3「同步状态」拆 3 个落盘点（brainstorm.md / milestones.md / state+spec+decisions）
- [2026-07-14] S16: brainstorm R2 候选方案每条限 1 句思路 + 1 句优劣，控制注意力负载