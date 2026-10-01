# milestones: S17-slim-tools-registry

## 选定方案
方案 A「两步走」：v3.2 止血包（零破坏，立即见效）→ v4.0 结构收敛 + 工具注册表（一次性 breaking，独立分支）。工具组织采用三层正交 + adapter 注册表；新工具「集成优先于自研」。

## 子步骤

### S17-A: 止血包 v3.2（零破坏）
- 内容：init 生成减量（只建 state.md + project.json，空表头文件首次写入才建）；轻档 quick-plan 不落盘；中档落盘前确认（收编 S16-A R1/R2/R3）；rec 硬检查 state.md ≤ 50 行（超标拒绝并引导 /em migrate-state）；新增 `/em logs-clean`（logs/ 滚动保留 N 份，默认 10）；problem-log closed > 30 天条目移 history/
- 依赖：无
- 验证：/em verify s17-a —— 在本元仓库 + slack_app 双场景跑 rec/logs-clean；state.md 53 行场景触发硬检查
- 预估：M

### S17-B: 工具 adapter 化 P0（行为不变重构）
- 内容：tools/ 重构为 adapters/{build,flash,observe}/ + lib/；现有 keil_builder.py / openocd_flasher.py / serial_monitor.py 挪入并抽统一接口（build(project)→log、flash(image,target)→log）；新建 registry.json（能力矩阵 st/gd 先行）；chips.json 并入 registry；initem 锁定组合写 project.json.embedded = {vendor, family, build, flash, flash_args}；verify-embedded.md 三连改读组合驱动
- 依赖：无（可与 S17-A 并行）
- 验证：/em verify s17-b —— 现有 GD/ST 项目回归：编译→烧录→串口三连与重构前行为一致；_loader 与 PLUGIN.md provides 声明同步
- 预估：M

### S17-C: TI 支持（ccs.py + dslite.py）
- 内容：新增 adapters/build/ccs.py（CCS headless 编译）+ adapters/flash/dslite.py（XDS110 烧录）；registry 加 ti.c2000（slack_app TMS320F280033 实测）
- 依赖：S17-B
- 验证：/em verify s17-c —— slack_app 走 /em build + /em flash 全流程；HVR 记录
- 预估：M
- 备注：外部工具（debugger-mcp/Renode/Bloaty 等）2026-10-01 裁决**默认不集成**，research.md 降级为后备清单

### S17-D: v4.0 结构收敛（breaking，独立分支）
- 内容：features/<S<N>-slug>/ 目录制（plan+hvr 同址，合并 discussion/+checkpoints/）；journal.md（append-only，合并 sessions/+decisions.md+memory-log.md）；活文件收敛到 state.md + journal.md 两个；生命周期规则表进 docs/（各命令收尾引用同一张表）；/em migrate 重写支持 v2→v4 一键迁移；本仓库自身先迁移 dogfood
- 依赖：S17-A（规则先立）+ S17-B（同版本捆绑）
- 验证：/em verify s17-d —— 迁移脚本在本仓库 + slack_app 双场景通过；新项目 init 产物 ≤ 2 文件；rec 只读 state.md
- 预估：L

## 关键决策（记入决策日志）
- [2026-10-01] S17 拆 A/B/C/D 四子步；A 与 B 可并行，D 必须等 A+B 完成
- [2026-10-01] v4.0 为一次性 breaking（feature/s17-v4 分支），杜绝再次出现双轨并存
