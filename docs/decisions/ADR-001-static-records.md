# ADR-001: File-based records and static publishing

Date: 2026-11-02. Status: accepted for bootstrap. Decision-maker: bootstrap implementation, subject to independent review.

Use structured JSON records, Python validation and rendering, Git history, GitHub Issues/PRs, and GitHub Pages. This keeps operation portable across agent providers and avoids a database, frontend framework, or proprietary orchestration dependency.

Alternatives: Markdown-only records are approachable but weaker for reference checks; a database supports richer queries but adds service operation; a dynamic frontend adds dependencies without an initial need. Evidence considered: an initially empty repository and the founder's requirements for durable knowledge, static reports, and minimal infrastructure. No research findings informed this technical decision.

Revisit when measured collection scale exceeds practical build/search limits, record relationships require complex queries, or authenticated/private reports become necessary. Record migration and URL preservation plans before changing the design.
