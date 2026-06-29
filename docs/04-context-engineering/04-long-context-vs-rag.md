# Long Context vs RAG

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. Why bigger context windows did not eliminate RAG — the cost, latency, and lost-in-the-middle reasons large-context stuffing loses to targeted retrieval at scale, and where each approach actually wins.

!!! note "Template: Decision Framework"
    This is a judgment call between approaches, not a system with its own components to diagram, so it will follow the lighter **Decision Framework** template (Overview, Definition, The Real Question, Core Concepts, Decision Framework, Worked Example, Tradeoffs, Cost Implications, Common Mistakes, Real World Examples, Interview Questions, Google-Level Follow-Ups, Key Takeaways) rather than the full systems-architecture template.

## What This Chapter Will Cover

- The naive argument ("just put it all in context") and why it breaks at scale
- Cost-per-query: full-context stuffing vs retrieval
- Retrieval precision vs recall-everything
- A decision framework: when long context wins, when RAG wins, when to combine both

---

*Part of [Context Engineering](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
