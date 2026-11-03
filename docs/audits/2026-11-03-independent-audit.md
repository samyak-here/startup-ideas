# Independent architecture audit — 2026-11-03

Auditor: Claude Code cloud session (`claude/architecture-audit-review-ej4kpp`), reviewing the Codex bootstrap at `e0a57e0`. This is an audit by a distinct provider execution, **not** a GitHub native approval, and the auditor does not approve its own corrective PR.

## Executive summary
The bootstrap is a small, honest, stdlib-only system: JSON records, a fail-closed schema subset validator, a deterministic static renderer, and clear policy docs. Core mechanics work (verified below). The weaknesses were (a) semantic validation that let *structurally valid but evidentially empty* records through, (b) a homepage whose size grew with total record content, (c) production Pages builds that included synthetic demo content, and (d) review independence being policy-only with no stated native enforcement recipe. (a)–(c) are fixed in this PR; (d) cannot be fixed in code and is listed under external setup. **The repository is ready for a first real research cycle once the external settings below are applied and this PR is independently reviewed and merged.** No real research was started.

## Verified working (executed)
- `python3 scripts/lab.py validate|build|check`, `python3 -m unittest discover -s tests` (26 → 34 tests), Python 3.13; no dependencies.
- Demo build renders 5 pages + homepage; opened in headless Chromium served under `/startup-ideas/` subpath: no 4xx, no console errors, search and filters work, no horizontal overflow at 390px; skip link, labels, `aria-live` result count present.
- Rendering escapes HTML; unsafe URL schemes rejected; stale/private pages removed on rebuild; demo content isolated to `demo/`.
- Probes that correctly **rejected**: unknown refs, wrong-type refs, public→private refs, prod→demo refs, observed/reported claim without source, bad dates, status/history mismatch.

## Requirements coverage
| Requirement | Status |
|---|---|
| Agent onboarding / provider neutrality (AGENTS.md, CLAUDE.md pointer) | Verified (docs read; links tested). Muse discovery **unverified/external** |
| Structured problem/source/investigation/opportunity/decision records, cross-refs | Verified |
| Duplicate prevention | Was missing (only ID dupes) → source-URL duplicate check added; problem-level dedup remains agent/review duty (P2) |
| Evidence/fact/hypothesis separation, counterevidence | Verified structurally; enforcement strengthened (estimates, completed investigations) |
| History incl. rejected work | Verified (history + statuses) |
| Async coordination via Issues, claims, handoffs | Policy only; labels/Issues need external setup |
| Independent review, SHA-bound | Policy only; **not enforceable in repo** → external |
| HTML library, subpath-safe, accessible, responsive | Verified locally; live deployment **unverified** |
| Pages deploy after merge | Implemented, **unverified** (needs Pages source = Actions) |
| Research→execution boundary | Policy (docs/operations/boundaries.md); consistent |

## Findings
**P1-1 Evidentially empty records validated.** `scripts/lab.py` accepted a `completed` investigation with no findings/sources, a `promising` opportunity with no problem, `estimate` claims with no source, and source dates in impossible order (reproduced). Impact: methodology.md's "completed investigation must cite sources" was unenforced. *Fixed* (`ADVANCED` statuses rule, estimate sourcing, date ordering).
**P1-2 No duplicate detection beyond ID.** Same URL could be recorded as many sources, splitting evidence streams. *Fixed* for sources (normalized URL).
**P1-3 Homepage O(total content).** `render.py` embedded each record's full JSON in a `data-search` attribute: 3,000 modest records → 8.2 MB `index.html`. *Fixed*: lazily fetched `search-index.json`, card-text fallback when it cannot load. Cards still all render (pagination is P3).
**P1-4 Production Pages build published demo content.** `pages.yml` ran `check --demo`, so the founder-facing site linked to fictional data. *Fixed*: Pages runs `check`; CI exercises both.
**P1-5 Independent review not enforceable in repo.** `review.md`/`operations/reviews/*.md` are self-attested prose; nothing binds them to a head SHA. This repo cannot fix that in code without fabricating assurance; use native rules (below). Unresolved/external.
**P2-1** No record-type filter ("categories") on the homepage → *fixed* (type filter added). Industry/stage filters remain; no per-category pages (P3).
**P2-2** Single shared status enum for all record types (e.g. a source can be "promising"). Left as is; changing schemas churns templates. Revisit before records accumulate.
**P2-3** Actions pinned to tags, not SHAs; CI ran on every push and PR (duplicate runs) → push now limited to `main`. SHA pinning left (needs network lookup).
**P2-4** `knowledge/` has no per-type directories or filename/ID check; `load_records` globs every `*.json`. Low risk now; add a layout check when first records land.
**P2-5** `lab.py` is written in dense one-line style; readable enough, covered by tests, not rewritten.
**P3** External link checking is manual by design; report pages repeat content in "Record detail"; no dark mode; no Issue/label bootstrap script.

## Security
Workflow permissions are least-privilege (`contents: read`; deploy-only `pages`/`id-token`). Output escaping and URL checks verified by tests. Secrets/private-data detection is human review only; nothing scans for them (consider GitHub secret scanning — external).

## External setup required (not verifiable here)
1. Ruleset on `main`: require PR, ≥1 approval, **"require approval of the most recent reviewable push"** (blocks the last pusher from approving), dismiss stale approvals, require the `validate` check, no bypass for agents. A single GitHub account shared by all agents cannot produce an independent native approval; the founder (or a second identity) must approve.
2. Pages source = GitHub Actions; `github-pages` environment limited to `main`; verify first deployment by HTTP fetch.
3. Create labels listed in collaboration.md; enable Issues.
4. Optionally CODEOWNERS for `.github/`, `scripts/`, `schemas/`, `docs/` so agents cannot weaken protections without founder review.
5. Muse / other providers: test read-only AGENTS.md discovery before use.
6. Enable secret scanning/push protection.

## Unresolved after this PR
P1-5 (external), problem-level duplicate detection, status-enum specialization, SHA pinning, pagination, live Pages verification.
