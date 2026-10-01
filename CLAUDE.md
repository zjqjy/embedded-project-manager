# CLAUDE.md — embedded-project-manager

> 项目级 Claude 指令。所有会话自动加载；与全局 `~/.claude/CLAUDE.md` 互补。

## 项目定位

- **类型**: meta-skill（EM-SKILL 元仓库本身）
- **状态目录**: `.emv2/`（旧版，建议 `/em migrate` 升级到 `.em/`）
- **当前分支**: 跟随 `feature/s16-*` 等活跃分支
- **会话连续性**: 见 `.emv2/state.md` 的 `sess-*` 字段

> ⚠️ **本项目多设备开发** — 每个开发者各自 clone 在不同位置。
> 文档中所有路径用**占位符**（`<PROJECT_ROOT>` / `<INSTALL_ROOT>`），不写死绝对路径。
> 任何脚本 / 命令必须基于**相对路径**或**环境变量**解析，避免绑定特定机器。

## EM-SKILL dev / install 路径约定

EM-SKILL 在本机存在**两份文件树**，角色不同：

| 路径 | 角色 | 备注 |
|------|------|------|
| `<PROJECT_ROOT>/EM-SKILL/` | **源码 / 开发版本**（source of truth） | git tracked；只改这里 |
| `<INSTALL_ROOT>/EM-SKILL/` | **安装版本**（运行副本） | 来自 dev 的同步产物 |

**占位符解析**：

| 占位符 | Windows | Linux / macOS |
|--------|---------|---------------|
| `<PROJECT_ROOT>` | clone 到的本地仓库根（如 `D:\WorkSpace\Code\embedded-project-manager\`） | `~/work/embedded-project-manager/` 等 |
| `<INSTALL_ROOT>` | `%USERPROFILE%\.claude\skills\` | `~/.claude/skills/` |
| `<INSTALL_ROOT>/EM-SKILL/` | `C:\Users\<你>\.claude\skills\EM-SKILL\` | `~/.claude/skills/EM-SKILL/` |

> 多设备开发时各设备的 `<PROJECT_ROOT>` 不同，但**两份副本的角色不变**。

**硬规则**：

- ✅ **只修改 `<PROJECT_ROOT>/EM-SKILL/`**（dev 副本）
- ❌ **绝不直接 Edit/Write `<INSTALL_ROOT>/EM-SKILL/`**（install 副本）
- 🔄 dev → install 同步 → 由用户手动 / 脚本执行

### 同步方式

**方式 1 — 跨平台脚本（推荐，只补不删）**：

脚本源在 `<PROJECT_ROOT>/EM-SKILL/tools/sync-to-install.<ext>`：

| 平台 | 脚本 |
|------|------|
| Windows | `EM-SKILL/tools/sync-to-install.cmd` |
| Linux/macOS | `EM-SKILL/tools/sync-to-install.sh`（待补，参见方式 2 用 rsync 替代） |

```cmd
:: Windows — 项目根目录下
EM-SKILL\tools\sync-to-install.cmd          :: 预览 + 确认 + 同步
EM-SKILL\tools\sync-to-install.cmd /y       :: 跳过确认

:: install 路径不对时
set EM_INSTALL_PATH=D:\other\path
EM-SKILL\tools\sync-to-install.cmd
```

```bash
# Linux / macOS
EM-SKILL/tools/sync-to-install.sh            # 预览 + 确认 + 同步
EM-SKILL/tools/sync-to-install.sh -y         # 跳过确认

# install 路径不对时
EM_INSTALL_PATH=~/.claude/skills/EM-SKILL EM-SKILL/tools/sync-to-install.sh
```

> 脚本用 **robocopy `/E`**（Windows）或 **rsync 不带 `--delete`**（Linux）— 只补不删，install 中 dev 没有的旧文件**不会**被自动清除，需手动清理。
> 这样做是为了避免误删（用户可能在 install 副本里加了本地笔记）。

**方式 2 — 手动命令**：

```cmd
:: Windows（robocopy /E = 只补不删）
robocopy "%PROJECT_ROOT%\EM-SKILL" ^
         "%USERPROFILE%\.claude\skills\EM-SKILL" ^
         /E /R:0 /W:0 ^
         /XD __pycache__ .git build dist *.egg-info ^
         /XF *.pyc *.pyo *.pyd
```

```bash
# Linux / macOS（rsync 不带 --delete = 只补不删）
rsync -av \
    --exclude='__pycache__' --exclude='.git' --exclude='*.egg-info' \
    --exclude='build' --exclude='dist' --exclude='*.pyc' \
    "<PROJECT_ROOT>/EM-SKILL/" "<INSTALL_ROOT>/EM-SKILL/"
```

**比对新旧**：

```bash
# 跨平台通用
diff -r "<PROJECT_ROOT>/EM-SKILL/commands/" \
        "<INSTALL_ROOT>/EM-SKILL/commands/" --brief
```

### AI 行为约束

1. 用户提出 EM-SKILL 文件改动 → 只动 `<PROJECT_ROOT>/EM-SKILL/`
2. 发现 install 与 dev 不一致 → **先提示用户「dev 有未同步变更，是否同步到 install？」**，不要自作主张
3. 用户明确说「也改 install」/「同步一下」→ 才动 install，但仍优先建议先改 dev 再同步
4. state.md / 决策日志中记录的是 **dev 版本变更**

### 为什么这么分

- install 是「运行副本」，被多个项目复用
- dev 是「源码」，git tracked，可回溯、可分支、可发版
- 直接改 install 会让 dev/install 同步关系混乱（谁是 source？谁在覆盖谁？），破坏可追溯性

## 通用原则（多设备兼容）

写文档 / 脚本 / 命令时遵守：

1. **路径用占位符**：`<PROJECT_ROOT>` / `<INSTALL_ROOT>` / `<SRC_ROOT>` 等，不用绝对路径
2. **跨平台语法**：示例同时给 Windows（`%VAR%` / `\`）和 Unix（`$VAR` / `/`）版本，或用跨平台 shell 语法
3. **脚本用相对路径或环境变量**：不假设脚本在哪个绝对目录
4. **环境变量覆盖默认**：每个脚本 / 命令支持 `EM_*` 环境变量覆盖内置默认值
5. **路径分隔符**：示例统一用 `/`（Git Bash / WSL 兼容）；脚本内部按平台处理

## 决策日志

- **[2026-09-07]** EM-SKILL dev/install 路径约定明确：dev = `<PROJECT_ROOT>/EM-SKILL/`，install = `<INSTALL_ROOT>/EM-SKILL/`，只改 dev
- **[2026-09-07]** 同步脚本使用「只补不删」语义（robocopy `/E` / rsync 不带 `--delete`），避免误删 install 中本地新增文件
- **[2026-09-07]** 新增 `/em pro` 命令 — 跨设备上报 EM-SKILL 插件问题到管家项目 `problem-log.md > 跨项目问题记录 (EM-SKILL)` 段
- **[2026-09-07]** 项目多设备开发：所有文档 / 脚本 / 命令改用占位符（`<PROJECT_ROOT>` / `<INSTALL_ROOT>`），不写死绝对路径
