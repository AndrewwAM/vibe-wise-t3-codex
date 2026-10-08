"""Probe native Codex skill and hook discovery, without starting a model turn."""

import argparse
import asyncio
import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
from install import install, SKILLS


def toml_value(value):
    if isinstance(value, dict):
        return "{" + ", ".join(json.dumps(key) + " = " + toml_value(item)
                                for key, item in value.items()) + "}"
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(item) for item in value) + "]"
    return json.dumps(value)


async def probe(project, binary, expected_source=None, registration=None):
    arguments = [binary, "app-server", "--stdio", "--disable", "apps", "-c",
                 "analytics.enabled=false"]
    if registration is not None:
        # Test the exact installed declaration as session flags. Project trust
        # cannot be granted by CLI overrides, and fixtures must not change it.
        arguments += ["-c", "hooks.SessionStart=" + toml_value(registration)]
    process = await asyncio.create_subprocess_exec(
        *arguments,
        cwd=project, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL)

    async def send(message):
        process.stdin.write((json.dumps(message) + "\n").encode())
        await process.stdin.drain()

    async def receive(request_id):
        async def read():
            while True:
                line = await process.stdout.readline()
                if not line:
                    raise RuntimeError("Codex app-server exited before responding.")
                response = json.loads(line)
                if response.get("id") == request_id:
                    if "error" in response:
                        raise RuntimeError(json.dumps(response["error"]))
                    return response["result"]
        return await asyncio.wait_for(read(), timeout=20)

    try:
        await send({"id": 1, "method": "initialize", "params": {
            "clientInfo": {"name": "vibe_wise_t3_codex_smoke", "version": "0.1.0-alpha.1"},
            "capabilities": {"experimentalApi": True}}})
        await receive(1)
        await send({"method": "initialized"})
        await send({"id": 2, "method": "skills/list", "params": {
            "cwds": [str(project)], "forceReload": True}})
        skills = await receive(2)
        await send({"id": 3, "method": "hooks/list", "params": {"cwds": [str(project)]}})
        hooks = await receive(3)
        found = [skill for entry in skills["data"] for skill in entry.get("skills", [])
                 if skill["name"] in SKILLS and
                 (expected_source is None or skill["path"].startswith(str(expected_source)))]
        registered = [hook for entry in hooks["data"] for hook in entry.get("hooks", [])
                      if hook.get("statusMessage") == "Restoring VibeWise learning context" and
                      (expected_source is None or str(expected_source) in hook.get("command", ""))]
        if {skill["name"] for skill in found} != set(SKILLS):
            raise RuntimeError("Codex did not discover both VibeWise skills.")
        if not all(skill["enabled"] for skill in found):
            raise RuntimeError("One or more VibeWise skills are disabled.")
        if not registered:
            await send({"id": 4, "method": "config/read", "params": {
                "cwd": str(project), "includeLayers": True}})
            effective = await receive(4)
            # Public error reports must not serialize private configuration.
            details = {
                "reported_hook_count": sum(len(entry.get("hooks", [])) for entry in hooks["data"]),
                "config_layer_count": len(effective.get("layers", [])),
            }
            raise RuntimeError("Codex did not load the VibeWise SessionStart hook: " + json.dumps(details))
        if not all(hook["enabled"] for hook in registered):
            raise RuntimeError("The VibeWise SessionStart hook is disabled.")
        return {"skills": [{"name": skill["name"], "scope": skill.get("scope"),
                            "enabled": skill["enabled"]} for skill in found],
                "hooks": [{"event": hook["eventName"], "enabled": hook["enabled"],
                           "trust": hook["trustStatus"], "source": hook["source"]}
                          for hook in registered]}
    finally:
        if process.returncode is None:
            process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=5)
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", default="codex", help="Codex CLI executable.")
    parser.add_argument("--installed", action="store_true", help="Inspect the installed prototype read-only.")
    args = parser.parse_args()
    if args.installed:
        result = asyncio.run(probe(Path.cwd().resolve(), args.codex))
    else:
        with tempfile.TemporaryDirectory(prefix="vibe-wise-native-smoke-") as temp:
            project = Path(temp).resolve() / "project with spaces"
            project.mkdir()
            subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "init", "--quiet", str(project)], check=True)
            install(project / ".codex", apply=True)
            registration = json.loads((project / ".codex" / "hooks.json").read_text())["hooks"]["SessionStart"]
            result = asyncio.run(probe(project, args.codex, expected_source=project,
                                       registration=registration))
            result["fixture_only"] = True
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, asyncio.TimeoutError) as error:
        print(json.dumps({"status": "error", "message": str(error)}))
        raise SystemExit(1)
