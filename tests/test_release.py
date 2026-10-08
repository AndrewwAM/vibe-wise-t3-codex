"""Catch accidental state/config publication, including forced Git additions."""

import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("vibe_wise_release", ROOT / "scripts/check_release.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleasePrivacyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="vibe-wise-package-test-")
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name) / "package"
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns(
            ".git", "__pycache__", ".vibe-wise", ".sensible-vibes", ".codex", ".venv"))
        self.git("init", "--quiet")
        self.git("add", ".")

    def git(self, *arguments):
        subprocess.run(["git", "-c", "core.hooksPath=/dev/null", *arguments],
                       cwd=self.repo, check=True, capture_output=True)

    def rules(self):
        return {item["rule"] for item in release.audit(self.repo)["findings"]}

    def test_complete_public_package_passes(self):
        self.assertEqual(release.audit(self.repo)["status"], "ok")

    def test_forced_learning_notes_and_auth_are_rejected(self):
        for name in (".vibe-wise/profile.md", ".sensible-vibes/progress.md", ".codex/auth.json", ".env"):
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("synthetic private data\n")
            self.git("add", "--force", name)
        self.assertIn("private-or-generated-file", self.rules())

    def test_checks_staged_blob_even_if_working_copy_was_sanitized(self):
        path = self.repo / "example.md"
        path.write_text("/" + "home" + "/example-person/private-project/\n")
        self.git("add", "example.md")
        path.write_text("sanitized working copy\n")
        self.assertIn("personal-absolute-path", self.rules())

    def test_linked_file_is_rejected(self):
        (self.repo / "linked.md").symlink_to("README.md")
        self.git("add", "linked.md")
        self.assertIn("symlink-or-submodule", self.rules())

    def test_missing_installed_license_is_rejected(self):
        path = "skills/vibe-wise-reset/LICENSE"
        (self.repo / path).unlink()
        self.git("add", "--update", path)
        self.assertIn("installed-license-differs", self.rules())

    def test_credentials_in_url_do_not_appear_in_diagnostics(self):
        value = "https://" + "example-person:synthetic-pass@" + "example.invalid/repo"
        (self.repo / "example.md").write_text(value)
        self.git("add", "example.md")
        result = release.audit(self.repo)
        self.assertIn("credentials-in-url", {item["rule"] for item in result["findings"]})
        self.assertNotIn("synthetic-pass", str(result))
