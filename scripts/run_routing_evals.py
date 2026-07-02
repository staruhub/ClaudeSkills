#!/usr/bin/env python3
"""Skill routing evals: L1 validation and L2 prompt bundling.

Usage:
  python3 scripts/run_routing_evals.py                 # L1: validate all eval files
  python3 scripts/run_routing_evals.py --emit-prompts  # L2: print agent test bundle

L1 checks (deterministic, exit 1 on error):
  - required fields: id / prompt / should_trigger / reason
  - optional fields: boundary / route_to / expected_mode (unknown fields -> warning)
  - ids globally unique
  - route_to target skill directory exists (or "none");
    warning if the target skill has no evals file yet
  - identical prompt across skills expected true by >1 skill -> error,
    unless every such case is marked boundary (mutex-pair mixed cases)

L2 (--emit-prompts) prints two sections:
  - PROMPTS: skill descriptions + shuffled-free numbered prompts, for a
    fresh subagent that judges which skill (or none) should trigger
  - ANSWER KEY: expected results, for the scorer only
Run the agent 3+ times before trusting a description change (single samples lie).
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"
PREFIX = "Geek-skills-"
REQUIRED = {"id", "prompt", "should_trigger", "reason"}
OPTIONAL = {"boundary", "route_to", "expected_mode"}


def short_name(skill_dir_name: str) -> str:
    return skill_dir_name.removeprefix(PREFIX)


def load_all():
    """Return {short_name: (path, cases)} for every routing-evals.json."""
    out = {}
    for path in sorted(SKILLS_DIR.glob("*/evals/routing-evals.json")):
        name = short_name(path.parent.parent.name)
        with open(path, encoding="utf-8") as fh:
            out[name] = (path, json.load(fh))
    return out


def read_description(skill: str) -> str:
    """Extract frontmatter description (single-line or folded '>') from SKILL.md."""
    path = SKILLS_DIR / f"{PREFIX}{skill}" / "SKILL.md"
    if not path.exists():
        return "(SKILL.md not found)"
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return "(no frontmatter)"
    lines = m.group(1).splitlines()
    desc, capture = [], False
    for line in lines:
        if line.startswith("description:"):
            rest = line.split(":", 1)[1].strip()
            capture = True
            if rest and rest != ">":
                desc.append(rest)
            continue
        if capture:
            if line.startswith("  "):
                desc.append(line.strip())
            else:
                break
    return " ".join(desc) or "(empty description)"


def validate(data) -> int:
    errors, warnings = [], []
    seen_ids = {}
    prompt_truth = {}  # prompt -> [(skill, should_trigger, boundary)]

    for skill, (path, cases) in data.items():
        rel = path.relative_to(REPO)
        if not isinstance(cases, list):
            errors.append(f"{rel}: top level must be a JSON array")
            continue
        for case in cases:
            cid = case.get("id", "<missing-id>")
            missing = REQUIRED - case.keys()
            if missing:
                errors.append(f"{rel}:{cid}: missing fields {sorted(missing)}")
            unknown = case.keys() - REQUIRED - OPTIONAL
            if unknown:
                warnings.append(f"{rel}:{cid}: unknown fields {sorted(unknown)}")
            if not isinstance(case.get("should_trigger"), bool):
                errors.append(f"{rel}:{cid}: should_trigger must be boolean")
            if cid in seen_ids:
                errors.append(f"{rel}:{cid}: duplicate id (also in {seen_ids[cid]})")
            seen_ids[cid] = skill

            route = case.get("route_to")
            if route and route != "none":
                target = SKILLS_DIR / f"{PREFIX}{route}"
                if not target.is_dir():
                    errors.append(f"{rel}:{cid}: route_to '{route}' has no skill directory")
                elif not (target / "evals" / "routing-evals.json").exists():
                    warnings.append(f"{rel}:{cid}: route_to '{route}' has no evals yet (mirror missing)")

            prompt_truth.setdefault(case.get("prompt", ""), []).append(
                (skill, case.get("should_trigger"), bool(case.get("boundary")))
            )

    for prompt, hits in prompt_truth.items():
        trues = [h for h in hits if h[1]]
        if len(trues) > 1 and not all(h[2] for h in trues):
            names = ", ".join(f"{s}" for s, _, _ in trues)
            errors.append(f"conflict: prompt claimed true by [{names}] without boundary flag: {prompt[:40]}...")

    total = sum(len(c) for _, c in data.values())
    print(f"checked {total} cases across {len(data)} skills")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if not errors:
        print("L1 PASS")
    return 1 if errors else 0


def emit_prompts(data) -> int:
    skills = sorted(data)
    # route_to targets must also be visible candidates, or the agent
    # cannot possibly produce the expected answer for handoff cases
    candidates = set(skills)
    for _, cases in data.values():
        for case in cases:
            route = case.get("route_to")
            if route and route != "none" and (SKILLS_DIR / f"{PREFIX}{route}").is_dir():
                candidates.add(route)
    print("# Routing eval bundle\n")
    print("## PROMPTS (give this section to a fresh agent)\n")
    print("你是 Claude Code 的 skill 路由器。已安装以下 skill（只有 description 可见）。")
    print("对每条用户输入，判断应触发哪个 skill；都不合适则回答 none。")
    print('只输出 JSON 数组：[{"n": 1, "skill": "<name-or-none>"}, ...]\n')
    for s in sorted(candidates):
        print(f"- **{s}**: {read_description(s)}")
    print()
    n = 0
    key = []
    for s in skills:
        for case in data[s][1]:
            n += 1
            print(f"{n}. {case['prompt']}")
            expected = s if case["should_trigger"] else case.get("route_to", "none")
            key.append((n, case["id"], expected, bool(case.get("boundary"))))
    print("\n## ANSWER KEY (scorer only, do not show to the agent)\n")
    for n, cid, expected, boundary in key:
        flag = " [boundary]" if boundary else ""
        print(f"{n}. {cid} -> {expected}{flag}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--emit-prompts", action="store_true", help="print L2 agent test bundle")
    args = ap.parse_args()
    data = load_all()
    if not data:
        print("no routing-evals.json found under skills/*/evals/")
        return 1
    return emit_prompts(data) if args.emit_prompts else validate(data)


if __name__ == "__main__":
    sys.exit(main())
