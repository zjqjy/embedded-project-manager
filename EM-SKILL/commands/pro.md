# 命令: /em pro (问题上报 - EM-SKILL 插件问题记录)

## 功能
在任意项目使用 EM-SKILL 遇到问题（命令报错、输出异常、缺失功能、文档不清等），用此命令把**问题详情 + 源项目现场快照**上报到「项目管家」项目的 `problem-log.md`，集中处理。

> ⚠️ **不是通用项目记录器** — 只用于报告 EM-SKILL 自身的问题。通用项目状态用 `/em stat` / `/em rec`。

适用场景：
- 在其他 Claude Code 项目跑 EM-SKILL 命令时遇到 bug
- 命令输出不符合预期
- 文档与实际行为不符
- 缺失某功能（建议）

## 触发
```
/em pro <问题描述>
/em pro                              # 不带描述则进入问答模式
```

- `<问题描述>`：可选，一句话说明问题（如 `rec 加载 learning 插件慢`、`new 中档确认后还落盘 brainstorm`）

## 执行流程

### 1. 【解析管家路径】

按以下顺序定位「管家项目」（即追加日志的目标项目）：

1. **环境变量**: `$EM_PROJECT_MANAGER_HOME`
2. **配置文件**: `~/.em-skill/manager-home`（单行路径）
3. **首次提示**: 都不存在 → **直接问路径**（不预设选项）

**首次提示方式**（v3.1 修复 #3 — 不强制新建目录）：

```python
# AI 行为 — 不用 AskUserQuestion 多选，直接问具体路径
manager_path = input("请输入管家项目根路径（绝对路径）：").strip()

# 校验：必须是已存在的目录
if not Path(manager_path).is_dir():
    error("该路径不存在，请确认后重试（不要新建目录；如需新建请先 /em init）")

# 校验：必须是已初始化的 EM 项目（含 .em/ 或 .emv2/project.json）
if not any((Path(manager_path) / d / "project.json").exists() 
           for d in [".em", ".emv2"]):
    error(f"{manager_path} 不是已初始化的 EM 项目，请先 cd 进去跑 /em init")
```

写入 `~/.em-skill/manager-home` 后继续。

> 修复要点：
> - ❌ 旧版：3 个预设选项（用 EM-SKILL 目录 / 指定新目录 / 先不记录） — 强制 `mkdir`
> - ✅ 新版：直接问路径；只接受已存在 + 已 init 的目录；不允许新建

### 2. 【收集问题信息】

| 字段 | 收集方式 |
|------|----------|
| `problem.summary` | 命令参数 / 问答收集（必需） |
| `problem.category` | 分类：`命令报错` / `输出异常` / `缺失功能` / `文档不清` / `性能问题` / `其他`（问答选择）|
| `problem.command` | 触发问题的 EM-SKILL 命令（如 `/em rec`）— 问答收集 |
| `problem.steps` | 复现步骤 — 问答收集（可空） |
| `problem.expected` | 期望行为 — 问答收集（可空） |
| `problem.actual` | 实际行为 — 问答收集（可空） |

> 问答用 `AskUserQuestion` 单题 2-4 选项 + 「Other」自定义；可多次追问直到收齐核心字段。
> 如用户已经写得很全（命令参数够长），可跳过部分问答。

### 3. 【自动捕获源项目现场】

用于问题定位的上下文，**只读不写**：

| 字段 | 来源 |
|------|------|
| `SRC_ROOT` | 当前 cwd |
| `SRC_STATE_DIR` | `get_state_dir()` → `.em/` 优先，回退 `.emv2/` |
| `project.name` | `<SRC_STATE_DIR>/project.json` → `name` 字段 |
| `project.type` | 同上 → `type` 字段 |
| `current_step` | `<SRC_STATE_DIR>/state.md` → `## Meta > 当前步骤` |
| `session_id` | `<SRC_STATE_DIR>/state.md` → `## Meta > 会话` |
| `em_skill_version` | 读 `<SKILL_DIR>/CHANGELOG.md` 第一行 + 当前 `git log -1 --format=%h` 的提交 hash |
| `state.md snapshot` | `<SRC_STATE_DIR>/state.md` 前 30 行 |
| `problem-log.md snapshot` | `<SRC_STATE_DIR>/problem-log.md` 前 30 行（如有） |
| `git status` | `git status --short`（在 `SRC_ROOT`，截断 50 行） |
| `git log -5` | `git log --oneline -5`（在 `SRC_ROOT`） |

> `<SKILL_DIR>` 即 EM-SKILL 安装位置：执行 `python -c "import os; print(os.path.dirname(os.path.abspath(__file__)))"` 取 `commands/` 上级；或读 `pyproject.toml` 定位。

### 4. 【构造条目】

