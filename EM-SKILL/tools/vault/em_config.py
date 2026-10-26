#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""em_config.py — ~/.em/config.json 读写：vault 路径解析（S1-C）

被 capture.py / search.py / triage.py / hook_session_end.py 共用。
vault 判定：目录存在 + 含 AGENTS.md 或 30_方法论/（知识库标记）。
"""
import json
import sys
from pathlib import Path

CONFIG_PATH = Path.home() / ".em" / "config.json"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def is_vault(p: Path) -> bool:
    return p.is_dir() and ((p / "AGENTS.md").exists() or (p / "30_方法论").is_dir())


def get_vault() -> Path | None:
    cfg = load_config()
    vp = cfg.get("vault_path")
    if not vp:
        return None
    p = Path(vp)
    return p if is_vault(p) else None


def set_vault(path: str) -> Path:
    p = Path(path).expanduser().resolve()
    if not is_vault(p):
        raise SystemExit(
            f"❌ {p} 不是知识库 vault（缺 AGENTS.md 或 30_方法论/）。\n"
            f"   请确认路径后重试 /em vault connect <路径>"
        )
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    cfg = load_config()
    cfg["vault_path"] = str(p)
    CONFIG_PATH.write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return p


def vault_or_die() -> Path:
    vp = get_vault()
    if vp is None:
        raise SystemExit(
            "❌ 未配置知识库 vault 路径。\n"
            "   运行 /em vault connect <vault路径> 完成连接（一次即可）"
        )
    return vp


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--set":
        p = set_vault(sys.argv[2])
        print(f"🔗 vault 已连接: {p}")
    elif len(sys.argv) >= 2 and sys.argv[1] == "--get":
        vp = get_vault()
        print(vp if vp else "未配置（/em vault connect <路径>）")
    else:
        print("用法: em_config.py --set <vault路径> | --get")
