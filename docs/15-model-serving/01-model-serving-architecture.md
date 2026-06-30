# Model Serving Architecture

## Overview

Model serving is the infrastructure that sits between a trained model's weights and a usable API: it accepts inference requests, decides how to group and schedule them across available accelerators, runs the forward pass, and streams tokens back to callers. It is the layer that determines whether a model costs $0.50 or $5.00 per million tokens to run, and whether a user waits 200ms or 4 seconds for the first word of a response — using the exact same weights and the exact same GPU.

## Definition

Model serving is the runtime system responsible for executing inference requests against a deployed model while jointly optimizing two metrics that are frequently in tension: **throughput** (aggregate tokens generated per second across all concurrent users on a given fleet of accelerators) and **latency** (time-to-first-token and time-per-output-token experienced by one individual request). A serving stack achieves this by batching concurrent requests together, managing the memory used to cache intermediate attention state (the KV cache), and keeping accelerators continuously busy rather than idling between requests.

## Problem Statement

Without a dedicated serving layer, the obvious implementation — load the model once, run one request through it at a time — is correctness-preserving but throws away most of the hardware. LLM token generation (the decode phase) is **memory-bandwidth-bound**, not compute-bound: for each new token, the accelerator reads the entire set of model weights and the growing KV cache from high-bandwidth memory, performs a comparatively small amount of arithmetic, and writes one token back. A single request cannot saturate the GPU's compute units no matter how large the model is, because the bottleneck is data movement, not math. Run requests one at a time and a GPU capable of computing thousands of tokens/sec in parallel sits at single-digit-percent utilization serving one user at a time.

The naive fix — wait for several requests, batch them, run the batch — creates a different problem: **head-of-line blocking**. If requests must be batched and dispatched together, a short request (a 5-token answer) is stuck in the same batch as a long one (a 2,000-token essay) until the longest request in the batch finishes, because classic batched execution doesn't return individual sequences early. Throughput improves; latency variance gets much worse, and short, cheap requests pay the latency cost of whatever the slowest request in their batch happens to be.

A production serving layer has to solve both problems simultaneously: keep accelerators busy enough to make the hardware spend worthwhile, without forcing every request to wait on the slowest peer sharing its batch.

## Why This Architecture Exists

The first generation of LLM-serving systems borrowed directly from classical ML model serving (think TensorFlow Serving): load a model, accept a request, run a fixed-shape forward pass, return a result. That works for single-pass classifiers with a known, fixed output size. It breaks down for autoregressive generation, where output length is unknown in advance and each token requires a fresh forward pass conditioned on everything generated so far.

The next attempt was **static batching**: collect requests until a batch-size target or time window is hit, pad every sequence to the same length, run the whole batch together, and return all results when the slowest member finishes. This improved utilization over one-at-a-time serving, but it has three structural flaws: padding wastes compute on requests shorter than the batch's longest member; the entire batch is held hostage by its slowest member (head-of-line blocking); and batch composition is frozen at dispatch — a request arriving mid-batch waits for the whole batch to drain before it can even begin.

