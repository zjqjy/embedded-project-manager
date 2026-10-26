#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""triage.py — 会话 transcript 分拣 → 待确认卡（S1-F，宪法 §9.1）

用法:
  python triage.py --transcript <path> [--session-id X]

由 hook 调用（Claude Code SessionEnd / ZCode Stop），也可手动跑。
机制：标记词启发式扫描（踩坑/结论/方案/决策），有候选→落 status: 待确认 卡；
无候选→零产出。同一 transcript 内容未变则跳过（状态存 ~/.em/triage_state.json）。
判断升级路径：--ai-cmd "headless 命令" 可选配置（V2），当前纯启发式。
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from em_config import vault_or_die  # noqa: E402
from capture import write_card, git_commit, check_dedup  # noqa: E402

STATE = Path.home() / ".em" / "triage_state.json"

MARKERS = re.compile(
    r"(踩坑|翻车|卡在|卡了|报错|死锁|根因|原因是|原来|并非|其实是|结论|学会了|搞定了|"
    r"经验|注意|方案|决定|决策|折衷|权衡|避坑|教训|入一下库|入库|记一下)"
)
NOISE = re.compile(r"^(```|---|\||#|!\[|<|claude|zcode|user:|assistant:)", re.I)


def extract_text(transcript: Path) -> list[str]:
    """JSONL（Claude/ZCode 会话）或纯文本 → 文本行"""
    raw = transcript.read_text(encoding="utf-8", errors="replace")
    lines: list[str] = []
    for ln in raw.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        if ln.startswith("{"):
            try:
                obj = json.loads(ln)
            except Exception:
                continue
            for s in _strings(obj):
                lines.extend(s.splitlines())
        else:
            lines.append(ln)
    return [l.strip() for l in lines if l.strip()]


def _strings(obj, depth: int = 0) -> list[str]:
    if depth > 6:
        return []
    if isinstance(obj, str):
        return [obj] if 30 < len(obj) < 4000 else []
    if isinstance(obj, dict):
        out = []
        for k, v in obj.items():
            if k in ("toolUseResult", "tool_results", "gitDiff"):
                continue
            out += _strings(v, depth + 1)
        return out
    if isinstance(obj, list):
        out = []
        for v in obj:
            out += _strings(v, depth + 1)
        return out
    return []


def candidate_lines(lines: list[str]) -> list[str]:
    picked, seen = [], set()
    for ln in lines:
        if len(ln) < 15 or len(ln) > 500 or NOISE.match(ln):
            continue
        if MARKERS.search(ln) and ln not in seen:
            seen.add(ln)
            picked.append(ln)
    return picked[:24]


def content_sig(transcript: Path) -> str:
    st = transcript.stat()
    with transcript.open("rb") as f:
        head = f.read(400)
        f.seek(max(0, st.st_size - 400))
        tail = f.read(400)
    return hashlib.sha1(head + tail + str(st.st_size).encode()).hexdigest()


def already_done(sig: str) -> bool:
    try:
        return STATE.read_text(encoding="utf-8").strip() == sig
    except Exception:
        return False


def mark_done(sig: str) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(sig, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--session-id", default="")
    a = ap.parse_args()

    t = Path(a.transcript)
    if not t.exists():
        print(json.dumps({"captured": 0, "reason": "transcript 不存在"}), flush=True)
        return

    sig = content_sig(t)
    if already_done(sig):
        print(json.dumps({"captured": 0, "reason": "内容未变化，跳过"}), flush=True)
        return

    picked = candidate_lines(extract_text(t))
    vault = vault_or_die()
    captured = 0
    if len(picked) >= 2:
        # 标题取第一条候选的前 24 字
        raw_title = re.sub(r"\s+", " ", picked[0])[:24]
        dedup = check_dedup(vault, raw_title)
        if not dedup:  # 与现有卡不相似才落卡，避免重复分拣
            title = f"hook分拣：{raw_title}"
            body = (
                "## 分拣摘录（自动，待人工确认）\n\n"
                + "\n".join(f"> {ln}" for ln in picked[:16])
                + "\n\n确认后把 status 改为 `快捕`；是误报就删卡。"
            )
            write_card(vault, title, body, [], "待确认", "hook分拣")
            git_commit(vault, "AI: hook分拣待确认卡（会话摘录）")
            captured = 1
    mark_done(sig)
    print(json.dumps({"captured": captured, "candidates": len(picked)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
