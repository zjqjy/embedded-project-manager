# 需求澄清实践调研 — 「追问先行、落盘最后」改造依据

**日期**: 2026-10-10
**背景**: S18 bug 修复 — `/em new` 三档此前 AI 收到描述就直接产出方案/计划（人工还没确认理解就开始写计划文档）。本次调研 GitHub 上成熟的 spec-driven / brainstorming 实践，作为改造依据。
**方法**: WebSearch + WebFetch 原文（spec-kit clarify 模板全文）+ 本机已安装的 superpowers brainstorming SKILL.md 原文。可信度高于 07-01 那次纯训练数据调研。

---

## 1. github/spec-kit — `/speckit.clarify`（🟢 高置信，读的是仓库模板原文）

> GitHub 官方 spec-driven 工具包。工作流：`/constitution → /specify → /clarify → /plan → /tasks → /implement`，**clarify 固定卡在 specify 与 plan 之间**。

`templates/commands/clarify.md` 关键机制：

| 机制 | 规则 |
|------|------|
| **一次一问** | "Present EXACTLY ONE question at a time"，后续问题不许提前剧透 |
| **问题预算** | 整个 session **最多 5 问**（单题澄清不算新题）；超出按 `Impact × Uncertainty` 启发式取 top 5 |
| **题型** | 选择题（2-5 个互斥选项，Markdown 表，**推荐项放首位** + 理由）或短答题（≤5 词，先给建议答案） |
| **每问结构** | `**Question:**` 完整问句 + 一句「Why it matters」；日常语言 |
| **覆盖扫描** | 11 类分类学（功能范围/数据模型/UX/非功能/集成/边界/约束/术语/完成信号/占位符…）逐类标 Clear/Partial/Missing |
| **排除项** | 不影响架构/测试/UX/运维/合规的问题不问；**实现细节、技术选型不问** |
| **答案归宿** | 每答一题立即折叠回 spec 对应章节（替换失效表述而非重复），另记 `## Clarifications → - Q: … → A: …` |
| **提前终止** | 用户说 done/stop/proceed 立即停；没有值得问的 → 明说「未发现关键歧义」建议直接继续；高影响未澄清的标 Deferred |

## 2. obra/superpowers — `brainstorming` skill（🟢 高置信，本机安装原文）

> EM-SKILL 三档分流本来就在借鉴 superpower；这次发现只学了一半（方案对比），漏了它的前置追问与硬闸门。

关键机制：

| 机制 | 规则 |
|------|------|
| **HARD-GATE** | 设计呈现并经用户批准前，禁止写代码、禁止 scaffold、禁止任何实现动作——**对每个项目无一例外** |
| **「太简单」反模式** | todo list / 单函数 / 改配置也必须走流程；设计可以短到几句话，但必须呈现并获批准 |
| **一次一问** | 每条消息只一个问题；能选择题就选择题；目的是搞清 purpose / constraints / success criteria |
| **范围预检** | 需求含多个独立子系统时先拆解，不为需要分解的项目浪费问题 |
| **写文档的位置** | checklist 9 步中「写设计文档」是第 6 步，前面依次是：探索上下文 → 追问 → 2-3 方案带取舍 → 分节呈现设计逐节确认；**写完还要 spec 自审 + 用户审一道门才进实现** |
| **用户反问时** | 先回答用户的疑问，当前问题保持挂着，答完重新抛出（后续 issue 修复的边界） |

## 3. Fission-AI/OpenSpec — change proposal（🟡 中置信，README + 第三方解读）

> 轻量 spec-driven：变更先走 proposal 评审，批准后才动代码。

- 产物链：`proposal.md`（**why + what changes**）→ specs 增量（what）→ design.md（how）→ tasks.md（清单）→ archive（合并回主 spec）
- 对本改造的启示主要一点：**「为什么做 + 范围」是独立于技术方案的第一份人工评审物**——对应 EM 的 R0 理解摘要（目标/边界/验证方式），而不是 AI 直接跳到 how。

## 4. 共性提炼（三家的交集 = 本改造的设计基线）

1. **追问在写任何东西之前**，且一次一问、选择题优先、每问给「为什么问」
2. **问题有预算**（5 问量级），只问高影响问题，实现细节不问
3. **没有问题 ≠ 跳过确认**：显式输出「未发现关键歧义 + 理解摘要」仍要用户点头
4. **用户可随时叫停追问**，叫停后汇总已有答案继续
5. **写文档是流程后段甚至最后一步**，且写完还有一道人工审门
6. 答案要**有归宿**：折叠进正式产物（spec/plan），不留散落对话

## 5. 映射到 EM-SKILL 的改造决定

| 调研结论 | EM 落地 |
|---------|---------|
| clarify 卡在 specify 与 plan 之间 | 新增 **R0 追问轮**，位于档位选定之后、任何方案输出之前；三档共用 `workflows/new-clarify.md` |
| ≤5 问、一次一问、选择题优先、Why it matters | R0 提问格式直接采用；预算：轻 ≤2 / 中 ≤5 / 重每子系统 ≤3 |
| 「太简单」反模式 | 轻档也不豁免理解摘要确认（免问路径：不问但必须给理解摘要） |
| HARD-GATE | 写入 `commands/new.md` 公共规则：理解摘要未确认禁止出方案草稿；**落盘永远是各档流程的最后一步** |
| 中档 R1/R2 原先各自带落盘点 | R1 方案 / R2 拆分改纯对话；**唯一落盘批次移到 R3**（plan.md 一次成文 + 状态同步），产物形状不变 |
| 重档已有 5 阶段问答、落盘本来就在最后 | 阶段2 改追问式（原「一大块请确认」），补 HARD-GATE 显式声明；status.json 路径修为 v4 `features/` 路径 |
| 答案有归宿 | R0 的 Q→A 并入 plan.md 方案章「需求理解」；轻档留对话（本来不落盘） |

## 6. 兼容性核对清单

- plan.md 两章结构（方案+拆分）、重档文件集、轻档零文件、status.json 字段——**产物形状零变化**，verify/result/arch/stat/pi/sessions 零改动
- 路径全部 `<STATE_DIR>` 抽象（`.em/` 与迁移前的 `.emv2/` 都适用）；重档产物对齐 v4（plan.md 合并 brainstorm/milestones 两章 + split/requirements/hardware）
- `--light/--std/--deep` 旗标、档位推荐交互不变；in-flight 的 `/em disc` 讨论结构不变（只是提问形式升级）
- 状态同步目标按项目形态自适应：v4 → `features/README.md` 索引 + `journal.md`；v3 → `project-spec.md` + `decisions.md`
