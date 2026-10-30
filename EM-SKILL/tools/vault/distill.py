#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""distill.py — 队列 → AI 蒸馏 → 结构化卡（S21-B/C）

用法:
  python distill.py --maybe      # 门控模式：距上次蒸馏 ≥ distill_min_hours 且有积压才跑（SessionStart hook 调）
  python distill.py --run        # 强制模式：sweep + 蒸馏 + 自维护（/em digest 调）
  python distill.py --maintain   # 只跑自维护（归档冷卡/待确认积压 + 转正建议）
  python distill.py --dry        # 只组 prompt 打印前 2500 字，不调 AI 不落卡

管线：sweep 多源增量入队 → 取队列（封顶）→ 书签±k 行回读 → headless AI 蒸馏
→ 严格 JSON 动作（NEW/UPDATE/NONE/need_context）→ capture 落卡 → commit → 清队列。
任何异常：记 ~/.em/distill.log、退出 0，永不阻塞 hook。
"""
import argparse
import datetime as dt
import glob as _glob
import json
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from em_config import load_config, vault_or_die  # noqa: E402
import capture  # noqa: E402
import triage  # noqa: E402

HOME_EM = Path.home() / ".em"
STATE_P = HOME_EM / "distill_state.json"
LOG_P = HOME_EM / "distill.log"
SUGGEST_P = HOME_EM / "promotion_suggestions.md"

DEFAULTS = {
    "ai_cmd": "claude -p --model haiku",
    "ai_timeout_s": 300,
    "distill_min_hours": 6,
    "maintain_interval_h": 20,
    "archive_min_days": 30,
    "backlog_days": 30,
    "queue_cap": 80,
    "window_k": 2,
    "window_max": 12,
    "window_k_big": 8,
    "material_char_cap": 28000,
    "dedup_skip_score": 8,
    "fail_limit": 3,
    "transcript_sources": [],
}
RULE_VER = 1

CTYPES = "踩坑排查|决策结论|速查|how-to|过程跟踪"

SKELETONS = """- 踩坑排查：现象/根因/解法/注意（备用方案放"注意"前）
- 决策结论：决定/为什么/影响范围/被否掉的备选
- 速查：直接表格/清单/命令块，不强迫成段
- how-to：编号步骤
- 过程跟踪：目标/已定决策（含为什么）/当前进展/待办/已踩的坑"""


def cfg_all() -> dict:
    cfg = dict(DEFAULTS)
    cfg.update({k: v for k, v in load_config().items() if k in DEFAULTS})
    return cfg


def log(msg: str) -> None:
    try:
        HOME_EM.mkdir(parents=True, exist_ok=True)
        with LOG_P.open("a", encoding="utf-8") as fh:
            fh.write(f"[{dt.datetime.now().isoformat(timespec='seconds')}] {msg}\n")
    except Exception:
        pass


def load_state() -> dict:
    try:
        return json.loads(STATE_P.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(st: dict) -> None:
    HOME_EM.mkdir(parents=True, exist_ok=True)
    STATE_P.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------------------------------------------------------------- sweep（pull 通道）

def _iter_source_files(src: dict):
    base = Path(str(src.get("path", "~"))).expanduser()
    pat = src.get("glob", "*")
    full = base / pat if not Path(pat).is_absolute() else Path(pat)
    try:
        for p in _glob.iglob(str(full), recursive=True):
            pp = Path(p)
            if pp.is_file():
                yield pp
    except Exception as e:
        log(f"sweep glob 失败 {src.get('name')}: {e}")


def sweep(cfg: dict) -> dict:
    sources = cfg.get("transcript_sources") or []
    if not sources:
        return {"sources": 0, "scanned": 0, "queued": 0}
    st = triage.load_ingest()
    files: dict = st.setdefault("files", {})
    scanned = queued = 0
    pending_file_state: dict = {}
    for s in sources:
        for p in _iter_source_files(s):
            try:
                sig = f"{p.stat().st_mtime_ns}:{p.stat().st_size}"
            except OSError:
                continue
            prev = files.get(str(p)) or {}
            if prev.get("sig") == sig and prev.get("ver") == RULE_VER:
                continue
            scanned += 1
            fmt, turns = triage.extract_turns(p)
            picked = triage.candidate_lines(turns)
            if picked:
                recs = [triage.bookmark(fmt, e, r, ln, part, p) for e, r, ln, part in picked]
                queued += triage.append_queue(recs)
            pending_file_state[str(p)] = {"sig": sig, "ver": RULE_VER}
    if pending_file_state:
        st = triage.load_ingest()  # append_queue 内部会保存 seen，这里重取再合并
        st.setdefault("files", {}).update(pending_file_state)
        triage.save_ingest(st)
    return {"sources": len(sources), "scanned": scanned, "queued": queued}


# ---------------------------------------------------------------- 队列与材料

def load_records(cap: int) -> list[dict]:
    if not triage.QUEUE.exists():
        return []
    out = []
    for ln in triage.QUEUE.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except Exception:
            continue
    return out[:cap]


def consume(records: list[dict]) -> None:
    """从队列移除已消化书签（按 h 匹配）"""
    done = {r.get("h") for r in records}
    rest = []
    for ln in triage.QUEUE.read_text(encoding="utf-8", errors="replace").splitlines():
        s = ln.strip()
        if not s:
            continue
        try:
            if json.loads(s).get("h") in done:
                continue
        except Exception:
            pass
        rest.append(s)
    tmp = triage.QUEUE.with_suffix(".tmp")
    tmp.write_text("\n".join(rest) + ("\n" if rest else ""), encoding="utf-8")
    tmp.replace(triage.QUEUE)


def build_material(records: list[dict], cfg: dict, big: bool = False, big_ids: set | None = None) -> str:
    k_big = int(cfg["window_k_big"])
    k, wmax = (k_big, 40) if big else (int(cfg["window_k"]), int(cfg["window_max"]))
    cap = int(cfg["material_char_cap"])
    parts, budget = [], cap
    for i, r in enumerate(records):
        ctx: list[tuple[str, str]] = []
        get_ctx = (not big) or (big_ids is None) or (i in big_ids)
        ctx = triage.window_strings(r.get("src", ""), int(r.get("entry", 0)), k=k, max_lines=wmax) if get_ctx else []
        seen = set()
        chunk = [f"[#{i}] ({r.get('role')}) {r.get('line', '')[:300]}"]
        for role, ln in ctx:
            if ln in seen or ln == r.get("line"):
                continue
            seen.add(ln)
            chunk.append(f"    - ({role}) {ln[:240]}")
        s = "\n".join(chunk)
        if len(s) > budget and parts:  # 预算尽：后续书签只给行本身
            parts.append(f"[#{i}] ({r.get('role')}) {r.get('line', '')[:200]}")
            budget -= 250
            continue
        parts.append(s)
        budget -= len(s)
    return "\n".join(parts)


# ---------------------------------------------------------------- prompt

EXIST_NOTE = """## 输出动作协议（只输出一个 JSON 对象，禁止 markdown 代码块、禁止解释）
{"actions": [
  {"action": "NEW", "card_type": "CTYPES", "title": "结论式标题", "summary": "≤40字核心结论", "body": "按骨架的正文", "tags": ["英文或短中文"], "sensitive": false, "files": ["可选：涉及的文件名"]},
  {"action": "UPDATE", "match_title": "现有过程卡标题（见下方列表）", "body": "过程跟踪五段新快照全文", "tags": ["..."]},
  {"action": "NONE", "reason": "一句话"},
  {"action": "need_context", "ids": [0, 2], "why": "一句话"}
]}
- UPDATE 只用于"过程跟踪"卡：同主题必须 UPDATE（新快照覆盖五段），绝不新建重复卡
- need_context 只在书签明显缺头尾无法判断时用，整批最多一次""".replace("CTYPES", CTYPES)

PROMPT_TMPL = """你在为个人知识库蒸馏会话材料。你要判断哪些内容值得永久留存，并写成结构化卡片。