目标文件：`<MANAGER_HOME>/.emv2/problem-log.md`

**段头初始化**（首次写入时）：在文件末尾追加：

```markdown

---

## 跨项目问题记录 (EM-SKILL)

> 由 `/em pro` 命令跨项目自动追加。每条记录是用户在某项目使用 EM-SKILL 时遇到的问题，含现场快照便于复现。
>
> 字段约定：
> - `problem.summary` — 一句话问题摘要
> - `problem.category` — 命令报错 / 输出异常 / 缺失功能 / 文档不清 / 性能问题 / 其他
> - `现场快照` — 自动捕获：state.md / problem-log.md 头部 + git 状态 + EM-SKILL 版本
>
> 处理建议：在管家项目 `Read <MANAGER_HOME>/.emv2/problem-log.md > 跨项目问题记录` 一次性浏览；或按 `problem.category` 过滤分组修复。

---
```

**单条记录格式**：

```markdown

### [<YYYY-MM-DD HH:MM>] EM-SKILL 问题 — <problem.summary>

- **问题类别**: <category>
- **触发命令**: <problem.command 或 「未指定」>
- **源项目**: `<SRC_ROOT>` (<project.name>, <project.type>)
- **EM-SKILL 版本**: <em_skill_version>
- **管家项目**: `<MANAGER_HOME>`

**问题描述**:
<problem.summary + 详细描述（用户口述）>

**复现步骤**:
<problem.steps 或 「未提供」>

**期望行为**:
<problem.expected 或 「未提供」>

**实际行为**:
<problem.actual 或 「未提供」>

**现场快照** (`<SRC_STATE_DIR>/state.md` 前 30 行):
```yaml
current_step: <current_step>
session_id:   <session_id>
...
```

**现场快照** (`<SRC_STATE_DIR>/problem-log.md` 前 30 行):
```yaml
（如有，无则跳过该段）
```

**git 状态** (cwd `<SRC_ROOT>`):
```
分支: <branch 或 N/A>
最近 5 条:
<hash> <msg>
工作树 (git status --short):
<输出>
```

---
```

### 5. 【写入】

- `Edit` 追加到文件末尾：先 `Read` 最后 10 行，用 `Edit` 的 `old_string` 匹配末尾 `---`，避免重复段头
- 失败回退：`Bash` 端用 `cat >>` 追加

### 6. 【反馈】

```
✅ 已上报问题
  时间:    <YYYY-MM-DD HH:MM>
  问题:    <problem.summary>
  管家:    <MANAGER_HOME>/.emv2/problem-log.md > 跨项目问题记录
  后续:    管家项目 /em pi 或直接 Read 该段统一处理
```

## 配置管理

### 首次设置管家路径

`/em pro` 首次运行会询问管家项目路径，结果缓存到：

| 位置 | 优先级 | 用途 |
|------|--------|------|
| `$EM_PROJECT_MANAGER_HOME` | 1 | 环境变量（CI / 脚本） |
| `~/.em-skill/manager-home` | 2 | 用户级配置文件 |

修改：

```bash
echo "D:/new/manager" > ~/.em-skill/manager-home
# 或临时
export EM_PROJECT_MANAGER_HOME="D:/new/manager"
```

## 边界与降级

| 场景 | 行为 |
|------|------|
| 用户只敲 `/em pro` 不带描述 | 进入问答模式（最多 5 问） |
| 源项目无 `.em/` 或 `.emv2/` | 仍记录，标注「无 state.md」 |
| 源项目无 git | git 段标 N/A |
| EM-SKILL 版本不可读 | 字段标 `unknown` |
| 管家项目 `.emv2/` 不存在 | 报错，提示先 `/em init` |
| 写入失败（权限 / 文件被锁） | 报错并提示手动检查 |

## 路径占位符

| 占位符 | 实际 |
|--------|------|
| `<SRC_ROOT>` | 当前 cwd |
| `<SRC_STATE_DIR>` | 源项目 `.em/` 优先，回退 `.emv2/` |
| `<MANAGER_HOME>` | 管家项目根目录 |
| `<SKILL_DIR>` | 当前 EM-SKILL 安装根（读 `pyproject.toml` 定位） |

## 关键提醒

⚠️ **只用于 EM-SKILL 问题** — 通用项目记录用 `/em stat` / `/em rec`
⚠️ **只读源项目** — 不修改任何文件
⚠️ **追加写入管家** — 不覆盖现有 problem-log.md
⚠️ **可重复** — 每次是新条目，不去重

## 相关文件

- `commands/rec.md` — 同源的 `get_state_dir()` 读取逻辑
- `commands/pi.md` — 管家侧浏览入口
- `templates/problem-log.md` — problem-log 模板（参考字段约定）
- `CHANGELOG.md` — EM-SKILL 版本号来源
