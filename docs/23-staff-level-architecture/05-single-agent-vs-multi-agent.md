# Single-Agent vs Multi-Agent

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. Why multi-agent systems are not "free parallelism" — the coordination tax, cost multiplication, and debugging difficulty that mean a single well-scoped agent beats a multi-agent system more often than the hype suggests.

!!! note "Template: Decision Framework"
    This is a judgment call between approaches, not a system with its own components to diagram, so it will follow the lighter **Decision Framework** template (Overview, Definition, The Real Question, Core Concepts, Decision Framework, Worked Example, Tradeoffs, Cost Implications, Common Mistakes, Real World Examples, Interview Questions, Google-Level Follow-Ups, Key Takeaways) rather than the full systems-architecture template.

## What This Chapter Will Cover

- The coordination tax: communication overhead, redundant work
- Cost multiplication (N agents, N times the tokens)
- When parallel sub-agents genuinely help (independent, parallelizable sub-tasks)
- A decision checklist

---

*Part of [Staff-Level Architecture](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
