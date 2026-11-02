# Asynchronous collaboration

GitHub Issues are the primary queue; local backlog files preserve actionable briefs when API access is unavailable. Prefer uncertainty reduction, promising extensions, new customer segments, connecting evidence, correction, and maintenance over report counts. Search open/closed issues, PRs, and records before creating a narrowly scoped task with objective and acceptance criteria.

## Claim protocol
Inspect assignees and recent comments. Assign yourself if authorized and post execution identity, branch, scope, claim timestamp, next checkpoint, and lease expiry (default 24 hours). Read back the issue before starting. Labels and comments are not atomic locks: if claims collide, pause overlapping work and agree on an owner or split scope. The earliest visible claim is a coordination convention, not a transactional guarantee.

Report progress at checkpoints and before interruption. Expired claims are candidates for recovery, not proof of abandonment: inspect PRs and handoffs, ask the prior owner through authorized GitHub coordination, and document reassignment. Do not erase ongoing work. If GitHub access is unavailable, record a local handoff and explicitly disclaim exclusive ownership.

## Branches and synchronization
Use `research/issue-N-topic`, `infra/issue-N-topic`, or `review/issue-N-topic`. In isolated cloud tasks use the existing checkout and a branch; do not create worktrees unless requested. Inspect cleanliness before switching branches. Fetch/sync the default branch when permitted; never overwrite another session's uncommitted work. Keep records independently editable. Resolve conflicts by reconciling evidence and preserving history, not by blindly choosing one side. Revalidate and request current-head review after rebasing or changes.

## Queue labels
Use `research:discovery`, `research:investigation`, `research:validation`, `research:maintenance`, `status:ready`, `status:claimed`, `status:blocked`, `priority:high`, and `agent:review-needed`. Templates do not create labels or grant permissions; an authorized maintainer configures them.

Open a PR with issue, changed IDs, evidence, uncertainty, report changes, validation, and follow-ups. Avoid speculative issue floods. An agent runs only when a user session, event, schedule, or supported runner invokes it. Merely opening the repository does not start continuous work.
