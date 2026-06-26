# Disaggregated Prefill/Decode

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. Why separating the compute-bound prefill phase from the memory-bandwidth-bound decode phase onto different hardware pools improves both throughput and latency predictability at scale.

## What This Chapter Will Cover

- Prefill (compute-bound) vs decode (bandwidth-bound) characteristics
- Why co-locating them causes interference
- Disaggregated serving architecture and the KV-cache transfer cost
- When disaggregation pays off vs added complexity

---

*Part of [Distributed Inference](index.md) in the [AI System Design Handbook](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
