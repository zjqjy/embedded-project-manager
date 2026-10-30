# plan — S22-setup-onboarding

> 给外部用户/AI agent 的一条命令环境自检+修复。中档（R0 两轮澄清 + R1/R2 对话 + R3 落盘，2026-10-30）。

## 方案

### 需求理解（R0 Q→A，用户已确认）

| # | 问题 | 结论 |
|---|------|------|
| 1 | 交付形态 | `/em setup` 自检+修复命令（不做纯文档）；AI agent 也能跑 |
| 2 | 平台范围 | v1 定双平台 → **v2 修订：Codex CLI 纳入**（sweep 源 + 引擎备选） |
| 3 | initem 重叠 | **合并**：initem 职责迁为 embedded 插件检查组，命令废弃为 `/em setup --embedded` 别名 |
| 4 | 蒸馏引擎依赖 | 自动发现链 claude → codex exec → 手动模式降级，外部用户没装 claude 也能用 |
| 5 | 交互形态 | **A+C 混合**：默认非交互（agent 友好，JSON+人话双输出），`--guide` 向导逐项问 |
| 6 | 自动改配置边界 | hook 注册自动写入用户配置，**改前必备份**（`.bak-时间戳`），JSON 合并式插入不覆盖既有 hook |

### 候选方案（R1）与选定理由

- **A. 检查项注册表 + 插件追加**（混入 C 的 `--guide` 向导）✅ 选定
  - 检查项模块化（每项独立函数、三态输出），插件经 `_loader.py` 声明 `provides.setup_checks` 追加检查组；embedded 注册组 = 原 initem 职责
  - 混合理由：合并原则（检查项化）是本需求本质；C 的交互友好作为 `--guide` 模式叠加，默认保持 agent 可消费的非交互态
- B. 单文件自检脚本：否——嵌入式逻辑进通用核，违背合并原则，插件无法扩展
- C. 纯交互向导：否——AI agent 会被交互卡住，与 agent 可消费目标冲突

### 关键技术点

1. **检查项框架**：每项 `check() -> {id, name, state: ok|fix|guide|info, detail, fix?()}`；runner 聚合执行 → ✅就绪 / 🔧已自动修 / 📋需人工（附精确命令）；输出 machine-readable JSON + 人话表格双形态；`--guide` 对 🔧/📋 项逐项问（问答由执行命令的会话 AI 承担，脚本只提供逐项模式）；`--smoke` 才跑真实蒸馏冒烟（默认不花 token）
2. **引擎发现链**：`shutil.which("claude")` + 最小 headless 冒烟 → `ai_cmd = claude -p --model haiku`；无 → 探测 `codex exec` 可用性 → `ai_cmd = codex exec`；均无 → 手动模式（`ai_cmd` 留空，vault/入队/ask 照常，报告提示蒸馏走 `/em digest` 需先配引擎）
3. **hook 自动注册**：读现有配置 → 检查同命令是否已注册 → 缺则 JSON 合并式插入（**不覆盖既有 hook**，如 buddy_bridge）→ 备份原文件 `.bak-<时间戳>` → 写回。三处：ZCode `~/.zcode/cli/config.json` 的 `events.Stop`（入队）+ `events.SessionStart`（蒸馏触发）、`~/.claude/settings.json` 的 `hooks.SessionEnd`
4. **Codex sweep 源**：`~/.codex/sessions/` 存在 → `~/.em/config.json` 的 `transcript_sources` 追加 `{"name":"codex","path":"~","glob":".codex/sessions/**/*.jsonl","format":"jsonl"}`（幂等）
5. **插件检查组机制**：`plugins/_loader.py` 新增 `provides.setup_checks` 声明类型（值 = 检查模块路径）；setup.py 经 loader 发现并调用其 `register_checks()` 获得检查项列表；embedded 插件注册组 = 原 initem 四块职责（权限配置/工具路径探测/OpenOCD 下载/CLAUDE.md 触发器），重活仍调既有 `detect_tools.py` 等脚本——移位不重造
6. **initem 别名化**：`initem.md` 重写为薄指针（`/em initem` = `/em setup --embedded`），老习惯不断
7. **验收基线**：本机全绿走查；破坏性测试（删 hook 注册 → 检出并修复+备份存在）；降级测试（PATH 摘 claude → 引擎链走 codex/手动）；用户点头

## 拆分

依赖线性 A→B→C→D。

| ID | 名称 | 内容 | 验证方式 | 预估 |
|----|------|------|----------|------|
| S22-A | setup 框架+基础组 | 框架（三态/双输出/--guide/--smoke）+ 基础检查组（Python≥3.10/git/vault 有效性→引导 init） | 本机跑三态正确；--guide 逐项问；JSON 可消费 | M |
| S22-B | 引擎+hook+Codex | 引擎发现链；hook 三处自动注册（备份）；Codex sweep 源幂等写入 | 删 hook→检出修复+备份；PATH 摘 claude→降级链正确；伪 .codex→源写入 | M |
| S22-C | embedded 检查组 | `_loader.py` 加 `provides.setup_checks`；embedded 注册 initem 职责；`initem.md` 别名化 | `--embedded` 真实跑本机 EIM 环境；initem.md 是别名指针 | M |
| S22-D | 挂表+实测验收 | `commands/setup.md` + SKILL.md 挂表 + initem 废弃说明；全平台走查 | 全绿走查 + 用户点头 | S |

### 拆分关键决策
- 框架先行（A）：B/C 的检查项都是往框架里挂
- initem 重活（detect_tools.py 等）只调用不重写——移位不重造
- 实现全部在 dev 仓，完成后用户同步 install
