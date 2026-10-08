# Compatibility and limitations

| Component | Baseline | Evidence |
| --- | --- | --- |
| Helpers | Python 3.8+ | Standard library only; CI matrix 3.8, 3.12, 3.13. |
| Local execution | Python 3.13.11, Linux | Unit suite and isolated installation. |
| Codex | 0.159.3, 0.162.0 | Native skill/hook discovery; no model turn. |
| T3 | v0.0.44 | Integration source inspection; conversational testing pending. |

These are verified baselines, not the oldest supported versions. macOS, Windows,
and WSL lack recorded execution tests. The shell hook requires `python3` on PATH.

## Trust and lifecycle

Review new/changed hooks through `/hooks` in Codex CLI. Enabled but untrusted hooks
are skipped. T3 must use the profile in which you installed and reviewed the hook.

Metadata smoke checks loading, not trust or lifecycle execution. Fixture declarations
load through temporary session flags without bypassing/persisting trust. Unit
tests execute the helper for `startup`, `resume`, `clear`, and `compact`; they do
not prove delivery to a model in an actual conversation.

## T3 modes

Plan retains onboarding/pending decisions in chat without code or note writes.
Default permits notes and authorized implementation. The skill changes neither
mode nor permissions. Question tools are used only within their runtime restrictions;
otherwise questions use chat.

## Distribution

The standalone installer is the tested alpha path. Root `plugin.json` follows
Agent Plugins and declares hooks under `extensions.com.openai`. Marketplace
installation is unvalidated. Combining installation methods may duplicate hooks.

This is a GitHub release. The [OpenAI packaging documentation](https://developers.openai.com/plugins/build/plugins)
states that plugins containing lifecycle hooks are not eligible for its public
plugin directory; this release does not claim directory availability.

Automatic upgrades/uninstall and wider platforms remain future work. Teaching
quality and checkpoint compliance depend on the model; see [testing.md](testing.md).