## 有用性硬闸门（先判再写）
- 只收"将来会用得上"的可复用知识：解法/结论/决策/速查/避坑/纠正认知
- 过程性讨论、寒暄、情绪、重复确认、一次性琐事 → 全部跳过
- 整批材料都无用时只输出 {{"actions": [{{"action": "NONE", "reason": "..."}}]}}——零产出是正常且正确的结果，宁少勿多
- 不要为了产出而产出；出一堆平庸的卡比出零张卡更失败
- **例外——进行中的事**：材料描述某个进行中主题的状态（新进展/新决定/待办/踩坑），必须落入该主题的"过程跟踪"卡：有同主题过程卡就 UPDATE（新快照覆盖），没有就 NEW card_type=过程跟踪。过程卡记状态不记流水账，这正是它的价值，不许因为"还不是最终结论"而丢弃

## 输入隔离（防反馈循环）
材料来自对话 transcript，可能含有对旧笔记的引用、命令输出回显、别人的文章片段。
被引用的旧内容不是新知识，除非本轮对话产生了新结论。系统/工具的自我描述一律跳过。

## 不值得入库的反例（mem0 审计教训）
- "好的，我来看看这个文件"——过程性对话
- 离开对话上下文就无法读懂的碎片（除非伴随可复用解法）
- 同一事实的再次确认；包安装成功、空目录列表之类无发现的操作记录

