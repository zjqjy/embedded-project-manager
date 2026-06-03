#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
changelog_gen.py - Git 提交日志转 CHANGELOG.md 工具

EM-SKILL 专用工具：从 git log 输出解析 EM 自定义 commit 格式，生成
符合 Keep a Changelog 规范的 CHANGELOG.md。

零外部依赖（仅 Python 3 标准库）。

Commit 格式（EM 自定义）：
    [S<n>] type: message
    [S<n>-<sub>] type: message

支持的 type：
    feat      → Added
    fix       → Fixed
    docs      → Documentation
    refactor  → Changed
    test      → Tests
    chore     → Other
    perf      → Changed
    style     → Other
    build     → Other
    ci        → Other
    其他      → Other

用法：
    python changelog_gen.py [--repo <path>] [--output <path>]
                            [--from <tag>] [--to <ref>]
                            [--version <ver>]
"""
from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

# Conventional Commits 风格 type → Keep a Changelog section 映射
_TYPE_TO_SECTION = {
    "feat": "Added",
    "fix": "Fixed",
    "docs": "Documentation",
    "refactor": "Changed",
    "perf": "Changed",
    "test": "Tests",
    "style": "Other",
    "chore": "Other",
    "build": "Other",
    "ci": "Other",
    "revert": "Fixed",
}

# 类别顺序（按 Keep a Changelog 习惯）
_SECTION_ORDER = ["Added", "Changed", "Fixed", "Removed", "Deprecated",
                  "Security", "Documentation", "Tests", "Other"]


@dataclass
class Commit:
    """单条 commit 的解析结果。"""
    sha: str
    step: str               # 来自 [S<n>] 前缀，如 "S10" 或 "S10-D"
    type_: str              # feat / fix / docs / ...
    message: str            # type: 后面的内容
    section: str            # 推导出的 Keep a Changelog section
    date: str = ""          # ISO 日期（YYYY-MM-DD）
    author: str = ""        # 作者（可选）

    @property
    def display(self) -> str:
        """在 CHANGELOG 中显示的一行。"""
        prefix = f"[{self.step}] " if self.step else ""
        return f"- {prefix}{self.message}"


# ---------------------------------------------------------------------------
# 解析逻辑
# ---------------------------------------------------------------------------

# 匹配：[S<n>] 或 [S<n>-<x>] type: message
# 例：[S10] feat: add git workflow
# 例：[S10-D] docs: update initem.md
_COMMIT_RE = re.compile(
    r"^\[(?P<step>S\d+(?:[-A-Z][A-Za-z0-9]*)?)\]\s+"
    r"(?P<type>[a-zA-Z]+)(?:\([^)]*\))?(?P<bang>!)?:\s+"
    r"(?P<msg>.+)$"
)

# 匹配：仅 [S<n>] 前缀，无 type（归类为 Other）
_STEP_ONLY_RE = re.compile(
    r"^\[(?P<step>S\d+(?:[-A-Z][A-Za-z0-9]*)?)\]\s+(?P<msg>.+)$"
)


def parse_commits(git_log_output: str) -> List[Commit]:
    """
    解析 `git log` 的多行输出（每行格式：<sha>|<date>|<author>|<subject>）。

    返回按时间倒序排列的 Commit 列表。
    """
    commits: List[Commit] = []
    for raw in git_log_output.splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.split("|", 3)
        if len(parts) < 4:
            # 容忍宽松格式：仅 subject
            sha, date, author, subject = "", "", "", line
        else:
            sha, date, author, subject = parts[0], parts[1], parts[2], parts[3]

        commit = _parse_subject(sha, date, author, subject.strip())
        if commit is not None:
            commits.append(commit)
    return commits


def _parse_subject(sha: str, date: str, author: str, subject: str) -> Optional[Commit]:
    """从 subject 行解析出 Commit 对象；非 EM 格式则返回 None。"""
    # 主格式：[S<n>] type: msg
    m = _COMMIT_RE.match(subject)
    if m:
        step = m.group("step")
        type_ = m.group("type").lower()
        msg = m.group("msg").strip()
        section = _TYPE_TO_SECTION.get(type_, "Other")
        return Commit(sha=sha, step=step, type_=type_, message=msg,
                      section=section, date=date, author=author)

    # 退化格式：仅有 [S<n>] 前缀
    m2 = _STEP_ONLY_RE.match(subject)
    if m2:
        return Commit(sha=sha, step=m2.group("step"), type_="other",
                      message=m2.group("msg").strip(),
                      section="Other", date=date, author=author)

    # 完全非 EM 格式：跳过（保持 CHANGELOG 干净）
    return None


def group_by_version(commits: List[Commit]) -> Dict[str, List[Commit]]:
    """
    按版本分组 commits。

    分组规则：
    1. 如果两个 commit 之间的版本 tag 不同（或从无 tag 到第一个 tag），按 tag 切分
    2. 简化实现：当前按日期（年月）粗分（与 tag 触发点对齐）

    返回有序字典：key 为版本/时间标签，value 为 commits（按 section 排序后）。
    """
    if not commits:
        return {}

    # 简化策略：按 "YYYY-MM" 分组（每月一个版本段）
    # 实际归档完成时会以 tag 触发，此处给出可用默认
    groups: Dict[str, List[Commit]] = {}
    for c in commits:
        key = _version_key(c.date, c.step)
        groups.setdefault(key, []).append(c)

    # 排序 commits：section 顺序优先，再按 step / message
    for key in groups:
        groups[key].sort(key=lambda x: (
            _SECTION_ORDER.index(x.section) if x.section in _SECTION_ORDER else 99,
            x.step,
            x.message.lower(),
        ))

    return groups


def _version_key(date: str, step: str) -> str:
    """生成版本分组 key。"""
    if not date:
        return f"Unreleased ({step or 'pending'})"
    # 取 YYYY-MM
    ym = date[:7]
    return f"{ym} - {step or 'general'}"


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------

_HEADER_TEMPLATE = """# Changelog

