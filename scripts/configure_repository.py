"""Preview or explicitly apply the checked-in settings to norvul/skills."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "norvul/skills"
BASE = f"repos/{REPOSITORY}"
CHECK_NAME = "Validate repository"


def github_api(method: str, endpoint: str, payload=None):
    command = [
        "gh", "api", "--hostname", "github.com", "--method", method, endpoint,
        "-H", "Accept: application/vnd.github+json",
        "-H", "X-GitHub-Api-Version: 2026-03-10",
    ]
    if payload is not None:
        command.extend(["--input", "-"])
    result = subprocess.run(
        command,
        input=json.dumps(payload) if payload is not None else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"{method} {endpoint}: {result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def configuration(root: Path = ROOT):
    def read(relative):
        return json.loads((root / ".github" / relative).read_text(encoding="utf-8"))

    settings = read("repository-settings.json")
    rulesets = [read("rulesets/main.json"), read("rulesets/releases.json")]
    operations = [
        ("PUT", f"{BASE}/vulnerability-alerts", None),
        ("PUT", f"{BASE}/automated-security-fixes", None),
        ("PATCH", BASE, settings),
        ("PUT", f"{BASE}/private-vulnerability-reporting", None),
        ("PUT", f"{BASE}/actions/permissions", {
            "enabled": True, "allowed_actions": "selected", "sha_pinning_required": True,
        }),
        ("PUT", f"{BASE}/actions/permissions/selected-actions", {
            "github_owned_allowed": True, "verified_allowed": False, "patterns_allowed": [],
        }),
        ("PUT", f"{BASE}/actions/permissions/workflow", {
            "default_workflow_permissions": "read", "can_approve_pull_request_reviews": False,
        }),
        ("PUT", f"{BASE}/actions/permissions/fork-pr-contributor-approval", {
            "approval_policy": "all_external_contributors",
        }),
    ]
    return operations, rulesets


def apply_configuration(api=github_api):
    # Complete all preflight checks before the first mutation.
    repository = api("GET", BASE)
    if not repository.get("permissions", {}).get("admin"):
        raise RuntimeError(f"The active GitHub CLI account needs Admin access to {REPOSITORY}.")
    if repository.get("visibility") != "public" or repository.get("default_branch") != "main":
        raise RuntimeError("Expected a public repository with main as its default branch.")

    branch = api("GET", f"{BASE}/branches/main")
    sha = branch["commit"]["sha"]
    checks = api("GET", f"{BASE}/commits/{sha}/check-runs?per_page=100")["check_runs"]
    trusted = [check for check in checks if (
        check["name"] == CHECK_NAME
        and check.get("head_sha") == sha
        and check.get("status") == "completed"
        and check.get("conclusion") == "success"
        and check.get("app", {}).get("slug") == "github-actions"
    )]
    if not trusted:
        raise RuntimeError(f"Wait for {CHECK_NAME!r} to pass on the current main commit first.")
    integration_id = trusted[0]["app"]["id"]
    existing = api("GET", f"{BASE}/rulesets?includes_parents=false&per_page=100")
    operations, rulesets = configuration()
    for ruleset in rulesets:
        if sum(item["name"] == ruleset["name"] for item in existing) > 1:
            raise RuntimeError(f"Resolve duplicate rulesets named {ruleset['name']!r} first.")
        for rule in ruleset["rules"]:
            if rule["type"] == "required_status_checks":
                for check in rule["parameters"]["required_status_checks"]:
                    check["integration_id"] = integration_id

    for method, endpoint, payload in operations:
        api(method, endpoint, payload)
        print(f"Applied {method} {endpoint}")
    for ruleset in rulesets:
        match = next((item for item in existing if item["name"] == ruleset["name"]), None)
        if match:
            api("PUT", f"{BASE}/rulesets/{match['id']}", ruleset)
        else:
            api("POST", f"{BASE}/rulesets", ruleset)
        print(f"Applied ruleset: {ruleset['name']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Apply settings using GitHub CLI admin access.")
    arguments = parser.parse_args()
    if not arguments.apply:
        operations, rulesets = configuration()
        print(json.dumps({"repository": REPOSITORY, "operations": operations, "rulesets": rulesets}, indent=2))
        print("Preview only. Pass --apply to change GitHub settings.")
        return 0
    try:
        apply_configuration()
    except (RuntimeError, OSError) as error:
        print(f"Configuration stopped: {error}", file=sys.stderr)
        return 1
    print("Repository settings applied. Organization two-factor authentication is managed separately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
