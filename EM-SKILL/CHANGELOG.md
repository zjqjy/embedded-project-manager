# Changelog

> EM-SKILL 项目变更日志 | 由 `tools/git-changelog/changelog_gen.py` 自动生成
>
> 格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
> commit 遵循 EM 自定义规范 `[Sx] type: message`。
>
> 手动重新生成：
> ```bash
> python EM-SKILL/tools/git-changelog/changelog_gen.py
> ```

## [Unreleased]

### Changed
- **[S18] new 三档「追问先行、落盘最后」**: 修复「AI 不问人工就直接写计划文档」——`/em new` 三档现在必经 **R0 追问轮**（新 `workflows/new-clarify.md`：一次一问、选择题优先、预算轻≤2/中≤5/重每子系统≤3、免问也须理解摘要确认）；硬闸门写入 `commands/new.md` 公共规则（理解未确认禁止出方案草稿/写文件）。中档 R1/R2 改纯对话，落盘合并为 R3 统一批次（plan.md 一次成文，产物形状不变）；重档阶段2 改追问式、补硬闸门、status.json 路径与文件集对齐 v4（plan.md 合并 brainstorm/milestones 两章）。产物形状零变化，verify/result/arch 零改动；状态同步目标按项目形态自适应（v4: features/README.md + journal.md；v3: project-spec.md + decisions.md）。依据调研 `docs/research/2026-10-10-clarify-before-write.md`（github/spec-kit /clarify 模板原文 + obra/superpowers brainstorming + OpenSpec）。
- SKILL.md / help.md / disc.md: 三档描述同步 R0 语义；help.md 中档产物陈旧描述修正（brainstorm.md+milestones.md → plan.md）。
- **【breaking·v4.0】状态目录 v4 结构**（feature/s17-v4 分支演练通过后生效）: `discussion/`+`checkpoints/` 收敛为 `features/S<N>-<slug>/`（plan.md + hvr.md + README 状态卡）；`sessions/`+`decisions.md`+`memory-log.md` 合并为 append-only `journal.md`；`project-spec.md` 转为 `features/README.md` 索引。活文件 11 类 → 2 个（state.md + journal.md）。命令文档（new/verify/result/init/stat/rec/arch）与 SKILL.md 布局已切 v4 路径；v3 项目由 `/em migrate` §v4 一键迁移。管家项目迁移映射三段式提交：28edd20（move）/ a85dc26（consolidate）/ ce26da1（slim）。

### Added
- **[S18] 工作流**: 新增 `workflows/new-clarify.md` — R0 需求澄清追问轮（三档共用）：一次一问、选择题优先、Why it matters、问题预算、免问路径、理解摘要确认门；依据为 spec-kit `/clarify` 与 superpowers `brainstorming` 的共识实践。
- **[S18] 调研**: 新增 `docs/research/2026-10-10-clarify-before-write.md` — 需求澄清实践调研（spec-kit clarify 模板原文 / superpowers brainstorming / OpenSpec proposal），含共性提炼与 EM 映射、兼容性核对清单。
- **命令**: 新增 `/em pro` 插件问题上报命令 — 在任意项目使用 EM-SKILL 遇到 bug / 输出异常 / 缺失功能 / 文档不清时执行，把问题详情 + 源项目现场快照（state.md / problem-log.md / git 状态 / EM-SKILL 版本）追加到管家项目 `problem-log.md > 跨项目问题记录 (EM-SKILL)` 段，集中处理。**只用于 EM-SKILL 自身问题**，通用项目状态用 `/em stat` / `/em rec`。管家路径解析顺序 `$EM_PROJECT_MANAGER_HOME` → `~/.em-skill/manager-home` → 首次直接问路径（不强制新建目录）。
- **脚本**: 新增 `tools/sync-to-install.cmd` — EM-SKILL dev → install 同步脚本，使用 robocopy `/E`「只补不删」语义（不执行 rm），避免误删 install 中本地新增文件。多设备兼容：路径用 `<PROJECT_ROOT>` / `<INSTALL_ROOT>` 占位符，支持 `EM_INSTALL_PATH` 环境变量覆盖。
- **[S17-A] 命令**: 新增 `/em logs-clean` — logs/ 滚动清理（保留最新 N 份，默认 10），被 HVR/problem-log 引用的日志豁免，`--dry-run` 只预览；`--all` 连 cache/ 一起清。
- **[S17-B] 工具注册表**: 新增 `plugins/embedded/tools/registry.json` — 芯片(vendor×family) × 动词(build/flash/observe) × adapter 能力矩阵。新增芯片 = registry 加行，命令文档不随工具增长而修改。st.f1/f4、gd.f1/f4、ti.c2000 已收录。
- **[S17-C] adapter**: 新增 `adapters/build/ccs.py`（TI CCS headless 编译）与 `adapters/flash/dslite.py`（XDS100/XDS110 烧录）— L1 完成，待 slack_app（TMS320F280033 + CCS 12.5 + XDS100v2）实机验收。
- **[S17-D] 生命周期**: 新增 `docs/LIFECYCLE.md`（12 项文件生死规则总表 + v4 目标结构）与模板 `templates/journal.md` / `templates/feature-README.md`（v4 features/ 目录制 + append-only journal）。

