#!/usr/bin/env python3
"""
Citation Verifier V2 — Check report citations against source pool.

Usage:
    python verify_citations.py report.md sources.json [--output results.json]

Checks:
1. Every [n] in report has a matching reference entry
2. Every reference URL exists in the source pool (not invented)
3. No dangling references (in list but never cited)
4. Citation numbering is sequential with no gaps
5. Source concentration check (no single source > 25%)

URL matching uses domain + path segments for robust comparison,
not naive prefix matching.
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """Normalize URL for comparison: lowercase, strip trailing slash, remove fragments."""
    url = url.strip().rstrip("/").lower()
    # Remove fragment
    url = re.sub(r"#.*$", "", url)
    # Remove common tracking params
    url = re.sub(r"[?&](utm_\w+|ref|source|fbclid|gclid)=[^&]*", "", url)
    # Clean up leftover ? or &
    url = re.sub(r"\?$", "", url)
    return url


def get_url_signature(url: str) -> tuple:
    """Extract (domain, path_segments[:3]) for robust matching.

    Instead of comparing full URLs (which may differ in query params,
    trailing slashes, or protocol), we compare the domain and first 3
    path segments. This catches:
    - Same article with different tracking params
    - HTTP vs HTTPS variants
    - With/without www prefix
    """
    parsed = urlparse(url.lower())
    hostname = parsed.hostname or ""
    # Remove www prefix for comparison
    if hostname.startswith("www."):
        hostname = hostname[4:]

    # Extract first 3 non-empty path segments
    path_parts = [p for p in parsed.path.split("/") if p][:3]
    return (hostname, tuple(path_parts))


def extract_inline_citations(report_text: str) -> dict:
    """Extract all [n] citations from report body (before References section)."""
    # Split at References section
    ref_split = re.split(
        r"^##\s*(?:参考文献|References)", report_text, flags=re.MULTILINE
    )
    body = ref_split[0] if ref_split else report_text

    # Find all [n] patterns
    citations = {}
    for match in re.finditer(r"\[(\d+)\]", body):
        num = int(match.group(1))
        line_start = body.rfind("\n", 0, match.start()) + 1
        line_end = body.find("\n", match.end())
        if line_end == -1:
            line_end = len(body)
        context = body[line_start:line_end].strip()
        if num not in citations:
            citations[num] = {"count": 0, "contexts": []}
        citations[num]["count"] += 1
        if len(citations[num]["contexts"]) < 3:  # Keep up to 3 examples
            citations[num]["contexts"].append(context[:120])

    return citations


def extract_references(report_text: str) -> dict:
    """Extract reference entries from the References section."""
    ref_match = re.search(
        r"^##\s*(?:参考文献|References)\s*\n(.*)",
        report_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not ref_match:
        return {}

    ref_section = ref_match.group(1)
    references = {}

    for match in re.finditer(
        r"\[(\d+)\]\s*(.*?)(?=\n\[|\n##|\Z)", ref_section, flags=re.DOTALL
    ):
        num = int(match.group(1))
        entry = match.group(2).strip()

        # Extract URL from entry
        url_match = re.search(r"https?://[^\s\)>\"]+", entry)
        url = url_match.group(0).rstrip(".,;") if url_match else None

        references[num] = {"entry": entry, "url": url}

    return references


def load_source_pool(sources: list) -> dict:
    """Build URL lookup structures from source pool.

    Returns dict with:
    - normalized: set of normalized URLs for exact matching
    - signatures: set of (domain, path_segments) tuples for fuzzy matching
    - url_map: signature → original URL for reference
    """
    normalized = set()
    signatures = set()
    url_map = {}

    for s in sources:
        url = s.get("url", "")
        if url:
            norm = normalize_url(url)
            normalized.add(norm)
            sig = get_url_signature(url)
            signatures.add(sig)
            url_map[sig] = url

    return {
        "normalized": normalized,
        "signatures": signatures,
        "url_map": url_map,
    }


def match_url(ref_url: str, pool: dict) -> str:
    """Check if URL matches the source pool.

    Returns:
    - "exact" if normalized URL matches
    - "signature" if domain + path segments match (likely same article)
    - "domain_only" if only domain matches (suspicious)
    - "none" if no match (likely invented)
    """
    norm = normalize_url(ref_url)
    if norm in pool["normalized"]:
        return "exact"

    sig = get_url_signature(ref_url)

    # Check signature match (domain + first 3 path segments)
    if sig in pool["signatures"]:
        return "signature"

    # Check domain-only match (weaker — flag as warning)
    ref_domain = sig[0]
    pool_domains = {s[0] for s in pool["signatures"]}
    if ref_domain in pool_domains:
        return "domain_only"

    return "none"


def verify(report_path: str, sources_path: str) -> dict:
    """Run all citation verification checks."""
    report_text = Path(report_path).read_text(encoding="utf-8")
    sources = json.loads(Path(sources_path).read_text(encoding="utf-8"))

    inline = extract_inline_citations(report_text)
    refs = extract_references(report_text)
    pool = load_source_pool(sources)

    issues = []
    warnings = []

    # Check 1: Every inline [n] has a reference entry
    for num in sorted(inline.keys()):
        if num not in refs:
            issues.append({
                "type": "MISSING_REFERENCE",
                "severity": "critical",
                "citation": num,
                "message": f"[{num}] cited in text but no reference entry found",
                "fix": f"Add reference entry for [{num}] or remove citation",
            })

    # Check 2: Every reference URL exists in source pool (improved matching)
    for num, ref in sorted(refs.items()):
        if ref["url"]:
            match_type = match_url(ref["url"], pool)

            if match_type == "exact" or match_type == "signature":
                pass  # Good — URL verified
            elif match_type == "domain_only":
                warnings.append({
                    "type": "DOMAIN_ONLY_MATCH",
                    "severity": "warning",
                    "citation": num,
                    "url": ref["url"],
                    "message": f"[{num}] URL domain matches source pool but specific path differs — may be a different article from the same site",
                    "fix": "Verify this is the correct article, not a different page from the same domain",
                })
            elif match_type == "none":
                issues.append({
                    "type": "INVENTED_URL",
                    "severity": "critical",
                    "citation": num,
                    "url": ref["url"],
                    "message": f"[{num}] URL not found in source pool — possible hallucination",
                    "fix": "REMOVE this citation or replace with verified URL from search results",
                })
        else:
            warnings.append({
                "type": "MISSING_URL",
                "severity": "warning",
                "citation": num,
                "message": f"[{num}] reference has no URL",
                "fix": "Add URL or note that source is offline/print",
            })

    # Check 3: Dangling references (in list but never cited)
    for num in sorted(refs.keys()):
        if num not in inline:
            warnings.append({
                "type": "DANGLING_REFERENCE",
                "severity": "warning",
                "citation": num,
                "message": f"[{num}] in reference list but never cited in text",
                "fix": "Either cite it in text or remove from references",
            })

    # Check 4: Sequential numbering
    if inline or refs:
        all_nums = sorted(set(list(inline.keys()) + list(refs.keys())))
        if all_nums:
            expected = list(range(1, max(all_nums) + 1))
            gaps = set(expected) - set(all_nums)
            if gaps:
                issues.append({
                    "type": "NUMBERING_GAP",
                    "severity": "minor",
                    "message": f"Citation numbering has gaps: {sorted(gaps)}",
                    "fix": "Renumber citations sequentially",
                })

    # Check 5: Source concentration
    if inline:
        total_citations = sum(c["count"] for c in inline.values())
        for num, data in inline.items():
            share = data["count"] / max(total_citations, 1)
            if share > 0.25:
                warnings.append({
                    "type": "SOURCE_CONCENTRATION",
                    "severity": "warning",
                    "citation": num,
                    "message": f"[{num}] accounts for {share:.0%} of all citations (>{25}% threshold)",
                    "fix": "Diversify sources — find alternative references for some claims",
                })

    # Summary
    total_citations = sum(c["count"] for c in inline.values())
    unique_sources = len(refs)
    critical_count = len([i for i in issues if i["severity"] == "critical"])

    return {
        "summary": {
            "total_inline_citations": total_citations,
            "unique_citation_numbers": len(inline),
            "reference_entries": unique_sources,
            "critical_issues": critical_count,
            "warnings": len(warnings),
            "verdict": "PASS" if critical_count == 0 else "FAIL",
        },
        "issues": issues,
        "warnings": warnings,
        "citation_coverage": {
            "inline_numbers": sorted(inline.keys()),
            "reference_numbers": sorted(refs.keys()),
        },
    }


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    report_path = sys.argv[1]
    sources_path = sys.argv[2]
    output_path = None

    if len(sys.argv) > 4 and sys.argv[3] == "--output":
        output_path = sys.argv[4]

    results = verify(report_path, sources_path)

    output = json.dumps(results, indent=2, ensure_ascii=False)
    if output_path:
        Path(output_path).write_text(output, encoding="utf-8")
        print(f"Results written to {output_path}")
    else:
        print(output)

    # Exit with error code if critical issues found
    if results["summary"]["verdict"] == "FAIL":
        sys.exit(1)


if __name__ == "__main__":
    main()
