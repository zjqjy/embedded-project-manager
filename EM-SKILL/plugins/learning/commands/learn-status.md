# 命令: /em learn status [topic-slug] [-v]

## 功能
查看学习模式状态：活跃主题 / 最近完成 / 单主题详情 / 知识图谱统计。

## 触发
```
/em learn status                  # 总览：活跃主题数 + 最近 3 个完成
/em learn status -v               # 全景：所有主题 + 知识图谱统计
/em learn status <topic-slug>     # 单主题详情：当前 L 阶段 + 产物清单
```

## 参数
| 参数 | 必填 | 说明 |
|------|------|------|
| topic-slug | 否 | 主题标识（缺省则显示总览） |
| -v | 否 | 全景模式：所有主题 + 图谱统计 |

## 执行流程

### 步骤 1: 检查学习模式启用

读 `<STATE_DIR>/learning/state.md`：

- 文件不存在 → 提示"无学习模式，请 `/em learn new <topic>` 启用"。
- 文件存在 → 进入步骤 2。

### 步骤 2: 按模式分支

#### 模式 A: 无参数（总览）

输出示例：

```
🎓 学习模式状态

活跃主题: 2
最近完成: 3 条
知识图谱: 12 节点 / 18 边

下一步: /em learn verify ota-firmware-upgrade 推进 L4 阶段
```

数据来源：
- 活跃主题数 → `state.md` 的「活跃主题」表行数
- 最近完成 → `state.md` 的「最近完成」列表
- 知识图谱 → `<STATE_DIR>/learning/_index.json.knowledge_graph`

#### 模式 B: -v（全景）

输出三段：

1. **活跃主题表**（所有 status=active 的主题）
2. **全部完成主题表**（status=done）
3. **知识图谱 Mermaid**（从 `_index.json.knowledge_graph` 渲染）

#### 模式 C: 指定 topic-slug（详情）

输出示例：

```
📖 OTA 固件升级  [active]

当前阶段: L4 - Synthesis
创建日期: 2026-07-10
复杂度:   M
标签:     embedded, mcu, networking

产物清单:
  ✅ research/bib.json      (24 条引用)
  ✅ knowledge.md          (180 行)
  ⏳ knowledge-pack.md
  ❌ code/demo
  ❌ verify-report.md
  ❌ README.md (L5)

下一步: /em learn verify ota-firmware-upgrade l5
```

产物清单的判定规则：

| 文件 | L 阶段 | 判定逻辑 |
|------|--------|----------|
| research/bib.json | L1 | 引用数 ≥ 阈值 ✅ |
| knowledge.md | L2 | 行数 ≥ 50 ✅ |
| knowledge-pack.md | L3 | 文件存在 ⏳ |
| code/demo | L4 | 目录存在 ❌ |
| verify-report.md | L4 | 文件存在 ❌ |
| README.md | L5 | 文件存在（仅终态）❌ |

## 复用 state.md / _index.json

| 数据 | 路径 |
|------|------|
| 活跃主题表 | `<STATE_DIR>/learning/state.md` |
| 主题元数据 | `<STATE_DIR>/learning/_index.json` |
| 知识图谱 | `_index.json.knowledge_graph` |
| 主题关联 | `_index.json[topic].related_topics` |

## 输出示例（state.md 格式参考）

```
# 🎯 当前学习状态

## 活跃主题
| 主题 | 当前阶段 | 下一步动作 | 截止日期 |
|------|----------|------------|----------|
| ota-firmware-upgrade | L4 Synthesis | /em learn verify l5 | 2026-07-20 |
| can-bus-protocol | L2 Comprehension | /em learn verify l3 | 2026-07-25 |

## 最近完成
- ✅ 2026-07-13: OTA 固件升级 → L5 Surface
- ✅ 2026-07-08: FreeRTOS 任务调度 → L5 Surface
- ✅ 2026-07-01: I2C 总线协议 → L5 Surface
```

## 相关文件

- `workflows/learn-lpr.md` — LPR 阶段定义
- `learn-new.md` — 创建主题命令
- `learn-verify.md` — 推进阶段命令
- `learn-link.md` — 主题关联（写入 related_topics）