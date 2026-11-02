# Canonical records and lifecycle

Use the checked-in schemas and templates as the executable field contract. Store one JSON object per file within its entity directory. Generate a stable, collision-resistant identifier once; never recycle it or use a mutable title as identity. IDs survive rename, archive, rejection, and reopening. Search existing records before allocating a new ID.

Problems describe customers, tasks, context, consequences, geography, alternatives, supporting and contradictory evidence, uncertainty, relationships, questions, and recommended next actions. Sources preserve provenance and limitations. Investigations connect objectives and questions to findings, counterfindings, conclusions, and source IDs. Opportunities connect proposed solutions and customer/value/revenue/distribution/differentiation hypotheses to problems and risks. Decisions retain rationale, evidence, alternatives, actor, date, and revisit conditions.

Use explicit unknown values permitted by the schema; absence of evidence must not become invented detail. Every record carries creation/update timestamps and provenance. A substantive update preserves history with date, reason, and what changed. Source changes should explain how conclusions change.

Lifecycle meanings:
- Discovered: a signal, not a proven recurring problem.
- Initial evidence collected: enough evidence to articulate the issue.
- Investigating: an active question with an owner/issue.
- Promising: reasoned priority for further work, not validation.
- Needs validation: research cannot resolve an important real-world uncertainty.
- Paused: blocked or deprioritized, with a revisit condition.
- Rejected: current evidence argues against pursuit; retain rationale.
- Archived: retained for history and discovery.

Use the exact serialized states allowed by the schema. Every transition needs a timestamp and rationale. Reopening records preserves past rejection or pause decisions. Link duplicates explicitly and select one canonical record; do not silently delete their evidence. Keep related problem and opportunity references explicit and valid.
