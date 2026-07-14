#!/usr/bin/env python3
"""
package-skill.py — 打包 EM-SKILL 为 .skill 文件
用法: python package-skill.py
---
EM-SKILL 学习模式插件 · tools/package-skill.py
归属: plugins/learning/ (与 plugins/embedded/ 同构)
注: 路径默认以 CWD 为基准（项目根目录），调用方需先 cd 到项目根。
"""

import zipfile, json
from pathlib import Path
from datetime import datetime

def package(skill_dir: Path = None, output: Path = None):
    # 默认路径保持 CWD-相对，向后兼容 CLI 行为
    skill_dir = Path(skill_dir) if skill_dir else Path('.claude/skills/em-skill')
    output = Path(output) if output else Path('em-skill-v4.1.skill')
    if not skill_dir.exists(): print(f"Error: {skill_dir} not found"); return False

    manifest = {
        "name": "em-skill",
        "version": "4.1.0",
        "description": "Embedded Project Manager + Learning Mode",
        "author": "zjqjy",
        "license": "MIT",
        "entry": "SKILL.md",
        "includes": [".em/learning/templates/", ".em/learning/scripts/"]
    }

    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('manifest.json', json.dumps(manifest, indent=2))
        for f in skill_dir.rglob('*'):
            if f.is_file(): zf.write(f, f.relative_to(skill_dir.parent))
    print(f"Packaged: {output} ({output.stat().st_size / 1024:.1f} KB)")
    return True

if __name__ == '__main__': package()