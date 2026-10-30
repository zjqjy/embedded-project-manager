#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""triage.py — 会话 transcript 入队器（S21-A，原 S1-F 落卡行为废除）

用法:
  python triage.py --transcript <path> [--session-id X] [--dry]

由 hook 调用（Claude Code SessionEnd / ZCode Stop），也可手动跑。
机制（S21 起）：确定性提取候选行（书签）→ 追加 ~/.em/pending_lines.jsonl，
零 token、零落卡；蒸馏由 distill.py 门控批量执行。
书签记录 = 行内容 + transcript 指针（路径/格式/条目号）+ 角色标记；
幂等靠 ~/.em/ingest_state.json 的已见哈希（FIFO 封顶），push/pull 两通道共用。
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from em_config import vault_or_die  # noqa: E402  (保持与旧版一致的 vault 自检)

QUEUE = Path.home() / ".em" / "pending_lines.jsonl"
INGEST_STATE = Path.home() / ".em" / "ingest_state.json"
STATE = Path.home() / ".em" / "triage_state.json"  # 单槽：同 transcript 未变则跳过

SEEN_CAP = 8000
MAX_PER_RUN = 24

MARKERS = re.compile(
    r"(踩坑|翻车|卡在|卡了|报错|错误|异常|死锁|根因|原因|原来|并非|其实是|"
    r"结论|学会了|搞定了|解决|换成|替代|发现|问题是|避免|经验|注意|"
    r"方案|决定|决策|折衷|权衡|避坑|教训|推荐|更好|本质|"
    r"入一下库|入库|记一下)"
)
NOISE = re.compile(r"^(```|---|\||#|!\[|<|claude|zcode|user:|assistant:)", re.I)


def content_texts(c) -> list[str]:
    """message.content → 文本块列表（只取 text 字段，工具结果噪声天然排除）"""
    if isinstance(c, str):
        return [c] if c else []
    if isinstance(c, list):
        out = []
        for p in c:
            if isinstance(p, dict) and isinstance(p.get("text"), str) and p["text"]:
                out.append(p["text"])
        return out
    return []


def _strings(obj, depth: int = 0) -> list[str]:
    """未知格式的通用兜底（旧 triage 行为）"""
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


def entry_turns(obj) -> list[tuple[str, str, str]]:
    """一条 JSONL 记录 → [(role, text, part)]。只取新增轮次：
    - ZCode rollout（type=model_io）：request.messages 累积全历史，只取最后一条非 system；
      assistant 新输出在 response.text
    - Claude Code 事件式：type=user/assistant + message.content
    - 未知格式：通用字符串兜底（role=unknown）
    """
    if not isinstance(obj, dict):
        return []
    if obj.get("type") == "model_io":
        out: list[tuple[str, str, str]] = []
        msgs = (obj.get("request") or {}).get("messages") or []
        if msgs:
            m = msgs[-1]
            role = m.get("role") or "unknown"
            if role != "system":
                for t in content_texts(m.get("content")):
                    out.append((role, t, "req_last"))
        resp = obj.get("response") or {}
        t = resp.get("text")
        if isinstance(t, str) and t:
            out.append(("assistant", t, "resp"))
        return out
    msg = obj.get("message")
    if isinstance(msg, dict):
        role = msg.get("role") or obj.get("type") or "unknown"
        if role != "system":
            return [(role, t, "event") for t in content_texts(msg.get("content"))]
    return [("unknown", s, "any") for s in _strings(obj)]


def detect_fmt(p: Path) -> str:
    try:
        with p.open(encoding="utf-8", errors="replace") as fh:
            for ln in fh:
                s = ln.strip()
                if s:
                    return "jsonl" if s.startswith("{") else "text"
    except Exception:
        pass
    return "text"


def extract_turns(p: Path) -> tuple[str, list[tuple[int, str, str, str]]]:
    """transcript → (fmt, [(entry_idx, role, line, part)])，行级展平"""
    fmt = detect_fmt(p)
    turns: list[tuple[int, str, str, str]] = []
    if fmt == "text":
        with p.open(encoding="utf-8", errors="replace") as fh:
            for i, ln in enumerate(fh):
                s = ln.strip()
                if s:
                    turns.append((i, "unknown", s, "line"))
        return fmt, turns
    with p.open(encoding="utf-8", errors="replace") as fh:
        for i, ln in enumerate(fh):
            s = ln.strip()
            if not s:
                continue
            try:
                obj = json.loads(s)
            except Exception:
                continue
            for role, txt, part in entry_turns(obj):
                for sub in txt.splitlines():
                    sub = sub.strip()
                    if sub:
                        turns.append((i, role, sub, part))
    return fmt, turns


