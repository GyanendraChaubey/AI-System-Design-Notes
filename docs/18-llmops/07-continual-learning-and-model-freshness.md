# Continual Learning and Model Freshness

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. How production AI systems stay current without full retraining — knowledge cutoff management, online learning patterns for personalisation, RLHF as a production feedback loop, and detecting when a model's world model has become stale.

!!! note "Template: Topic-Specific Structure"
    This chapter will be designed from scratch with sections that fit its specific topic rather than inheriting the generic system-architecture template or the decision-framework template. The outline above serves as the intended section plan. When writing the flagship version, use those outline points as top-level `## Section` headings and add subsections, diagrams, and worked examples inside each one — no generic Architecture / Components / Request Lifecycle / Scalability / Monitoring scaffolding unless those titles genuinely fit the content.

## What This Chapter Will Cover

- The knowledge cutoff problem: retrieval vs fine-tuning vs full retrain
- Online learning for personalisation: per-user adapters and preference vectors
- RLHF as a production loop: collecting preference data and deploying updates
- Concept drift detection: when AI outputs silently diverge from expectations
- Catastrophic forgetting mitigation when fine-tuning on new data

---

*Part of [LLMOps](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
