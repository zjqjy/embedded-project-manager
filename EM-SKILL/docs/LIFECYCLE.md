# EM-SKILL 文件生命周期总表（LIFECYCLE）

> S17-D 交付。**每个文件的生、老、死规则集中在此一张表**；各命令的收尾步骤引用本表，
> 不再各自定义。口诀：**生成要吝啬、死亡要自动、活文件越少越好**。

## 一、生命周期规则表（单一事实来源）

| # | 文件 / 目录 | 生成时机（吝啬） | 死亡规则（自动） | 触发点 |
|---|------------|-----------------|-----------------|--------|
| 1 | `state.md` | init 时创建（2 文件之一） | **不归档**；> 50 行 → rec **硬拒绝**，强制 `/em migrate-state` 瘦身 | `/em rec` 每次检查 |
| 2 | `project.json` | init 时创建 | 永不死亡（项目元数据） | — |
| 3 | `project-spec.md` | **首次写步骤表时**创建（new 中/重档） | 已归档主步骤的行 > 20 → 老段移 `history/spec-archive-<date>.md` | `/em arch` |
| 4 | `decisions.md` | 首次记决策时创建 | > 300 行 → 头部老条目移 history | `/em arch` |
| 5 | `problem-log.md` | 首次记问题时创建 | closed 条目关闭 > 30 天 → 整段移 `history/<年>/<月>/problem-log-closed.md` | `/em arch` |
| 6 | `memory-log.md`（旧版） | 仅旧项目存在 | > 600 行按会话归档；v4 迁移后由 journal.md 取代 | `/em arch` / `/em migrate` |
| 7 | `sessions/sess-*.md` | `/em result` 每次追加 | 单文件永不改；会话数无上限，`/em sessions` 只列最近 N | — （v4 起由 journal.md 取代） |
| 8 | `discussion/<date>-<slug>/` | **用户确认后**才创建（S17-A 落盘确认门） | 轻档**不创建**；主步骤归档 → 整目录移 history | `/em result s<N>-通过` |
| 9 | `checkpoints/HVR-*.md` | `/em verify` 生成 | 随所属步骤 discussion 目录一起归档（v4 起与 plan 同目录） | `/em result` / `/em arch` |
| 10 | `logs/*.log` | verify/串口/编译时写入 | 保留最新 10 份，其余删除（被 HVR/problem-log 引用的豁免） | `/em logs-clean` |
| 11 | `cache/` | loader 运行时 | `--all` 时整删（自动重建）；**不入 git**（.gitignore 已覆盖） | `/em logs-clean --all` |
| 12 | `history/**` | 归档动作写入 | 永不删除（最终归宿） | — |

## 二、各命令的收尾义务（引用上表，不自创规则）

| 命令 | 收尾时必须检查 |
|------|---------------|
| `/em rec` | #1 state.md 行数（硬闸门） |
| `/em result s<N>-通过` | #8 discussion 归档提示（主步骤完成时） |
| `/em arch` | #3 #4 #5 #6 归档扫描 |
| `/em logs-clean` | #10 #11 |
| `/em verify` | 无归档义务（只生成 #9） |

## 三、v4 目标结构（S17-D 定义，迁移见 commands/migrate.md §v4）

```
<STATE_DIR>/
├── state.md          # 唯一活状态（≤50 行）
├── journal.md        # append-only 时间线（合并 sessions/ + decisions.md + memory-log.md 职责）
├── problem-log.md    # 只留 open 问题
├── features/
│   └── S<N>-<slug>/  # 每步骤一目录：plan.md + hvr.md（合并 discussion/ + checkpoints/）
│       └── README.md # 一行状态卡（templates/feature-README.md）
├── history/          # 完成的 feature 整目录 + 各类归档
└── logs/             # 滚动保留 N 份
```

- 活文件从 v3 的 9 类收敛到 **2 个**（state.md + journal.md）
- 归档单位 = **整个 feature 目录 mv**（不再逐文件清理）
- journal.md > 500 行 → 头部截出到 `history/journal-<date>.md`（rec 顺带检查）

## 四、设计依据（外部参考）

- spec-kit：按 feature 组织、每 feature 3 文件上限、生命周期绑定 git 分支
- superpowers：单一 journal append-only
- 详见 `.emv2/discussion/20261001-s17-slim-tools-registry/brainstorm.md`
