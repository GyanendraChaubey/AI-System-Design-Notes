# SSO, Permissions & RAG ACL Enforcement

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. The hard enterprise-RAG problem — making sure retrieval never surfaces a document the requesting user isn't permitted to see — and the architectural patterns that enforce this at retrieval time, not just at the UI layer.

## What This Chapter Will Cover

- Why permission checks must happen at retrieval time, not display time
- Document-level ACL syncing from source systems
- Permission-aware indexing vs post-retrieval filtering
- Performance cost of ACL enforcement at retrieval scale

---

*Part of [Enterprise AI](index.md) in the [AI System Design Handbook](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
