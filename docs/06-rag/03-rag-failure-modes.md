# RAG Failure Modes

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. The catalog of ways RAG systems fail in production — retrieval misses, irrelevant-context distraction, stale indexes, citation hallucination — and the detection signal for each.

## What This Chapter Will Cover

- Retrieval failure: the relevant doc never makes top-k
- Generation failure despite correct retrieval: distraction, ignoring context
- Staleness: index lag vs source-of-truth changes
- Citation hallucination and how to catch it

---

*Part of [RAG](index.md) in the [AI System Design Handbook](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
