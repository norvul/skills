from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.validate_skills import check_frontmatter, validate_repository


VALID = "---\nname: example-skill\ndescription: Use this skill to demonstrate validation.\n---\n\n# Example\nInstructions.\n"


class SkillValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill = self.root / "skills" / "example-skill"
        self.skill.mkdir(parents=True)
        self.document = self.skill / "SKILL.md"
        self.document.write_text(VALID, encoding="utf-8")

    def test_valid_skill_with_referenced_resources(self):
        resource = self.skill / "references" / "usage guide.md"
        resource.parent.mkdir()
        resource.write_text("# Usage\n", encoding="utf-8")
        self.document.write_text(
            VALID + "\n[Usage](references/usage%20guide.md#usage)\n",
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(self.root), (1, []))

    def test_invalid_metadata_is_rejected(self):
        cases = [
            VALID.replace("name: example-skill", "name: other-skill"),
            VALID.replace("name: example-skill", "name: example--skill"),
            VALID.replace("description: Use this skill to demonstrate validation.", "description: 123"),
            VALID.replace("description: Use this skill to demonstrate validation.", "description: " + "x" * 1025),
            VALID.replace("name: example-skill", "name: [example-skill]"),
            VALID.replace("name: example-skill", "name: example-skill\nname: something-else"),
            VALID.replace("---\n\n#", "metadata: {version: 1}\n---\n\n#"),
            VALID.replace("---\n\n#", "unsupported: value\n---\n\n#"),
            VALID.replace("---\n\n#", "compatibility: " + "x" * 501 + "\n---\n\n#"),
            "---\nname: [\n---\nInstructions.\n",
            "---\n- example\n---\nInstructions.\n",
            "---\nname: example-skill\n",
            "# No frontmatter\n",
            VALID.split("\n\n#")[0] + "\n",
        ]
        for text in cases:
            with self.subTest(text=text[:100]):
                self.assertTrue(check_frontmatter(text, "example-skill"))

    def test_supported_optional_metadata(self):
        text = VALID.replace(
            "---\n\n#",
            'license: MIT\ncompatibility: Requires Python 3.12.\n'
            'allowed-tools: Read\nmetadata: {version: "1.0"}\n---\n\n#',
        )
        self.assertEqual(check_frontmatter(text, "example-skill"), [])

    def test_missing_instruction_file_is_rejected(self):
        self.document.unlink()
        self.assertIn("missing SKILL.md", "\n".join(validate_repository(self.root)[1]))

    def test_broken_links_in_supporting_documents_are_rejected(self):
        (self.skill / "REFERENCE.md").write_text("[Missing](missing.md)", encoding="utf-8")
        self.assertIn("missing linked file", "\n".join(validate_repository(self.root)[1]))

    def test_reference_links_and_images_are_checked(self):
        self.document.write_text(
            VALID + "\n[Guide][guide]\n\n[guide]: missing.md\n\n![Image](missing.png)\n",
            encoding="utf-8",
        )
        self.assertEqual(len(validate_repository(self.root)[1]), 2)

    def test_remote_links_anchors_and_fenced_examples_are_ignored(self):
        self.document.write_text(
            VALID + "\n[Remote](https://example.com/a) [Section](#example)\n"
            "\n```markdown\n[Example](missing.md)\n```\n",
            encoding="utf-8",
        )
        self.assertEqual(validate_repository(self.root), (1, []))

    def test_links_cannot_escape_the_repository_or_use_machine_paths(self):
        for target in ("../../../outside.md", "/etc/passwd", "file:///C:/private.txt", "C:/private.txt"):
            with self.subTest(target=target):
                self.document.write_text(VALID + f"\n[Bad]({target})\n", encoding="utf-8")
                self.assertTrue(validate_repository(self.root)[1])

    def test_empty_library_is_valid_but_unstructured_skill_files_are_not(self):
        self.document.unlink()
        self.skill.rmdir()
        self.assertEqual(validate_repository(self.root), (0, []))
        (self.root / "skills" / "loose.py").write_text("", encoding="utf-8")
        self.assertTrue(validate_repository(self.root)[1])

    def test_invalid_text_encoding_is_rejected(self):
        self.document.write_bytes(b"\xff\xfe\x00")
        self.assertIn("UTF-8", "\n".join(validate_repository(self.root)[1]))


if __name__ == "__main__":
    unittest.main()
