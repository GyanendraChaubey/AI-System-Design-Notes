# PII and Privacy Engineering in AI Systems

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. How to handle sensitive personal data in the AI request path — PII detection and redaction in prompts and context, logging and retention under compliance constraints, the GDPR right-to-delete problem for vector indexes and fine-tuned models, and data residency for multi-regional AI products.

!!! note "Template: Topic-Specific Structure"
    This chapter will be designed from scratch with sections that fit its specific topic rather than inheriting the generic system-architecture template or the decision-framework template. The outline above serves as the intended section plan. When writing the flagship version, use those outline points as top-level `## Section` headings and add subsections, diagrams, and worked examples inside each one — no generic Architecture / Components / Request Lifecycle / Scalability / Monitoring scaffolding unless those titles genuinely fit the content.

## What This Chapter Will Cover

- PII detection in prompts and context: NER, regex, learned classifiers
- Redaction and pseudonymisation before sending to external model APIs
- Logging policies: full-fidelity vs anonymised vs no-logging under compliance
- Right-to-delete: removing PII from vector indexes and fine-tuned weights
- Data residency: per-tenant regional routing for compliance, not just latency

---

*Part of [Enterprise AI](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
