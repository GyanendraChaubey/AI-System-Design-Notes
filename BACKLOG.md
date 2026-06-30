# Backlog

Source of truth: `scripts/new_stub.py` (the `SECTIONS` list). Edit entries there and re-run the script rather than hand-editing this file — it is regenerated.

## Status Legend

- ✅ Flagship — full Staff-level depth, written
- 📋 Stub — scaffolded with synopsis + outline, not yet expanded

## Fundamentals (`docs/01-fundamentals/`)

- ✅ `01-introduction.md` — Introduction to AI System Design
- ✅ `02-core-mental-models.md` — Core Mental Models
- ✅ `03-anatomy-of-an-ai-system.md` — Anatomy of an AI System
- ✅ `04-capacity-planning-primer.md` — Capacity Planning Primer

## LLM Architecture (`docs/02-llm-architecture/`)

- ✅ `01-transformer-internals-for-systems-engineers.md` — Transformer Internals for Systems Engineers
- ✅ `02-tokenization-and-vocabulary.md` — Tokenization & Vocabulary
- ✅ `03-context-windows-and-positional-encoding.md` — Context Windows & Positional Encoding
- ✅ `04-decoding-and-inference-strategies.md` — Decoding & Inference Strategies
- ✅ `05-model-families-and-selection.md` — Model Families & Selection

## Prompt Architecture (`docs/03-prompt-architecture/`)

- 📋 `01-prompt-engineering-as-systems-design.md` — Prompt Engineering as Systems Design
- 📋 `02-prompt-templates-and-versioning.md` — Prompt Templates & Versioning
- 📋 `03-structured-output-and-grammars.md` — Structured Output & Grammars
- 📋 `04-prompt-injection-resilient-design.md` — Prompt-Injection-Resilient Design
- 📋 `05-automated-prompt-optimisation.md` — Automated Prompt Optimisation *(topic-specific structure)*

## Context Engineering (`docs/04-context-engineering/`)

- ✅ `01-what-is-context-engineering.md` — What Is Context Engineering
- 📋 `02-context-window-budgeting.md` — Context Window Budgeting
- 📋 `03-context-compression-and-summarization.md` — Context Compression & Summarization
- 📋 `04-long-context-vs-rag.md` — Long Context vs RAG *(decision framework template)*
- 📋 `05-context-rot-and-failure-modes.md` — Context Rot & Failure Modes

## Retrieval Systems (`docs/05-retrieval-systems/`)

- 📋 `01-embedding-models.md` — Embedding Models
- 📋 `02-vector-databases.md` — Vector Databases
- 📋 `03-indexing-algorithms-ann.md` — Indexing Algorithms (ANN/HNSW/IVF)
- 📋 `04-hybrid-search-and-reranking.md` — Hybrid Search & Reranking
- 📋 `05-chunking-strategies.md` — Chunking Strategies
- 📋 `06-knowledge-base-lifecycle-management.md` — Knowledge Base Lifecycle Management *(topic-specific structure)*

## RAG (`docs/06-rag/`)

- ✅ `01-rag-architecture.md` — RAG Architecture
- 📋 `02-rag-evaluation-metrics.md` — RAG Evaluation Metrics
- 📋 `03-rag-failure-modes.md` — RAG Failure Modes
- 📋 `04-advanced-rag-patterns.md` — Advanced RAG Patterns

## GraphRAG (`docs/07-graphrag/`)

- 📋 `01-graphrag-architecture.md` — GraphRAG Architecture
- 📋 `02-knowledge-graph-construction.md` — Knowledge Graph Construction
- 📋 `03-when-graphrag-beats-vector-rag.md` — When GraphRAG Beats Vector RAG *(decision framework template)*

## Agentic RAG (`docs/08-agentic-rag/`)

- 📋 `01-agentic-rag-architecture.md` — Agentic RAG Architecture
- 📋 `02-iterative-retrieval-and-self-correction.md` — Iterative Retrieval & Self-Correction

## Agents (`docs/09-agents/`)

- ✅ `01-agent-fundamentals-and-the-agent-loop.md` — Agent Fundamentals & the Agent Loop
- 📋 `02-react-and-reasoning-patterns.md` — ReAct & Reasoning Patterns
- 📋 `03-tool-use-architecture.md` — Tool Use Architecture
- 📋 `04-agent-evaluation.md` — Agent Evaluation
- 📋 `05-agent-failure-modes-and-guardrails.md` — Agent Failure Modes & Guardrails
- 📋 `06-human-in-the-loop-architecture.md` — Human-in-the-Loop Architecture *(topic-specific structure)*

## Multi-Agent Systems (`docs/10-multi-agent-systems/`)

