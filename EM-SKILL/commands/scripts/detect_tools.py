#!/usr/bin/env python
"""自动探测嵌入式开发工具路径并注册到 tool_config。"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

# 加入 embed-ai-tool 的 shared 路径
_EMBED_AI_TOOL = Path(
    __file__).resolve().parents[3] / "embed-ai-tool"
# 优先使用 EM-SKILL 内置的 shared
_EM_TOOLS_SHARED = Path(
    __file__).resolve().parents[3] / "EM-SKILL" / "tools" / "shared"
if (_EM_TOOLS_SHARED / "tool_config.py").exists():
    sys.path.insert(0, str(_EM_TOOLS_SHARED))
else:
    # fallback 到 embed-ai-tool 的 shared
    _shared = _EMBED_AI_TOOL / "shared"
    if _shared.exists():
        sys.path.insert(0, str(_shared))
from tool_config import set_tool_path, list_tools

# ── 探测策略 ──────────────────────────────────────────────

TOOL_CHECKS: dict[str, list[str | Path]] = {
    "uv4": [
        # PATH 查找
        "UV4.exe",
        # Keil MDK 常见安装路径
        "C:/Keil_v5/UV4/UV4.exe",
        "C:/Keil/UV4/UV4.exe",
        "C:/Program Files/Keil/UV4/UV4.exe",
        "C:/Program Files (x86)/Keil/UV4/UV4.exe",
        "C:/Program Files/MDK/UV4/UV4.exe",
        "C:/Program Files (x86)/MDK/UV4/UV4.exe",
    ],
    "openocd": [
        "openocd",
        "openocd.exe",
        # xpack 常见路径
        str(Path.home() / "AppData/Local/xpack-openocd/*/bin/openocd.exe"),
        "C:/Program Files/xpack-openocd/*/bin/openocd.exe",
        "C:/Program Files (x86)/xpack-openocd/*/bin/openocd.exe",
        "C:/OpenOCD*/bin/openocd.exe",
        "D:/OpenOCD*/bin/openocd.exe",
    ],
    "jlink": [
        "JLink.exe",
        "JLink",
        "C:/Program Files/SEGGER/JLink*/JLink.exe",
        "C:/Program Files (x86)/SEGGER/JLink*/JLink.exe",
    ],
}

# 额外检查的注册表/环境变量位置
REGISTRY_HINTS: dict[str, list[str]] = {
    "uv4": ["MDK_PATH", "KEIL_PATH", "UV4_PATH"],
    "openocd": ["OPENOCD_PATH", "OPENOCD_HOME"],
    "jlink": ["JLINK_PATH", "SEGGER_PATH", "JLink_PATH"],
}


def find_tool(name: str, checks: list[str | Path]) -> str | None:
    """依次尝试 PATH 查找、路径校验、通配符扫描。"""
    for candidate in checks:
        candidate_str = str(candidate)
        # 先试 shutil.which（处理 PATH 和扩展名）
        found = shutil.which(candidate_str)
        if found:
            return os.path.normpath(found)

        # 通配符路径（含 *）
        if "*" in candidate_str:
            from glob import glob
            matches = sorted(glob(candidate_str))
            if matches:
                return os.path.normpath(matches[0])

        # 精确路径校验
        p = Path(candidate_str)
        if p.exists():
            return os.path.normpath(str(p.resolve()))

    # 环境变量探测
    for env_key in REGISTRY_HINTS.get(name, []):
        env_val = os.environ.get(env_key)
        if env_val:
            env_path = Path(env_val)
            if env_path.is_dir():
                # 如果是目录，找里面的可执行文件
                exe_name = {
                    "uv4": "UV4.exe",
                    "openocd": "openocd.exe",
                    "jlink": "JLink.exe",
                }.get(name, name)
                for exe in env_path.rglob(exe_name):
                    return os.path.normpath(str(exe))
            elif env_path.exists():
                return os.path.normpath(str(env_path))

    return None


def main() -> int:
    print("🔧 embed-ai-tool 工具路径自动探测\n")
    print(f"项目根: {_EMBED_AI_TOOL.parent}\n")

    found_count = 0
    missing_count = 0

    for tool_name, checks in TOOL_CHECKS.items():
        path = find_tool(tool_name, checks)
        if path:
            print(f"  ✅ {tool_name}: {path}")
            set_tool_path(tool_name, path, global_=True)
            found_count += 1
        else:
            print(f"  ⬜ {tool_name}: 未自动找到")
            missing_count += 1

    print(f"\n{'═' * 50}")
    print(f"结果: {found_count} 个工具已注册, {missing_count} 个需手动配置\n")

    if missing_count > 0:
        print("手动注册命令参考:")
        print(f'  python -c "')
        print(f'  import sys; sys.path.insert(0, r\'{_EMBED_AI_TOOL}\')')
        print(f'  from shared.tool_config import set_tool_path')
        print(f'  set_tool_path(\'<工具名>\', r\'<完整路径>\', global_=True)')
        print(f'  print(\'✅ 已注册\')')
        print(f'  "')

    print("\n当前已注册工具:")
    existing = list_tools()
    if existing:
        for name, info in existing.items():
            print(f"  {name}: {info['path']} ({info['source']})")
    else:
        print("  (无)")

    return 0 if found_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
