#!/usr/bin/env python
"""TI DSLite（XDS100/XDS110）烧录 adapter。

这个脚本是 EM-SKILL 嵌入式插件的 **flash/dslite adapter**（S17-C 新增），
由 `tools/registry.json` 能力矩阵路由调用（chips.ti.c2000 → flash: dslite），支持：

- 探测 DSLite（CCS 自带：`<CCS>/ccs/ccs_base/common/uscif/`）
- 按目标配置（.ccxml）生成烧录命令文件并执行（loadOperation Flash program）
- 可选烧录后复位（restart）
- 解析烧录输出（Succeeded / Error），输出结构化结果

适用：TI C2000 / MSP430 等，XDS100v2 / XDS110 探针。
⚠️ L1 代码完成，L2 硬件实测待 slack_app（TMS320F280033 + XDS100v2）验证。

用法:
    python dslite.py --detect
    python dslite.py --artifact <固件 .out/.hex> --ccxml <目标配置>
                     [--reset-after] [--dslite <dslite 路径>] [--ccs-root <CCS 目录>]

退出码:
    0 成功 / 1 烧录失败 / 2 环境或参数错误
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
class FlashResult:
    success: bool = False
    verified: bool = False
    failure_kind: str = ""   # connection-failure / target-response-abnormal / command-error
    log_lines: list[str] = field(default_factory=list)
    message: str = ""


# ----------------------------------------------------------------------------
# DSLite 探测：CLI 参数 → 环境变量 → tool_config → CCS 安装目录
# ----------------------------------------------------------------------------

def _dslite_name() -> str:
    return "dslite.bat" if platform.system() == "Windows" else "dslite.sh"


def find_ccs_roots() -> list[Path]:
    """常见 CCS 安装根目录（用于推断自带 DSLite）。"""
    roots: list[Path] = []
    if platform.system() == "Windows":
        bases = [Path("C:/ti")]
        for b in bases:
            if b.is_dir():
                roots.extend(sorted(b.glob("ccs*"), reverse=True))
    else:
        p = Path.home() / "ti"
        if p.is_dir():
            roots.extend(sorted(p.glob("ccs*"), reverse=True))
    return roots


def find_dslite(dslite_arg: str | None = None, ccs_root: str | None = None) -> Path | None:
    """返回 DSLite 可执行文件路径。"""
    name = _dslite_name()
    candidates: list[Path] = []

    if dslite_arg:
        p = Path(dslite_arg)
        return p if p.is_file() else None
    if ccs_root:
        candidates.append(Path(ccs_root) / "ccs" / "ccs_base" / "common" / "uscif" / name)
    if os.environ.get("DSLITE_PATH"):
        p = Path(os.environ["DSLITE_PATH"])
        if p.is_file():
            return p
        candidates.append(p / name)
    # tool_config（initem 注册：键 dslite；也可能注册的是 ccs 根）
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
        from tool_config import get_tool_path  # type: ignore
        for key in ("dslite", "ccs"):
            v = get_tool_path(key)
            if v:
                p = Path(v)
                if p.is_file() and key == "dslite":
                    return p
                if p.is_dir():
                    candidates.append(p / "ccs" / "ccs_base" / "common" / "uscif" / name)
    except Exception:
        pass
    # CCS 安装目录扫描
    for root in find_ccs_roots():
        candidates.append(root / "ccs" / "ccs_base" / "common" / "uscif" / name)

    for c in candidates:
        if c.is_file():
            return c
    return None


# ----------------------------------------------------------------------------
# 烧录
# ----------------------------------------------------------------------------

def build_cmd_file(artifact: Path, reset_after: bool) -> str:
    """生成 DSLite 命令文件内容（loadOperation JSON 方言）。"""
    art = str(artifact.resolve()).replace("\\", "/")
    lines = [
        'loadOperation ? {',
        '    "name" : "Flash program",',
        '    "options" : [',
        f'        {{ "program" : "{art}" }}',
        '    ]',
        '}',
    ]
    if reset_after:
        lines.append("restart")
    return "\n".join(lines) + "\n"


def run_flash(dslite: Path, artifact: Path, ccxml: Path, reset_after: bool,
              timeout: int = 300) -> FlashResult:
    if not artifact.is_file():
        return FlashResult(failure_kind="command-error",
                           message=f"固件不存在: {artifact}")
    if not ccxml.is_file():
        return FlashResult(failure_kind="command-error",
                           message=f"目标配置不存在: {ccxml}（从 CCS Debug 导出，或工程 user_files）")

    cmd_file = Path(tempfile.gettempdir()) / "em_dslite_flash.txt"
    cmd_file.write_text(build_cmd_file(artifact, reset_after), encoding="utf-8")

    cmd = [str(dslite), "--config", str(ccxml), "-f", str(cmd_file)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout)
    except FileNotFoundError:
        return FlashResult(failure_kind="command-error", message=f"dslite 不存在: {dslite}")
    except subprocess.TimeoutExpired:
        return FlashResult(failure_kind="target-response-abnormal",
                           message=f"烧录超时（>{timeout}s）")

    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    lines = [ln for ln in out.splitlines() if ln.strip()]
    r = FlashResult(log_lines=lines)

    lowered = out.lower()
    if re.search(r"succeeded", lowered) and proc.returncode == 0:
        r.success = True
        r.verified = "verify" in lowered
        r.message = "烧录成功" + ("（含校验）" if r.verified else "")
    elif re.search(r"error.*connect|connect.*error|unable to open shared library|no target", lowered):
        r.failure_kind = "connection-failure"
        r.message = "连接失败（探针/驱动/供电）"
    elif proc.returncode != 0:
        r.failure_kind = "target-response-abnormal"
        r.message = f"烧录失败（returncode={proc.returncode}）"
    else:
        r.failure_kind = "command-error"
        r.message = "输出未含成功标记，按失败处理"
    return r


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    _utf8_console()
    parser = argparse.ArgumentParser(
        prog="dslite-flash-adapter",
        description="EM-SKILL flash/dslite adapter — TI DSLite/XDS 烧录（S17-C）")
    parser.add_argument("--detect", action="store_true", help="只探测 DSLite 环境")
    parser.add_argument("--artifact", type=Path, default=None, help="固件（.out / .hex）")
    parser.add_argument("--ccxml", type=Path, default=None, help="目标配置文件（.ccxml）")
    parser.add_argument("--reset-after", action="store_true", help="烧录后 restart")
    parser.add_argument("--dslite", default=None, help="dslite 路径（覆盖自动探测）")
    parser.add_argument("--ccs-root", default=None, help="CCS 安装根目录")
    parser.add_argument("--timeout", type=int, default=300, help="超时秒数")
    args = parser.parse_args(argv)

    dslite = find_dslite(args.dslite, args.ccs_root)

    if args.detect:
        print("🔍 DSLite 环境探测")
        print(f"  dslite: {dslite or '未找到（CCS 安装目录 / DSLITE_PATH / initem 注册）'}")
        print(f"  CCS 根: {find_ccs_roots()[:3] or '未发现'}")
        return 0 if dslite else 2

    if not dslite:
        print("❌ 未找到 DSLite。请 /em initem 注册，或 --dslite 指定，或设 DSLITE_PATH")
        return 2
    if not args.artifact or not args.ccxml:
        print("❌ 需要 --artifact <固件> --ccxml <目标配置>（来源 registry flash_args / initem 锁定）")
        return 2

    print("🔧 DSLite 烧录")
    print(f"  dslite:   {dslite}")
    print(f"  固件:     {args.artifact}")
    print(f"  ccxml:    {args.ccxml}")
    r = run_flash(dslite, args.artifact, args.ccxml, args.reset_after, args.timeout)

    mark = "✅" if r.success else "❌"
    print(f"\n{mark} {r.message}")
    print(f"  校验: {'verified' if r.verified else 'skipped'}"
          + (f"  失败分类: {r.failure_kind}" if r.failure_kind else ""))
    if not r.success:
        print("\n--- 日志尾部 ---")
        for ln in r.log_lines[-30:]:
            print(f"  {ln}")
    return 0 if r.success else 1


if __name__ == "__main__":
    sys.exit(main())
