# state.md — embedded-project-manager-v2

## Meta
- **项目**: embedded-project-manager-v2 (EM-SKILL 元仓库)
- **类型**: general (meta-skill repo)
- **当前步骤**: S11  ✅ 完成（重构 + 双子代理验收 + 路径残留修复）
- **更新时间**: 2026-06-03
- **会话**: sess-20260603-001

## 下一步动作
1. 同步 EM-SKILL 到 ~/.claude/skills/（之前选择跳过；如改主意：`cp -r EM-SKILL ~/.claude/skills/`）
2. /em arch S11 → 打 tag v0.11.0 → 生成 CHANGELOG
3. 完成 S10-E L2 用户端到端验证（OTA 项目）— 沿用旧任务

## 最近 3 条关键决策
- [2026-06-03] EM-SKILL v3.0：通用核 + plugins/embedded/ 物理解耦
- [2026-06-03] new 三档分流借鉴 superpower（轻 5min / 中 15min / 重 45min）
- [2026-06-03] 状态文件三拆：state.md + sessions/ + decisions.md（rec 体感瘦身 5×）

## 阻塞项 / 待办
- [ ] S10-E L2 用户端到端验证（沿用 S10）
- [ ] S12: 串口监控+initem 优化（原 S11，被本轮重构顺延）

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
