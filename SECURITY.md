# Security

## Reporting a vulnerability

Please report vulnerabilities privately through
[GitHub's vulnerability reporting form](https://github.com/norvul/skills/security/advisories/new).
Include the affected skill and commit, reproduction steps, and the likely impact.
Do not include live credentials or other people's private data.

Use ordinary issues for non-sensitive bugs and feature requests. We do not promise
a response deadline, and we do not currently offer a bug bounty.

## Scope and support

Reports about the current `main` branch and the latest release, when one exists,
are in scope. Older versions may require updating to receive a fix.

Skill instructions can cause an agent to run commands, change files, or contact
external services. Review instructions, scripts, dependencies, and requested access
before enabling a skill. Test unfamiliar behavior in an isolated environment with
no production credentials.

Repository validation checks format and file links. It does not execute skills or
guarantee safe behavior. Maintainers review instruction changes, network access,
and executable code before merging.
