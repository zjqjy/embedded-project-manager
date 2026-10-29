#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""em_config.py — ~/.em/config.json 读写：vault 路径解析 + 初始化（S1-C / S20）

被 capture.py / search.py / triage.py / hook_session_end.py 共用。
vault 判定：目录存在 + 含 AGENTS.md 或 30_方法论/（知识库标记）。
init：为没有知识库的用户 scaffold AGENTS.md + 08_快捕/，并写入 vault_path/vault_dirs。
Obsidian 不是必需——任何本地 Markdown 目录都能当 vault。
"""
import json
import subprocess
import sys
from pathlib import Path

CONFIG_PATH = Path.home() / ".em" / "config.json"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CAPTURE_DIR = "08_快捕"
# 探测检索目录时排除：工具目录、隐藏目录、归档区
SKIP_DIRS = {
    ".git", ".obsidian", ".trash", ".em", ".scripts", ".prompts", ".logs",
    "node_modules", "06_归档",
}

AGENTS_TEMPLATE = """# 知识库宪法（EM-SKILL 生成）

> 本文件是 `/em note` `/em ask` 的规则真值，也是 EM-SKILL 认定「这是知识库」的标记。
> Obsidian 可选：本目录就是普通 Markdown 文件夹，任何编辑器都能读写。
> 可以自由追加内容；§九 的字段名被脚本读取，改动前先看 `EM-SKILL/tools/vault/`。

## 九、知识流

### 9.1 快捕区（08_快捕/）
- 对话知识一句话入库：`/em note`，AI 负责 frontmatter / 查重 / git commit
- 卡片路径：`08_快捕/YYYY-MM-DD_<标题>.md`；标题即结论，不用《记录一下》
- frontmatter 固定字段：`type` `created` `tags` `status` `surfaced_count` `last_surfaced` `source`
- `status` 生命周期：`快捕` → `待确认` → `已归档`
  - `快捕`：用户主动 `/em note`
  - `待确认`：hook 会话分拣自动产出，等人工审阅
- 写前查重：有相似卡时 AI 给三个选择——新建 / 更新旧卡 / 追加进旧卡

### 9.2 转正
- `surfaced_count` 是转正信号：被 `/em ask` 命中的次数越多，越值得转正
- 转正 = 人工把卡片内容并入主题笔记，状态改 `已归档`；AI 不擅自转正或删卡

### 9.3 检索（/em ask）
- 纯本地关键词/二元组计分：标题×3、tags×2、正文×1；无索引服务
- 检索范围 = `~/.em/config.json` 的 `vault_dirs`（init 时自动探测顶层目录）
  - 新增顶层目录后重跑 `/em vault init <本目录>` 刷新
  - `06_归档/`、点目录、node_modules 不参与检索
- 命中快捕卡自动回写 `surfaced_count` / `last_surfaced` 并 commit

