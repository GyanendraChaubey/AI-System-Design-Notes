# Context Windows & Positional Encoding

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. How models extend usable context length via positional encoding schemes (RoPE, ALiBi, NTK/YaRN scaling), and why a model's advertised context window is rarely the length at which it reasons reliably.

## What This Chapter Will Cover

- Absolute vs relative vs rotary positional encoding
- Context-length extension techniques and their failure modes
- Lost in the middle: effective vs advertised context length
- Implications for context engineering and RAG chunk placement

---

*Part of [LLM Architecture](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
