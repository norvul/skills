import unittest

from scripts.configure_repository import BASE, CHECK_NAME, apply_configuration


class FakeGitHub:
    def __init__(self, *, admin=True, validation_passes=True, existing=None):
        self.admin = admin
        self.validation_passes = validation_passes
        self.existing = existing or []
        self.writes = []

    def __call__(self, method, endpoint, payload=None):
        if method != "GET":
            self.writes.append((method, endpoint, payload))
            return {}
        if endpoint == BASE:
            return {"permissions": {"admin": self.admin}, "visibility": "public", "default_branch": "main"}
        if endpoint.endswith("/branches/main"):
            return {"commit": {"sha": "current-main"}}
        if "/check-runs?" in endpoint:
            return {"check_runs": [{
                "name": CHECK_NAME,
                "head_sha": "current-main",
                "status": "completed",
                "conclusion": "success" if self.validation_passes else "failure",
                "app": {"slug": "github-actions", "id": 1234},
            }]}
        if "/rulesets?" in endpoint:
            return self.existing
        raise AssertionError(f"Unexpected request: {method} {endpoint}")


class RepositoryConfigurationTests(unittest.TestCase):
    def test_no_mutation_without_admin_access(self):
        api = FakeGitHub(admin=False)
        with self.assertRaisesRegex(RuntimeError, "Admin access"):
            apply_configuration(api)
        self.assertEqual(api.writes, [])

    def test_no_mutation_without_successful_main_validation(self):
        api = FakeGitHub(validation_passes=False)
        with self.assertRaisesRegex(RuntimeError, "current main"):
            apply_configuration(api)
        self.assertEqual(api.writes, [])

    def test_status_check_is_bound_to_the_observed_actions_app(self):
        api = FakeGitHub()
        apply_configuration(api)
        main = next(payload for _, endpoint, payload in api.writes if (
            endpoint.endswith("/rulesets") and payload["target"] == "branch"
        ))
        rule = next(rule for rule in main["rules"] if rule["type"] == "required_status_checks")
        self.assertEqual(rule["parameters"]["required_status_checks"], [
            {"context": CHECK_NAME, "integration_id": 1234},
        ])
        self.assertEqual(main["bypass_actors"], [])

    def test_reapplication_updates_matching_rulesets_and_preserves_others(self):
        api = FakeGitHub(existing=[
            {"id": 1, "name": "Norvul main protection"},
            {"id": 2, "name": "Norvul release tag protection"},
            {"id": 3, "name": "Unrelated rule"},
        ])
        apply_configuration(api)
        updates = [(method, endpoint) for method, endpoint, _ in api.writes if "/rulesets" in endpoint]
        self.assertEqual(updates, [("PUT", f"{BASE}/rulesets/1"), ("PUT", f"{BASE}/rulesets/2")])

    def test_duplicate_names_stop_before_any_mutation(self):
        api = FakeGitHub(existing=[
            {"id": 1, "name": "Norvul main protection"},
            {"id": 2, "name": "Norvul main protection"},
        ])
        with self.assertRaisesRegex(RuntimeError, "duplicate"):
            apply_configuration(api)
        self.assertEqual(api.writes, [])


if __name__ == "__main__":
    unittest.main()
