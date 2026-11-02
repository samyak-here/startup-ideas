# Architecture

JSON files are the canonical knowledge store. Stable IDs identify entities independently of filenames and titles. Explicit source and record references support joins, duplicate detection, and future migration. Git preserves history; no database service is required. Separate records minimize merge contention and allow thousands of files without a shared progress ledger.

The validator enforces machine-checkable shape and reference integrity. Tests exercise invalid inputs and rendering. The static generator consumes records in stable order and emits reproducible HTML, a searchable library, and stable report paths. The generator must escape text and reject unsafe URL schemes. Human review evaluates truth, source independence, and sensitive content; schema validity cannot do that.

GitHub Issues are the primary work queue. PRs and independent review gate incorporation; Pages publishes generated output from the default branch. CI credentials use the least privilege required for each job. There is no installed agent runner or implicit continuous execution.

`knowledge/` stores source, problem, investigation, opportunity, and decision entities. `examples/` contains clearly synthetic inputs. `templates/` supports repeatable contributions, `operations/` preserves handoffs, and `docs/decisions/` preserves architecture rationale. Generated `site/` content is not canonical.

For large collections, benchmark build time and client-side search size before introducing pagination, segmented indexes, or a database. Preserve stable IDs and URLs through any migration. Add an architecture decision before changing canonical storage or review trust boundaries.