### Changed
- **【breaking】技能触发名**: SKILL.md frontmatter `name: em-skill` → `name: em`，Claude Code 现在以 `/em` 显示和触发（之前是 `/em-skill` 或 `/EM-SKILL`）。
- **【breaking】状态目录统一 `.em/`**: `commands/init.md` / `commands/si.md` / `commands/rec.md` 不再生成或回退 `.emv2/`。v3.1+ 全新项目只创建 `.em/`。**旧 `.emv2/` 项目必须先 `/em migrate` 升级才能用新命令**。
- **CLAUDE.md（项目级）**: 重写 EM-SKILL dev/install 路径约定段，明确只改 dev、install 用「只补不删」脚本同步；路径全部改用占位符，支持 Windows / Linux / macOS。
- **[S17-A] init 最小生成**: init 只创建 state.md + project.json 两个文件 + 空目录骨架；project-spec / decisions / problem-log 改为**首次写入时自动创建**（生成要吝啬）。
- **[S17-A] 轻档不落盘**: `workflows/new-light.md` quick-plan 只留对话，默认不建 discussion 目录（`留档` 为显式例外）；`workflows/new-standard.md` 重写为 R1/R2/R3 渐进确认流，**落盘前必须用户确认**（收编 S16-A，S16 就此关闭）。
- **[S17-A] rec 硬闸门**: state.md > 50 行时 rec 拒绝加载并强制引导 `/em migrate-state`（止血，slack_app 53 行现场）。
- **[S17-A] arch 归档扩展**: problem-log closed 条目关闭 > 30 天整段移 history；state.md 超行引导 migrate-state；logs 超份数引导 logs-clean。
- **[S17-B] 工具目录重构**: `tools/build-keil|flash-openocd|serial-monitor|shared/` → `tools/adapters/{build,flash,observe}/` + `tools/lib/`（行为不变， PLUGIN.md v1.1.0 同步声明 verb + registry）。
- **[S17-B] verify 三连数据驱动**: `workflows/verify-embedded.md` 与 build/flash/serial 命令改为读 `project.json.embedded`（initem 锁定的组合）→ 查 registry 路由，不再硬编码 Keil+OpenOCD；`commands/initem.md` 新增「步骤 5: 锁定芯片工具组合」。
- **[S17-D] migrate v4**: `commands/migrate.md` 新增 v3→v4 结构收敛迁移段（discussion→features、sessions/decisions→journal 三段式 commit 边界）；命令层暂保持 v3 兼容，管家项目演练通过后统一切 v4 路径发版。
- **SKILL.md/help.md**: 通用命令计数修正 17→19（补 logs-clean）；插件命令说明统一为 S15 lazy-load 语义（不再写「type=embedded 自动加载」）。

### Fixed
- **/em pro 强制新建管家目录**: 之前首次执行时强制 3 个预设选项（EM-SKILL 目录 / 新目录 / 不记录），现改为直接问具体路径，只接受已存在 + 已 init 的目录。
- **[S17-B] _loader.py import 副作用**: 不再在 import 时替换 `sys.stdout/stderr`（曾导致 pytest 崩溃 `ValueError: I/O operation on closed file`），UTF-8 控制台修复移到 CLI 入口且改用 `reconfigure`。
- **[S17-B] 状态目录误判**: `find_state_dir()` 现要求目录含状态标记（project.json/state.md/memory-log.md）——只装了 loader 缓存的 `.em/` 不再劫持解析（元仓库双轨事故根因）；项目外运行缓存落 `~/.em-skill/cache/`。
- **[S17-B] 测试硬编码路径**: `plugins/learning/tests/test_registration.py` 的 `F:\workspace\...` 绝对路径改为相对本文件解析（多设备可跑，本机 7 个失败测试恢复）。
- **[S17-B] initem 坏引用**: `tools/shared/detect_tools.py`（不存在）→ `commands/scripts/detect_tools.py`；serial-mcp.json PYTHONPATH 指向迁移后的 `tools/lib`。
- **learning/PLUGIN.md**: 补 `version: 4.1.0`（loader 不再显示 `v?`）。

### Removed
- **[S17-B] 仓库垃圾清理**: 移除被跟踪的 `em_skill_loader.egg-info/`、`plugins/embedded/tools/serial-mcp/.emv2/`（12 个串口日志）、`.em/` 缓存目录（散落的 learning 讨论副本已抢救至 `.emv2/learning/discussion/`）；`.gitignore` 补 `.em/cache/`、`.emv2/cache/`、`*.egg-info/`。
- **[S17-B] PLUGIN.md hooks 声明**: 移除从未存在的 `hooks/log-build.sh` 声明。

### Tests
- 新增 `plugins/tests/test_registry.py`（12 用例：registry 自洽性 / adapter 文件存在 / chips 引用合法 / 旧目录清除断言）；全套 **67/67 通过**（此前因 F:\ 硬编码 + stdout 副作用长期 7 failed + 崩溃）。

### Other
- S17 讨论档案：`.emv2/discussion/20261001-s17-slim-tools-registry/`（brainstorm / milestones / research——外部工具调研裁决「默认不集成」）；HVR：`.emv2/checkpoints/HVR-S17-001.md`。
