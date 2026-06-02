# git-changelog

> EM-SKILL 专用工具：从 `git log` 自动生成 `CHANGELOG.md`

## 定位

EM-SKILL 在每次主步骤完成时需要一份可读的变更日志。
本工具通过解析 EM 自定义的 commit 格式（`[Sx] type: message`），
将 `git log` 输出转换为符合
[Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 规范的 Markdown。

- **零外部依赖**：仅依赖 Python 3 标准库
- **可独立运行**：纯 CLI 工具，无外部状态
- **可与 EM-SKILL 工作流联动**：arch 流程会自动调用

## 目录结构

```
tools/git-changelog/
├── README.md           # 本文件
├── changelog_gen.py    # 主脚本
└── examples/
    └── CHANGELOG.md    # 输出示例
```

## 安装

无需安装。确保系统有 Python 3.7+ 和 Git 即可。

## 使用

### 基本用法

```bash
# 在项目根目录执行，输出到 ./CHANGELOG.md
python EM-SKILL/tools/git-changelog/changelog_gen.py
```

### 常用参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `--repo <path>` | Git 仓库路径 | `.`（当前目录） |
| `--output <path>` | 输出文件 | `./CHANGELOG.md` |
| `--from <tag>` | 起始 tag | 自动检测最新 tag |
| `--to <ref>` | 结束 ref | `HEAD` |
| `--version <ver>` | 强制指定版本号 | 覆盖自动检测 |
| `--dry-run` | 打印到 stdout，不写文件 | - |

### 示例

```bash
# 从最新 tag 到 HEAD
python changelog_gen.py

# 指定输出文件
python changelog_gen.py --output docs/CHANGELOG.md

# 指定范围
python changelog_gen.py --from v0.9.0 --to v0.10.0

# 指定版本号
python changelog_gen.py --version v0.10.0

# 预览（不写文件）
python changelog_gen.py --dry-run

# 指定仓库路径
python changelog_gen.py --repo ../my-project
```

## Commit 格式约定

本工具**仅识别 EM 自定义格式**的 commit message，其他格式会被跳过。

### 主格式

```
[S<n>] type: message
```

例：

```
[S10] feat: integrate git workflow
[S10-D] docs: add git permissions to initem
[S10-D] fix: typo in changelog_gen
```

### 退化格式（仅前缀，无 type）

```
[S<n>] message
```

会被归类为 `Other`。

### Type 映射

| Commit type | CHANGELOG section |
|-------------|-------------------|
| `feat`      | Added             |
| `fix`       | Fixed             |
| `docs`      | Documentation     |
| `refactor`  | Changed           |
| `perf`      | Changed           |
| `test`      | Tests             |
| `style`     | Other             |
| `chore`     | Other             |
| `build`     | Other             |
| `ci`        | Other             |
| `revert`    | Fixed             |
| 其他 / 无    | Other             |

## 与 EM-SKILL 工作流集成

### 在 `/em arch` 流程中

主步骤归档（步骤 5/5）完成时自动触发：

1. 执行 `git tag` 标记当前版本（如 `v0.10.0`）
2. 调用本工具：
   ```bash
   python EM-SKILL/tools/git-changelog/changelog_gen.py \
       --repo . \
       --output ./CHANGELOG.md \
       --from <上一tag> \
       --to <当前tag>
   ```
3. AI 提议 commit：包含 CHANGELOG.md 更新 + tag 信息
4. 提醒用户手动 `git push` 与 `git push --tags`（**禁止自动 push**）

详见 `commands/arch.md`。

### 在 CI / 手动场景

```bash
# 一次性生成全量 CHANGELOG（首次或重置）
python changelog_gen.py --from <最早tag>

# 增量更新
python changelog_gen.py --from v0.9.0 --to HEAD
```

## 输出示例

完整示例见 [`examples/CHANGELOG.md`](./examples/CHANGELOG.md)。

典型片段：

```markdown
# Changelog

> 项目变更日志 | 由 `tools/git-changelog/changelog_gen.py` 自动生成

## [2026-06 (S10-D)]

### Added
- [S10-D] git workflow integration with propose-commit UX

### Changed
- [S10-D] update initem.md with git permissions section

### Documentation
- [S10-D] add changelog tool README
```

## 函数签名（供二次开发）

```python
def parse_commits(git_log_output: str) -> list[Commit]:
    """解析 git log 输出（每行：<sha>|<date>|<author>|<subject>）。"""

def group_by_version(commits: list[Commit]) -> dict[str, list[Commit]]:
    """按版本/年月分组 commits。"""

def render_markdown(groups: dict[str, list[Commit]],
                    existing: Optional[str] = None) -> str:
    """渲染 CHANGELOG.md 文本。"""

def main(argv: Optional[list[str]] = None) -> int:
    """CLI 入口。"""
```

## 设计原则

1. **零外部依赖** — 仅 Python 3 标准库，可在任何环境运行
2. **可被覆盖** — `--from / --to / --version` 均允许用户覆盖
3. **保留手写段落** — 已存在的 `[Unreleased]` 段会被保留
4. **安全只读（git 端）** — 只调用 `git log` / `git describe`，不会修改仓库
5. **不涉及 push** — 工具链中所有 push 操作由用户手动执行

## 相关文件

- `commands/initem.md` — Git 权限白名单
- `commands/verify.md` — 验证流程中的"提议 commit"
- `commands/arch.md` — 归档完成时的自动 tag + CHANGELOG 更新
- `CHANGELOG.md` — 当前 EM-SKILL 项目的变更日志
