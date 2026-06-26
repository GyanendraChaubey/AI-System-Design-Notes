# Tracing LLM Calls

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. What a useful trace of an LLM/agent call actually captures — prompts, retrieved context, tool calls, token counts, latency per hop — and the instrumentation pattern that scales to multi-step agents.

## What This Chapter Will Cover

- Span structure for a single LLM call vs a multi-step agent trace
- Capturing prompts/context without blowing up storage cost
- Correlating traces across retrieval, model, and tool calls
- Sampling strategy for trace storage at scale

---

*Part of [Observability](index.md) in the [AI System Design Handbook](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