> 项目变更日志 | 由 `tools/git-changelog/changelog_gen.py` 自动生成
> 格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
> commit 遵循 EM 自定义规范 `[Sx] type: message`。

"""

_VERSION_TEMPLATE = "## [{version}] - {date}\n"
_SECTION_HEADER = "### {section}\n"


def render_markdown(groups: Dict[str, List[Commit]],
                    existing: Optional[str] = None) -> str:
    """
    渲染 CHANGELOG.md 文本。

    - `groups`: group_by_version() 的输出
    - `existing`: 现有 CHANGELOG 内容（用于保留"未发布"段落）
    """
    parts: List[str] = [_HEADER_TEMPLATE]

    # 保留 Unreleased 段（来自 existing）
    if existing:
        unreleased = _extract_unreleased(existing)
        if unreleased:
            parts.append("## [Unreleased]\n")
            parts.append(unreleased)
            parts.append("\n")

    if not groups:
        if not parts[-1].strip():
            parts.append("_暂无已发布变更。_\n")
        return "".join(parts)

    for version, commits in groups.items():
        # 推导版本号
        version_label = _format_version_label(version)
        date = commits[0].date if commits else ""

        parts.append(_VERSION_TEMPLATE.format(version=version_label, date=date))

        # 按 section 聚合
        by_section: Dict[str, List[Commit]] = {}
        for c in commits:
            by_section.setdefault(c.section, []).append(c)

        for section in _SECTION_ORDER:
            items = by_section.get(section)
            if not items:
                continue
            parts.append(_SECTION_HEADER.format(section=section))
            for c in items:
                parts.append(c.display + "\n")
            parts.append("\n")

    return "".join(parts)


def _format_version_label(raw: str) -> str:
    """将分组 key 格式化为版本标签。"""
    # raw 形如 "2026-06 - S10"
    if " - " in raw:
        ym, step = raw.split(" - ", 1)
        return f"{ym} ({step})"
    return raw


def _extract_unreleased(text: str) -> str:
    """从现有 CHANGELOG 中提取 [Unreleased] 段。"""
    m = re.search(r"##\s*\[Unreleased\]\s*\n(.*?)(?=\n##\s|\Z)", text, re.DOTALL)
    if not m:
        return ""
    return m.group(1).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Git 集成
# ---------------------------------------------------------------------------

def _run_git_log(repo: Path, git_ref_range: str) -> str:
    """
    在指定仓库中执行 `git log`，输出格式：
        <sha>|<iso-date>|<author>|<subject>
    """
    fmt = "%H|%aI|%an|%s"
    cmd = ["git", "log", f"--pretty=format:{fmt}"]
    if git_ref_range:
        cmd.append(git_ref_range)
    try:
        result = subprocess.run(
            cmd, cwd=str(repo), capture_output=True, text=True,
            encoding="utf-8", check=True,
        )
    except FileNotFoundError:
        raise RuntimeError("未找到 git 命令，请先安装 Git 并加入 PATH")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git log 执行失败：{e.stderr.strip()}")
    return result.stdout


def _detect_ref_range(from_tag: Optional[str], to_ref: str) -> str:
    """根据 from/to 参数构造 git log 的 ref range。"""
    if from_tag:
        # from_tag..to_ref
        return f"{from_tag}..{to_ref}"
    return to_ref


def _detect_version_tag(repo: Path) -> Optional[str]:
    """获取最新 tag（按版本号排序）。"""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=str(repo), capture_output=True, text=True, check=True,
        )
        tag = result.stdout.strip()
        return tag or None
    except subprocess.CalledProcessError:
        return None


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="changelog_gen",
        description="从 git log 生成 CHANGELOG.md（EM-SKILL 专用）",
    )
    parser.add_argument(
        "--repo", default=".",
        help="Git 仓库路径（默认：当前目录）",
    )
    parser.add_argument(
        "--output", "-o", default="./CHANGELOG.md",
        help="输出文件路径（默认：./CHANGELOG.md）",
    )
    parser.add_argument(
        "--from", dest="from_tag", default=None,
        help="起始 tag（默认：自动检测最新 tag）",
    )
    parser.add_argument(
        "--to", default="HEAD",
        help="结束 ref（默认：HEAD）",
    )
    parser.add_argument(
        "--version", default=None,
        help="强制指定当前版本号（覆盖自动检测）",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="仅打印到 stdout，不写文件",
    )
    parser.add_argument(
        "--print-only", action="store_true",
        help="同 --dry-run（兼容别名）",
    )

    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    if not (repo / ".git").exists() and not (repo / ".git").is_file():
        print(f"[!] 警告：{repo} 似乎不是 Git 仓库，继续尝试执行 git log",
              file=sys.stderr)

    from_tag = args.from_tag
    if from_tag is None:
        from_tag = _detect_version_tag(repo)
        if from_tag:
            print(f"[*] 自动检测到最新 tag：{from_tag}", file=sys.stderr)
        else:
            print("[*] 未找到任何 tag，将从仓库起点生成", file=sys.stderr)

    ref_range = _detect_ref_range(from_tag, args.to)
    print(f"[*] git log 范围：{ref_range or args.to}", file=sys.stderr)

    try:
        log_output = _run_git_log(repo, ref_range)
    except RuntimeError as e:
        print(f"[!] {e}", file=sys.stderr)
        return 2

    commits = parse_commits(log_output)
    print(f"[*] 解析到 {len(commits)} 条 EM 格式 commit", file=sys.stderr)

    if not commits and not _file_exists(args.output):
        # 空白 CHANGELOG 模板
        out = _HEADER_TEMPLATE + "## [Unreleased]\n\n_暂无变更。_\n"
    else:
        existing = _read_file(args.output) if _file_exists(args.output) else None
        groups = group_by_version(commits)
        out = render_markdown(groups, existing=existing)

    if args.dry_run or args.print_only:
        sys.stdout.write(out)
        return 0

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(out, encoding="utf-8")
    print(f"[OK] CHANGELOG 已写入：{output_path}", file=sys.stderr)
    return 0


def _file_exists(path: str) -> bool:
    return Path(path).is_file()


def _read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
