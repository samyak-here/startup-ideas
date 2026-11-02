# Canonical schemas

Each JSON Schema describes one record type. `scripts/lab.py` implements the small
subset of schema keywords used here using Python's standard library, and rejects
unknown keywords. Semantic validation additionally checks unique IDs, typed
references, synthetic/publication boundaries, citation presence, history dates,
and lifecycle consistency. JSON Schema files are usable with standard Draft
2020-12 validators; semantic rules still require the lab validator.

All dates use YYYY-MM-DD. Add history entries when status or conclusions change,
with reasons; keep old entries and use Git history for full record revisions.
Dates cannot precede creation or exceed the updated date. `completed` means the
investigation is documented, not that an opportunity has been validated.
