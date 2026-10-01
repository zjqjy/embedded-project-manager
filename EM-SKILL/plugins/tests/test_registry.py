"""
EM-SKILL embedded tool registry tests — S17-B
==============================================

验证 tools/registry.json 能力矩阵的自洽性：
1. JSON 可解析、动词声明完整
2. 声明的 adapter 文件真实存在
3. 每个 chips 条目引用的 adapter 都在 adapters 段注册

Run:    python -m pytest EM-SKILL/plugins/tests/test_registry.py
"""
from __future__ import annotations

import json
from pathlib import Path
import unittest

EMBEDDED_TOOLS = Path(__file__).resolve().parents[1] / "embedded" / "tools"
REGISTRY_FILE = EMBEDDED_TOOLS / "registry.json"

REQUIRED_VERBS = {"build", "flash", "observe"}


def _load() -> dict:
    return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))


class TestRegistryStructure(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.reg = _load()

    def test_registry_file_exists(self):
        self.assertTrue(REGISTRY_FILE.exists(), f"missing: {REGISTRY_FILE}")

    def test_verbs_declared(self):
        self.assertTrue(REQUIRED_VERBS.issubset(set(self.reg["verbs"])))

    def test_adapters_declared_per_verb(self):
        for verb in REQUIRED_VERBS:
            self.assertIn(verb, self.reg["adapters"], f"adapters 缺 {verb} 段")
            self.assertTrue(self.reg["adapters"][verb], f"adapters.{verb} 为空")


class TestAdapterFiles(unittest.TestCase):

    def setUp(self):
        self.reg = _load()

    def test_every_declared_adapter_file_exists(self):
        missing = []
        for verb, adapters in self.reg["adapters"].items():
            for name, meta in adapters.items():
                f = EMBEDDED_TOOLS / meta["file"]
                if not f.is_file():
                    missing.append(f"{verb}/{name} → {meta['file']}")
        self.assertEqual(missing, [], f"adapter 文件缺失: {missing}")

    def test_legacy_adapters_migrated(self):
        """S17-B 迁移后旧目录不应存在"""
        for legacy in ("build-keil", "flash-openocd", "serial-monitor", "shared"):
            self.assertFalse((EMBEDDED_TOOLS / legacy).exists(),
                             f"旧目录残留: {legacy}")
        self.assertTrue((EMBEDDED_TOOLS / "lib" / "tool_config.py").exists())


class TestChipEntries(unittest.TestCase):

    def setUp(self):
        self.reg = _load()

    def test_known_vendors_present(self):
        for vendor in ("st", "gd", "ti"):
            self.assertIn(vendor, self.reg["chips"], f"chips 缺 {vendor}")

    def test_chip_entries_reference_registered_adapters(self):
        bad = []
        for vendor, families in self.reg["chips"].items():
            for family, cap in families.items():
                for verb, spec in cap.items():
                    if verb not in REQUIRED_VERBS or not isinstance(spec, dict):
                        continue
                    adapter = spec.get("adapter")
                    if adapter not in self.reg["adapters"].get(verb, {}):
                        bad.append(f"{vendor}.{family}.{verb} → {adapter}")
        self.assertEqual(bad, [], f"chips 引用了未注册的 adapter: {bad}")

    def test_ti_c2000_build_flash_route(self):
        """S17-C：TI C2000 应路由到 ccs + dslite"""
        ti = self.reg["chips"]["ti"]["c2000"]
        self.assertEqual(ti["build"]["adapter"], "ccs")
        self.assertEqual(ti["flash"]["adapter"], "dslite")


if __name__ == "__main__":
    unittest.main(verbosity=2)
