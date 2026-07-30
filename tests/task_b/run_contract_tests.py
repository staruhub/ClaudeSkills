#!/usr/bin/env python3
"""Executable Task B contract tests.

This runner parses real fixtures, executes skill validators/renderers, asserts
positive and negative behavior, and writes a machine-readable summary. Expected
negative tests pass only when the invoked validator returns a non-zero code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
PM = REPO / "skills" / "Geek-skills-product-manager"
WECHAT = REPO / "skills" / "Geek-skills-wechat-article-writer"
DEEP = REPO / "skills" / "Geek-skills-deep-research"
DECK = REPO / "skills" / "Geek-skills-deck-studio"


class ResultLog:
    def __init__(self) -> None:
        self.cases: list[dict[str, Any]] = []

    def case(
        self,
        case_id: str,
        skill: str,
        scenario: str,
        fn,
    ) -> None:
        started = datetime.now(timezone.utc)
        try:
            details = fn() or {}
            status = "blocked" if details.get("execution_status") == "blocked" else "pass"
            error = None
        except Exception as exc:  # intentional test harness boundary
            details = {}
            status = "fail"
            error = f"{type(exc).__name__}: {exc}"
        finished = datetime.now(timezone.utc)
        self.cases.append(
            {
                "id": case_id,
                "skill": skill,
                "scenario": scenario,
                "status": status,
                "error": error,
                "started_at": started.isoformat(),
                "finished_at": finished.isoformat(),
                "details": details,
            }
        )


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return {
        "command": command,
        "cwd": str(cwd),
        "exit_code": completed.returncode,
        "output": completed.stdout,
    }


def canonical_to_crlf(data: bytes) -> bytes:
    text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return text.replace("\n", "\r\n").encode("utf-8")


def require_exit(result: dict[str, Any], expected: int | str) -> None:
    if expected == "nonzero":
        assert result["exit_code"] != 0, result["output"]
    else:
        assert result["exit_code"] == expected, result["output"]


def static_skill_check() -> dict[str, Any]:
    checked = []
    for skill_dir in (DECK, DEEP, PM, WECHAT):
        path = skill_dir / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
        assert match, f"{path}: invalid frontmatter"
        frontmatter = match.group(1)
        assert re.search(r"^name:\s*\S+", frontmatter, flags=re.MULTILINE)
        assert re.search(r"^description:\s*.+", frontmatter, flags=re.MULTILINE)
        assert text.count("\n") + 1 <= 500
        for ref in re.findall(
            r"`((?:references|scripts|schemas|templates|evals|assets)/[^`\s]+)",
            text,
        ):
            assert (skill_dir / ref).exists() or (REPO / ref).exists(), (
                f"{path}: missing referenced file {ref}"
            )
        checked.append(str(path.relative_to(REPO)))
    fixture_integrity = run(
        [sys.executable, str(Path(__file__).resolve().parent / "verify_fixture_integrity.py")],
        REPO,
    )
    require_exit(fixture_integrity, 0)
    encoding_probe = run(
        [
            sys.executable,
            "-c",
            "import os; os.write(1, 'UTF-8 编码探针'.encode('utf-8'))",
        ],
        REPO,
    )
    require_exit(encoding_probe, 0)
    assert encoding_probe["output"] == "UTF-8 编码探针"
    return {
        "checked": checked,
        "fixture_integrity": fixture_integrity,
        "utf8_subprocess_probe": encoding_probe,
    }


def pm_positive() -> dict[str, Any]:
    fixture = FIXTURES / "product-manager"
    result = run(
        [
            sys.executable,
            str(PM / "scripts" / "validate_grill_session.py"),
            "--state",
            str(fixture / "grill-state.json"),
            "--transcript",
            str(fixture / "transcript.json"),
            "--product-doc",
            str(fixture / "PRODUCT-DOC.md"),
        ],
        REPO,
    )
    require_exit(result, 0)
    transcript = json.loads((fixture / "transcript.json").read_text(encoding="utf-8"))
    questions = [e for e in transcript["events"] if e["kind"] == "question"]
    assert len(questions) == 5
    assert all(len(re.findall(r"[?？]", e["question"])) == 1 for e in questions)
    assert any(e["kind"] == "resume" for e in transcript["events"])
    resume = next(e for e in transcript["events"] if e["kind"] == "resume")
    state_before = (fixture / resume["state_path"]).read_bytes()
    canonical_state = (
        state_before.decode("utf-8")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .encode("utf-8")
    )
    assert hashlib.sha256(canonical_state).hexdigest() == resume["state_sha256"]
    with tempfile.TemporaryDirectory(prefix="pm-crlf-") as raw:
        temp = Path(raw)
        shutil.copy2(fixture / "transcript.json", temp / "transcript.json")
        (temp / resume["state_path"]).write_bytes(canonical_to_crlf(state_before))
        crlf_result = run(
            [
                sys.executable,
                str(PM / "scripts" / "validate_grill_session.py"),
                "--state",
                str(fixture / "grill-state.json"),
                "--transcript",
                str(temp / "transcript.json"),
                "--product-doc",
                str(fixture / "PRODUCT-DOC.md"),
            ],
            REPO,
        )
        require_exit(crlf_result, 0)
    final = next(e for e in transcript["events"] if e["kind"] == "final")
    assert final["implementation_started"] is False
    return {
        **result,
        "question_turns": len(questions),
        "resume_verified": True,
        "crlf_resume_validation": crlf_result,
    }


def pm_invalid_multi_question() -> dict[str, Any]:
    fixture = FIXTURES / "product-manager"
    result = run(
        [
            sys.executable,
            str(PM / "scripts" / "validate_grill_session.py"),
            "--state",
            str(fixture / "grill-state.json"),
            "--transcript",
            str(fixture / "transcript-invalid-multi-question.json"),
            "--product-doc",
            str(fixture / "PRODUCT-DOC.md"),
        ],
        REPO,
    )
    require_exit(result, "nonzero")
    assert "exactly one question" in result["output"]
    return result


def pm_invalid_hard_stop() -> dict[str, Any]:
    fixture = FIXTURES / "product-manager"
    result = run(
        [
            sys.executable,
            str(PM / "scripts" / "validate_grill_session.py"),
            "--state",
            str(fixture / "state-invalid-implementation.json"),
            "--transcript",
            str(fixture / "transcript.json"),
            "--product-doc",
            str(fixture / "PRODUCT-DOC.md"),
        ],
        REPO,
    )
    require_exit(result, "nonzero")
    assert "implementation_allowed must be false" in result["output"]
    return result


def assert_safe_html(path: Path, expected_ids: set[str], raw_edge: bool = False) -> None:
    text = path.read_text(encoding="utf-8")
    assert re.search(r"<section[^>]+style=", text)
    assert "max-width:100%" in text
    assert "<style" not in text.lower()
    assert "<script" not in text.lower()
    assert not re.search(r"\son[a-z]+\s*=", text, flags=re.IGNORECASE)
    assert not re.search(r"\sclass\s*=|\sid\s*=", text, flags=re.IGNORECASE)
    assert "<img" not in text.lower(), "prompt-only output must not pretend an image exists"
    actual_ids = set(re.findall(r'data-image-id="([^"]+)"', text))
    assert actual_ids == expected_ids
    if raw_edge:
        assert "&lt;script&gt;" in text
        assert "should-not-run" in text


def wechat_positive(artifact_dir: Path) -> dict[str, Any]:
    fixture = FIXTURES / "wechat"
    manifest = fixture / "image-manifest.json"
    article = fixture / "article.md"
    validation = run(
        [
            sys.executable,
            str(WECHAT / "scripts" / "validate_image_manifest.py"),
            str(manifest),
            "--article",
            str(article),
        ],
        REPO,
    )
    require_exit(validation, 0)
    output = artifact_dir / "wechat" / "layout.html"
    rendering = run(
        [
            sys.executable,
            str(WECHAT / "scripts" / "render_wechat_layout.py"),
            "--article",
            str(article),
            "--manifest",
            str(manifest),
            "--output",
            str(output),
        ],
        REPO,
    )
    require_exit(rendering, 0)
    assert_safe_html(output, {"img-contract-cover", "img-contract-structure"})
    crlf_article = artifact_dir / "wechat" / "article-crlf.md"
    crlf_article.write_bytes(canonical_to_crlf(article.read_bytes()))
    crlf_output = artifact_dir / "wechat" / "layout-crlf.html"
    crlf_rendering = run(
        [
            sys.executable,
            str(WECHAT / "scripts" / "render_wechat_layout.py"),
            "--article",
            str(crlf_article),
            "--manifest",
            str(manifest),
            "--output",
            str(crlf_output),
        ],
        REPO,
    )
    require_exit(crlf_rendering, 0)
    assert_safe_html(crlf_output, {"img-contract-cover", "img-contract-structure"})
    return {
        "validation": validation,
        "rendering": rendering,
        "crlf_rendering": crlf_rendering,
        "output": str(output),
    }


def wechat_image_prompts() -> dict[str, Any]:
    fixture = FIXTURES / "wechat"
    manifest_path = fixture / "image-manifest-edge.json"
    article_path = fixture / "article-edge-raw-html.md"
    result = run(
        [
            sys.executable,
            str(WECHAT / "scripts" / "validate_image_manifest.py"),
            str(manifest_path),
            "--article",
            str(article_path),
        ],
        REPO,
    )
    require_exit(result, 0)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["mode"] == "image-prompts"
    assert all(item["provider_status"] == "prompt-only" for item in manifest["images"])
    assert all("asset_ref" not in item for item in manifest["images"])
    return {**result, "images": len(manifest["images"]), "image_generation_claimed": False}


def wechat_layout_only(artifact_dir: Path) -> dict[str, Any]:
    fixture = FIXTURES / "wechat"
    output = artifact_dir / "wechat" / "layout-only.html"
    result = run(
        [
            sys.executable,
            str(WECHAT / "scripts" / "render_wechat_layout.py"),
            "--article",
            str(fixture / "article.md"),
            "--manifest",
            str(fixture / "image-manifest.json"),
            "--output",
            str(output),
        ],
        REPO,
    )
    require_exit(result, 0)
    assert_safe_html(output, {"img-contract-cover", "img-contract-structure"})
    return {**result, "output": str(output)}


def wechat_edge_raw_html(artifact_dir: Path) -> dict[str, Any]:
    fixture = FIXTURES / "wechat"
    output = artifact_dir / "wechat" / "layout-edge.html"
    result = run(
        [
            sys.executable,
            str(WECHAT / "scripts" / "render_wechat_layout.py"),
            "--article",
            str(fixture / "article-edge-raw-html.md"),
            "--manifest",
            str(fixture / "image-manifest-edge.json"),
            "--output",
            str(output),
        ],
        REPO,
    )
    require_exit(result, 0)
    assert_safe_html(output, {"img-edge-safe"}, raw_edge=True)
    return {**result, "output": str(output)}


def wechat_invalid_manifest() -> dict[str, Any]:
    fixture = FIXTURES / "wechat"
    result = run(
        [
            sys.executable,
            str(WECHAT / "scripts" / "validate_image_manifest.py"),
            str(fixture / "image-manifest-invalid.json"),
            "--article",
            str(fixture / "article.md"),
        ],
        REPO,
    )
    require_exit(result, "nonzero")
    assert "height" in result["output"]
    assert "placement_anchor" in result["output"]
    return result


def wechat_article_only() -> dict[str, Any]:
    text = (FIXTURES / "wechat" / "article-only.md").read_text(encoding="utf-8")
    assert text.startswith("# ")
    assert not ANCHOR_OR_PLACEHOLDER.search(text)
    return {"bytes": len(text.encode("utf-8")), "manifest_created": False}


ANCHOR_OR_PLACEHOLDER = re.compile(r"<!-- image:|\{\{IMAGE:")


def deep_positive(artifact_dir: Path) -> dict[str, Any]:
    fixture = FIXTURES / "deep-research"
    output = artifact_dir / "deep-research" / "citation-results.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    verify = run(
        [
            sys.executable,
            str(DEEP / "scripts" / "verify_citations.py"),
            str(fixture / "report-positive.md"),
            str(fixture / "sources.json"),
            "--output",
            str(output),
        ],
        REPO,
    )
    require_exit(verify, 0)
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["summary"]["verdict"] == "PASS"
    assert result["summary"]["total_inline_citations"] == 5
    assert result["summary"]["reference_entries"] == 5
    packets = sorted((fixture / "source-packet").glob("*.txt"))
    assert len(packets) == 5
    keywords = ["citation", "limitations", "conflicting", "summary", "routing"]
    for packet, keyword in zip(packets, keywords):
        assert keyword in packet.read_text(encoding="utf-8").lower()
    scored = artifact_dir / "deep-research" / "source-scores.json"
    evaluate = run(
        [
            sys.executable,
            str(DEEP / "scripts" / "source_evaluator.py"),
            str(fixture / "sources.json"),
            "--mode",
            "lightweight",
            "--as-of",
            "2026-07-30",
            "--output",
            str(scored),
        ],
        REPO,
    )
    require_exit(evaluate, 0)
    score_data = json.loads(scored.read_text(encoding="utf-8"))
    assert score_data["summary"]["as_of"] == "2026-07-30"
    return {
        "verify": verify,
        "evaluate": evaluate,
        "citation_summary": result["summary"],
        "source_threshold_met": score_data["summary"]["meets_source_threshold"],
        "external_reachability": "not tested",
    }


def deep_invalid() -> dict[str, Any]:
    fixture = FIXTURES / "deep-research"
    result = run(
        [
            sys.executable,
            str(DEEP / "scripts" / "verify_citations.py"),
            str(fixture / "report-invalid-invented-url.md"),
            str(fixture / "sources.json"),
        ],
        REPO,
    )
    require_exit(result, "nonzero")
    assert "INVENTED_URL" in result["output"]
    assert '"verdict": "FAIL"' in result["output"]
    return result


def deep_delta_resume(artifact_dir: Path) -> dict[str, Any]:
    delta = FIXTURES / "deep-research" / "delta"
    handoff = (delta / "handoff.md").read_text(encoding="utf-8")
    required = [
        "## Research Question",
        "## Current Phase",
        "## Artifacts (read these files)",
        "## Key Decisions Made",
        "## Known Issues",
        "## Acceptance Status",
    ]
    for heading in required:
        assert heading in handoff
    artifact_paths = re.findall(r"^- (.+\.md|.+\.json)$", handoff, flags=re.MULTILINE)
    assert artifact_paths
    for relative in artifact_paths:
        assert (delta / relative).resolve().exists(), relative
    output = artifact_dir / "deep-research" / "delta-run-summary.json"
    result = run(
        [
            sys.executable,
            str(DEEP / "scripts" / "emit_run_summary.py"),
            "--draft",
            str(delta / "delta-draft.md"),
            "--registry",
            str(delta / "registry.md"),
            "--output-type",
            "delta",
            "--stakes",
            "low",
            "--orchestration",
            "delta",
            "--skill-version",
            "8.1.2",
            "--output",
            str(output),
        ],
        REPO,
    )
    require_exit(result, 0)
    summary = json.loads(output.read_text(encoding="utf-8"))
    assert summary["output_type"] == "delta"
    assert summary["orchestration_mode"] == "delta"
    assert summary["skill_version"] == "8.1.2"
    return {**result, "handoff_artifacts": artifact_paths, "output": str(output)}


def deck_generate_all() -> dict[str, Any]:
    outputs = []
    background_bleed_marker_verified = False
    with tempfile.TemporaryDirectory(prefix="deck-generate-") as raw:
        temp = Path(raw)
        for source in sorted((DECK / "examples").glob("*/generate.js")):
            target = temp / source.parent.name
            shutil.copytree(source.parent, target)
            result = run(["node", str(target / "generate.js")], temp)
            require_exit(result, 0)
            pages = sorted((target / "html").glob("p*.html"))
            assert len(pages) == 9
            assert not (temp / "html").exists(), "script wrote into caller cwd"
            for page in pages:
                text = page.read_text(encoding="utf-8")
                assert "width:1280px" in text and "height:720px" in text
                assert not re.search(r"https?://|<script", text, flags=re.IGNORECASE)
            if source.parent.name == "polar-night-ai-native":
                cover = pages[0].read_text(encoding="utf-8")
                assert 'data-deck-background-bleed="true"' in cover
                assert 'aria-hidden="true"' in cover
                assert "pointer-events:none" in cover
                background_bleed_marker_verified = True
            outputs.append({"example": source.parent.name, **result, "pages": len(pages)})
    return {
        "examples": outputs,
        "background_bleed_marker_verified": background_bleed_marker_verified,
    }


def deck_missing_png_fails() -> dict[str, Any]:
    source = DECK / "examples" / "polar-night-ai-native"
    with tempfile.TemporaryDirectory(prefix="deck-invalid-") as raw:
        target = Path(raw) / "polar-night-ai-native"
        shutil.copytree(source, target)
        env = os.environ.copy()
        node_modules = env.get("CODEX_PRIMARY_RUNTIME_NODE_MODULES")
        if node_modules:
            env["NODE_PATH"] = node_modules
        result = run(["node", str(target / "assemble.js")], target, env=env)
        require_exit(result, "nonzero")
        assert "missing rendered page" in result["output"]
        return result


def deck_full_composition(artifact_dir: Path) -> dict[str, Any]:
    source = DECK / "examples" / "polar-night-ai-native"
    target = artifact_dir / "deck" / "polar-night-ai-native"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    env = os.environ.copy()
    node_modules = env.get("CODEX_PRIMARY_RUNTIME_NODE_MODULES")
    if node_modules:
        env["NODE_PATH"] = node_modules
    generate = run(["node", str(target / "generate.js")], target, env=env)
    require_exit(generate, 0)
    render = run(
        [
            "node",
            str(Path(__file__).resolve().parent / "render_deck_html.cjs"),
            "--input-dir",
            str(target / "html"),
            "--output-dir",
            str(target / "png"),
            "--overflow-fixture-dir",
            str(FIXTURES / "deck"),
        ],
        REPO,
        env=env,
    )
    if render["exit_code"] != 0 and "Executable doesn't exist" in render["output"]:
        return {
            "generate": generate,
            "render": render,
            "execution_status": "blocked",
            "blocker": "Playwright library is present but its Chromium executable is absent.",
            "reproduction_command": render["command"],
            "html_dir": str(target / "html"),
            "editable": False,
        }
    require_exit(render, 0)
    assert "marked background bleed accepted; foreground overflow rejected" in render["output"]
    assemble = run(["node", str(target / "assemble.js")], target, env=env)
    require_exit(assemble, 0)
    pptx = target / "ai-native-methodology.pptx"
    assert pptx.exists() and pptx.stat().st_size > 10_000
    assert len(list((target / "png").glob("p*.png"))) == 9
    return {
        "generate": generate,
        "render": render,
        "assemble": assemble,
        "overflow_contract_verified": True,
        "pptx": str(pptx),
        "editable": False,
        "editability_reason": "each slide is a full-slide raster image",
    }


def secret_scan() -> dict[str, Any]:
    patterns = {
        "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "openai_key": re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
        "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    }
    hits = []
    scanned = 0
    scan_roots = (DECK, DEEP, PM, WECHAT, Path(__file__).resolve().parent)
    seen: set[Path] = set()
    for root in scan_roots:
        for path in root.rglob("*"):
            path = path.resolve()
            if path in seen or not path.is_file():
                continue
            seen.add(path)
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".pptx", ".zip", ".pyc"}:
                continue
            if path.stat().st_size > 2_000_000:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            scanned += 1
            for name, pattern in patterns.items():
                if pattern.search(text):
                    hits.append({"type": name, "path": str(path.relative_to(REPO))})
    assert not hits, hits
    return {"files_scanned": scanned, "hits": hits}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--artifact-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.artifact_dir = args.artifact_dir.resolve()
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    log = ResultLog()
    log.case("static-01", "all", "frontmatter/reference/static parse", static_skill_check)
    log.case("pm-positive", "product-manager", "positive multi-turn + approval + hard stop", pm_positive)
    log.case("pm-invalid-question", "product-manager", "invalid two-question turn", pm_invalid_multi_question)
    log.case("pm-invalid-stop", "product-manager", "invalid implementation authorization", pm_invalid_hard_stop)
    log.case("wechat-article", "wechat-article-writer", "article-only mode", wechat_article_only)
    log.case("wechat-image-prompts", "wechat-article-writer", "image-prompts mode stops before generation", wechat_image_prompts)
    log.case("wechat-layout", "wechat-article-writer", "layout-only mode", lambda: wechat_layout_only(args.artifact_dir))
    log.case("wechat-full", "wechat-article-writer", "full pipeline + mapping", lambda: wechat_positive(args.artifact_dir))
    log.case("wechat-edge-html", "wechat-article-writer", "raw HTML escaped", lambda: wechat_edge_raw_html(args.artifact_dir))
    log.case("wechat-invalid", "wechat-article-writer", "invalid manifest rejected", wechat_invalid_manifest)
    log.case("deep-positive", "deep-research", "citation bundle + deterministic as-of", lambda: deep_positive(args.artifact_dir))
    log.case("deep-delta", "deep-research", "resume/delta handoff", lambda: deep_delta_resume(args.artifact_dir))
    log.case("deep-invalid", "deep-research", "invented URL rejected", deep_invalid)
    log.case("deck-positive", "deck-studio", "all HTML examples generate in own directory", deck_generate_all)
    log.case("deck-edge", "deck-studio", "missing raster pages rejected", deck_missing_png_fails)
    log.case("deck-composition", "deck-studio", "HTML to PNG to PPTX composition", lambda: deck_full_composition(args.artifact_dir))
    log.case("secret-scan", "all", "credential pattern scan", secret_scan)
    failed = [case for case in log.cases if case["status"] == "fail"]
    blocked = [case for case in log.cases if case["status"] == "blocked"]
    summary = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "repo": str(REPO),
        "total": len(log.cases),
        "passed": len(log.cases) - len(failed) - len(blocked),
        "blocked": len(blocked),
        "failed": len(failed),
        "verdict": (
            "FAIL"
            if failed
            else "PASS_WITH_LIMITATIONS"
            if blocked
            else "PASS"
        ),
        "cases": log.cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"{summary['verdict']} "
        f"{summary['passed']} passed, {summary['blocked']} blocked, "
        f"{summary['failed']} failed"
    )
    for case in log.cases:
        print(f"{case['status'].upper():4} {case['id']}: {case['scenario']}")
        if case["error"]:
            print(f"     {case['error']}")
    print(f"summary: {args.output}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
