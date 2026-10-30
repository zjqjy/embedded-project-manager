# plan — S21-distill-archive

> 对话知识自动蒸馏入库 + 快捕区自维护。中档（R0 澄清 + R1/R2 对话 + R3 落盘，2026-10-30）。

## 方案

### 需求理解（R0 Q→A，用户已确认）

| # | 问题 | 结论 |
|---|------|------|
| 1 | 档位 | 中档 |
| 2 | "定时整理归档"边界 | 快捕区自维护：待确认积压清理、冷卡归档、转正只出建议（不落地、不全库体检） |
| 3 | 触发机制（AI 代答，用户追认） | SessionStart 后台补跑，6h 门控可配；不用系统定时任务 |
| 4 | 蒸馏卡落卡状态 | 直接落快捕，不落待确认；质量靠入口闸门，冷卡归档兜底 |
| 5 | 内容标准（用户强调） | "有用"是硬标准：无用 → 零产出是正常结果；宁少勿多写进验收 |
| 6 | 进行中主题 | 过程卡：状态快照（目标/已定/进展/待办/坑），同主题永远合并一张，不写流水账 |
| 7 | 内容来源 | 多源：push（ZCode Stop / Claude Code SessionEnd hook）+ pull（sweep 声明式配置） |
| 8 | 完整性 | 队列 = 书签（行 + transcript 指针 + 角色标记），蒸馏时回读 ±5 行；need_context 二次扩窗；原文永不删 |
| 9 | token 约束 | 攒批：6h 内 N 会话一次调用，约 3-6k token/次，单次队列 80 行封顶 |

### 候选方案（R1）与选定理由

- **A. headless CLI 子进程蒸馏** ✅ 选定：`claude -p`（本机实测可用），`--ai-cmd` 可配。零密钥管理、管线除 AI 步骤外全确定性、triage.py docstring 里 V2 规划的原落地
- B. 直连 API：否——引入密钥管理面，为省 20s 冷启动不值
- C. 会话内 AI 软约定：否——软约定不可靠（用户原则：机制用确定性 hook），蒸馏插在正事前打扰

### 关键技术点

1. **管线**：`triage.py`（Stop hook）砍落卡改写队列 `~/.em/pending_lines.jsonl`（行内容 + transcript 指针 + 行号 + 角色标记，按内容哈希幂等）→ `distill.py` 门控触发（`~/.em/distill_state.json`：上次蒸馏时间、sweep 文件状态、规则版本）→ headless 蒸馏 → `capture.py` 落卡 → git commit → 清队列
2. **蒸馏 prompt 三合一配方**：LX 卡范例（结构基准）+ claude-mem 模板（身份句 "Record what was LEARNED, not what you are doing"、WHEN TO SKIP 负面清单、facts 微规则：自包含/禁代词/带文件名数值、skip 精确格式）+ mem0 教训（输入隔离：绝不混入 vault 已有卡内容；NONE 默认；负面 few-shot）
3. **输出动作协议（严格 JSON，解析失败重试 1 次，再失败丢弃并记日志，不带病入库）**：
   - `NEW` — 新知识卡（type / skeleton / tags / sensitive）
   - `UPDATE` — 过程卡：dedup 定位旧卡 → 新快照覆盖，不新建
   - `NONE` — 默认动作，带 reason（零产出是正常结果）
   - `need_context` — 书签信息不够 → 机械层回读 ±20 行补一次调用，最多两轮
4. **卡结构定稿**：3 硬规则（标题即结论；首段 ≤40 字核心结论供 /em ask snippet；禁套话）+ 模板族 5+1（踩坑排查/决策结论/速查/how-to/过程跟踪 + sensitive 标记）。frontmatter 新增 `type`、可选 `files:`；检测到密钥/凭证 → 明文脱敏（前4后4）+ `#sensitive` 标签（AGENTS.md 硬约束）
5. **自维护**（每天最多一次，同触发点，纯规则零 token）：待确认积压处理；surfaced_count=0 超 30 天 → 已归档；高价值卡 → 转正建议报告（AI 不动正式目录）
6. **手动**：`/em note` 不动（即时全量蒸馏）；新增 `/em digest`（跳门控清积压 + 跑自维护 + 汇报 `~/.em/distill.log` 上次错误）
7. **可靠性**：hook 永不阻塞会话（异常退出 0）+ 全部异常追加 `~/.em/distill.log`（静默失败出口——claude-mem 自审 132 个吞异常反模式的教训）
8. **多源**：push = ZCode Stop（已通）+ Claude Code SessionEnd（C 步骤交付注册片段）；pull = `~/.em/config.json` 新增 `transcript_sources`（目录 glob + 简化声明式字段映射，claude-mem codex schema 翻译），按 mtime+size 增量，状态按文件记录并带规则版本号（未来规则升级可重扫旧文件）
9. **验收基线**：同一 transcript 蒸馏 3 次出卡稳定；一次隔夜积压出 0-2 张且每张值得留（出一堆 = 不合格）；LX 卡标准人工验收（用户点头）

### 借鉴清单摘要

15 项借鉴（claude-mem 机制/prompt/数据模型/运维/评测 + mem0 反馈循环教训）、6 项明确不借（常驻 worker、SQLite/向量库、PostToolUse 逐条调 AI、CloudSync、read-gate、open-core）。全文见 `docs/research/2026-10-30-conversation-knowledge-capture.md`。

## 拆分

依赖线性 A→B→C→D，每步独立可 verify。

| ID | 名称 | 内容 | 验证方式 | 预估 |
|----|------|------|----------|------|
| S21-A | 队列改造 | triage.py 砍落卡改写队列；记录=行+指针+角色；幂等 | 喂真实 transcript → 队列有候选行、vault 零新卡、重复跑不重复入队 | S |
| S21-B | 蒸馏器 | distill.py：门控状态 + 三合一 prompt + 动作协议 + 严格校验/重试/need_context + 过程卡合并 + 日志 | 无用材料 0 卡；有料达 LX 标准；过程卡合并不新建；同 transcript 3 次稳定 | M |
| S21-C | 触发接线+多源+手动 | SessionStart 后台补跑入口；transcript_sources sweep；`/em digest` 命令定义 + SKILL.md 挂表；双平台 hook 注册片段 | 改状态模拟隔夜触发、6h 内跳过、digest 全链路、sweep 增量正确 | M |
| S21-D | 存量清理+实战验收 | 17 张垃圾卡引用原文重蒸（有料成卡/没料删）；首轮自维护；真实隔夜场景用户验收 | `hook分拣：` 垃圾卡清零、待确认清零、用户点头 | S |

### 拆分关键决策
- A 先行且独立可验：蒸馏器未上线前队列先止血（不再产垃圾卡）
- D 含一次性数据迁移：旧管线 17 张卡视为"原始材料"喂新管线后删除
- 全部改动只在 dev 仓（`<PROJECT_ROOT>/EM-SKILL/`），完成后用户手动同步 install（`sync-to-install.cmd`）
