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
| **轻 light** | < 2h 工作量、单文件改动、bugfix、调参 | `quick-plan.md` (1) | ~5 min | `workflows/new-light.md` |
| **中 standard**（默认）| 跨模块特性、需设计但非系统级 | `brainstorm.md` + `milestones.md` (2) | ~15 min | `workflows/new-standard.md` |
| **重 deep** | 系统级、新外设、协议栈、状态机重构 | 5 个文件（split/req/hardware/brainstorm/milestones）| ~45 min | `workflows/discussion-flow.md`（沿用）|

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
2. **【步骤号分配】** 读 `<STATE_DIR>/state.md` 或 `project-spec.md` 步骤表，取最大 S + 1
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
5. **【按工作流执行】** 详见对应 workflow 文件
6. **【收尾】** 更新 `state.md`（下一步动作 = `/em verify s<N>`），写入 `project-spec.md` 步骤表

## 公共规则

- **步骤编号**：`S<数字>`，废弃不复用
- **讨论目录**：`<STATE_DIR>/discussion/<YYYYMMDD>-<slug>/`
- **进度文件**：`status.json` 标记当前阶段（轻档可省）
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
- **三档分流**：避免轻量需求被重流程拖累
- **披露式加载**：每档独立 workflow 文件，按选档加载
- **现有重档保留**：原 5 阶段 disc 完整保留，零破坏
- **嵌入式自动加档**：涉及硬件外设自动推荐 deep（保留嵌入式严谨性）

## 相关文件
- `workflows/new-light.md` — 轻档流程（新）
- `workflows/new-standard.md` — 中档流程（新，brainstorm + milestones）
- `workflows/discussion-flow.md` — 重档 5 阶段流程（沿用）
- `commands/disc.md` — 单独触发讨论模式（可继续重档）
- `commands/state.md` — 步骤号读自 state.md
