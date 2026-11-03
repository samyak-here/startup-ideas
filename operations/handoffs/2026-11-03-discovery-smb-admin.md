# Handoff: first bounded discovery (US small-business admin problems)

- Execution/agent: Claude Code cloud session (session_01LQxkVvFKqYivoTtCXoQ4cs)
- Timestamp (UTC): 2026-11-03
- Issue / PR / branch: https://github.com/samyak-here/startup-ideas/issues/3 / none yet / research/discovery-smb-admin-problems (base main ecba14a)
- Ownership and next checkpoint: claimed in issue #3, 24h lease; resume once primary-source hosts are reachable.
- Objective: see operations/backlog/first-session.md.
- Completed work and changed record IDs: none. **No records were written.**
- Blocker: WebFetch could not resolve `www.ama-assn.org` and `www.fedsmallbusiness.org` (outside the session's network allowlist). Only search-result summaries were available, which are secondary and were not verified against the primary documents, so nothing was recorded as evidence.
- Unverified leads (NOT findings; verify at the primary source before creating any source/problem record):
  1. Medical practices / prior authorization: AMA physician prior-authorization surveys (reported ~13-16 hours/week of physician and staff time; ~40 requests per physician per week; share of practices with dedicated PA staff). Years, sample sizes and wording differ across surveys; one aggregator's 2025 figures could not be traced to AMA.
  2. Cross-industry small-business payments: Federal Reserve Small Business Credit Survey, 2024 Report on Payments (fees top challenge; slow-paying customers and settlement delays reported). Need exact percentages, sample (reported as ~4,920 employer firms), fielding period.
  3. Tax-compliance time: NSBA surveys (2015, 2018; older) and an unverified claim attributed to SBA Office of Advocacy/IRS. Need primary IRS/SBA/NSBA documents; likely dated.
  4. Contractor permitting: no credible primary US source found; vendor blog figures attributed to NAHB are untraceable. Treat as unsupported until nahb.org/government data is read.
- Counterevidence still to seek: whether these burdens are concentrated in larger practices/firms, vendor-sponsored survey bias, existing automation products (competitors).
- Validation performed: none needed (no record changes).
- Exact next actions: (1) founder allows the hosts above (and likely nahb.org, sba.gov, irs.gov, ama-assn.org subdomains) in the environment's network settings; (2) fetch primary documents, create source records (accessed date, limitations) then problem records; (3) run validate/tests/build/check; (4) open PR and request independent review.
- Supersedes / superseded by: none
