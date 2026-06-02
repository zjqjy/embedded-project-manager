# 命令: /em arch (归档)

## 功能
归档旧记录，避免文件膨胀

## 触发
```
/em arch [文件名]
```

## 无参数时
检查并归档所有需要归档的文件

## 有参数时
归档指定文件

## 归档文件类型

| 文件 | 触发条件 | 说明 |
|------|----------|------|
| memory-log.md | > 600行 | 记忆日志，按会话归档 |
| project-spec.md | S完成后 | 项目规格单，按里程碑归档 |
| problem-log.md | > 300行 | 问题追踪记录 |
| decision-log.md | > 300行 | 关键决策记录 |

## 执行流程

1. **【状态目录检测】** 调用 `get_state_dir()` 确定 `<STATE_DIR>`（S10-B 通用化）
2. 检查需要归档的文件
3. 按日期归档: `<STATE_DIR>/history/<年份>/<月份>/<日期>/`
4. 在原文件开头添加引用注释
5. 更新 `<STATE_DIR>/history/index.md` 索引
6. 如文件过大（>阈值行），清空原文件内容并保留模板头部
7. 🏷️ **【Git tag + CHANGELOG】（S10-D 集成）** 仅在主步骤 5/5 完成时执行，见下方

> 📌 **目录通用化（S10-B）**：所有 `.emv2/` 引用替换为 `<STATE_DIR>/`，
> 实际路径由 `get_state_dir()` 解析。详见 `commands/init.md`。

## 归档目录结构

```
<STATE_DIR>/history/
├── index.md              # 归档索引（总入口）
├── 2026/
│   ├── 04/
│   │   ├── 15/
│   │   │   ├── memory-log.md
│   │   │   ├── project-spec.md
│   │   │   ├── problem-log.md
│   │   │   └── decision-log.md
```

## Git tag + CHANGELOG 自动更新（S10-D）

> **触发条件**：**仅** 主步骤归档完成时（即子步骤 5/5 完成 → 步骤状态从"开发中"变为"已完成"）
> 才执行本节流程。子步骤归档（4/5、3/5 等）**不**打 tag，仅做"提议 commit"。

### 自动 tag 策略

| 步骤类型 | Tag 格式 | 示例 |
|----------|----------|------|
| 主步骤归档（5/5） | `v0.<主步骤号>.0` 或 `em-s<n>-final` | `v0.10.0` / `em-s10-final` |

> 在 `/em initem` 阶段由用户选择版本策略（Q3.3 决策）；
> 未选择则默认采用 `v0.<n>.0`（语义化版本）。

### 执行流程

主步骤归档（5/5）完成后，AI 按以下顺序执行：

#### 步骤 A：确定 tag 名称

```bash
# 默认策略 v0.<n>.0
TAG_NAME="v0.<主步骤号>.0"

# 或按用户 init 选择的策略 em-s<n>-final
# TAG_NAME="em-s<n>-final"
```

#### 步骤 B：调用 changelog 工具

```bash
python EM-SKILL/tools/git-changelog/changelog_gen.py \
    --repo . \
    --output ./CHANGELOG.md \
    --from <上一tag> \
    --to HEAD \
    --version "${TAG_NAME}"
```

> 工具会：
> 1. 读取 `<上一tag>..HEAD` 之间的所有 EM 格式 commit
> 2. 按版本/时间分组
> 3. 渲染为 Keep a Changelog 格式的 Markdown
> 4. 写入 `./CHANGELOG.md`

#### 步骤 C：打 tag

```bash
git tag -a "${TAG_NAME}" -m "EM-SKILL 主步骤 <n> 归档完成"
```

> 必须是 `-a`（annotated tag），不是 lightweight tag，便于追溯归档时刻。

#### 步骤 D：提议 commit（CHANGELOG 更新）

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 提议 commit  (S10-D Git 集成 / 归档流程)
━━━━━━━━━━━━━━━━━━━━━━━━━━
建议 commit message:
  [S<n>] chore: update CHANGELOG for ${TAG_NAME}

待提交文件:
  M  CHANGELOG.md
  A  CHANGELOG.md  (首次生成时)

Tag 已创建:
  ${TAG_NAME}

确认提交？[y/n/edit]
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 步骤 E：等待用户确认后执行

用户确认后：

```bash
git add CHANGELOG.md
git commit -m "[S<n>] chore: update CHANGELOG for ${TAG_NAME}"
```

### ⚠️ push 提醒（强制）

**无论本流程执行多少次，都不会自动 push。** 归档完成后 AI 必须向用户输出：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 归档完成 — 请手动推送
━━━━━━━━━━━━━━━━━━━━━━━━━━
Tag:        ${TAG_NAME}
Branch:     feature/s<n>（如已合并到 main 则为 main）

请手动执行:
  git push origin <branch>
  git push origin ${TAG_NAME}
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**为什么禁止自动 push？**
- EM-SKILL 的 initem.md 中 `permissions.deny` 已禁止 `Bash(git push:*)`
- 推送涉及远端仓库权限，避免误推到生产分支
- 用户应自行决定推送时机（如 code review 通过后）

### 跳过条件

下列情况**不**打 tag、**不**更新 CHANGELOG：

- 子步骤归档（如 4/5、3/5 等）
- 手动归档（`/em arch <文件名>` 带参数）
- 工作区未完成主步骤的归档判定
- 仓库不是 git 仓库（`git rev-parse --is-inside-work-tree` 失败）

## 触发条件

- 提交结果成功时自动归档
- 会话结束自动归档
- 文件过大时自动归档
  - memory-log.md: > 600行
  - project-spec.md: S完成后
  - problem-log.md: > 300行
  - decision-log.md: > 300行
- 手动命令归档: `/em arch`

## 引用完整性

归档格式:
- `[<STATE_DIR>/history/<年>/<月>/<日>/memory-log.md#会话ID]`
- `[<STATE_DIR>/history/<年>/<月>/<日>/project-spec.md#版本]`
- `[<STATE_DIR>/history/<年>/<月>/<日>/problem-log.md#标题]`
- `[<STATE_DIR>/history/<年>/<月>/<日>/decision-log.md#日期]`

> 注：实际写入路径由 `get_state_dir()` 决定，新项目为 `.em/`，旧项目为 `.emv2/`。

## 相关文件
- templates/history-index.md - 归档索引模板
- templates/memory-log.md - 记忆日志模板
- templates/project-spec.md - 项目规格单模板
- templates/problem-log.md - 问题追踪模板