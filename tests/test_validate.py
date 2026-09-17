"""Tests of repository checks, not evaluations of an assistant's behavior."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate", ROOT / "scripts/validate.py")
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class FrontmatterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = (ROOT / validator.SKILL).read_text(encoding="utf-8")

    def test_valid_metadata(self) -> None:
        fields, body = validator.parse_skill(self.text)
        self.assertEqual(fields["name"], "the-perfection-system")
        self.assertTrue(body.startswith("# The Perfection System"))

    def test_invalid_names(self) -> None:
        for name in ("UPPERCASE", "two--hyphens", "-leading", "trailing-", "x" * 65):
            with self.subTest(name=name), self.assertRaises(ValueError):
                validator.parse_skill(self.text.replace("name: the-perfection-system", f"name: {name}"))

    def test_duplicate_field(self) -> None:
        with self.assertRaises(ValueError):
            validator.parse_skill(self.text.replace("name: the-perfection-system", "name: the-perfection-system\nname: duplicate"))

    def test_missing_frontmatter(self) -> None:
        with self.assertRaises(ValueError):
            validator.parse_skill("# A body with no frontmatter\n")

    def test_unclosed_frontmatter(self) -> None:
        with self.assertRaises(ValueError):
            validator.parse_skill('---\nname: sample\ndescription: "test"\n')

    def test_description_constraints(self) -> None:
        for description in ('""', '"   "', "null", '"' + "x" * 1025 + '"', "unquoted"):
            with self.subTest(description=description[:20]), self.assertRaises(ValueError):
                validator.parse_skill(f"---\nname: sample\ndescription: {description}\n---\nBody\n")

    def test_missing_description(self) -> None:
        with self.assertRaises(ValueError):
            validator.parse_skill("---\nname: sample\n---\nBody\n")

    def test_empty_body(self) -> None:
        with self.assertRaises(ValueError):
            validator.parse_skill('---\nname: sample\ndescription: "test"\n---\n\n')

    def test_standalone_rebases_links(self) -> None:
        standalone = validator.standalone_text(self.text)
        self.assertNotIn("\nname: the-perfection-system\n", standalone)
        self.assertIn("](skills/the-perfection-system/references/review-protocol.md)", standalone)
        self.assertIn("](skills/the-perfection-system/assets/run-template.md)", standalone)


class RepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repository"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def test_repository_passes(self) -> None:
        self.assertEqual(validator.validate(self.root), [])

    def test_stale_standalone(self) -> None:
        (self.root / validator.STANDALONE).write_text("stale\n", encoding="utf-8")
        self.assertTrue(any("stale" in e for e in validator.validate(self.root)))

    def test_missing_resource(self) -> None:
        (self.root / validator.SKILL.parent / "assets/run-template.md").unlink()
        self.assertTrue(any("missing required file" in e for e in validator.validate(self.root)))

    def test_broken_link(self) -> None:
        with (self.root / "README.md").open("a", encoding="utf-8") as output:
            output.write("\n[Broken](missing.md)\n")
        self.assertTrue(any("broken relative link" in e for e in validator.validate(self.root)))

    def test_link_escape(self) -> None:
        with (self.root / "README.md").open("a", encoding="utf-8") as output:
            output.write("\n[Escape](../outside.md)\n")
        self.assertTrue(any("link leaves repository" in e for e in validator.validate(self.root)))

    def test_required_symlink_rejected(self) -> None:
        path = self.root / "CHANGELOG.md"
        path.unlink()
        try:
            path.symlink_to(self.root / "README.md")
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable on this platform")
        self.assertTrue(any("regular file" in e for e in validator.validate(self.root)))

    def test_invalid_json(self) -> None:
        (self.root / "tests/scenarios.json").write_text("not JSON", encoding="utf-8")
        self.assertTrue(validator.validate(self.root))


class ScenarioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = json.loads((ROOT / "tests/scenarios.json").read_text(encoding="utf-8"))

    def test_valid_scenarios(self) -> None:
        self.assertEqual(validator.validate_scenarios(self.cases), [])

    def test_duplicate_id(self) -> None:
        cases = copy.deepcopy(self.cases)
        cases.append(cases[0])
        self.assertTrue(any("duplicate id" in e for e in validator.validate_scenarios(cases)))

    def test_missing_expectations(self) -> None:
        cases = copy.deepcopy(self.cases)
        cases[0]["expect"] = []
        self.assertTrue(validator.validate_scenarios(cases))

    def test_malformed_case(self) -> None:
        self.assertTrue(validator.validate_scenarios([{"id": "incomplete"}]))

    def test_wrong_root_types(self) -> None:
        for value in (None, {}, "text", 1, []):
            with self.subTest(value=value):
                self.assertTrue(validator.validate_scenarios(value))

    def test_wrong_field_types(self) -> None:
        cases = copy.deepcopy(self.cases)
        cases[0]["id"] = []
        cases[0]["expect"] = [None]
        self.assertTrue(validator.validate_scenarios(cases))


if __name__ == "__main__":
    unittest.main()
