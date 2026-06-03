# 工作流: new 中档（standard）

> 适用：跨模块特性、需设计但非系统级（默认档位）
> 产出：`brainstorm.md` + `milestones.md`（2 个文件）

## 核心理念（借鉴 superpower）
**brainstorm → plan → execute**：
1. **brainstorm（发散）**：列方案、对比、取舍 → 选定方向
2. **plan（收敛）**：拆 milestones（子步骤） → 锁定路径
3. **execute**：进 verify

跳过 deep 档的 split/requirements/hardware（这些放到重档讨论）。

## 流程

```
阶段 1: brainstorm — AI 提案 → 用户确认
   ↓
阶段 2: milestones — AI 拆子步骤 → 用户确认
   ↓
阶段 3: 同步状态 → 提示 verify
```

## 阶段 1: brainstorm

**目标**: 用 ~3 个候选方案对比，选定方向。

**AI 输出格式**:

```markdown
# brainstorm: S<N>-<slug>

## 需求理解
<1-2 段，AI 复述需求，对齐认知>

## 候选方案

### 方案 A: <名字>
- 思路：<一段话>
- 优点：<列表>
- 缺点 / 风险：<列表>
- 预估工作量：<S/M/L>

### 方案 B: <名字>
（同上）

### 方案 C: <名字>
（同上，若有）

## 推荐
**方案 <X>**，理由：<一句话>

## 关键技术点
- <技术点 1>
- <技术点 2>
```

提示：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 输入 `继续` 采用推荐方案
🅰️🅱️🅲️ 输入 `A` / `B` / `C` 选别的方案
✏️ 输入 `补充: <...>` 添加缺失方案/约束
❌ 输入 `取消` 退出
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**保存**: `<STATE_DIR>/discussion/<YYYYMMDD>-<slug>/brainstorm.md`

## 阶段 2: milestones

**目标**: 把选定方案拆成可独立 verify 的子步骤。

**AI 输出格式**:

```markdown
# milestones: S<N>-<slug>

## 选定方案
<复述 brainstorm 选定的方案 + 关键决策>

## 子步骤

### S<N>-A: <名字>
- 内容：<2-3 行>
- 依赖：无 | S<N>-? 完成
- 验证：<verify 时怎么验>
- 预估：<S/M/L>

### S<N>-B: <名字>
（同上）

### S<N>-C: <名字>
（同上）

## 关键决策（记入 decisions.md）
- [YYYY-MM-DD] <决策一句话>
```

**约束**:
- 子步骤数量 ≤ 5（否则建议升档 deep）
- 每个子步骤必须可独立 verify

提示：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 输入 `继续` 采用拆分
🔧 输入 `合并 A B` / `拆分 A` 调整
✏️ 直接编辑拆分内容
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**保存**: `<STATE_DIR>/discussion/<YYYYMMDD>-<slug>/milestones.md`

## 阶段 3: 同步状态

1. `state.md`:
   - 当前步骤 = `S<N>-A`（首子步骤）
   - 下一步动作 = `/em verify s<N>-a`
   - 追加最近决策
2. `project-spec.md` 步骤表追加：`| S<N> | <名字> | 🚧 开发中 | YYYY-MM-DD |`
3. `decisions.md` 追加 brainstorm 选定方案的关键决策

## 收尾输出

```
🎉 S<N> 计划完成（中档）

📄 brainstorm: <STATE_DIR>/discussion/<...>/brainstorm.md
📄 milestones: <STATE_DIR>/discussion/<...>/milestones.md
🎯 选定方案: <名字>
📦 子步骤数: <N>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
首子步骤: S<N>-A — <名字>
下一步:
  开始编码 S<N>-A → 完成后 /em verify s<N>-a
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 升降档触发

| 触发 | 建议 |
|------|------|
| brainstorm 时发现「这就是个 bugfix」| 降轻档（`--light`），保留 brainstorm.md 作参考 |
| brainstorm 时发现「涉及新外设/协议栈」| 升重档（`--deep`），追加 hardware/requirements 讨论 |
| milestones 子步骤 > 5 | 升重档，做子流程拆分 |
