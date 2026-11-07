# Skill catalog

No skills have been published yet.

Each accepted skill will live in its own directory here and have a catalog entry
with its purpose, requirements, and a usage example. The root `README.md` is not
itself an installable skill.

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
