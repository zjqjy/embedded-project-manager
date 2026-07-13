# 命令: /em learn new <topic-slug> [topic-title]

## 功能

基于主题创建一个新的 LPR（Learn-Pack-Verify-Surface）学习闭环，从 L1 调研阶段开始，按 5 阶段流转生成主题卡片、知识包、实验代码、验证报告与最终展示物。命令完成后主题进入「活跃主题」表，可通过 `/em learn verify l<n>` 推进阶段。

## 触发

```
/em learn new <topic-slug> [topic-title]
```

**示例**

```
/em learn new ota-firmware-upgrade STM32 OTA 固件升级实战
/em learn new freertos-task-scheduler
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| topic-slug | 是 | 主题短标识（kebab-case，例：`ota-firmware-upgrade`） |
| topic-title | 否 | 主题标题（缺省时由 slug 转 Title Case） |

## 执行流程

### 步骤 1: 检查学习模式启用

读 `<STATE_DIR>/project.json`，确认 `type == "learning"` 或检测到 `<STATE_DIR>/learning/state.md`：

- 已启用 → 进入步骤 2
- 未启用 → 提示「学习模式未启用，是否启用？(Y/n)」，确认后写入 `project.json`

### 步骤 2: 创建主题目录骨架

在 `<STATE_DIR>/learning/topics/<slug>/` 下创建三类产物文件：

| 文件 | 模板来源 | 说明 |
|------|----------|------|
| `README.md` | `templates/README-card.md` | 主题卡片（面向读者，含 1-2-3 学习路径） |
| `deep-dive.md` | `templates/topic-deep-dive.md` | 深度梳理文档 |
| `cheatsheet.md` | `templates/topic-cheatsheet.md` | 速查表 |

模板未到位时（S14-B 实施前）使用骨架文件占位，正文待后续阶段填充。

### 步骤 3: 更新 _index.json

追加主题元数据到 `<STATE_DIR>/learning/_index.json`：

```json
{
  "slug": "<slug>",
  "title": "<title>",
  "status": "active",
  "lpr_stage": "L1-Learn",
  "created_at": "<ISO8601>",
  "complexity": "<待 L2 时评估>",
  "tags": []
}
```

若 `_index.json` 不存在则创建，初始化为 `{ "topics": [] }`。

### 步骤 4: 更新 state.md

在 `<STATE_DIR>/learning/state.md` 的「活跃主题」表格追加一行：

```
| <slug> | <title> | L1-Learn | <created_at> | 待 L2 评估 |
```

### 步骤 5: 写入 project.json（如未启用）

若 `project.json.type != "learning"`，询问后写入：

```json
"type": "learning"
```

## LPR 阶段流转（提示）

创建后主题进入 **L1 Learn** 阶段。下一步用 `/em learn verify` 推进。

| L | 名称 | 产物 | 触发命令 |
|---|------|------|----------|
| L1 | Learn | `research/bib.json` + `knowledge.md` | `/em learn verify l1` |
| L2 | Pack | `knowledge-pack.md` + 概念图 | `/em learn verify l2` |
| L3 | Practice | `code/` 实验代码 + 复用 `/em new` | `/em learn verify l3` |
| L4 | Verify | `verify-report.md` + 实战记录 | `/em learn verify l4` |
| L5 | Surface | README 卡片定稿 + 视频脚本 | `/em learn verify l5` |

## 验证

- `topics/<slug>/README.md` 存在
- `topics/<slug>/deep-dive.md` 存在
- `topics/<slug>/cheatsheet.md` 存在
- `_index.json` 含新主题条目
- `state.md` 活跃主题表已更新
- `project.json.type == "learning"`（如未启用会询问）

## 相关文件

- `workflows/learn-lpr.md` — LPR 5 阶段流转细则
- `templates/README-card.md` — 主题 README 卡片模板（S14-B 实施）
- `templates/topic-deep-dive.md` — 深度梳理模板
- `templates/topic-cheatsheet.md` — 速查表模板
- `../PLUGIN.md` — 学习模式插件入口