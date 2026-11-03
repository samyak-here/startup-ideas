# Static HTML publishing

Canonical records are the source of truth. From the repository root run:

```sh
python3 scripts/lab.py validate
python3 -m unittest discover -s tests
python3 scripts/lab.py build
python3 scripts/lab.py check
```

The generator writes disposable `site/` HTML and assets. Use `build --demo` for explicitly synthetic demonstration content; the production build must not count synthetic fixtures as real findings. Inspect the homepage, report hierarchy, mobile layout, citations, uncertainty labels, source links, and revision provenance. Internal links and asset paths must work under `/startup-ideas/`, not just at a domain root.

Reviewed changes merged into `main` trigger validation, production generation (`check`, without demo content), artifact upload, and official GitHub Pages deployment. PR CI validates without publishing. Configure Settings → Pages → Build and deployment → Source: GitHub Actions. The deployment environment is `github-pages`; give deploy jobs `pages: write` and `id-token: write`, with repository reading limited to `contents: read`. Restrict deployment to the default branch and configure environment approvals if required by the founder.

Expected URL after successful deployment: `https://samyak-here.github.io/startup-ideas/`. Do not call it live until the deployment job succeeds and an HTTP request verifies its content. Diagnose failures from Actions logs, Pages source settings, environment branch rules, token permissions, artifact upload, and repository visibility/plan support. Never bypass protections to fix deployment.

Everything published through Pages must be treated as public. Human review checks private data, credentials, copyrighted material, and unsupported factual presentation. Automated escaping prevents markup injection but does not certify privacy or truth.

The homepage loads full-text search from `search-index.json` on first query (falls back to visible card text if unavailable). The index contains only published records.
