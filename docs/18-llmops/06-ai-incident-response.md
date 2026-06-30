# AI Incident Response

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. What to do when your AI system has a quality incident — the taxonomy of AI failure types, rollback decision frameworks, root cause analysis for non-deterministic systems, and post-mortem formats that capture what actually went wrong.

!!! note "Template: Topic-Specific Structure"
    This chapter will be designed from scratch with sections that fit its specific topic rather than inheriting the generic system-architecture template or the decision-framework template. The outline above serves as the intended section plan. When writing the flagship version, use those outline points as top-level `## Section` headings and add subsections, diagrams, and worked examples inside each one — no generic Architecture / Components / Request Lifecycle / Scalability / Monitoring scaffolding unless those titles genuinely fit the content.

## What This Chapter Will Cover

- AI incident taxonomy: quality regression, prompt regression, distribution shift
- Rollback decisions: when to roll back a prompt vs model vs serving config
- Root cause analysis in non-deterministic systems: replay, bisection, anchoring
- Incident communication: AI quality issues vs outages to users
- AI-specific post-mortem: what information is actually useful

---

*Part of [LLMOps](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
