from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import install_skill  # noqa: E402


class InstallSkillTests(unittest.TestCase):
    def test_agents_is_the_cross_client_default(self) -> None:
        self.assertEqual(
            install_skill.target_base(
                "agents",
                False,
                home=Path("/home/example"),
            ),
            Path("/home/example/.agents/skills"),
        )

    def test_project_scope_uses_the_selected_client_directory(self) -> None:
        project = Path("/work/project")
        self.assertEqual(
            install_skill.target_base(
                "agents",
                True,
                cwd=project,
            ),
            project / ".agents" / "skills",
        )
        self.assertEqual(
            install_skill.target_base(
                "claude-code",
                True,
                cwd=project,
            ),
            project / ".claude" / "skills",
        )

    def test_claude_code_remains_an_explicit_compatibility_target(self) -> None:
        self.assertEqual(
            install_skill.target_base(
                "claude-code",
                False,
                home=Path("/home/example"),
            ),
            Path("/home/example/.claude/skills"),
        )


if __name__ == "__main__":
    unittest.main()
