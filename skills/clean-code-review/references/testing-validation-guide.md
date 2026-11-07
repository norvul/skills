# Testing And Validation Guide

Apply this pass when tests exist, when validation quality is questionable, or when the skill makes behavior-changing edits.

## Coverage Expectations

- Check whether critical paths are protected by unit, integration, smoke, or end-to-end coverage as appropriate.
- Check boundary cases, failure paths, negative cases, async paths, and state transitions.
- Treat happy-path-only tests as incomplete protection.

## Test Quality

- Prefer tests that validate behavior and contracts over tests that mirror implementation details.
- Flag weak assertions, shallow snapshots, and tests that would pass through obvious regressions.
- Flag over-mocking when mocks erase the behavior that actually needs protection.
- Check fixture clarity, setup sprawl, and brittle hidden dependencies.

## Reliability

- Flag flaky timing assumptions, shared mutable state, order dependence, and environment-sensitive tests.
- Check retries, sleeps, and polling-heavy tests for hidden instability.

## Validation For Edits

- The stronger the risk, the stronger the validation required.
- Prefer targeted, relevant validation over cargo-cult full-suite runs when the change is local.
- When validation cannot be run, say exactly what remains unverified and why.

## Characterization And Safety

- Before refactoring weakly tested active behavior, add a focused characterization test or a concrete reproducible manual check.
- Treat public API behavior, schema behavior, CLI semantics, and user-visible flows as contracts that should be preserved unless the change intentionally fixes them.
- If the diff is broader than the validation story, narrow the change.
