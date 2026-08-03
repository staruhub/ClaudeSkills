#!/usr/bin/env python3
"""Install a curated Agent Skill under a clean directory name.

By default, this installer uses the cross-client `.agents/skills/` convention.
Use `--client claude-code` when you specifically want Claude Code's native
`.claude/skills/` location. The source prefix is stripped in either case, so
`skills/Geek-skills-<x>/` is installed as `<x>/`.

Usage:
  python3 scripts/install_skill.py <name> [--client agents|claude-code]
      [--project] [--force] [--dry-run]
  python3 scripts/install_skill.py --list

  <name>        short skill name (e.g. deep-research) or full dir name
  --client      target `agents` (default) or `claude-code`
  --project     install in the current project instead of the user home
  --force       overwrite an existing install
  --dry-run     print what would happen, do nothing
  --list        list installable skills and exit
"""

import argparse
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"
PREFIX = "Geek-skills-"
CLIENT_DIRECTORIES = {
    "agents": ".agents",
    "claude-code": ".claude",
}


def installable():
    """Return {short_name: source_path} for every curated skill."""
    out = {}
    for d in sorted(SKILLS_DIR.glob(f"{PREFIX}*")):
        if (d / "SKILL.md").exists():
            out[d.name.removeprefix(PREFIX)] = d
    return out


def resolve(name, skills):
    short = name.removeprefix(PREFIX)
    if short in skills:
        return short, skills[short]
    return None, None


def target_base(client, project, *, cwd=None, home=None):
    """Return the client skill directory without touching the filesystem."""
    root = (cwd or Path.cwd()) if project else (home or Path.home())
    return root / CLIENT_DIRECTORIES[client] / "skills"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", nargs="?", help="skill name (short or full dir name)")
    ap.add_argument(
        "--client",
        choices=tuple(CLIENT_DIRECTORIES),
        default="agents",
        help="installation target (default: agents)",
    )
    ap.add_argument(
        "--project",
        action="store_true",
        help="install for the current project instead of the user",
    )
    ap.add_argument("--force", action="store_true", help="overwrite existing install")
    ap.add_argument("--dry-run", action="store_true", help="print actions only")
    ap.add_argument("--list", action="store_true", help="list installable skills")
    args = ap.parse_args()

    skills = installable()

    if args.list or not args.name:
        print(f"{len(skills)} installable Agent Skills:")
        for short in skills:
            print(f"  {short}")
        return 0 if args.list else 1

    short, src = resolve(args.name, skills)
    if not src:
        print(f"unknown skill: {args.name}\nrun --list to see available names")
        return 1

    base = target_base(args.client, args.project)
    dest = base / short

    if dest.exists() and not args.force:
        print(f"already installed: {dest}\nuse --force to overwrite")
        return 1

    print(f"install {src.relative_to(REPO)} -> {dest}")
    if args.dry_run:
        print("(dry-run, nothing written)")
        return 0

    base.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "._*"))
    if args.client == "claude-code":
        print(f"installed for Claude Code. slash command: /{short}")
    else:
        print("installed for skills-compatible agents. invocation depends on the client.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
