import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate.py"
SPEC = importlib.util.spec_from_file_location("skill_release_validator", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PublicPackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.skill = self.root / "skills" / "paper-ppt-cn"
        (self.skill / "agents").mkdir(parents=True)
        (self.skill / "references").mkdir()
        (self.skill / "SKILL.md").write_text(
            "---\nname: paper-ppt-cn\ndescription: Make evidence-based paper presentations.\n---\n\n"
            "# Paper presentations\n\n[Guide](references/guide.md)\n", encoding="utf-8")
        (self.skill / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")
        (self.skill / "agents" / "openai.yaml").write_text(
            'interface:\n  default_prompt: "Use $paper-ppt-cn."\n', encoding="utf-8")

    def test_complete_package_passes(self):
        self.assertEqual(MODULE.validate(self.root), [])

    def test_missing_reference_is_reported(self):
        (self.skill / "references" / "guide.md").unlink()
        self.assertTrue(any("Broken relative" in e for e in MODULE.validate(self.root)))

    def test_personal_path_is_reported_without_echoing_value(self):
        personal = "C:" + chr(92) + "Users" + chr(92) + "ExamplePerson" + chr(92) + "notes"
        (self.root / "notes.md").write_text(personal, encoding="utf-8")
        errors = MODULE.validate(self.root)
        self.assertTrue(any("Personal absolute path" in e for e in errors))
        self.assertTrue(all(personal not in e for e in errors))

    def test_credentials_are_reported_without_echoing_value(self):
        fake = "gh" + "p_" + "x" * 36
        (self.root / "notes.md").write_text(fake, encoding="utf-8")
        errors = MODULE.validate(self.root)
        self.assertTrue(any("Credential-like" in e for e in errors))
        self.assertTrue(all(fake not in e for e in errors))

    def test_third_party_binary_is_not_silently_distributed(self):
        (self.root / "example.pdf").write_bytes(b"sample binary")
        self.assertTrue(any("outside this text-only" in e for e in MODULE.validate(self.root)))

    def test_links_outside_package_are_rejected(self):
        (self.root / "notes.md").write_text("[Outside](../outside.md)", encoding="utf-8")
        self.assertTrue(any("escapes release" in e for e in MODULE.validate(self.root)))


if __name__ == "__main__":
    unittest.main()
