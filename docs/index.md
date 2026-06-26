# AI System Design Handbook

A Staff-level reference for designing, scaling, and shipping production AI systems — written for engineers who need to go past "call the OpenAI API" into how ChatGPT, Claude, Perplexity, Cursor, and Glean-style platforms are actually architected, scaled, secured, and paid for.

This is not a machine learning theory book. You will not find derivations of backpropagation, SVMs, or random forests here. Every chapter is about **systems**: the architecture, the tradeoffs, the failure modes, the cost model, and the interview-ready depth behind production AI.

## Who this is for

- AI / Applied AI / LLM Engineers who want a production-architecture reference, not just API docs
- Software Engineers transitioning into AI who already think in systems but need the AI-specific primitives
- Senior and Staff Engineers preparing for AI System Design interviews at Google, OpenAI, Anthropic, Meta, Microsoft, Amazon, Uber, Airbnb, Stripe, Glean, Cursor, or Perplexity
- Engineering Managers and founders who need to make build-vs-buy and architecture calls for an AI product

## How to use this handbook

Each **chapter** (Fundamentals through Staff-Level Architecture) follows the same fixed format: Overview → Definition → Problem Statement → Architecture → Components → Request Lifecycle → Design Patterns → Tradeoffs → Scalability → Reliability → Security → Cost → Monitoring → Production Best Practices → Real World Examples → Interview Questions (Beginner/Intermediate/Senior/Staff) → Google-Level Follow-Ups → Common Mistakes → Key Takeaways — with 5 Mermaid diagrams each.

Each **case study** (Case Studies section) follows a 16-part format built for whiteboarding practice: Requirements → Capacity Planning → Scale Estimation → High Level Design → Detailed Design → API Design → Data Flow → Retrieval/Agent/Model Layers → Observability → Security → Cost Model → Failure Handling → Tradeoff Analysis → Interview Discussion.

If you're prepping for an interview, start with [How AI System Design Interviews Work](24-interview-prep/01-how-ai-system-design-interviews-work.md), then work through [Anatomy of an AI System](01-fundamentals/03-anatomy-of-an-ai-system.md) and the [ChatGPT case study](25-case-studies/01-chatgpt.md) before picking the case studies closest to the company you're targeting.

## Status

This handbook is under active construction. Every topic in the curriculum below already has a page — nothing 404s — but pages are at one of two depths:

- **✅ Complete** — full Staff-level depth: all required sections, 5 Mermaid diagrams, concrete numbers, answered interview questions.
- **📋 Planned** — scaffolded with a real synopsis and outline, expanded in a future pass.

See [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md) in the repo for the exact, up-to-date list. Currently complete: **18 flagship chapters/case studies** spanning every major section, so you can see the target depth everywhere in the curriculum.

## Curriculum

| # | Section | Focus |
|---|---|---|
| 01 | [Fundamentals](01-fundamentals/index.md) | Mental models, the reference architecture, capacity-planning math |
| 02 | [LLM Architecture](02-llm-architecture/index.md) | Transformers, tokenization, context windows, decoding — for systems engineers |
| 03 | [Prompt Architecture](03-prompt-architecture/index.md) | Prompts as versioned, tested production artifacts |
| 04 | [Context Engineering](04-context-engineering/index.md) | Budgeting, compressing, and routing what goes into the context window |
| 05 | [Retrieval Systems](05-retrieval-systems/index.md) | Embeddings, vector databases, ANN indexing, hybrid search |
| 06 | [RAG](06-rag/index.md) | The canonical retrieve-then-generate architecture, evaluated and hardened |
| 07 | [GraphRAG](07-graphrag/index.md) | Graph-structured retrieval for multi-hop, corpus-wide queries |
| 08 | [Agentic RAG](08-agentic-rag/index.md) | Retrieval as a tool call, not a fixed pre-step |
| 09 | [Agents](09-agents/index.md) | The agent loop, reasoning patterns, tool use, evaluation |
| 10 | [Multi-Agent Systems](10-multi-agent-systems/index.md) | Orchestration patterns and coordination failure |
| 11 | [Planning Systems](11-planning-systems/index.md) | Task decomposition, plan-and-execute vs ReAct, replanning |
| 12 | [Memory Systems](12-memory-systems/index.md) | Working, episodic, and semantic memory for agents |
| 13 | [Tool Calling](13-tool-calling/index.md) | Function-calling architecture, MCP, tool selection at scale |
| 14 | [AI Infrastructure](14-ai-infrastructure/index.md) | The stack map: hardware through orchestration |
| 15 | [Model Serving](15-model-serving/index.md) | Batching, KV cache, quantization, multi-model routing |
| 16 | [GPU Systems](16-gpu-systems/index.md) | GPU fundamentals, sizing math, multi-GPU topology |
| 17 | [Distributed Inference](17-distributed-inference/index.md) | Tensor/pipeline parallelism, disaggregation, speculative decoding |
| 18 | [LLMOps](18-llmops/index.md) | Versioning, canary/shadow deployment, CI/CD for graded artifacts |
| 19 | [Evaluation](19-evaluation/index.md) | Offline/online eval, LLM-as-judge, human annotation, regression testing |
| 20 | [Observability](20-observability/index.md) | Tracing, cost monitoring, drift detection |
| 21 | [AI Security](21-ai-security/index.md) | Prompt injection, tool abuse, guardrails, supply chain |
| 22 | [Enterprise AI](22-enterprise-ai/index.md) | Multi-tenancy, governance, permission-aware RAG |
| 23 | [Staff-Level Architecture](23-staff-level-architecture/index.md) | Build vs buy, fine-tune vs RAG, cost/latency/reliability engineering |
| 24 | [Interview Prep](24-interview-prep/index.md) | The whiteboarding framework, estimation drills, company-specific focus |
| 25 | [Case Studies](25-case-studies/index.md) | 20 full system designs: ChatGPT, Claude, Perplexity, Cursor, Glean, and more |

---

*This handbook draws inspiration from [AI Engineering Notes](https://gyanendrachaubey.github.io/AI-Engineering-Notes/) but is organized around production system architecture rather than interview Q&A — every chapter is a design reference first, an interview-prep page second.*
