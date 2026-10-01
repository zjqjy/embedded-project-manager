# journal.md — embedded-project-manager-v2

> **append-only**：只追加条目，不修改历史；> 500 行由 `/em arch` 截出到 history。
> v4 迁移（2026-10-01）由 memory-log.md（190 行）+ 决策段压缩生成；原件：`history/2026/10/01/memory-log.md`。
> 恢复上下文：读 state.md；翻近期历史：读本文件尾部。

---

## [2026-02-25] 会话: 项目初始化，创建基本功能结构（sess-20260225-001）

## [2026-03-27] 会话: S2 实用性修复方案讨论
- 产出: features/S2-practical-fix/

## [2026-04-15] 决策: SKILL.md 重构，命令前缀统一 `/em`

## [2026-04-16] 会话: S4 芯片学习验证通过（/em si GD32F7xx 识别成功）；S6 归档机制讨论
- 产出: features/S4/hvr.md

## [2026-04-16] 决策: S6 归档目标 = memory-log + project-spec 为主

## [2026-04-17] 会话: S6 归档机制验证通过（阈值：memory-log > 600 行，其他 > 300 行）
- 产出: features/S6-arch-review/hvr.md

## [2026-04-19] 会话: S5 串口调试工具讨论 + 开发 + MCP 测试通过
- 决策: 定位 = MCP 工具 + GUI + 人-AI 协作验证；方案 C-b（tkinter + pyserial + MCP Server）
- 产出: features/S5-serial-debug/

## [2026-04-19] 决策: S5 工作流修正 — /em result 在验证阶段；失败流程 = AI 读 MCP + 人类观察 → 共同分析

## [2026-04-28] 会话: S7 EM-SKILL GUI 讨论完成（Tauri + Vue3 + CLI 管道常驻子进程；9 子步规划 S7-A~I）
- 产出: features/S7-em-skill-gui/

## [2026-04-28] 决策: S7 ⏸️ 暂停 — Windows 兼容性问题待后续版本修复，整体延后

## [2026-04-29] 会话: S9 embed-ai-tool 整合实施（A~E 完成）
- 决策: 整合模型 = EM 流程控制 + embed-ai-tool 执行；脚本并入 EM-SKILL/tools/（自包含）
- 产出: features/S9-embed-ai-tool-integration/

## [2026-04-30] 会话: S9-F 全流程验证通过（OTA 项目编译→烧录→串口）
- 修复: P0-1 detect 配置路径优先 / P0-2 auto-reset 引入 tool_config / P1-2 verify 三连 / P1-3 J-Link 烧后自运行 / P1-8 OpenOCD erase 参数 / P2 initem 权限说明
- 产出: features/S9-embed-ai-tool-integration/hvr.md

## [2026-06-02] 会话: S10 标准化+通用化+Git集成（5 阶段讨论 + A~E 子代理开发 + E 验证 L1 25/25）
- 决策: 标准化（frontmatter skill 模板）/ 通用化（.em/.emv2 双轨）/ Git（提议 commit + tag，禁 push）/ CHANGELOG 自写脚本 / 编号冲突：原 S10 串口顺延 S11
- 产出: features/S10-skill-standardize-universal-git/（plan + hvr×3）

## [2026-06-03] 会话: S11 EM-SKILL v3.0 重构（通用核解耦 + new 三档 + state 瘦身）
- 产出: features/S11/hvr.md

## [2026-07-13] 决策: S14 学习模式定位 — plugins/learning/ 物理解耦 + /em learn 子命令；学习状态归用户项目 .em/learning/，插件只出 schema
## [2026-07-13] 决策: S14 — S10 重档设计档案归档至 history/2026/07/13/S10-learning-v4-design/

## [2026-07-13] 会话: S14 学习模式整合完成（有 P3-1 失败记录，S15 解）
- 产出: features/S14-integrate-learning-v4/

## [2026-07-14] 决策: S15 插件 lazy-load（命令驱动替代 type 驱动）+ S16 中档改 R1/R2/R3 落盘前必须确认 + 阶段 3 拆 3 落盘点 + R2 方案每条限 1 句思路

## [2026-07-14] 会话: S15 lazy-load 完成（A~E，P3-1 关闭）；S16 规划落盘
- 产出: features/S15-plugin-lazy-load/（hvr×2）/ features/S16-new-flow-optimize/

## [2026-10-01] 会话: S17 瘦身 + 工具注册表四子步开发完成
- S17-A 止血包（init 减量/落盘确认门/rec 硬闸门/logs-clean）/ S17-B+C adapters + registry + TI / S17-D v4 能力
- 67/67 测试全绿；slack_app 工具组合锁定（ti.c2000 → ccs+dslite）
- 产出: features/S17-slim-tools-registry/（plan + research + hvr）

## [2026-10-01] 决策: 外部工具（debugger-mcp/Renode/Bloaty 等）默认不集成 — research.md 降级后备清单，触发条件各自注明

## [2026-10-01] 维护: v4 迁移演练（feature/s17-v4）— discussion/checkpoints → features/；memory-log/project-spec 压缩为本 journal + features/README.md 索引，原件入 history/2026/10/01/

<!-- newest 在最下，此后由 /em result / arch / 维护动作追加 -->
