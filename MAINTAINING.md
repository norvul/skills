# Maintaining this repository

`main` contains accepted skills. Work on short-lived branches, open pull requests,
review the entire diff, and squash merge after the `Validate repository` check
passes. Delete merged branches. Substantial new skills should start with an issue.

## Access and review

`norvul-admin` is the initial maintainer and code owner. Public contributors use
forks and pull requests; they do not need repository write access. Give issue
helpers Triage access and reserve write/admin access for trusted maintainers.

While there is one maintainer, pull requests are required but the required approval
count is zero so the maintainer can merge their own work. Manually review external
pull requests before merging. Once a second trusted maintainer is active, change
the required approval count to one and require code-owner review where useful.
Never give an automation routine permission to approve or merge unreviewed skills.

## Repository settings

Desired settings are checked into `.github/repository-settings.json` and
`.github/rulesets/`. These files describe settings; GitHub does not apply them
automatically. Preview the configuration:

```sh
python scripts/configure_repository.py
```

After the initial commit is on `main` and its GitHub Actions validation succeeds,
an authenticated repository administrator can apply or reapply the configuration:

```sh
python scripts/configure_repository.py --apply
```

The script checks admin access and a successful validation run on the current
`main` commit before making changes. It updates matching Norvul rulesets by name
and preserves unrelated rulesets. It enables:

- Required pull requests, resolved review threads, a linear history, and the
  `Validate repository` status check, bound to the GitHub Actions app.
- Blocked force pushes and deletion of `main`, with no routine bypass actors.
- Protected `v*` release tags: new tags can be created, but existing ones cannot
  be moved or deleted without changing the ruleset.
- Squash merging, automatic deletion of merged branches, and public issues.
- Read-only workflow defaults, no workflow PR approvals, full-SHA action pinning,
  and workflow approval for all external contributors.
- Secret scanning, secret push protection, dependency vulnerability alerts,
  automated dependency security fixes, and private vulnerability reporting.

The script does not change repository visibility, invite collaborators, change
organization membership, or configure account authentication. Keep organization
base permissions at Read or None. Require two-factor authentication in the Norvul
organization's Authentication security settings; account enrollment is managed by
each person, not by this repository script.

GitHub Actions runs on hosted runners with no repository secrets and does not
execute submitted skill scripts. Review workflow and dependency changes before
approving an external contributor's workflow run. Dependency update pull requests
also require normal review and validation.

## Releases

Publish a version tag such as `v0.1.0` only when there are useful skills ready for a
release. Point it at an accepted `main` commit and write release notes identifying
added skills, behavior changes, new dependencies, and compatibility changes. Offer
version tags or full commit hashes for reproducible installations. Never move a
published version tag; publish a new version instead.
