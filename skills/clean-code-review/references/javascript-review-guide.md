# JavaScript Review Guide

Apply this pass to `.js`, `.jsx`, `.ts`, `.tsx`, and JavaScript or TypeScript logic outside the purely presentational frontend pass.

## Correctness And Contracts

- Check input validation, output correctness, and contract alignment.
- Check `null`, `undefined`, empty, missing, and partial-input handling.
- Check default-value behavior, truthy or falsy assumptions, and equality coercion mistakes.
- Check async sequencing, promise resolution order, and state-transition correctness.
- Check time, timezone, locale, encoding, and numeric precision behavior when those concerns exist.

## Async And State Safety

- Flag unhandled promises, fire-and-forget behavior without justification, and weak error propagation.
- Check stale closures, duplicate state, hidden mutation, and race-prone updates.
- Check lifecycle cleanup for listeners, timers, subscriptions, observers, and fetch cancellation where relevant.
- Check that loading, success, error, empty, and disabled states are explicit and coherent.

## Types And Boundaries

- In TypeScript, flag loose `any`, unsafe assertions, and weak narrowing when the real type is knowable.
- Check API boundary typing, serializer or parser assumptions, and data-shape drift.
- Prefer explicit boundary validation over trusting external inputs.

## Security

- Check unsafe `innerHTML`, `dangerouslySetInnerHTML`, `eval`, `new Function`, and unsafe URL handling.
- Check token storage, secret exposure, and sensitive logging in client or server JavaScript.
- Check client-side trust assumptions, especially when authorization or validation appears to rely on the browser.

## Performance

- Flag repeated expensive work in render or request paths.
- Check excessive rerenders, unstable props or handlers, and redundant network work where relevant.
- Check bundle growth, repeated parsing, and unbounded event or DOM work when the impact is real.
- Check whether expensive computations belong outside render, behind memoized selectors, or behind server-side precomputation when that materially improves responsiveness.
- Prefer fewer network round trips, better batching, and smaller client work on latency-sensitive paths.

## Maintainability

- Remove dead code, abandoned feature flags, commented-out branches, and placeholder fallbacks.
- Collapse contradictory patterns for async handling, state updates, and fetch logic.
- Prefer explicit readable logic over clever shorthand that hides control flow.
