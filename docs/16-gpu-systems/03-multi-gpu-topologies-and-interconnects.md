# Multi-GPU Topologies & Interconnects

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. How GPUs within a node and across nodes are connected (NVLink, InfiniBand), and why interconnect topology — not just GPU count — determines whether multi-GPU serving actually scales.

## What This Chapter Will Cover

- Intra-node interconnect (NVLink/NVSwitch) vs inter-node (InfiniBand/Ethernet)
- Topology-aware placement for tensor/pipeline parallelism
- Network as the bottleneck at cluster scale
- Cost implications of topology choices

---

*Part of [GPU Systems](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
