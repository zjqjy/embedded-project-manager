# state.md — embedded-project-manager-v2

## Meta
- **项目**: embedded-project-manager-v2 (EM-SKILL 元仓库)
- **类型**: learning ⚠️ 试用模式（meta-skill 本质保留在 project.json.is_meta）
- **当前步骤**: S17 ✅ A/B/C/D 开发完成（L1 全绿）— L2 实机验收待做
- **更新时间**: 2026-10-01
- **会话**: sess-20261001-001
- **分支**: master（含大量删除的变更集，commit 前请 review；v4 演练时切 feature/s17-v4）

## 下一步动作
1. **review + commit**：70 个文件变更（S17 + 此前 pro/sync-to-install 未提交项），建议按 HVR-S17-001 提议分批 commit
2. L2 验收（slack_app）：/em initem 锁 TI 组合 → /em build → /em flash（ccs/dslite 首战）+ rec 硬闸门体感 + logs-clean
3. v4 演练：本仓库 feature 分支跑 migrate v4 段 → 通过后统一切命令路径发 v4.0
4. install 副本同步：dev 领先（S17 + humanize 回流），跑 sync-to-install.cmd /y（注意其交互确认有 cmd 延迟展开 bug，review 遗留未修）

## 最近 3 条关键决策
- [2026-10-01] S17-两步走落地: v3.2 止血包（生命周期规则+生成减量，零破坏，SKILL 3.2.0）+ v4.0 换骨能力已交付（LIFECYCLE + migrate v4 段 + journal/feature 模板）；命令层暂保持 v3 兼容，管家项目演练后才切换
- [2026-10-01] S17-工具组织: `tools/adapters/{build,flash,observe}/` + `registry.json`（st/gd/ti 三厂商收录）；initem 锁定组合写 project.json.embedded，verify 三连数据驱动；外部工具裁决不集成（research.md 后备清单）
- [2026-10-01] S17-工程修复: _loader import 副作用 / find_state_dir 状态标记 / 测试 F:\ 硬编码 / 仓库垃圾（egg-info、嵌套 .emv2 日志、.em 缓存）全清，67/67 全绿

## 阻塞项 / 待办
- [ ] S17-L2: slack_app 实机验收（ccs/dslite + rec 闸门 + logs-clean）
- [ ] S17-v4: 管家项目 migrate v4 演练 → 命令切换发版
- [ ] install 同步（sync 脚本确认 bug 修复后再跑）
- [x] S17-A/B/C/D: ✅ 开发完成（HVR: checkpoints/HVR-S17-001.md）

## 详细资料指针
| 内容 | 文件 |
|------|------|
| S17 讨论与调研 | `discussion/20261001-s17-slim-tools-registry/` |
| S17 验证记录 | `checkpoints/HVR-S17-001.md` |
| 生命周期总表（新） | `EM-SKILL/docs/LIFECYCLE.md` |
| 工具能力矩阵（新） | `EM-SKILL/plugins/embedded/tools/registry.json` |
| 步骤全表 | `project-spec.md` |
| 问题追踪 | `problem-log.md`（臃肿条目已 closed-by-S17）|
