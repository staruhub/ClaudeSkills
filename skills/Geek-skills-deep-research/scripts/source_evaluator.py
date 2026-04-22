#!/usr/bin/env python3
"""
Source Evaluator V2 — Score and rank research sources.

Usage:
    python source_evaluator.py sources.json [options]

Options:
    --topic-velocity SPEED  Topic change speed: fast|medium|slow (default: medium)
    --min-score SCORE       Minimum composite score to keep (default: 5.0)
    --mode MODE             Research mode: standard|lightweight (default: standard)
    --output PATH           Output file path (default: stdout)

Input JSON format:
[
  {
    "url": "https://example.com/article",
    "title": "Article Title",
    "date": "2024-06-15",
    "sub_question": 1,
    "notes": "Key findings from this source",
    "relevance_score": 7.0,
    "depth_score": 6.0
  }
]
"""

import json
import sys
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse
from pathlib import Path


# === Domain Authority Tiers ===

TIER_1 = {  # Score 9-10: Peer-reviewed, official bodies
    "nature.com", "science.org", "thelancet.com", "nejm.org",
    "cell.com", "pnas.org", "ieee.org", "acm.org",
    "who.int", "nih.gov", "cdc.gov", "europa.eu",
    "arxiv.org", "scholar.google.com", "semanticscholar.org",
    # Chinese academic
    "cnki.net", "wanfangdata.com.cn", "cqvip.com",
    "cas.cn", "nsfc.gov.cn", "xueshu.baidu.com",
}

TIER_2 = {  # Score 7-8: Reputable news, established tech
    "reuters.com", "apnews.com", "bbc.com", "nytimes.com",
    "theguardian.com", "washingtonpost.com", "economist.com",
    "techcrunch.com", "arstechnica.com", "wired.com",
    "github.com", "stackoverflow.com", "hbr.org",
    "mckinsey.com", "bcg.com", "gartner.com",
    # Chinese reputable
    "xinhuanet.com", "people.com.cn", "thepaper.cn",
    "36kr.com", "infoq.cn", "juejin.cn", "jiqizhixin.com",
    "leiphone.com", "geekpark.net",
}

TIER_3 = {  # Score 5-6: Industry blogs, conferences
    "medium.com", "substack.com", "dev.to",
    "engineering.fb.com", "blog.google", "aws.amazon.com",
    "openai.com", "anthropic.com", "deepmind.google",
    "huggingface.co", "pytorch.org", "tensorflow.org",
    # Chinese industry
    "zhihu.com", "csdn.net", "segmentfault.com",
    "oschina.net", "toutiao.com", "sspai.com",
    "volcengine.com", "cloud.tencent.com",
}

# .gov and .edu domains get automatic tier boost
GOV_EDU_SUFFIXES = {".gov", ".edu", ".gov.cn", ".edu.cn", ".ac.uk", ".ac.jp", ".ac.cn"}


def get_domain(url: str) -> str:
    """Extract registrable domain from URL."""
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    parts = hostname.split(".")

    # Handle multi-part TLDs like .com.cn, .co.uk
    multi_tlds = {".com.cn", ".gov.cn", ".edu.cn", ".ac.cn", ".org.cn",
                  ".co.uk", ".ac.uk", ".org.uk", ".co.jp", ".ac.jp"}
    for tld in multi_tlds:
        if hostname.endswith(tld):
            tld_parts = tld.count(".")
            if len(parts) > tld_parts:
                return ".".join(parts[-(tld_parts + 1):])
            return hostname

    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return hostname


def is_subdomain_blog(url: str) -> bool:
    """Detect if URL is a user blog on a platform (lower authority)."""
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    blog_platforms = ["medium.com", "substack.com", "zhihu.com", "csdn.net", "dev.to"]
    domain = get_domain(url)
    if domain in blog_platforms and hostname != domain and hostname != f"www.{domain}":
        return True
    # Check for user-content paths on non-subdomain platforms
    path = parsed.path.lower()
    if domain == "zhihu.com" and "/p/" in path:
        return True  # Individual zhihu answers
    return False


def score_authority(url: str) -> float:
    """Score source authority (0-10)."""
    domain = get_domain(url)
    parsed = urlparse(url)
    hostname = parsed.hostname or ""

    # Check gov/edu suffix boost
    for suffix in GOV_EDU_SUFFIXES:
        if hostname.endswith(suffix):
            return 8.5

    # Check tiers
    if domain in TIER_1:
        return 9.5
    if domain in TIER_2:
        score = 7.5
        if is_subdomain_blog(url):
            score -= 1.5  # User blog on platform = lower authority
        return score
    if domain in TIER_3:
        score = 5.5
        if is_subdomain_blog(url):
            score -= 1.0
        return score

    # Unknown domain baseline
    return 3.0


def score_recency(date_str: str, topic_velocity: str = "medium") -> float:
    """Score source recency (0-10) based on topic velocity."""
    if not date_str:
        return 3.0  # Unknown date = low score

    try:
        pub_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        try:
            pub_date = datetime.strptime(date_str, "%Y-%m")
        except ValueError:
            try:
                pub_date = datetime.strptime(date_str, "%Y")
            except ValueError:
                return 3.0

    age_days = (datetime.now() - pub_date).days

    thresholds = {
        "fast": [(180, 10), (365, 7), (730, 4), (float("inf"), 2)],
        "medium": [(365, 10), (1095, 7), (1825, 4), (float("inf"), 2)],
        "slow": [(1825, 10), (3650, 7), (7300, 4), (float("inf"), 2)],
    }

    for max_days, score in thresholds.get(topic_velocity, thresholds["medium"]):
        if age_days <= max_days:
            return score
    return 2.0


