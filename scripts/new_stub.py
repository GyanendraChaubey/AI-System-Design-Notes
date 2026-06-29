#!/usr/bin/env python3
"""Generates section index pages and structured stub chapters/case studies
for the AI System Design Notes.

This is the single source of truth for which docs/ pages are flagship
(full Staff-level depth, hand-written) vs stub (scaffolded synopsis +
outline, planned for a future round). Edit the SECTIONS list below, then
re-run:

    python3 scripts/new_stub.py

Re-running is safe: it only overwrites section index.md pages and stub
files. It never touches a flagship file's content (those are written
directly with an editor, not by this script) and it regenerates
BACKLOG.md from the same SECTIONS data so the two never drift apart.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

STUB_TMPL = """# {title}

!!! info "📋 Planned"
    This page is scaffolded but not yet written at full depth. {synopsis}

## What This {kind_label} Will Cover

{outline}

---

*Part of [{section_title}](index.md) in the [AI System Design Notes](../index.md). Tracked in [BACKLOG.md](https://github.com/GyanendraChaubey/AI-System-Design-Notes/blob/main/BACKLOG.md).*
"""

INDEX_TMPL = """# {title}

{intro}

| Page | Status |
|---|---|
{rows}
"""


def render_outline(items):
    return "\n".join(f"- {i}" for i in items)


def render_index_rows(section):
    rows = []
    for e in section["entries"]:
        status = "✅ Complete" if e["flagship"] else "📋 Planned"
        rows.append(f"| [{e['title']}]({e['file']}) | {status} |")
    return "\n".join(rows)


def kind_label(section):
    return "Case Study" if section["kind"] == "case_study" else "Chapter"


# ---------------------------------------------------------------------------
# SECTIONS data — populated below by section. Each section:
#   dir, title, kind ("chapter" | "case_study"), intro, entries[]
# Each entry: file, title, flagship (bool), synopsis, outline (list[str])
# ---------------------------------------------------------------------------
SECTIONS = [
    {
        "dir": "01-fundamentals",
        "title": "Fundamentals",
        "kind": "chapter",
        "intro": (
            "Start here. This section establishes the mental models, vocabulary, and "
            "back-of-envelope math that every later chapter assumes you already have — "
            "what makes AI system design different from system design as you've "
            "practiced it before, and the reference architecture diagram you'll see "
            "referenced throughout the rest of these notes."
        ),
        "entries": [
            {
                "file": "01-introduction.md",
                "title": "Introduction to AI System Design",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "02-core-mental-models.md",
                "title": "Core Mental Models",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "03-anatomy-of-an-ai-system.md",
                "title": "Anatomy of an AI System",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "04-capacity-planning-primer.md",
                "title": "Capacity Planning Primer",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
        ],
    },
    {
        "dir": "02-llm-architecture",
        "title": "LLM Architecture",
        "kind": "chapter",
        "intro": (
            "The model itself, from a systems engineer's perspective — not a deep "
            "learning course. You need enough understanding of transformer internals, "
            "tokenization, and context windows to reason about latency, cost, and "
            "failure modes; you don't need to derive backpropagation."
        ),
        "entries": [
            {
                "file": "01-transformer-internals-for-systems-engineers.md",
                "title": "Transformer Internals for Systems Engineers",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "02-tokenization-and-vocabulary.md",
                "title": "Tokenization & Vocabulary",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "03-context-windows-and-positional-encoding.md",
                "title": "Context Windows & Positional Encoding",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "04-decoding-and-inference-strategies.md",
                "title": "Decoding & Inference Strategies",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "05-model-families-and-selection.md",
                "title": "Model Families & Selection",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
        ],
    },
    {
        "dir": "03-prompt-architecture",
        "title": "Prompt Architecture",
        "kind": "chapter",
        "intro": (
            "Prompts as production software: versioned, tested, owned, and rolled "
            "out like any other deploy. This section covers the architecture around "
            "prompts, not prompt-writing tips."
        ),
        "entries": [
            {
                "file": "01-prompt-engineering-as-systems-design.md",
                "title": "Prompt Engineering as Systems Design",
                "flagship": False,
                "synopsis": (
                    "Treating prompts as versioned, tested, owned software artifacts "
                    "rather than throwaway strings — the architectural shift that "
                    "separates prototype AI products from production ones."
                ),
                "outline": [
                    "Prompts as code: ownership, review, and testing",
                    "System prompt vs developer prompt vs user prompt layering",
                    "Few-shot example selection as a retrieval problem",
                    "Where prompt architecture ends and context engineering begins",
                ],
            },
            {
                "file": "02-prompt-templates-and-versioning.md",
                "title": "Prompt Templates & Versioning",
                "flagship": False,
                "synopsis": (
                    "How production teams template, parameterize, and version "
                    "prompts so that a prompt change is a reviewable, rollback-able "
                    "deploy rather than a silent behavior shift."
                ),
                "outline": [
                    "Template engines and variable injection safety",
                    "Versioning strategies: semantic tags, hashes, shadow prompts",
                    "Rollout strategies for prompt changes (canary, A/B, staged)",
                    "Linking prompt versions to evaluation results",
                ],
            },
            {
                "file": "03-structured-output-and-grammars.md",
                "title": "Structured Output & Grammars",
                "flagship": False,
                "synopsis": (
                    "Forcing reliable, parseable output from a fundamentally "
                    "unstructured generator — JSON mode, function-calling schemas, "
                    "and constrained/grammar-based decoding."
                ),
                "outline": [
                    "JSON mode and schema-constrained generation",
                    "Grammar-based decoding (context-free-grammar constrained sampling)",
                    "Failure modes: schema drift, truncation, invalid-JSON recovery",
                    "When to validate vs when to regenerate",
                ],
            },
            {
                "file": "04-prompt-injection-resilient-design.md",
                "title": "Prompt-Injection-Resilient Design",
                "flagship": False,
                "synopsis": (
                    "Architectural patterns — not just filtering — that reduce blast "
                    "radius when untrusted content reaches the model: privilege "
                    "separation, input provenance tagging, and output-side controls."
                ),
                "outline": [
                    "Why \"just detect the injection\" doesn't scale",
                    "Privilege separation between system instructions and untrusted content",
                    "Provenance tagging and trust boundaries in the context window",
                    "Where this connects to the full AI Security chapter",
                ],
            },
        ],
    },
    {
        "dir": "04-context-engineering",
        "title": "Context Engineering",
        "kind": "chapter",
        "intro": (
            "The discipline of deciding exactly what goes into the context window, "
            "in what order, at what cost — arguably the highest-leverage skill in "
            "applied LLM engineering, and the connective tissue between prompting, "
            "retrieval, and agents."
        ),
        "entries": [
            {
                "file": "01-what-is-context-engineering.md",
                "title": "What Is Context Engineering",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "02-context-window-budgeting.md",
                "title": "Context Window Budgeting",
                "flagship": False,
                "synopsis": (
                    "Treating the context window as a finite, costed resource that "
                    "must be allocated across system instructions, retrieved "
                    "knowledge, history, and tool outputs — with an explicit budget, "
                    "not leftovers."
                ),
                "outline": [
                    "The context window as a budget, not a buffer",
                    "Allocation strategies across instructions/retrieval/history/tools",
                    "Dynamic budgeting based on query complexity",
                    "Cost implications of over-provisioning context",
                ],
            },
            {
                "file": "03-context-compression-and-summarization.md",
                "title": "Context Compression & Summarization",
                "flagship": False,
                "synopsis": (
                    "Techniques for keeping long-running conversations and large "
                    "tool outputs inside budget — rolling summarization, hierarchical "
                    "memory, and selective truncation — and what quality each one "
                    "sacrifices."
                ),
                "outline": [
                    "Rolling/recursive summarization",
                    "Hierarchical compression (recent verbatim, older summarized)",
                    "Selective truncation and salience scoring",
                    "Measuring information loss from compression",
                ],
            },
            {
                "file": "04-long-context-vs-rag.md",
                "title": "Long Context vs RAG",
                "flagship": False,
                "synopsis": (
                    "Why bigger context windows did not eliminate RAG — the cost, "
                    "latency, and lost-in-the-middle reasons large-context stuffing "
                    "loses to targeted retrieval at scale, and where each approach "
                    "actually wins."
                ),
                "outline": [
                    "The naive argument (\"just put it all in context\") and why it breaks at scale",
                    "Cost-per-query: full-context stuffing vs retrieval",
                    "Retrieval precision vs recall-everything",
                    "A decision framework: when long context wins, when RAG wins, when to combine both",
                ],
            },
            {
                "file": "05-context-rot-and-failure-modes.md",
                "title": "Context Rot & Failure Modes",
                "flagship": False,
                "synopsis": (
                    "How model quality degrades as context fills up — even within "
                    "the advertised window — and the engineering practices that "
                    "detect and mitigate this \"context rot\" in production."
                ),
                "outline": [
                    "Symptoms of context rot: instruction drift, attention dilution",
                    "Measuring effective context length empirically",
                    "Mitigations: context refresh, instruction repetition, context pruning",
                    "Monitoring signals that catch this in production",
                ],
            },
        ],
    },
    {
        "dir": "05-retrieval-systems",
        "title": "Retrieval Systems",
        "kind": "chapter",
        "intro": (
            "The infrastructure that finds relevant information before generation "
            "happens: embeddings, vector databases, indexing algorithms, and the "
            "hybrid search/reranking pipelines production retrieval actually runs."
        ),
        "entries": [
            {
                "file": "01-embedding-models.md",
                "title": "Embedding Models",
                "flagship": False,
                "synopsis": (
                    "How dense and sparse embedding models turn text into vectors, "
                    "what makes one embedding model better than another for a given "
                    "domain, and the operational cost of embedding at scale."
                ),
                "outline": [
                    "Dense (bi-encoder) vs sparse (BM25-style/learned sparse) representations",
                    "Domain adaptation and fine-tuning embeddings",
                    "Embedding dimensionality vs storage/latency tradeoffs",
                    "Re-embedding cost when you change models",
                ],
            },
            {
                "file": "02-vector-databases.md",
                "title": "Vector Databases",
                "flagship": False,
                "synopsis": (
                    "What a vector database actually has to do beyond \"store "
                    "vectors\" — indexing, filtering, hybrid queries, multi-tenancy "
                    "— and how to choose among the current generation of options."
                ),
                "outline": [
                    "Core requirements: ANN search, metadata filtering, hybrid queries",
                    "Managed vs self-hosted vs library-embedded (in-process) options",
                    "Multi-tenancy and namespace isolation",
                    "Selection criteria by scale and query pattern",
                ],
            },
            {
                "file": "03-indexing-algorithms-ann.md",
                "title": "Indexing Algorithms (ANN/HNSW/IVF)",
                "flagship": False,
                "synopsis": (
                    "The approximate-nearest-neighbor algorithms (HNSW, IVF, product "
                    "quantization) that make billion-scale vector search possible, "
                    "and the recall/latency/memory tradeoffs each one makes."
                ),
                "outline": [
                    "HNSW: graph structure, build cost, recall/latency tradeoff",
                    "IVF and IVF-PQ: clustering plus quantization for memory savings",
                    "Recall@k as the metric that matters",
                    "Index choice as a function of corpus size and update frequency",
                ],
            },
            {
                "file": "04-hybrid-search-and-reranking.md",
                "title": "Hybrid Search & Reranking",
                "flagship": False,
                "synopsis": (
                    "Why production retrieval almost always combines lexical (BM25) "
                    "and dense retrieval, then reranks with a cross-encoder — and "
                    "how each stage trades latency for precision."
                ),
                "outline": [
                    "Why dense-only retrieval misses exact-match and rare-term queries",
                    "Fusion strategies (RRF, weighted scoring)",
                    "Cross-encoder reranking: cost vs precision gain",
                    "Multi-stage retrieval pipelines as the production default",
                ],
            },
            {
                "file": "05-chunking-strategies.md",
                "title": "Chunking Strategies",
                "flagship": False,
                "synopsis": (
                    "How document-splitting decisions — fixed-size, semantic, "
                    "structural, hierarchical — directly determine retrieval recall "
                    "and downstream answer quality, often more than embedding model "
                    "choice does."
                ),
                "outline": [
                    "Fixed-size vs semantic vs structure-aware chunking",
                    "Chunk size/overlap tradeoffs",
                    "Hierarchical and parent-child chunking",
                    "Chunking failure modes that silently hurt RAG quality",
                ],
            },
        ],
    },
    {
        "dir": "06-rag",
        "title": "RAG",
        "kind": "chapter",
        "intro": (
            "Retrieval-Augmented Generation: the default architecture for grounding "
            "LLM output in your own data. This section covers the canonical "
            "pipeline, how to evaluate it, how it fails, and the patterns that go "
            "beyond naive retrieve-then-generate."
        ),
        "entries": [
            {
                "file": "01-rag-architecture.md",
                "title": "RAG Architecture",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "02-rag-evaluation-metrics.md",
                "title": "RAG Evaluation Metrics",
                "flagship": False,
                "synopsis": (
                    "The metrics — retrieval recall/precision, faithfulness, answer "
                    "relevance, context precision — that separate \"the demo looks "
                    "good\" from a RAG system you can actually trust in production."
                ),
                "outline": [
                    "Retrieval-side metrics: recall@k, MRR, precision",
                    "Generation-side metrics: faithfulness/groundedness, answer relevance",
                    "Composite metric-suite frameworks (RAGAS-style)",
                    "Building a regression eval set from production queries",
                ],
            },
            {
                "file": "03-rag-failure-modes.md",
                "title": "RAG Failure Modes",
                "flagship": False,
                "synopsis": (
                    "The catalog of ways RAG systems fail in production — retrieval "
                    "misses, irrelevant-context distraction, stale indexes, citation "
                    "hallucination — and the detection signal for each."
                ),
                "outline": [
                    "Retrieval failure: the relevant doc never makes top-k",
                    "Generation failure despite correct retrieval: distraction, ignoring context",
                    "Staleness: index lag vs source-of-truth changes",
                    "Citation hallucination and how to catch it",
                ],
            },
            {
                "file": "04-advanced-rag-patterns.md",
                "title": "Advanced RAG Patterns",
                "flagship": False,
                "synopsis": (
                    "Patterns that go beyond naive retrieve-then-generate — query "
                    "rewriting, HyDE, RAG-fusion, self-RAG — each addressing a "
                    "specific failure mode from the previous chapter."
                ),
                "outline": [
                    "Query rewriting and decomposition",
                    "HyDE (hypothetical document embeddings)",
                    "RAG-fusion and multi-query retrieval",
                    "Self-RAG / reflective retrieval loops",
                ],
            },
        ],
    },
    {
        "dir": "07-graphrag",
        "title": "GraphRAG",
        "kind": "chapter",
        "intro": (
            "When your corpus's value is in the relationships between entities, not "
            "just the text itself — graph-structured retrieval for multi-hop and "
            "corpus-wide synthesis queries that vector RAG cannot answer well."
        ),
        "entries": [
            {
                "file": "01-graphrag-architecture.md",
                "title": "GraphRAG Architecture",
                "flagship": False,
                "synopsis": (
                    "How GraphRAG represents a corpus as an entity-relationship "
                    "graph instead of (or alongside) flat vector chunks, enabling "
                    "multi-hop and corpus-wide summarization queries vector RAG "
                    "cannot answer."
                ),
                "outline": [
                    "Graph construction from unstructured text (entities, relations, communities)",
                    "Local search vs global (community-summary) search",
                    "Query routing between graph and vector retrieval",
                    "Latency and cost profile vs vector RAG",
                ],
            },
            {
                "file": "02-knowledge-graph-construction.md",
                "title": "Knowledge Graph Construction",
                "flagship": False,
                "synopsis": (
                    "The extraction pipeline that turns documents into a usable "
                    "knowledge graph — entity/relation extraction, resolution, and "
                    "community detection — and where it breaks at scale."
                ),
                "outline": [
                    "Entity and relation extraction via LLM pipelines",
                    "Entity resolution and deduplication",
                    "Community detection and hierarchical summarization",
                    "Incremental graph updates vs full rebuilds",
                ],
            },
            {
                "file": "03-when-graphrag-beats-vector-rag.md",
                "title": "When GraphRAG Beats Vector RAG",
                "flagship": False,
                "synopsis": (
                    "A decision framework for when the extra construction cost of "
                    "GraphRAG pays for itself versus when vector RAG is simply the "
                    "better engineering tradeoff."
                ),
                "outline": [
                    "Query types that need multi-hop reasoning vs single-fact lookup",
                    "Corpus characteristics that favor graph structure",
                    "Build/maintenance cost comparison",
                    "Hybrid architectures that use both",
                ],
            },
        ],
    },
    {
        "dir": "08-agentic-rag",
        "title": "Agentic RAG",
        "kind": "chapter",
        "intro": (
            "Retrieval as a tool the model calls iteratively, not a fixed "
            "pre-generation step — the bridge between RAG and agents."
        ),
        "entries": [
            {
                "file": "01-agentic-rag-architecture.md",
                "title": "Agentic RAG Architecture",
                "flagship": False,
                "synopsis": (
                    "RAG where retrieval is a tool the model calls iteratively and "
                    "adaptively, rather than a fixed pre-generation step — letting "
                    "the agent decide when, what, and how many times to retrieve."
                ),
                "outline": [
                    "Static retrieve-then-generate vs agentic, model-driven retrieval",
                    "Retrieval as a tool call in the agent loop",
                    "Multi-step retrieval for compositional questions",
                    "Cost and latency implications of iterative retrieval",
                ],
            },
            {
                "file": "02-iterative-retrieval-and-self-correction.md",
                "title": "Iterative Retrieval & Self-Correction",
                "flagship": False,
                "synopsis": (
                    "How agentic RAG systems detect insufficient or contradictory "
                    "retrieved evidence and self-correct by reformulating queries or "
                    "seeking additional sources before answering."
                ),
                "outline": [
                    "Sufficiency checks before generation",
                    "Query reformulation triggers",
                    "Self-critique loops and their cost",
                    "Stopping criteria to avoid infinite retrieval loops",
                ],
            },
        ],
    },
    {
        "dir": "09-agents",
        "title": "Agents",
        "kind": "chapter",
        "intro": (
            "The reasoning loop that turns an LLM from a text completion engine "
            "into a system that can take actions, observe results, and decide what "
            "to do next."
        ),
        "entries": [
            {
                "file": "01-agent-fundamentals-and-the-agent-loop.md",
                "title": "Agent Fundamentals & the Agent Loop",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "02-react-and-reasoning-patterns.md",
                "title": "ReAct & Reasoning Patterns",
                "flagship": False,
                "synopsis": (
                    "ReAct (reason+act) and the family of prompting patterns — "
                    "chain-of-thought, tree-of-thought, reflection — that structure "
                    "how an agent reasons between tool calls."
                ),
                "outline": [
                    "ReAct: interleaving thought, action, and observation",
                    "Chain-of-thought vs tree-of-thought search",
                    "Reflection/self-critique patterns",
                    "When explicit reasoning traces help vs add cost without benefit",
                ],
            },
            {
                "file": "03-tool-use-architecture.md",
                "title": "Tool Use Architecture",
                "flagship": False,
                "synopsis": (
                    "The systems layer around tool calling — tool registries, "
                    "permissioning, sandboxing, and result-feeding — that turns "
                    "\"the model can call functions\" into a safe production "
                    "capability."
                ),
                "outline": [
                    "Tool registry and schema design",
                    "Permissioning and least-privilege tool access",
                    "Sandboxing side-effecting tools",
                    "Feeding tool results back into context efficiently",
                ],
            },
            {
                "file": "04-agent-evaluation.md",
                "title": "Agent Evaluation",
                "flagship": False,
                "synopsis": (
                    "Why evaluating an agent is harder than evaluating a single LLM "
                    "call — trajectory evaluation, task success rate, and the "
                    "combinatorics of multi-step failure."
                ),
                "outline": [
                    "Outcome-based vs trajectory-based evaluation",
                    "Task success rate and partial-credit scoring",
                    "Simulated environments and tool mocking for eval",
                    "Regression testing multi-step agent behavior",
                ],
            },
            {
                "file": "05-agent-failure-modes-and-guardrails.md",
                "title": "Agent Failure Modes & Guardrails",
                "flagship": False,
                "synopsis": (
                    "How agents fail in distinctive ways — looping, tool misuse, "
                    "goal drift, runaway cost — and the guardrails (budgets, step "
                    "limits, human-in-the-loop checkpoints) that contain them."
                ),
                "outline": [
                    "Infinite loops and repeated-failure detection",
                    "Goal drift over long trajectories",
                    "Cost/step budgets as a hard safety mechanism",
                    "Human-in-the-loop checkpoints for high-stakes actions",
                ],
            },
        ],
    },
    {
        "dir": "10-multi-agent-systems",
        "title": "Multi-Agent Systems",
        "kind": "chapter",
        "intro": (
            "When and how to coordinate multiple agents instead of one — the "
            "orchestration patterns, communication protocols, and the coordination "
            "failures that come with them."
        ),
        "entries": [
            {
                "file": "01-multi-agent-architecture-patterns.md",
                "title": "Multi-Agent Architecture Patterns",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "02-agent-communication-protocols.md",
                "title": "Agent Communication Protocols",
                "flagship": False,
                "synopsis": (
                    "How agents exchange state, results, and intent — shared "
                    "scratchpads, structured message passing, and emerging "
                    "standards like A2A — and the tradeoffs versus a single shared "
                    "context."
                ),
                "outline": [
                    "Shared memory/blackboard vs explicit message passing",
                    "Structured message schemas between agents",
                    "Emerging interoperability protocols (A2A-style)",
                    "Coordination overhead as a function of agent count",
                ],
            },
            {
                "file": "03-coordination-failure-and-emergent-behavior.md",
                "title": "Coordination Failure & Emergent Behavior",
                "flagship": False,
                "synopsis": (
                    "The failure modes unique to multi-agent systems — deadlock, "
                    "redundant work, conflicting actions, emergent behavior no "
                    "single agent intended — and how to detect them."
                ),
                "outline": [
                    "Deadlock and circular delegation",
                    "Redundant/conflicting work across agents",
                    "Emergent behavior from agent-to-agent feedback loops",
                    "Observability requirements specific to multi-agent systems",
                ],
            },
        ],
    },
    {
        "dir": "11-planning-systems",
        "title": "Planning Systems",
        "kind": "chapter",
        "intro": (
            "How agents decompose ambiguous goals into executable steps, and "
            "recover when a plan stops matching reality mid-execution."
        ),
        "entries": [
            {
                "file": "01-task-decomposition-and-planning.md",
                "title": "Task Decomposition & Planning",
                "flagship": False,
                "synopsis": (
                    "How an agent breaks an ambiguous high-level goal into an "
                    "executable sequence of sub-tasks, and the architectural "
                    "difference between explicit upfront planning and emergent "
                    "step-by-step planning."
                ),
                "outline": [
                    "Upfront decomposition vs emergent (just-in-time) planning",
                    "Hierarchical task networks",
                    "Dependency tracking between sub-tasks",
                    "When decomposition itself becomes the bottleneck",
                ],
            },
            {
                "file": "02-plan-and-execute-vs-react.md",
                "title": "Plan-and-Execute vs ReAct",
                "flagship": False,
                "synopsis": (
                    "The architectural fork between planning the whole trajectory "
                    "upfront (plan-and-execute) and deciding one step at a time "
                    "(ReAct) — and the latency, cost, and robustness tradeoffs of "
                    "each."
                ),
                "outline": [
                    "Plan-and-execute: upfront plan, then execute with checkpoints",
                    "ReAct: interleaved, reactive step selection",
                    "Hybrid approaches (plan, execute, replan)",
                    "Choosing based on task volatility and step cost",
                ],
            },
            {
                "file": "03-replanning-and-error-recovery.md",
                "title": "Replanning & Error Recovery",
                "flagship": False,
                "synopsis": (
                    "How systems detect that a plan has gone stale or failed "
                    "mid-execution, and the replanning strategies that recover "
                    "without restarting from scratch."
                ),
                "outline": [
                    "Failure detection mid-plan",
                    "Partial replanning vs full restart",
                    "State reconciliation after a failed step",
                    "Cost of replanning vs cost of failure",
                ],
            },
        ],
    },
    {
        "dir": "12-memory-systems",
        "title": "Memory Systems",
        "kind": "chapter",
        "intro": (
            "How agents remember — within a session and across sessions — and the "
            "engineering tradeoffs in deciding what to keep, what to retrieve, and "
            "what to forget."
        ),
        "entries": [
            {
                "file": "01-memory-architecture-for-agents.md",
                "title": "Memory Architecture for Agents",
                "flagship": False,
                "synopsis": (
                    "The layered memory architecture — working memory, episodic "
                    "memory, semantic memory — that lets an agent behave "
                    "consistently across a session and across sessions."
                ),
                "outline": [
                    "Working memory (current context) vs persistent memory",
                    "Episodic memory (what happened) vs semantic memory (what's known)",
                    "Memory write policy: what gets persisted and when",
                    "Storage backends for each memory type",
                ],
            },
            {
                "file": "02-short-term-vs-long-term-memory.md",
                "title": "Short-Term vs Long-Term Memory",
                "flagship": False,
                "synopsis": (
                    "The engineering tradeoff between keeping everything in the "
                    "active context window (short-term) versus persisting and later "
                    "retrieving facts (long-term), and how production systems blend "
                    "both."
                ),
                "outline": [
                    "Short-term: cheap, fast, bounded by context window",
                    "Long-term: unbounded, retrieval-latency cost, consolidation needed",
                    "Consolidation: promoting short-term to long-term memory",
                    "Failure modes: premature forgetting, stale long-term facts",
                ],
            },
            {
                "file": "03-memory-retrieval-and-forgetting.md",
                "title": "Memory Retrieval & Forgetting",
                "flagship": False,
                "synopsis": (
                    "How agents decide what to recall from long-term memory for the "
                    "current task, and the deliberate forgetting/decay strategies "
                    "that keep memory stores from degrading retrieval quality over "
                    "time."
                ),
                "outline": [
                    "Memory retrieval as a RAG problem over the agent's own history",
                    "Recency, relevance, and importance scoring",
                    "Decay and deliberate forgetting policies",
                    "Privacy and correction (the right to delete a memory)",
                ],
            },
        ],
    },
    {
        "dir": "13-tool-calling",
        "title": "Tool Calling",
        "kind": "chapter",
        "intro": (
            "The protocol layer underneath agentic tool use: schemas, execution, "
            "standardization (MCP), and selecting the right tool out of hundreds "
            "at scale."
        ),
        "entries": [
            {
                "file": "01-function-calling-architecture.md",
                "title": "Function Calling Architecture",
                "flagship": False,
                "synopsis": (
                    "The request/response contract underneath \"function calling\" "
                    "— schema definition, the model's structured call output, "
                    "execution, and result injection — and where each step can "
                    "silently fail."
                ),
                "outline": [
                    "Schema definition and the model's view of available tools",
                    "Parsing and validating structured call output",
                    "Execution, timeouts, and retries",
                    "Result serialization back into context",
                ],
            },
            {
                "file": "02-model-context-protocol.md",
                "title": "Model Context Protocol (MCP)",
                "flagship": False,
                "synopsis": (
                    "What MCP standardizes — a common protocol for exposing "
                    "tools/resources to any model client — and why standardization "
                    "matters once you have more than a handful of tools and more "
                    "than one model provider."
                ),
                "outline": [
                    "The problem MCP solves: N tools x M model clients without N*M integrations",
                    "Servers, clients, and the resource/tool/prompt primitives",
                    "Security implications of a standardized tool-exposure protocol",
                    "Where MCP fits versus proprietary function-calling APIs",
                ],
            },
            {
                "file": "03-tool-selection-at-scale.md",
                "title": "Tool Selection at Scale",
                "flagship": False,
                "synopsis": (
                    "Once a system has hundreds of available tools, \"list them all "
                    "in the prompt\" stops working — the retrieval and routing "
                    "problem of tool selection at scale."
                ),
                "outline": [
                    "Why tool-list-in-context breaks down past roughly 20-50 tools",
                    "Tool retrieval: embedding and ranking tool descriptions",
                    "Hierarchical tool routing (categories, then specific tools)",
                    "Measuring tool-selection accuracy",
                ],
            },
        ],
    },
    {
        "dir": "14-ai-infrastructure",
        "title": "AI Infrastructure",
        "kind": "chapter",
        "intro": (
            "The infrastructure stack underneath every AI product, from GPUs to "
            "the API gateway — the map for the next four sections (Model Serving, "
            "GPU Systems, Distributed Inference, LLMOps)."
        ),
        "entries": [
            {
                "file": "01-ai-infrastructure-overview.md",
                "title": "AI Infrastructure Overview",
                "flagship": False,
                "synopsis": (
                    "The full infrastructure stack underneath an AI product — from "
                    "GPU clusters and model serving up through orchestration, "
                    "retrieval, and observability — and how the next several "
                    "chapters map onto it."
                ),
                "outline": [
                    "The stack: hardware, serving, orchestration, data, observability",
                    "Build vs buy at each layer",
                    "How this section relates to Model Serving, GPU Systems, and Distributed Inference",
                    "A capacity-planning checklist that spans the whole stack",
                ],
            },
            {
                "file": "02-the-inference-stack.md",
                "title": "The Inference Stack",
                "flagship": False,
                "synopsis": (
                    "The layered software stack a request passes through between "
                    "\"API call\" and \"tokens generated\" — API gateway, router, "
                    "scheduler, serving engine, hardware — and where latency "
                    "actually accumulates."
                ),
                "outline": [
                    "API gateway and request validation",
                    "Model router and tiering",
                    "Scheduler and batching layer",
                    "Serving engine and hardware execution",
                ],
            },
        ],
    },
    {
        "dir": "15-model-serving",
        "title": "Model Serving",
        "kind": "chapter",
        "intro": (
            "How a trained model actually gets turned into a low-latency, "
            "high-throughput API: batching, KV cache management, quantization, and "
            "multi-model routing."
        ),
        "entries": [
            {
                "file": "01-model-serving-architecture.md",
                "title": "Model Serving Architecture",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "02-batching-and-continuous-batching.md",
                "title": "Batching & Continuous Batching",
                "flagship": False,
                "synopsis": (
                    "How serving engines batch concurrent requests to maximize GPU "
                    "utilization, and why continuous (in-flight) batching "
                    "specifically solved the head-of-line blocking that static "
                    "batching couldn't."
                ),
                "outline": [
                    "Static batching and its head-of-line blocking problem",
                    "Continuous/in-flight batching mechanics",
                    "Throughput vs latency tradeoff as batch size grows",
                    "Interaction with KV cache memory limits",
                ],
            },
            {
                "file": "03-kv-cache-management.md",
                "title": "KV Cache Management",
                "flagship": False,
                "synopsis": (
                    "Why the KV cache, not raw compute, is usually the binding "
                    "memory constraint in LLM serving, and the management "
                    "techniques (paging, eviction, prefix sharing) that determine "
                    "effective concurrency."
                ),
                "outline": [
                    "Why KV cache memory grows with sequence length and batch size",
                    "PagedAttention-style memory management",
                    "Prefix/prompt caching and sharing across requests",
                    "Eviction policies under memory pressure",
                ],
            },
            {
                "file": "04-quantization-and-compression.md",
                "title": "Quantization & Compression",
                "flagship": False,
                "synopsis": (
                    "How reducing numeric precision (FP16/INT8/INT4) and other "
                    "compression techniques trade a measured amount of quality for "
                    "significant latency, memory, and cost savings."
                ),
                "outline": [
                    "Precision formats and their quality/speed tradeoff",
                    "Post-training quantization vs quantization-aware training",
                    "Distillation and pruning as complementary techniques",
                    "Measuring quality regression after compression",
                ],
            },
            {
                "file": "05-multi-model-serving-and-routing.md",
                "title": "Multi-Model Serving & Routing",
                "flagship": False,
                "synopsis": (
                    "How production systems serve many models behind one endpoint "
                    "— tiered routing by query difficulty, multi-LoRA serving, and "
                    "the infrastructure that makes per-request model choice cheap."
                ),
                "outline": [
                    "Tiered routing by query complexity/cost",
                    "Serving many fine-tuned variants efficiently (multi-LoRA)",
                    "Cold-start and model-loading latency",
                    "Fallback routing on provider/model failure",
                ],
            },
        ],
    },
    {
        "dir": "16-gpu-systems",
        "title": "GPU Systems",
        "kind": "chapter",
        "intro": (
            "GPU fundamentals, sizing math, and multi-GPU topology — enough "
            "hardware literacy to size a cluster and defend the number in a design "
            "review."
        ),
        "entries": [
            {
                "file": "01-gpu-fundamentals-for-ai-systems.md",
                "title": "GPU Fundamentals for AI Systems",
                "flagship": False,
                "synopsis": (
                    "The GPU concepts a systems engineer needs without needing a "
                    "hardware background — memory bandwidth vs compute (FLOPs), "
                    "why LLM inference is usually memory-bandwidth-bound, and how "
                    "GPU generations compare."
                ),
                "outline": [
                    "Compute (FLOPs) vs memory bandwidth, and why inference is usually bandwidth-bound",
                    "HBM capacity and bandwidth across GPU generations",
                    "Interconnect basics (NVLink/NVSwitch) preview",
                    "Reading a GPU spec sheet for serving decisions",
                ],
            },
            {
                "file": "02-gpu-sizing-and-capacity-planning.md",
                "title": "GPU Sizing & Capacity Planning",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "03-multi-gpu-topologies-and-interconnects.md",
                "title": "Multi-GPU Topologies & Interconnects",
                "flagship": False,
                "synopsis": (
                    "How GPUs within a node and across nodes are connected (NVLink, "
                    "InfiniBand), and why interconnect topology — not just GPU "
                    "count — determines whether multi-GPU serving actually scales."
                ),
                "outline": [
                    "Intra-node interconnect (NVLink/NVSwitch) vs inter-node (InfiniBand/Ethernet)",
                    "Topology-aware placement for tensor/pipeline parallelism",
                    "Network as the bottleneck at cluster scale",
                    "Cost implications of topology choices",
                ],
            },
        ],
    },
    {
        "dir": "17-distributed-inference",
        "title": "Distributed Inference",
        "kind": "chapter",
        "intro": (
            "Serving a single model across many GPUs and many machines: "
            "parallelism strategies, disaggregated serving, and speculative "
            "decoding."
        ),
        "entries": [
            {
                "file": "01-tensor-and-pipeline-parallelism.md",
                "title": "Tensor & Pipeline Parallelism",
                "flagship": False,
                "synopsis": (
                    "The two primary ways to split a model too large for one GPU "
                    "across many GPUs — sharding within a layer (tensor "
                    "parallelism) versus sharding across layers (pipeline "
                    "parallelism) — and their communication tradeoffs."
                ),
                "outline": [
                    "Tensor parallelism: intra-layer sharding and all-reduce cost",
                    "Pipeline parallelism: inter-layer sharding and bubble overhead",
                    "Combining both (and data parallelism) at large scale",
                    "Choosing a parallelism strategy by model size and interconnect",
                ],
            },
            {
                "file": "02-disaggregated-prefill-decode.md",
                "title": "Disaggregated Prefill/Decode",
                "flagship": False,
                "synopsis": (
                    "Why separating the compute-bound prefill phase from the "
                    "memory-bandwidth-bound decode phase onto different hardware "
                    "pools improves both throughput and latency predictability at "
                    "scale."
                ),
                "outline": [
                    "Prefill (compute-bound) vs decode (bandwidth-bound) characteristics",
                    "Why co-locating them causes interference",
                    "Disaggregated serving architecture and the KV-cache transfer cost",
                    "When disaggregation pays off vs added complexity",
                ],
            },
            {
                "file": "03-speculative-decoding-at-scale.md",
                "title": "Speculative Decoding at Scale",
                "flagship": False,
                "synopsis": (
                    "How a small draft model proposes multiple tokens that a "
                    "larger model verifies in parallel, trading extra compute for "
                    "fewer sequential decode steps — and the production conditions "
                    "where this actually wins."
                ),
                "outline": [
                    "Draft-and-verify mechanics",
                    "Acceptance rate as the metric that determines speedup",
                    "Self-speculative and lookahead variants",
                    "When speculative decoding doesn't help (already throughput-bound regimes)",
                ],
            },
        ],
    },
    {
        "dir": "18-llmops",
        "title": "LLMOps",
        "kind": "chapter",
        "intro": (
            "Operating AI systems in production: versioning, deployment strategy, "
            "and CI/CD adapted for artifacts (prompts, models) that are graded, "
            "not just pass/fail."
        ),
        "entries": [
            {
                "file": "01-llmops-overview.md",
                "title": "LLMOps Overview",
                "flagship": False,
                "synopsis": (
                    "How MLOps practices extend (and where they break) for "
                    "LLM-based systems — what's the same (CI/CD, monitoring), and "
                    "what's genuinely new (prompt versioning, eval-gated releases, "
                    "drift on subjective quality)."
                ),
                "outline": [
                    "What carries over from MLOps vs what's new",
                    "The LLMOps lifecycle: prompt/model change -> eval -> staged rollout -> monitor",
                    "Ownership model: who owns a prompt change in production",
                    "Tooling landscape overview",
                ],
            },
            {
                "file": "02-prompt-and-model-versioning.md",
                "title": "Prompt & Model Versioning",
                "flagship": False,
                "synopsis": (
                    "Treating prompts and model versions as first-class deployable "
                    "artifacts with their own version history, rollback path, and "
                    "link to the eval results that justified promotion."
                ),
                "outline": [
                    "Versioning schemes for prompts and fine-tuned models",
                    "Linking versions to eval runs and approval gates",
                    "Rollback strategy when a new version regresses",
                    "Config management across environments",
                ],
            },
            {
                "file": "03-deployment-strategies-canary-shadow.md",
                "title": "Deployment Strategies: Canary & Shadow",
                "flagship": False,
                "synopsis": (
                    "How canary releases, shadow traffic, and A/B tests apply to "
                    "model/prompt rollouts, and the AI-specific wrinkle that "
                    "\"correctness\" is graded, not binary."
                ),
                "outline": [
                    "Shadow deployment for risk-free comparison",
                    "Canary rollout with automatic rollback triggers",
                    "A/B testing with quality (not just latency/error rate) as the guardrail metric",
                    "Statistical power challenges with subjective quality metrics",
                ],
            },
            {
                "file": "04-ci-cd-for-ai-systems.md",
                "title": "CI/CD for AI Systems",
                "flagship": False,
                "synopsis": (
                    "What belongs in an AI system's CI/CD pipeline beyond unit "
                    "tests — eval suites as a merge gate, regression detection on "
                    "golden sets, and automated prompt-diff review."
                ),
                "outline": [
                    "Eval suites as a required CI check",
                    "Golden-set regression testing",
                    "Automated prompt-diff and impact estimation",
                    "Release gating criteria for AI changes vs code changes",
                ],
            },
        ],
    },
    {
        "dir": "19-evaluation",
        "title": "Evaluation",
        "kind": "chapter",
        "intro": (
            "How you know an AI system is actually good — offline and online "
            "evaluation, LLM-as-judge, human annotation, and regression testing "
            "for a component that doesn't have a fixed right answer."
        ),
        "entries": [
            {
                "file": "01-llm-evaluation-architecture.md",
                "title": "LLM Evaluation Architecture",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "02-offline-vs-online-evaluation.md",
                "title": "Offline vs Online Evaluation",
                "flagship": False,
                "synopsis": (
                    "The complementary roles of offline eval (golden sets, before "
                    "deploy) and online eval (real traffic, after deploy) and why "
                    "neither one alone is sufficient."
                ),
                "outline": [
                    "Offline eval: golden/regression sets, pros and ceiling",
                    "Online eval: real traffic signals, implicit and explicit feedback",
                    "Online/offline correlation and why it degrades over time",
                    "Building a feedback loop from online back into offline sets",
                ],
            },
            {
                "file": "03-llm-as-judge.md",
                "title": "LLM-as-Judge",
                "flagship": False,
                "synopsis": (
                    "Using a model to grade another model's output at scale — the "
                    "dominant evaluation pattern in production — along with its "
                    "known biases and the techniques that make it trustworthy "
                    "enough to gate releases."
                ),
                "outline": [
                    "Why LLM-as-judge replaced pure human eval for scale",
                    "Known biases: position, verbosity, self-preference",
                    "Calibrating judge models against human-labeled samples",
                    "Rubric design for consistent grading",
                ],
            },
            {
                "file": "04-human-evaluation-and-annotation.md",
                "title": "Human Evaluation & Annotation",
                "flagship": False,
                "synopsis": (
                    "Where human judgment remains irreplaceable in evaluation, how "
                    "to design annotation guidelines that produce consistent "
                    "labels, and how to measure annotator agreement."
                ),
                "outline": [
                    "When human eval is still required despite LLM-as-judge",
                    "Annotation guideline design and calibration sessions",
                    "Inter-annotator agreement metrics",
                    "Sampling strategy: what fraction of traffic needs human eyes",
                ],
            },
            {
                "file": "05-regression-testing-for-llms.md",
                "title": "Regression Testing for LLMs",
                "flagship": False,
                "synopsis": (
                    "How to know a prompt or model change didn't silently break "
                    "something that used to work — golden-set regression suites, "
                    "semantic diffing, and the threshold-setting problem unique to "
                    "graded (not pass/fail) tests."
                ),
                "outline": [
                    "Golden sets as the regression baseline",
                    "Semantic diffing of outputs across versions",
                    "Setting pass/fail thresholds on a continuous quality score",
                    "Catching regressions that only show up on tail-distribution inputs",
                ],
            },
        ],
    },
    {
        "dir": "20-observability",
        "title": "Observability",
        "kind": "chapter",
        "intro": (
            "Seeing what your AI system is actually doing in production: tracing, "
            "cost monitoring, and drift detection for a non-deterministic core."
        ),
        "entries": [
            {
                "file": "01-ai-observability-architecture.md",
                "title": "AI Observability Architecture",
                "flagship": False,
                "synopsis": (
                    "What \"observability\" means for a system whose core "
                    "component is a non-deterministic model — the three pillars "
                    "(traces, metrics, evals-as-signal) and how they differ from "
                    "classical APM."
                ),
                "outline": [
                    "Why classical APM (latency/errors/logs) is necessary but not sufficient",
                    "The added pillar: quality/eval signal as a first-class observability dimension",
                    "Trace structure for a multi-step AI request",
                    "Building dashboards a non-ML on-call engineer can actually use",
                ],
            },
            {
                "file": "02-tracing-llm-calls.md",
                "title": "Tracing LLM Calls",
                "flagship": False,
                "synopsis": (
                    "What a useful trace of an LLM/agent call actually captures — "
                    "prompts, retrieved context, tool calls, token counts, latency "
                    "per hop — and the instrumentation pattern that scales to "
                    "multi-step agents."
                ),
                "outline": [
                    "Span structure for a single LLM call vs a multi-step agent trace",
                    "Capturing prompts/context without blowing up storage cost",
                    "Correlating traces across retrieval, model, and tool calls",
                    "Sampling strategy for trace storage at scale",
                ],
            },
            {
                "file": "03-cost-and-token-monitoring.md",
                "title": "Cost & Token Monitoring",
                "flagship": False,
                "synopsis": (
                    "Why token-level cost monitoring has to be a first-class "
                    "metric (not a monthly invoice surprise) — per-feature, "
                    "per-customer cost attribution and the alerting that catches "
                    "runaway spend early."
                ),
                "outline": [
                    "Token counting and cost attribution per request",
                    "Per-feature and per-tenant cost breakdown",
                    "Budget alerts and automatic circuit breakers",
                    "Cost anomaly detection (e.g. a prompt change that doubles token usage)",
                ],
            },
            {
                "file": "04-drift-and-quality-monitoring.md",
                "title": "Drift & Quality Monitoring",
                "flagship": False,
                "synopsis": (
                    "Detecting that a model or system has quietly gotten worse — "
                    "input distribution drift, output quality drift, and the "
                    "monitoring that catches degradation before users complain en "
                    "masse."
                ),
                "outline": [
                    "Input distribution drift (what users are asking changes over time)",
                    "Output quality drift (silent provider model updates, prompt regressions)",
                    "Proxy metrics for quality when ground truth is unavailable",
                    "Alert design for a metric that's inherently noisy",
                ],
            },
        ],
    },
    {
        "dir": "21-ai-security",
        "title": "AI Security",
        "kind": "chapter",
        "intro": (
            "The threat model unique to AI systems: prompt injection, jailbreaks, "
            "tool abuse, and the layered guardrails that contain (not eliminate) "
            "the risk."
        ),
        "entries": [
            {
                "file": "01-ai-security-architecture.md",
                "title": "AI Security Architecture",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "02-prompt-injection-and-jailbreaks.md",
                "title": "Prompt Injection & Jailbreaks",
                "flagship": False,
                "synopsis": (
                    "The mechanics of direct and indirect prompt injection and "
                    "jailbreaking, why they are fundamentally different from "
                    "classical injection attacks, and the layered defenses that "
                    "reduce (but don't eliminate) risk."
                ),
                "outline": [
                    "Direct injection vs indirect injection (poisoned tool/document content)",
                    "Jailbreak patterns and why instruction-following itself is the attack surface",
                    "Layered defenses: input filtering, privilege separation, output validation",
                    "Why \"prompt injection is unsolved\" is the correct threat-model stance today",
                ],
            },
            {
                "file": "03-data-exfiltration-and-tool-abuse.md",
                "title": "Data Exfiltration & Tool Abuse",
                "flagship": False,
                "synopsis": (
                    "How an agent with tool access becomes a data-exfiltration "
                    "vector — and the architectural controls (egress allowlisting, "
                    "output scanning, tool permissioning) that contain the blast "
                    "radius."
                ),
                "outline": [
                    "Exfiltration via tool side-effects (e.g. sending retrieved secrets to an external URL)",
                    "Egress allowlisting for agent-initiated network calls",
                    "Output scanning for sensitive-data leakage",
                    "Least-privilege tool scoping per session/tenant",
                ],
            },
            {
                "file": "04-guardrails-and-content-safety.md",
                "title": "Guardrails & Content Safety",
                "flagship": False,
                "synopsis": (
                    "The layered guardrail architecture — input classifiers, "
                    "output classifiers, and policy enforcement — that sits around "
                    "a model to catch unsafe or policy-violating content in both "
                    "directions."
                ),
                "outline": [
                    "Input-side vs output-side guardrails",
                    "Classifier-based vs rule-based vs model-based guardrails",
                    "Latency cost of guardrails and where to place them in the request path",
                    "False-positive/negative tradeoffs and tuning for the product's risk tolerance",
                ],
            },
            {
                "file": "05-supply-chain-and-model-security.md",
                "title": "Supply Chain & Model Security",
                "flagship": False,
                "synopsis": (
                    "Security risks introduced by the AI supply chain itself — "
                    "third-party model weights, fine-tuning data poisoning, "
                    "vulnerable dependencies in the serving stack, and vendor API "
                    "trust boundaries."
                ),
                "outline": [
                    "Model weight provenance and integrity",
                    "Training/fine-tuning data poisoning risk",
                    "Dependency and serving-stack vulnerabilities",
                    "Vendor API trust boundaries and shared responsibility",
                ],
            },
        ],
    },
    {
        "dir": "22-enterprise-ai",
        "title": "Enterprise AI",
        "kind": "chapter",
        "intro": (
            "What changes when your AI product has to satisfy enterprise buyers: "
            "multi-tenancy, data governance, and permission-aware retrieval."
        ),
        "entries": [
            {
                "file": "01-enterprise-ai-architecture.md",
                "title": "Enterprise AI Architecture",
                "flagship": False,
                "synopsis": (
                    "The architectural requirements that change once an AI "
                    "product moves from consumer-single-user to "
                    "enterprise-multi-tenant — identity, permissions, data "
                    "isolation, auditability — layered onto everything covered so "
                    "far."
                ),
                "outline": [
                    "What's different about enterprise requirements vs consumer AI",
                    "Identity, SSO, and per-tenant configuration",
                    "Data isolation guarantees customers actually ask for",
                    "Auditability as a first-class requirement",
                ],
            },
            {
                "file": "02-multi-tenancy-for-ai-platforms.md",
                "title": "Multi-Tenancy for AI Platforms",
                "flagship": False,
                "synopsis": (
                    "The isolation models (shared everything, shared "
                    "compute/isolated data, fully isolated) for serving many "
                    "enterprise customers from one AI platform, and how each "
                    "affects cost, security, and operational complexity."
                ),
                "outline": [
                    "Isolation models: shared, pooled-with-isolation, dedicated",
                    "Noisy-neighbor risk in shared inference capacity",
                    "Per-tenant rate limiting and fair-share scheduling",
                    "Cost allocation across tenants",
                ],
            },
            {
                "file": "03-data-governance-and-compliance.md",
                "title": "Data Governance & Compliance",
                "flagship": False,
                "synopsis": (
                    "The governance requirements (data residency, retention, "
                    "right-to-delete, audit trails) that AI products must satisfy "
                    "to sell into regulated enterprises, and how they constrain "
                    "architecture."
                ),
                "outline": [
                    "Data residency and regional processing requirements",
                    "Retention policies for prompts, outputs, and embeddings",
                    "Right-to-delete and its implications for vector indexes and fine-tuned models",
                    "Compliance frameworks relevant to enterprise AI (SOC 2, GDPR, HIPAA) at a systems level",
                ],
            },
            {
                "file": "04-sso-permissions-and-rag-acl-enforcement.md",
                "title": "SSO, Permissions & RAG ACL Enforcement",
                "flagship": False,
                "synopsis": (
                    "The hard enterprise-RAG problem — making sure retrieval never "
                    "surfaces a document the requesting user isn't permitted to "
                    "see — and the architectural patterns that enforce this at "
                    "retrieval time, not just at the UI layer."
                ),
                "outline": [
                    "Why permission checks must happen at retrieval time, not display time",
                    "Document-level ACL syncing from source systems",
                    "Permission-aware indexing vs post-retrieval filtering",
                    "Performance cost of ACL enforcement at retrieval scale",
                ],
            },
        ],
    },
    {
        "dir": "23-staff-level-architecture",
        "title": "Staff-Level Architecture",
        "kind": "chapter",
        "intro": (
            "The recurring decisions that define Staff-level AI engineering work "
            "— not how to implement a pattern, but how to decide which pattern, "
            "and how to defend that decision in a design review."
        ),
        "entries": [
            {
                "file": "01-how-staff-engineers-think.md",
                "title": "How Staff Engineers Think",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "02-build-vs-buy.md",
                "title": "Build vs Buy",
                "flagship": False,
                "synopsis": (
                    "A decision framework for build-vs-buy across the AI stack — "
                    "model, retrieval, orchestration, evaluation — weighing "
                    "differentiation, talent cost, and time-to-market against "
                    "vendor lock-in and margin."
                ),
                "outline": [
                    "Layers where buying is almost always right (commodity infra)",
                    "Layers where building is a genuine differentiator",
                    "Total cost of ownership beyond the sticker price",
                    "A worked example decision",
                ],
            },
            {
                "file": "03-open-source-vs-closed-models.md",
                "title": "Open Source vs Closed Models",
                "flagship": False,
                "synopsis": (
                    "How a Staff Engineer weighs open-weight models against "
                    "closed/API models on cost, data control, customization, and "
                    "operational burden — and why the answer is usually \"both, "
                    "tiered.\""
                ),
                "outline": [
                    "Cost crossover point: API spend vs self-hosting cost",
                    "Data control and compliance drivers toward open weights",
                    "Customization (fine-tuning) flexibility",
                    "Operational burden of self-hosting at the frontier",
                ],
            },
            {
                "file": "04-fine-tuning-vs-rag.md",
                "title": "Fine-Tuning vs RAG",
                "flagship": False,
                "synopsis": (
                    "The single most common architectural fork in applied AI — "
                    "when fine-tuning beats RAG, when RAG beats fine-tuning, and "
                    "why most production systems eventually use both for "
                    "different jobs."
                ),
                "outline": [
                    "What fine-tuning is actually good at (style, format, latent skill) vs bad at (fresh facts)",
                    "What RAG is actually good at (fresh, citable facts) vs bad at (deep behavior change)",
                    "Cost and iteration-speed comparison",
                    "Combined architectures",
                ],
            },
            {
                "file": "05-single-agent-vs-multi-agent.md",
                "title": "Single-Agent vs Multi-Agent",
                "flagship": False,
                "synopsis": (
                    "Why multi-agent systems are not \"free parallelism\" — the "
                    "coordination tax, cost multiplication, and debugging "
                    "difficulty that mean a single well-scoped agent beats a "
                    "multi-agent system more often than the hype suggests."
                ),
                "outline": [
                    "The coordination tax: communication overhead, redundant work",
                    "Cost multiplication (N agents, N times the tokens)",
                    "When parallel sub-agents genuinely help (independent, parallelizable sub-tasks)",
                    "A decision checklist",
                ],
            },
            {
                "file": "06-multi-tenant-architecture.md",
                "title": "Multi-Tenant Architecture",
                "flagship": False,
                "synopsis": (
                    "Staff-level tradeoffs in multi-tenant AI platform design — "
                    "isolation vs cost efficiency, per-tenant customization vs "
                    "operational simplicity — extending the Enterprise AI chapter "
                    "with the \"how do I decide\" framing."
                ),
                "outline": [
                    "Isolation-cost tradeoff curve",
                    "Per-tenant customization without per-tenant maintenance burden",
                    "Capacity planning across tenants with different usage patterns",
                    "Migration paths from shared to dedicated as a tenant grows",
                ],
            },
            {
                "file": "07-cost-engineering.md",
                "title": "Cost Engineering",
                "flagship": False,
                "synopsis": (
                    "Systematically treating AI cost as an engineering problem "
                    "with levers (caching, routing, batching, model tiering) "
                    "rather than a finance problem solved by negotiating vendor "
                    "discounts."
                ),
                "outline": [
                    "The cost levers, ranked by typical impact",
                    "Prompt caching and its effect on margin",
                    "Model routing/tiering as the highest-leverage lever",
                    "Building a cost dashboard a team will actually look at",
                ],
            },
            {
                "file": "08-latency-engineering.md",
                "title": "Latency Engineering",
                "flagship": False,
                "synopsis": (
                    "Where latency actually accumulates in an AI request "
                    "(network, queueing, prefill, decode, tool calls) and the "
                    "engineering levers — streaming, speculative decoding, "
                    "caching, parallelization — for each segment."
                ),
                "outline": [
                    "Latency budget breakdown across a typical request",
                    "Streaming as a perceived-latency lever",
                    "Prefill vs decode latency and the levers for each",
                    "Parallelizing independent sub-calls (retrieval, tool calls)",
                ],
            },
            {
                "file": "09-reliability-engineering.md",
                "title": "Reliability Engineering",
                "flagship": False,
                "synopsis": (
                    "SLOs for a system with a probabilistic core — what "
                    "\"available\" and \"correct\" mean when the model itself is "
                    "a dependency with its own failure modes, rate limits, and "
                    "silent quality regressions."
                ),
                "outline": [
                    "Defining SLOs when correctness is graded, not binary",
                    "Provider failure handling: timeouts, retries, fallback models",
                    "Blast radius containment for a single bad model/prompt version",
                    "Chaos-testing an AI system (provider outage, rate-limit, latency spike)",
                ],
            },
            {
                "file": "10-ai-governance-and-platform-strategy.md",
                "title": "AI Governance & Platform Strategy",
                "flagship": False,
                "synopsis": (
                    "How Staff Engineers design the internal platform (shared "
                    "infra, guardrails, golden paths) that lets many product "
                    "teams ship AI features safely without each one re-solving "
                    "security, cost, and eval from scratch."
                ),
                "outline": [
                    "The platform-vs-product-team boundary",
                    "Golden paths: paved roads that make the safe choice the easy choice",
                    "Central governance (model approval, security review) vs team autonomy",
                    "Measuring platform success (adoption, incident rate, time-to-ship)",
                ],
            },
        ],
    },
    {
        "dir": "24-interview-prep",
        "title": "Interview Prep",
        "kind": "chapter",
        "intro": (
            "How AI system design interviews actually run, the framework for "
            "structuring your 45-60 minutes, and the mistakes that separate "
            "Senior from Staff answers."
        ),
        "entries": [
            {
                "file": "01-how-ai-system-design-interviews-work.md",
                "title": "How AI System Design Interviews Work",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "02-the-whiteboarding-framework.md",
                "title": "The Whiteboarding Framework",
                "flagship": False,
                "synopsis": (
                    "A repeatable framework for structuring 45-60 minutes of AI "
                    "system design whiteboarding — requirements, capacity "
                    "estimation, high-level design, deep dive, tradeoffs — and the "
                    "time allocation that keeps you from running out of clock."
                ),
                "outline": [
                    "Time-boxing each phase of the interview",
                    "Requirements-gathering questions that signal seniority",
                    "When to go high-level vs when to go deep",
                    "Recovering when you've gone down the wrong path",
                ],
            },
            {
                "file": "03-estimation-and-capacity-planning-drills.md",
                "title": "Estimation & Capacity Planning Drills",
                "flagship": False,
                "synopsis": (
                    "Worked practice problems for the back-of-envelope math "
                    "interviewers expect — QPS, token throughput, GPU counts, "
                    "storage — with the assumptions made explicit so you can "
                    "defend your numbers."
                ),
                "outline": [
                    "A library of worked estimation problems",
                    "Common assumption values to memorize (tokens/word, GPU throughput ranges)",
                    "How interviewers actually grade estimation (process over precision)",
                    "Practice drills with answers",
                ],
            },
            {
                "file": "04-company-specific-focus-areas.md",
                "title": "Company-Specific Focus Areas",
                "flagship": False,
                "synopsis": (
                    "What Google, OpenAI, Anthropic, Meta, Amazon, Uber, Stripe, "
                    "Glean, Cursor, and Perplexity each tend to emphasize in an AI "
                    "system design round, based on their product surface and "
                    "public engineering culture."
                ),
                "outline": [
                    "Infra-heavy companies vs product-heavy companies as a spectrum",
                    "What each company's product surface implies about likely case studies",
                    "Adjusting your depth allocation by company",
                    "Caveats: this is a heuristic, not a guarantee",
                ],
            },
            {
                "file": "05-common-mistakes-and-red-flags.md",
                "title": "Common Mistakes & Red Flags",
                "flagship": False,
                "synopsis": (
                    "The recurring mistakes that separate a Senior-level answer "
                    "from a Staff-level answer in AI system design interviews — "
                    "and the subtler red flags that fail otherwise-strong "
                    "candidates."
                ),
                "outline": [
                    "Designing for scale before establishing requirements",
                    "Treating the model as a black box with no failure modes",
                    "No mention of evaluation, cost, or security unless prompted",
                    "Going deep on the model and shallow on everything else",
                ],
            },
        ],
    },
    {
        "dir": "25-case-studies",
        "title": "Case Studies",
        "kind": "case_study",
        "intro": (
            "Twenty complete system designs for real AI products, each following "
            "the same 16-part format: Requirements through Interview Discussion. "
            "Use these as worked examples, not just reading material — try "
            "designing each one yourself before reading the chapter."
        ),
        "entries": [
            {
                "file": "01-chatgpt.md",
                "title": "ChatGPT",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "02-claude.md",
                "title": "Claude",
                "flagship": False,
                "synopsis": (
                    "How Anthropic's assistant architecture compares to ChatGPT's "
                    "at the system level — a long-context-first design "
                    "philosophy, Artifacts as a distinct product surface, and "
                    "Constitutional AI as an architectural layer, not a bolt-on."
                ),
                "outline": [
                    "Long-context-first design vs aggressive RAG reliance",
                    "Artifacts and structured-output as a first-class product surface",
                    "Safety/alignment layer as an architectural component",
                    "Contrast with the ChatGPT case study's architecture choices",
                ],
            },
            {
                "file": "03-gemini.md",
                "title": "Gemini",
                "flagship": False,
                "synopsis": (
                    "How native multimodality (text, image, video, audio in one "
                    "model) and deep integration with Google's existing "
                    "infrastructure (Search, Workspace) shape Gemini's system "
                    "architecture differently from text-first assistants."
                ),
                "outline": [
                    "Native multimodal architecture vs bolt-on modality adapters",
                    "Integration surface with Search/Workspace as a retrieval and distribution advantage",
                    "Serving infrastructure leverage (TPUs) as a cost/scale lever",
                    "Tradeoffs of a unified model across many product surfaces",
                ],
            },
            {
                "file": "04-perplexity.md",
                "title": "Perplexity",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "05-cursor.md",
                "title": "Cursor",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "06-github-copilot.md",
                "title": "GitHub Copilot",
                "flagship": False,
                "synopsis": (
                    "The system design of an in-IDE code-completion and chat "
                    "product — extremely tight latency budgets for inline "
                    "completion, repository-aware context construction, and a "
                    "usage pattern fundamentally different from chat-based coding "
                    "agents."
                ),
                "outline": [
                    "Inline completion latency budget (sub-second) vs chat latency budget",
                    "Repository/file context construction without a full agent loop",
                    "Telemetry-driven ranking of completions",
                    "Contrast with Cursor's more agentic architecture",
                ],
            },
            {
                "file": "07-deep-research-agent.md",
                "title": "Deep Research Agent",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "08-enterprise-rag-platform.md",
                "title": "Enterprise RAG Platform",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
            {
                "file": "09-ai-customer-support-platform.md",
                "title": "AI Customer Support Platform",
                "flagship": False,
                "synopsis": (
                    "A generic support-automation architecture — intent "
                    "classification, knowledge-base RAG, escalation-to-human "
                    "handoff, and the resolution-rate/cost tradeoff that defines "
                    "this product category."
                ),
                "outline": [
                    "Deflection rate vs resolution quality as the core business metric",
                    "Knowledge-base RAG with confidence-gated escalation",
                    "Human handoff as a first-class flow, not a failure path",
                    "Multi-channel (chat/email/voice) architecture differences",
                ],
            },
            {
                "file": "10-ai-coding-agent.md",
                "title": "AI Coding Agent",
                "flagship": False,
                "synopsis": (
                    "The generic architecture of an autonomous coding agent "
                    "(distinct from IDE-embedded products) — sandboxed execution, "
                    "test-driven verification loops, and multi-file change "
                    "planning."
                ),
                "outline": [
                    "Sandboxed code execution as a required safety boundary",
                    "Test-driven self-verification before presenting a change",
                    "Multi-file/repository-scale context and change planning",
                    "Where this overlaps with and differs from Cursor and Copilot",
                ],
            },
            {
                "file": "11-ai-voice-agent.md",
                "title": "AI Voice Agent",
                "flagship": False,
                "synopsis": (
                    "The added real-time constraints of a voice interface — "
                    "ASR/TTS pipeline latency, barge-in/interruption handling, and "
                    "turn-taking — layered on top of a standard agent "
                    "architecture."
                ),
                "outline": [
                    "End-to-end latency budget (ASR -> LLM -> TTS) under roughly one second",
                    "Streaming ASR/TTS and partial-result handling",
                    "Barge-in and interruption handling",
                    "Telephony/real-time infrastructure (WebRTC/SIP) considerations",
                ],
            },
            {
                "file": "12-ai-tutor.md",
                "title": "AI Tutor",
                "flagship": False,
                "synopsis": (
                    "An education-focused architecture where pedagogical state "
                    "(what the student knows, where they're stuck) matters as "
                    "much as retrieval — mastery tracking, Socratic-style response "
                    "design, and curriculum-aware sequencing."
                ),
                "outline": [
                    "Student mastery/knowledge-state modeling",
                    "Socratic response design vs answer-giving (a product/safety decision)",
                    "Curriculum-aware content sequencing and retrieval",
                    "Evaluation: learning outcomes, not just answer correctness",
                ],
            },
            {
                "file": "13-ai-healthcare-assistant.md",
                "title": "AI Healthcare Assistant",
                "flagship": False,
                "synopsis": (
                    "A high-stakes vertical architecture where guardrails, "
                    "human-in-the-loop escalation, and regulatory compliance "
                    "(HIPAA-level data handling) dominate the design more than raw "
                    "model capability."
                ),
                "outline": [
                    "Strict scope boundaries (information vs diagnosis) as an architectural constraint",
                    "Mandatory human-in-the-loop for high-risk outputs",
                    "PHI handling and compliance-driven data architecture",
                    "Liability-aware design: audit trails and disclaimers as system requirements",
                ],
            },
            {
                "file": "14-ai-meeting-assistant.md",
                "title": "AI Meeting Assistant",
                "flagship": False,
                "synopsis": (
                    "The pipeline from real-time audio to structured, actionable "
                    "output — streaming transcription, speaker diarization, and "
                    "summarization/action-item extraction at meeting scale."
                ),
                "outline": [
                    "Streaming ASR and speaker diarization pipeline",
                    "Real-time vs post-meeting summarization tradeoffs",
                    "Action-item and decision extraction as structured output",
                    "Integration surface (calendar, task trackers) and data-retention sensitivity",
                ],
            },
            {
                "file": "15-ai-search-engine.md",
                "title": "AI Search Engine",
                "flagship": False,
                "synopsis": (
                    "A generic AI-native search architecture (distinct from the "
                    "Perplexity case study) covering the crawl/index/retrieve/"
                    "synthesize pipeline and how it differs from both classic web "
                    "search and pure RAG."
                ),
                "outline": [
                    "Crawl and freshness-aware indexing at web scale",
                    "Query understanding and retrieval fan-out",
                    "Answer synthesis with citation grounding",
                    "Ranking signals unique to AI-synthesized search results",
                ],
            },
            {
                "file": "16-multi-agent-research-system.md",
                "title": "Multi-Agent Research System",
                "flagship": False,
                "synopsis": (
                    "An orchestrator-worker architecture where a lead agent "
                    "decomposes a research question across parallel sub-agents, "
                    "each with isolated context, before synthesizing a final "
                    "report."
                ),
                "outline": [
                    "Orchestrator-worker decomposition of a research task",
                    "Parallel sub-agent context isolation and cost multiplication",
                    "Synthesis/aggregation of sub-agent findings into one coherent report",
                    "Failure handling when a sub-agent returns a low-quality result",
                ],
            },
            {
                "file": "17-autonomous-software-engineer.md",
                "title": "Autonomous Software Engineer",
                "flagship": False,
                "synopsis": (
                    "A long-horizon agent architecture for end-to-end software "
                    "tasks (issue to PR) — repository-scale planning, multi-step "
                    "execution with checkpoints, and CI feedback as part of the "
                    "agent's own loop."
                ),
                "outline": [
                    "Long-horizon planning across a multi-hour or multi-day task",
                    "CI/test feedback as a signal inside the agent loop, not just a final gate",
                    "Checkpointing and human review gates before merge",
                    "Failure containment for an agent with repository write access",
                ],
            },
            {
                "file": "18-ai-recruiter.md",
                "title": "AI Recruiter",
                "flagship": False,
                "synopsis": (
                    "An architecture for sourcing, screening, and scheduling at "
                    "hiring-funnel scale, with fairness/compliance constraints "
                    "(anti-discrimination law) shaping the design as much as "
                    "retrieval or matching quality."
                ),
                "outline": [
                    "Sourcing and resume-matching as a retrieval/ranking problem",
                    "Screening automation and required human-in-the-loop checkpoints",
                    "Fairness and anti-discrimination compliance as a hard architectural constraint",
                    "Scheduling/coordination integration surface",
                ],
            },
            {
                "file": "19-ai-sdr.md",
                "title": "AI SDR",
                "flagship": False,
                "synopsis": (
                    "An outbound-sales-automation architecture — lead enrichment, "
                    "personalized outreach generation, and reply-handling — where "
                    "deliverability and compliance (CAN-SPAM, opt-out) constrain "
                    "the system as much as generation quality."
                ),
                "outline": [
                    "Lead enrichment and retrieval from multiple data sources",
                    "Personalized outreach generation at scale without sounding templated",
                    "Reply classification and handoff to a human rep",
                    "Deliverability and opt-out/compliance constraints",
                ],
            },
            {
                "file": "20-glean-enterprise-search.md",
                "title": "Glean-Style Enterprise Search",
                "flagship": True,
                "synopsis": "",
                "outline": [],
            },
        ],
    },
]


def main():
    backlog = [
        "# Backlog\n\n",
        "Source of truth: `scripts/new_stub.py` (the `SECTIONS` list). "
        "Edit entries there and re-run the script rather than hand-editing "
        "this file — it is regenerated.\n\n",
        "## Status Legend\n\n",
        "- ✅ Flagship — full Staff-level depth, written\n",
        "- 📋 Stub — scaffolded with synopsis + outline, not yet expanded\n",
    ]
    total_flagship = 0
    total_stub = 0

    for section in SECTIONS:
        section_dir = os.path.join(DOCS, section["dir"])
        os.makedirs(section_dir, exist_ok=True)

        with open(os.path.join(section_dir, "index.md"), "w") as f:
            f.write(
                INDEX_TMPL.format(
                    title=section["title"],
                    intro=section["intro"],
                    rows=render_index_rows(section),
                )
            )

        backlog.append(f"\n## {section['title']} (`docs/{section['dir']}/`)\n\n")
        for e in section["entries"]:
            if e["flagship"]:
                total_flagship += 1
                backlog.append(f"- ✅ `{e['file']}` — {e['title']}\n")
                continue
            total_stub += 1
            backlog.append(f"- 📋 `{e['file']}` — {e['title']}\n")
            with open(os.path.join(section_dir, e["file"]), "w") as sf:
                sf.write(
                    STUB_TMPL.format(
                        title=e["title"],
                        synopsis=e["synopsis"],
                        kind_label=kind_label(section),
                        outline=render_outline(e["outline"]),
                        section_title=section["title"],
                    )
                )

    backlog.append(
        f"\n## Totals\n\n- {total_flagship} flagship chapters/case studies complete\n"
        f"- {total_stub} stubs remaining\n"
    )
    with open(os.path.join(ROOT, "BACKLOG.md"), "w") as f:
        f.writelines(backlog)

    print(
        f"Wrote {len(SECTIONS)} section indexes, {total_stub} stub files "
        f"(skipped {total_flagship} flagship files — write those directly). "
        f"BACKLOG.md updated."
    )


if __name__ == "__main__":
    main()
