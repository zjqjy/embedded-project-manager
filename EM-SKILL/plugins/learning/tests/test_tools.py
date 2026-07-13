"""
test_tools.py — EM-SKILL 学习模式插件 tools/ 单测
覆盖 4 个 L5 Surface 工具脚本的核心逻辑。
"""
import sys
import json
import zipfile
import importlib.util
from pathlib import Path

import pytest

# ---------------------------------------------------------------
# 动态加载带连字符命名的脚本（build-html / generate-script 等）
# ---------------------------------------------------------------
TOOLS_DIR = Path(__file__).parent.parent / "tools"


def _load_module(alias: str, filename: str):
    """以 alias 名为模块名导入 <filename>.py（处理连字符命名）"""
    path = TOOLS_DIR / filename
    spec = importlib.util.spec_from_file_location(alias, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def build_html():
    return _load_module("build_html", "build-html.py")


@pytest.fixture(scope="module")
def generate_script():
    return _load_module("generate_script", "generate-script.py")


@pytest.fixture(scope="module")
def generate_poster():
    return _load_module("generate_poster", "generate-poster.py")


@pytest.fixture(scope="module")
def package_skill():
    return _load_module("package_skill", "package-skill.py")


# ===============================================================
# TestBuildHtml — Markdown → HTML
# ===============================================================
class TestBuildHtml:
    def test_convert_simple_markdown(self, build_html, tmp_path):
        """最小 markdown → HTML 转换"""
        topic = tmp_path / "topic1"
        topic.mkdir()
        (topic / "README.md").write_text("# Hello\n\nThis is **bold**.", encoding="utf-8")
        html = build_html.convert(topic)
        # markdown.toc 自动给 <h1> 加 id 属性，用宽松匹配
        assert "<h1" in html and "Hello</h1>" in html
        assert "<strong>bold</strong>" in html

    def test_video_embedding(self, build_html, tmp_path):
        """[video:url] 自定义语法 → <video> 标签"""
        topic = tmp_path / "topic2"
        topic.mkdir()
        (topic / "README.md").write_text("See [video:http://x.com/v.mp4] here", encoding="utf-8")
        html = build_html.convert(topic)
        assert "<video" in html and "x.com/v.mp4" in html

    def test_missing_readme_raises(self, build_html, tmp_path):
        """README.md 不存在时抛 FileNotFoundError"""
        topic = tmp_path / "empty"
        topic.mkdir()
        with pytest.raises(FileNotFoundError):
            build_html.convert(topic)

    def test_mermaid_block_preserved(self, build_html, tmp_path):
        """Mermaid 代码块保留为 ```mermaid 或 HTML <pre> 块"""
        topic = tmp_path / "topic3"
        topic.mkdir()
        (topic / "README.md").write_text("```mermaid\ngraph TD\nA-->B\n```", encoding="utf-8")
        html = build_html.convert(topic)
        # markdown 库会把 ```mermaid 转成 <pre><code>mermaid ...</code></pre>
        assert "mermaid" in html or "graph TD" in html


# ===============================================================
# TestGenerateScript — README → 视频口播稿
# ===============================================================
class TestGenerateScript:
    def test_template_placeholders(self, generate_script):
        """TEMPLATE 含 {topic} {author} {hook} 占位符"""
        assert "{topic}" in generate_script.TEMPLATE
        assert "{author}" in generate_script.TEMPLATE
        assert "{hook}" in generate_script.TEMPLATE

    def test_template_has_5_sections(self, generate_script):
        """TEMPLATE 含 5 段: 开场钩子/正文/总结/代码/踩坑"""
        assert "开场钩子" in generate_script.TEMPLATE
        assert "核心架构解析" in generate_script.TEMPLATE
        assert "踩坑" in generate_script.TEMPLATE

    def test_extract_hook_from_blockquote(self, generate_script, tmp_path):
        """extract() 能从 > 开头的 blockquote 提取 hook"""
        readme = tmp_path / "README.md"
        readme.write_text("> 一句话钩子\n\n# Title\n", encoding="utf-8")
        s = generate_script.extract(readme)
        assert s["hook"] == "一句话钩子"

    def test_extract_fallback_default(self, generate_script, tmp_path):
        """无 blockquote 时使用默认 hook"""
        readme = tmp_path / "README.md"
        readme.write_text("# No hook here\n\nbody", encoding="utf-8")
        s = generate_script.extract(readme)
        assert "实战技巧" in s["hook"]


# ===============================================================
# TestGeneratePoster — README → SVG 海报
# ===============================================================
class TestGeneratePoster:
    def test_svg_template_has_title_placeholder(self, generate_poster):
        """SVG_TEMPLATE 含 {title} {hook} {badge1} 占位"""
        assert "{title}" in generate_poster.SVG_TEMPLATE
        assert "{hook}" in generate_poster.SVG_TEMPLATE
        assert "{badge1}" in generate_poster.SVG_TEMPLATE

    def test_svg_dimensions(self, generate_poster):
        """SVG 尺寸 1200x630（OG 标准）"""
        assert 'width="1200"' in generate_poster.SVG_TEMPLATE
        assert 'height="630"' in generate_poster.SVG_TEMPLATE

    def test_svg_has_dark_theme_colors(self, generate_poster):
        """暗色主题色 #0d1117"""
        assert "#0d1117" in generate_poster.SVG_TEMPLATE  # 背景色

    def test_generate_creates_svg_file(self, generate_poster, tmp_path):
        """generate() 写出 poster.svg 文件"""
        topic = tmp_path / "topic"
        topic.mkdir()
        (topic / "README.md").write_text("# Title\n> hook\n", encoding="utf-8")
        generate_poster.generate(topic)
        out = topic / "poster.svg"
        assert out.exists()
        assert "<svg" in out.read_text(encoding="utf-8")


# ===============================================================
# TestPackageSkill — 打包为 .skill
# ===============================================================
class TestPackageSkill:
    def test_package_creates_zip(self, package_skill, tmp_path, monkeypatch):
        """package() 在指定目录下创建 .skill 文件"""
        skill_dir = tmp_path / ".claude/skills/em-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Skill", encoding="utf-8")
        out = tmp_path / "em-skill-v4.1.skill"

        ok = package_skill.package(skill_dir=skill_dir, output=out)
        assert ok is True
        assert out.exists()
        assert zipfile.is_zipfile(out)

    def test_zip_contains_manifest(self, package_skill, tmp_path):
        """打包的 zip 含 manifest.json"""
        skill_dir = tmp_path / ".claude/skills/em-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Skill", encoding="utf-8")
        out = tmp_path / "test.skill"

        package_skill.package(skill_dir=skill_dir, output=out)
        with zipfile.ZipFile(out) as zf:
            names = zf.namelist()
            assert "manifest.json" in names
            manifest = json.loads(zf.read("manifest.json"))
            assert manifest["name"] == "em-skill"
            assert manifest["version"] == "4.1.0"

    def test_package_returns_false_on_missing(self, package_skill, tmp_path):
        """skill_dir 不存在时返回 False"""
        ghost = tmp_path / "nope"
        out = tmp_path / "x.skill"
        ok = package_skill.package(skill_dir=ghost, output=out)
        assert ok is False
        assert not out.exists()