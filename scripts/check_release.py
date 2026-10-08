"""Check the Git-staged package without printing potentially sensitive values."""

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
NAME = "vibe-wise-t3-codex"
REQUIRED = {
    "README.md", "README.es.md", "LICENSE", "ATTRIBUTION.md", "CHANGELOG.md",
    "SECURITY.md", "CONTRIBUTING.md", "plugin.json", "hooks/hooks.json",
    ".github/workflows/ci.yml", "docs/compatibility.md", "docs/testing.md",
    "scripts/install.py", "scripts/smoke_app_server.py", "scripts/check_release.py",
    "skills/vibe-wise-learn/SKILL.md", "skills/vibe-wise-learn/LICENSE",
    "skills/vibe-wise-learn/scripts/session_start.py",
    "skills/vibe-wise-reset/SKILL.md", "skills/vibe-wise-reset/LICENSE",
    "skills/vibe-wise-reset/scripts/reset.py",
}
PRIVATE_PARTS = {
    ".vibe-wise", ".sensible-vibes", ".codex", ".agents", ".ssh", ".aws",
    ".azure", ".venv", "venv", "__pycache__", "node_modules",
}
PRIVATE_NAMES = {"auth.json", "credentials.json", "credentials", "config.toml"}
PRIVATE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".log", ".jsonl", ".pyc"}
PERSONAL_PATH = re.compile(r"/(?:home|Users)/[^/\s\"'<>]+/")
URL_CREDENTIALS = re.compile(r"https?://[^/@\s]+:[^/@\s]+@")


def staged_files(root):
    """Read the index blobs, not a possibly different working-tree copy."""
    process = subprocess.run(
        ["git", "ls-files", "--stage", "-z"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    )
    result = {}
    for entry in process.stdout.split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, blob, stage = metadata.decode("ascii").split()
        path = raw_path.decode("utf-8")
        if stage != "0":
            raise ValueError("Resolve index conflicts before checking a release.")
        content = subprocess.run(
            ["git", "cat-file", "blob", blob], cwd=root,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
        ).stdout
        result[path] = (mode, content)
    return result


def audit(root):
    files = staged_files(root)
    findings = []

    def report(path, rule):
        # Only relative package paths and rule names are safe to include.
        findings.append({"path": path, "rule": rule})

    for path in sorted(REQUIRED - files.keys()):
        report(path, "required-file-missing")
    for path, (mode, content) in files.items():
        parsed = PurePosixPath(path)
        if mode not in {"100644", "100755"}:
            report(path, "symlink-or-submodule")
        if (PRIVATE_PARTS.intersection(parsed.parts)
                or parsed.name in PRIVATE_NAMES or parsed.suffix.lower() in PRIVATE_SUFFIXES
                or (parsed.name.startswith(".env") and parsed.name != ".env.example")
                or parsed.name.startswith(("id_rsa", "id_ed25519", "hooks.json.vibe-wise-backup-"))
                or (parsed.name == "hooks.json" and path != "hooks/hooks.json")):
            report(path, "private-or-generated-file")
        if len(content) > 1024 * 1024:
            report(path, "unexpected-large-file")
        try:
            text = content.decode("utf-8")
        except UnicodeError:
            report(path, "unexpected-binary-file")
            continue
        if "\0" in text:
            report(path, "unexpected-binary-file")
        if PERSONAL_PATH.search(text):
            report(path, "personal-absolute-path")
        if URL_CREDENTIALS.search(text):
            report(path, "credentials-in-url")

    license_bytes = files.get("LICENSE", (None, b""))[1]
    if b"MIT License" not in license_bytes or b"Copyright (c) 2026 Noah Kim" not in license_bytes:
        report("LICENSE", "original-license-notice-missing")
    for name in ("vibe-wise-learn", "vibe-wise-reset"):
        path = "skills/" + name + "/LICENSE"
        if files.get(path, (None, None))[1] != license_bytes:
            report(path, "installed-license-differs")

    try:
        manifest = json.loads(files["plugin.json"][1])
        if (manifest.get("name") != NAME or manifest.get("license") != "MIT"
                or not re.fullmatch(r"\d+\.\d+\.\d+-alpha\.\d+", manifest.get("version", ""))
                or manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
                or manifest.get("extensions", {}).get("com.openai", {}).get("hooks") != "./hooks/hooks.json"):
            report("plugin.json", "invalid-alpha-metadata")
        json.loads(files["hooks/hooks.json"][1])
    except (KeyError, TypeError, ValueError):
        report("plugin.json", "invalid-package-json")
    return {"status": "ok" if not findings else "failed",
            "tracked_files": len(files), "findings": findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        result = audit(args.root)
    except (OSError, ValueError, subprocess.CalledProcessError):
        print(json.dumps({"status": "failed", "message": "Unable to inspect the Git index."}))
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
