# HVR — S17 EM-SKILL 瘦身 + 工具注册表（A/B/C/D 四子步）

**步骤**: S17（A 止血包 / B 工具 adapter 化 / C TI 支持 / D v4 结构收敛）
**验证时间**: 2026-10-01
**验证人**: Claude（L1 自动验证）+ zjq（L2 待验收）
**关联问题**: problem-log.md「2026-09-12 长期使用后项目文件臃肿、自动维护机制缺失」open 条目
**讨论目录**: `discussion/20261001-s17-slim-tools-registry/`

---

## 验证目标（对照 milestones.md）

- S17-A 止血包：init 减量 / 轻档不落盘 / 中档落盘确认门 / rec 硬检查 / logs-clean / problem-log 归档
- S17-B 工具 adapter 化：目录重构 + registry.json + initem 锁定组合 + verify 数据驱动 + 测试全绿
- S17-C TI：ccs.py + dslite.py + registry ti.c2000
- S17-D v4：生命周期总表 + journal/feature 模板 + migrate v4 路径

---

## 验证结果（L1 自动）

### ✅ 单元测试 67/67

| 测试文件 | 覆盖 | 结果 |
|---|---|---|
| plugins/tests/test_loader.py | S15 loader（16 用例，回归） | 16/16 |
| plugins/tests/test_registry.py | **S17-B 新增**：registry 结构 / adapter 文件存在 / chips 引用合法 / ti 路由 / 旧目录清除 | 12/12 |
| plugins/learning/tests/test_registration.py | 注册一致性（**修复 F:\ 硬编码**后首次全过） | 11/11 |
| plugins/learning/tests/test_tools.py + test_templates.py | learning 工具（装 markdown 依赖后全过） | 28/28 |

### ✅ S17-A 行为验证

| 项 | 证据 |
|---|---|
| init 最小生成 | commands/init.md 步骤 3 改为「只建 state.md + project.json + 空目录」，产物 = 2 文件 |
| 轻档不落盘 | workflows/new-light.md 流程改为对话内计划，`留档` 为显式例外 |
| 中档落盘确认门 | workflows/new-standard.md 重写为 R1/R2/R3，三个落盘点逐一确认（收编 S16-A） |
| rec 硬检查 | commands/rec.md 步骤 3：>50 行拒绝继续 + 引导 migrate-state |
| logs-clean | commands/logs-clean.md 新命令（滚动 N 份 + HVR 引用豁免 + --dry-run） |
| problem-log 归档 | commands/arch.md：closed > 30 天整段移 history |

### ✅ S17-B 结构验证

| 项 | 证据 |
|---|---|
| 目录重构 | `tools/adapters/{build,flash,observe}/` + `tools/lib/`；旧 build-keil/flash-openocd/serial-monitor/shared 已删（test_registry 断言） |
| registry.json | st.f1/st.f4/gd.f1/gd.f4/ti.c2000 全路由测试通过 |
| 命令文档数据驱动 | build.md/flash.md/serial.md/verify-embedded.md/initem.md 全部改为「读 project.json.embedded → 查 registry」 |
| PLUGIN.md v1.1.0 | tools 声明带 verb；移除从未存在的 hooks/log-build.sh；changelog 记录 |
| loader 修复 | ① import 不再替换 stdout（pytest 崩溃根因）② find_state_dir 要求状态标记（.em 只剩缓存不再劫持）③ 项目外缓存落 ~/.em-skill/cache |
| 旧路径残留 | 全仓 grep 0 残留（history/discussion 归档除外） |
| adapter 冒烟 | 5/5 `--help` 通过（keil/openocd/serial/ccs/dslite）；迁移中漏改的 `tool_config` sys.path 候选（shared→lib）已补并被冒烟逮住修复 |
| SKILL 计数 | commands/*.md = 19 = SKILL.md 表 19 行 ✓（原 17 计数错误一并修正） |

### ✅ S17-C 冒烟（无 TI 硬件环境）

| 调用 | 结果 |
|---|---|
| `python adapters/build/ccs.py --detect` | ✓ 语法/路径探测正常降级（本机无 CCS，slack_app 机器命中 C:\ti 扫描） |
| `python adapters/flash/dslite.py --detect` | ✓ 同上 |
| registry.ti.c2000 路由测试 | ✓ build→ccs, flash→dslite |

### ✅ S17-D 交付物

- `docs/LIFECYCLE.md` — 12 项生命周期规则表 + 命令收尾义务 + v4 目标结构
- `templates/journal.md` + `templates/feature-README.md` — v4 新模板
- `commands/migrate.md` 新增「v4 结构收敛迁移」：映射表 / 三段式 commit 边界 / 错误处理 / 与命令切换的分步策略

### ✅ 顺带修复（review 遗留，S17 范围内）

- `.gitignore` 补 `.em/cache/` `.emv2/cache/` `*.egg-info/`
- 删除被跟踪的垃圾：`em_skill_loader.egg-info/`、`serial-mcp/.emv2/`（12 个串口日志）、`.em/`（缓存 + 散落 learning 副本，副本已抢救到 `.emv2/learning/discussion/`）
- learning/PLUGIN.md 补 `version: 4.1.0`（loader 不再显示 v?）
- initem.md 修复坏引用 `tools/shared/detect_tools.py` → `commands/scripts/detect_tools.py`

---

## ⏳ L2 待用户验收（2026-10-01 收口进展见✅）

| 项 | 验收方式 | 状态 |
|---|---|---|
| 71 变更 commit | ✅ 已分 4 批提交：fb79970（S16 既有工作）/ 84782ae（S17-A）/ c82b3e5（S17-B+C）/ c007395（S17-D+状态），工作区干净，提交后 67/67 复测通过 | ✅ 完成 |
| slack_app `/em initem` 锁定组合 | ✅ 已按 registry ti.c2000 写入 `slack_app/.em/project.json.embedded`（build:ccs + Release + prj / flash:dslite + prj/targetConfigs/TMS320F280033.ccxml），JSON 与引用文件校验通过（该仓库的 commit 由用户自行处理） | ✅ 完成 |
| rec 硬闸门体感 | ✅ 触发条件实测成立：slack_app state.md = 52 行 > 50（只读验证）；文案体验待用户下次 /em rec 确认 | 🟡 条件确认 |
| slack_app `/em build` → `/em flash` | ❌ **本机无 CCS**（C:\ti 仅有 C2000Ware devtools，无 eclipsec/dslite；CCS 12.5.0 在另一台开发机）。待该机执行：`python <SKILL>/plugins/embedded/tools/adapters/build/ccs.py --project prj --configuration Release` → `python <SKILL>/plugins/embedded/tools/adapters/flash/dslite.py --artifact prj/Release/<file>.out --ccxml prj/targetConfigs/TMS320F280033.ccxml --reset-after` | 🔴 阻塞：硬件/CCS 在他机 |
| logs-clean 实操 | slack_app logs/ 当前 0 文件（无可清对象）；管家 .emv2/logs 有 3 个历史串口日志可演练（命令设计要求用户确认删除，未代办） | 🟡 待用户实操 |
| v4 迁移演练 | migrate v4 段的映射预览**按设计需用户逐项确认**（S17-A 自家落盘确认门），且建议在 feature/s17-v4 分支执行 | 🟡 设计上需用户参与 |

## 结论

✅ **S17 四子步 L1 验证全部通过**（67/67 测试 + 结构断言 + 冒烟），L2 实机验收项已列出。
建议 commit（见 verify.md 提议规则，含大量删除需用户 review）。
