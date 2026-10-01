# brainstorm: S17-slim-tools-registry

> 中档（standard）| 2026-10-01 | 来源：仓库 review + 两轮方向讨论 + GitHub 调研

## 需求理解

EM-SKILL 长期使用后暴露两类结构性问题，本步骤一并治理：

1. **项目文件臃肿、无废弃机制**（problem-log 2026-09-12 open 条目，slack_app 现场：state.md 53 行超标、project-spec.md 只增不减、logs/ 无清理、11 类文件职责不清）。
2. **嵌入式工具组织不可扩展**——现有 build-keil + flash-openocd 只覆盖 GD/ST（Keil+OpenOCD），slack_app（TI C2000 + CCS + XDS110）已无法套用；且芯片/工具链/探针三个维度耦合在命令文档里。

外部参考（调研结论）：spec-kit（按 feature 组织、每 feature 3 文件、生命周期=git 分支）、superpowers（单一 journal.md append-only）、PlatformIO（platform.json 声明式工具包注册表）、probe-rs/pyOCD（target 定义文件驱动芯片支持）。共同思想：**能力是数据，不是代码/文档**。

## 候选方案

### 方案 A: 两步走 — v3.2 止血 + v4.0 换骨（推荐）
- **v3.2 止血包（零破坏）**：init 生成减量（只建 state.md + project.json，其余首次写入才建）；轻档不落盘；rec 硬检查 state.md > 50 行（拒绝继续并引导 migrate-state）；新增 `/em logs-clean`；problem-log closed 条目归档。
- **v4.0 换骨（一次性 breaking）**：结构收敛 11 类 → 6 类（state.md / journal.md / problem-log.md / features/<S<N>-slug>/ / history/ / logs/），生命周期规则表随新结构落地；与工具 adapter 重构**捆绑**为同一版本，一条 `/em migrate` 完成迁移。
- 优点：止血立即可用（slack_app 直接受益）；breaking 只发生一次；规则在新旧结构下都不白做
- 缺点：v4.0 前有过渡期，两套结构并存约 1-2 个版本

### 方案 B: 一次性 v4.0 大爆炸
- 优点：无过渡期脏状态
- 缺点：改动面 = 全部命令 md + 工具层 + migrate，周期长且中途不可用；历史教训——`.em/`/`.emv2/` 双轨就是半迁移的产物，大爆炸更容易烂尾

### 方案 C: 只做工具注册表，不动文件结构
- 优点：最小改动
- 缺点：臃肿问题（用户主诉 1）不解决；problem-log open 条目继续挂起

## 推荐

**方案 A**。理由：两个问题优先级不同（臃肿每天都在疼，工具扩展随新项目来），拆成「立即止血 + 攒一次性换骨」风险最低；且文件结构与工具注册表同属「数据驱动化」一个思想，v4.0 捆绑做避免两次 breaking。

## 关键技术点

1. **工具三层正交模型**：芯片(vendor×family) × 构建器(keil/ccs/cmake-gcc) × 探针(openocd/jlink/dslite) + 观测(serial)；`tools/adapters/{build,flash,debug,observe}/` + `registry.json` 数据驱动；initem 时锁定组合写 `project.json.embedded`；verify 三连读组合，不再猜。
2. **工具角色三分法**（决定新工具归宿）：能进 verify 循环的 → adapters；一年几次人主导的 → workflows how-to 文档；需要人手的（示波器/逻辑分析仪）→ HVR 检查点。口诀：**能进 verify 的进 adapters，低频的进 workflows，人手的进 HVR**。
3. **外部工具默认不集成**（2026-10-01 用户裁决）：GitHub 调研清单（debugger-mcp / Renode / Bloaty 等）均不进当前 verify 循环——现有「编译→烧录→串口→人观察」闭环已被自有工具覆盖，TI 缺口只能自写。工具部分的价值在**组织现有的**（registry + adapter 抽象），不在引入新的；research.md 降级为后备清单，出现具体痛点再按需引入单项。
4. **结构收敛**（v4.0）：features/<S<N>-slug>/ 承载 plan+hvr（合并 discussion/ + checkpoints/）；journal.md 合并 sessions/ + decisions.md + memory-log.md；归档单位 = 整目录 mv。
5. **S16 处置**：S16-A（new-standard R1/R2/R3 落盘前确认）目标被 S17-A 覆盖，S16 关闭并入 S17-A。

## 关键决策（同步 state.md）
- [2026-10-01] 采用方案 A 两步走：v3.2 止血（零破坏）+ v4.0 换骨（一次性 breaking，与工具重构捆绑）
- [2026-10-01] 工具组织改 adapter 注册表，registry.json 数据驱动；外部工具默认不集成（调研清单全部降级后备，见 research.md 裁决记录）
- [2026-10-01] S16 剩余目标并入 S17-A，S16 关闭
