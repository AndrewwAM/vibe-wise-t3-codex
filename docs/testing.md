# Alpha validation record

## Automated coverage

Tests use synthetic data in temporary directories. Coverage includes new/paused
projects, restoration JSON, large notes and pending decisions, legacy state,
Git/worktree boundaries, symlinks, malformed events, reset previews, changed
confirmation snapshots, backups, and installer rollback/idempotence.

The native smoke starts Codex app-server and queries `skills/list` and `hooks/list`
in an isolated project. It starts no model turn, needs no API credentials, executes
no hook through a conversation, and changes no persisted trust. `--installed`
inspects the user's installation read-only; untrusted is not execution success.

CI runs unit tests on Python 3.8/3.12/3.13, Git-tracked release/privacy checks,
full-history Gitleaks, and native discovery with pinned Codex CLI 0.162.0.

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/check_release.py
python3 -B scripts/smoke_app_server.py
```

## Recorded results

- Development: 45 tests passed; native discovery passed with Codex 0.159.3.
- Release preparation (2026-10-08): **51 tests passed**, both skills validated,
  portable manifest schema validated, and the 33 Git-tracked package files passed
  the release/privacy check.
- Gitleaks 8.30.1 found no secrets in the working directory or Git history.
- A clean exported source archive installed into a fresh temporary Codex profile;
  preview wrote nothing, reinstall was idempotent, and installed MIT notices matched.
- Native discovery passed with Codex 0.162.0. The fixture hook was loaded but
  untrusted; no automatic lifecycle execution is claimed.
- Hosted results are linked from the `v0.1.0-alpha.1` release notes and CI run.
- Release host versions: Codex 0.162.0, T3 v0.0.44, Python 3.13.11.
- T3 source integration inspected; no complete conversational pass is claimed.

## Manual end-to-end checklist — pending

Use a disposable repo and synthetic notes. Record versions, mode, trust, and actual
results in Codex and T3. The following checks remain pending:

1. Install into a clean profile; check skill visibility, untrusted-hook skipping,
   and review/trust only VibeWise through `/hooks`.
2. Invoke Learn, answer onboarding, propose a design. Confirm design without
   authorizing implementation; check that application code remains unchanged.
3. Authorize the described implementation; check scope, accurate reporting,
   and evidence-based notes.
4. Request direct implementation and skip a decision; check for no redundant gate.
5. Leave a pending checkpoint and restart/resume; check its stage, no repeated
   onboarding, and no application changes before authorization.
6. Compact and repeat the checkpoint check; record actual hook delivery.
7. Pause/restart; check inactive restoration. Explicitly invoke Learn to resume.
8. In T3 Plan, discuss/onboard with no code/notes written. Switch to Default;
   check accurate persisted state and authorized implementation.
9. Preview/cancel Reset; check unchanged files. Confirm a new preview; inspect
   backups/onboarding and preserved application code/Git.
10. Use nested paths/worktrees; check repo boundaries and rejected linked notes.

A single successful conversation does not guarantee future model compliance.