## 写法微规则
- 每句话自包含、禁代词（"它/这个"）、必须带具体细节（文件名/命令/数值/链接）
- 标题即结论：一句话、含可检索关键词，不用《记录一下》
- summary：≤40 字核心结论，将作为卡片首段
- 禁套话："值得注意的是""综上所述""总的来说"零容忍
- 材料含密钥/凭证/token：明文脱敏（保留前4后4），sensitive=true
- files：知识直接关于某代码文件时填文件名，否则省略

## 卡片骨架（card_type 决定；内容不 fit 就换或简化，宁可裸结论也不许凑槽）
SKELETONS

## 现有卡标题（NEW 前自查，明显重复就不要新建）
{existing_titles}

## 现有"过程跟踪"卡（同主题必须 UPDATE）
{process_titles}

## 待蒸馏材料（[#{{i}}] 是书签行，缩进行是其上下文窗口）
{material}

{EXIST_NOTE}"""


def build_prompt(records: list[dict], cfg: dict, vault: Path, material: str) -> str:
    titles, process_titles = [], []
    for p in capture.card_files(vault):
        t, _ = capture.read_card(p)
        if not t:
            continue
        titles.append(t)
        meta = capture.read_meta(p)
        if meta.get("card_type") == "过程跟踪" or "过程" in t or "跟踪" in t:
            process_titles.append(t)
    ex = titles[-80:]
    return PROMPT_TMPL.replace("SKELETONS", SKELETONS).format(
        existing_titles="\n".join("- " + t for t in ex) or "（暂无）",
        process_titles="\n".join("- " + t for t in process_titles) or "（暂无）",
        material=material,
        EXIST_NOTE=EXIST_NOTE,
    )


# ---------------------------------------------------------------- AI 调用与解析

def _nowin() -> int:
    """Windows 下禁止子进程弹控制台窗口（cmd shim / git 都会 allocations）"""
    if sys.platform == "win32":
        return getattr(subprocess, "CREATE_NO_WINDOW", 0)
    return 0


def call_ai(prompt: str, cfg: dict) -> str:
    cmd = shlex.split(str(cfg["ai_cmd"]))
    if sys.platform == "win32":
        import shutil
        exe = shutil.which(cmd[0])
        if exe:
            cmd[0] = exe
        if cmd[0].lower().endswith((".cmd", ".bat")):  # npm shim 必须经 cmd.exe
            cmd = ["cmd", "/c"] + cmd
    r = subprocess.run(
        cmd, input=prompt, capture_output=True, encoding="utf-8", errors="replace",
        timeout=int(cfg["ai_timeout_s"]), creationflags=_nowin(),
    )
    if r.returncode != 0 and not r.stdout.strip():
        raise RuntimeError(f"ai_cmd 退出码 {r.returncode}: {r.stderr[:200]}")
    return r.stdout


def parse_actions(text: str):
    """从 AI 输出提取 JSON actions；失败返回 None"""
    cands = []
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if m:
        cands.append(m.group(1))
    i, j = text.find("{"), text.rfind("}")
    if i != -1 and j > i:
        cands.append(text[i:j + 1])
    for c in cands:
        try:
            obj = json.loads(c)
        except Exception:
            continue
        if isinstance(obj, dict) and isinstance(obj.get("actions"), list):
            return obj["actions"]
    return None


# ---------------------------------------------------------------- 动作落地

def _find_card_by_title(vault: Path, title: str) -> Path | None:
    best, best_score = None, 0
    qt = set(capture.tokenize(title))
    for p in capture.card_files(vault):
        t, _ = capture.read_card(p)
        if not t:
            continue
        score = len(qt & capture.tokenize(t))
        if score > best_score:
            best, best_score = p, score
    return best if best and best_score >= max(3, len(qt) // 2) else None


def apply_actions(actions: list[dict], vault: Path) -> dict:
    rep = {"new": 0, "updated": 0, "none": 0, "dup_skip": 0, "invalid": 0}
    skip = int(cfg_all()["dedup_skip_score"])
    for a in actions:
        if not isinstance(a, dict):
            rep["invalid"] += 1
            continue
        act = a.get("action")
        if act == "NONE":
            rep["none"] += 1
            log(f"NONE: {(a.get('reason') or '')[:120]}")
        elif act == "NEW":
            title = (a.get("title") or "").strip()
            body = (a.get("body") or "").strip()
            if not title or not body:
                rep["invalid"] += 1
                continue
            dup = capture.check_dedup(vault, title)
            if dup and dup[0]["score"] >= skip:
                rep["dup_skip"] += 1
                log(f"NEW 查重跳过：{title}（相似：{dup[0]['title'][:40]}）")
                continue
            ct = a.get("card_type") or "踩坑排查"
            tags = [t for t in (a.get("tags") or []) if t][:6]
            if a.get("sensitive"):
                tags.append("sensitive")
            summary = (a.get("summary") or "").strip()
            full_body = (summary + "\n\n" + body).strip()
            extra: dict = {"card_type": ct}
            files = [f for f in (a.get("files") or []) if f][:6]
            if files:
                extra["files"] = files
            capture.write_card(vault, title, full_body, tags, "快捕", "自动蒸馏", extra)
            rep["new"] += 1
            log(f"NEW: {title}（{ct}）")
        elif act == "UPDATE":
            body = (a.get("body") or "").strip()
            mt = (a.get("match_title") or "").strip()
            if not body:
                rep["invalid"] += 1
                continue
            p = _find_card_by_title(vault, mt) if mt else None
            if p is not None and capture.rewrite_body(p, body):
                rep["updated"] += 1
            else:  # 找不到旧卡 → 降级为过程跟踪新卡
                title = mt or (a.get("title") or "").strip() or "过程跟踪"
                tags = [t for t in (a.get("tags") or []) if t][:6] or ["过程跟踪"]
                capture.write_card(vault, title, body, tags, "快捕", "自动蒸馏",
                                   {"card_type": "过程跟踪"})
                rep["new"] += 1
        elif act == "need_context":
            rep["invalid"] += 1  # 二轮后仍要上下文 → 视为无效
        else:
            rep["invalid"] += 1
    return rep


# ---------------------------------------------------------------- 自维护

def maintain(vault: Path, cfg: dict) -> dict:
    today = dt.date.today()
    arch_days = int(cfg["archive_min_days"])
    backlog_days = int(cfg["backlog_days"])
    rep = {"archived_cold": 0, "archived_backlog": 0, "promotion": []}
    changed = False
    for p in capture.card_files(vault):
        meta = capture.read_meta(p)
        if not meta:
            continue
        status = str(meta.get("status", "")).strip()
        try:
            created = dt.date.fromisoformat(str(meta.get("created", ""))[:10])
        except Exception:
            continue
        age = (today - created).days
        if status == "待确认" and age >= backlog_days:
            capture.set_status(p, "已归档")
            rep["archived_backlog"] += 1
            changed = True
        elif status == "快捕" and age >= arch_days:
            sc = re.sub(r"\D", "", str(meta.get("surfaced_count", "0"))) or "0"
            if int(sc) == 0:
                capture.set_status(p, "已归档")
                rep["archived_cold"] += 1
                changed = True
            elif int(sc) >= 3:
                t, _ = capture.read_card(p)
                rep["promotion"].append(f"{t}（surfaced {sc} 次）")
    if rep["promotion"]:
        try:
            SUGGEST_P.write_text(
                "# 转正建议（AI 只建议，转不转人工定）\n\n"
                + "\n".join("- " + s for s in rep["promotion"]) + "\n",
                encoding="utf-8",
            )
        except Exception:
            pass
    if changed:
        capture.git_commit(vault, "AI: 自维护归档冷卡/待确认积压（S21）")
    return rep


# ---------------------------------------------------------------- 主流程

def _hours_since(ts: str | None) -> float:
    if not ts:
        return 1e9
    try:
        return (dt.datetime.now() - dt.datetime.fromisoformat(ts)).total_seconds() / 3600
    except Exception:
        return 1e9


def distill_once(vault: Path, cfg: dict, records: list[dict]) -> dict:
    material = build_material(records, cfg)
    prompt = build_prompt(records, cfg, vault, material)
    text = call_ai(prompt, cfg)
    actions = parse_actions(text)
    if actions is None:
        retry = call_ai(
            prompt + "\n\n【重试提示】上一次输出无法解析为 JSON。只输出一个 JSON 对象，"
            "第一个字符必须是 {，最后一个字符必须是 }，不要任何其他文字。",
            cfg,
        )
        actions = parse_actions(retry)
        if actions is None:
            raise ValueError(f"AI 输出两次无法解析：{text[:200]!r}")

    # need_context 二轮：ids 扩窗重取材料，补一次调用
    nc = [a for a in actions if isinstance(a, dict) and a.get("action") == "need_context"]
    if nc:
        ids = set()
        for a in nc:
            ids |= {int(x) for x in (a.get("ids") or []) if str(x).lstrip("-").isdigit()}
        ids = {i for i in ids if 0 <= i < len(records)}
        if ids:
            subset = [records[i] for i in sorted(ids)]
            material2 = build_material(subset, cfg, big=True)
            prompt2 = (
                "以下是上一轮你标记 need_context 的书签的更大上下文窗口。\n\n" + material2 +
                "\n\n结合上一轮的全部材料，现在输出最终 JSON 动作（不许再要上下文）。\n\n" + EXIST_NOTE
            )
            text2 = call_ai(prompt2, cfg)
            actions2 = parse_actions(text2)
            if actions2 is not None:
                actions = [a for a in actions if not (isinstance(a, dict) and a.get("action") == "need_context")] + actions2

    rep = apply_actions([a for a in actions if isinstance(a, dict) and a.get("action") != "need_context"], vault)
    if rep["new"] + rep["updated"] > 0:
        capture.git_commit(vault, f"AI: 自动蒸馏 {rep['new']} 新卡 / {rep['updated']} 更新（S21）")
    return rep


def run(vault: Path, cfg: dict, mode: str) -> dict:
    st = load_state()
    sweep_res = sweep(cfg)
    records = load_records(int(cfg["queue_cap"]))
    res: dict = {"mode": mode, "sweep": sweep_res, "backlog": len(records)}

    if not records:
        res["result"] = "无积压"
    elif mode == "maybe" and _hours_since(st.get("last_distill")) < float(cfg["distill_min_hours"]):
        res["result"] = f"距上次蒸馏不足 {cfg['distill_min_hours']}h，跳过"
    else:
        try:
            rep = distill_once(vault, cfg, records)
            consume(records)
            st["last_distill"] = dt.datetime.now().isoformat(timespec="seconds")
            st["fail_count"] = 0
            res["result"] = rep
        except Exception as e:
            fails = int(st.get("fail_count", 0)) + 1
            st["fail_count"] = fails
            if fails >= int(cfg["fail_limit"]):
                bak = triage.QUEUE.parent / (triage.QUEUE.name + ".bak")
                try:
                    triage.QUEUE.replace(bak)
                    log(f"连续失败 {fails} 次，队列已转存 {bak.name}，熔断待人工检查")
                except Exception:
                    pass
            res["result"] = "error"
            res["error"] = str(e)[:300]
            log(f"distill 失败({fails}): {e}")

    # 自维护门控
    due = _hours_since(st.get("last_maintain")) >= float(cfg["maintain_interval_h"])
    if mode in ("run", "maintain") or (mode == "maybe" and due):
        try:
            res["maintenance"] = maintain(vault, cfg)
            st["last_maintain"] = dt.datetime.now().isoformat(timespec="seconds")
        except Exception as e:
            res["maintenance"] = "error"
            res["maintain_error"] = str(e)[:200]
            log(f"maintain 失败: {e}")

    save_state(st)
    log(f"{mode}: {json.dumps(res, ensure_ascii=False)[:400]}")
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--maybe", action="store_true")
    g.add_argument("--run", action="store_true")
    g.add_argument("--maintain", action="store_true")
    g.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    try:
        vault = vault_or_die()
        cfg = cfg_all()
        if a.dry:
            records = load_records(int(cfg["queue_cap"])) or [
                {"line": "示例：LX音源导入超时原来是GitHub raw被墙，换jsDelivr就行", "role": "user",
                 "src": "demo", "fmt": "text", "entry": 0, "part": "line", "h": "demo"}]
            prompt = build_prompt(records, cfg, vault, build_material(records, cfg))
            print(prompt[:2500])
            print(f"\n...（共 {len(prompt)} 字符）")
            return
        if a.maintain:
            res = {"mode": "maintain", "maintenance": maintain(vault, cfg)}
            log(f"maintain: {json.dumps(res, ensure_ascii=False)[:300]}")
        else:
            res = run(vault, cfg, "maybe" if a.maybe else "run")
        print(json.dumps(res, ensure_ascii=False), flush=True)
    except SystemExit as e:
        raise
    except Exception as e:
        log(f"main 异常: {e}")
        print(json.dumps({"mode": "error", "error": str(e)[:300]}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
