# Estimation & Capacity Planning Drills

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. Worked practice problems for the back-of-envelope math interviewers expect — using Alex Xu's estimation framework adapted for AI systems: QPS, token throughput, GPU counts, storage, and cost-constrained design (e.g. '$500/month for 10K users') — with every assumption named and defended.

!!! note "Template: Topic-Specific Structure"
    This chapter will be designed from scratch with sections that fit its specific topic rather than inheriting the generic system-architecture template or the decision-framework template. The outline above serves as the intended section plan. When writing the flagship version, use those outline points as top-level `## Section` headings and add subsections, diagrams, and worked examples inside each one — no generic Architecture / Components / Request Lifecycle / Scalability / Monitoring scaffolding unless those titles genuinely fit the content.

## What This Chapter Will Cover

- The Alex Xu back-of-envelope framework: DAUs, QPS avg, QPS peak, storage, bandwidth
- AI-specific assumption anchors: tokens/word, tokens/request by workload type, GPU throughput ranges
- Worked drill 1: Conversational AI at 1M DAU — fleet size and API cost
- Worked drill 2: Enterprise RAG at 50K employees — index size, retrieval QPS, storage
- Worked drill 3: Coding assistant with real-time completion — sub-100ms budget breakdown
- Worked drill 4: Cost-constrained design — '$500/month, 10K users, build what you can'
- Worked drill 5: Reasoning model workload at 100K DAU — KV cache and token-volume sizing
- How interviewers grade estimation: process and defensibility over precision
- Numbers worth memorizing before an interview

---

*Part of [Interview Prep](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
