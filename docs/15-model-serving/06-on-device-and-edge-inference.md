# On-Device and Edge Inference

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. The architecture for running AI models on device rather than in the cloud — when privacy, latency, or connectivity requirements demand it, how to choose and deploy models under hardware constraints, and hybrid device-cloud routing patterns.

!!! note "Template: Topic-Specific Structure"
    This chapter will be designed from scratch with sections that fit its specific topic rather than inheriting the generic system-architecture template or the decision-framework template. The outline above serves as the intended section plan. When writing the flagship version, use those outline points as top-level `## Section` headings and add subsections, diagrams, and worked examples inside each one — no generic Architecture / Components / Request Lifecycle / Scalability / Monitoring scaffolding unless those titles genuinely fit the content.

## What This Chapter Will Cover

- When edge inference is the right architecture: privacy, sub-100ms, offline
- Quantization for edge hardware: INT4/INT8 on NPUs and mobile GPUs
- Hybrid edge-cloud routing: device handles simple, cloud handles complex
- Model update distribution to millions of devices without CDN blowout
- Hardware diversity: CoreML, ONNX, ExecuTorch and per-device gaps

---

*Part of [Model Serving](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
