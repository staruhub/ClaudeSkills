#!/usr/bin/env python3
"""Fail-closed integrity checks for Task B positive and negative fixtures."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

REPO = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def to_crlf(data: bytes) -> bytes:
    text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return text.replace("\n", "\r\n").encode("utf-8")


def main() -> int:
    pm = load_module(
        "task_b_pm_validator",
        REPO
        / "skills"
        / "Geek-skills-product-manager"
        / "scripts"
        / "validate_grill_session.py",
    )
    wechat = load_module(
        "task_b_wechat_validator",
        REPO
        / "skills"
        / "Geek-skills-wechat-article-writer"
        / "scripts"
        / "validate_image_manifest.py",
    )
    errors: list[str] = []
    checked: dict[str, object] = {}

    pm_fixture = FIXTURES / "product-manager"
    transcript = json.loads((pm_fixture / "transcript.json").read_text(encoding="utf-8"))
    resume_events = [event for event in transcript["events"] if event.get("kind") == "resume"]
    if len(resume_events) != 1:
        errors.append(f"expected one PM resume event, found {len(resume_events)}")
    else:
        resume = resume_events[0]
        state_bytes = (pm_fixture / resume["state_path"]).read_bytes()
        digest = pm.canonical_text_sha256(state_bytes)
        crlf_digest = pm.canonical_text_sha256(to_crlf(state_bytes))
        if digest != resume["state_sha256"]:
            errors.append("PM resume event hash drifted from canonical state fixture")
        if crlf_digest != digest:
            errors.append("PM canonical state hash differs for LF and CRLF")
        checked["pm_resume_sha256"] = digest

    wechat_fixture = FIXTURES / "wechat"
    pairs = (
        ("image-manifest.json", "article.md"),
        ("image-manifest-edge.json", "article-edge-raw-html.md"),
    )
    checked_manifests: dict[str, str] = {}
    for manifest_name, article_name in pairs:
        manifest = wechat.load_manifest(wechat_fixture / manifest_name)
        article_bytes = (wechat_fixture / article_name).read_bytes()
        for label, candidate in (("native", article_bytes), ("crlf", to_crlf(article_bytes))):
            manifest_errors = wechat.validate_manifest(manifest, candidate)
            if manifest_errors:
                errors.append(
                    f"{manifest_name}/{label} validation failed: {'; '.join(manifest_errors)}"
                )
        digest = wechat.canonical_text_sha256(article_bytes)
        if manifest["article_sha256"] != digest:
            errors.append(f"{manifest_name} hash drifted from canonical article fixture")
        checked_manifests[manifest_name] = digest

    negative = wechat.load_manifest(wechat_fixture / "image-manifest-invalid.json")
    negative_errors = wechat.validate_manifest(
        negative,
        (wechat_fixture / "article.md").read_bytes(),
    )
    if not negative_errors:
        errors.append("negative WeChat manifest unexpectedly passed")
    checked["wechat_manifest_sha256"] = checked_manifests
    checked["negative_error_count"] = len(negative_errors)

    result = {"status": "FAIL" if errors else "PASS", "checked": checked, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