- ✅ `01-multi-agent-architecture-patterns.md` — Multi-Agent Architecture Patterns
- 📋 `02-agent-communication-protocols.md` — Agent Communication Protocols
- 📋 `03-coordination-failure-and-emergent-behavior.md` — Coordination Failure & Emergent Behavior

## Planning Systems (`docs/11-planning-systems/`)

- 📋 `01-task-decomposition-and-planning.md` — Task Decomposition & Planning
- 📋 `02-plan-and-execute-vs-react.md` — Plan-and-Execute vs ReAct *(decision framework template)*
- 📋 `03-replanning-and-error-recovery.md` — Replanning & Error Recovery

## Memory Systems (`docs/12-memory-systems/`)

- 📋 `01-memory-architecture-for-agents.md` — Memory Architecture for Agents
- 📋 `02-short-term-vs-long-term-memory.md` — Short-Term vs Long-Term Memory
- 📋 `03-memory-retrieval-and-forgetting.md` — Memory Retrieval & Forgetting

## Tool Calling (`docs/13-tool-calling/`)

- 📋 `01-function-calling-architecture.md` — Function Calling Architecture
- 📋 `02-model-context-protocol.md` — Model Context Protocol (MCP)
- 📋 `03-tool-selection-at-scale.md` — Tool Selection at Scale

## AI Infrastructure (`docs/14-ai-infrastructure/`)

- 📋 `01-ai-infrastructure-overview.md` — AI Infrastructure Overview
- 📋 `02-the-inference-stack.md` — The Inference Stack
- 📋 `03-ai-data-pipelines.md` — AI Data Pipelines: Ingestion, Quality, and Freshness *(topic-specific structure)*
- 📋 `04-real-time-and-streaming-ai.md` — Real-Time and Streaming AI Architecture *(topic-specific structure)*
- 📋 `05-ai-api-design.md` — AI API Design *(topic-specific structure)*

## Model Serving (`docs/15-model-serving/`)

- ✅ `01-model-serving-architecture.md` — Model Serving Architecture
- 📋 `02-batching-and-continuous-batching.md` — Batching & Continuous Batching
- 📋 `03-kv-cache-management.md` — KV Cache Management
- 📋 `04-quantization-and-compression.md` — Quantization & Compression
- 📋 `05-multi-model-serving-and-routing.md` — Multi-Model Serving & Routing
- 📋 `06-on-device-and-edge-inference.md` — On-Device and Edge Inference *(topic-specific structure)*

## GPU Systems (`docs/16-gpu-systems/`)

- 📋 `01-gpu-fundamentals-for-ai-systems.md` — GPU Fundamentals for AI Systems
- ✅ `02-gpu-sizing-and-capacity-planning.md` — GPU Sizing & Capacity Planning
- 📋 `03-multi-gpu-topologies-and-interconnects.md` — Multi-GPU Topologies & Interconnects

## Distributed Inference (`docs/17-distributed-inference/`)

- 📋 `01-tensor-and-pipeline-parallelism.md` — Tensor & Pipeline Parallelism
- 📋 `02-disaggregated-prefill-decode.md` — Disaggregated Prefill/Decode
- 📋 `03-speculative-decoding-at-scale.md` — Speculative Decoding at Scale

## LLMOps (`docs/18-llmops/`)

- 📋 `01-llmops-overview.md` — LLMOps Overview
- 📋 `02-prompt-and-model-versioning.md` — Prompt & Model Versioning
- 📋 `03-deployment-strategies-canary-shadow.md` — Deployment Strategies: Canary & Shadow
- 📋 `04-ci-cd-for-ai-systems.md` — CI/CD for AI Systems
- 📋 `05-the-fine-tuning-pipeline.md` — The Fine-Tuning Engineering Pipeline *(topic-specific structure)*
- 📋 `06-ai-incident-response.md` — AI Incident Response *(topic-specific structure)*
- 📋 `07-continual-learning-and-model-freshness.md` — Continual Learning and Model Freshness *(topic-specific structure)*

## Evaluation (`docs/19-evaluation/`)

- ✅ `01-llm-evaluation-architecture.md` — LLM Evaluation Architecture
- 📋 `02-offline-vs-online-evaluation.md` — Offline vs Online Evaluation
- 📋 `03-llm-as-judge.md` — LLM-as-Judge
- 📋 `04-human-evaluation-and-annotation.md` — Human Evaluation & Annotation
- 📋 `05-regression-testing-for-llms.md` — Regression Testing for LLMs

## Observability (`docs/20-observability/`)

