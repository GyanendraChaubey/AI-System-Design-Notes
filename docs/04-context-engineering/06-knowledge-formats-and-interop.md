# Knowledge Formats & Interop (OKF)

## Overview

Everything discussed so far in this section — budgeting, compression, long-context vs. RAG — assumes the knowledge being assembled into context already exists in some consumable form. In practice it rarely does. Organizational knowledge sits in metadata catalogs with proprietary APIs, wikis, shared drives, code comments, runbooks, and people's heads. Before any budgeting or retrieval logic can run, someone has to solve a prior problem: what format does the knowledge itself live in, so that it can be authored once and consumed by any retriever, any agent framework, any model provider?

The **Open Knowledge Format (OKF)** is the most concrete recent attempt to answer that question. It isn't a context-engineering technique in the sense of budgeting or compression — it's the raw material and container those techniques operate on. This chapter covers what it is, where it came from, and where it fits relative to RAG, memory systems, and GraphRAG.

## Origin: From a Pattern to a Spec

In April 2026, Andrej Karpathy published a gist describing what he called the **"LLM Wiki" pattern**. The observation: standard RAG re-derives an answer from raw chunks on every query — the model "has to find and piece together the relevant fragments every time. Nothing is built up." His alternative: an LLM agent incrementally builds and maintains a persistent markdown wiki that sits between raw sources and the user, so knowledge compounds instead of being re-synthesized from scratch each time.

The pattern has three layers — raw sources (immutable), the wiki (LLM-maintained markdown), and a schema document (e.g., a `CLAUDE.md`) defining structure — and three operations: **ingest** (integrate new sources into existing pages, not just index them), **query** (search, synthesize with citations, file results back into the wiki), and **lint** (periodic health-check for contradictions, staleness, and orphaned pages).

On June 12, 2026, Google Cloud's Data Cloud team (Sam McVeety, Amir Hormati) formalized this pattern into an open, versioned specification — **OKF v0.1** — published at [`GoogleCloudPlatform/knowledge-catalog`](https://github.com/GoogleCloudPlatform/knowledge-catalog), and wired Google Cloud's Knowledge Catalog product to ingest and serve it. The gist-to-spec path matters: OKF didn't emerge from a standards committee, it emerged from a working pattern that a vendor then made portable and rigorous enough for other producers and consumers to interoperate around.

## What OKF Actually Specifies

OKF v0.1 represents knowledge as a directory of markdown files with YAML frontmatter. Two core units:

- **Concept** — a single markdown file describing one thing: a table, a metric, a playbook, an API endpoint, a business process. The concept ID is the file path minus `.md`.
- **Bundle** — a self-contained, hierarchical directory of concepts, the unit of distribution. Bundles can be shipped as tarballs, hosted in git, or mounted on any filesystem.

```
sales/
├── index.md
├── datasets/
│   └── orders_db.md
├── tables/
│   ├── orders.md
│   └── customers.md
└── metrics/
    └── weekly_active_users.md
```

A concept document:

```yaml
---
type: BigQuery Table
title: Orders
description: One row per completed customer order.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orders
tags: [sales, revenue]
timestamp: 2026-05-28T14:30:00Z
---
# Schema
| Column | Type | Description |
|--------|------|-------------|
| `order_id` | STRING | Globally unique order identifier. |
| `customer_id` | STRING | FK to [customers](/tables/customers.md). |
```

The design is deliberately minimal — **exactly one required field: `type`**. Everything else (`title`, `description`, `resource`, `tags`, `timestamp`, and any producer-defined keys) is recommended, not required. Two reserved filenames carry special meaning: `index.md` (an optional directory listing) and `log.md` (an append-only change history grouped by ISO date). Cross-links between concepts are plain markdown links — `/tables/customers.md` — which turns the directory into a graph of relationships richer than the parent/child structure the filesystem alone implies.

Conformance is intentionally loose. A bundle is valid if every non-reserved `.md` file has parseable frontmatter with a non-empty `type`. Consumers are explicitly required to tolerate missing optional fields, unknown `type` values, broken links, and absent `index.md` files — so partially generated agent output stays usable rather than getting rejected by a strict parser. The spec's own stated non-goals: it does not define a fixed taxonomy of concept types, does not prescribe storage or serving infrastructure, and does not replace domain-specific schemas — it references them instead.

## Why Not Just Use RAG, or a Graph Database?

This is the question worth being precise about, since it's easy to conflate OKF with things it isn't.

**OKF vs. RAG.** These aren't competitors — OKF is upstream of RAG. RAG solves *retrieval*: given a corpus, find the right chunks for a query. OKF solves *organization*: what shape should the corpus be in before retrieval even runs. A RAG pipeline can chunk and embed an OKF bundle exactly like it would any other markdown corpus; OKF just gives producers a shared convention so every RAG system doesn't reinvent how to represent a "table" or a "metric." The failure mode OKF targets is upstream of retrieval quality — it's the mess of incompatible source formats that makes building a retrieval pipeline over internal knowledge expensive in the first place.