### 9.4 归属
- vault 是用户资产：AI 只新增 `08_快捕/` 卡片、只改 surfaced 字段
- 不删改其他笔记；需要整理时先征得用户同意
"""


def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_config(cfg: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def is_vault(p: Path) -> bool:
    return p.is_dir() and ((p / "AGENTS.md").exists() or (p / "30_方法论").is_dir())


def detect_dirs(p: Path) -> list[str]:
    """探测检索目录：顶层目录（排除工具/隐藏/归档），快捕区始终在列。"""
    dirs = sorted(
        d.name for d in p.iterdir()
        if d.is_dir() and not d.name.startswith(".") and d.name not in SKIP_DIRS
    )
    if CAPTURE_DIR not in dirs:
        dirs.insert(0, CAPTURE_DIR)
    return dirs


def get_vault() -> Path | None:
    cfg = load_config()
    vp = cfg.get("vault_path")
    if not vp:
        return None
    p = Path(vp)
    return p if is_vault(p) else None


def _run_git(args: list[str], cwd: Path):
    try:
        return subprocess.run(
            ["git", "-C", str(cwd), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
    except FileNotFoundError:
        return None


def init_vault(path: str, git: bool = False) -> dict:
    """scaffold 一个 vault（幂等）：AGENTS.md + 08_快捕/ + 配置，可选 git init。"""
    p = Path(path).expanduser().resolve()
    if p.exists() and not p.is_dir():
        raise SystemExit(f"❌ {p} 是文件，不是目录；请换一个目录路径")
    existed_vault = is_vault(p)
    try:
        p.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise SystemExit(f"❌ 无法创建目录 {p}: {e}")

    created: list[str] = []
    agents = p / "AGENTS.md"
    if not agents.exists():
        agents.write_text(AGENTS_TEMPLATE, encoding="utf-8")
        created.append("AGENTS.md")

    cap = p / CAPTURE_DIR
    if not cap.is_dir():
        cap.mkdir(parents=True, exist_ok=True)
        created.append(CAPTURE_DIR + "/")
    if not any(cap.iterdir()):
        (cap / ".gitkeep").write_text("", encoding="utf-8")

    dirs = detect_dirs(p)

    git_state, git_hash = "未启用", None
    if git:
        probe = _run_git(["rev-parse", "--show-toplevel"], p)
        if probe is None:
            git_state = "git 不可用（已跳过）"
        elif probe.returncode == 0:
            top = Path(probe.stdout.strip()).resolve()
            if top == p:
                git_state = "已是 git 仓库（骨架未提交；之后 /em note 自动 commit）"
            else:
                git_state = f"位于仓库 {top} 内（非库根，不自动提交）"
        else:
            r = _run_git(["init"], p)
            if r is None or r.returncode != 0:
                git_state = "git init 失败（已跳过）"
            else:
                _run_git(["add", "-A"], p)
                c = _run_git(["commit", "-m", "init: EM 知识库骨架"], p)
                h = _run_git(["rev-parse", "--short", "HEAD"], p)
                if c is not None and c.returncode == 0 and h is not None:
                    git_hash = h.stdout.strip()
                    git_state = f"已初始化并提交 {git_hash}"
                else:
                    git_state = "已 git init（首次提交失败，检查 git user 配置）"

    cfg = load_config()
    cfg["vault_path"] = str(p)
    cfg["vault_dirs"] = dirs
    save_config(cfg)

    return {
        "path": str(p), "existed_vault": existed_vault, "created": created,
        "dirs": dirs, "git": git_state, "commit": git_hash,
        "cards": len(list(cap.glob("*.md"))),
    }


def set_vault(path: str) -> Path:
    p = Path(path).expanduser().resolve()
    if not is_vault(p):
        raise SystemExit(
            f"❌ {p} 不是知识库 vault（缺 AGENTS.md 或 30_方法论/）。\n"
            f"   已有笔记目录 → /em vault init {p} 接管为知识库（只补 AGENTS.md + 08_快捕/，不动其他笔记）\n"
            f"   还没有目录   → /em vault init <新目录>"
        )
    cfg = load_config()
    cfg["vault_path"] = str(p)
    cfg["vault_dirs"] = detect_dirs(p)
    save_config(cfg)
    return p


def vault_or_die() -> Path:
    vp = get_vault()
    if vp is None:
        raise SystemExit(
            "❌ 未配置知识库 vault 路径。\n"
            "   还没有库 → /em vault init <目录>（任意本地 md 目录即可，无需 Obsidian）\n"
            "   已有库   → /em vault connect <vault路径>"
        )
    return vp


def report(info: dict) -> None:
    head = "✅ vault 已连接（已有知识库，只补缺失骨架）" if info["existed_vault"] else "✅ vault 已初始化"
    made = "、".join(info["created"]) if info["created"] else "无（骨架已存在）"
    print(f"{head}: {info['path']}")
    print(f"   新建: {made}")
    print(f"   快捕区: {CAPTURE_DIR}/（现有 {info['cards']} 张卡）")
    print(f"   检索目录: {', '.join(info['dirs'])}")
    print(f"   git: {info['git']}")
    print(f"   配置: {CONFIG_PATH}")
    print("   下一步: /em note 入库，/em ask 检索；Obsidian 可直接打开该目录")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--init"] and len(args) >= 2:
        report(init_vault(args[1], git="--git" in args[2:]))
    elif args[:1] == ["--set"] and len(args) >= 2:
        p = set_vault(args[1])
        print(f"🔗 vault 已连接: {p}")
        print(f"   检索目录: {', '.join(detect_dirs(p))}")
    elif args[:1] == ["--get"]:
        vp = get_vault()
        print(vp if vp else "未配置（/em vault init <目录> 或 /em vault connect <路径>）")
    else:
        print("用法: em_config.py --init <目录> [--git] | --set <vault路径> | --get")
