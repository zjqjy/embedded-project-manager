#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""capture.py — 快捕卡落盘 + 写前查重粗筛（S1-C，宪法 §9.1）

用法:
  python capture.py check --title "标题"                 # 查重粗筛，输出 top3 相似卡 JSON
  python capture.py write --title "标题" --body "几行正文"
        [--body-file f] [--tags a,b] [--status 快捕|待确认] [--source 对话快捕|hook分拣]

卡落 08_快捕/，机器生成 frontmatter（surfaced_count 等），落卡即 git commit。
查重 = 标题关键词与现有卡的重叠度粗筛，判断交给对话里的 AI（不引向量库）。
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from em_config import vault_or_die  # noqa: E402

CAPTURE_DIR = "08_快捕"


def out(s: str) -> None:
    print(s, flush=True)


def tokenize(text: str) -> set[str]:
    """ latin 词 + 中文二元组 """
    toks = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_+-]{1,}", text))
    cjk = re.sub(r"[^\u4e00-\u9fff]", "", text)
    toks |= {cjk[i:i + 2] for i in range(len(cjk) - 1)}
    return toks


def card_files(vault: Path):
    d = vault / CAPTURE_DIR
    return sorted(d.glob("*.md")) if d.is_dir() else []


def read_card(p: Path) -> tuple[str, str]:
    """返回 (标题, 正文)"""
    try:
        t = p.read_text(encoding="utf-8")
    except Exception:
        return "", ""
    m = re.search(r"^#\s+(.+)$", t, re.M)
    title = m.group(1).strip() if m else p.stem
    return title, t


def check_dedup(vault: Path, title: str, top: int = 3) -> list[dict]:
    q = tokenize(title)
    if not q:
        return []
    scored = []
    for p in card_files(vault):
        t, _ = read_card(p)
        score = len(q & tokenize(p.stem + " " + t))
        if score > 0:
            scored.append({"path": str(p.relative_to(vault)), "title": t, "score": score})
    scored.sort(key=lambda x: -x["score"])
    return scored[:top]


def safe_name(title: str) -> str:
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", title).strip().rstrip(".")
    return (s or "快捕")[:60]


def frontmatter(status: str, source: str, tags: list[str], created: str, extra: dict | None = None) -> str:
    tags_s = "[" + ", ".join(tags) + "]" if tags else "[]"
    lines = [
        "---",
        "type: 快捕",
        f"created: {created}",
        f"tags: {tags_s}",
        f"status: {status}          # 快捕 / 待确认 / 已归档",
        "surfaced_count: 0",
        "last_surfaced: null",
        f"source: {source}",
    ]
    for k, v in (extra or {}).items():
        if isinstance(v, list):
            lines.append(f"{k}: [" + ", ".join(str(x) for x in v) + "]")
        elif v is not None:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def write_card(vault: Path, title: str, body: str, tags: list[str], status: str, source: str,
               extra: dict | None = None) -> Path:
    d = vault / CAPTURE_DIR
    d.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now()
    created = now.strftime("%Y-%m-%d")
    stem = f"{created}_{safe_name(title)}"
    p = d / f"{stem}.md"
    n = 2
    while p.exists():
        p = d / f"{stem}-{n}.md"
        n += 1
    content = (
        frontmatter(status, source, tags, created, extra)
        + f"\n# {title}\n\n{body.strip()}\n\n## 相关\n\n<!-- 暂无相关笔记 -->\n"
    )
    p.write_text(content, encoding="utf-8")
    return p


def read_meta(p: Path) -> dict:
    """frontmatter → dict（值保留字符串；列表解析为 list）"""
    try:
        t = p.read_text(encoding="utf-8")
    except Exception:
        return {}
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not m:
        return {}
    meta: dict = {}
    for ln in m.group(1).splitlines():
        if ":" not in ln:
            continue
        k, _, v = ln.partition(":")
        v = v.split("#")[0].strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        meta[k.strip()] = v
    return meta


def set_status(p: Path, new_status: str) -> bool:
    try:
        t = p.read_text(encoding="utf-8")
    except Exception:
        return False
    t2, n = re.subn(r"^(status:).*$", rf"\1 {new_status}", t, count=1, flags=re.M)
    if not n:
        return False
    p.write_text(t2, encoding="utf-8")
    return True


def rewrite_body(p: Path, new_body: str) -> bool:
    """过程卡覆盖：保留 frontmatter 和标题行，正文整段替换（S21 过程卡 UPDATE）"""
    try:
        t = p.read_text(encoding="utf-8")
    except Exception:
        return False
    m = re.match(r"^(---\n.*?\n---\n)(\n#[^\n]*\n)\n", t, re.S)
    if not m:
        return False
    t2 = m.group(1) + m.group(2) + "\n" + new_body.strip() + "\n\n## 相关\n\n<!-- 暂无相关笔记 -->\n"
    p.write_text(t2, encoding="utf-8")
    return True


def git_commit(vault: Path, msg: str) -> str | None:
    try:
        nowin = getattr(subprocess, "CREATE_NO_WINDOW", 0) if sys.platform == "win32" else 0
        # vault 必须是仓库根：选在父仓库子目录时，避免 add -A 波及无关改动
        top = subprocess.run(
            ["git", "-C", str(vault), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            creationflags=nowin,
        )
        if top.returncode != 0 or Path(top.stdout.strip()).resolve() != vault.resolve():
            return None
        subprocess.run(
            ["git", "-C", str(vault), "add", "-A"], check=True, capture_output=True,
            creationflags=nowin,
        )
        r = subprocess.run(
            ["git", "-C", str(vault), "commit", "-m", msg],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            creationflags=nowin,
        )
        if r.returncode == 0:
            h = subprocess.run(
                ["git", "-C", str(vault), "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, encoding="utf-8",
            ).stdout.strip()
            return h
        return None  # nothing to commit / not a repo
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="查重粗筛")
    c.add_argument("--title", required=True)

    w = sub.add_parser("write", help="落卡")
    w.add_argument("--title", required=True)
    w.add_argument("--body", default="")
    w.add_argument("--body-file", default=None)
    w.add_argument("--tags", default="")
    w.add_argument("--status", default="快捕", choices=["快捕", "待确认"])
    w.add_argument("--source", default="对话快捕", choices=["对话快捕", "hook分拣", "自动蒸馏"])
    w.add_argument("--no-commit", action="store_true")

    a = ap.parse_args()
    vault = vault_or_die()

    if a.cmd == "check":
        res = check_dedup(vault, a.title)
        out(json.dumps({"candidates": res}, ensure_ascii=False))
        if res:
            out(f"⚠️ 发现 {len(res)} 张相似卡——AI 判断：新建 / 更新旧卡 / 追加进旧卡？")
        else:
            out("✅ 无相似卡，可直接新建")
        return

    body = a.body
    if a.body_file:
        body = Path(a.body_file).read_text(encoding="utf-8")
    if not body.strip():
        raise SystemExit("❌ 正文为空：--body 或 --body-file 必须给一个")
    tags = [t.strip() for t in a.tags.split(",") if t.strip()]
    p = write_card(vault, a.title, body, tags, a.status, a.source)
    h = None
    if not a.no_commit:
        h = git_commit(vault, f"AI: 快捕 {a.title}" + ("（待确认）" if a.status == "待确认" else ""))
    out(json.dumps({"card": str(p.relative_to(vault)), "commit": h}, ensure_ascii=False))
    out(f"✅ 已落卡 {CAPTURE_DIR}/{p.name}" + (f"（commit {h}）" if h else "（未 commit）"))


if __name__ == "__main__":
    main()
