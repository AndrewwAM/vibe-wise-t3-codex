"""Verify installation preserves unrelated configuration and user changes."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("vibe_wise_install", ROOT / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="vibe-wise-install-test-")
        self.addCleanup(temporary.cleanup)
        self.codex = Path(temporary.name) / "codex profile with spaces"

    def test_preview_does_not_create_any_files(self):
        result = installer.install(self.codex)
        self.assertEqual(result["status"], "preview")
        self.assertFalse(self.codex.exists())

    def test_install_preserves_existing_hooks_and_is_idempotent(self):
        self.codex.mkdir()
        old = {"description": "Keep this", "custom": {"value": 3},
               "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "true"}]}]}}
        original = json.dumps(old, separators=(",", ":")).encode()
        hookfile = self.codex / "hooks.json"
        hookfile.write_bytes(original)
        first = installer.install(self.codex, apply=True)
        new = json.loads(hookfile.read_bytes())
        self.assertEqual(new["hooks"]["Stop"], old["hooks"]["Stop"])
        self.assertEqual(new["description"], old["description"])
        self.assertEqual(new["custom"], old["custom"])
        self.assertEqual(Path(first["hooks_backup"]).read_bytes(), original)
        for name in installer.SKILLS:
            self.assertEqual(installer.files(self.codex / "skills" / name),
                             installer.files(ROOT / "skills" / name))
        before = hookfile.read_bytes()
        second = installer.install(self.codex, apply=True)
        self.assertEqual(second["status"], "unchanged")
        self.assertEqual(hookfile.read_bytes(), before)
        self.assertEqual(len(list(self.codex.glob("hooks.json.vibe-wise-backup-*"))), 1)

    def test_conflicting_skill_is_not_overwritten(self):
        skill = self.codex / "skills" / installer.SKILLS[0]
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("User's different skill")
        with self.assertRaises(ValueError):
            installer.install(self.codex, apply=True)
        self.assertEqual((skill / "SKILL.md").read_text(), "User's different skill")
        self.assertFalse((self.codex / "hooks.json").exists())
        self.assertFalse((skill.parent / installer.SKILLS[1]).exists())

    def test_hook_write_failure_removes_only_newly_installed_skills(self):
        self.codex.mkdir()
        original = b'{"hooks": {"Stop": []}}\n'
        (self.codex / "hooks.json").write_bytes(original)
        with patch.object(installer, "atomic_write", side_effect=OSError("fixture write failure")):
            with self.assertRaises(OSError):
                installer.install(self.codex, apply=True)
        self.assertEqual((self.codex / "hooks.json").read_bytes(), original)
        self.assertEqual(list((self.codex / "skills").iterdir()), [])

    def test_linked_hooks_file_is_rejected_without_changing_target(self):
        self.codex.mkdir()
        target = self.codex.parent / "other-hooks.json"
        target.write_text('{}\n')
        (self.codex / "hooks.json").symlink_to(target)
        with self.assertRaises(ValueError):
            installer.install(self.codex, apply=True)
        self.assertEqual(target.read_text(), '{}\n')
        self.assertFalse((self.codex / "skills").exists())