def candidate_lines(turns) -> list[tuple[int, str, str, str]]:
    """书签筛选：长度窗 + 噪声过滤 + 标记词，role=system 已在提取层排除"""
    picked, seen = [], set()
    for entry, role, ln, part in turns:
        if len(ln) < 15 or len(ln) > 500 or NOISE.match(ln):
            continue
        if MARKERS.search(ln) and ln not in seen:
            seen.add(ln)
            picked.append((entry, role, ln, part))
    return picked[:MAX_PER_RUN]


def line_hash(line: str) -> str:
    return hashlib.sha1(line.encode("utf-8", "replace")).hexdigest()[:16]


def load_ingest() -> dict:
    try:
        return json.loads(INGEST_STATE.read_text(encoding="utf-8"))
    except Exception:
        return {"seen": [], "files": {}}


def save_ingest(st: dict) -> None:
    INGEST_STATE.parent.mkdir(parents=True, exist_ok=True)
    INGEST_STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def append_queue(records: list[dict]) -> int:
    """书签入队（幂等）：命中已见哈希的跳过；返回实际新增数"""
    st = load_ingest()
    seen = set(st.get("seen", []))
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    added = 0
    with QUEUE.open("a", encoding="utf-8") as fh:
        for r in records:
            h = r["h"]
            if h in seen:
                continue
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            seen.add(h)
            added += 1
    st["seen"] = list(seen)[-SEEN_CAP:]
    save_ingest(st)
    return added


def bookmark(fmt: str, entry: int, role: str, ln: str, part: str, src: Path) -> dict:
    return {
        "line": ln, "role": role, "src": str(src), "fmt": fmt,
        "entry": entry, "part": part, "ts": dt.datetime.now().isoformat(timespec="seconds"),
        "h": line_hash(ln), "ver": 1,
    }


def window_strings(src: str, entry: int, k: int = 3, max_lines: int = 24) -> list[tuple[str, str]]:
    """蒸馏回读：entry±k 条记录的文本行 [(role, line)]——书签的上下文窗口"""
    p = Path(src) if src else None
    if p is None or not p.is_file():
        return []
    out: list[tuple[str, str]] = []
    if detect_fmt(p) == "text":
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        for l in lines[max(0, entry - k): entry + k + 1]:
            s = l.strip()
            if s:
                out.append(("context", s))
        return out[:max_lines]
    with p.open(encoding="utf-8", errors="replace") as fh:
        for i, ln in enumerate(fh):
            if abs(i - entry) > k:
                continue
            try:
                obj = json.loads(ln)
            except Exception:
                continue
            for role, txt, _part in entry_turns(obj):
                for sub in txt.splitlines():
                    s = sub.strip()
                    if s:
                        out.append((role, s))
    return out[:max_lines]


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
    ap.add_argument("--dry", action="store_true", help="只报告候选，不入队")
    a = ap.parse_args()

    t = Path(a.transcript)
    if not t.exists():
        print(json.dumps({"queued": 0, "reason": "transcript 不存在"}), flush=True)
        return

    sig = content_sig(t)
    if already_done(sig) and not a.dry:
        print(json.dumps({"queued": 0, "reason": "内容未变化，跳过"}), flush=True)
        return

    fmt, turns = extract_turns(t)
    picked = candidate_lines(turns)
    if a.dry:
        print(json.dumps({"dry": True, "candidates": len(picked), "fmt": fmt}, ensure_ascii=False), flush=True)
        return
    vault = vault_or_die()  # 未配 vault 时报错退出（与旧版一致）
    queued = 0
    if picked:
        records = [bookmark(fmt, e, r, ln, part, t) for e, r, ln, part in picked]
        queued = append_queue(records)
    mark_done(sig)
    print(json.dumps(
        {"queued": queued, "candidates": len(picked), "fmt": fmt},
        ensure_ascii=False,
    ), flush=True)


if __name__ == "__main__":
    main()
