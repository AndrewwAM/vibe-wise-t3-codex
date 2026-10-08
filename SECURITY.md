# Security and data handling

This experimental alpha guides model behavior; checkpoints do not enforce a
sandbox, access policy, or permission boundary.

## Data flow

- Helpers run locally, make no network requests, and collect no telemetry.
- Notes and reset backups live in `.vibe-wise/` or legacy `.sensible-vibes/`.
- The hook checks pause state and returns file pointers, without copying note contents.
- Codex reads notes as context; contents and paths can reach the configured model
  provider, whose policies apply.
- Installation changes only skills and `hooks.json` in the selected Codex profile.
  It does not copy auth, approve hooks, or change sandbox/model settings.
  Local hook backups may contain private configuration and must stay private.

## Sharing projects and diagnostics

Keep credentials, personal/customer data, and private URLs out of learning notes.
Ignore both state directory names in each project's Git configuration. Ignore
rules do not remove previously committed files; review tracked files and history.

Never share full Codex config, auth files, hook backups, environment dumps, raw
app-server traffic, or transcripts. Smoke output is compact, but subprocess errors
can still contain local details. Review diagnostics before posting publicly.

CI runs Gitleaks and package/privacy checks. These reduce disclosure risk but do
not prove that every file is free of sensitive information; inspect staged files
and history too.

## Reporting vulnerabilities

Use GitHub **Security → Report a vulnerability** privately when available.
Do not post credentials or exploitable private details in public issues. If private
reporting is unavailable, open an issue requesting a private reporting channel,
with no sensitive details. Only the current alpha receives fixes.

If a credential was exposed, revoke/rotate it with its issuer before sharing a reproduction.
