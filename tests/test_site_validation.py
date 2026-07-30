from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_site  # noqa: E402


class SiteValidationTests(unittest.TestCase):
    def test_repository_site_passes(self) -> None:
        self.assertEqual(validate_site.validate_repo(REPO_ROOT), [])

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
