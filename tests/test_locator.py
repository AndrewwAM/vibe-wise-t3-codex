"""Check creation paths without leaking learning state across project boundaries."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("vibe_wise_locator", ROOT / "skills/vibe-wise-learn/scripts/session_start.py")
locator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(locator)


class LocatorTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="vibe-wise-locator-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()

    def test_new_state_belongs_at_git_root_from_a_subdirectory(self):
        project = self.root / "repo"
        nested = project / "src" / "feature"
        nested.mkdir(parents=True)
        (project / ".git").mkdir()
        result = locator.locate(nested)
        self.assertEqual(result["status"], "new")
        self.assertEqual(result["state"], str(project / ".vibe-wise"))
        self.assertFalse((project / ".vibe-wise").exists())

    def test_invalid_nearest_state_does_not_fall_back_to_parent(self):
        (self.root / ".vibe-wise").mkdir()
        nested = self.root / "src"
        nested.mkdir()
        (nested / ".vibe-wise").symlink_to(self.root / ".vibe-wise", target_is_directory=True)
        result = locator.locate(nested)
        self.assertEqual(result["status"], "invalid")
        self.assertIsNone(locator.state_directory(nested))

    def test_no_git_uses_current_directory_for_new_notes(self):
        result = locator.locate(self.root)
        self.assertEqual(result["status"], "new")
        self.assertEqual(result["state"], str(self.root / ".vibe-wise"))
