# The Fine-Tuning Engineering Pipeline

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. The end-to-end engineering workflow for improving a model through fine-tuning — data collection and curation, PEFT/LoRA/QLoRA training infrastructure, the evaluation loop during training, DPO and RLHF pipelines, and the complete loop from production failure to deployed model improvement.

!!! note "Template: Topic-Specific Structure"
    This chapter will be designed from scratch with sections that fit its specific topic rather than inheriting the generic system-architecture template or the decision-framework template. The outline above serves as the intended section plan. When writing the flagship version, use those outline points as top-level `## Section` headings and add subsections, diagrams, and worked examples inside each one — no generic Architecture / Components / Request Lifecycle / Scalability / Monitoring scaffolding unless those titles genuinely fit the content.

## What This Chapter Will Cover

- Data collection and curation: sourcing, filtering, format normalisation
- PEFT techniques: LoRA, QLoRA, DoRA — trade-offs in serving cost and quality
- Training orchestration: FSDP vs DeepSpeed, gradient checkpointing
- DPO/ORPO/RLHF as engineering systems: preference data and policy optimisation
- The full improvement loop: prod failure to data to train to eval to deploy

---

*Part of [LLMOps](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
