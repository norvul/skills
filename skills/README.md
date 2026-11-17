# Skill catalog

| Skill | Purpose | Requirements |
| --- | --- | --- |
| [Clean Code Review](clean-code-review/SKILL.md) | Audit code repositories, make focused fixes, and report validation and remaining gaps. | An agent with file and shell access. Bundled helpers require Python 3.10+ with no extra packages; Git is optional for history. |
| [Beast Mode](beast-mode/SKILL.md) | Route an explicitly requested engineering task through only the supporting workflows it needs. | Alpha skill loading; task-specific tools; the thirteen companions below for full routing. |
| [Bro](bro/SKILL.md) | Restate the last explanation in plain language on request. | Conversation context; no tools required. |
| [How](how/SKILL.md) | Explain runtime flow, ownership, and placement from source. | Source/search tools and authorized Alpha delegation. |
| [Why](why/SKILL.md) | Explain decisions from available history and records. | Source/history access; optional Git and connected review records. |
| [Architect](architect/SKILL.md) | Compare consequential interface and ownership choices. | Source tools; Arena for large or contested designs. |
| [Arena](arena/SKILL.md) | Compare candidates, select a base, and combine their strongest parts. | Authorized Alpha delegation, isolated candidate outputs, and relevant project checks. |
| [Model the Domain](principle-model-the-domain/SKILL.md) | Represent valid states and rules with appropriate data structures. | Source tools; file/check tools for authorized implementation. |
| [Create Verification Skill](create-verification-skill/SKILL.md) | Generate a project verification skill and initial feature map. | Repository write access and the project harness; execution permission for live proof. |
| [Maintain Verification Skill](maintain-verification-skill/SKILL.md) | Audit every mapped feature and repair proven recipe drift. | An existing project verification skill, its harness, and authorized Alpha delegation. |
| [Deslop](deslop/SKILL.md) | Clean actual code in the task diff while preserving behavior. | Source/diff/file tools and relevant project checks. |
| [Blast Radius](blast-radius/SKILL.md) | Investigate affected consumers and test safety assumptions beyond the diff. | Source/diff tools, runtime probes, and Arena for wide changes. |
| [Interrogate](interrogate/SKILL.md) | Challenge a change and report reproduced findings. | Source/diff tools, runtime probes, and Arena. |
| [Correct](correct/SKILL.md) | Prevent recurring mistakes through architecture, types, lint, tests, and rules. | Source/history tools, Git, and project checks. |
| [Swarm](swarm/SKILL.md) | Fan out parallel workers and return one consolidated report. | Authorized Alpha agent tools; task-specific tools for each worker. |

## Clean Code Review

Example request:

```text
Use $clean-code-review to review this repository, fix clear correctness and
maintainability issues, and report validation and remaining gaps.
```

For findings without edits, say "review only; do not edit files." For a performance
pass, identify the slow workflow and ask for before-and-after evidence.

The skill includes Python, JavaScript/TypeScript, HTML, frontend, testing, and
performance review guides, plus two read-only repository inventory helpers.
Its instructions may lead the agent to edit code and run relevant project checks
when requested. Primary-source research may use web access; the bundled helpers
make no network requests and need no accounts or credentials.

Copy the complete `clean-code-review/` directory when installing manually. See
the [repository installation instructions](../README.md#using-a-skill) for an
installer command and version-pinning guidance.

## Beast Mode pack

```text
Use $beast-mode to fix the CLI losing zero-quantity rows, using the existing
regression checks and keeping the change focused.
```

The pack consists of `beast-mode` and the thirteen companion skills listed above.
Copy each complete directory, including `agents/openai.yaml` and license notices,
to the chosen host-supported location. Alpha supports portable project skills in
`.agents/skills/` and personal skills under the user's `.agents/skills/` directory.
This repository stores the distributable source; it does not install the pack.
Check existing same-name skills before copying; respect the host's resolved
project/global overrides instead of overwriting them blindly.

Beast Mode and the twelve pstack-derived companions use explicit-only invocation
metadata. Deslop retains its upstream automatic-selection default. In Alpha,
invoke Beast Mode through `/beast-mode` or explicitly ask for it; it can load the
named companions as needed even when they are absent from automatic skill lists.
Other hosts may interpret invocation metadata differently.

Beast Mode selects which companions to load. The companions retain the upstream
workflows, including full feature-map audits, proof requirements, retries, and
commit/PR steps. Host permissions and the user's scope govern those operations.
Depending on the skill, they may edit files, run project commands, create helper
scripts, start local apps, or access the project's review records. No executable
scripts, runtime dependencies, credentials, or service integrations are bundled.

The twelve pstack companions come from Lauren Tan's MIT-licensed skills; Deslop
comes from Cursor Team Kit. The original twelve selected companions preserve
upstream wording except for Alpha compatibility and redundant dependency changes.
Arena is a compact adaptation that keeps the shared phases its callers use.
Each folder records the pinned source, license, and changes in `LICENSE.txt`.
Beast Mode is the new coordinator.

## Adding a skill

Discuss a substantial new skill in an issue first. Then create
`skills/<skill-name>/SKILL.md` with YAML frontmatter and instructions:

```markdown
---
name: my-skill
description: Explain what this skill does and when an agent should use it.
license: MIT
---

# My skill

Write focused instructions and a realistic usage example here.
```

The `name` must match the directory name. Bundle referenced scripts, references,
and assets in the same skill directory. See the
[format specification](https://agentskills.io/specification) and
[contribution requirements](../CONTRIBUTING.md).
