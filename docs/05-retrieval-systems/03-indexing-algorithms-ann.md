# Indexing Algorithms (ANN/HNSW/IVF)

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. The approximate-nearest-neighbor algorithms (HNSW, IVF, product quantization) that make billion-scale vector search possible, and the recall/latency/memory tradeoffs each one makes.

## What This Chapter Will Cover

- HNSW: graph structure, build cost, recall/latency tradeoff
- IVF and IVF-PQ: clustering plus quantization for memory savings
- Recall@k as the metric that matters
- Index choice as a function of corpus size and update frequency

---

*Part of [Retrieval Systems](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
