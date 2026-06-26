# Hybrid Search & Reranking

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. Why production retrieval almost always combines lexical (BM25) and dense retrieval, then reranks with a cross-encoder — and how each stage trades latency for precision.

## What This Chapter Will Cover

- Why dense-only retrieval misses exact-match and rare-term queries
- Fusion strategies (RRF, weighted scoring)
- Cross-encoder reranking: cost vs precision gain
- Multi-stage retrieval pipelines as the production default

---

*Part of [Retrieval Systems](index.md) in the [AI System Design Handbook](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
