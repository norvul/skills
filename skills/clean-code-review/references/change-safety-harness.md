# Change Safety Harness

Apply this harness before making edits. The goal is to improve code aggressively without breaking behavior, widening scope, or slipping into speculative rewrites.

## Core Principle

The skill exists to make the codebase better, not different for its own sake. Preserve working behavior by default and change only what you can justify, validate, and contain.

## Change Budget

Default to a small patch:

- one logical issue set
- tight file scope
- no unrelated cleanup
- no hidden architecture rewrite

If the work starts expanding beyond the original issue, stop and either narrow the patch or report the broader problem separately.

## Risk Tiers

### Low-Risk Changes

- dead code deletion with strong evidence
- local simplification with behavior preserved
- naming cleanup with no contract impact
- targeted test strengthening
- obvious safe performance wins on a measured or strongly inferred hot path

These can usually be implemented directly if validation exists.

### Medium-Risk Changes

- behavior-affecting fixes on active paths
- refactors across multiple modules
- cache introduction or batching changes
- query changes
- render-flow or state-flow rewiring
- changes that rely on inferred rather than tested behavior

These require stronger validation and a tighter explanation of what is preserved.

### High-Risk Changes

- public API changes
- schema or migration changes
- auth, permission, or secret handling changes
- deployment, release, or infrastructure changes
- payment, billing, or other business-critical workflow changes
- wide-reaching rewrites or changes across many surfaces

Do not make these casually. Narrow the patch, add strong evidence, or stop and report.

## Behavior Preservation Rules

- Preserve public interfaces unless the request or source of truth requires a change.
- Preserve CLI flags, config keys, environment variable semantics, schema shape, and externally consumed outputs unless the change is explicitly justified.
- Preserve frontend semantics, keyboard flows, and accessibility unless fixing a defect.
- Preserve operational expectations for logs, deployment paths, health checks, and rollback behavior unless correcting a documented problem.

## Validation Ladder

Use the strongest practical validation available for the risk level:

1. Existing tests relevant to the change.
2. Typecheck, lint, build, and static checks.
3. Characterization tests or focused regression tests added before or with the refactor.
4. Smoke checks or manual verification steps for visible or operational behavior.
5. Before or after measurements for optimization work.

If stronger validation is unavailable, say exactly what remains unverified.

## Characterization Test Rule

Before changing active behavior in weakly tested code:

- add a focused test if the behavior is knowable and testable
- or record a concrete manual reproduction path if automation is not practical

Do not rely on memory alone when the path matters.

## Protected Paths

Use extra caution for:

- authentication and authorization
- payment, billing, or money movement
- migrations and data writes
- deployment and release logic
- secrets and token handling
- caching and invalidation logic
- concurrency, retries, and job processing
- startup, shutdown, and health logic

For protected paths, prefer stronger validation and smaller edits.

## Rollback Rules

- If validation fails, revert or discard the change.
- If the patch works only by adding complexity you cannot justify, revert or narrow it.
- If the final diff is broader than the evidence supports, split it or stop.
- If you cannot explain what behavior is preserved, you are not done validating.

## Output Requirements

For any implemented change, report:

1. What behavior was intended to stay the same.
2. What behavior was intentionally changed.
3. What validation was run before and after the edit.
4. What remains uncertain.
