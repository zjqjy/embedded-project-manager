#!/usr/bin/env python3
"""
generate-script.py — 基于 README 自动生成视频口播稿
用法: python generate-script.py topics/ota-firmware-upgrade/ --author=昵称 --next=下期主题
---
EM-SKILL 学习模式插件 · tools/generate-script.py
归属: plugins/learning/ (与 plugins/embedded/ 同构)
"""

import re, sys
from pathlib import Path
from datetime import datetime

TEMPLATE = """# 🎬 视频口播稿

> 自动生成于 {date} | 基于: {source} | 预计时长: {duration} 分钟

---

## 🎯 开场钩子 (30秒)

{hook}

大家好，我是 {author}，今天我们来聊 {topic}。

---

## 📖 正文

### 第一部分：什么是 {topic}？ (2分钟)

{summary}

### 第二部分：核心架构解析 (3分钟)

{architecture}

### 第三部分：关键代码实战 (4分钟)

{code_demo}

### 第四部分：踩坑与解决方案 (3分钟)

{pitfalls}

---

## 🔗 结尾引导 (30秒)

如果你觉得有用，记得点赞收藏。完整的技术文档和代码已经放在 GitHub，链接在简介里。

下期我们聊 {next_topic}，关注我，不迷路。

---

## 📎 画面提示

- 开场: 展示 GitHub README 截图
- 架构: 展示 Mermaid 图表，配合鼠标指针移动
- 代码: 分屏展示代码 + 实际硬件调试画面
- 踩坑: 展示错误日志 + 修正后的正确输出
- 结尾: 展示 GitHub 仓库二维码

---

*本脚本由 EM-SKILL v4.1 自动生成*
"""

def extract(readme: Path) -> dict:
    with open(readme, 'r', encoding='utf-8') as f: c = f.read()
    s = {}
    m = re.search(r'> (.*?)(?:\n|$)', c)
    s['hook'] = m.group(1) if m else "今天分享一个嵌入式实战技巧"
    m = re.search(r'## 🧠 3 句话总结\n\n(.*?)(?=\n##)', c, re.DOTALL)
    s['summary'] = '\n'.join([l.strip() for l in m.group(1).split('\n') if l.strip() and l.strip()[0].isdigit()]) if m else "（请补充）"
    m = re.search(r'## 📐 核心架构\n\n(.*?)(?=```mermaid)', c, re.DOTALL)
    s['architecture'] = m.group(1).strip() if m else "（请补充）"
    cb = re.findall(r'```c\n(.*?)```', c, re.DOTALL)
    s['code_demo'] = f"我们来看看核心代码：\n\n```c\n{cb[0]}```\n\n（配合屏幕录制展示实际运行效果）" if cb else "（请补充）"
    m = re.search(r'## ⚠️ 踩坑记录\n\n(.*?)(?=\n##)', c, re.DOTALL)
    if m:
        pts = re.findall(r'> \*\*🕳️ (.*?)\*\*', m.group(1))
        s['pitfalls'] = "我们来聊聊实际开发中遇到的坑：\n\n" + '\n'.join([f"{i+1}. {t}" for i, t in enumerate(pts)])
    else: s['pitfalls'] = "（请补充）"
    return s

def main():
    if len(sys.argv) < 2: print("Usage: generate-script.py <topic-dir> [--author=昵称] [--next=主题]"); sys.exit(1)
    d = Path(sys.argv[1]); author, next_t = "你的昵称", "下一个主题"
    for a in sys.argv[2:]:
        if a.startswith('--author='): author = a.split('=')[1]
        elif a.startswith('--next='): next_t = a.split('=')[1]
    s = extract(d / "README.md")
    out = d / "video-script.md"
    with open(out, 'w', encoding='utf-8') as f:
        f.write(TEMPLATE.format(
            date=datetime.now().strftime("%Y-%m-%d"), source=f"{d.name}/README.md",
            duration=13, hook=s['hook'], author=author,
            topic=d.name.replace('-', ' ').title(), summary=s['summary'],
            architecture=s['architecture'], code_demo=s['code_demo'],
            pitfalls=s['pitfalls'], next_topic=next_t
        ))
    print(f"Generated: {out}")

if __name__ == '__main__': main()