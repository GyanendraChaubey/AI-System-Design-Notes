# Capacity Planning Primer

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. A back-of-envelope toolkit for sizing AI systems — converting DAU/MAU into QPS, QPS into tokens/sec, and tokens/sec into GPU counts — reused throughout every case study in this handbook.

## What This Chapter Will Cover

- From DAU to QPS: peak-to-average ratios and why AI traffic is burstier than typical web traffic
- From QPS to tokens/sec: input/output token ratios per use case
- From tokens/sec to GPU count: throughput-per-GPU as the conversion factor
- A worked example carried through later case studies

---

*Part of [Fundamentals](index.md) in the [AI System Design Handbook](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
