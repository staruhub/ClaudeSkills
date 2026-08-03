from pathlib import Path
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_site  # noqa: E402


class SiteValidationTests(unittest.TestCase):
    def test_repository_site_passes(self) -> None:
        self.assertEqual(validate_site.validate_repo(REPO_ROOT), [])

    def test_release_version_is_synchronized(self) -> None:
        self.assertEqual(
            (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip(),
            validate_site.RELEASE_VERSION,
        )
        for filename in ("README.md", "README.zh-CN.md"):
            text = (REPO_ROOT / filename).read_text(encoding="utf-8")
            self.assertIn(validate_site.RELEASE_URL, text)
        for filename in validate_site.SITE_PAGES:
            text = (REPO_ROOT / "site" / filename).read_text(encoding="utf-8")
            self.assertIn(
                f'<meta name="version" content="{validate_site.RELEASE_VERSION}">',
                text,
            )
            self.assertIn(validate_site.RELEASE_URL, text)

    def test_release_validation_rejects_wrong_version_and_missing_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo_root = Path(directory)
            (repo_root / "VERSION").write_text("1.0.1\n", encoding="utf-8")
            (repo_root / "CHANGELOG.md").write_text(
                "## [1.0.1] — unreleased\n",
                encoding="utf-8",
            )
            for filename in ("README.md", "README.zh-CN.md"):
                (repo_root / filename).write_text(
                    f"{validate_site.EXPECTED_SITE_URL}\n",
                    encoding="utf-8",
                )

            release_errors = validate_site.validate_release_version(repo_root)
            readme_errors = validate_site.validate_readmes(repo_root)

        self.assertTrue(any("expected '1.0.0'" in error for error in release_errors))
        self.assertTrue(
            any("missing release 1.0.0 link" in error for error in readme_errors)
        )

    def test_agent_skills_positioning_is_cross_client(self) -> None:
        for filename in ("README.md", "README.zh-CN.md"):
            text = (REPO_ROOT / filename).read_text(encoding="utf-8")
            for marker in validate_site.AGENT_SKILLS_MARKERS:
                self.assertIn(marker, text)
            for phrase in validate_site.LEGACY_EXCLUSIVE_POSITIONING[filename]:
                self.assertNotIn(phrase, text)

        for filename in validate_site.SITE_PAGES:
            text = (REPO_ROOT / "site" / filename).read_text(encoding="utf-8")
            for marker in validate_site.AGENT_SKILLS_MARKERS:
                self.assertIn(marker, text)
            for phrase in validate_site.LEGACY_EXCLUSIVE_POSITIONING[filename]:
                self.assertNotIn(phrase, text)

    def test_invalid_fixture_fails_for_project_path_and_contract(self) -> None:
        fixture = REPO_ROOT / "tests" / "fixtures" / "site-invalid"
        errors = validate_site.validate_repo(fixture)

        self.assertTrue(errors)
        self.assertTrue(
            any("root-relative asset path" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("canonical website link" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("path: ./site" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
