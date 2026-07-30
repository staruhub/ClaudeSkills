#!/usr/bin/env python3
"""Validate a provider-neutral image manifest and optional article mapping."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ENVELOPE_KEYS = {
    "schema_version",
    "manifest_id",
    "article_id",
    "article_sha256",
    "mode",
    "provider_neutral",
    "images",
}
IMAGE_REQUIRED = {
    "id",
    "purpose",
    "placement_anchor",
    "placeholder",
    "aspect_ratio",
    "width",
    "height",
    "positive_prompt",
    "negative_prompt",
    "alt",
    "caption",
    "provider_status",
}
IMAGE_ALLOWED = IMAGE_REQUIRED | {"asset_ref"}
PURPOSES = {"cover", "section", "explainer", "quote", "data", "case", "cta"}
STATUSES = {
    "not-requested",
    "prompt-only",
    "generating",
    "generated",
    "failed",
    "blocked",
}
ID_RE = re.compile(r"^img-[a-z0-9][a-z0-9-]{2,63}$")
ANCHOR_RE = re.compile(
    r"^<!-- image:(img-[a-z0-9][a-z0-9-]{2,63}) -->$",
    re.MULTILINE,
)
PLACEHOLDER_RE = re.compile(
    r"^\{\{IMAGE:(img-[a-z0-9][a-z0-9-]{2,63})\}\}$",
    re.MULTILINE,
)


def canonical_utf8_lf(data: bytes) -> bytes:
    """Return UTF-8 text with CRLF/CR normalized to LF and no other changes."""
    text = data.decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def canonical_text_sha256(data: bytes) -> str:
    return hashlib.sha256(canonical_utf8_lf(data)).hexdigest()


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: cannot parse JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("manifest top level must be an object envelope")
    return value


def validate_manifest(
    manifest: dict[str, Any],
    article_bytes: bytes | None = None,
) -> list[str]:
    errors: list[str] = []
    missing = ENVELOPE_KEYS - manifest.keys()
    extra = manifest.keys() - ENVELOPE_KEYS
    if missing:
        errors.append(f"manifest missing keys: {sorted(missing)}")
    if extra:
        errors.append(f"manifest has unknown keys: {sorted(extra)}")
    if manifest.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if manifest.get("mode") not in {"image-prompts", "full-pipeline"}:
        errors.append("mode must be image-prompts or full-pipeline")
    if manifest.get("provider_neutral") is not True:
        errors.append("provider_neutral must be true")
    if not re.fullmatch(r"manifest-[a-z0-9][a-z0-9-]{2,63}", str(manifest.get("manifest_id", ""))):
        errors.append("manifest_id is invalid")
    if not re.fullmatch(r"article-[a-z0-9][a-z0-9-]{2,63}", str(manifest.get("article_id", ""))):
        errors.append("article_id is invalid")
    if not re.fullmatch(r"[a-f0-9]{64}", str(manifest.get("article_sha256", ""))):
        errors.append("article_sha256 is invalid")

    images = manifest.get("images")
    if not isinstance(images, list) or not images:
        errors.append("images must be a non-empty array")
        images = []
    seen: set[str] = set()
    for index, item in enumerate(images):
        prefix = f"images[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing_item = IMAGE_REQUIRED - item.keys()
        extra_item = item.keys() - IMAGE_ALLOWED
        if missing_item:
            errors.append(f"{prefix} missing keys: {sorted(missing_item)}")
        if extra_item:
            errors.append(f"{prefix} has unknown keys: {sorted(extra_item)}")
        image_id = str(item.get("id", ""))
        if not ID_RE.fullmatch(image_id):
            errors.append(f"{prefix}.id is invalid")
        if image_id in seen:
            errors.append(f"{prefix}.id is duplicated")
        seen.add(image_id)
        if item.get("purpose") not in PURPOSES:
            errors.append(f"{prefix}.purpose is invalid")
        expected_anchor = f"<!-- image:{image_id} -->"
        expected_placeholder = f"{{{{IMAGE:{image_id}}}}}"
        if item.get("placement_anchor") != expected_anchor:
            errors.append(f"{prefix}.placement_anchor does not derive from id")
        if item.get("placeholder") != expected_placeholder:
            errors.append(f"{prefix}.placeholder does not derive from id")
        ratio = re.fullmatch(r"([1-9][0-9]*):([1-9][0-9]*)", str(item.get("aspect_ratio", "")))
        width = item.get("width")
        height = item.get("height")
        if not isinstance(width, int) or isinstance(width, bool) or not 320 <= width <= 4096:
            errors.append(f"{prefix}.width must be an integer from 320 to 4096")
        if not isinstance(height, int) or isinstance(height, bool) or not 320 <= height <= 4096:
            errors.append(f"{prefix}.height must be an integer from 320 to 4096")
        if ratio and isinstance(width, int) and isinstance(height, int):
            left, right = int(ratio.group(1)), int(ratio.group(2))
            if width * right != height * left:
                errors.append(f"{prefix} dimensions do not match aspect_ratio")
        elif not ratio:
            errors.append(f"{prefix}.aspect_ratio is invalid")
        for field, minimum in (("positive_prompt", 40), ("negative_prompt", 10)):
            if not isinstance(item.get(field), str) or len(item[field].strip()) < minimum:
                errors.append(f"{prefix}.{field} is too short")
        for field, maximum in (("alt", 160), ("caption", 240)):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{prefix}.{field} must be non-empty")
            elif len(item[field]) > maximum:
                errors.append(f"{prefix}.{field} exceeds {maximum} characters")
        status = item.get("provider_status")
        if status not in STATUSES:
            errors.append(f"{prefix}.provider_status is invalid")
        if status == "generated" and not item.get("asset_ref"):
            errors.append(f"{prefix}.asset_ref is required for generated status")

    if article_bytes is not None:
        canonical_article = canonical_utf8_lf(article_bytes)
        article_sha = hashlib.sha256(canonical_article).hexdigest()
        if manifest.get("article_sha256") != article_sha:
            errors.append("article_sha256 does not match canonical UTF-8/LF article bytes")
        article = canonical_article.decode("utf-8")
        anchors = ANCHOR_RE.findall(article)
        placeholders = PLACEHOLDER_RE.findall(article)
        if len(anchors) != len(set(anchors)):
            errors.append("article contains duplicate image anchors")
        if len(placeholders) != len(set(placeholders)):
            errors.append("article contains duplicate image placeholders")
        if set(anchors) != seen:
            errors.append(
                f"article anchors {sorted(set(anchors))} do not match manifest ids {sorted(seen)}"
            )
        if set(placeholders) != seen:
            errors.append(
                f"article placeholders {sorted(set(placeholders))} do not match manifest ids {sorted(seen)}"
            )
        for image_id in seen:
            pair = (
                f"<!-- image:{image_id} -->\n"
                f"{{{{IMAGE:{image_id}}}}}"
            )
            if pair not in article:
                errors.append(f"article mapping for {image_id} is not an adjacent deterministic pair")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--article", type=Path)
    args = parser.parse_args()
    try:
        manifest = load_manifest(args.manifest)
        article_bytes = args.article.read_bytes() if args.article else None
        errors = validate_manifest(manifest, article_bytes)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"FAIL {len(errors)} error(s)")
        return 1
    print(f"PASS image manifest ({len(manifest['images'])} images)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
