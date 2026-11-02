# Independent peer review

The author must not approve its own research. A reviewer is a distinct agent execution that did not author the changes. Prefer a separate authorized GitHub identity where native review approval is required. Two executions under one account may provide useful review but do not constitute two independent GitHub approvals.

Manual path: open the PR, request another authorized reviewer or launch a separate reviewing session, supply the issue and exact head SHA, and ask it to inspect canonical records and generated reports. The reviewer must not edit the contribution while acting as its independent approver; proposed corrections return to the author. Review must identify concrete checks and findings, not rubber-stamp.

Checklist: source authenticity; claim/source alignment; unsupported assumptions; counterevidence; duplicate research; schema and cross-reference validity; HTML rendering and readability; safe publication; proportionate conclusions. Verify source samples directly when access allows, and disclose unverified claims and inaccessible links.

Record reviewer identity, execution ID, exact commit SHA, result, checks run, limitations, findings, and resolution evidence using the review template. A repository attestation or review comment is not a native GitHub approval. Do not invent an execution identifier or imply unavailable integration.

Merge requires passing CI, completed independent review of the current head, resolved findings, satisfied repository protection rules, and no sensitive/prohibited content. New commits invalidate the prior head attestation until reassessed. Configure protected branches to require checks and native reviews when available; dismiss stale approvals. Without configured protections, this remains an explicit operational policy, not an automated security guarantee. If no reviewer is available, leave the PR pending. Never weaken protections to merge.
