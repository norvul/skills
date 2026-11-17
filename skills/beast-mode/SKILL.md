---
name: beast-mode
description: Coordinate focused investigation, design, implementation cleanup, and verification when the user explicitly asks for Beast Mode.
license: MIT
---

# Beast Mode

Use only when explicitly requested. Carry the authorized task through to its
outcome; this is a workflow for that task, not a persistent host mode.

## Work proportionally

1. Establish the requested outcome, constraints, and current task diff. Preserve
   unrelated edits. Reuse Alpha's acceptance guidance and the project's existing
   checks. In Plan or a read-only request, investigate and report within that
   scope; do not implement.
2. Trace the affected entry point, state owner, callers, and changed contracts.
   Expand only when evidence crosses another boundary. A large repository needs
   focused slices, not a full-repository tour.
3. Resolve consequential design uncertainty before editing. Implement the
   smallest coherent change; keep each piece of state owned in one place.
4. Clean the task's changed code where useful, then run the relevant project
   verification and boundary checks. Broaden checks for concrete risks or required
   project policy. Do not manufacture a new verification workflow for a small fix.
5. Report the outcome, evidence, and remaining gaps plainly. If blocked, name the
   missing prerequisite and what remains unverified; continue independent work
   that is still useful. Never claim a run, screenshot, or measurement you lack.

## Load only what earns its cost

These are optional routes, not a checklist. Skip work already established in
context; load only the selected skill and relevant resources.

| Need | Skill |
| --- | --- |
| Unclear runtime flow, ownership, or placement | `how` |
| Consequential design rationale or history | `why` |
| Meaningful interface or module decision | `architect` |
| Competing designs or artifacts need comparison and synthesis | `arena` |
| Unclear states, transitions, or repeated shape assumptions | `principle-model-the-domain` |
| A reusable project verification recipe is missing and creating one is in scope | `create-verification-skill` |
| The relevant verification recipe has drifted | `maintain-verification-skill` |
| Actual code in this task's diff needs cleanup | `deslop` |
| A change may break consumers or lifecycle assumptions beyond the diff | `blast-radius` |
| A requested or justified adversarial challenge | `interrogate` |
| Independent slices benefit from authorized delegation | `swarm` |
| A demonstrated recurring mistake merits an in-scope prevention change | `correct` |
| The user asks for a simpler explanation, including "bro" | `bro` |

Load a known name directly through Alpha's `skill` tool, using its current
schema (`action: "load"`, `skill`, `args`, `cursor`). Explicit-only skills
need not appear in lists. Consume all instruction pages before acting. Use the
resolved skill identity and its resources, not assumed sibling paths. Reuse
instructions already loaded for that identity. If unavailable, report the gap
and use ordinary task methods where permitted; honor host restrictions without
reading a blocked skill's file around them.

Delegation is conditional on host and user authority. Children share files and
inherit scope, policy, and a frozen skill catalog. Keep integration with the
coordinator; pass necessary context without assuming new skills can be discovered.
Use the current model/profile; overrides require explicit user authorization and
host availability. A skill cannot change Code/Plan mode, approvals, or permissions.

## Requirements and example

Requires Alpha skill loading and the tools needed by the task; file/shell access
for code work, optional authorized agent tools for parallel work. Install the
thirteen companion directories for full routing. No bundled scripts, downloads,
accounts, or fixed network services. Edits and project checks follow task scope;
commits, publication, deployment, and installation require their own authority.

Example: "Use $beast-mode to fix this CLI losing zero-quantity rows." Trace the
CLI path, make the focused fix, clean its diff if needed, and exercise the existing
CLI regression check. Skip architecture review and delegation when they add nothing.

License: [MIT](LICENSE.txt).
