# Handoff: first bounded discovery (US small-business admin problems), PR #10

- Execution/agent: Claude Code cloud session (session_01LQxkVvFKqYivoTtCXoQ4cs)
- Timestamp (UTC): 2026-11-03
- Issue / PR / branch: https://github.com/samyak-here/startup-ideas/issues/3 / https://github.com/samyak-here/startup-ideas/pull/10 / research/discovery-smb-admin-problems
- Resolution of duplicate discovery work: three sessions covered the same brief (PRs #5, #9, #10). The founder chose PR #9 (issue #7) as canonical. This PR is stacked on #9's branch and no longer creates separate problem records: it adds two sources not in #9 and attaches their evidence to #9's two problem records.
- Added sources: AMA 2017 article on its prior-authorization survey (separate, earlier survey from the same advocacy organization); Federal Reserve Banks 2024 Report on Payments (independent corroboration of slow-paying customers, with different measures and magnitudes than #9's vendor source).
- Removed from this PR as duplicates: my AMA 2025 press-release source (same survey as #9's source-efe163a1) and my two problem records.
- Not recorded (no verified primary source): tax compliance (NSBA), contractor permitting (NAHB).
- Open: PR #5 (prior authorization, certified payroll, Medicare adjustments) still has a prior-authorization problem record overlapping #9 and needs the same reconciliation. This PR must merge after #9.
- Validation: `scripts/lab.py validate`, unit tests and production `check` pass locally.
- Reviewer focus: re-open the two added source URLs and confirm the two appended claims; confirm no AMA article from the same survey is treated as independent evidence.

## Integration correction
PR #10 was merged into the PR #9 branch while this integration session began. Its AMA2017 and Federal Reserve sources and evidence are preserved. The live canonical prior-authorization problem is now `problem-df174fd556554536` from #5, combining CMS non-drug rule context with explicitly broader AMA survey workload evidence. The former #9 problem `problem-ef2f4753-d46b-48cc-a5ef-28a973eca056` remains as an archived, linked duplicate so historical URLs and provenance survive; it must not be counted as a separate problem. The investigation now points to the canonical ID. Dedicated staff are labor allocation, not proof of willingness to buy relief. Existing Fed evidence provides partial directional corroboration, not reproduction of vendor percentages or dollar balances. No research execution or launch is authorized.
