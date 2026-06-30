# Automated Prompt Optimisation

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. How to programmatically improve prompts rather than hand-tuning them — DSPy-style compilation, APE (Automatic Prompt Engineering), RIME, and LLM-as-judge feedback loops that outperform manual iteration on most structured task types.

!!! note "Template: Topic-Specific Structure"
    This chapter will be designed from scratch with sections that fit its specific topic rather than inheriting the generic system-architecture template or the decision-framework template. The outline above serves as the intended section plan. When writing the flagship version, use those outline points as top-level `## Section` headings and add subsections, diagrams, and worked examples inside each one — no generic Architecture / Components / Request Lifecycle / Scalability / Monitoring scaffolding unless those titles genuinely fit the content.

## What This Chapter Will Cover

- The limits of manual prompt iteration at scale
- DSPy: compile prompts from task signature + training examples
- APE and gradient-free prompt search (LLM-as-proposer + scorer)
- RIME and instruction induction from examples
- LLM-as-judge feedback loops for continuous prompt refinement
- When automated optimisation beats manual: task types and data requirements

---

*Part of [Prompt Architecture](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
