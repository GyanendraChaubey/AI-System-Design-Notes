# Tensor & Pipeline Parallelism

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. The two primary ways to split a model too large for one GPU across many GPUs — sharding within a layer (tensor parallelism) versus sharding across layers (pipeline parallelism) — and their communication tradeoffs.

## What This Chapter Will Cover

- Tensor parallelism: intra-layer sharding and all-reduce cost
- Pipeline parallelism: inter-layer sharding and bubble overhead
- Combining both (and data parallelism) at large scale
- Choosing a parallelism strategy by model size and interconnect

---

*Part of [Distributed Inference](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
