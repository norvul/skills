# Comprehensive Audit Framework

Use this reference when the request is broad: annual review, repo garbage collector, full cleanup, full audit, or "no stone unturned."

## Audit Goal

Evaluate the repo as a system, not just as a pile of files. The target is code and process that are readable, maintainable, secure, performant, testable, operationally sane, and structurally coherent.

## Review Setup

1. Start with `python "<skill-dir>/scripts/inventory_repo_surface.py" --root "<repo-root>"`, resolving the installed skill directory separately from the repository under review.
2. Identify the best available source of truth for behavior:
- requirements
- docs
- schemas
- tests
- API contracts
- UX copy
- migration intent
- operator expectations
3. Identify the languages and surfaces that require dedicated review passes.
4. Never infer correctness from implementation alone.
5. Read `references/change-safety-harness.md` before implementing edits.

## Severity And Noise Control

- Use `Critical`, `High`, `Medium`, `Low`.
- Use `must-fix`, `should-fix`, and `advisory`.
- Treat correctness, security, data loss, auth, reliability collapse, and core accessibility failures as `Critical`.
- Do not waste review budget on style-only commentary.

## Required Coverage

1. Functional correctness and contracts
- Does the implementation satisfy the documented or implied contract?
- Are outputs correct, defaults correct, and state transitions valid?
- Are boundary cases, partial inputs, and fallback paths safe?
- Are time, timezone, locale, encoding, and numeric precision handled correctly where relevant?

2. Project structure and architecture
- Do directories, modules, and packages match their real responsibility?
- Are there stale areas, dead subtrees, duplicate layers, or abandoned experiments?
- Are interfaces, boundaries, and ownership lines understandable?

3. Workflow and process
- Is there one clear path for build, test, lint, release, deploy, migrations, and local development?
- Are scripts, CI, docs, and actual practice aligned?

4. Data flow and state flow
- How does data move through the system?
- Where are transformations duplicated, hidden, or split across too many layers?
- Are there multiple sources of truth?

5. Code quality and maintainability
- Where is the code hard to explain, change, or validate?
- Where did AI layering leave repeated helpers, placeholder abstractions, or dead branches?

6. Reliability and robustness
- Are failure modes explicit?
- Are retries, cleanup, timeouts, edge cases, idempotency, and validation handled with intent?
- Are race conditions, partial failures, or non-atomic updates plausible?

7. Security and privacy
- Look for secrets handling mistakes, unsafe shell or process execution, injection surfaces, path traversal risk, unsafe deserialization, weak input validation, auth or permission confusion, sensitive logging, and stale high-risk dependencies where relevant.

8. Performance and resource use
- Look for hot-path waste, N+1 behavior, repeated scans, redundant network work, excessive bundle or render cost, memory leaks, and unbounded work on important paths.
- Identify which performance dimension matters: latency, throughput, startup, memory, query volume, or UI responsiveness.
- Prefer measured or strongly evidenced optimizations over speculative tuning.

9. Dependency and configuration hygiene
- Look for stale dependencies, duplicated configs, contradictory env vars, unused flags, shadow config files, and setup drift.

10. Tests and validation
- Are critical paths protected by tests, smoke checks, or other verification?
- Are assertions meaningful, or are tests mostly cargo-cult coverage?
- Are failure paths, boundary paths, and async or state-transition paths covered?

11. Observability and operations
- Are failures visible?
- Can maintainers diagnose issues with logs, metrics, traces, health checks, or error reporting?
- Are rollout, rollback, startup, shutdown, and operator workflows understandable?

12. Documentation and onboarding
- Do docs match reality?
- Can a new maintainer set up, run, validate, and ship the project without tribal knowledge?

13. Frontend and UI layers
- When present, load `references/frontend-clean-code-extension.md` and review UI architecture, state flow, styling, accessibility, and render hygiene.

14. Language-specific passes
- Load `references/python-review-guide.md` when Python is present.
- Load `references/javascript-review-guide.md` when JavaScript or TypeScript is present.
- Load `references/html-review-guide.md` when HTML or server-rendered templates are present.
- Load `references/testing-validation-guide.md` when test quality or validation depth is in scope.
- Load `references/performance-optimization-guide.md` when the request emphasizes speed, snappiness, task execution time, render performance, or throughput.

## AI-Generated Code Smells

Specifically hunt for:

- duplicate helpers with overlapping names
- wrapper layers added on top of wrapper layers
- inconsistent naming caused by many incremental passes
- placeholder comments or TODOs that became permanent
- dead flags, dead states, dead routes, and dead experiments
- repeated code with slightly different variable names
- fake abstractions that only hide trivial logic
- generic util files that became junk drawers
- contradictory patterns for the same problem

## Coverage Discipline

- Build a review ledger with these statuses: `reviewed`, `edited`, `flagged`, `not present`, `not verified`.
- Never say the audit was comprehensive unless every surfaced domain has a status.
- If a surfaced domain could not be checked deeply, say why and what evidence was missing.

## Change Strategy

- Correctness before cleanup.
- Fix the clearest, highest-leverage problems first.
- Prefer deletion, consolidation, and existing clean patterns over new framework or architecture work.
- Make local edits when possible; split out larger architectural issues instead of forcing rewrites.
- Validate every active-path change with the strongest practical check available.
- For optimization work, prefer the smallest change that materially improves the measured or clearly inferred bottleneck.
- Respect the change budget and protected-path rules from `references/change-safety-harness.md`.

## Output Contract

For full audits, always provide:

1. Severity-ordered findings.
2. Coverage summary across all surfaced domains.
3. Closure ledger: `fixed now`, `flagged for follow-up`, `not verified`, `out of scope`.
4. Edits made and why they were safe.
5. Validation evidence.
6. Remaining risks, blind spots, or larger decisions.
7. The top `1-3` next highest-leverage follow-up gaps and whether another pass should be rerun, with the exact next focus.
