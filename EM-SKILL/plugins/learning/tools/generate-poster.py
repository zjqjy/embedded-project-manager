#!/usr/bin/env python3
"""
generate-poster.py — 生成社交媒体海报 (SVG)
用法: python generate-poster.py topics/ota-firmware-upgrade/
---
EM-SKILL 学习模式插件 · tools/generate-poster.py
归属: plugins/learning/ (与 plugins/embedded/ 同构)
"""

import json, sys
from pathlib import Path
from datetime import datetime

SVG_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#0d1117"/>
  <rect x="40" y="40" width="1120" height="550" rx="16" fill="#161b22" stroke="#30363d" stroke-width="2"/>
  <text x="80" y="120" font-family="system-ui, sans-serif" font-size="48" font-weight="bold" fill="#58a6ff">{title}</text>
  <text x="80" y="180" font-family="system-ui, sans-serif" font-size="24" fill="#8b949e">{hook}</text>
  <rect x="80" y="220" width="200" height="40" rx="20" fill="rgba(88,166,255,0.15)"/>
  <text x="180" y="248" font-family="system-ui, sans-serif" font-size="16" font-weight="600" fill="#58a6ff" text-anchor="middle">{badge1}</text>
  <rect x="300" y="220" width="120" height="40" rx="20" fill="rgba(63,185,80,0.15)"/>
  <text x="360" y="248" font-family="system-ui, sans-serif" font-size="16" font-weight="600" fill="#3fb950" text-anchor="middle">{badge2}</text>
  <rect x="80" y="300" width="1040" height="2" fill="#30363d"/>
  <text x="80" y="350" font-family="system-ui, sans-serif" font-size="20" fill="#c9d1d9">{summary1}</text>
  <text x="80" y="390" font-family="system-ui, sans-serif" font-size="20" fill="#c9d1d9">{summary2}</text>
  <text x="80" y="430" font-family="system-ui, sans-serif" font-size="20" fill="#c9d1d9">{summary3}</text>
  <text x="80" y="540" font-family="system-ui, sans-serif" font-size="18" fill="#8b949e">EM-SKILL v4.1 | {date}</text>
  <text x="80" y="570" font-family="system-ui, sans-serif" font-size="18" fill="#8b949e">github.com/zjqjy/embedded-project-manager</text>
</svg>"""

def generate(topic_dir: Path):
    readme = topic_dir / "README.md"
    with open(readme, 'r', encoding='utf-8') as f: c = f.read()
    import re
    title = re.search(r'^# (.*)', c)
    title = title.group(1) if title else topic_dir.name
    hook = re.search(r'> (.*?)(?:\n|$)', c)
    hook = hook.group(1) if hook else ""
    badges = re.findall(r'!\[([^\]]+)\]\([^)]+\)', c)
    s = re.search(r'## 🧠 3 句话总结\n\n(.*?)(?=\n##)', c, re.DOTALL)
    sums = ["", "", ""]
    if s:
        lines = [l.strip() for l in s.group(1).split('\n') if l.strip() and l.strip()[0].isdigit()]
        for i, l in enumerate(lines[:3]): sums[i] = l
    out = topic_dir / "poster.svg"
    with open(out, 'w', encoding='utf-8') as f:
        f.write(SVG_TEMPLATE.format(
            title=title, hook=hook[:60] + "..." if len(hook) > 60 else hook,
            badge1=badges[0] if len(badges) > 0 else "STM32",
            badge2=badges[2] if len(badges) > 2 else "Embedded",
            summary1=sums[0][:80] + "..." if len(sums[0]) > 80 else sums[0],
            summary2=sums[1][:80] + "..." if len(sums[1]) > 80 else sums[1],
            summary3=sums[2][:80] + "..." if len(sums[2]) > 80 else sums[2],
            date=datetime.now().strftime("%Y-%m-%d")
        ))
    print(f"Generated: {out}")

def main():
    if len(sys.argv) < 2: print("Usage: generate-poster.py <topic-dir>"); sys.exit(1)
    generate(Path(sys.argv[1]))

if __name__ == '__main__': main()