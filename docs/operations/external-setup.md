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
