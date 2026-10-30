#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""setup.py — /em setup 环境自检+修复（S22）

用法:
  python setup.py                 # 默认：全量检测 + 安全项自动修复，JSON+人话双输出
  python setup.py --guide         # 向导模式：不自动修，输出逐项待决清单（由会话 AI 逐项问用户）
  python setup.py --fix-only <id> # 只执行指定检查项的修复
  python setup.py --smoke         # 附带真实引擎冒烟（花少量 token，默认跳过）
  python setup.py --embedded      # 附带嵌入式检查组（原 /em initem 职责，插件注册）
  python setup.py --json          # 只输出 JSON（agent 消费）

检查项三态: ok=就绪 / fix=已自动修(或 --guide 下待确认) / guide=需人工(附精确指引) / info=仅报告。
所有写配置的修复改前备份 .bak-<时间戳>，幂等可重复跑。
插件可经 PLUGIN.md 声明 provides.setup_checks（相对插件目录的模块路径，
模块须提供 register_checks() -> list[dict]）追加检查组——embedded 插件即用此机制。
"""
import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "vault"))  # em_config 在 tools/vault/
sys.path.insert(0, str(Path(__file__).parent))

SKILL_ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
NOW = dt.datetime.now()
TS = NOW.strftime("%Y%m%d-%H%M%S")

ZCODE_CFG = Path.home() / ".zcode" / "cli" / "config.json"
CLAUDE_SETTINGS = Path.home() / ".claude" / "settings.json"
EM_CFG = Path.home() / ".em" / "config.json"
CODEX_SESSIONS = Path.home() / ".codex" / "sessions"

HOOK_END = TOOLS / "vault" / "hook_session_end.py"
HOOK_START = TOOLS / "vault" / "hook_session_start.py"


def nowin() -> int:
    return getattr(subprocess, "CREATE_NO_WINDOW", 0) if sys.platform == "win32" else 0


def run(cmd: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout, creationflags=nowin())


def backup(p: Path) -> Path | None:
    if not p.exists():
        return None
    b = p.with_name(p.name + f".bak-{TS}")
    b.write_bytes(p.read_bytes())
    return b


def read_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_json(p: Path, obj: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- 通用检查组

def check_python() -> dict:
    v = sys.version_info
    if (v.major, v.minor) >= (3, 10):
        return {"state": "ok", "detail": f"Python {v.major}.{v.minor}.{v.micro}"}
    return {"state": "guide",
            "detail": f"Python {v.major}.{v.minor} 过旧（需 ≥3.10）",
            "guide": "安装 Python 3.10+：https://www.python.org/downloads/"}


def check_git() -> dict:
    if shutil.which("git"):
        r = run(["git", "--version"])
        return {"state": "ok", "detail": (r.stdout or "").strip() or "git 可用"}
    return {"state": "guide", "detail": "git 未安装（卡 commit/回溯需要）",
            "guide": "安装 git：https://git-scm.com/downloads"}


def check_vault() -> dict:
    from em_config import get_vault, load_config
    vp = get_vault()
    if vp:
        return {"state": "ok", "detail": f"vault: {vp}"}
    cfg = load_config()
    if cfg.get("vault_path"):
        return {"state": "guide", "detail": f"vault_path 已配置但目录无效: {cfg.get('vault_path')}",
                "guide": "修正目录或重建：/em vault init <目录>"}
    return {"state": "guide", "detail": "未配置知识库 vault",
            "guide": "/em vault init <目录>（任意本地 Markdown 目录即可，无需 Obsidian）"}


def _engine_claude() -> str | None:
    return shutil.which("claude")


def _engine_codex() -> str | None:
    return shutil.which("codex")


def check_engine(cfg: dict, smoke: bool, apply: bool) -> dict:
    """发现链 claude → codex exec → 手动模式；ai_cmd 已显式配置则尊重并只校验"""
    from em_config import save_config
    ai_cmd = cfg.get("ai_cmd")
    if ai_cmd:
        return {"state": "ok", "detail": f"ai_cmd 已配置: {ai_cmd}"}
    if _engine_claude():
        cmd = "claude -p --model haiku"
        if smoke:
            r = run(_resolve_engine_cmd(cmd), input="只回复两个字：就绪", timeout=90)
            if r.returncode != 0 or not r.stdout.strip():
                return {"state": "guide", "detail": "claude CLI 存在但 headless 调用失败（可能未登录）",
                        "guide": "运行 claude 完成登录，或 /em 手动配置 ai_cmd"}
        if not apply:
            return {"state": "guide", "detail": f"可自动修：发现 claude CLI，将写入 ai_cmd = {cmd}",
                    "guide": "确认后执行 /em setup --fix-only engine"}
        save_config({**cfg, "ai_cmd": cmd})
        return {"state": "fix", "detail": f"发现 claude CLI，已写入 ai_cmd = {cmd}"}
    if _engine_codex():
        cmd = "codex exec"
        if not apply:
            return {"state": "guide", "detail": f"可自动修：未装 claude CLI，将写入 ai_cmd = {cmd}",
                    "guide": "确认后执行 /em setup --fix-only engine"}
        save_config({**cfg, "ai_cmd": cmd})
        return {"state": "fix", "detail": f"未装 claude CLI，发现 codex CLI，已写入 ai_cmd = {cmd}"}
    return {"state": "guide",
            "detail": "蒸馏引擎缺失（claude / codex CLI 均未找到）——进入手动模式",
            "guide": "安装 claude CLI：npm install -g @anthropic-ai/claude-code 并登录；"
                     "或装 Codex CLI。不装也可用：vault/入队/检索照常，蒸馏走 /em digest 配好引擎后手动跑"}


def _resolve_engine_cmd(cmd_str: str) -> list[str]:
    import shlex
    parts = shlex.split(cmd_str)
    if sys.platform == "win32":
        exe = shutil.which(parts[0])
        if exe:
            parts[0] = exe
        if parts[0].lower().endswith((".cmd", ".bat")):
            parts = ["cmd", "/c"] + parts
    return parts


def _zcode_hook_present(events: dict, key: str, script: str) -> bool:
    for entry in events.get(key) or []:
        for h in (entry or {}).get("hooks") or []:
            if script in " ".join(h.get("args") or []) or script in str(h.get("command", "")):
                return True
    return False


def _zcode_hook_entry(script: Path, timeout: int) -> dict:
    return {"hooks": [{"type": "process", "command": "python",
                       "args": ["-X", "utf8", str(script)], "timeoutMs": timeout}]}


def check_hook_zcode(apply: bool) -> dict:
    """ZCode Stop(入队) + SessionStart(蒸馏触发) 两处，一次查/修"""
    if not ZCODE_CFG.exists():
        return {"state": "guide", "detail": "未找到 ZCode 配置（~/.zcode/cli/config.json）——非 ZCode 用户可忽略",
                "guide": "使用 ZCode 时重跑 /em setup"}
    cfg = read_json(ZCODE_CFG)
    events = cfg.get("hooks", {}).get("events", {})
    missing = []
    if HOOK_END.exists() and not _zcode_hook_present(events, "Stop", HOOK_END.name):
        missing.append(("Stop", _zcode_hook_entry(HOOK_END, 30000)))
    if HOOK_START.exists() and not _zcode_hook_present(events, "SessionStart", HOOK_START.name):
        missing.append(("SessionStart", _zcode_hook_entry(HOOK_START, 10000)))
    if not missing:
        return {"state": "ok", "detail": "ZCode hook 已注册（Stop 入队 / SessionStart 蒸馏）"}
    detail = f"可自动修：ZCode hook 缺 {', '.join(k for k, _ in missing)} 注册"
    if not apply:
        return {"state": "guide", "detail": detail,
                "guide": "确认后执行 /em setup --fix-only hook_zcode"}
    b = backup(ZCODE_CFG)
    events = cfg.setdefault("hooks", {}).setdefault("events", {})
    for key, entry in missing:
        events.setdefault(key, []).append(entry)
    write_json(ZCODE_CFG, cfg)
    return {"state": "fix", "detail": "ZCode hook 已补注册: " + ", ".join(k for k, _ in missing)
            + (f"（备份 {b.name}）" if b else "")}


def check_hook_claude(apply: bool) -> dict:
    if not CLAUDE_SETTINGS.parent.exists():
        return {"state": "info", "detail": "未使用 Claude Code（~/.claude 不存在），跳过其 hook"}
    st = read_json(CLAUDE_SETTINGS)
    hooks = st.get("hooks", {})
    for e in hooks.get("SessionEnd") or []:
        if HOOK_END.name in str(e):
            return {"state": "ok", "detail": "Claude Code SessionEnd hook 已注册"}
    if not apply:
        return {"state": "guide", "detail": "可自动修：Claude Code 缺 SessionEnd hook（多源 push）",
                "guide": "确认后执行 /em setup --fix-only hook_claude"}
    b = backup(CLAUDE_SETTINGS)
    hooks = st.setdefault("hooks", {})
    entry = {"matcher": "", "hooks": [{"type": "command",
             "command": f"python -X utf8 {HOOK_END}"}]}
    hooks.setdefault("SessionEnd", []).append(entry)
    write_json(CLAUDE_SETTINGS, st)
    return {"state": "fix", "detail": "Claude Code SessionEnd hook 已补注册（多源 push）"
            + (f"（备份 {b.name}）" if b else "")}


def check_codex_sweep(cfg: dict, apply: bool) -> dict:
    if not CODEX_SESSIONS.is_dir():
        return {"state": "info", "detail": "未使用 Codex CLI（~/.codex 不存在），跳过 sweep 源"}
    sources = cfg.get("transcript_sources") or []
    if any(s.get("name") == "codex" for s in sources):
        return {"state": "ok", "detail": "Codex sweep 源已在 transcript_sources"}
    if not apply:
        return {"state": "guide", "detail": "可自动修：检测到 ~/.codex/sessions，将加入 transcript_sources（sweep 拉取）",
                "guide": "确认后执行 /em setup --fix-only codex_sweep"}
    from em_config import save_config
    sources.append({"name": "codex", "path": "~",
                    "glob": ".codex/sessions/**/*.jsonl", "format": "jsonl"})
    save_config({**cfg, "transcript_sources": sources})
    return {"state": "fix", "detail": "Codex sweep 源已写入 transcript_sources"}


# ---------------------------------------------------------------- 插件检查组发现

def _plugin_setup_check_modules() -> list[Path]:
    """扫 plugins/*/PLUGIN.md 的 provides.setup_checks（轻量行解析，不依赖 yaml）"""
    out = []
    plugins = SKILL_ROOT / "plugins"
    if not plugins.is_dir():
        return out
    for pd in sorted(plugins.iterdir()):
        mf = pd / "PLUGIN.md"
        if not mf.is_file():
            continue
        try:
            for ln in mf.read_text(encoding="utf-8", errors="replace").splitlines():
                m = re.match(r"^\s*setup_checks:\s*(.+?)\s*$", ln)
                if m:
                    val = m.group(1).split("#", 1)[0].strip()  # 剥行内注释
                    if val:
                        out.append(pd / val)
                    break
        except Exception:
            continue
    return out


def load_plugin_checks(apply: bool = True) -> list[dict]:
    checks: list[dict] = []
    for mod_path in _plugin_setup_check_modules():
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                f"em_setup_{mod_path.parent.name}", mod_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            checks += mod.register_checks(apply)
        except Exception as e:
            checks.append({"id": f"plugin_{mod_path.parent.name}", "group": "插件",
                           "name": "检查组加载失败", "state": "info",
                           "detail": f"{mod_path}: {e}"})
    return checks


# ---------------------------------------------------------------- runner

def run_group(checks: list[tuple[str, dict]], guide: bool) -> list[dict]:
    results = []
    for cid, c in checks:
        r = {"id": cid, "group": c.get("group", "通用"), "name": c.get("name", cid),
             "state": c.get("state", "info"), "detail": c.get("detail", "")}
        if c.get("guide"):
            r["guide"] = c["guide"]
        results.append(r)
    return results


def human_report(results: list[dict]) -> str:
    icon = {"ok": "✅", "fix": "🔧", "guide": "📋", "info": "ℹ️"}
    lines = ["🩺 /em setup 环境体检"]
    for r in results:
        lines.append(f" {icon.get(r['state'], '·')} [{r['group']}] {r['name']} — {r['detail']}")
        if r["state"] == "guide" and r.get("guide"):
            lines.append(f"      ↳ {r['guide']}")
    n_ok = sum(1 for r in results if r["state"] == "ok")
    n_fix = sum(1 for r in results if r["state"] == "fix")
    n_guide = sum(1 for r in results if r["state"] == "guide")
    lines.append(f"就绪 {n_ok} / 自动修 {n_fix} / 需人工 {n_guide}")
    if n_guide:
        lines.append("📋 项按上面指引处理后重跑 /em setup 复查；--guide 可逐项交互处理")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--guide", action="store_true", help="向导模式：不自动修，列出待决项供逐项确认")
    ap.add_argument("--fix-only", metavar="ID", help="只执行指定检查项的修复")
    ap.add_argument("--smoke", action="store_true", help="附带真实引擎冒烟（花少量 token）")
    ap.add_argument("--embedded", action="store_true", help="附带嵌入式检查组（原 initem 职责）")
    ap.add_argument("--json", action="store_true", help="只输出 JSON")
    a = ap.parse_args()

    try:
        from em_config import load_config
        cfg = load_config()
        apply = not a.guide
        fix_id = a.fix_only

        all_checks: list[tuple[str, object]] = [
            ("python", lambda: {**check_python(), "group": "基础", "name": "Python ≥3.10"}),
            ("git", lambda: {**check_git(), "group": "基础", "name": "git"}),
            ("vault", lambda: {**check_vault(), "group": "知识流", "name": "知识库 vault"}),
            ("engine", lambda: {**check_engine(cfg, a.smoke, apply or fix_id == "engine"),
                                "group": "知识流", "name": "蒸馏引擎"}),
            ("hook_zcode", lambda: {**check_hook_zcode(apply or fix_id == "hook_zcode"),
                                    "group": "知识流", "name": "ZCode hook（入队+蒸馏触发）"}),
            ("hook_claude", lambda: {**check_hook_claude(apply or fix_id == "hook_claude"),
                                     "group": "知识流", "name": "Claude Code SessionEnd hook"}),
            ("codex_sweep", lambda: {**check_codex_sweep(cfg, apply or fix_id == "codex_sweep"),
                                     "group": "知识流", "name": "Codex sweep 源"}),
        ]
        if fix_id:
            checks = [(cid, fn()) for cid, fn in all_checks if cid == fix_id]
            if not checks:
                print(json.dumps({"mode": "error", "error": f"未知检查项: {fix_id}"},
                                 ensure_ascii=False), flush=True)
                return
        else:
            checks = [(cid, fn()) for cid, fn in all_checks]
        if a.embedded:
            checks += [(c.get("id", c.get("name", "?")), c)
                       for c in load_plugin_checks(apply=apply or bool(fix_id))]

        results = run_group(checks, a.guide)
        report = {
            "time": NOW.isoformat(timespec="seconds"),
            "mode": "guide" if a.guide else ("fix-only" if a.fix_only else "auto"),
            "checks": results,
            "summary": {
                "ok": sum(1 for r in results if r["state"] == "ok"),
                "fixed": sum(1 for r in results if r["state"] == "fix"),
                "guide": sum(1 for r in results if r["state"] == "guide"),
                "info": sum(1 for r in results if r["state"] == "info"),
            },
        }
        if a.json:
            print(json.dumps(report, ensure_ascii=False, indent=1), flush=True)
        else:
            print(json.dumps(report, ensure_ascii=False), flush=True)
            print(human_report(results), flush=True)
    except Exception as e:
        print(json.dumps({"mode": "error", "error": str(e)[:300]}, ensure_ascii=False), flush=True)
        sys.exit(0)


if __name__ == "__main__":
    main()
