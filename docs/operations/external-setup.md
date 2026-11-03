# External setup and capability boundaries

Repository code implements validation, static rendering, tests, workflow definitions, policies, and templates. Definitions alone do not establish successful GitHub execution or publication.

An authorized maintainer must verify:
1. The repository has a default `main` branch and bootstrap changes are pushed through the available review process.
2. Actions are enabled; PR CI runs and its actual check name is required by a branch ruleset.
3. `main` requires PRs, appropriate independent native review, dismissal of stale approvals, and no author bypass. Do not claim these rules exist without reading repository configuration.
4. Pages uses GitHub Actions, the `github-pages` environment permits only the default branch, and a deployment succeeds. See publishing instructions.
5. Labels listed in collaboration guidance exist and issue assignment/review permissions work.
6. Provider apps/runners are independently installed, authorized with least privilege, and tested before scheduling work. No API key is needed for local validation/rendering.

Claude Code, Codex, and Muse can read the repository when invoked with access. `CLAUDE.md` is a compatibility pointer. Muse's instruction discovery, execution behavior, and GitHub event support remain unverified; test a harmless read-only session and confirm it reads AGENTS.md before relying on it. The founder's reported Muse access does not prove automation.

There is no built-in cross-provider scheduler or event-driven reviewer. Use the manual independent-review path until an external integration is installed and tested. Do not emulate approvals or add fake successful checks. Keep API failures, read access, push access, admin access, and native review permissions distinct. Never request credentials in chat; use supported secure settings when truly required.

## Bootstrap observations (2026-11-02)

The platform HTTPS Git read operation succeeded but returned no remote refs: the repository initially had no commits or `main` branch. GitHub repository and Pages API inspection through `gh` returned Forbidden. Therefore Pages activation, rulesets, review permissions, and PR creation could not be established through that API. Read-only Git success does not prove push or administrative access. Local tests and browser checks are recorded in the bootstrap handoff; successful local rendering does not prove a live deployment.

Subsequent verification: Git push succeeded for `bootstrap/research-lab`. PR creation reached GitHub GraphQL but failed because `main` is absent ("Base ref must be a branch"). The remote now advertises the bootstrap branch as HEAD. Do not infer that the earlier REST API denial applies to every GitHub operation. Initial bootstrap review must be completed before a maintainer establishes the reviewed code as `main`; no merge or default-branch publication was performed by the bootstrap agent. Later contributions can use normal PRs against that established branch.

## Audit update (2026-11-02) — supersedes the bootstrap observations above

Verified by the independent audit in
[operations/reviews/architecture-audit-2026-11-02.md](../../operations/reviews/architecture-audit-2026-11-02.md);
the dated observations above are preserved as history and no longer describe
current state:

- `main` exists (bootstrap commits `226011f`, `e0a57e0`, pushed directly
  because no base branch existed at the time). GitHub Pages is **live**:
  `https://samyak-here.github.io/startup-ideas/` returns HTTP 200 and the CI
  and Pages workflows both succeeded on `main`.
- The Pages workflow was publishing the synthetic demo to the production
  site (audit P0-1); the fix is in the audit PR and needs a post-merge check
  that `/demo/` returns 404.
- Still outstanding: the documented queue labels do **not** exist (the repo
  has only GitHub's default labels), and branch protection / required
  independent native review could not be verified through the available API
  (the rulesets endpoint lists none). Treat both as unconfigured until a
  maintainer confirms them in repository settings.
- Audit issue #1 was the repository's first issue; no pull request existed
  before the audit PR.
