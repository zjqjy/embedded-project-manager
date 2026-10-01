#!/usr/bin/env python
"""TI CCS headless 编译 adapter。

这个脚本是 EM-SKILL 嵌入式插件的 **build/ccs adapter**（S17-C 新增），
由 `tools/registry.json` 能力矩阵路由调用（chips.ti.c2000 → build: ccs），支持：

- 探测 CCS 安装路径（eclipsec / eclipse headless 可执行文件）
- 定位 CCS 工程（.ccsproject / .project 所在目录）
- 通过 `com.ti.ccstudio.apps.projectBuild` headless 应用执行编译
- 解析编译日志，提取错误/警告统计与产物路径

适用：TI C2000 / MSP430 / MSPM0 等 CCS 工程（CCS 9.x–12.x，eclipse 内核）。
⚠️ L1 代码完成，L2 硬件实测待 slack_app（TMS320F280033 + CCS 12.5.0）验证。

用法:
    python ccs.py --detect
    python ccs.py --project <CCS 工程目录> [--configuration Debug]
                  [--workspace <dir>] [--ccs-root <CCS 安装目录>]

退出码:
    0 成功 / 1 编译失败 / 2 环境或参数错误
"""

from __future__ import annotations

import argparse
import os
import platform
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# CCS headless 应用（TI 官方，CCS 9+）：
HEADLESS_APP = "com.ti.ccstudio.apps.projectBuild"


def _utf8_console() -> None:
    if sys.platform == "win32":
        for name in ("stdout", "stderr"):
            s = getattr(sys, name, None)
            try:
                if s is not None and hasattr(s, "reconfigure"):
                    s.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


@dataclass
class CCSBuildResult:
    success: bool = False
    errors: int = 0
    warnings: int = 0
    artifacts: list[str] = field(default_factory=list)
    log_lines: list[str] = field(default_factory=list)
    message: str = ""


# ----------------------------------------------------------------------------
# CCS 路径探测：CLI 参数 → 环境变量 → tool_config(.em_skill.json) → 常见安装目录
# ----------------------------------------------------------------------------

def find_eclipsec(ccs_root: str | None = None) -> Path | None:
    """返回 eclipsec.exe（Windows）/ eclipse（Linux）路径。"""
    exe = "eclipsec.exe" if platform.system() == "Windows" else "eclipse"
    if ccs_root:
        p = Path(ccs_root) / "ccs" / "eclipse" / exe
        return p if p.is_file() else None
    if os.environ.get("CCS_PATH"):
        p = Path(os.environ["CCS_PATH"]) / "ccs" / "eclipse" / exe
        if p.is_file():
            return p
    # tool_config（initem 注册，工作区优先于全局）
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
        from tool_config import get_tool_path  # type: ignore
        ccs = get_tool_path("ccs")
        if ccs:
            p = Path(ccs)
            if p.is_file():
                return p
            if p.is_dir():
                q = p / "ccs" / "eclipse" / exe
                if q.is_file():
                    return q
    except Exception:
        pass
    # 常见安装位置（C:\ti\ccs1250\ 等）
    if platform.system() == "Windows":
        for base in (Path("C:/ti"),):
            if base.is_dir():
                for d in sorted(base.glob("ccs*"), reverse=True):
                    p = d / "ccs" / "eclipse" / exe
                    if p.is_file():
                        return p
    else:
        p = Path.home() / "ti" / "ccs" / "eclipse" / exe
        if p.is_file():
            return p
    return None


def find_ccs_project(start: Path) -> Path | None:
    """向上/向下定位 CCS 工程（.ccsproject 或 .project 所在目录）。"""
    start = start.resolve()
    for p in [start] + list(start.parents):
        if (p / ".ccsproject").is_file() or (p / ".project").is_file():
            return p
    # 在工作区向下找（常见：工程在子目录）
    for p in sorted(start.rglob(".ccsproject")):
        return p.parent
    for p in sorted(start.rglob(".project")):
        if (p.parent / ".ccsproject").is_file():
            return p.parent
    return None


# ----------------------------------------------------------------------------
# headless 编译
# ----------------------------------------------------------------------------

