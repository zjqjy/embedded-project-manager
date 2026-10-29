# 命令: /em vault (知识库初始化 / 连接 / 状态)

## 功能
把项目连接到知识库 vault（一次配置全局生效）；用户还没有知识库时，初始化一个再连接。

## 触发
```
/em vault init [路径] [--git]   # 新建/接管目录为知识库，并连接
/em vault connect <路径>        # 连接已有 vault
/em vault status                # 连接状态
/em vault briefing              # 近 7 天入库摘要（含待确认卡数）
```

## init 执行流程（无库用户的入口）

> 入口有两个：`/em initem` 首次工具初始化时顺带问一次（见 `plugins/embedded/commands/initem.md` 步骤 7），或用户直接敲 `/em vault init`。本文件是流程真值。

1. **【问路】** 用户没给路径时，一次一问，给两个选项：
   - **A 选一个目录**（现有笔记目录或新建目录都行）
   - **B 没有笔记体系** → 先走下面的「Obsidian 安装指引」，装完再回到 A
   > Obsidian 不是必需项：任何本地 Markdown 目录都能当 vault，装 OB 只是多双链/图谱/移动端。
2. **【初始化】**
   ```bash
   python "<SKILL_DIR>/tools/vault/em_config.py" --init <路径> [--git]
   ```
   脚本自动（幂等，可重复执行）：
   - 生成 `AGENTS.md`（知识库宪法 §九：快捕/转正/检索/归属）——已存在则不覆盖
   - 生成快捕区 `08_快捕/`
   - 探测检索目录（顶层目录，排除点目录 / `06_归档` / node_modules）→ 写 `vault_dirs`
   - 写 `~/.em/config.json`（`vault_path` + `vault_dirs`）
   - `--git`：目录还不是仓库时 `git init` + 首次提交；已在仓库内则跳过（不碰父仓库）
   > 是否要 git 问一句：新库建议要（`/em note` 落卡即 commit，可回溯）；已有笔记目录默认不要。
3. **【报告】** 原样转述脚本输出（路径 / 快捕区 / 检索目录 / git 状态），补一句下一步。

## Obsidian 安装指引（B 路线）

1. 下载安装：<https://obsidian.md/download>（个人使用免费）
2. 首次启动选「Open folder as vault」：
   - 已有笔记目录 → 直接选它
   - 没有 → 先建一个空目录（如 `~/notes`）再选
3. 回到对话：
   ```
   /em vault init <刚才那个目录>
   ```
4. OB 里会直接看到 `08_快捕/` 下的卡片，不需要装任何插件。
   > 已经装过 OB、只是没连过 EM-SKILL → 直接 `/em vault connect <vault路径>`，不必 init。

## connect 执行流程

1. 路径自检（脚本内做）：目录存在 + 含 `AGENTS.md` 或 `30_方法论/`
   - 不合格时脚本会提示改用 `init` 接管
2. 写 `~/.em/config.json`（`vault_path` + 刷新 `vault_dirs`）：
   ```bash
   python "<SKILL_DIR>/tools/vault/em_config.py" --set <路径>
   ```
3. 报告：
   ```
   🔗 vault 已连接: <路径>
      快捕区: 08_快捕/（现有 N 张卡）
      检索目录: <vault_dirs>
      下次起 /em note、/em ask 直接可用
   ```

## status

读 `~/.em/config.json` + 校验路径存活；未配置则提示 `init` / `connect`。附带统计：`08_快捕/` 各 status 卡数、当前 `vault_dirs`。

## briefing

```bash
python "<SKILL_DIR>/tools/vault/search.py" briefing
```
输出近 7 天入库列表 + 快捕/待确认/已归档计数 + vault 最近 commit。

## 设计原则
- 配置文件只有 `vault_path` + `vault_dirs`——多机各自 init/connect 本机路径（EM-SKILL 多设备约定不冲突）
- 不存密钥、不存其他状态；分拣状态在 `~/.em/triage_state.json`（hook 自动维护）
- 用户资产优先：init 只补缺失的骨架文件，绝不覆盖已有 `AGENTS.md`，不删改用户笔记

## 相关文件
- `tools/vault/em_config.py` — vault 路径解析 / 初始化 / 目录探测
- `tools/vault/search.py` — 检索（读 `vault_dirs`）/ surfaced 回写 / 摘要
- `tools/vault/capture.py` — 落卡（`08_快捕/` 不存在时自动创建）
