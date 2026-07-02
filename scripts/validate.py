#!/usr/bin/env python3
"""Structural L1 assertions for every curated skill (Skill Quality Standard v1.0).

Usage: python3 scripts/validate.py

Checks per skills/Geek-skills-*/SKILL.md:
  gates (ERROR, exit 1):
    - frontmatter present with name + description
    - description <= 1024 chars
    - SKILL.md <= 500 lines
    - no platform-hardcoded paths (/mnt/skills, /mnt/user-data, /home/claude)
    - no orphan files: everything under references/ assets/ scripts/
      style-library/ templates/ evals/ must be mentioned by basename
      somewhere in the skill's .md/.json files
  quality (WARN):
    - SKILL.md > 300 lines (still passing, but over the full-score line)
    - missing 三件套 sections: 验收标准/自查, 不做什么/不用于, 陷阱
    - name not lowercase kebab-case (Geek-skills- prefix tolerated)
    - CVE ids other than whitelisted historical examples

Run scripts/run_routing_evals.py separately for eval-file consistency.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = sorted((REPO / "skills").glob("Geek-skills-*/"))
ASSET_DIRS = ["references", "assets", "scripts", "style-library", "templates", "evals"]
IGNORE_BASENAMES = re.compile(r"^\.|\.pyc$|__pycache__")
PLATFORM_PATHS = ("/mnt/skills", "/mnt/user-data", "/home/claude")
CVE_WHITELIST = {"CVE-2021-44228"}  # historical class examples allowed
SANJIANTAO = [
    ("验收标准|自查|自检|should produce", "验收标准"),
    ("不做什么|不用于|Do not use|不触发|#+ 不做|请改用|When NOT to use", "不做什么/负触发"),
    ("陷阱|Common Mistakes|特有缺陷|反翻译腔|Degraded mode|Stop conditions|优雅降级|AI抵抗", "已知陷阱/失败处理"),
]


def main() -> int:
    errors, warnings = [], []
    for skill_dir in SKILLS:
        name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{name}: SKILL.md missing")
            continue
        text = skill_md.read_text(encoding="utf-8")
        lines = text.count("\n") + 1

        fm = re.match(r"^---\n(.*?)\n---", text, re.S)
        if not fm:
            errors.append(f"{name}: no frontmatter")
        else:
            body = fm.group(1)
            m_name = re.search(r"^name:\s*(\S+)", body, re.M)
            if not m_name:
                errors.append(f"{name}: frontmatter missing name")
            elif not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*", m_name.group(1)):
                errors.append(f"{name}: frontmatter name not kebab-case: {m_name.group(1)}")
            elif m_name.group(1) != m_name.group(1).lower():
                warnings.append(f"{name}: name not all-lowercase ({m_name.group(1)}) — tolerated legacy prefix")
            desc = re.search(r"^description:\s*(.*?)(?=^\w+:|\Z)", body, re.M | re.S)
            if not desc or not desc.group(1).strip():
                errors.append(f"{name}: frontmatter missing description")
            elif len(" ".join(desc.group(1).split())) > 1024:
                errors.append(f"{name}: description > 1024 chars")

        if lines > 500:
            errors.append(f"{name}: SKILL.md {lines} lines > 500 hard cap")
        elif lines > 300:
            warnings.append(f"{name}: SKILL.md {lines} lines > 300 full-score line")

        for p in PLATFORM_PATHS:
            if p in text:
                errors.append(f"{name}: platform-hardcoded path {p}")

        for cve in set(re.findall(r"CVE-\d{4}-\d{4,7}", text)) - CVE_WHITELIST:
            warnings.append(f"{name}: non-whitelisted CVE id {cve} (staleness risk)")

        for pattern, label in SANJIANTAO:
            if not re.search(pattern, text):
                warnings.append(f"{name}: missing {label}")

        # orphan check: search all md/json in the skill dir for each asset basename
        haystack = "\n".join(
            f.read_text(encoding="utf-8", errors="ignore")
            for f in skill_dir.rglob("*")
            if f.is_file() and f.suffix in (".md", ".json")
        )
        for adir in ASSET_DIRS:
            base = skill_dir / adir
            if not base.is_dir():
                continue
            for f in base.rglob("*"):
                if not f.is_file() or IGNORE_BASENAMES.search(f.name):
                    continue
                if f.name not in haystack:
                    errors.append(f"{name}: orphan file {f.relative_to(skill_dir)}")

    prefix_warns = [w for w in warnings if "tolerated legacy prefix" in w]
    warnings = [w for w in warnings if "tolerated legacy prefix" not in w]
    print(f"validated {len(SKILLS)} skills")
    if prefix_warns:
        print(f"NOTE  {len(prefix_warns)} skills use legacy 'Geek-skills-' capitalized prefix (governance decision pending)")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print("L1 PASS" if not errors else f"L1 FAIL ({len(errors)} errors)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
