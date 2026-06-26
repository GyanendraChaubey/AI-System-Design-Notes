# Speculative Decoding at Scale

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. How a small draft model proposes multiple tokens that a larger model verifies in parallel, trading extra compute for fewer sequential decode steps — and the production conditions where this actually wins.

## What This Chapter Will Cover

- Draft-and-verify mechanics
- Acceptance rate as the metric that determines speedup
- Self-speculative and lookahead variants
- When speculative decoding doesn't help (already throughput-bound regimes)

---

*Part of [Distributed Inference](index.md) in the [AI System Design Handbook](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
