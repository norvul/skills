---
name: arena
description: "Spawn parallel candidates at the same task, pick a base, and combine their strongest parts. Use for /arena, competing designs, or a non-trivial artifact where one attempt could lock in the wrong shape."
---

# Arena

Use Alpha's authorized agent tools. If delegation is unavailable, report the arena
blocked. Keep a short task list for Frame, Fan out, Cross-judge, Pick, Graft, Verify.

## Phase A: Frame

The shared task is the contract.

1. State the artifact each candidate must produce.
2. Define 3-6 concrete criteria for success. Candidates see the task; the rubric
   guides judging and selection.
3. Start with two candidates, within host concurrency limits. Omit provider,
   profile, model, and reasoning overrides to inherit Alpha's current settings.
   Use alternatives only when explicitly requested and available in the host.
4. Give each candidate its own output location. Alpha children share the parent's
   checkout; they are not automatically isolated. For competing code edits,
   prepare separate checkouts/worktrees when permitted, including relevant
   uncommitted changes, or have candidates return patches in separate scratch
   directories without editing shared product files. Keep shared app/database
   access serialized; separate output paths alone do not isolate runtime state.

## Phase B: Fan out

Use `spawn_agent` with `fork_turns: "none"` and a self-contained message for each
candidate: the same task, shared grounding, its output path, and a request for
the artifact plus a short rationale naming alternatives considered and rejected.
Use `wait_agent` to collect results. Report dropouts; fewer than two usable
candidates leaves the comparison incomplete.

## Phase C: Cross-judge

After candidates finish, give one read-only judge the task, rubric, and candidate
paths, with `fork_turns: "none"`. Inherit the current model configuration unless
an explicitly requested alternative is available. Do not claim a different-vendor
check when none ran. The judge scores each candidate against each criterion and
recommends a base while the parent reads. If unavailable, report the judge skipped.

## Phase D: Pick a base

Read every candidate. Score each criterion, compare with the judge, and resolve
disagreements from the artifacts and rationales. Prefer the base a maintainer can
extend without breaking invariants; break ties with a cleaner boundary or smaller
API.

## Phase E: Graft

Review each losing candidate for the few parts worth incorporating. The parent
integrates them into one coherent design; do not paste incompatible pieces or let
candidates overwrite each other. If candidates converge, use the shared shape
without manufacturing grafts. If they diverge because the task was unclear,
reframe before another attempt instead of averaging incompatible designs.

## Phase F: Verify

Exercise the synthesized artifact with the relevant real project checks and
inspect the observed results. For review findings, rerun the claimed reproduction
and compare actual with expected behavior. Report blocked or unrun checks as
unverified. If a failure reveals a missing requirement, revisit Frame; if a
candidate already solved it, revisit Graft.

## Outputs

Return the artifact and a short synthesis note: chosen base and why, judge verdict
or skip, each graft and source, rejected parts, convergence/dropouts, and actual
verification results. Keep evidence; clean only temporary resources this arena
created. Commit or publish only within the user's and host's authority.
