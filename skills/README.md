# Skill catalog

| Skill | Purpose | Requirements |
| --- | --- | --- |
| [Clean Code Review](clean-code-review/SKILL.md) | Audit code repositories, make focused fixes, and report validation and remaining gaps. | An agent with file and shell access. Bundled helpers require Python 3.10+ with no extra packages; Git is optional for history. |

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
