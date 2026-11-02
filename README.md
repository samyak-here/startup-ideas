# Startup Research Lab

A persistent, provider-neutral research organization for finding real customer problems before proposing products. Canonical structured records become a static research library; GitHub Issues coordinate work and reviewed pull requests preserve findings.

**Start here:** agents read [AGENTS.md](AGENTS.md); contributors read [CONTRIBUTING.md](CONTRIBUTING.md); the [documentation index](docs/README.md) explains the system. No real startup research is included in bootstrap. Demonstration content is fictional and separate from the production library.

## Local workflow
Use Python 3.12 or newer. Run from the repository root:

```sh
python3 scripts/lab.py validate
python3 -m unittest discover -s tests
python3 scripts/lab.py build
python3 scripts/lab.py check
```

Use `python3 scripts/lab.py build --demo` to exercise the synthetic report pipeline. Generated HTML is disposable; JSON records are authoritative. See [publishing](docs/operations/publishing.md) for output, Pages configuration, and deployment limits.

The intended public library is `https://samyak-here.github.io/startup-ideas/` once GitHub Pages deployment succeeds. This URL is an expected destination, not a claim of a live deployment.

## What this system does
Validates records and references, generates escaped static HTML and navigable reports, tests the pipeline, and provides repository workflows for CI and Pages. It does not run autonomous agents, authenticate external providers, provide atomic task locks, prove source truth, or approve its own research. Those boundaries are explicit in [external setup](docs/operations/external-setup.md).

## First research session
After bootstrap review and environment configuration, follow [the first-task brief](operations/backlog/first-session.md). Bootstrap itself must not perform that investigation.
