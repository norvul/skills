# Performance Optimization Guide

Apply this pass when the user asks for speed, snappiness, lower latency, faster task execution, higher throughput, render performance, or general optimization.

## Objective

Make active paths materially faster without sacrificing correctness, safety, or maintainability. Optimize for real user or operator benefit, not for clever micro-tuning.

## Core Rules

- Identify the bottleneck before optimizing.
- Prefer measured evidence when the repo gives you a way to benchmark, profile, trace, count queries, inspect bundle size, or compare timings.
- If hard measurement is unavailable, use explicit hot-path reasoning and say that the optimization is inference-based.
- Prefer algorithmic, query, batching, caching, and render-structure improvements over micro-optimizations.
- Do not increase complexity for noise-level gains.
- Do not claim a path is "optimal" without evidence. The target is the best practical solution supported by the repo context.

## Review Sequence

1. Identify the performance-sensitive path.
2. Determine the performance dimension that matters most:
- latency
- throughput
- startup time
- render responsiveness
- memory pressure
- query or network volume
3. Find the likely bottleneck:
- repeated work
- blocking work
- unnecessary allocations
- expensive queries
- too many network round trips
- excessive rerenders
- oversized payloads or bundles
- unbounded scans or loops
4. Prefer the smallest high-leverage fix.
5. Validate the result with before or after evidence whenever possible.

## High-Value Optimization Targets

- Algorithmic complexity reductions.
- Query-count reduction and better batching.
- Eliminating repeated serialization, parsing, and transformation work.
- Avoiding repeated filesystem or network I/O on hot paths.
- Reducing unnecessary rerenders or DOM work.
- Lowering startup or hydration cost on important entry points.
- Caching only when invalidation, freshness, and memory cost are understood.

## Things To Be Skeptical Of

- Micro-optimizations with no measurable impact.
- Added abstraction that makes the code harder to debug for tiny gains.
- Caches with unclear invalidation or memory growth.
- Concurrency added to hide slow logic without improving the true bottleneck.
- Premature optimization on code paths that are not user-visible or operationally important.

## Validation Expectations

- Prefer benchmarks, timing comparisons, profiler output, query counts, bundle diffs, render counts, or request-count comparisons.
- If exact measurement is unavailable, document the strongest available proxy signal.
- Report what got faster, why it got faster, and what tradeoff was introduced or avoided.

## Output Discipline

For optimization-focused runs, include:

1. The path or workflow optimized.
2. The performance dimension improved.
3. The bottleneck removed or reduced.
4. The evidence used: measurement, proxy, or reasoned inference.
5. The validation run or the remaining uncertainty.
