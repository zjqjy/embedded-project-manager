# ACCEPT - 嵌入式项目场景端到端验收

- **场景**: STM32F407VET6 LED Blinker（mock 工具调用）
- **测试日期**: 2026-06-03
- **EM-SKILL 版本**: v3.0 (重构后)
- **验收员**: 子代理 B
- **项目目录**: `F:\workspace\embedded-project-manager\test-runs\embedded-blink\`

---

## 一、命令流测试

| # | 命令 | 结果 | 备注 |
|---|------|------|------|
| 1 | `/em init led-blink` | ✅ | 扫描命中 `led_blink.uvprojx` → 自动推荐 embedded；用户确认；写 `.em/` + `project.json.type=embedded`；触发 chip-learning 选 STM32F407VET6 / Keil / stlink；加载 `plugins/embedded/PLUGIN.md` |
| 2 | `/em initem` | ✅ | mock tool_config 写入 `.em/embedded/tool_config.json`（uv4 + openocd + serial_port = COM5；未真实调 detect_tools.py） |
| 3 | `/em new "LED 闪烁基础功能"` | ✅ | AI 推荐档：**重档**（启发式：embedded + 涉外设）；用户改：**中档**（"基础功能简单，中档就行"）；产出 `brainstorm.md` (3 方案) + `milestones.md` (S1-A / S1-B) |
| 4 | 编码 `main.c` | ✅ | 33 行最小 STM32F407 闪烁代码（mock，不真实编译） |
| 5 | `/em verify s1-a` | ✅ | 读 `project.json.type=embedded` → 加载 `plugins/embedded/workflows/verify-embedded.md`；mock 三连全绿：编译 `0 errors, 2 warnings, Flash≈3KB` / 烧录 `stlink, verified` / 串口抓到 `[BOOT][GPIO][LOOP]`；生成 `HVR-S1-A-001.md` 含"嵌入式执行记录"表格；commit 提议输出（用户选 n 留待 S1-B 合并） |
| 6 | `/em result S1-A-通过` | ✅ | S1-A 状态 🔄 → ✅；自动推进到 S1-B 🚧；同步 state.md / project-spec.md / HVR 决策段 |
| 7 | `/em rec`（重启视角） | ✅ | 只读 `state.md (29 行)` + `project.json (12 行)` = 41 行；正确恢复"S1-B 开发中"上下文 |

---

## 二、产出文件清单

```
test-runs/embedded-blink/
├── led_blink.uvprojx                 # init 诱饵（空文件）
├── main.c                            # 33 行 mock 嵌入式代码
├── README.md                         # 既有
├── ACCEPT-EMBEDDED-20260603.md       # 本报告
└── .em/
    ├── state.md                      # 29 行 ✅ ≤50
    ├── project.json                  # 12 行（含 embedded.chip/toolchain/interface + plugins=["embedded"]）
    ├── project-spec.md               # 步骤表含 S1 / S1-A ✅ / S1-B 🚧
    ├── decisions.md                  # 3 条决策（类型选定 / 芯片 / S1 档位）
    ├── problem-log.md                # 空骨架
    ├── embedded/
    │   └── tool_config.json          # mock 工具路径（uv4 / openocd / COM5）
    ├── sessions/
    │   └── sess-20260603-001.md      # 命令时间线
    ├── discussion/
    │   └── 20260603-led-blink/
    │       ├── brainstorm.md         # 3 方案对比（A 阻塞 / B TIM6 / C SysTick）
    │       ├── milestones.md         # S1-A / S1-B
    │       └── status.json           # level=standard, ai_recommended=deep, user_override
    ├── checkpoints/
    │   └── HVR-S1-A-001.md           # 含"嵌入式执行记录"表格 + 3 工具执行记录 + 决策段
    ├── logs/
    │   ├── build_S1-A_20260603-1228.log
    │   └── serial_S1-A_20260603-1230.log
    └── history/                      # 空
