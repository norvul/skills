# Clean Code Review Rubric

Use this reference to calibrate findings and to avoid turning personal style preferences into weak review comments.

## Non-Negotiables

- No dead code in active paths without a documented reason.
- No speculative abstraction that is larger than the problem it solves.
- No active-path code assumed correct just because it currently runs.
- No hidden failure modes when a direct guard or explicit error would do.
- No duplicate workflow entrypoints without a clear ownership boundary.
- No wrapper layers that mainly rename or re-route an existing command.
- No obvious security foot-guns on active paths.
- No obviously wasteful hot-path work without a reason.

## Correctness And Contract Bar

- Verify behavior against a source of truth when one exists.
- Treat contract mismatches, invalid state transitions, wrong defaults, and bad boundary handling as first-class issues.
- Check `None`, `null`, `undefined`, empty, and partial-input cases on active paths.
- Look for time, timezone, locale, encoding, and numeric precision mistakes when the domain depends on them.

## Workflow And Process Smells

- Multiple competing entrypoints for the same recurring task.
- Important steps that exist only in tribal knowledge or chat history.
- Legacy scripts that duplicate behavior already covered by CI, task runners, or platform tooling.
- Automation that bypasses the documented path and creates drift between local and production behavior.
- Release or deploy logic scattered across many small wrappers with no single source of truth.

## Stale Script Signals

Strong signals:

- No references in docs, CI, task runners, or sibling scripts.
- Target files, environments, or workflows no longer exist.
- A newer script or workflow clearly replaces it.
- The script name or comments identify it as one-off, legacy, temporary, or migration-only.

Weak signals:

- Few references.
- Old git history.
- Awkward naming or unclear purpose.

Do not call a script stale from age alone.

## Script Quality Bar

- Keep the control flow easy to explain.
- Keep inputs, outputs, and side effects explicit.
- Fail loudly enough that operators can act on the problem.
- Keep destructive behavior gated, reversible, or at least clearly signposted.
- Remove dead branches, unused helpers, and options that no longer change behavior.
- Prefer platform or standard-library features over custom wrappers when they are good enough.
- Require a realistic validation path for non-trivial behavior.

## Simplicity Versus Robustness

- Prefer deletion first.
- Prefer smaller functions and flatter control flow over abstraction stacks.
- Prefer a little repetition over a wrong abstraction.
- Add indirection only when it improves reliability, clarity, or change safety.
- Robust code is predictable, validated, and easy to debug; it is not merely elaborate.

## Security And Performance Bar

- Protect secrets, boundaries, and untrusted input.
- Avoid unsafe command construction, path handling, deserialization, or exposed debug behavior when relevant.
- Remove obvious repeated work, hot-path waste, redundant queries or requests, and wasteful render loops when the impact is real.
- Treat clear security weaknesses as high severity even if exploitability is not fully proven.
- Prefer algorithmic and architecture-level wins over micro-optimizations.
- Require evidence or a strong hot-path argument before calling a performance optimization high confidence.
- Treat user-visible latency and task completion speed as first-class quality signals in performance-sensitive applications.

## Testing And Validation Bar

- Expect meaningful protection on critical paths: unit, integration, smoke, or end-to-end checks as appropriate.
- Prefer boundary, failure-path, and state-transition coverage over shallow happy-path-only tests.
- Treat weak assertions, flaky tests, and heavy mocking of core behavior as review issues.

## Edit-Or-Block Rules

- Edit immediately when the issue is clear, local, and easy to validate.
- Delete stale files and dead references together.
- Collapse indirection before introducing a new abstraction.
- Add or tighten validation when behavior remains active after the cleanup.
- Add characterization coverage before changing weakly tested active behavior when feasible.
- Block and explain instead of guessing when behavior or ownership is unclear.

## Change Safety Bar

- Preserve contracts and observable behavior unless the defect or source of truth justifies the change.
- Keep the patch smaller than the uncertainty.
- Treat auth, migrations, deployment, secrets, caching, and public interfaces as protected paths.
- If the validation story is weak, the change scope must shrink.

## Research Triggers

- Framework or library behavior depends on version or runtime.
- Shell, CI, deployment, or packaging semantics are easy to get subtly wrong.
- The repo follows a documented house style or platform contract that should override generic advice.
- The fix would otherwise rely on memory with meaningful uncertainty.

## Severity Guide

- Critical: Likely correctness breakage, security exposure, data loss risk, auth or permission failure, or core accessibility failure on active paths.
- High: Can break recurring workflows, releases, deployments, migrations, or important operator actions; can mislead maintainers into using a wrong path; or leaves a serious defect or reliability risk in active code.
- Medium: Creates real maintenance drag, hides behavior, weakens failure handling, or leaves confusing unused code in important areas.
- Low: Clarity or style issue with limited operational impact.

## Noise Control

- Do not reward cleanup that weakens confidence in behavior.
- Do not emit style-only comments without a concrete maintenance, correctness, or safety payoff.
- Prefer fewer high-signal findings with clear evidence over long checklists of preferences.