- 📋 `01-ai-observability-architecture.md` — AI Observability Architecture
- 📋 `02-tracing-llm-calls.md` — Tracing LLM Calls
- 📋 `03-cost-and-token-monitoring.md` — Cost & Token Monitoring
- 📋 `04-drift-and-quality-monitoring.md` — Drift & Quality Monitoring

## AI Security (`docs/21-ai-security/`)

- ✅ `01-ai-security-architecture.md` — AI Security Architecture
- 📋 `02-prompt-injection-and-jailbreaks.md` — Prompt Injection & Jailbreaks
- 📋 `03-data-exfiltration-and-tool-abuse.md` — Data Exfiltration & Tool Abuse
- 📋 `04-guardrails-and-content-safety.md` — Guardrails & Content Safety
- 📋 `05-supply-chain-and-model-security.md` — Supply Chain & Model Security

## Enterprise AI (`docs/22-enterprise-ai/`)

- 📋 `01-enterprise-ai-architecture.md` — Enterprise AI Architecture
- 📋 `02-multi-tenancy-for-ai-platforms.md` — Multi-Tenancy for AI Platforms
- 📋 `03-data-governance-and-compliance.md` — Data Governance & Compliance
- 📋 `04-sso-permissions-and-rag-acl-enforcement.md` — SSO, Permissions & RAG ACL Enforcement
- 📋 `05-pii-and-privacy-engineering.md` — PII and Privacy Engineering in AI Systems *(topic-specific structure)*
- 📋 `06-bias-fairness-and-responsible-ai.md` — Bias, Fairness, and Responsible AI Systems *(topic-specific structure)*

## Staff-Level Architecture (`docs/23-staff-level-architecture/`)

- ✅ `01-how-staff-engineers-think.md` — How Staff Engineers Think
- 📋 `02-build-vs-buy.md` — Build vs Buy *(decision framework template)*
- 📋 `03-open-source-vs-closed-models.md` — Open Source vs Closed Models *(decision framework template)*
- 📋 `04-fine-tuning-vs-rag.md` — Fine-Tuning vs RAG *(decision framework template)*
- 📋 `05-single-agent-vs-multi-agent.md` — Single-Agent vs Multi-Agent *(decision framework template)*
- 📋 `06-multi-tenant-architecture.md` — Multi-Tenant Architecture *(decision framework template)*
- 📋 `07-cost-engineering.md` — Cost Engineering
- 📋 `08-latency-engineering.md` — Latency Engineering
- 📋 `09-reliability-engineering.md` — Reliability Engineering
- 📋 `10-ai-governance-and-platform-strategy.md` — AI Governance & Platform Strategy *(decision framework template)*

## Interview Prep (`docs/24-interview-prep/`)

- ✅ `01-how-ai-system-design-interviews-work.md` — How AI System Design Interviews Work
- 📋 `02-the-whiteboarding-framework.md` — The Whiteboarding Framework *(decision framework template)*
- 📋 `03-estimation-and-capacity-planning-drills.md` — Estimation & Capacity Planning Drills *(topic-specific structure)*
- 📋 `04-company-specific-focus-areas.md` — Company-Specific Focus Areas *(decision framework template)*
- 📋 `05-common-mistakes-and-red-flags.md` — Common Mistakes & Red Flags *(decision framework template)*

## Case Studies (`docs/25-case-studies/`)

- ✅ `01-chatgpt.md` — ChatGPT
- 📋 `02-claude.md` — Claude
- 📋 `03-gemini.md` — Gemini
- ✅ `04-perplexity.md` — Perplexity
- ✅ `05-cursor.md` — Cursor
- 📋 `06-github-copilot.md` — GitHub Copilot
- ✅ `07-deep-research-agent.md` — Deep Research Agent
- ✅ `08-enterprise-rag-platform.md` — Enterprise RAG Platform
- 📋 `09-ai-customer-support-platform.md` — AI Customer Support Platform
- 📋 `10-ai-coding-agent.md` — AI Coding Agent
- 📋 `11-ai-voice-agent.md` — AI Voice Agent
- 📋 `12-ai-tutor.md` — AI Tutor
- 📋 `13-ai-healthcare-assistant.md` — AI Healthcare Assistant
- 📋 `14-ai-meeting-assistant.md` — AI Meeting Assistant
- 📋 `15-ai-search-engine.md` — AI Search Engine
- 📋 `16-multi-agent-research-system.md` — Multi-Agent Research System
- 📋 `17-autonomous-software-engineer.md` — Autonomous Software Engineer
- 📋 `18-ai-recruiter.md` — AI Recruiter
- 📋 `19-ai-sdr.md` — AI SDR
- ✅ `20-glean-enterprise-search.md` — Glean-Style Enterprise Search

## Totals

- 25 flagship chapters/case studies complete
- 106 stubs remaining
