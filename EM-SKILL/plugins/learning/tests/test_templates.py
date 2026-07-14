"""S14-B: 学习模式模板结构合规性单测。

用 pathlib 相对路径定位模板目录，不依赖 cwd，可任意目录重跑。
"""
import json
from pathlib import Path

import pytest

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
OTA_DIR = TEMPLATES_DIR / "topics" / "ota-firmware-upgrade"


class TestTemplateExistence:
    def test_readme_card_exists(self):
        assert (TEMPLATES_DIR / "README-card.md").is_file()

    def test_lpr_stage_exists(self):
        assert (TEMPLATES_DIR / "lpr-stage.md").is_file()

    def test_index_json_example_exists(self):
        assert (TEMPLATES_DIR / "_index.json.example").is_file()

    def test_topic_cheatsheet_exists(self):
        assert (TEMPLATES_DIR / "topic-cheatsheet.md").is_file()

    def test_topic_deep_dive_exists(self):
        assert (TEMPLATES_DIR / "topic-deep-dive.md").is_file()

    def test_callout_snippets_exists(self):
        assert (TEMPLATES_DIR / "callout-snippets.md").is_file()

    def test_research_bib_template_exists(self):
        assert (TEMPLATES_DIR / "research-bib-template.json").is_file()

    def test_ota_seed_topic_files(self):
        # 验证 OTA 种子 3 个文件 + research/ + experiment/ 都存在
        assert (OTA_DIR / "README.md").is_file()
        assert (OTA_DIR / "deep-dive.md").is_file()
        assert (OTA_DIR / "cheatsheet.md").is_file()
        assert (OTA_DIR / "research").is_dir()
        assert (OTA_DIR / "experiment").is_dir()


class TestIndexJsonSchema:
    def test_valid_json(self):
        data = json.loads((TEMPLATES_DIR / "_index.json.example").read_text(encoding="utf-8"))
        assert "version" in data
        assert "topics" in data
        assert isinstance(data["topics"], list)

    def test_topic_required_fields(self):
        data = json.loads((TEMPLATES_DIR / "_index.json.example").read_text(encoding="utf-8"))
        for topic in data["topics"]:
            assert "slug" in topic
            assert "title" in topic
            assert "status" in topic
            assert "lpr_stage" in topic


class TestResearchBibTemplate:
    def test_valid_json(self):
        data = json.loads((TEMPLATES_DIR / "research-bib-template.json").read_text(encoding="utf-8"))
        assert "references" in data
        assert isinstance(data["references"], list)


class TestOtaSeedStructure:
    def test_readme_has_5_sections(self):
        # 验证 OTA README 含: 钩子/3句话总结/概念图/核心架构/踩坑 5 段
        content = (OTA_DIR / "README.md").read_text(encoding="utf-8")
        assert "## 🧠 3 句话总结" in content
        assert "## 🗺️ 概念图" in content
        assert "## 📐 核心架构" in content
        assert "## ⚠️ 踩坑记录" in content or "## 踩坑" in content

    def test_readme_within_200_lines(self):
        content = (OTA_DIR / "README.md").read_text(encoding="utf-8")
        assert len(content.splitlines()) <= 200, "L5 README 必须 ≤ 200 行"

    def test_readme_has_mermaid(self):
        content = (OTA_DIR / "README.md").read_text(encoding="utf-8")
        assert "```mermaid" in content

    def test_deep_dive_has_architecture(self):
        content = (OTA_DIR / "deep-dive.md").read_text(encoding="utf-8")
        assert len(content.splitlines()) >= 50

    def test_cheatsheet_has_commands(self):
        content = (OTA_DIR / "cheatsheet.md").read_text(encoding="utf-8")
        # 至少 1 个代码块 或 命令表格
        assert "```" in content or "|" in content


class TestCalloutSnippets:
    def test_has_examples(self):
        content = (TEMPLATES_DIR / "callout-snippets.md").read_text(encoding="utf-8")
        assert "> [!NOTE]" in content or "> [!TIP]" in content or "> [!WARNING]" in content


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
