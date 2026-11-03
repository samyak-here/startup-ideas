# Independent architecture audit — bootstrap scaffolding

Reviewer execution: Muse (Biscuit), a distinct agent execution from the Codex
bootstrap author. Date: 2026-11-02. Issue:
[#1](https://github.com/samyak-here/startup-ideas/issues/1). Branch:
`review/issue-1-architecture-audit`.

Scope: the complete repository at `main` head
`e0a57e0fd2fe6c26383806698051a8015972d810` (2 commits: `226011f`, `e0a57e0`) —
instructions, docs, schemas, templates, examples, `scripts/lab.py`,
`scripts/render.py`, tests, assets, both GitHub Actions workflows, issue/PR
templates — plus live GitHub state (issues, PRs, labels, rulesets, Actions
runs) and the live Pages site. No startup research was performed.

Method: read everything, then *ran* everything — full test suite, all three
CLI commands, production and demo builds — and probed the validator with
malformed, misplaced, duplicated, self-referencing, placeholder, and
secret-bearing records. Generated HTML was inspected in headless Chromium at
desktop and 390px widths. Findings below cite the probe that proved them;
claims I could not verify are marked unverified, not assumed.

This is not a native GitHub approval and does not approve the accompanying
pull request. The PR from this branch requires a different execution's review
of its current head, per `docs/agents/review.md`.

## Executive summary

The bootstrap is unusually honest and mostly sound: a dependency-free
validator with real integrity tests, deterministic escaped rendering,
relative links that work under the Pages subpath, least-privilege workflow
permissions, and documentation that repeatedly states what the system does
*not* do. Those claims largely survived verification.

One critical defect does not: **the Pages workflow publishes the synthetic
demo to the production website** (P0-1, live-verified). Around it sits a
cluster of validator gaps that let placeholder, duplicate, misplaced, or
evidence-free "completed" research pass CI (P1), and onboarding documents
whose bootstrap-era status is now factually wrong (P1-8). All P0/P1 findings
except semantic duplication and the lifecycle-enum question are fixed in the
accompanying PR with regression tests. The repository is **not ready for its
first real research cycle until the P0 fix is merged and live-verified, and
the founder configures branch protection and labels** (see External setup).

## Requirements coverage matrix

Status key: **Verified** = exercised and works · **Partial** = implemented
with material gaps · **Policy only** = documented, not enforceable in-repo ·
**Missing** · **External** = requires configuration outside the repository.

| Requirement | Status | Evidence |
|---|---|---|
| Problem-first, broad, US-focused mission | Verified (docs) | `AGENTS.md`, `docs/research/methodology.md`; first-session brief is bounded and fabrication-averse |
| New agent onboards with no prior context | Partial | `AGENTS.md` + docs index are concise and consistent, but status sections are stale (P1-8, fixed by supersession notes) |
| Provider independence (Claude Code / Codex / Muse / Muse) | Partial | `AGENTS.md` canonical, `CLAUDE.md` is a pointer; no `.github/copilot-instructions.md`; Copilot behaviour unverified (`docs/operations/external-setup.md` says so honestly) |
| GitHub Issues coordinate work | Partial | 8 issue templates + claim protocol exist; **no issues have ever been filed**, documented queue labels do not exist on the repo (API-verified: only GitHub defaults), templates cannot apply labels |
| Branches/PRs isolate contributions | Policy only | Branch naming + PR template documented; bootstrap itself landed directly on `main` with no PR (API-verified: 0 PRs) because no `main` existed at the time |
| Independent review before merge | Policy only | `docs/agents/review.md` is rigorous; nothing in-repo enforces it. Bootstrap review (`operations/reviews/bootstrap.md`) is a pre-commit attestation with no SHA. Branch protection unverifiable via public API; rulesets endpoint returns none |
| Interrupted sessions leave handoffs | Partial | Template + procedure + bootstrap handoff exist; bootstrap handoff content is stale (P1-8) |
| Reuse over duplication | Partial | ID uniqueness enforced; content duplication is not detected (P1-4) |
| Evidence-driven, facts vs hypotheses separated | Verified (structure) | Claim classifications in schemas; validator requires sources for `observed`/`reported` claims (tested) |
| Structured records, cross-references | Verified with gaps | Typed reference checking works (tested); placement, self-reference, reciprocity gaps (P2-3, P2-7 fixed; P2-8 open) |
| Contradictory evidence preserved | Verified (structure) | Dedicated fields on problems/investigations; no probe found a path that drops them |
| Complete history incl. rejected work | Verified (structure) | Append-only `history` with status-consistency check; lifecycle enum inconsistency remains (P2-4) |
| No fabricated sources/data | Partial | Nothing can prove truth (docs say so); placeholder records and evidence-free completion passed validation (P1-1, P1-3, fixed) |
| Polished Pages library homepage | Verified | Local build + live site inspected in Chromium; polished, responsive, labelled demo banner |
| Standalone HTML reports | Partial | Reports render and are readable, but one problem-centric template serves all types: a source report shows 12 sections, 12 of them "Unknown" (P2-1, improved) |
| Browseable categories, search/filtering | Partial | Text + industry + status work; no record-type filter (P2-2, fixed); search payload embeds whole records (P2-5, improved) |
| Clickable citations | Verified | Source IDs render as links to source reports; external URLs render as safe links in record detail |
| Provenance and dates on reports | Verified | Created/updated/status/provenance/history rendered on every report |
| Responsive, accessible layout | Verified with defect | Skip link, labels, focus styles, `[hidden]` rule all present; long titles can overflow on mobile (P2-10, fixed) |
| Works under `/startup-ideas/` subpath | Verified | All links relative; `check_site` resolves them; live site confirms |
| Reports generated reproducibly from canonical data | Verified | Deterministic-build test passes; build is byte-stable across input order |
| Deployment after merges to `main` | Verified — and see P0-1 | Pages run succeeded on `main`; the same workflow ships the demo |
| Research/execution boundary (no spending/outreach/launch) | Verified (docs) | `docs/operations/boundaries.md`, `AGENTS.md`; nothing in code can or does act externally |
| Secrets not published | Partial → improved | Escaping is solid; no credential guard existed and the repo is **public**, so `publish: false` is not privacy (P1-7, guard added) |
| Scales to thousands of findings | Unverified / at risk | One-file-per-record scales in git; homepage search is a full-DOM scan over embedded JSON (P2-5). No benchmark exists, as `docs/architecture/overview.md` concedes |

## Verified functionality (commands actually run)

Environment: Python 3.12.3, repository root, head `e0a57e0`.

- `python3 scripts/lab.py validate` → exit 0, "0 research and 0 synthetic records".
- `python3 -m unittest discover -s tests` → **26 tests, OK** (integrity,
  publication, documentation links).
- `python3 scripts/lab.py check` → exit 0; `check --demo` → exit 0, 5 synthetic records.
- Live site: `https://samyak-here.github.io/startup-ideas/` → HTTP 200,
  matches a local production build; Actions API shows `Validate research`
  and `Publish research library` both **succeeded** on `main` (2026-11-02T23:58Z).
- Headless Chromium: demo homepage at 1280px is polished with no layout
  breakage; a 390px report page has no page-level horizontal scroll from the
  layout grid (long unbroken titles excepted, P2-10).
- Escaping/URL safety: existing tests inject `<img onerror>` and
  `javascript:` URLs; both are neutralised. Independently re-confirmed by the
  test run above.
- Demo separation **in the local CLI** works and is tested: a plain `check`
  after `check --demo` removes the marked demo output and refuses to delete
  unmarked output. The failure is only in what the Pages workflow uploads.

## Findings

### P0 — Critical

**P0-1. The Pages workflow deploys the synthetic demo as part of the
production site.** `.github/workflows/pages.yml` runs
`python3 scripts/lab.py check --demo` — which builds `site/` *including*
`site/demo/` and injects a demo link into the production homepage — and then
uploads the whole `site/` directory as the Pages artifact. Live-verified
2026-11-02: `https://samyak-here.github.io/startup-ideas/demo/` and
`/demo/reports/problem-demo.html` return HTTP 200, and the production
homepage contains "Explore the synthetic demonstration". This breaks the
repository's own rule (`docs/operations/publishing.md`: the production build
must not count synthetic fixtures; README: demonstration content is
"separate from the production library"). The demo is labelled synthetic, so
this is not deception — it is a failed separation guarantee on the founder's
public library, one stale-link or screenshot away from fictional "findings"
being quoted as research. **Fixed in this PR:** the workflow validates with
`--demo` into a throwaway directory, builds the artifact with a separate
production-only `check`, and fails if `site/demo` exists; a workflow
regression test guards the invariant.

### P1 — Major

**P1-1. A template copied verbatim passes validation as real research.**
Probe: appending `templates/problem.json` unchanged to a valid record set
validates cleanly — ID `problem-replace-me`, title "Replace with descriptive
title", provenance `replace-me`/`replace-me`. `scripts/lab.py: validate()`
has no placeholder guard, contradicting `knowledge/README.md`'s
collision-resistant-ID guidance. **Fixed:** validator rejects placeholder
IDs, titles, and provenance; tests assert templates are structurally valid
but semantically rejected as records.

**P1-2. ID rules permit trivially collid
...[truncated 9492 chars]