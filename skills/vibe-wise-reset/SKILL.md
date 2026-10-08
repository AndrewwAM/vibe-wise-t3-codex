---
name: vibe-wise-reset
description: Back up this project's VibeWise learning notes and restart onboarding after explicit confirmation. Application code and Git history are preserved.
---

# Reset VibeWise learning

Use only when explicitly invoked. Reset the profile, progress, pending learning
decisions, and project map after showing the exact target and obtaining consent.
Respond in the user's language. Resolve the helper relative to this SKILL.md.

1. Preview the current project without changing notes:

   ```sh
   python3 "<this skill directory>/scripts/reset.py" --cwd "<absolute project cwd>"
   ```

   For `no_notes`, explain that there is nothing to reset and point to
   `$vibe-wise-learn`. On an error, stop and explain the error.

2. Show the absolute project and state paths, the files being reset, and the
   backup location. Ask in chat whether to reset that project's learning notes.
   Wait for an explicit answer after presenting this preview. Invocation alone,
   silence, or permission to use tools does not confirm this snapshot.

3. After confirmation, run the helper with the original cwd and preview token:

   ```sh
   python3 "<this skill directory>/scripts/reset.py" --cwd "<original cwd>" --confirm "<confirmation token>"
   ```

   In Plan mode, defer this write until T3 Code is switched to Default. If the
   notes changed, preview again and get confirmation for the new snapshot.
   Do not improvise deletion commands or claim a failed reset succeeded.

4. On success, report the backup path and read the sibling
   `vibe-wise-learn/SKILL.md`. Resume onboarding with the incomplete new profile.
   Discard pre-reset preferences, mastery, pending decisions, and answers.
   Inspect actual code to rebuild the map; backups are historical data.

Install both VibeWise skills together; the helper shares the Learn skill's
project-boundary lookup. Notes remain in .vibe-wise/ or the existing legacy
.sensible-vibes/ directory. No application source or plugin files are reset.
