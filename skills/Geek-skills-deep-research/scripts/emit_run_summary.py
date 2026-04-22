#!/usr/bin/env python3
"""
Emit a structured run summary for Deep Research V8.

Example:
  python emit_run_summary.py \
    --draft workspace/draft.md \
    --registry workspace/registry.md \
    --evaluation workspace/evaluation.md \
    --output-type full \
    --stakes medium \
    --orchestration lead+subagents \
    --skill-version 8.0 \
    --output workspace/run-summary.json
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


def read_text(path: Optional[str]) -> str:
    if not path:
        return ""
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def count_words(text: str) -> int:
    # Rough word count that works acceptably for mixed English/Chinese reports.
    english_words = re.findall(r"[A-Za-z0-9_'-]+", text)
    cjk_chars = re.findall(r"[\u4e00-\u9fff]", text)
    return len(english_words) + len(cjk_chars)


def extract_citations(text: str) -> List[int]:
    return [int(x) for x in re.findall(r"\[(\d+)\]", text)]


def extract_registry_refs(text: str) -> List[int]:
    refs = []
    for m in re.finditer(r"^\[(\d+)\]", text, flags=re.MULTILINE):
        refs.append(int(m.group(1)))
    return refs


def parse_eval(text: str) -> Dict[str, object]:
    if not text.strip():
        return {
            "evaluation_run": False,
            "evaluation_verdict": None,
            "dimension_scores": {},
        }

    verdict_match = re.search(r"Overall Verdict:\s*(PASS|FAIL)", text)
    verdict = verdict_match.group(1) if verdict_match else None

    dimension_scores: Dict[str, float] = {}
    for line in text.splitlines():
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 5:
            continue
        name, _, score, _, _ = parts[:5]
        m = re.match(r"(\d+(?:\.\d+)?)\s*/\s*10", score)
        if m and name.lower() != "dimension":
            dimension_scores[name] = float(m.group(1))

    return {
        "evaluation_run": True,
        "evaluation_verdict": verdict,
        "dimension_scores": dimension_scores,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit structured run summary JSON.")
    parser.add_argument("--draft", help="Path to draft markdown")
    parser.add_argument("--registry", help="Path to registry markdown")
    parser.add_argument("--evaluation", help="Path to evaluation markdown", default=None)
    parser.add_argument("--output-type", required=True, choices=["brief", "full", "delta"])
    parser.add_argument("--stakes", required=True, choices=["low", "medium", "high"])
    parser.add_argument("--orchestration", required=True, help="single-agent / lead+subagents / delta")
    parser.add_argument("--skill-version", default="8.0")
    parser.add_argument("--search-count", type=int, default=None)
    parser.add_argument("--fetch-count", type=int, default=None)
    parser.add_argument("--used-subagents", action="store_true")
    parser.add_argument("--used-tension-discovery", action="store_true")
    parser.add_argument("--used-landscape-scan", action="store_true")
    parser.add_argument("--used-reverse-search", action="store_true")
    parser.add_argument("--manual-spotcheck-run", action="store_true")
    parser.add_argument("--issues", nargs="*", default=[])
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    draft_text = read_text(args.draft)
    registry_text = read_text(args.registry)
    eval_text = read_text(args.evaluation)

    citations = extract_citations(draft_text)
    registry_refs = extract_registry_refs(registry_text)
    eval_info = parse_eval(eval_text)

    summary = {
        "skill_version": args.skill_version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "output_type": args.output_type,
        "stakes": args.stakes,
        "orchestration_mode": args.orchestration,
        "used_subagents": args.used_subagents,
        "used_tension_discovery": args.used_tension_discovery,
        "used_landscape_scan": args.used_landscape_scan,
        "used_reverse_search": args.used_reverse_search,
        "manual_spotcheck_run": args.manual_spotcheck_run,
        "search_count": args.search_count,
        "fetch_count": args.fetch_count,
        "word_count": count_words(draft_text),
        "citation_count": len(citations),
        "unique_citations": sorted(set(citations)),
        "source_count": len(registry_refs),
        "evaluation_run": eval_info["evaluation_run"],
        "evaluation_verdict": eval_info["evaluation_verdict"],
        "dimension_scores": eval_info["dimension_scores"],
        "issues": args.issues,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Run summary written to {out_path}")


if __name__ == "__main__":
    main()
