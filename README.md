# VibeWise for T3 Code and Codex

[![CI](https://github.com/AndrewwAM/vibe-wise-t3-codex/actions/workflows/ci.yml/badge.svg)](https://github.com/AndrewwAM/vibe-wise-t3-codex/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Experimental alpha](https://img.shields.io/badge/status-experimental%20alpha-orange.svg)](CHANGELOG.md)

[Español](README.es.md)

Learn to design software while Codex implements the scope you agree on.
This independent adaptation of [VibeWise](https://github.com/nykooi1/vibe-wise)
by **Noah Kim (@nykooi1)** targets Codex and T3 Code.

**Experimental alpha — `0.1.0-alpha.1`.** Local helpers and native skill/hook
discovery are tested. Full T3 conversations, educational quality, and restoration
after an actual resume or compaction still need end-to-end validation. Try a
disposable project first. This is not an official OpenAI or T3 product.

## Features

- `$vibe-wise-learn`: onboarding, learner-led design, explanations, and implementation checkpoints.
- `$vibe-wise-reset`: preview and confirmed reset of learning notes, with a backup.
- A read-only SessionStart hook for active projects on `startup`, `resume`, `clear`, and `compact`.
- T3 Code Plan/Default instructions that respect the active mode and available tools.
- A preview-first installer that preserves existing hooks and refuses to overwrite different skills.

You can ask for hints, skip a decision, pause, or explicitly request direct implementation.
Existing authorization is respected without redundant confirmations. These are model
instructions, not a security boundary or a guarantee of checkpoint compliance.

## Requirements

- Python **3.8+**, available as `python3`; helpers use only the standard library.
- Codex with native skills/hooks. Discovery checked with **0.159.3** during
  development and **0.162.0** for this alpha.
- T3 is optional: integration source inspected at **v0.0.44**. Use the same Codex
  profile as the CLI. Full conversational testing remains pending.
- Linux/macOS-style shell environment. Linux is tested; macOS, Windows, and WSL are unverified.

These are verified baselines, not the oldest compatible versions. See
[compatibility and limitations](docs/compatibility.md).

## Install

Review the code before running it:

```sh
git clone https://github.com/AndrewwAM/vibe-wise-t3-codex.git
cd vibe-wise-t3-codex
git checkout v0.1.0-alpha.1
python3 -B scripts/install.py
python3 -B scripts/install.py --apply
```

The first command is read-only. `--apply` installs both skills under `~/.codex/skills`
or the existing `CODEX_HOME`, and merges the hook into `hooks.json`. Existing hook
configuration is backed up before modification. Repeating the same installation
adds no duplicates. Select another profile with `--codex-dir /absolute/path/to/codex-profile`.

**Review the hook:** open `codex`, run `/hooks`, inspect “Restoring VibeWise learning
context”, and trust it if you accept its behavior. Enabled but untrusted hooks are
skipped. Installation does not bypass review or change authentication, sandbox,
model, or other settings. See [official hook documentation](https://learn.chatgpt.com/docs/hooks).

Skills are discovered on a subsequent turn. If T3's selector is stale, start a new
conversation or refresh its provider. Confirm that T3 uses the same Codex profile.

## Use

Inside a project:

```text
$vibe-wise-learn I want to build a command-line tool for organizing my notes.
```

Codex asks for your approach, explains unfamiliar concepts, discusses tradeoffs,
and implements the scope you authorize. Say “pause learning mode” to pause.
Invoking Learn again resumes existing notes without resetting them.

State lives in `.vibe-wise/profile.md`, `progress.md`, and `project-map.md`.
Legacy `.sensible-vibes/` is supported in place. The hook does not activate new
projects, write notes, or copy notes into its output; it points Codex to the files.
Lookup stops at Git/worktree boundaries and rejects linked state paths.

`$vibe-wise-reset` previews the selected state and files. After confirmation of
that snapshot, it backs up notes and restarts onboarding. Application code and
Git history are preserved. Backups remain in the local state directory.

In T3 **Plan**, inspect and discuss without writing code or notes. Switch to
**Default** to persist state or implement the agreed step. The skill does not
change T3's mode for you.

## Privacy

The Python helpers make no network requests and collect no telemetry. Codex reads
notes as model context, so notes and paths can reach your configured model provider.
Local notes do not imply offline inference. Keep credentials, private URLs,
customer data, and conversation transcripts out of them.

Ignore `.vibe-wise/` and `.sensible-vibes/` in **every learning project's** `.gitignore`
before publishing it. Installation does not edit other projects' ignore rules.
See [security and data handling](SECURITY.md).

## Validation

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_release.py
python3 -B scripts/smoke_app_server.py
```

The release check inspects Git-tracked files; stage intended files first. The native
smoke requires `codex` and queries discovery in an isolated temporary project. It
starts no model turn, persists no trust, and does not exercise a real conversational
lifecycle. Unit tests execute the hook directly with synthetic events.

CI runs tests, package/privacy checks, Gitleaks, and native Codex discovery. See
[test results and the manual checklist](docs/testing.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Updates, removal, and packaging

This alpha has no automatic upgrade/uninstall command. Different installed skills
cause the installer to stop. Compare and back up existing skill folders before
replacing them; do not delete a different adaptation.

To remove this adaptation, inspect and remove **only** its SessionStart registration
from your Codex profile's `hooks.json`, then remove its two skill folders after
backing up edits. Preserve unrelated hooks, configuration, and project notes.
Use `/hooks` to disable restoration without uninstalling.

Root `plugin.json` and `hooks/hooks.json` also support portable local packaging.
Marketplace installation is **not validated**; the standalone installer is the
tested alpha path. Use one method to avoid duplicate hooks. This GitHub release
is not a submission to OpenAI's public plugin directory.

## Credits and license

The learning workflow, checkpoints, and Markdown state originate in **VibeWise
by Noah Kim**. Base: upstream **0.1.43**, commit
[`c5fc8d813ce6789ebaf631ff4dd2a69658da3f31`](https://github.com/nykooi1/vibe-wise/tree/c5fc8d813ce6789ebaf631ff4dd2a69658da3f31).
The original **MIT license and copyright notice are preserved** in the root and
each installed skill. See [LICENSE](LICENSE) and [ATTRIBUTION.md](ATTRIBUTION.md).

Other public adaptations include [djolex999/vibe-wise-codex](https://github.com/djolex999/vibe-wise-codex)
and [yava-code/vibe-wise-mcp](https://github.com/yava-code/vibe-wise-mcp).
This project derives from the original, not those ports, and does not claim to
be the first Codex port or endorsed by their authors.