def run_headless_build(eclipsec: Path, project: Path, configuration: str,
                       workspace: Path, timeout: int = 900) -> CCSBuildResult:
    """执行 CCS headless 编译并解析结果。"""
    workspace.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(eclipsec),
        "-noSplash",
        "-data", str(workspace),
        "-application", HEADLESS_APP,
        "-ccs.projects", str(project),
        "-ccs.configurations", configuration,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout)
    except FileNotFoundError:
        return CCSBuildResult(message=f"eclipsec 不存在: {eclipsec}")
    except subprocess.TimeoutExpired:
        return CCSBuildResult(message=f"编译超时（>{timeout}s）")

    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    lines = [ln for ln in out.splitlines() if ln.strip()]
    result = CCSBuildResult(log_lines=lines)

    # 结果判定：TI headless 成功时输出 "Build Finished"，失败输出错误统计
    if re.search(r"Build Finished", out, re.IGNORECASE) and proc.returncode == 0:
        result.success = True
    m = re.search(r"(\d+)\s+errors?,\s*(\d+)\s+warnings?", out, re.IGNORECASE)
    if m:
        result.errors, result.warnings = int(m.group(1)), int(m.group(2))
    # 产物：工程目录 <configuration>/ 下的 .out / .hex
    out_dir = project / configuration
    if out_dir.is_dir():
        result.artifacts = [str(p) for p in
                            sorted(list(out_dir.glob("*.out")) + list(out_dir.glob("*.hex")))]
    if not result.message:
        result.message = "成功" if result.success else (
            f"失败（errors={result.errors} warnings={result.warnings}，returncode={proc.returncode}）")
    return result


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    _utf8_console()
    parser = argparse.ArgumentParser(
        prog="ccs-build-adapter",
        description="EM-SKILL build/ccs adapter — TI CCS headless 编译（S17-C）")
    parser.add_argument("--detect", action="store_true", help="只探测 CCS 环境")
    parser.add_argument("--project", type=Path, default=None, help="CCS 工程目录（默认自动扫描）")
    parser.add_argument("--configuration", default="Debug", help="编译配置（默认 Debug）")
    parser.add_argument("--workspace", type=Path, default=None,
                        help="eclipse workspace（默认 <工程>/../.em-ccs-workspace）")
    parser.add_argument("--ccs-root", default=None, help="CCS 安装根目录（覆盖自动探测）")
    parser.add_argument("--timeout", type=int, default=900, help="超时秒数")
    args = parser.parse_args(argv)

    eclipsec = find_eclipsec(args.ccs_root)

    if args.detect:
        print("🔍 CCS 环境探测")
        print(f"  eclipsec: {eclipsec or '未找到（设置 CCS_PATH 或经 /em initem 注册）'}")
        proj = find_ccs_project(Path.cwd())
        print(f"  CCS 工程: {proj or '当前目录未发现'}")
        return 0 if eclipsec else 2

    if not eclipsec:
        print("❌ 未找到 CCS（eclipsec）。请 /em initem 注册，或 --ccs-root 指定，或设 CCS_PATH")
        return 2

    project = args.project or find_ccs_project(Path.cwd())
    if not project:
        print("❌ 未找到 CCS 工程（.ccsproject/.project）。用 --project 指定目录")
        return 2

    workspace = args.workspace or (project.parent / ".em-ccs-workspace")

    print(f"🔧 CCS headless 编译")
    print(f"  eclipsec:     {eclipsec}")
    print(f"  工程:         {project}")
    print(f"  configuration: {args.configuration}")
    r = run_headless_build(eclipsec, project, args.configuration, workspace, args.timeout)

    print(f"\n{'✅' if r.success else '❌'} 编译{'成功' if r.success else '失败'}: {r.message}")
    print(f"  错误: {r.errors}  警告: {r.warnings}")
    for a in r.artifacts:
        size_kb = Path(a).stat().st_size / 1024 if Path(a).exists() else 0
        print(f"  产物: {a} ({size_kb:.0f} KB)")
    if not r.success:
        print("\n--- 日志尾部 ---")
        for ln in r.log_lines[-30:]:
            print(f"  {ln}")
    return 0 if r.success else 1


if __name__ == "__main__":
    sys.exit(main())
