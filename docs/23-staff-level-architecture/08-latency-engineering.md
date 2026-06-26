# Latency Engineering

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. Where latency actually accumulates in an AI request (network, queueing, prefill, decode, tool calls) and the engineering levers — streaming, speculative decoding, caching, parallelization — for each segment.

## What This Chapter Will Cover

- Latency budget breakdown across a typical request
- Streaming as a perceived-latency lever
- Prefill vs decode latency and the levers for each
- Parallelizing independent sub-calls (retrieval, tool calls)

---

*Part of [Staff-Level Architecture](index.md) in the [AI System Design Handbook](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
