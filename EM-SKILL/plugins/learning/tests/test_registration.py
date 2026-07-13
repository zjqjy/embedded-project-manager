import json
from pathlib import Path
import pytest

ROOT = Path(r"F:\workspace\embedded-project-manager\EM-SKILL")
PLUGINS_DIR = ROOT / "plugins"
LEARNING_DIR = PLUGINS_DIR / "learning"
INDEX_FILE = PLUGINS_DIR / "INDEX.md"
README_FILE = ROOT / "README.md"

HISTORY_DIR = Path(r"F:\workspace\embedded-project-manager\.emv2\history\2026\07\13\S10-learning-v4-design")
STATE_FILE = Path(r"F:\workspace\embedded-project-manager\.emv2\state.md")
SPEC_FILE = Path(r"F:\workspace\embedded-project-manager\.emv2\project-spec.md")


class TestPluginRegistration:
    def test_index_file_exists(self):
        assert INDEX_FILE.exists()

    def test_index_lists_embedded(self):
        content = INDEX_FILE.read_text(encoding="utf-8")
        assert "embedded" in content
        assert "plugins/embedded/" in content

    def test_index_lists_learning(self):
        content = INDEX_FILE.read_text(encoding="utf-8")
        assert "learning" in content
        assert "plugins/learning/" in content

    def test_readme_has_plugins_section(self):
        content = README_FILE.read_text(encoding="utf-8")
        # 中文/英文 "插件" 或 "Plugins"
        assert "插件" in content or "Plugins" in content or "Plugin" in content

    def test_readme_mentions_learning_plugin(self):
        content = README_FILE.read_text(encoding="utf-8")
        assert "learning" in content

    def test_readme_links_to_index(self):
        content = README_FILE.read_text(encoding="utf-8")
        assert "INDEX.md" in content or "plugins/INDEX.md" in content

    def test_learning_plugin_md_exists(self):
        assert (LEARNING_DIR / "PLUGIN.md").exists()


class TestArchive:
    def test_archive_dir_exists(self):
        assert HISTORY_DIR.exists()

    def test_archive_has_brainstorm(self):
        assert (HISTORY_DIR / "brainstorm.md").exists()

    def test_archive_has_split(self):
        assert (HISTORY_DIR / "split.md").exists()

    def test_archive_has_requirements(self):
        """req.md 被重命名为 requirements.md"""
        assert (HISTORY_DIR / "requirements.md").exists()

    def test_archive_has_hardware(self):
        assert (HISTORY_DIR / "hardware.md").exists()

    def test_archive_has_milestones(self):
        assert (HISTORY_DIR / "milestones.md").exists()

    def test_archive_has_status_json(self):
        assert (HISTORY_DIR / "status.json").exists()
        data = json.loads((HISTORY_DIR / "status.json").read_text(encoding="utf-8"))
        assert data.get("step") == "S10"

    def test_archive_has_execution_log(self):
        assert (HISTORY_DIR / "execution-log.md").exists()

    def test_archive_has_readme(self):
        assert (HISTORY_DIR / "README.md").exists()


class TestStateSync:
    def test_state_md_updated(self):
        content = STATE_FILE.read_text(encoding="utf-8")
        # S14 应该标记为完成或进行中
        assert "S14" in content

    def test_state_next_action_is_verify(self):
        content = STATE_FILE.read_text(encoding="utf-8")
        assert "/em verify" in content

    def test_project_spec_updated(self):
        content = SPEC_FILE.read_text(encoding="utf-8")
        # S14 行存在
        assert "| S14 |" in content