```

---

## 三、设计目标验收

| 验收项 | 期望 | 实际 | 结论 |
|--------|------|------|------|
| init 自动识别 embedded | 是（命中 `*.uvprojx`） | 命中 `led_blink.uvprojx`，推荐 embedded，用户确认 | ✅ |
| 插件 PLUGIN.md 被加载 | 是 | `project.json.type=embedded` 触发 `plugins/embedded/PLUGIN.md` 加载（已读取） | ✅ |
| 嵌入式 verify 三连 | 编译→烧录→串口 | HVR 含 build-keil / flash-openocd / serial-monitor 三行 + 启动日志 + 物理现象段 | ✅ |
| state.md ≤ 50 行 | ≤ 50 | **29 行** | ✅ |
| state + project.json ≤ 70 行 | ≤ 70 | **41 行** | ✅ |
| tools 路径在 `plugins/embedded/tools/` | 是 | 物理目录 ✅；PLUGIN.md & verify-embedded.md 全部用新路径；**但 initem.md / hvr-workflow.md / em-migration.md 仍用旧路径** | ⚠️ 部分通过 |
| HVR 含「嵌入式执行记录」表格 | 是 | `HVR-S1-A-001.md` 第 9-15 行三行表格 + 启动日志节选 + 物理现象段 | ✅ |
| 披露式加载（执行前先 Read 命令文件） | 是 | 本验收按序 Read 了 init.md / new.md / verify.md / result.md / rec.md / PLUGIN.md / initem.md / verify-embedded.md / chip-learning.md / new-standard.md / state.md / project.json | ✅ |
| AI 推重档/用户可改档 | 是 | new.md 启发式表"嵌入式+新外设→重"已命中；用户输入"中档"后流程切换 workflows/new-standard.md | ✅ |
| 嵌入式项目 rec 也只读 state.md | 是 | rec.md 第 27-29 行明确"只读 state.md + project.json"；本验收 41 行恢复成功 | ✅ |

---

## 四、发现的问题

### P1（必修）— tools 路径双轨制残留

新插件物理目录在 `plugins/embedded/tools/`，但**三处仍指向旧路径** `EM-SKILL/tools/...`，造成命令执行真实工具时会找不到：

| 文件 | 行号 | 旧路径片段 | 应改为 |
|------|------|----------|--------|
| `plugins/embedded/commands/initem.md` | 37-39 | `Bash(python */EM-SKILL/tools/build-keil/*.py)` | `Bash(python */EM-SKILL/plugins/embedded/tools/build-keil/*.py)` |
| `plugins/embedded/commands/initem.md` | 58 | `python EM-SKILL/tools/shared/detect_tools.py` | `python EM-SKILL/plugins/embedded/tools/shared/detect_tools.py` |
| `workflows/hvr-workflow.md` | 215-217 | `EM-SKILL/tools/build-keil/scripts/keil_builder.py` 等三行 | 同上加 `plugins/embedded/` |
| `templates/em-migration.md` | 89-92 | 工具表 4 行旧路径 | 同上 |
| `README.md` | 283 | `cd EM-SKILL/tools/serial-mcp` | 同上 |

**影响**：`/em initem` 第 1 步写入的 Claude 权限白名单不匹配实际工具位置；用户首次跑真实工具会被 permission ask 拦截或脚本 not found；HVR 模板字段也会写错路径，造成事故定位混乱。

### P2（建议）— tool_config 存放路径不统一

- `initem.md` 步骤 3 说"自动注册到 `%APPDATA%/em_skill/config.json`"（用户级）
- 本验收按"项目自包含"原则放在 `.em/embedded/tool_config.json`（项目级）
- 二者**没有任何文档明确优先级**。建议：
  - 全局工具路径（uv4/openocd 安装位置）→ `%APPDATA%/em_skill/config.json`
  - 项目专属（COM 口/baud/interface）→ `.em/embedded/tool_config.json`
  - 在 `initem.md` 头部补一段"两层 config"说明

### P3（建议）— PLUGIN.md 「插件加载机制」与 init.md 文案不对齐

- `init.md` 第 31 行说"自动识别 + 用户确认"
- `PLUGIN.md` 第 32 行说"自动检测特征 → 询问用户是否启用插件"
- 两者描述吻合，但 init.md 没有提到「用户拒绝采用 embedded 推荐」时的回退分支（强制 general 后能否仍手动 /em initem 启用插件？）
- 建议补一句：拒绝后仍可 `/em initem` 把 `type` 翻回 `embedded`（PLUGIN.md 第 38 行已有此能力）

### P4（轻微）— chip-learning.md 模板偏旧

- chip-learning.md 第 1-118 行**完全未被 v3.0 改动**，与新插件结构未同步
- 引用的 `~/.claude/chips.json` 路径合理，但 `init.md` 第 64 行说"chip-learning 在 init 时跑"，没有显式调用 chips.json 学习逻辑
- 建议：在 chip-learning.md 顶部加一段"由 init.md / si.md 通过披露式 Read 加载"的说明，并去掉模板里 chips.json 既存示例的「lastUsed: 2026-03-27」过时日期

### P5（极轻微）— HVR 字段「嵌入式执行记录」表格缺标准模板

- `verify-embedded.md` 第 162-177 行**定义**了该字段
- `templates/hvr-template.md` 通用模板里**未包含**这个嵌入式扩展段
- 建议：在 `templates/` 下新增 `hvr-template-embedded.md`（或在原模板加 `<!-- embedded-only -->` 占位段），让 verify 命令做差异化渲染时有源头

---

## 五、最终结论

⚠️ **部分通过**（功能层面 100% 跑通，但 tools 路径双轨制残留是必修阻断）

### 总评
- **架构层面 ✅**：通用核 vs 嵌入式插件的物理隔离非常干净；按需加载（披露式）实测可行；state.md 瘦身在嵌入式场景同样成立（29 行）。
- **新 `/em new` 三档分流 ✅**：嵌入式 + 外设 的启发式确实推到「重」，用户改「中」也能顺畅切到 `new-standard.md`，brainstorm + milestones 两文件简洁有效。
- **verify 嵌入式三连 ✅**：HVR 文件结构清晰，「嵌入式执行记录」表格 + 启动日志节选 + 物理现象段三段式齐备。
- **rec 恢复 ✅**：从零会话恢复 led-blink 项目只需 41 行（state + project.json），未触碰 HVR / 讨论 / 日志。
- **阻断项 P1 ❌**：`initem.md` 写入的权限白名单和 `hvr-workflow.md` 模板里的工具路径与实际物理目录不一致，新项目首次 `initem` + `verify` 时会触发 "command not allowed" 或 "file not found"。建议在收尾 commit 前把 P1 列表的三个文件批量替换 `EM-SKILL/tools/` → `EM-SKILL/plugins/embedded/tools/`。

### 修复建议优先级
1. **P1 必修**（10 分钟）：批量替换三个文件的旧路径
2. **P5 建议**（15 分钟）：新增 `templates/hvr-template-embedded.md` 或在通用模板加占位段
3. **P2/P3 文档**（10 分钟）：补两段文案对齐
4. **P4 极轻微**：可放到下一次小版本
