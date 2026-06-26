# Cursor — System Design Case Study

## Requirements

**Functional**
- **Inline completion ("Tab")**: as a developer types, suggest single-line and multi-line code completions inline in the editor, accepted with a keystroke.
- **Chat with the codebase**: a conversational panel that can answer questions and propose changes grounded in the open repository, not just the open file.
- **Agent mode**: given a natural-language task ("add pagination to this endpoint and update the tests"), autonomously plan and execute a multi-file change — read files, write edits, run terminal commands (build, test, lint), observe the output, and iterate until the task converges or a budget is hit.
- **Codebase-aware context**: completions and chat answers should reflect symbols, types, and patterns defined elsewhere in the repository, not only the text visible in the current buffer.
- **Support for very large repositories**: monorepos with hundreds of thousands of files; indexing and retrieval must not require reading the whole repo into context per request.
- **Local-first editing semantics**: the working tree is the source of truth and changes constantly (saves, branch switches, external edits); the product must reconcile its index against that continuously, not against a stable snapshot.

**Non-functional**
- **Inline completion latency**: the dominant non-functional constraint of the entire product. Time-to-suggestion needs to land well under a second — ideally 100-300ms — because anything slower is perceived as the editor "lagging" rather than "thinking," and a slow suggestion that arrives after the developer has kept typing is worse than no suggestion at all.
- **Agent-mode latency is a completely different budget**: tens of seconds to several minutes per session is acceptable and expected, because the unit of work is "implement a feature," not "predict the next token."
- **High completion-acceptance precision over recall**: a wrong but fast suggestion that's easy to ignore is fine; a wrong agent-mode edit that silently corrupts code is not — review-ability of multi-file diffs is a hard requirement.
- **Sandboxed execution**: any terminal command or file write the agent performs must be contained — it cannot have implicit access to the developer's full machine, credentials, or network by default.
- **Reversibility**: every agent-mode change must be inspectable and revertible before or after it lands, since the product is editing a developer's actual source of truth, not a sandboxed copy.
- **Index freshness against a fast-changing local tree**: the codebase index cannot drift far behind the developer's actual edits without degrading both completion and agent quality.

**Explicitly out of scope for this case study**: training or fine-tuning the underlying foundation models (a separate ML research system, see [Transformer Internals for Systems Engineers](../02-llm-architecture/01-transformer-internals-for-systems-engineers.md)), the editor's non-AI IDE features (syntax highlighting, debugging, version control UI), and team/enterprise billing infrastructure.

## Capacity Planning

The single most important framing for this product is that **two workloads with wildly different cost-per-request share one product**, so capacity has to be planned separately for each and then combined, following the method in [GPU Sizing & Capacity Planning](../16-gpu-systems/02-gpu-sizing-and-capacity-planning.md). All figures below are illustrative, order-of-magnitude assumptions, not reported usage numbers.

**Inline completion (Tab)**

| Step | Assumption | Result |
|---|---|---|
| Active developers | 1M daily active developers | 1M DAU |
| Active coding time | ~4 hours of actual editing per developer per day | — |
| Completion-trigger rate | A completion is requested roughly every 2-4 keystrokes of meaningful typing — call it once every 4 seconds of active typing, conservatively | ~3,600 requests/hour-of-coding per developer |
| Completions/developer/day | 4 hours active coding × 900 requests/hour | ~3,600 completion requests/developer/day |
| Total completion requests/day | 1M developers × 3,600 | ~3.6B completion requests/day |
| Average QPS | 3.6B / 86,400s | ~42,000 QPS average |
| Peak-to-average ratio | Developer activity concentrates heavily in business hours across a handful of overlapping time zones — sharper peaking than consumer chat | ~3-4x | 
| Peak QPS | ~42,000 × 3.5 | ~150,000 QPS peak |
| Tokens per completion request | Small: ~200-400 input tokens (local context window) and ~20-40 output tokens (a short completion) | ~250 input / 30 output tokens avg |
| Peak token throughput | 150,000 QPS × (250 in + 30 out) | ~37M input tok/s, ~4.5M output tok/s at peak |

**Agent-mode sessions**

