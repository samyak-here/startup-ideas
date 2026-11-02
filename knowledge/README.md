# Canonical research

No real research has been conducted during bootstrap. Add one JSON record per file
under a type directory (for example `knowledge/problems/problem-<uuid>.json`). IDs
are immutable and must begin with their singular type: `problem-`, `source-`,
`investigation-`, `opportunity-`, or `decision-`. Generate UUID suffixes for parallel
work; filenames are not identity. Use the corresponding template and schema.

Production records must set `demo: false`. `publish: false` is the default;
review content for public release before setting it true. Never commit private
information even in unpublished records. Synthetic fixtures belong in `examples/`
and are emitted only with `--demo`, under the separate `demo/` library.

JSON null means unknown. Empty lists mean nothing documented yet, not proof of
absence. Claims carry an explicit classification and source IDs. Observed and
reported claims require references. Automated checks cannot prove source truth
or detect every secret; independent review remains mandatory.
