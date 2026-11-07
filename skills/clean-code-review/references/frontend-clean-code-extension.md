# Frontend Clean Code Extension

Apply this pass to frontend UI-layer files after the general clean-code pass. Use it for HTML, CSS, SCSS, JavaScript, TypeScript, JSX, TSX, Vue SFCs, template files, and adjacent UI logic.

## Objective

Refactor frontend code to be clean, maintainable, predictable, and production-grade while preserving behavior unless a defect is obvious and low-risk to fix.

Focus on common iterative-AI frontend damage:

- duplicated logic
- bloated components
- inconsistent patterns
- dead UI code
- fragile DOM manipulation
- unclear state flow
- styling sprawl
- hacky event handling

## Core Rules

- Do not rewrite for style only.
- Preserve behavior unless a bug or clear anti-pattern is present.
- Prefer small, safe refactors over broad rewrites.
- Remove workaround layers that accumulated through repeated edits.
- Standardize patterns across the frontend instead of allowing multiple competing approaches in the same codebase.
- Flag uncertainty instead of inventing architecture.
- Preserve the existing design system and visual language unless the current UI behavior is clearly broken or contradictory.
- Treat semantic HTML, accessibility, and client-side security as correctness concerns, not polish.

## Review Sequence

1. Identify the frontend architecture that already exists.
2. Find the cleanest existing pattern for common UI problems before inventing a new one.
3. Remove dead code, duplicate logic, and fake abstraction first.
4. Simplify state, effects, and event flow next.
5. Clean markup, styles, accessibility, and render hygiene after the behavior is understandable.
6. Make the smallest safe refactor set that materially improves durability.

## 1. Component And File Structure

- Break apart oversized components that mix rendering, state, data transformation, side effects, and utilities.
- Separate rendering from state orchestration when the file is hard to reason about.
- Extract repeated UI patterns into reusable components only when reuse is real, not hypothetical.
- Eliminate copy-pasted sections, near-duplicate components, and one-off wrappers with no value.
- Ensure file naming and placement match the actual responsibility of the code.
- Avoid splitting files so aggressively that the flow becomes harder to follow.

## 2. State And Data Flow

- Remove redundant derived state and duplicated sources of truth.
- Simplify prop chains and reduce unnecessary drilling when there is a local, low-risk improvement.
- Eliminate state that can be computed directly from props or existing state.
- Make loading, empty, error, success, and disabled states explicit and consistent.
- Clean up race-prone effects, stale closures, hidden mutation, and scattered update logic.
- Prefer direct and explainable state flow over clever state orchestration.

## 3. JavaScript And TypeScript Quality

- Remove dead code, unused imports, abandoned helpers, debug logging, commented-out blocks, and temporary fallbacks that never got removed.
- Replace vague naming with precise naming when the current name hides intent.
- Flatten deeply nested conditionals when it improves readability.
- Consolidate repeated logic into focused utilities, hooks, or modules only when the extraction reduces real duplication.
- Reduce brittle inline anonymous handlers when they hurt readability or make reuse harder.
- Tighten type usage where the repo uses TypeScript; remove loose escapes such as `any` when the real type is knowable.
- Prefer explicit readable logic over cleverness.
- Check unhandled promises, bad async sequencing, stale closures, incorrect dependency arrays, and hidden mutation.
- Check truthy or falsy bugs, equality coercion mistakes, and accidental reliance on JavaScript quirks.
- Check unsafe `innerHTML`, `dangerouslySetInnerHTML`, token storage, and weak client-side trust assumptions when relevant.

## 4. DOM And Event Handling

- Remove fragile direct DOM manipulation unless there is a strong reason it must exist.
- Standardize event handling patterns within the existing framework.
- Eliminate duplicated listeners, broken cleanup, and timing hacks that substitute for correct lifecycle management.
- Ensure subscriptions, timers, observers, and listeners are cleaned up correctly.
- Reduce hidden coupling between distant UI elements.

## 5. HTML And Markup Quality