| Step | Assumption | Result |
|---|---|---|
| Fraction of developers using agent mode daily | ~15% of DAU | 150,000 developers/day |
| Sessions per developer/day | ~2 agent-mode tasks/day | ~300,000 sessions/day |
| Average session QPS | 300,000 / 86,400s | ~3.5 sessions/sec average — roughly **four orders of magnitude lower** than completion QPS |
| Tokens per session | Repo-scale context retrieval, multi-step plan, several tool calls with file contents and test/build output round-tripped through the model — easily 50K-300K input tokens and 5K-20K output tokens accumulated over the session (the agent loop's resent-history effect, see [Agent Fundamentals & the Agent Loop](../09-agents/01-agent-fundamentals-and-the-agent-loop.md)) | ~150K input / ~10K output tokens/session, illustrative midpoint |
| Total daily agent tokens | 300,000 sessions × 160K tokens | ~48B tokens/day from agent mode alone |
| Comparable daily completion tokens | 3.6B requests × 280 tokens | ~1T tokens/day from completion |

The arithmetic is the whole point of this section: **completion is a request-rate problem and agent mode is a per-session cost problem.** Completion QPS is four to five orders of magnitude higher than agent-session QPS, but completion's per-request token cost is three orders of magnitude lower than a single agent session's. The two workloads cannot be sized off the same dial — a fleet provisioned for completion's QPS profile (many cheap, fast, small-batch requests at a tight p99 latency SLO) looks nothing like a fleet provisioned for agent mode's profile (far fewer requests, much larger context windows, tool-call round trips, tolerant of multi-second per-step latency). This is also why the two paths use different model tiers (see Model Layer below) — running every Tab keystroke through an agent-capable model would be both far too slow and roughly 100-1000x more expensive per request than the workload justifies.

## Scale Estimation

- **Codebase index size**: a mid-size repository (~50K files, ~10M lines) produces, at a typical chunking granularity of ~50-100 lines per chunk, on the order of 150K-300K embeddable chunks. At ~1.5KB per dense vector (a few hundred float dimensions) plus metadata, that's roughly 200-500MB of vector index per repository — trivial per-repo, but multiplied across millions of indexed repositories (most privately hosted, many with multiple branches checked out locally) the aggregate index storage is in the tens of petabytes range industry-wide, and crucially must be partitioned per-repo/per-tenant, never pooled into one shared global index.
- **Re-indexing churn**: a developer actively editing generates file-save events continuously — assume one meaningful save every 30-60 seconds of active editing. Across 1M DAU at 4 active hours/day, that's tens of millions of incremental re-index events per day, each touching a small delta (one or a few files), not a full repo re-embed — full re-embeds must stay rare (initial clone/index, or large branch switches) or the indexing pipeline itself becomes the bottleneck.
- **Symbol/lexical index**: a parsed symbol table (functions, classes, identifiers, call graph) for a 10M-line repo is on the order of low hundreds of MBs — much smaller than the embedding index, and far cheaper to keep perfectly fresh on every keystroke, which matters because exact-identifier lookups are latency-critical for completion (see Retrieval Layer).
- **Agent-mode session storage**: a single session's trajectory (every tool call, file read/write, test/build output) can run into hundreds of KB to a few MB of logged transcript; at 300,000 sessions/day that's on the order of hundreds of GB/day of trajectory data if retained in full — a meaningful storage line item, and one of the highest-value sources for offline eval and regression detection.
- **Fan-out**: a single agent-mode task commonly fans out into 5-30 tool calls (file reads, an edit, a test run, a re-read after the test fails, another edit...) before completing — so agent-mode's effective backend load (file I/O, sandboxed process execution, retrieval calls) is 1-2 orders of magnitude higher than its already-low session count alone would suggest, even though it remains nowhere near completion's raw QPS.

## High Level Design

```mermaid
flowchart TB
    DEV[Developer in Editor] --> ROUTE{Request type}

    ROUTE -->|Keystroke| FASTPATH[Inline Completion Path]
    FASTPATH --> LOCALCTX[Local Context Gatherer:\ncurrent file, cursor position,\nnearby symbols]
    LOCALCTX --> SMALLMODEL[Fast/Small Completion Model]
    SMALLMODEL --> SUGGEST[Inline Suggestion\n<1s budget]
    SUGGEST --> DEV

    ROUTE -->|Chat / Agent task| AGENTPATH[Agent-Mode Path]
    AGENTPATH --> RETRIEVE[Repo-Scale Retrieval:\nembedding + symbol/lexical search]
    RETRIEVE --> ORCH[Agent Orchestrator / Loop]
    ORCH --> BIGMODEL[Larger Reasoning Model]
    BIGMODEL --> TOOLS{Tool call?}
    TOOLS -->|Edit file| SANDBOX[Sandboxed Workspace:\nfile write, terminal exec]
    TOOLS -->|Run tests/build| SANDBOX
    SANDBOX --> ORCH
    TOOLS -->|Done| DIFF[Multi-file Diff for Review]
    DIFF --> DEV

    INDEX[(Codebase Index:\nembeddings + symbols)] --> LOCALCTX
    INDEX --> RETRIEVE
    DEV -.->|file saves, edits| INDEXER[Incremental Indexer]
    INDEXER --> INDEX
```

## Detailed Design

```mermaid
flowchart TB
    subgraph Editor["Editor Client"]
        KEYSTROKE[Keystroke Event] --> DEBOUNCE[Debounce/Trigger Logic]
        CHATIN[Chat/Agent Task Input]
    end

    subgraph Indexing["Codebase Indexing Pipeline"]
        WATCH[File Watcher] --> DIFF_DET[Diff Detector:\nchanged regions only]
        DIFF_DET --> PARSE[AST/Symbol Parser]
        DIFF_DET --> CHUNK[Chunker]
        CHUNK --> EMBED[Embedding Service]
        PARSE --> SYMDB[(Symbol/Lexical Index)]
        EMBED --> VECDB[(Vector Index, per-repo)]
    end

    subgraph FastPath["Inline Completion Service"]
        DEBOUNCE --> LCTX[Local Context Builder:\nopen file + cursor window\n+ nearby symbol lookups]
        SYMDB -.->|fast exact lookup| LCTX
        LCTX --> CBUDGET{Context ready\nwithin timeout?}
        CBUDGET -->|Yes| SMALLINFER[Small Model Inference\nlow-latency fleet]
        CBUDGET -->|No, timeout| SMALLINFER
        SMALLINFER --> RANK[Rank/filter candidates]
        RANK --> RETURN[Return suggestion]
    end

    subgraph AgentPath["Agent-Mode Service"]
        CHATIN --> HYBRID[Hybrid Retrieval:\nVECDB semantic + SYMDB lexical]
        VECDB -.-> HYBRID
        SYMDB -.-> HYBRID
        HYBRID --> PLAN[Planner: larger model]
        PLAN --> LOOP{Agent Loop}
        LOOP -->|edit| FSWRITE[Sandboxed File Writer]
        LOOP -->|exec| SHELLEXEC[Sandboxed Terminal/Process]
        FSWRITE --> OBSERVE[Observe: diff applied]
        SHELLEXEC --> OBSERVE2[Observe: test/build output]
        OBSERVE --> LOOP
        OBSERVE2 --> LOOP
        LOOP -->|budget hit or done| PRESENT[Present Multi-file Diff]
    end

    subgraph Shared["Shared Substrate"]
        VECDB
        SYMDB
        BUDGETMGR[Cost/Step Budget Manager]
        AUTH[Repo Access Control]
    end

    LOOP -.-> BUDGETMGR
    AUTH -.-> HYBRID
    AUTH -.-> LCTX

    subgraph Obs["Observability"]
        TRACE[(Per-request/per-session traces)]
        METER[(Token usage metering)]
    end

    SMALLINFER -.-> TRACE
    PLAN -.-> TRACE
    LOOP -.-> METER
```

## API Design

Two endpoints, deliberately shaped differently because their latency contracts are different.

**Completion endpoint — synchronous, low-latency**

```
POST /v1/completions
{
  "file_path": "src/api/users.ts",
  "prefix": "...code before cursor (truncated to local window)...",
  "suffix": "...code after cursor (truncated)...",
  "cursor_position": {"line": 142, "col": 18},
  "max_context_ms": 80   // hard budget for context gathering before inference must start
}

Response (target p50 < 200ms, p99 < 800ms):
{
  "suggestion": "  return users.filter(u => u.active);",
  "multiline": false,
  "context_used": ["local_file", "nearby_symbols"],  // what was actually gathered before the timeout
  "latency_ms": 134
}
```

The `context_used` field matters operationally: it lets the client and telemetry distinguish "answered fast with full context" from "answered fast because we gave up on retrieval early" — the two look identical in latency but very different in suggestion quality, and conflating them hides the tradeoff this product lives on.

**Agent-mode endpoint — asynchronous, streamed progress**

```
POST /v1/agent-sessions
{
  "task": "Add pagination to GET /users and update the existing tests.",
  "repo_id": "repo_abc123",
  "scope": {"paths": ["src/api/", "tests/"]},   // optional, narrows retrieval/edit scope
  "max_steps": 25,
  "max_cost_usd": 2.00
}

Response: a session id immediately, then a streamed event sequence —
  event: plan           data: {"steps": ["locate GET /users handler", "add limit/offset params", "update tests"]}
  event: tool_call       data: {"tool": "read_file", "path": "src/api/users.ts"}
  event: tool_result     data: {"tool": "read_file", "bytes": 4213}
  event: tool_call       data: {"tool": "edit_file", "path": "src/api/users.ts", "diff": "..."}
  event: tool_call       data: {"tool": "run_command", "cmd": "npm test -- users"}
  event: tool_result     data: {"tool": "run_command", "exit_code": 1, "output": "...assertion failed..."}
  event: tool_call       data: {"tool": "edit_file", "path": "tests/users.test.ts", "diff": "..."}
  event: tool_call       data: {"tool": "run_command", "cmd": "npm test -- users"}
  event: tool_result     data: {"tool": "run_command", "exit_code": 0}
  event: done            data: {"files_changed": 2, "steps_used": 6, "cost_usd": 0.18}
```

`max_steps` and `max_cost_usd` are accepted as client-supplied hints but enforced as hard ceilings server-side regardless of what the client requests — the same non-negotiable runtime enforcement described generally in [Agent Fundamentals & the Agent Loop](../09-agents/01-agent-fundamentals-and-the-agent-loop.md).

## Data Flow

The sequence diagram below traces the agent-mode path specifically, since it's the architecturally interesting one — the completion path is a single hop and is covered by its latency budget in Tradeoff Analysis instead.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Orch as Agent Orchestrator
    participant Ret as Hybrid Retrieval
    participant LLM as Reasoning Model
    participant Sbx as Sandbox (FS + Terminal)

    Dev->>Orch: "Add pagination to GET /users and update tests"
    Orch->>Ret: retrieve relevant files/symbols (+200-600ms)
    Ret-->>Orch: top-k chunks: handler file, route config, existing test file
    Orch->>LLM: plan given task + retrieved context (+1-3s)
    LLM-->>Orch: plan: edit handler, add params, update tests
    Orch->>LLM: step 1 observation
    LLM-->>Orch: action: read_file(users.ts)
    Orch->>Sbx: read_file(users.ts)
    Sbx-->>Orch: file contents (+50ms)
    Orch->>LLM: step 2 observation (+file contents)
    LLM-->>Orch: action: edit_file(users.ts, diff) (+2-5s)
    Orch->>Sbx: apply edit in sandboxed workspace
    Sbx-->>Orch: edit applied
    Orch->>LLM: step 3 observation
    LLM-->>Orch: action: run_command("npm test -- users")
    Orch->>Sbx: execute test command (sandboxed, no network/creds)
    Sbx-->>Orch: exit_code 1, assertion failure output (+2-10s, test runtime)
    Orch->>LLM: step 4 observation (+test failure output)
    LLM-->>Orch: action: edit_file(users.test.ts, diff) (+2-5s)
    Orch->>Sbx: apply edit
    Sbx-->>Orch: edit applied
    Orch->>LLM: step 5 observation
    LLM-->>Orch: action: run_command("npm test -- users")
    Orch->>Sbx: execute test command
    Sbx-->>Orch: exit_code 0 (+2-10s)
    Orch->>LLM: step 6 observation
    LLM-->>Orch: final: task complete, no further action
    Orch->>Orch: termination check: model done, under step/cost budget
    Orch-->>Dev: present multi-file diff for review (~15-30s total elapsed)
```

A handful of details generalize across most agent-mode sessions: retrieval happens once up front to seed the plan (not re-run every step, to control cost), each tool round-trip is dominated by either model thinking time (seconds) or actual test/build execution time (which can itself run into tens of seconds for a real test suite), and the developer sees nothing applied to their actual working tree until the final diff is presented — the sandbox, not the developer's live files, absorbs every intermediate edit and test run.

## Retrieval Layer

The retrieval layer is the substrate both paths share, and it has to satisfy two very different access patterns from the same index.

- **Embedding-based semantic search**: dense vector embeddings over chunked files, used for "find code conceptually related to this task" — useful for agent-mode planning ("where is rate limiting implemented?") and weak on exact-identifier recall, the classic dense-embedding failure mode covered in [Hybrid Search & Reranking](../05-retrieval-systems/04-hybrid-search-and-reranking.md).
- **Symbol/lexical search**: an exact-match index over identifiers, function/class definitions, imports, and call graphs, built from parsing (AST-level, not just text tokenization). This is what answers "where is `UserRepository.findById` defined and who calls it?" reliably — a query dense embeddings handle poorly, because two identifiers can be semantically similar in embedding space while being completely different symbols, and vice versa. Both inline completion (resolving a symbol referenced near the cursor) and agent mode (finding every call site before renaming a function) depend on this index being exact, not approximate.
- **Hybrid retrieval as the default, not an optimization**: production queries combine both — semantic search to find conceptually relevant regions of an unfamiliar part of the codebase, lexical/symbol search to pin down exact definitions and usages once a candidate area is identified, then a reranking pass over the combined candidate set. The general pattern is covered in depth in [Hybrid Search & Reranking](../05-retrieval-systems/04-hybrid-search-and-reranking.md); the code-specific addition is that the lexical side must be symbol-aware (parsed), not plain keyword search, or it inherits the same false-positive problems as generic full-text search on highly repetitive code (common variable names, boilerplate).
- **Incremental re-indexing**: re-embedding and re-parsing on every keystroke is infeasible at the QPS this product runs at — the indexer instead watches file-save events, diffs the changed region, and re-chunks/re-embeds/re-parses only the affected spans, propagating updates to the vector and symbol indexes asynchronously. The completion path's local-context gatherer does not wait on this propagation — it reads the live buffer directly for the current file and only consults the index for *other* files, which is what keeps completion latency decoupled from indexing latency.
- **Freshness against a fast-changing working tree is the layer's hardest problem**: unlike a server-side document corpus that changes on the order of minutes, a local working tree changes on every keystroke and can change wholesale on a branch switch or git pull. The practical resolution is a staleness tolerance, not a freshness guarantee: the open file and immediate neighbors are always read live (zero staleness), while the rest of the repo's index is allowed to lag by seconds, with full re-indexing reserved for large diffs (branch switches, merges) where incremental diffing isn't worth the bookkeeping overhead.

## Agent Layer

Agent mode is a direct application of the bounded [agent loop](../09-agents/01-agent-fundamentals-and-the-agent-loop.md): observe (task + retrieved context + prior tool results), think (planner model decides next action), act (execute a file edit or terminal command in the sandbox), observe the result, repeat until termination.

- **Plan**: an initial pass over retrieved context produces a rough multi-step plan ("locate handler, add params, update tests") before any edits happen — closer to plan-then-execute than pure ReAct, because code tasks usually decompose predictably enough to benefit from an upfront plan, with replanning triggered when a step's result (a failing test, an unexpected file structure) invalidates it.
- **Propose edit**: edits are generated as diffs against the current file content the agent actually read in this session, not as full-file rewrites — this keeps the blast radius of a single bad step small and makes the eventual presented diff reviewable.
- **Execute**: file writes and terminal commands run inside a sandboxed workspace (see Security Layer) — never directly against the developer's live working tree until the session completes and the developer accepts the result.
- **Observe**: test and build output is fed back into the next step's observation verbatim (truncated/summarized if very large) — a failing assertion or compiler error is the dominant signal the loop uses to decide whether to keep iterating.
- **Iterate or stop**: termination fires on the model signaling completion (tests pass, task addressed), a step-count ceiling, a cost ceiling, or wall-clock timeout — all enforced by the orchestrator runtime, not the model's self-report, per the same non-negotiable principle in [Agent Failure Modes & Guardrails](../09-agents/05-agent-failure-modes-and-guardrails.md).
- **Loop and cost budgets per session**: a typical session caps in the range of 15-30 steps and a small single-digit dollar cost ceiling — generous enough for a real multi-file task, bounded enough that a stuck or oscillating loop (the model re-running the same failing test without changing its hypothesis) cannot silently consume unbounded compute. Loop-detection (repeated identical action+argument pairs) is a forced-stop trigger independent of the step counter, for exactly the oscillation failure mode covered in that chapter.

## Model Layer

The product's defining model decision is running **two structurally different models behind two structurally different latency contracts**, not one model serving both paths at different "effort levels."

| | Inline completion | Agent mode |
|---|---|---|
| Latency budget | Sub-second (target 100-300ms) | Seconds to minutes per step, tens of seconds to minutes total |
| Model class | Small/distilled, optimized for fast single-token-stream generation over a short context window | Larger, stronger reasoning model, optimized for multi-step planning and tool-call correctness over a long, retrieval-augmented context |
| Context size | Hundreds of tokens (local file window + a few symbol lookups) | Tens to hundreds of thousands of tokens across a session (retrieved files, accumulated tool results) |
| Cost per request | Fractions of a cent | Cents to low dollars per session |
| Fallback behavior on overload | Serve a shorter/cheaper completion or skip the suggestion silently | Queue or degrade to a smaller model with an explicit "reduced capability" note, never silently drop a step mid-session |

The latency budget, not model capability preference, is what forces this split: even if a single large model could in principle produce a slightly better inline suggestion than a small distilled one, it cannot do so within the time the developer will tolerate before perceiving lag — so the completion path's model choice is dictated by the latency SLO first, quality second, while the agent path inverts that priority because its SLO is generous. This mirrors the fast-tier/reasoning-tier split described for chat products in [Multi-Model Serving & Routing](../15-model-serving/05-multi-model-serving-and-routing.md), with the key difference that here the two tiers aren't routed dynamically per-request based on difficulty — they're routed structurally based on which *feature* the developer invoked.

## Observability Layer

- **Completion latency histograms (p50/p95/p99) per stage**: context-gathering time vs. model inference time vs. network round-trip, tracked separately, because a regression in any one stage looks identical at the client ("suggestions feel slow") but requires a completely different fix.
- **Completion acceptance rate**: the leading product-quality signal for the fast path — a falling acceptance rate after a model or context-window change is the earliest sign of a quality regression, often before any latency metric moves.
- **Agent-session trajectories logged in full**: every observation, tool call, and result per session, mirroring the agent-loop best practice of trajectory-level logging rather than input/output-pair logging — essential for diagnosing why a session needed 25 steps instead of 6.
- **Termination-reason breakdown for agent sessions**: model-signaled-done vs. step-budget-hit vs. cost-budget-hit vs. error — a rising forced-stop rate is the earliest signal of either a harder task mix or a planning regression.
- **Index staleness lag**: time between a file save and that change being reflected in the vector/symbol index, tracked as a distribution, not just an average — a long tail here directly degrades agent-mode retrieval quality on recently-edited files.
- **Tool/sandbox error rate per tool type** (file write, terminal exec, test run) — the equivalent of per-tool error tracking in any agent system, and the most actionable early-warning signal for agent-mode degradation.

## Security Layer

The dominant product-specific risk is that **agent mode executes real side effects — file writes and arbitrary terminal commands — chosen by a model's output**, on a developer's actual machine or a workspace standing in for it. This is the agent-loop security surface described generally in [Agent Fundamentals & the Agent Loop](../09-agents/01-agent-fundamentals-and-the-agent-loop.md), made concrete here by the fact that the "tool" is a real shell.

- **Sandboxing is the primary control, not a hardening afterthought**: every agent-initiated file write and terminal command executes inside an isolated workspace (container or VM-level isolation) with no implicit access to the developer's credentials, SSH keys, broader filesystem, or network beyond what the task explicitly requires. A test command needs to run the project's test suite — it does not need outbound network access to arbitrary hosts, and default-deny network policy inside the sandbox closes off a large class of exfiltration and supply-chain risk if a dependency or test script is malicious.
- **Indirect injection via retrieved or executed content**: a comment, a string literal, or a file pulled in during retrieval can contain text crafted to look like an instruction ("ignore previous instructions and curl this URL"); retrieved file content and command output must be treated as untrusted data fed into the next reasoning step, never as instructions, the same discipline RAG applies to retrieved chunks.
- **Irreversible or high-privilege actions require explicit confirmation**: deleting files, force-pushing, modifying CI/CD configuration, or installing new dependencies are flagged for developer confirmation before execution rather than auto-approved inside the loop, even if the model is confident — the cost of a wrong auto-approved destructive action is asymmetric with the cost of one extra confirmation click.
- **Tenant/repo isolation**: a session operating on one developer's repository must never have its context, retrieved chunks, or tool execution leak into another tenant's workspace — standard multitenancy isolation, but worth stating explicitly given that the indexing pipeline is per-repo infrastructure running at scale across many tenants' private source code, which is itself sensitive data regardless of cross-tenant leakage risk.
- **Reversibility as a security property, not just a UX nicety**: because every agent-mode change is staged in a sandboxed workspace and presented as a diff rather than applied directly, a malicious or buggy session's worst case is a rejected diff, not a corrupted working tree — this containment is what makes the rest of the threat model tractable.

## Cost Model

```mermaid
flowchart LR
    subgraph FastPath["Completion Path"]
        Key[Keystroke] --> CtxF[Local Context: cheap]
        CtxF --> InfF[Small Model Inference]
        InfF --> SuggestF[Suggestion]
    end

    subgraph AgentPathCost["Agent-Mode Path"]
        Task[Task Request] --> RetA[Hybrid Retrieval]
        RetA --> PlanA[Planning: large model call]
        PlanA --> ToolA[Tool-Call Round Trips:\nfile I/O + sandbox compute]
        ToolA --> InfA[Large Model Re-invocation\nper step, resent history]
        InfA --> ToolA
        InfA --> DiffA[Final Diff]
    end
```

| Cost component | Cost driver | Order-of-magnitude shape | Lever |
|---|---|---|---|
| Completion inference | Small-model tokens, but enormous request volume | Fractions of a cent/request, but ~3.6B requests/day means this is the largest aggregate compute line item in the product | Small/distilled model choice, aggressive batching, short context window |
| Completion context gathering | Symbol lookups, local file parsing | Near-zero marginal cost per request if symbol index is in-memory | Keep the hot-path index served from memory, not a network round trip |
| Agent-mode inference | Large-model tokens, resent history compounding across steps (triangular growth, see [Agent Fundamentals & the Agent Loop](../09-agents/01-agent-fundamentals-and-the-agent-loop.md)) | Cents to low dollars per session, but only ~300K sessions/day | Step caps, history summarization between steps |
| Agent-mode retrieval | Embedding search + symbol search per session, run once upfront | Small relative to inference cost per session | Cache hot repos' retrieval results across nearby sessions in the same repo |
| Sandbox compute | Container/VM time for file I/O and command execution (test/build runs) | Can dominate wall-clock time per session even when it's cheap in $ terms | Reuse warm sandboxes per repo session rather than cold-starting a container per tool call |
| Indexing pipeline | Embedding + parsing cost amortized across incremental re-index events | Small per-event, but tens of millions of events/day in aggregate | Incremental diffing instead of full re-embeds; debounce rapid consecutive saves |

The single highest-leverage lever in this cost model cuts in opposite directions for the two paths: on the completion path, the lever is **keeping the small model small and the context window short**, because the workload's sheer volume means even tiny per-request savings compound into the dominant aggregate cost line; on the agent path, the lever is **capping steps and summarizing history**, because a single unconstrained session can cost orders of magnitude more than a typical one, the same unbounded-loop risk quantified generally in [Agent Fundamentals & the Agent Loop](../09-agents/01-agent-fundamentals-and-the-agent-loop.md).

## Failure Handling

| Failure | Degradation strategy |
|---|---|
| Completion model times out or is overloaded | Fail instantly and silently — show no suggestion rather than blocking the keystroke or showing a stale one; the editor must never feel like it's waiting on the network |
| Context gathering exceeds the timeout budget | Proceed to inference with whatever context was gathered so far (even just the local file) rather than waiting for the full retrieval to complete — a worse completion beats a late one |
| Agent-mode tool call (test/build) fails | Feed the failure output back into the loop as an observation so the model can revise its approach — this is expected, routine signal, not an error state |
| Agent-mode loop oscillates (repeats the same failing fix) | Loop-detection on repeated identical action+argument pairs forces a stop rather than burning the full step/cost budget unproductively |
| Agent-mode step or cost budget exhausted | Force-stop and present the best-effort partial diff plus an explicit "stopped: budget exceeded" reason — never discard partial progress |
| Sandbox crashes or becomes unresponsive mid-session | Treat as a tool error fed back to the model if recoverable; otherwise terminate the session and surface a clear error rather than silently dropping in-flight edits |
| Index lagging behind a recent edit | Retrieval falls back to a live read of the open/recently-touched files rather than serving stale indexed content for those specific files |
| Developer rejects the presented multi-file diff | Full rollback is trivial because nothing was applied to the real working tree during the session — the sandboxed diff staging from the Security Layer is what makes this cheap |

## Tradeoff Analysis

```mermaid
flowchart TD
    Q1{Is more context available\nwithin the latency budget\nremaining?} -->|Yes, cheap local lookup| GATHER[Gather it: nearby symbols,\nopen tabs, recent edits]
    GATHER --> Q1
    Q1 -->|No more time left| Q2{Has the hard timeout\nbeen reached?}
    Q2 -->|No| Q3{Is current context\nsufficient for a\nreasonable completion?}
    Q3 -->|Yes| SERVE[Serve completion now]
    Q3 -->|No, but still time left| GATHER
    Q2 -->|Yes, timeout hit| FORCESERVE[Serve best-effort completion\nwith whatever context exists,\nor serve nothing]
```

The central architectural fork in this product is the **inline-completion latency/context tradeoff**: more retrieved context (cross-file symbol resolution, related function definitions, recently edited regions) measurably improves completion quality, but every millisecond spent gathering it is subtracted directly from a sub-second budget the user will not tolerate exceeding. Unlike agent mode, where more retrieval is close to free relative to the overall session budget, the completion path cannot simply "retrieve more" as a default — it has to decide, per request, how much context-gathering it can afford before timing out and serving whatever it has. Production systems resolve this with a hard context-gathering deadline (a strict timeout, not a soft target) that the local-context builder must respect: cheap, in-memory lookups (current file, immediately adjacent symbols already resolved) are attempted first and almost always complete in budget; more expensive lookups (cross-file semantic search) are attempted opportunistically and simply dropped if the deadline arrives first, rather than being allowed to delay the response. The product accepts that this means some completions are served with deliberately incomplete context — a calculated quality loss in exchange for the latency guarantee the entire feature depends on.

## Interview Discussion

This case study is increasingly asked precisely because it resists the lazy framing. A weak answer treats it as "a Copilot clone with chat" and designs one pipeline: gather context, call a model, return a suggestion — then tries to bolt agent mode onto that same pipeline as "just a longer version of the same call." That framing collapses immediately under any follow-up question about latency, because it has no answer for why the same architecture would serve both a 150ms keystroke-triggered request and a 90-second multi-file task.

A strong answer opens by explicitly naming the two latency regimes as the organizing fact of the system — sub-second inline completion at very high QPS and low per-request cost, versus multi-minute agent-mode sessions at low QPS and high per-session cost — and reasons forward from there: different model tiers (forced by the latency budget, not a quality preference), different context-gathering strategies (a hard timeout with graceful degradation on the fast path vs. a thorough hybrid-retrieval pass on the agent path), and different failure-handling philosophies (fail silently and instantly on the fast path; feed failures back into an iterating loop on the agent path). Critically, a strong answer also identifies what the two paths *share*: the codebase index (embedding + symbol/lexical search) and the incremental-reindexing pipeline that keeps it fresh against a constantly-changing local working tree — recognizing that this is the one piece of infrastructure that has to serve both a 100ms lookup and a deep multi-hop retrieval pass without becoming the bottleneck for either.

Staff-level follow-up probes to expect: "Your completion p99 latency just regressed by 200ms — where do you look first?" (decompose into context-gathering time vs. inference time vs. network, exactly as the Observability Layer does, rather than guessing); "How would you decide how many tool-call iterations to allow an agent-mode session before forcing a stop?" (tie the cap to task-type cost/step economics, not a single global number, per [Agent Fundamentals & the Agent Loop](../09-agents/01-agent-fundamentals-and-the-agent-loop.md)); "A test suite a sandboxed agent session runs takes 90 seconds — how does that change your orchestrator design?" (the loop's wall-clock budget has to accommodate tool execution time, not just model thinking time, and long-running tool calls may need async polling rather than a blocking call); and "How do you keep the embedding index from drifting stale while a developer is actively editing, without re-embedding on every keystroke?" (incremental diffing on save events plus a live-read fallback for the open file, per the Retrieval Layer's staleness-tolerance design, rather than a freshness guarantee). A candidate who volunteers the shared-substrate-versus-divergent-paths framing without being prompted is demonstrating exactly the cross-cutting-architecture instinct the rest of this handbook is structured to teach.
