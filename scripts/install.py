"""Preview or install both standalone Codex skills and a native SessionStart hook."""

import argparse
import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shlex
import shutil
import stat
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("vibe-wise-learn", "vibe-wise-reset")


def files(directory):
    result = {}
    for path in directory.rglob("*"):
        if path.is_symlink():
            raise ValueError("Refusing a symlink inside skill: " + str(path))
        if path.is_file():
            result[str(path.relative_to(directory))] = path.read_bytes()
    return result


def atomic_write(path, content, mode=0o600):
    fd, name = tempfile.mkstemp(prefix=".vibe-wise-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            os.fchmod(stream.fileno(), mode)
            stream.write(content)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def install(codex_dir, apply=False):
    codex_dir = Path(codex_dir).expanduser().resolve()
    skills_dir = codex_dir / "skills"
    hooks_file = codex_dir / "hooks.json"
    if skills_dir.is_symlink() or hooks_file.is_symlink():
        raise ValueError("Skill root and hooks.json must not be symlinks.")
    if hooks_file.exists() and not hooks_file.is_file():
        raise ValueError("hooks.json must be a regular file.")
    old_bytes = hooks_file.read_bytes() if hooks_file.exists() else None
    config = json.loads(old_bytes) if old_bytes is not None else {}
    if not isinstance(config, dict) or not isinstance(config.get("hooks", {}), dict):
        raise ValueError("Existing hooks.json has an invalid hooks object.")
    merged = copy.deepcopy(config)
    hooks = merged.setdefault("hooks", {})
    groups = hooks.setdefault("SessionStart", [])
    if not isinstance(groups, list):
        raise ValueError("Existing SessionStart configuration must be a list.")
    script = skills_dir / SKILLS[0] / "scripts" / "session_start.py"
    registration = {
        "matcher": "startup|resume|clear|compact",
        "hooks": [{"type": "command", "command": "python3 " + shlex.quote(str(script)),
                   "timeout": 5, "statusMessage": "Restoring VibeWise learning context"}],
    }
    hook_changed = registration not in groups
    if hook_changed:
        groups.append(registration)
    new_skills = []
    for name in SKILLS:
        destination = skills_dir / name
        if destination.is_symlink():
            raise ValueError("Refusing to replace linked skill: " + str(destination))
        if destination.exists():
            if not destination.is_dir() or files(destination) != files(ROOT / "skills" / name):
                raise ValueError("Existing skill differs; refusing to overwrite: " + str(destination))
        else:
            new_skills.append(name)
    result = {
        "status": "preview", "codex_dir": str(codex_dir),
        "skills": [str(skills_dir / name) for name in SKILLS],
        "new_skills": new_skills, "hooks_file": str(hooks_file),
        "hook_changed": hook_changed,
        "hook_trust": "Codex requires review of new or changed hooks via /hooks.",
    }
    if not apply:
        return result

    skills_dir.mkdir(parents=True, exist_ok=True)
    created = []
    staging = []
    backup = None
    try:
        for name in new_skills:
            stage = Path(tempfile.mkdtemp(prefix=".vibe-wise-install-", dir=skills_dir))
            staging.append(stage)
            shutil.copytree(ROOT / "skills" / name, stage, dirs_exist_ok=True)
            destination = skills_dir / name
            if destination.exists() or destination.is_symlink():
                raise ValueError("Skill target changed during installation: " + str(destination))
            stage.rename(destination)
            created.append(destination)
        current = hooks_file.read_bytes() if hooks_file.exists() else None
        if current != old_bytes or hooks_file.is_symlink():
            raise ValueError("hooks.json changed during installation; retry the preview.")
        if hook_changed:
            mode = stat.S_IMODE(hooks_file.stat().st_mode) if hooks_file.exists() else 0o600
            if old_bytes is not None:
                suffix = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
                backup = hooks_file.with_name("hooks.json.vibe-wise-backup-" + suffix)
                with backup.open("xb") as stream:
                    stream.write(old_bytes)
                backup.chmod(0o600)
            content = (json.dumps(merged, indent=2, ensure_ascii=False) + "\n").encode()
            atomic_write(hooks_file, content, mode)
    except Exception:
        for destination in reversed(created):
            shutil.rmtree(destination)
        raise
    finally:
        for stage in staging:
            if stage.exists():
                shutil.rmtree(stage)
    result["status"] = "installed" if new_skills or hook_changed else "unchanged"
    result["hooks_backup"] = str(backup) if backup else None
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-dir", default=os.environ.get("CODEX_HOME") or str(Path.home() / ".codex"))
    parser.add_argument("--apply", action="store_true", help="Install; default is read-only preview.")
    args = parser.parse_args()
    try:
        result = install(args.codex_dir, args.apply)
    except (OSError, ValueError) as error:
        print(json.dumps({"status": "error", "message": str(error)}))
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
