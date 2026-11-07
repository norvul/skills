# End-State And Follow-Up

Use this reference when the request is broad, when the patch set is intentionally narrow, or when the repo may still be far from the desired end-state.

## Mode Selection

Classify every run as exactly one of:

- `correctness cleanup`: fix concrete defects while preserving contracts.
- `contract alignment`: compare implementation against the source of truth and repair drift.
- `performance optimization`: improve latency, throughput, startup, or responsiveness with evidence.
- `operational hardening`: improve reliability, deploy safety, rollback safety, observability, and operator trust.
- `follow-up audit`: reassess after an earlier pass, close verified gaps, and re-scope what remains.
- `full-surface review`: inspect the repo broadly, fix bounded issues, and produce a closure-aware roadmap.

## End-State Statement

State early:

1. What "good" means for this repo or request.
2. Whether this pass is expected to fully close the gap or only improve it.
3. What evidence would be required to claim closure.

## Closure Ledger

For broad reviews, always maintain:

- `fixed now`
- `flagged for follow-up`
- `not verified`
- `out of scope`

Do not let `fixed now` imply that the whole repo is clean.

## False Completeness Guardrail

Do not imply:

- `fully optimized`
- `complete cleanup`
- `production-ready`

unless the reviewed evidence actually supports that statement across the relevant domains.

## Follow-Up Guidance

When the repo is improved but not complete:

1. Identify the top `1-3` remaining highest-leverage gaps.
2. Say whether another pass should be rerun.
3. If yes, name the exact next focus, for example:
- `rerun in performance optimization mode on query path x`
- `rerun in contract alignment mode on API surface y`
- `rerun in operational hardening mode on deploy and rollback flow z`

## Patch Versus Closure

Always separate:

- what was safely patched now
- what still prevents end-state closure
