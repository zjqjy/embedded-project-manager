import json
from pathlib import Path
import pytest

# 多设备兼容（S17-B 修复）：全部相对本文件解析，不再硬编码机器绝对路径
# 本文件位于 <repo>/EM-SKILL/plugins/learning/tests/
ROOT = Path(__file__).resolve().parents[3]      # EM-SKILL/
REPO = ROOT.parent                              # 仓库根（管家项目自身）
PLUGINS_DIR = ROOT / "plugins"
LEARNING_DIR = PLUGINS_DIR / "learning"
INDEX_FILE = PLUGINS_DIR / "INDEX.md"
README_FILE = ROOT / "README.md"


def _state_dir() -> Path:
    """状态目录：.em/ 优先，回退 .emv2/（与 get_state_dir() 同语义）。"""
    for d in (REPO / ".em", REPO / ".emv2"):
        if d.is_dir():
            return d
    return REPO / ".em"


STATE_DIR = _state_dir()
HISTORY_DIR = STATE_DIR / "history" / "2026" / "07" / "13" / "S10-learning-v4-design"
STATE_FILE = STATE_DIR / "state.md"
SPEC_FILE = STATE_DIR / "project-spec.md"


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