def score_source(source: dict, topic_velocity: str = "medium") -> dict:
    """Score a single source and return enriched dict."""
    url = source.get("url", "")
    date = source.get("date", "")

    authority = score_authority(url)
    recency = score_recency(date, topic_velocity)
    # Relevance and depth must be scored by the LLM — use provided or defaults
    relevance = source.get("relevance_score", 5.0)
    depth = source.get("depth_score", 5.0)

    # Adjust recency weight for slow topics
    if topic_velocity == "slow":
        composite = (authority * 0.35) + (recency * 0.05) + (relevance * 0.35) + (depth * 0.25)
    else:
        composite = (authority * 0.3) + (recency * 0.2) + (relevance * 0.3) + (depth * 0.2)

    return {
        **source,
        "scores": {
            "authority": round(authority, 1),
            "recency": round(recency, 1),
            "relevance": round(relevance, 1),
            "depth": round(depth, 1),
            "composite": round(composite, 1),
        },
        "domain": get_domain(url),
        "is_blog": is_subdomain_blog(url),
    }


def check_diversity(scored_sources: list) -> dict:
    """Check source diversity requirements."""
    domains = set(s["domain"] for s in scored_sources)
    domain_counts = {}
    for s in scored_sources:
        d = s["domain"]
        domain_counts[d] = domain_counts.get(d, 0) + 1

    total = len(scored_sources) or 1
    max_share = max(domain_counts.values(), default=0) / total
    dominant = max(domain_counts, key=domain_counts.get, default="none")

    # Classify source types
    source_types = set()
    for s in scored_sources:
        domain = s["domain"]
        if domain in TIER_1:
            source_types.add("academic")
        elif domain in TIER_2:
            source_types.add("news/industry")
        elif domain in TIER_3:
            source_types.add("blog/community")
        else:
            source_types.add("other")

    return {
        "unique_domains": len(domains),
        "max_single_domain_share": round(max_share, 2),
        "dominant_domain": dominant,
        "source_types": list(source_types),
        "type_diversity": len(source_types) >= 3,
        "passes_diversity": len(domains) >= 5 and max_share <= 0.25,
    }


def check_sub_question_coverage(scored_sources: list) -> dict:
    """Check if every sub-question has adequate source coverage."""
    sq_counts = {}
    for s in scored_sources:
        sq = s.get("sub_question")
        if sq is not None:
            sq_counts[sq] = sq_counts.get(sq, 0) + 1

    weak = {sq: count for sq, count in sq_counts.items() if count < 2}
    return {
        "coverage": sq_counts,
        "weak_sub_questions": weak,
        "all_covered": len(weak) == 0,
    }


def evaluate(
    sources: list,
    topic_velocity: str = "medium",
    min_score: float = 5.0,
    mode: str = "standard",
) -> dict:
    """Evaluate all sources and return ranked results."""
    # Adjust min_score for lightweight mode
    if mode == "lightweight" and min_score == 5.0:
        min_score = 4.5

    scored = [score_source(s, topic_velocity) for s in sources]
    scored.sort(key=lambda x: x["scores"]["composite"], reverse=True)

    kept = [s for s in scored if s["scores"]["composite"] >= min_score]
    dropped = [s for s in scored if s["scores"]["composite"] < min_score]

    diversity = check_diversity(kept)
    coverage = check_sub_question_coverage(kept)

    # Mode-specific thresholds
    min_sources = 15 if mode == "standard" else 8
    min_domains = 5 if mode == "standard" else 3

    return {
        "kept": kept,
        "dropped": dropped,
        "diversity": diversity,
        "coverage": coverage,
        "summary": {
            "total_evaluated": len(sources),
            "kept": len(kept),
            "dropped": len(dropped),
            "avg_composite": round(
                sum(s["scores"]["composite"] for s in kept) / max(len(kept), 1), 1
            ),
            "meets_source_threshold": len(kept) >= min_sources,
            "meets_diversity_threshold": diversity["unique_domains"] >= min_domains,
            "mode": mode,
            "topic_velocity": topic_velocity,
        },
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    min_score = 5.0
    output_path = None
    topic_velocity = "medium"
    mode = "standard"

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--min-score" and i + 1 < len(sys.argv):
            min_score = float(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_path = Path(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--topic-velocity" and i + 1 < len(sys.argv):
            topic_velocity = sys.argv[i + 1]
            if topic_velocity not in ("fast", "medium", "slow"):
                print(f"Error: --topic-velocity must be fast|medium|slow, got '{topic_velocity}'")
                sys.exit(1)
            i += 2
        elif sys.argv[i] == "--mode" and i + 1 < len(sys.argv):
            mode = sys.argv[i + 1]
            if mode not in ("standard", "lightweight"):
                print(f"Error: --mode must be standard|lightweight, got '{mode}'")
                sys.exit(1)
            i += 2
        else:
            i += 1

    with open(input_path) as f:
        sources = json.load(f)

    results = evaluate(sources, topic_velocity=topic_velocity, min_score=min_score, mode=mode)

    output = json.dumps(results, indent=2, ensure_ascii=False)
    if output_path:
        with open(output_path, "w") as f:
            f.write(output)
        print(f"Results written to {output_path}")
    else:
        print(output)


if __name__ == "__main__":
    main()
