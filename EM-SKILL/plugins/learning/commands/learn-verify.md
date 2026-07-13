# 命令: /em learn verify [topic-slug] [l<N>]

## 功能
验证当前 LPR（Learn-Pack-Practice-Verify-Surface）阶段的产物是否达标。通过则推进到下一阶段（L1 → L2 → ... → L5），未通过则列出缺失项。

## 触发
```
/em learn verify                       # 默认：所有活跃主题 + 当前阶段产物自检
/em learn verify ota-firmware-upgrade  # 指定主题：自检该主题当前 L 阶段
/em learn verify ota-firmware-upgrade l2  # 推进：L1 → L2（验证 L1 产物后）
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| topic-slug | 否 | 主题标识（缺省则扫描所有活跃主题） |
| l<N> | 否 | 目标阶段 L1-L5（缺省则验证当前阶段） |

## LPR 阶段验证清单

### L1 Learn → L2 Pack

**必须产物**：

- [ ] `<STATE_DIR>/learning/topics/<slug>/research/bib.json` 存在且 ≥ 3 条引用
- [ ] `<STATE_DIR>/learning/topics/<slug>/knowledge.md` 存在（核心概念 + 关键引用）

**自检命令**：

```bash
ls <STATE_DIR>/learning/topics/<slug>/research/bib.json
wc -l <STATE_DIR>/learning/topics/<slug>/knowledge.md  # 应 ≥ 50 行
```

**通过条件**：两个产物齐全 → 推进到 L2。

### L2 Pack → L3 Practice

**必须产物**：

- [ ] `knowledge-pack.md` 存在（含知识图谱 Mermaid）
- [ ] 至少 1 个概念图（架构 / 流程 / 时序任一）

### L3 Practice → L4 Verify

**必须产物**：

- [ ] `code/` 目录存在
- [ ] 至少 1 个可运行 demo（README 含运行说明）
- [ ] 复用 `/em new` 三档产物（如适用）

### L4 Verify → L5 Surface

**必须产物**：

- [ ] `verify-report.md` 存在（实战记录 + 性能数据 + 踩坑）
- [ ] 至少 3 条「踩坑记录」段落

### L5 完成（归档）

**必须产物**：

- [ ] `README.md` 精简版 ≤ 200 行
- [ ] `deep-dive.md` 架构详解完整
- [ ] `cheatsheet.md` 命令速查
- [ ] `_index.json` 中 `lpr_stage: "L5-Surfaced"`
- [ ] `state.md`「活跃主题」移除该主题，「最近完成」追加

## 执行流程

### 步骤 1: 解析参数

- 无参数 → 列出所有活跃主题，提示用户选
- 单参数 → 验证该主题当前 L 阶段
- 双参数 → 验证并推进到指定 L

### 步骤 2: 阶段产物检查

按当前 L 阶段的「必须产物」清单逐项检查，输出缺失项。

### 步骤 3: 用户确认推进

- 全部通过 → 询问 "推进到 L<N+1>？(Y/n)"
- 有缺失 → 列出缺失项，建议"补齐后重试"

### 步骤 4: 状态同步

- 更新 `_index.json` 的 `lpr_stage` 字段
- 若 L5 完成：移动主题从 `state.md`「活跃主题」到「最近完成」

## 与通用核 /em verify 的区别

- 通用 `/em verify` 是步骤验证（工程交付物）
- `/em learn verify` 是学习阶段验证（知识沉淀度）
- 两者互不冲突，可独立使用

## 相关文件

- `workflows/learn-lpr.md` — LPR 5 阶段流转细则
- `learn-new.md` — 创建主题命令
- `learn-status.md` — 查看状态命令