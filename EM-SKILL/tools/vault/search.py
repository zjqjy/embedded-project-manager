#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""search.py — vault 检索 + surfaced 回写 + 近 7 天入库摘要（S1-D，宪法 §9.3）

用法:
  python search.py query "问题" [--limit 5] [--surface-top 3] [--dirs 10_嵌入式,20_自媒体,30_方法论,08_快捕]
  python search.py briefing        # 近 7 天入库摘要（/em rec 时可附带）

检索 = 关键词/二元组计分（标题×3、tags×2、正文×1），纯本地无索引服务。
--surface-top N：命中前 N 张快捕卡回写 surfaced_count/last_surfaced——转正信号在此产生。
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

DEFAULT_DIRS = ["10_嵌入式", "20_自媒体", "30_方法论", "08_快捕"]
SKIP_PARTS = {".git", ".obsidian", ".em", ".scripts", ".prompts", ".logs", "06_归档", "node_modules"}


def out(s: str) -> None:
    print(s, flush=True)


def tokenize(text: str) -> list[str]:
    words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_+-]{1,}", text)]
    cjk = re.sub(r"[^\u4e00-\u9fff]", " ", text)
    grams = []
    for chunk in cjk.split():
        grams += [chunk[i:i + 2] for i in range(len(chunk) - 1)]
    return words + grams


def md_files(vault: Path, dirs: list[str]):
    for d in dirs:
        base = vault / d
        if not base.is_dir():
            continue
        for p in base.rglob("*.md"):
            if SKIP_PARTS & set(p.parts):
                continue
            yield p


def parse_fm(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                fm[k.strip()] = v.split("#")[0].strip()  # 去行内注释
    return fm


def bump_surface(vault: Path, rel: str) -> bool:
    p = vault / rel
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return False
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm or "surfaced_count" not in fm.group(1):
        return False
    today = dt.date.today().isoformat()
    head = fm.group(1)
    head = re.sub(r"^surfaced_count:\s*(\d+)", lambda m: f"surfaced_count: {int(m.group(1)) + 1}", head, flags=re.M)
    head = re.sub(r"^last_surfaced:.*$", f"last_surfaced: {today}", head, flags=re.M)
    p.write_text(text.replace(fm.group(0), f"---\n{head}\n---\n", 1), encoding="utf-8")
    return True


def git_commit(vault: Path, msg: str) -> str | None:
    try:
        subprocess.run(["git", "-C", str(vault), "add", "-A"], check=True, capture_output=True)
        r = subprocess.run(["git", "-C", str(vault), "commit", "-m", msg],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0:
            return subprocess.run(["git", "-C", str(vault), "rev-parse", "--short", "HEAD"],
                                  capture_output=True, text=True).stdout.strip()
    except Exception:
        pass
    return None


def do_query(vault: Path, q: str, limit: int, surface_top: int, dirs: list[str]) -> None:
    toks = [t for t in tokenize(q) if t]
    if not toks:
        raise SystemExit("❌ 查询词为空")
    scored = []
    for p in md_files(vault, dirs):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        title_m = re.search(r"^#\s+(.+)$", text, re.M)
        title = title_m.group(1) if title_m else p.stem
        tags_line = ""
        fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if fm:
            tm = re.search(r"^tags:.*$", fm.group(1), re.M)
            tags_line = tm.group(0) if tm else ""
        score = 0
        for t in set(toks):
            if t in title.lower():
                score += 3
            if t in tags_line.lower():
                score += 2
            score += 1 if t in text.lower() else 0
        if score <= 0:
            continue
        snippet = ""
        for line in text.splitlines():
            ll = line.lower()
            if any(t in ll for t in toks) and line.strip() and not line.startswith(("---", "type:", "tags:", "status:", "created:")):
                snippet = line.strip()[:120]
                break
        scored.append({
            "path": str(p.relative_to(vault)), "title": title, "score": score,
            "status": parse_fm(text).get("status", ""),
            "snippet": snippet,
        })
    scored.sort(key=lambda x: -x["score"])
    results = scored[:limit]
    out(json.dumps({"results": results}, ensure_ascii=False, indent=1))
    if surface_top and results:
        n = 0
        for r in results[:surface_top]:
            if bump_surface(vault, r["path"]):
                n += 1
        h = git_commit(vault, f"AI: surfaced 回写 {n} 卡（/em ask）") if n else None
        out(f"✍️ surfaced 回写 {n} 张" + (f"（commit {h}）" if h else ""))


def do_briefing(vault: Path) -> None:
    cap = vault / "08_快捕"
    week = (dt.date.today() - dt.timedelta(days=7)).isoformat()
    recent, counts = [], {"快捕": 0, "待确认": 0, "已归档": 0}
    if cap.is_dir():
        for p in sorted(cap.glob("*.md")):
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                continue
            fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            g = lambda k: (re.search(rf"^{k}:\s*(.*)$", fm.group(1), re.M).group(1).split("#")[0].strip() if fm and re.search(rf"^{k}:", fm.group(1), re.M) else "")
            status = g("status") or "快捕"
            counts[status] = counts.get(status, 0) + 1
            if g("created") >= week:
                title_m = re.search(r"^#\s+(.+)$", text, re.M)
                recent.append({"path": str(p.relative_to(vault)), "title": title_m.group(1) if title_m else p.stem, "status": status})
    h = subprocess.run(["git", "-C", str(vault), "log", "--oneline", "-1"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()
    out(json.dumps({"recent_7d": recent, "counts": counts, "last_commit": h}, ensure_ascii=False, indent=1))
    out(f"📋 近 7 天入库 {len(recent)} 张（快捕 {counts.get('快捕',0)} / 待确认 {counts.get('待确认',0)} / 已归档 {counts.get('已归档',0)}）")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("query")
    q.add_argument("text")
    q.add_argument("--limit", type=int, default=5)
    q.add_argument("--surface-top", type=int, default=3)
    q.add_argument("--dirs", default=",".join(DEFAULT_DIRS))
    sub.add_parser("briefing")
    a = ap.parse_args()
    vault = vault_or_die()
    if a.cmd == "briefing":
        do_briefing(vault)
    else:
        do_query(vault, a.text, a.limit, a.surface_top, [d.strip() for d in a.dirs.split(",") if d.strip()])


if __name__ == "__main__":
    main()
