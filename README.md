# Norvul AI Skills

Practical AI agent skills built and used at Norvul AI.

This is a curated collection: contributions are welcome, and maintainers review
what becomes part of the published library.

## Skills

| Skill | Purpose |
| --- | --- |
| [Clean Code Review](skills/clean-code-review/SKILL.md) | Review correctness, maintainability, security, stale code, and performance; make bounded fixes and report the evidence. |

See the [skill catalog](skills/README.md) for requirements and an example request.

## Using a skill

Skills follow the [Agent Skills format](https://agentskills.io/specification).
With Node.js 22.20+ installed, you can use the
[skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add norvul/skills --skill clean-code-review
```

Or install a skill manually:

1. Read its `SKILL.md`, included scripts, and dependency requirements.
2. Copy that skill's complete directory into your agent's supported skills location.
3. Follow your agent's instructions for enabling the skill.

Read the skill before installing it through either method. Code review skills may
edit source files and run project checks within the scope of your request.

For a reproducible installation, use a specific commit or version tag. `main`
contains the latest accepted changes. Release tags will identify published
milestones; no releases have been published yet.

## Contributing

Bug reports, focused fixes, and improvements are welcome. Please discuss a
substantial new skill in an issue before implementing it.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and local checks, and
[SECURITY.md](SECURITY.md) for private security reporting.

## License

[MIT](LICENSE). Contributions must be compatible with that license, and any
third-party material must retain its own required notices.
