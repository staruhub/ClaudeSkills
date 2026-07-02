#!/usr/bin/env python3
"""Install a curated skill under a clean command name.

The Claude Code slash command comes from the *installed directory name*, not
the frontmatter `name`. This installer copies `skills/Geek-skills-<x>/` to the
target as `<x>/` (prefix stripped) so the command is `/<x>` — no manual rename,
no `dist/` duplication in the repo.

Usage:
  python3 scripts/install_skill.py <name> [--project] [--force] [--dry-run]
  python3 scripts/install_skill.py --list

  <name>        short skill name (e.g. deep-research) or full dir name
  --project     install to ./.claude/skills/ instead of ~/.claude/skills/
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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", nargs="?", help="skill name (short or full dir name)")
    ap.add_argument("--project", action="store_true", help="install to ./.claude/skills/")
    ap.add_argument("--force", action="store_true", help="overwrite existing install")
    ap.add_argument("--dry-run", action="store_true", help="print actions only")
    ap.add_argument("--list", action="store_true", help="list installable skills")
    args = ap.parse_args()

    skills = installable()

    if args.list or not args.name:
        print(f"{len(skills)} installable skills (command = /<name>):")
        for short in skills:
            print(f"  /{short}")
        return 0 if args.list else 1

    short, src = resolve(args.name, skills)
    if not src:
        print(f"unknown skill: {args.name}\nrun --list to see available names")
        return 1

    base = (Path.cwd() / ".claude" / "skills") if args.project else (Path.home() / ".claude" / "skills")
    dest = base / short

    if dest.exists() and not args.force:
        print(f"already installed: {dest}\nuse --force to overwrite")
        return 1

    print(f"install {src.relative_to(REPO)} -> {dest}  (command: /{short})")
    if args.dry_run:
        print("(dry-run, nothing written)")
        return 0

    base.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "._*"))
    print(f"installed. invoke with /{short}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