**Continuous batching** (in-flight batching), pioneered in systems like Orca and popularized in production by [vLLM](https://github.com/vllm-project/vllm), restructured the execution loop around individual tokens instead of whole sequences. At each scheduling step, the engine generates exactly one next token for every in-flight request, immediately evicts any request that just produced an end-of-sequence token, and immediately admits a newly arrived request into the freed slot — without waiting for any other sequence to finish. This is the shift that made high GPU utilization and low per-request latency variance compatible goals instead of competing ones. The mechanics are covered in depth in [Batching & Continuous Batching](02-batching-and-continuous-batching.md); this chapter treats it as the default scheduling discipline a serving stack is built around.

A second pressure point pushed the architecture further: even with perfect batching, every in-flight sequence needs its KV cache resident in accelerator memory for its entire duration, and that memory — not raw FLOPs — became the binding constraint on concurrency. That fact reshaped serving-engine design around memory management as a first-class concern; see [KV Cache Management](03-kv-cache-management.md).

## Core Concepts

- **Prefill vs. decode** — prefill is the single forward pass over the entire input prompt, computing attention over all prompt tokens at once; it is compute-bound and produces the first output token. Decode is the repeated, one-token-at-a-time loop that follows; it is memory-bandwidth-bound, dominated by reading weights and KV cache rather than arithmetic. These opposite hardware profiles are why some architectures schedule the two phases separately (see [Disaggregated Prefill/Decode](../17-distributed-inference/02-disaggregated-prefill-decode.md)).
- **Time-to-first-token (TTFT)** — latency from request arrival to the first streamed token; dominated by prefill time and queueing delay.
- **Time-per-output-token (TPOT)** — the steady-state latency between successive streamed tokens; dominated by decode-phase memory bandwidth and current batch occupancy.
- **KV cache** — the cached key/value attention tensors for every token already processed, kept resident so each new token's attention doesn't recompute over the entire prior context from scratch. Its size grows linearly with sequence length and batch size, and at production scale it is typically the dominant consumer of accelerator memory — ahead of the model weights — for long-context, high-concurrency workloads.
- **Batch occupancy / utilization** — the fraction of an accelerator's compute or memory-bandwidth capacity actually used; the purpose of a serving engine is to push this up without blowing the latency budget.
- **Throughput vs. latency tension** — larger batches raise aggregate tokens/sec (more requests sharing the same weight-read cost per step) but raise TPOT for every request in the batch (more total memory traffic per step), until the batch's KV cache exceeds available memory — the hard ceiling on how far batching alone can go.
- **Cold start / model loading latency** — the time to load weights into accelerator memory and warm up the execution graph (e.g., CUDA graph capture, kernel autotuning) before a replica can serve its first request; tens of seconds to minutes for large models, which makes autoscaling a slower lever than it is for stateless web services.

## The Serving Stack

```mermaid
flowchart TB
    C[Client Request] --> GW[API Gateway]
    GW --> Q[Request Queue]
    Q --> SCHED[Scheduler / Batcher]
    SCHED --> ACC[Accelerator Pool\nGPU/TPU]
    ACC --> STREAM[Token Streaming]
    STREAM --> C
```

The detailed view shows what the scheduler and accelerator boxes actually contain in a production engine: admission control, a continuous-batching loop, KV cache paging, and routing across many model replicas.

```mermaid
flowchart TB
    subgraph Edge["Edge / Control Plane"]
        REQ[Inference Request] --> AUTHN[Auth + Rate Limit]
        AUTHN --> ROUTER[Model Router]
    end

    subgraph Replica1["Serving Replica"]
        ROUTER --> RQ[(Request Queue)]
        RQ --> ADMIT{Admission Control:\nKV budget available?}
        ADMIT -->|Yes| INFLIGHT[In-Flight Batch]
        ADMIT -->|No, queue full| BACKPRESSURE[Reject / 429\nor route elsewhere]
        INFLIGHT --> STEP[Scheduler Step:\n1 token per active sequence]
        STEP --> KVMGR[KV Cache Manager\nPaged blocks + eviction]
        KVMGR --> STEP
        STEP --> EXEC[Forward Pass on Accelerators]
        EXEC --> DONE{Sequence finished\nor evicted?}
        DONE -->|No| INFLIGHT
        DONE -->|Yes| EMIT[Stream Final/Next Token]
    end

    subgraph Fleet["Replica Fleet"]
        ROUTER --> Replica2[Replica 2]
        ROUTER --> Replica3[Replica 3]
        ROUTER --> ReplicaN[Replica N]
    end

    EMIT --> RESP[Response to Client]
    LB[Load Balancer /\nLeast-Busy or Cache-Aware Routing] --> ROUTER
```

## Components

| Component | Responsibility | Does NOT own |
|---|---|---|
| API gateway | AuthN/AuthZ, request validation, rate limiting, request shaping | Scheduling, batching |
| Model router | Picks which model/replica/version serves a request (see [Multi-Model Serving & Routing](05-multi-model-serving-and-routing.md)) | Token generation |
| Request queue | Holds admitted-but-not-yet-scheduled requests; provides backpressure when full | Memory management |
| Scheduler / batcher | Decides which requests run in the next decode step; implements continuous batching | The forward pass itself |
| KV cache manager | Allocates, pages, and evicts attention cache memory per sequence | Request admission policy |
| Accelerator pool | Executes the forward pass (prefill and decode) | Routing, queueing |
| Token streaming layer | Pushes generated tokens back to the client incrementally (SSE/gRPC streaming) | Generation correctness |
| Load balancer | Distributes traffic across replicas, ideally cache- or load-aware | Per-replica scheduling |
| Autoscaler | Adds/removes replicas based on queue depth and utilization signals | Per-request latency guarantees during scale-up |

## Continuous Batching in Action

```mermaid
sequenceDiagram
    participant U1 as Request A (short)
    participant U2 as Request B (long)
    participant U3 as Request C (new arrival)
    participant Q as Queue
    participant S as Scheduler
    participant KV as KV Cache Mgr
    participant GPU as Accelerator

    U1->>Q: enqueue (+1-3ms gateway/auth)
    U2->>Q: enqueue
    Q->>S: admit A, B into batch (+1-5ms admission check)
    S->>KV: allocate KV blocks for A, B
    S->>GPU: prefill A, prefill B (+50-200ms, compute-bound)
    GPU-->>U1: first token A (TTFT)
    GPU-->>U2: first token B (TTFT)
    loop Continuous batching: one step per active sequence
        S->>GPU: decode step for A, B together
        GPU-->>U1: next token A (~10-30ms TPOT)
        GPU-->>U2: next token B (~10-30ms TPOT)
        U3->>Q: enqueue mid-flight
        Q->>S: admit C into next free batch slot
        S->>KV: allocate KV blocks for C
        S->>GPU: decode step for A, B, C together
        GPU-->>U3: first token C (TTFT, no wait for A/B to finish)
    end
    GPU-->>U1: EOS, evict A, free KV blocks
    Note over S,KV: A's slot is immediately reusable —\nB and C continue unaffected
```

The critical property this diagram is making concrete: Request C's first token does not wait for Request A or B to complete, and Request A's completion does not stall B or C. That decoupling — only possible because scheduling happens per-token, not per-batch — is the entire reason continuous batching replaced static batching in every serious serving engine.

## Serving Engine Patterns

```mermaid
flowchart LR
    subgraph T0["t=0"]
        A0[Req A: prefill] 
        B0[Req B: prefill]
    end
    subgraph T1["t=1"]
        A1[Req A: decode tok 1]
        B1[Req B: decode tok 1]
    end
    subgraph T2["t=2"]
        A2[Req A: decode tok 2]
        B2[Req B: decode tok 2]
        C2[Req C: prefill, just arrived]
    end
    subgraph T3["t=3"]
        A3[Req A: EOS, evicted]
        B3[Req B: decode tok 3]
        C3[Req C: decode tok 1]
        D3[Req D: prefill, fills A's slot]
    end
    T0 --> T1 --> T2 --> T3
```

This is continuous batching's defining workflow: the batch composition is fluid across scheduling steps. The patterns built on top of this core loop, roughly in order of how production engines layer them in:

1. **Static batching (legacy baseline)** — fixed-membership batches, padded to the longest sequence, dispatched as a unit. Still seen in older serving stacks or for workloads with uniform, short, fixed-length outputs (e.g., classification-style single-token outputs) where the downsides don't bite.
2. **Continuous / in-flight batching** — per-step admission and eviction, as shown above. The default in vLLM, TensorRT-LLM, and SGLang, and the baseline assumption for the rest of this chapter.
3. **Prefix / prompt caching** — when multiple requests share an identical prefix (a system prompt, a few-shot template, a long shared document), the KV cache for that prefix is computed once and reused, turning a repeated prefill into a cache hit. High-leverage for any product with a shared system prompt across many users.
4. **Speculative decoding** — a small draft model proposes several tokens ahead, and the main model verifies them in a single batched forward pass, trading extra (cheap) compute for fewer expensive sequential decode steps when the draft is accepted; see [Speculative Decoding at Scale](../17-distributed-inference/03-speculative-decoding-at-scale.md).
5. **Disaggregated prefill/decode** — running prefill (compute-bound) and decode (bandwidth-bound) on physically separate accelerator pools tuned for each phase's profile, transferring the KV cache between them, to avoid one phase's traffic pattern degrading the other's; see [Disaggregated Prefill/Decode](../17-distributed-inference/02-disaggregated-prefill-decode.md).
6. **Tiered/multi-model routing** — sending easy queries to a small, cheap model and hard queries to a large one behind a single logical endpoint; see [Multi-Model Serving & Routing](05-multi-model-serving-and-routing.md).

## Multi-LoRA Serving: One Base, Many Adapters

Fine-tuned LoRA adapters are small (50–500 MB) relative to their base model (10–70 GB). This size asymmetry enables **multi-LoRA serving**: one GPU replica holds the base model weights in GPU memory, and multiple adapters are loaded or swapped at request time, letting a single physical deployment serve hundreds of fine-tuned variants.

**Why this matters for product architectures:**

A common pattern in enterprise AI is per-customer or per-use-case fine-tuning — a legal AI platform might have 50 law-firm-specific adapters, each fine-tuned on that firm's documents and style. Without multi-LoRA, serving 50 variants means 50 GPU replicas, each holding a full copy of the base model. With multi-LoRA, you hold the base model once and hot-load adapters as requests arrive.

**How it works:**

1. The serving engine (vLLM, TGI, and purpose-built LoRA routers) keeps the base model weights in GPU HBM at all times.
2. For each request, the adapter ID is resolved from a routing header or tenant identifier.
3. The adapter's weight deltas (the LoRA matrices) are loaded into GPU memory and applied to the relevant base weight matrices during the forward pass.
4. A small adapter cache (typically 10–50 adapters in GPU memory simultaneously, depending on adapter size and available HBM) keeps recently-used adapters warm; cold adapters are loaded from host memory or storage, typically in 10–100ms.

**Sizing multi-LoRA deployments:**

- GPU memory required = base model weights + active adapter cache + KV cache for current batch.
- A 7B model at BF16 uses ~14 GB; 50 rank-16 LoRA adapters for common layers add perhaps 2–5 GB total. A single A100 80 GB can hold the base model and an adapter cache comfortably alongside KV cache for dozens of concurrent requests.
- For very large adapter counts (thousands), add an adapter tier: store adapters on NVMe SSDs, pre-warm the top-N most-used adapters in GPU memory using recent traffic patterns, and pay a cold-load penalty only on cache misses.

**Limitations:**

Multi-LoRA requires all adapters to be trained against the same base model at the same precision. Mixing adapters from different base models or ranks on one replica is not supported.

## Batch and Offline Inference

The serving patterns above optimise for **online inference**: interactive, latency-sensitive requests where users wait for a response. A large category of AI workloads doesn't fit that model — they process large volumes of data in the background, where latency per item is unimportant and throughput is the only metric that matters.

**When offline/batch inference is the right pattern:**

- **Embedding generation pipelines** — embedding 10 million documents for a RAG corpus update; throughput matters, not latency.
- **Bulk classification or scoring** — running a content-safety classifier over a week of uploaded images overnight.
- **Pre-computing summaries or structured extractions** — processing a corpus of legal documents to extract structured data for downstream search.
- **Eval suite execution** — running 2,000 golden-set examples through an LLM judge; this should not compete with user traffic for GPU capacity.

**How offline inference differs architecturally:**

| Dimension | Online serving | Offline batch |
|---|---|---|
| Latency target | p50/p95 SLO (100ms–3s) | None — throughput per hour |
| KV cache strategy | Minimise resident time, rapid eviction | Large batches, no eviction pressure |
| Batch size | Dynamically bounded by KV cache | Maximise to GPU memory limit |
| Request ordering | FIFO with priority lanes | Sort by sequence length to minimise padding waste |
| Infrastructure | Always-on replicas | Spot or preemptible instances, start/stop per job |
| Cost target | p99 latency SLO | Cost per 1M tokens processed |

**Practical guidance:**

Do not run batch jobs on the same serving infrastructure as your real-time user traffic. Batch workloads use large KV cache allocations and long-running sequences that crowd out the short, latency-sensitive requests that arrive interactively. Use a separate GPU pool (or schedule batch jobs during off-peak hours on a pool with explicit admission limits) and optimise that pool independently for throughput: larger batch sizes, sorted-by-length batching to minimise padding, and no speculative decoding (which optimises for latency, not throughput).

## Tradeoffs

```mermaid
flowchart TD
    Q1{Is the bottleneck\nqueueing/throughput\nunder load?} -->|Yes, GPUs are saturated| Q2{Is KV cache memory\nthe limiter, not compute?}
    Q1 -->|No, latency is fine but\ncost per token is high| QUANT[Quantize the model]
    Q2 -->|Yes| Q3{Can the model tolerate\nlower precision?}
    Q2 -->|No, raw compute is the limiter| REPLICAS[Add replicas]
    Q3 -->|Yes| QUANT2[Quantize to shrink\nKV cache + weights]
    Q3 -->|No, quality-sensitive| Q4{Is traffic bursty\nor steady-state high?}
    Q4 -->|Bursty| AUTOSCALE[Autoscale replicas\n+ accept cold-start cost]
    Q4 -->|Steady-state high| REPLICAS
    REPLICAS --> Q5{Is per-request\nlatency still too high\nafter adding capacity?}
    Q5 -->|Yes| SMALLER[Route easy traffic to\na smaller/distilled model]
    Q5 -->|No| DONE[Tune batch size /\nscheduler policy]
```

| Advantages (continuous batching + quantization + horizontal scaling, together) | Disadvantages |
|---|---|
| Order-of-magnitude better GPU utilization than naive per-request serving | Significant engineering complexity vs. a simple model.generate() call |
| Decoupled per-request latency — one slow request doesn't stall others | KV cache memory becomes a hard, easy-to-underestimate ceiling on concurrency |
| Horizontal scaling (replicas) handles steady-state load growth cleanly | Cold start (tens of seconds to minutes for large models) makes autoscaling a slow lever, not an instant one |
| Quantization buys latency/memory headroom with a measured quality cost | Every lever (batch size, precision, replica count) interacts with the others — tuning one in isolation can regress another |
| Multiple independent levers (batch, precision, replicas, model size) give real flexibility | Requires production-grade observability to know *which* lever is actually the bottleneck at a given moment |

## Scalability

- **Batch size vs. latency**, illustrative shape for a mid-size open model on a single high-end GPU: at batch size 1, TTFT might be ~80ms and steady-state throughput is a few dozen tokens/sec — almost entirely wasted bandwidth. Raising the batch to ~32 concurrent sequences can push aggregate throughput up by roughly 10-20x with TPOT rising only modestly (each decode step now serves 32 requests' worth of useful work per weight-read instead of 1). Past a certain batch size — commonly somewhere in the 64-256 range depending on model size, sequence length, and accelerator memory — the KV cache for the batch exceeds available memory, and throughput gains flatten or reverse if pushed further; the only ways forward are evicting/queueing requests, quantizing, or adding accelerators.
- **GPU utilization, naive vs. continuous batching**: serving one request at a time on a GPU sized for an LLM workload commonly leaves single-digit-percent compute utilization during decode. A well-tuned continuous-batching scheduler is routinely reported in the 3-10x throughput-per-GPU range over that baseline on the same hardware and model — the exact multiple depends on request-length distribution and prefix shareability, but the order of magnitude is consistent across public benchmarks from vLLM, TensorRT-LLM, and SGLang.
- **Replica scaling** handles load growth horizontally once a single replica is well-tuned, but each replica has fixed KV cache and compute capacity — adding replicas raises the ceiling on total concurrent requests, not the latency ceiling for any individual request.
- **Cold start** is the wrinkle that differs from typical web-service autoscaling: loading a large model's weights and warming the execution graph takes tens of seconds to minutes, so reactive autoscaling (scale up only once queueing is observed) arrives too late for sudden spikes — production systems pre-warm a buffer of idle-but-loaded replicas or scale predictively from leading traffic signals.
- **Sequence length** compounds both axes at once: a 10x increase in average context length roughly 10x's the KV cache footprint per sequence at the same batch size, cutting concurrency and increasing prefill time simultaneously — long-context products need this modeled explicitly, not extrapolated from short-prompt benchmarks.

## Reliability

| Failure | Degradation strategy |
|---|---|
| Accelerator/replica crash mid-generation | Route to a healthy replica; client-visible effect is a dropped stream, which clients should treat as retryable, not a corrupted answer |
| Queue saturation under load spike | Return fast, explicit backpressure (HTTP 429 / equivalent) rather than accepting requests that will time out anyway |
| KV cache exhaustion | Evict the lowest-priority in-flight sequence (policy-dependent: oldest, lowest-priority tier, or longest-remaining) rather than crashing the process |
| Cold replica during scale-up | Keep a warm buffer of pre-loaded standby replicas for latency-sensitive tiers; never assume scale-up capacity is available within the request's own latency budget |
| Model weight corruption / bad deploy | Canary new model versions on a small traffic slice with automatic rollback on quality/latency regression, the same discipline as any other production deploy |
| Upstream provider outage (for routed multi-provider setups) | Fall back to a secondary model/provider; see [Reliability Engineering](../23-staff-level-architecture/09-reliability-engineering.md) |

Useful SLO framing for a serving layer: track **TTFT p50/p95/p99** and **TPOT p50/p95/p99** as separate SLOs, not one blended "latency" number — they have different causes (queueing/prefill vs. steady-state batch occupancy) and regress independently. Track **admission rejection rate** as a leading indicator of capacity shortfall before it becomes a latency incident.

## Security

A serving layer's attack surface is different from a typical API's because the "compute" being protected is expensive, shared, and stateful across requests. Three risks are specific to this architecture:

- **Resource exhaustion / denial of service via the KV cache** — a small number of maliciously long-context or adversarially crafted requests can consume a disproportionate share of shared accelerator memory, starving other tenants' requests of KV cache budget. Per-tenant memory quotas and admission-time limits on context length are the standard mitigation, not just request-rate limiting.
- **Cross-tenant leakage through prefix caching** — if prompt/prefix caching is shared across tenants without correct isolation, a cache keyed only on token content (not also on tenant/session identity) can theoretically let one tenant's cached computation be reused in ways that leak timing or behavioral signal about another tenant's traffic. Cache keys must be scoped to the appropriate isolation boundary.
- **Side-channel timing on shared infrastructure** — response timing on shared multi-tenant accelerators can, in principle, leak information about other tenants' concurrent batch composition; this is a lower-probability, higher-sophistication risk but relevant in regulated multi-tenant deployments. See [Data Exfiltration & Tool Abuse](../21-ai-security/03-data-exfiltration-and-tool-abuse.md) for the broader threat model this fits into.

Standard API-layer concerns (authentication, authorization, input validation, rate limiting) still apply at the gateway in front of the serving stack and are not specific to this architecture — they are necessary but not sufficient.

## Cost Optimization

Illustrative shape: an unbatched (or poorly batched) deployment of a mid-size LLM might land in the **$5-15 per million output tokens** range purely from GPU-hours wasted on idle compute; a well-tuned continuous-batching deployment of the same model on the same hardware class commonly lands in the **$0.50-2 per million tokens** range. The gap is not from cheaper hardware — it's almost entirely from utilization, which is why the levers below are ordered by leverage:

- **Maximize batch occupancy before adding hardware.** Tuning the scheduler and batch size to keep accelerators busy is almost always the highest-leverage lever; buying more GPUs to compensate for a poorly batched stack multiplies the cost of the underlying inefficiency rather than fixing it.
- **Quantize where quality tolerance allows it.** Moving from FP16 to INT8 or INT4 roughly halves or quarters both weight memory and KV cache memory at the same context length, directly raising the batch size that fits in memory — see [Quantization & Compression](04-quantization-and-compression.md).
- **Route by difficulty, not uniformly to the largest model.** Sending simple queries to a smaller model and reserving the largest model for queries that need it is frequently a 50-80% cost reduction on the redirected fraction, with no perceptible quality loss — see [Multi-Model Serving & Routing](05-multi-model-serving-and-routing.md).
- **Exploit prefix caching for shared system prompts.** A large shared instruction block (system prompt, tool definitions, few-shot examples) repeated across most requests turns a meaningful fraction of every prefill into a cache hit instead of fresh compute.
- **Right-size replica count to traffic shape, not peak-forever.** Autoscaling tuned to the real diurnal/weekly curve, with a modest warm buffer for spikes, avoids paying for peak-capacity idle accelerators around the clock.

## Monitoring

- **TTFT and TPOT at p50/p95/p99**, tracked separately — the two most important latency signals, and they regress for different reasons.
- **Tokens/sec per accelerator (throughput)** and **batch occupancy / KV cache utilization** — the core efficiency signals; a healthy serving fleet runs hot on both, not idle "just in case."
- **Queue depth and admission rejection rate** — the leading indicator that capacity is falling behind demand, before users start seeing elevated latency.
- **Per-replica error rate and crash/restart frequency** — accelerator-level failures are a normal operating condition at fleet scale, not an anomaly, and need to be visible without paging on every individual occurrence.
- **Cost per million tokens, generated and tracked over time** — the metric that ties all the above together and catches silent regressions (e.g., a config change that quietly drops batch occupancy).
- **Cold-start / model-load duration** for new replicas — directly informs whether the autoscaler's reaction time matches real traffic spike timescales.

## Production Best Practices

- Default to **continuous batching**, not static batching, for any autoregressive generation workload — static batching's head-of-line blocking is a solved problem, and re-introducing it is a regression, not a simplification.
- Treat **KV cache budget as the primary capacity-planning unit**, not raw GPU count — two fleets with identical GPU counts can support very different concurrent-request ceilings depending on context length and precision.
- **Separate TTFT and TPOT SLOs** explicitly in dashboards and alerting; a blended "average latency" metric hides which phase actually regressed.
- **Pre-warm replica capacity** ahead of known traffic patterns rather than relying purely on reactive autoscaling, because cold start (tens of seconds to minutes for large models) is too slow to absorb a sudden spike.
- **Canary model and config changes on a small traffic slice** with automated rollback on regression, the same discipline applied to any other production deploy — a config change (batch size, scheduler policy, precision) can silently shift the latency/throughput tradeoff in ways that don't show until production load.
- **Measure before reaching for the next lever.** Adding replicas when the real bottleneck is poor batch occupancy, or quantizing when it's queueing delay, both "fix" the wrong problem at real cost — instrument first, then act.

## Real World Examples

The exact internal serving architectures of frontier-model providers are not public, but the publicly described shape — from engineering talks, blog posts, and the open-source engines implementing the same techniques — is consistent enough to describe at a pattern level:

- **OpenAI, Anthropic, and Google** all serve frontier models from fleets of many accelerator replicas behind load balancers, with traffic distributed across multiple regions/availability zones for both latency and resilience. Each has publicly discussed techniques in this space — continuous-batching-style scheduling, KV cache optimization, tiered model routing (cheaper/faster models for simpler requests) — consistent with this chapter's architecture, without disclosing exact internal configurations.
- **vLLM**, originating from UC Berkeley's Sky Computing Lab, popularized PagedAttention-style KV cache management and continuous batching as accessible, off-the-shelf techniques; it is the most common reference implementation cited when discussing these mechanics publicly, and many production stacks across the industry either build on it directly or replicate its scheduling ideas.
- **NVIDIA's TensorRT-LLM** targets the same problem from the compiled-kernel-optimization angle: aggressive kernel fusion, in-flight batching, and quantization tuned tightly to NVIDIA accelerators.
- **SGLang**, also from UC Berkeley's research community, extended the same family of ideas toward structured generation and complex multi-call workloads (agentic and tool-calling patterns).

These open-source engines are useful, inspectable reference points precisely because they implement the same techniques publicly discussed as in use, in some form, at every major frontier-model provider — they differ mainly in implementation detail and hardware targeting, not fundamental architecture.

## Interview Questions

### Beginner

**Q: Why can't you just call model.generate() once per incoming request in production?**
LLM decode is memory-bandwidth-bound, not compute-bound: each step reads the full model weights and KV cache from memory and does relatively little arithmetic per token. A single request can't use most of a modern accelerator's parallel compute capacity, so one-at-a-time serving leaves the GPU mostly idle. Batching requests together lets each weight-read serve many requests' worth of useful work — the entire reason a dedicated serving layer exists instead of a bare inference call.

**Q: What's the difference between time-to-first-token and time-per-output-token, and why track them separately?**
TTFT is latency from request arrival to the first streamed token; it's dominated by queueing delay and the compute-bound prefill pass. TPOT is the steady-state latency between subsequent tokens; it's dominated by memory-bandwidth-bound decode and current batch occupancy. They have different causes and regress independently — a blended average latency metric hides which one actually broke.

### Intermediate

**Q: Explain why continuous batching replaced static batching.**
Static batching fixes a batch's membership and length at dispatch time: every sequence is padded to the longest member, and the whole batch is held until its slowest member finishes. This wastes compute on padding and causes head-of-line blocking — a short request gets stuck behind a long one. Continuous batching schedules at the level of individual decode steps: every active sequence gets one new token per step, finished sequences are evicted and freed immediately, and new requests are admitted into the freed slot without waiting for the batch to drain. This decouples one request's latency from its batch-mates' length.

**Q: What determines how many concurrent requests a single GPU replica can serve?**
Primarily the KV cache memory budget, not raw compute. Each in-flight sequence needs its KV cache resident for its entire duration, growing with both sequence length and batch size. Once aggregate KV cache approaches available memory (after model weights), no more sequences can be admitted regardless of spare compute — which is why capacity planning is done in KV cache budget, not GPU-count, units.

### Senior

**Q: A serving fleet's GPU utilization metrics look high, but p99 latency is still bad. What do you check?**
High utilization with bad tail latency usually means a subset of requests are starved or stuck behind disproportionately expensive peers: long-context outliers dominating batch slots; a scheduler that isn't fairly rotating admission priority; KV cache pressure causing eviction-and-requeue cycles; or queueing delay at the gateway/router before requests reach the scheduler, which accelerator-level utilization metrics won't show at all. The fix is rarely "add more GPUs" — it's almost always a scheduling-fairness or admission-control issue.

**Q: How would you decide between adding replicas, increasing batch size, and quantizing, for a serving fleet under cost pressure?**
Identify the actual bottleneck via monitoring first, not by guessing. If KV cache is the limiting resource, quantization is usually highest-leverage, since it shrinks both weights and KV cache, raising the batch size that fits in memory. If compute is genuinely saturated and quality tolerance for quantization is low, horizontal scaling is the right lever. If the issue is bursty traffic with healthy steady-state utilization, the answer is neither — it's better autoscaling and pre-warming. Reaching for the wrong lever burns engineering time and can regress quality for no throughput gain.

### Staff

**Q: Design a serving architecture for a product with two traffic shapes: 90% short (sub-100-token) chat completions needing sub-second latency, and 10% long-document summarization (10K+ token inputs) where 5-10 second latency is acceptable. One shared fleet, or split?**
Split, behind a router that classifies request shape at admission time, once traffic reaches meaningful scale. Co-locating both shapes creates a memory-contention variant of head-of-line blocking: long-document requests carry disproportionately large KV cache footprints and prefill times, crowding out latency-sensitive batch slots even with continuous batching, because per-token scheduling alone doesn't solve memory contention. The pragmatic split: a latency-tuned pool sized for the short-chat profile's SLO, and a separate throughput-tuned pool (candidate for disaggregated prefill/decode, given the heavier compute-bound prefill) for summarization, where occupying a slot longer is acceptable. The router itself becomes worth instrumenting, since traffic-shape misclassification risk now lives there.

**Q: Your serving fleet's cost-per-token has crept up 3x over six months with no traffic-mix change and no code deploys. How do you find the cause?**
Treat it as a utilization regression. Check, in order: (1) average context length drift — prompts or retrieved context growing over time (common as RAG corpora grow) quietly shrinks effective batch occupancy even though request count hasn't changed; (2) scheduler/config drift — an unflagged "minor" change to batch-size caps, admission policy, or default kernel selection; (3) accelerator fleet composition drift toward a less efficient instance type; (4) a dependency regression silently falling back to a slower unquantized path. The unifying diagnostic: plot tokens/sec per accelerator and batch occupancy over the same six months — if utilization tracks the cost increase inversely, the cause is almost certainly in the first two buckets, not hardware pricing or traffic volume.

## Google-Level Follow-Ups

- "Your batch size keeps growing and aggregate throughput keeps improving — when does that stop being true, and what specifically breaks?" — probes whether the candidate understands that KV cache memory, not compute or an arbitrary scheduler limit, is the actual ceiling, and can describe what happens at that ceiling (eviction, queueing, OOM) rather than just asserting "it doesn't scale forever."
- "If you could only instrument three metrics for this entire serving stack, which three, and why those?" — probes prioritization under real constraints; a strong answer picks signals that are causally distinct (e.g., TTFT, TPOT, and KV cache/batch occupancy) rather than three variations on "latency," and can justify why each one catches a different failure mode the others miss.
- "How does this architecture change for a model so large it doesn't fit on a single accelerator?" — probes whether the candidate connects this chapter to tensor/pipeline parallelism and understands that cross-device communication now becomes part of every forward pass's latency budget, not just a deployment detail (see [Tensor and Pipeline Parallelism](../17-distributed-inference/01-tensor-and-pipeline-parallelism.md)).
- "Convince me continuous batching is strictly better than static batching — is there any workload where static batching is still the right choice?" — probes whether the candidate can find the real exception (extremely uniform, very short, fixed-length outputs — e.g., single-token classification-style workloads — where head-of-line blocking barely exists and static batching's simplicity has genuine value) instead of defending continuous batching dogmatically.

## Common Mistakes

- **Serving one request at a time and calling it "deployed."** This is correct but leaves a GPU at single-digit-percent utilization during decode — it's a prototype, not a production serving layer, and the cost difference at any real traffic volume is enormous.
- **Treating GPU count as the primary capacity metric.** Two fleets with identical accelerator counts can support very different concurrent-request ceilings depending on context length and precision; KV cache budget is the real capacity unit, and ignoring it leads to repeated, confusing under-provisioning surprises.
- **Blending TTFT and TPOT into one "average latency" number.** This hides which phase regressed and routinely sends an on-call engineer down the wrong debugging path.
- **Reactive-only autoscaling for a workload with large, fast traffic spikes.** Cold start for large models is tens of seconds to minutes; scaling only after queueing is observed means the spike has already caused a latency incident by the time new capacity comes online.
- **Quantizing (or adding replicas, or raising batch size) without first measuring which resource is actually the bottleneck.** Each lever fixes a different problem; applying the wrong one burns engineering effort, can regress quality for no throughput gain, and frequently doesn't even move the metric that prompted the change.
- **Sharing a single prefix/KV cache without correct tenant or session scoping.** A cache keyed purely on token content, without an isolation boundary, is a latent cross-tenant data-handling risk, not just a performance optimization detail.

## Key Takeaways

- Model serving exists because naive one-request-at-a-time inference leaves accelerators mostly idle during decode, which is memory-bandwidth-bound, not compute-bound — batching multiple requests together is the entire point.
- Continuous (in-flight) batching replaced static batching by scheduling at the granularity of individual decode steps, decoupling one request's latency from its batch-mates' length and eliminating head-of-line blocking.
- The KV cache, not raw FLOPs, is the dominant memory constraint at production scale — capacity planning should be done in KV cache budget terms, not GPU-count terms.
- Throughput and latency are genuinely in tension: larger batches raise aggregate tokens/sec but raise per-request TPOT, until KV cache memory becomes the hard limit on how far batching can go.
- Continuous batching can plausibly deliver a 3-10x GPU utilization improvement over naive serving, and a well-tuned serving stack can plausibly run at roughly a tenth the cost-per-million-tokens of a poorly batched one on identical hardware — the gap is almost entirely utilization, not hardware pricing.
- Quantization, horizontal replica scaling, and tiered model routing are complementary levers that each solve a different bottleneck — diagnose which resource is actually constrained before reaching for any of them.
- Cold start (tens of seconds to minutes for large models) makes serving-fleet autoscaling fundamentally slower than typical stateless-web-service autoscaling, which argues for pre-warmed capacity over purely reactive scaling.
- The open-source serving engines (vLLM, TensorRT-LLM, SGLang) are useful concrete reference points for these techniques precisely because they implement, in inspectable form, the same publicly-discussed patterns used across the industry at frontier-model scale.
