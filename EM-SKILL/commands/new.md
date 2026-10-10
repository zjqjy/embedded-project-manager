# 命令: /em new (新功能开发) — superpower 风格三档分流

## 功能
进入新功能开发流程。**借鉴 superpower 的「brainstorm → plan → execute」精神**，三档分流避免轻量需求被重流程拖累。

## 触发
```
/em new <功能描述>           # AI 推荐档位，用户确认
/em new <功能描述> --light   # 强制轻档
/em new <功能描述> --std     # 强制中档（默认）
/em new <功能描述> --deep    # 强制重档（原 5 阶段 disc）
```

## 三档总览

| 档位 | 适用 | 产出文件 | 时长 | 工作流 |
|------|------|---------|------|--------|
| **轻 light** | < 2h 工作量、单文件改动、bugfix、调参 | 0（对话内计划，`留档`例外）| ~5 min | `workflows/new-light.md` |
| **中 standard**（默认）| 跨模块特性、需设计但非系统级 | `features/S<N>-<slug>/plan.md` (1，R3 统一落盘) | ~15 min | `workflows/new-standard.md` |
| **重 deep** | 系统级、新外设、协议栈、状态机重构 | `features/S<N>-<slug>/`（plan + requirements/hardware/split）| ~45 min | `workflows/discussion-flow.md`（沿用）|

> **三档共用前置**：`workflows/new-clarify.md` 的 R0 追问轮——档位选定后、任何方案输出之前，AI 先一次一问澄清需求（下限：轻 ≥1 / 中 ≥2 / 重每子系统 ≥1；**不设上限**，以 AI 判断意图清晰为退出条件），需求理解摘要经用户确认后才进入档位工作流。**写文档永远是最后一步。**

## 档位推荐启发式

AI 收到 `<功能描述>` 后，按以下规则推荐：

| 信号 | 加分到 |
|------|--------|
| 描述 ≤ 30 字 | 轻 |
| 关键词：修复 / fix / 调整 / 优化 / 改进 / 重命名 | 轻 |
| 关键词：实现 / 接入 / 集成 / 添加模块 | 中 |
| 关键词：架构 / 系统 / 协议栈 / 状态机 / 重构 / 新硬件 | 重 |
| 描述含多个并列名词（"A、B、C 都要做"）| 中或重 |
| **嵌入式项目** + 涉及新外设/芯片 | 重（强制走硬件对齐阶段）|

**默认**: 中档。

## 执行流程（总入口）

1. **【状态目录】** `get_state_dir()` → `<STATE_DIR>`；不存在提示 `/em init`
2. **【步骤号分配】** 读 `<STATE_DIR>/state.md` 或步骤索引（v4: `features/README.md` 步骤总表；v3: `project-spec.md` 步骤表），取最大 S + 1
3. **【档位选择】**
   - 命令带 `--light/--std/--deep` → 直接采用
   - 否则按启发式推荐，输出：
     ```
     🆕 新功能: <描述>
        分配步骤: S<N>
        推荐档位: <轻|中|重>   理由: <一句话>
        其他档位: /em new ... --light | --std | --deep
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        输入 `继续` 采用推荐档位，或输入 `轻/中/重` 改档。
     ```
4. **【加载对应工作流文件】**（披露式按需加载，不一次性灌入所有）
   - 轻 → 立即读 `workflows/new-light.md`
   - 中 → 立即读 `workflows/new-standard.md`
   - 重 → 立即读 `workflows/discussion-flow.md`（沿用 5 阶段）
5. **【R0 追问轮（三档必经）】** 读 `workflows/new-clarify.md` 执行：
   - 一次一问澄清需求（下限：轻 ≥1 / 中 ≥2 / 重每子系统 ≥1；不设上限，意图清晰 + 摘要确认为退出条件）
   - 无真歧义时用「确认题」满足下限，但**理解摘要仍须用户确认**
   - 确认前禁止输出方案草稿、禁止写任何文件
6. **【按工作流执行】** 详见对应 workflow 文件（中档 R1/R2 对话、R3 统一落盘；重档 5 阶段对话后统一保存）
7. **【收尾】** 更新 `state.md`（下一步动作 = `/em verify s<N>`），同步步骤索引（v4: `features/README.md`；v3: `project-spec.md`）

## 公共规则

- **步骤编号**：`S<数字>`，废弃不复用
- **feature 目录**：`<STATE_DIR>/features/S<N>-<slug>/`（各档**首个落盘点**时创建——中档 R3 / 重档阶段5，含 README 状态卡；轻档不创建）
- **进度文件**：`status.json` 标记当前阶段（轻档可省）
- **硬闸门（HARD-GATE）**：
  - R0 需求理解摘要未经用户确认 → 禁止输出任何完整方案/计划草稿，禁止创建/写入任何文件
  - **写文档永远是流程的最后一步**——所有方案、拆分先在对话中确认，落盘集中在各档末尾的统一批次
- **强制约束**：流程未完成（如重档 5 阶段没走完）禁止 `/em verify`/`/em result`

## 输出格式（确认阶段后）

```
🆕 S<N>: <功能描述>
档位:   <轻|中|重>
讨论ID: <YYYYMMDD>-<slug>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<工作流首阶段提示，由对应 workflow 文件给出>
```

## 设计原则
- **superpower 精神**：先 brainstorm → 再 plan → 再 execute
- **clarify-first（S18）**：spec-kit `/clarify` + superpowers brainstorming 共识——追问在方案之前，一次一问、选择题优先、高影响优先；问题数不设上限，以意图清晰为退出条件（S18.1）
- **write-last（S18）**：写文档永远是最后一步，人工确认理解之前 AI 不产出任何文档
- **三档分流**：避免轻量需求被重流程拖累（追问下限按档位递增，轻档不被拖累）
- **披露式加载**：每档独立 workflow 文件，按选档加载；R0 三档共用一份规范
- **现有重档保留**：原 5 阶段 disc 完整保留，仅提问形式升级为追问式，零破坏
- **嵌入式自动加档**：涉及硬件外设自动推荐 deep（保留嵌入式严谨性）

## 相关文件
- `workflows/new-clarify.md` — **R0 追问轮规范（三档共用，S18 新增）**
- `workflows/new-light.md` — 轻档流程（R0 + 不落盘）
- `workflows/new-standard.md` — 中档流程（R0/R1/R2 对话 + R3 统一落盘）
- `workflows/discussion-flow.md` — 重档 5 阶段流程（阶段2 追问式）
- `commands/disc.md` — 单独触发讨论模式（可继续重档）
- `docs/research/2026-10-10-clarify-before-write.md` — 本次改造的调研依据
- `docs/LIFECYCLE.md` — 文件生命周期总表
