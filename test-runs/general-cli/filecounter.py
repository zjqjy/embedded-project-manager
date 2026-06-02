#!/usr/bin/env python3
"""filecounter — 统计目录中的文件数量

用法:
    python filecounter.py <path>           # 只统计顶层文件
    python filecounter.py <path> -r        # 递归统计所有子目录文件
"""
import argparse
import os
import sys


def count_files(path: str, recursive: bool = False) -> int:
    if recursive:
        total = 0
        for _root, _dirs, files in os.walk(path):
            total += len(files)
        return total
    return sum(1 for entry in os.scandir(path) if entry.is_file())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="统计目录中的文件数量")
    parser.add_argument("path", help="目标目录路径")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="递归统计子目录中的文件")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.path):
        print(f"error: not a directory: {args.path}", file=sys.stderr)
        return 2

    n = count_files(args.path, recursive=args.recursive)
    mode = "recursive" if args.recursive else "top-level"
    print(f"{args.path}: {n} files ({mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
