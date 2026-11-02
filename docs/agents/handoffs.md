# Handoffs and recovery

Before an incomplete session ends, save a compact handoff using `templates/handoff.md` in `operations/handoffs/` with a unique date/execution filename. Include objective, issue/PR/branch/head, completed work, relevant findings and source IDs, unanswered questions, blockers, exact next commands/actions, ownership/checkpoint, and validation status.

Do not dump conversation transcripts or secrets. Canonical findings belong in records; handoffs link to them. Save useful partial findings with explicit uncertainty even when investigation is interrupted.

To resume, inspect the current default branch, open PRs, issue ownership, and newer handoffs first. Compare referenced commit with current work. Reconcile intervening changes, renew a claim through the documented protocol, and validate after rebasing. Close the old handoff with a link to the successor or completion rather than deleting historical context.
