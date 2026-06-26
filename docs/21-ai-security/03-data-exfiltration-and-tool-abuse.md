# Data Exfiltration & Tool Abuse

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. How an agent with tool access becomes a data-exfiltration vector — and the architectural controls (egress allowlisting, output scanning, tool permissioning) that contain the blast radius.

## What This Chapter Will Cover

- Exfiltration via tool side-effects (e.g. sending retrieved secrets to an external URL)
- Egress allowlisting for agent-initiated network calls
- Output scanning for sensitive-data leakage
- Least-privilege tool scoping per session/tenant

---

*Part of [AI Security](index.md) in the [AI System Design Handbook](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
