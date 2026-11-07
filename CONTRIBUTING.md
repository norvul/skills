# Contributing

We welcome bug reports, focused fixes, and improvements to existing skills.
For a substantial new skill, open an issue first so we can agree on scope.
Inclusion depends on maintainer review, practical usefulness, and fit with the
collection. Please keep discussion respectful and feedback specific.

## Proposing a change

1. Fork the repository and create a short-lived branch, such as `fix/clearer-usage`.
2. Keep the pull request focused on one change.
3. Run the checks below, and describe any behavior you tested manually.
4. Open a pull request against `main` and address review feedback.

You do not need write access to contribute. Maintainers merge accepted changes
using squash merges. We use `main` as the only permanent branch.

## Local checks

Use Python 3.12 or newer in a virtual environment. On Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```sh
python3 -m venv .venv
. .venv/bin/activate
```

Then run:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate_skills.py
```

These checks validate metadata and relative Markdown file links. They do not
execute submitted skills or establish that a skill is safe or effective.

## Skill requirements

- Put each skill in `skills/<skill-name>/SKILL.md`, following the
  [Agent Skills specification](https://agentskills.io/specification).
- Explain when to use it, the steps it follows, and at least one usage example.
- Document required tools, accounts, network destinations, and expected side effects.
- Include referenced files and use portable relative links.
- Keep the main instructions focused; move supporting material into referenced files.
- Include a realistic example of how you tried a behavior change. Add focused
  automated tests when scripts have behavior that benefits from them.
- Do not include credentials, private data, personal machine paths, or material
  you do not have permission to distribute.
- Make external downloads and commands explicit. Do not hide executable behavior
  in instructions, examples, or installation steps.

Add accepted skills to the catalog in `skills/README.md`. Use the pull request
template to explain commands, permissions, dependencies, and external services.

## Licensing

By contributing, you agree to license your contribution under this repository's
[MIT license](LICENSE). Identify third-party material and preserve its license
and attribution requirements. Discuss incompatible licensing before submitting.

Report security problems using [SECURITY.md](SECURITY.md), rather than a public issue.
