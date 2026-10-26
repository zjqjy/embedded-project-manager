#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hook_session_end.py — 平台 hook 入口（S1-F）

Claude Code SessionEnd / ZCode Stop 都调这个：
stdin 收 JSON（尽力解析 transcript_path），调 triage.py；任何异常都静默退出 0，
hook 永不阻塞会话。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def main() -> int:
    raw = ""
    try:
        raw = sys.stdin.read(1_000_000)
    except Exception:
        pass
    transcript = None
    if raw.strip():
        try:
            obj = json.loads(raw)
            if isinstance(obj, dict):
                for k in ("transcript_path", "transcriptPath", "transcript"):
                    v = obj.get(k)
                    if v and Path(v).exists():
                        transcript = Path(v)
                        break
        except Exception:
            pass
    if transcript is None:
        return 0  # 无 transcript 可分拣（如 ZCode Stop 早期版本），静默
    try:
        import triage
        sys.argv = ["triage.py", "--transcript", str(transcript)]
        triage.main()
    except SystemExit:
        pass
    except Exception as e:
        print(f"triage error: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
