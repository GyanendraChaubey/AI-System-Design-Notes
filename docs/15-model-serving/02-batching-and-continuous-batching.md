# Batching & Continuous Batching

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. How serving engines batch concurrent requests to maximize GPU utilization, and why continuous (in-flight) batching specifically solved the head-of-line blocking that static batching couldn't.

## What This Chapter Will Cover

- Static batching and its head-of-line blocking problem
- Continuous/in-flight batching mechanics
- Throughput vs latency tradeoff as batch size grows
- Interaction with KV cache memory limits

---

*Part of [Model Serving](index.md) in the [AI System Design Handbook](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
