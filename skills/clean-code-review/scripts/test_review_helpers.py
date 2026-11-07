"""Run reviewed helper behavior checks against disposable local fixtures."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import find_stale_scripts as stale
import inventory_repo_surface as inventory


class ReviewHelperTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory(prefix="norvul-review-helper-")
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name).resolve()
        self.root = self.workspace / "repository"
        self.root.mkdir()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_script_to_script_references_count_but_self_references_do_not(self):
        self.write("scripts/run.sh", "#!/bin/sh\npython scripts/task.py\n")
        self.write("scripts/task.py", "print('task')\n")
        self.write("scripts/unused.py", "# scripts/unused.py is this file.\n")
        files = stale.iter_repo_files(self.root)
        candidates = stale.collect_candidates(self.root, files)
        stale.scan_references(self.root, files, candidates)
        records = {record.rel_path: record for record in candidates}
        self.assertEqual(records["scripts/task.py"].path_refs, {"scripts/run.sh"})
        self.assertNotEqual(records["scripts/task.py"].status, "likely-stale")
        self.assertEqual(records["scripts/unused.py"].status, "likely-stale")

    def test_git_history_is_optional_when_git_is_not_installed(self):
        with patch.object(stale.subprocess, "run", side_effect=FileNotFoundError):
            self.assertFalse(stale.git_available(self.root))

    def test_backend_source_folders_do_not_imply_a_frontend(self):
        self.write("src/app.py", "def serve(): pass\n")
        self.write("src/server.ts", "export function serve() {}\n")
        files = inventory.iter_repo_files(self.root)
        surfaces = inventory.detect_surfaces(self.root, files)
        self.assertFalse(surfaces["frontend"].paths)
        passes = inventory.suggested_review_passes(inventory.detect_languages(files), surfaces)
        self.assertIn("references/python-review-guide.md", passes)
        self.assertIn("references/javascript-review-guide.md", passes)
        self.assertNotIn("references/frontend-clean-code-extension.md", passes)

    def test_ui_files_still_select_the_frontend_review(self):
        self.write("src/App.tsx", "export function App() { return <main />; }\n")
        self.write("src/app.css", "main { display: block; }\n")
        files = inventory.iter_repo_files(self.root)
        surfaces = inventory.detect_surfaces(self.root, files)
        self.assertEqual(set(surfaces["frontend"].paths), {"src/App.tsx", "src/app.css"})
        self.assertIn(
            "references/frontend-clean-code-extension.md",
            inventory.suggested_review_passes(inventory.detect_languages(files), surfaces),
        )

    def test_ordinary_library_modules_are_not_assumed_to_be_executable_scripts(self):
        module = self.write("package/module.py", "def helper(): pass\n")
        if os.name != "nt":
            module.chmod(0o644)
        self.assertFalse(stale.is_candidate_script(self.root, module))

    def test_generated_directories_are_excluded(self):
        self.write(".venv/scripts/ignored.py", "print('generated')\n")
        kept = self.write("scripts/kept.py", "print('kept')\n")
        for helper in (stale, inventory):
            with self.subTest(helper=helper.__name__):
                self.assertEqual(helper.iter_repo_files(self.root), [kept])

    def test_symbolic_links_do_not_read_outside_the_requested_root(self):
        outside = self.workspace / "outside.py"
        outside.write_text("print('outside')\n", encoding="utf-8")
        link = self.root / "linked.py"
        try:
            link.symlink_to(outside)
        except OSError as error:
            self.skipTest(f"Symbolic links are unavailable on this host: {error}")
        for helper in (stale, inventory):
            with self.subTest(helper=helper.__name__):
                self.assertEqual(helper.iter_repo_files(self.root), [])

    def test_both_clis_reject_a_file_as_the_repository_root(self):
        root_file = self.write("README.md", "# A file is not a repository directory.\n")
        for helper in (stale, inventory):
            with self.subTest(helper=helper.__name__):
                result = subprocess.run(
                    [sys.executable, helper.__file__, "--root", str(root_file), "--json"],
                    capture_output=True, text=True, timeout=10, check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("directory", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_both_clis_emit_json_without_changing_the_scanned_files(self):
        self.write("README.md", "Run scripts/task.py to perform the task.\n")
        self.write("scripts/task.py", "print('task')\n")
        before = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        for helper in (stale, inventory):
            with self.subTest(helper=helper.__name__):
                result = subprocess.run(
                    [sys.executable, helper.__file__, "--root", str(self.root), "--json"],
                    capture_output=True, text=True, timeout=10, check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(Path(payload["root"]), self.root)
                if helper is stale:
                    self.assertEqual(payload["candidate_count"], 1)
                    self.assertEqual(payload["results"][0]["sample_refs"], ["README.md"])
                else:
                    self.assertEqual(payload["languages"], {"python": 1})
                    self.assertEqual(payload["surfaces"]["scripts"]["count"], 1)
        after = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
