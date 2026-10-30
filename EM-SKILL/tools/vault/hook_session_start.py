#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hook_session_start.py — SessionStart 触发蒸馏（S21-C）

ZCode SessionStart / Claude Code SessionStart 调这个：
后台拉起 distill.py --maybe（门控：距上次 ≥ min_hours 且有积压才真正跑），
本进程立即退出 0，绝不阻塞会话。任何异常静默（记 distill.log 的是 distill 自己）。
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

DISTILL = Path(__file__).parent / "distill.py"


def main() -> int:
    try:  # 尽力读掉 stdin（平台会传 JSON），内容不需要
        sys.stdin.read(100_000)
    except Exception:
        pass
    if not DISTILL.exists():
        return 0
    try:
        flags = 0
        if sys.platform == "win32":
            flags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NO_WINDOW", 0)
        subprocess.Popen(
            [sys.executable, "-X", "utf8", str(DISTILL), "--maybe"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=flags,
            close_fds=True,
        )
    except Exception:
        pass  # 蒸馏失败/没跑成都不影响会话
    return 0


if __name__ == "__main__":
    sys.exit(main())
