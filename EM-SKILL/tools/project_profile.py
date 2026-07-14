"""
EM-SKILL Project Profile Detector  —  S15-D
============================================

一次性项目类型识别；结果缓存到 `<STATE_DIR>/cache/project-profile.json`。
运行时（rec / stat / pi 等）通过缓存读取，不再扫工作区。

CLI:
    python project_profile.py --detect [path]   # 探测并写缓存
    python project_profile.py --show           # 显示缓存内容

识别规则（probe 5 类嵌入式工程标志）：
- Keil      : *.uvprojx / *.uvproj
- CubeMX    : *.ioc
- ESP-IDF   : sdkconfig
- PlatformIO: platformio.ini
- 默认      : general
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

CACHE_FILENAME = "project-profile.json"

# 检测规则：(glob pattern, project type hint, description)
PROBE_RULES = [
    ("*.uvprojx", "embedded-keil", "Keil MDK v5 工程"),
    ("*.uvproj", "embedded-keil", "Keil MDK v4 工程"),
    ("*.ioc", "embedded-cubemx", "STM32CubeMX 工程"),
    ("sdkconfig", "embedded-espidf", "ESP-IDF 工程"),
    ("platformio.ini", "embedded-platformio", "PlatformIO 工程"),
]


def find_state_dir(start: Path) -> Path | None:
    """Locate `.em/` (preferred) or `.emv2/` (fallback)."""
    current = start.resolve()
    for p in [current] + list(current.parents):
        for d in (".em", ".emv2"):
            candidate = p / d
            if candidate.is_dir():
                return candidate
    return None


def detect_profile(project_root: Path) -> dict:
    """Detect project profile by probing workspace markers."""
    matches: list[dict] = []
    for pattern, ptype, desc in PROBE_RULES:
        found = list(project_root.glob(pattern))
        if found:
            matches.append({
                "pattern": pattern,
                "type": ptype,
                "description": desc,
                "files": [str(f.relative_to(project_root)) for f in found[:10]],
            })
    if matches:
        # 多匹配时按优先级（嵌入式为主）
        types = {m["type"] for m in matches}
        if len(types) == 1:
            primary = next(iter(types))
        else:
            primary = "embedded-multi"  # 多类型并存
        return {
            "primary_type": primary,
            "is_embedded": True,
            "matches": matches,
            "profile_version": 1,
        }
    return {
        "primary_type": "general",
        "is_embedded": False,
        "matches": [],
        "profile_version": 1,
    }


def write_cache(profile: dict, cache_file: Path, project_root: Path) -> None:
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "profile_version": profile["profile_version"],
        "detected_at": datetime.now().isoformat(),
        "project_root": str(project_root),
        **profile,
    }
    cache_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="EM-SKILL project profile detector (S15-D)")
    p.add_argument("--detect", nargs="?", const=".", metavar="PATH",
                   help="Detect profile for PATH (default: cwd). Writes cache.")
    p.add_argument("--show", action="store_true", help="Show cached profile and exit.")
    p.add_argument("--json", action="store_true", help="Output as JSON.")
    p.add_argument("--cache-file", type=Path, default=None,
                   help="Override cache file path.")
    args = p.parse_args(argv)

    state_dir = find_state_dir(Path.cwd())
    cache_file = args.cache_file or (state_dir / "cache" / CACHE_FILENAME if state_dir else Path.cwd() / CACHE_FILENAME)

    if args.show:
        if not cache_file.exists():
            print(f"(no cache: {cache_file})", file=sys.stderr)
            return 1
        print(cache_file.read_text(encoding="utf-8"))
        return 0

    if args.detect is not None:
        project_root = Path(args.detect).resolve()
        profile = detect_profile(project_root)
        if not args.json:
            print(f"[OK] Detected: {profile['primary_type']} "
                  f"(embedded={profile['is_embedded']})")
            for m in profile["matches"]:
                print(f"  - {m['pattern']} → {m['type']} ({len(m['files'])} file(s))")
            print(f"  cache: {cache_file}")
        else:
            profile["cache_file"] = str(cache_file)
            print(json.dumps(profile, ensure_ascii=False, indent=2))
        write_cache(profile, cache_file, project_root)
        return 0

    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())