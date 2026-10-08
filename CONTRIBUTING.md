# Contributing

Keep changes focused. Preserve Noah Kim's credit, MIT notices, learner-led design,
existing authorization, and local-state boundaries. Avoid redundant implementation
gates and hard-coded host tool names. Helpers target Python 3.8+ standard library.

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/smoke_app_server.py
git add <intended-files>
python3 -B scripts/check_release.py
git diff --cached --check
```

The native smoke requires Codex but no credentials or inference. It does not
grant hook trust. CI also scans full Git history with Gitleaks. Test observable
behavior/failure paths rather than Markdown wording.

Use synthetic data in disposable projects for [behavioral tests](docs/testing.md).
Record host versions, mode, installation method, trust status, and actual results.
A successful conversation is not a guarantee of future model compliance.

Never commit learning notes, profiles, auth files, environment files, private keys,
transcripts, or diagnostic dumps. Remove secrets, personal paths, private repo
names, and customer data before filing an issue/PR. See [SECURITY.md](SECURITY.md).
