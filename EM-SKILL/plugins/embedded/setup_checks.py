#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""setup_checks.py — embedded 插件的 /em setup 检查组（S22-C，原 /em initem 职责迁入）

setup.py 经 PLUGIN.md 的 provides.setup_checks 发现本模块并调 register_checks(apply)。
职责（移位不重造）：Claude 权限配置 / CLAUDE.md 触发器注册 / OpenOCD 检测 / 工具路径报告。
芯片工具组合锁定（initem 步骤5）不在自检范围——那是项目级一次性动作，仍走 /em init / /em si。
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = PLUGIN_ROOT.parent.parent
CLAUDE_SETTINGS = Path.home() / ".claude" / "settings.json"

PERM_NEED = [
    "Bash(python */EM-SKILL/plugins/embedded/tools/adapters/*/*.py)",
    "Bash(python */EM-SKILL/plugins/embedded/tools/lib/*.py)",
]


def _run(cmd: list[str], timeout: int = 60, env: dict | None = None) -> subprocess.CompletedProcess:
    nowin = getattr(subprocess, "CREATE_NO_WINDOW", 0) if sys.platform == "win32" else 0
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout, creationflags=nowin, env=env)


def _backup(p: Path) -> str:
    ts = __import__("datetime").datetime.now().strftime("%Y%m%d-%H%M%S")
    b = p.with_name(p.name + f".bak-{ts}")
    b.write_bytes(p.read_bytes())
    return b.name


def _check_permissions(apply: bool) -> dict:
    """initem 步骤1：Claude 权限配置（EM-SKILL 脚本执行白名单）"""
    base = {"id": "emb_permissions", "group": "嵌入式", "name": "Claude 权限配置"}
    if not CLAUDE_SETTINGS.parent.exists():
        return {**base, "state": "info", "detail": "未使用 Claude Code，跳过权限配置"}
    try:
        st = json.loads(CLAUDE_SETTINGS.read_text(encoding="utf-8"))
    except Exception as e:
        return {**base, "state": "guide", "detail": f"settings.json 读取失败: {e}",
                "guide": "手工检查 ~/.claude/settings.json 的 permissions.allow"}
    allow = (st.get("permissions") or {}).get("allow") or []
    missing = [x for x in PERM_NEED if x not in allow]
    if not missing:
        return {**base, "state": "ok", "detail": "EM-SKILL 脚本执行权限已在白名单"}
    if not apply:
        return {**base, "state": "guide",
                "detail": f"可自动修：permissions.allow 缺 {len(missing)} 条 EM-SKILL 白名单",
                "guide": "确认后执行 /em setup --embedded 重跑（自动合并）"}
    b = _backup(CLAUDE_SETTINGS)
    perms = st.setdefault("permissions", {})
    perms["allow"] = list(allow) + missing
    CLAUDE_SETTINGS.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {**base, "state": "fix", "detail": f"已补 {len(missing)} 条权限白名单（备份 {b}）"}


def _check_claude_md(apply: bool) -> dict:
    """initem 步骤6：CLAUDE.md 嵌入式触发器注册（幂等，重活调既有脚本）"""
    base = {"id": "emb_claude_md", "group": "嵌入式", "name": "CLAUDE.md 触发器注册"}
    script = PLUGIN_ROOT / "tools" / "lib" / "register_claude_md.py"
    if not script.exists():
        return {**base, "state": "info", "detail": f"注册脚本缺失: {script}"}
    r = _run([sys.executable, "-X", "utf8", str(script), "--check"])
    if r.returncode == 0:
        return {**base, "state": "ok", "detail": "嵌入式触发器已在 CLAUDE.md 注册"}
    if not apply:
        return {**base, "state": "guide",
                "detail": "可自动修：CLAUDE.md 缺嵌入式工具触发器段（幂等写入指针 ≤10 行）",
                "guide": "确认后执行 /em setup --embedded 重跑（自动注册）"}
    r2 = _run([sys.executable, "-X", "utf8", str(script)])
    if r2.returncode == 0:
        return {**base, "state": "fix", "detail": "CLAUDE.md 触发器已注册（幂等脚本）"}
    return {**base, "state": "guide", "detail": f"注册脚本失败: {(r2.stderr or '')[:120]}",
            "guide": f"手动跑: python {script}"}


def _check_openocd(apply: bool) -> dict:
    """initem 步骤3/4：OpenOCD 检测（重量级下载不自动化，给指引）"""
    base = {"id": "emb_openocd", "group": "嵌入式", "name": "OpenOCD（烧录）"}
    if shutil.which("openocd"):
        return {**base, "state": "ok", "detail": "OpenOCD 在 PATH"}
    appdata = os.environ.get("APPDATA")
    cfg_p = Path(appdata) / "em_skill" / "config.json" if appdata else None
    if cfg_p and cfg_p.exists():
        try:
            v = json.loads(cfg_p.read_text(encoding="utf-8")).get("openocd")
            if v and Path(str(v)).exists():
                return {**base, "state": "ok", "detail": f"OpenOCD 已注册: {v}"}
        except Exception:
            pass
    return {**base, "state": "guide",
            "detail": "OpenOCD 未检测到（烧录必须；编译/检索功能不受影响）",
            "guide": "下载 xpack 版: https://github.com/xpack-dev-tools/openocd-xpack/releases"
                     " 解压后路径写入 %APPDATA%/em_skill/config.json 的 openocd 键，"
                     "或跑一次 /em initem 流程的自动下载"}


def _check_tool_paths(apply: bool) -> dict:
    """initem 步骤2：工具路径探测（报告型）"""
    base = {"id": "emb_tools", "group": "嵌入式", "name": "工具路径探测"}
    script = SKILL_ROOT / "commands" / "scripts" / "detect_tools.py"
    if not script.exists():
        return {**base, "state": "info", "detail": f"探测脚本缺失: {script}"}
    try:
        # detect_tools.py 按安装布局假设 tools/lib 在导入路径——源码树运行需注入 PYTHONPATH
        env = {**os.environ,
               "PYTHONPATH": str(PLUGIN_ROOT / "tools" / "lib") + os.pathsep + os.environ.get("PYTHONPATH", "")}
        r = _run([sys.executable, "-X", "utf8", str(script)], timeout=120, env=env)
    except subprocess.TimeoutExpired:
        return {**base, "state": "info", "detail": "工具探测超时（120s），可稍后单独重跑"}
    tail = (r.stdout or r.stderr or "").strip().splitlines()
    summary = tail[-1][:160] if tail else "无输出"
    return {**base, "state": "info", "detail": f"探测完成: {summary}",
            "guide": f"完整输出: python {script}"}


def register_checks(apply: bool = True) -> list[dict]:
    return [fn(apply) for fn in (_check_permissions, _check_claude_md,
                                 _check_openocd, _check_tool_paths)]


if __name__ == "__main__":
    for c in register_checks(apply=False):
        print(json.dumps(c, ensure_ascii=False))