**OKF vs. GraphRAG.** OKF's markdown links do form a graph — concepts as nodes, links as directed edges — but it's a much lighter structure than what [GraphRAG](../07-graphrag/02-knowledge-graph-construction.md) builds. GraphRAG typically involves LLM-driven entity/relation extraction into a real graph database, with typed edges, community detection, and graph-algorithm-driven multi-hop retrieval. OKF has none of that machinery — no entity resolution, no typed relationships, no query language, no embeddings on edges. It's closer to a wiki's link structure than a constructed knowledge graph. The realistic relationship: an OKF bundle is a plausible **source format** that a GraphRAG ingestion pipeline could parse and formalize into an actual graph — not a substitute for one.

**OKF vs. a memory system.** [Memory architectures for agents](../12-memory-systems/01-memory-architecture-for-agents.md) are about what an individual agent accumulates and forgets across a session or across time — episodic, working, long-term memory tied to one agent's lifecycle. OKF is organization-wide and producer/consumer-agnostic: it's written once by humans, pipelines, or agents, and read by any number of unrelated consumers. Karpathy's original LLM Wiki pattern is arguably closer to an agent memory system (one agent maintaining its own wiki); OKF generalizes that into a distribution format meant to be shared across systems that didn't write it.

## Producer and Consumer Independence

A design principle stated directly in the spec, and probably the most consequential one for system design: OKF cleanly separates who writes knowledge from who reads it, and requires neither side to depend on a specific vendor.

Producers can be humans authoring by hand, agents built on any framework (Google ADK, LangChain, a custom loop), export pipelines from existing catalogs (Dataplex, Unity Catalog, Collibra), or a script walking a database schema. Consumers can be a static file server, a knowledge-management UI (Obsidian, Notion, MkDocs), an LLM loading files directly into context, a search index, or a graph viewer. Because the contract is "valid markdown + frontmatter with a `type`," a producer never needs to know what will consume its output, and a consumer never needs a bespoke integration per producer — the format itself is the integration surface, the same role a wire protocol or an API schema plays elsewhere in a system.

Google shipped reference tooling alongside the spec: a BigQuery enrichment agent that auto-generates OKF bundles from live datasets, a static HTML graph visualizer with no backend, and sample bundles (GA4 e-commerce, Stack Overflow, Bitcoin datasets) at [`okf/samples`](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf/samples).

## Security Consideration

OKF bundles are exactly the kind of untrusted content the [context engineering security model](01-what-is-context-engineering.md#security) already warns about: retrieved chunks and tool outputs are data, not instructions, regardless of formatting. An OKF concept file authored by an external producer — a vendor's export pipeline, a partner's shared bundle — carries the same indirect-prompt-injection risk as any other document an agent ingests into context. The spec's permissiveness (tolerate unknown fields, don't reject malformed bundles) is good for interoperability and bad for this risk in isolation: a consuming agent must still apply the same delimiter discipline and trust boundary to OKF content as to any other retrieved source, rather than treating "it's in a recognized format" as a reason to trust it more.

## Adoption Status

OKF v0.1 is new — published June 2026, explicitly framed by its authors as "a starting point, not a finished standard." There is no independent benchmark data yet on retrieval quality or adoption breadth outside Google Cloud's own Knowledge Catalog integration; claims about its trajectory (some early commentary compares it to how APIs or databases became foundational infrastructure) are opinion, not established fact. Worth tracking, not yet worth treating as settled industry practice.

## Sources

- [OKF Specification (SPEC.md)](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- [How the Open Knowledge Format can improve data sharing — Google Cloud Blog](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/)
- [Karpathy's original LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [OKF sample bundles](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf/samples)

## Related

- [What Is Context Engineering](01-what-is-context-engineering.md) — where OKF bundles fit as one possible source feeding the assembly layer.
- [RAG Architecture](../06-rag/01-rag-architecture.md) — the retrieval layer OKF is upstream of, not a replacement for.
- [Knowledge Graph Construction](../07-graphrag/02-knowledge-graph-construction.md) — the heavier machinery OKF's link-graph is sometimes mistaken for.
- [Memory Architecture for Agents](../12-memory-systems/01-memory-architecture-for-agents.md) — single-agent memory vs. OKF's org-wide, producer/consumer-agnostic scope.
- [Knowledge Base Lifecycle Management](../05-retrieval-systems/06-knowledge-base-lifecycle-management.md) — operational concerns (freshness, dedup, versioning) that apply to OKF bundles once they're being served in production.