- Clean up deeply nested or semantically weak markup.
- Remove meaningless wrappers and container spam.
- Use more semantic structure when it improves maintainability or accessibility.
- Ensure forms, buttons, labels, headings, and interactive elements are structured correctly.
- Make conditional rendering easier to follow.
- Check for invalid nesting, duplicate IDs, broken label-control associations, and misuse of tables or lists.
- Check `doctype`, `lang`, page title or meta basics, and heading order when the file owns document structure.
- Check safe templating boundaries and inline handler usage where server-rendered or raw HTML is involved.

## 6. CSS And Styling Discipline

- Remove unused styles, duplicate classes, dead selectors, conflicting rules, and over-specific selectors.
- Consolidate repeated styling patterns into existing tokens, utilities, or reusable component styles when appropriate.
- Reduce magic numbers unless they are clearly justified by the layout.
- Standardize spacing, sizing, naming, and layout patterns around the codebase's real conventions.
- Eliminate styling that fights itself across files.
- Keep styles local and intentional; avoid accidental global leakage.

## 7. UX Robustness

Ensure the UI handles these states clearly and consistently when they apply:

- loading
- empty
- error
- disabled
- edge-case input
- slow async responses

Remove UI behavior that is visually inconsistent, logically surprising, or awkward because of repeated incremental edits.

## 8. Accessibility And Interaction Quality

- Fix obvious accessibility problems when the change is low-risk.
- Preserve accessibility when refactoring.
- Improve missing labels, poor button semantics, keyboard traps, broken focus behavior, and inaccessible click targets when they are clearly present.
- Do not bolt on large frameworks just to claim accessibility work.
- Check landmark structure, alt text, placeholder-as-label misuse, and ARIA misuse when the markup uses them.

## 9. Performance And Render Hygiene

- Remove wasteful rerenders caused by poor state placement, unnecessary recalculation, or unstable props and functions when the problem is obvious and relevant.
- Avoid premature optimization.
- Defer heavy work away from render paths when appropriate.
- Remove redundant network or UI work introduced by layered patches.
- Prioritize user-visible latency, interaction responsiveness, and startup cost on important screens.
- Prefer measuring render counts, bundle size, request count, or interaction delay when the repo provides a way to do so.

## 10. Consistency Enforcement

Unify patterns for recurring UI problems:

- forms
- modals
- tables and lists
- loading indicators
- error displays
- fetch handling
- state updates
- event wiring
- styling conventions

If the codebase already has multiple patterns for the same problem, prefer the cleanest existing standard or establish the smallest clear standard that fits the current repo.

## Anti-Pattern Hunt

Specifically search for:

- duplicated UI logic
- huge monolithic components
- inline business logic in render blocks
- nested ternary abuse
- scattered conditionals for the same state
- dead feature flags and abandoned experiments
- CSS patch stacking
- DOM query hacks
- arbitrary timeout-based fixes
- inconsistent modal, form, or list implementations
- prop explosion
- hidden side effects
- mixed responsibilities in a single file
- inconsistent naming caused by multiple AI passes
- "temporary" code that became permanent

## Edit Expectations

- Make the smallest safe set of refactors that materially improves frontend quality.
- Keep patches local unless a broader cleanup is clearly justified.
- Preserve the user-visible surface unless the current behavior is obviously defective.
- If a larger architectural decision is needed, flag it separately instead of forcing a rewrite.

## Output Discipline

For each frontend cleanup pass:

1. Identify the highest-value cleanup opportunities.
2. Make the smallest safe refactors that materially improve quality.
3. Briefly explain what changed, why it changed, and what risk was reduced.
4. Separate larger architectural concerns from the changes actually made.

## Decision Standard

A frontend cleanup is successful when the result is:

- easier to read
- easier to modify
- more consistent
- less fragile
- less duplicated
- safer for future AI iterations
- more semantically correct
- harder to misuse or break in production

Do not optimize for cleverness. Optimize for durability.
