#!/usr/bin/env python3
"""Dependency-free checks for the GitHub Pages site and its publication contract."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


EXPECTED_SITE_URL = "https://staruhub.github.io/ClaudeSkills/"
RELEASE_VERSION = "1.0.0"
RELEASE_URL = f"https://github.com/staruhub/ClaudeSkills/releases/tag/{RELEASE_VERSION}"
SITE_PAGES = ("index.html", "zh-CN.html")
AGENT_SKILLS_MARKERS = (
    "Agent Skills",
    ".agents/skills",
    "--client claude-code",
)
LEGACY_EXCLUSIVE_POSITIONING = {
    "index.html": (
        "workflows for Claude Code",
        "permissions Claude may request",
    ),
    "zh-CN.html": (
        "给 Claude Code 一套能交付的工作流",
        "Claude 可能向你申请什么权限",
    ),
    "README.md": ("Give Claude Code workflows that finish the job.",),
    "README.zh-CN.md": ("给 Claude Code 装上真正能把活做完的工作流。",),
}
REQUIRED_REPOSITORY_LINKS = (
    "https://github.com/staruhub/ClaudeSkills",
    RELEASE_URL,
    "https://github.com/staruhub/ClaudeSkills/blob/main/SECURITY.md",
    "https://github.com/staruhub/ClaudeSkills/blob/main/CONTRIBUTING.md",
    "https://github.com/staruhub/ClaudeSkills/blob/main/LICENSE",
    "https://github.com/staruhub/ClaudeSkills/issues",
)
REQUIRED_WORKFLOW_MARKERS = (
    "actions/checkout@v6",
    "actions/setup-python@v6",
    "actions/configure-pages@v5",
    "actions/upload-pages-artifact@v4",
    "actions/deploy-pages@v4",
    "path: ./site",
    "contents: read",
    "pages: write",
    "id-token: write",
    "name: github-pages",
    "needs: build",
    "workflow_dispatch:",
    '"VERSION"',
)


class SiteHTMLParser(HTMLParser):
    """Collect the small subset of document structure needed by the checks."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[str] = []
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.resources: list[tuple[str, str]] = []
        self.heading_levels: list[int] = []
        self.html_lang = ""
        self.nav_labels: list[str] = []
        self.skip_targets: list[str] = []
        self.button_attrs: list[dict[str, str]] = []
        self.detail_count = 0
        self.summary_count = 0
        self.th_scopes: list[str] = []
        self.meta_names: dict[str, str] = {}
        self.title_count = 0

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = {key: value or "" for key, value in attrs}
        self.tags.append(tag)

        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "html":
            self.html_lang = attributes.get("lang", "")
        if tag == "a":
            href = attributes.get("href", "")
            self.links.append(href)
            classes = attributes.get("class", "").split()
            if "skip-link" in classes:
                self.skip_targets.append(href)
        if tag == "link" and attributes.get("href"):
            self.resources.append(("href", attributes["href"]))
        if tag in {"script", "img", "source"} and attributes.get("src"):
            self.resources.append(("src", attributes["src"]))
        if tag == "nav":
            self.nav_labels.append(attributes.get("aria-label", ""))
        if tag == "button":
            self.button_attrs.append(attributes)
        if tag == "details":
            self.detail_count += 1
        if tag == "summary":
            self.summary_count += 1
        if tag == "th":
            self.th_scopes.append(attributes.get("scope", ""))
        if re.fullmatch(r"h[1-6]", tag):
            self.heading_levels.append(int(tag[1]))
        if tag == "meta" and attributes.get("name"):
            self.meta_names[attributes["name"]] = attributes.get("content", "")
        if tag == "title":
            self.title_count += 1


def _is_external_or_fragment(value: str) -> bool:
    scheme = urlsplit(value).scheme
    return bool(scheme) or value.startswith(("#", "mailto:", "tel:", "data:"))


def _relative_target(page: Path, value: str) -> Path:
    clean = value.split("#", 1)[0].split("?", 1)[0]
    return (page.parent / clean).resolve()


def _contrast_ratio(foreground: str, background: str) -> float:
    def luminance(color: str) -> float:
        channels = [
            int(color[index : index + 2], 16) / 255
            for index in (1, 3, 5)
        ]
        linear = [
            channel / 12.92
            if channel <= 0.04045
            else ((channel + 0.055) / 1.055) ** 2.4
            for channel in channels
        ]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    lighter = max(luminance(foreground), luminance(background))
    darker = min(luminance(foreground), luminance(background))
    return (lighter + 0.05) / (darker + 0.05)


def _css_variables(css: str) -> dict[str, str]:
    return {
        name: value.lower()
        for name, value in re.findall(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{6})", css)
    }


def validate_html_page(page: Path, site_root: Path) -> list[str]:
    errors: list[str] = []
    if not page.is_file():
        return [f"{page}: missing HTML page"]

    text = page.read_text(encoding="utf-8")
    parser = SiteHTMLParser()
    parser.feed(text)

    prefix = page.relative_to(site_root)
    for marker in AGENT_SKILLS_MARKERS:
        if marker not in text:
            errors.append(f"{prefix}: missing Agent Skills positioning marker: {marker}")
    for phrase in LEGACY_EXCLUSIVE_POSITIONING.get(page.name, ()):
        if phrase in text:
            errors.append(f"{prefix}: legacy single-client positioning remains: {phrase}")

    if not re.match(r"(?is)^\s*<!doctype html>", text):
        errors.append(f"{prefix}: missing HTML5 doctype")
    if parser.html_lang not in {"en", "zh-CN"}:
        errors.append(f"{prefix}: html lang must be 'en' or 'zh-CN'")
    for tag in ("header", "nav", "main", "section", "footer"):
        if tag not in parser.tags:
            errors.append(f"{prefix}: missing semantic <{tag}>")
    if parser.heading_levels.count(1) != 1:
        errors.append(f"{prefix}: expected exactly one h1")
    for previous, current in zip(parser.heading_levels, parser.heading_levels[1:]):
        if current > previous + 1:
            errors.append(
                f"{prefix}: heading level jumps from h{previous} to h{current}"
            )
    if "main-content" not in parser.ids:
        errors.append(f"{prefix}: main content target is missing")
    if "#main-content" not in parser.skip_targets:
        errors.append(f"{prefix}: skip link must target #main-content")
    if not all(parser.nav_labels):
        errors.append(f"{prefix}: every nav needs an aria-label")
    if parser.detail_count == 0 or parser.detail_count != parser.summary_count:
        errors.append(f"{prefix}: FAQ details/summary structure is incomplete")
    if parser.title_count != 1:
        errors.append(f"{prefix}: expected exactly one title element")
    if "viewport" not in parser.meta_names:
        errors.append(f"{prefix}: missing viewport meta tag")
    if "description" not in parser.meta_names:
        errors.append(f"{prefix}: missing description meta tag")
    if parser.meta_names.get("version") != RELEASE_VERSION:
        errors.append(
            f"{prefix}: version meta must be '{RELEASE_VERSION}'"
        )
    if any(scope not in {"col", "row"} for scope in parser.th_scopes):
        errors.append(f"{prefix}: every table header needs scope='col' or scope='row'")

    for attributes in parser.button_attrs:
        if attributes.get("type") != "button":
            errors.append(f"{prefix}: non-submit buttons need type='button'")
        if not attributes.get("aria-label"):
            errors.append(f"{prefix}: buttons need an aria-label")

    for attribute, value in parser.resources:
        if _is_external_or_fragment(value):
            continue
        if value.startswith("/") or value.startswith("../"):
            errors.append(f"{prefix}: root-relative asset path is not project-site safe: {value}")
            continue
        target = _relative_target(page, value)
        if site_root.resolve() not in target.parents and target != site_root.resolve():
            errors.append(f"{prefix}: asset escapes site directory: {value}")
        elif not target.is_file():
            errors.append(f"{prefix}: missing local asset from {attribute}: {value}")

    for href in parser.links:
        if not href or _is_external_or_fragment(href):
            continue
        if href.startswith("/") or href.startswith("../"):
            errors.append(f"{prefix}: root-relative link is not project-site safe: {href}")
            continue
        target = _relative_target(page, href)
        if not target.exists():
            errors.append(f"{prefix}: missing local link target: {href}")

    links = set(parser.links)
    for required in REQUIRED_REPOSITORY_LINKS:
        if required not in links:
            errors.append(f"{prefix}: missing key repository link: {required}")

    return errors


def validate_css(site_root: Path) -> list[str]:
    errors: list[str] = []
    css_path = site_root / "styles.css"
    if not css_path.is_file():
        return ["site/styles.css: missing stylesheet"]

    css = css_path.read_text(encoding="utf-8")
    for marker in (":focus-visible", ".skip-link", "prefers-reduced-motion"):
        if marker not in css:
            errors.append(f"site/styles.css: missing accessibility rule {marker}")

    variables = _css_variables(css)
    required_pairs = (
        ("ink", "paper"),
        ("muted", "paper"),
        ("surface", "accent"),
        ("surface", "ink"),
    )
    for foreground, background in required_pairs:
        if foreground not in variables or background not in variables:
            errors.append(
                f"site/styles.css: missing color variable for {foreground}/{background}"
            )
            continue
        ratio = _contrast_ratio(variables[foreground], variables[background])
        if ratio < 4.5:
            errors.append(
                f"site/styles.css: {foreground}/{background} contrast {ratio:.2f} is below 4.5"
            )

    for legacy_token in ("green-700", "green-600", "green-100"):
        if legacy_token in variables:
            errors.append(
                f"site/styles.css: misleading legacy color token remains: {legacy_token}"
            )

    return errors


def validate_skill_links(repo_root: Path, site_root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = repo_root / "skills"
    if not skills_root.is_dir():
        return ["skills/: missing curated skills directory"]

    skill_names = sorted(
        path.name.removeprefix("Geek-skills-")
        for path in skills_root.glob("Geek-skills-*")
        if path.is_dir()
    )
    if not skill_names:
        return ["skills/: no curated skill directories found"]

    for filename in SITE_PAGES:
        page = site_root / filename
        if not page.is_file():
            continue
        text = page.read_text(encoding="utf-8")
        for name in skill_names:
            expected = f"skills/Geek-skills-{name}/SKILL.md"
            if expected not in text:
                errors.append(f"site/{filename}: missing curated skill link: {name}")

    return errors


def validate_readmes(repo_root: Path) -> list[str]:
    errors: list[str] = []
    counts: dict[str, int] = {}
    for filename in ("README.md", "README.zh-CN.md"):
        path = repo_root / filename
        if not path.is_file():
            errors.append(f"{filename}: missing README")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in AGENT_SKILLS_MARKERS:
            if marker not in text:
                errors.append(
                    f"{filename}: missing Agent Skills positioning marker: {marker}"
                )
        for phrase in LEGACY_EXCLUSIVE_POSITIONING.get(filename, ()):
            if phrase in text:
                errors.append(
                    f"{filename}: legacy single-client positioning remains: {phrase}"
                )
        counts[filename] = text.count(EXPECTED_SITE_URL)
        if counts[filename] != 1:
            errors.append(
                f"{filename}: expected one canonical website link, found {counts[filename]}"
            )
        if RELEASE_URL not in text:
            errors.append(
                f"{filename}: missing release {RELEASE_VERSION} link"
            )

    if len(counts) == 2 and len(set(counts.values())) != 1:
        errors.append("README website links are not synchronized")

    return errors


def validate_release_version(repo_root: Path) -> list[str]:
    errors: list[str] = []
    version_path = repo_root / "VERSION"
    if not version_path.is_file():
        errors.append("VERSION: missing canonical release version file")
    elif version_path.read_text(encoding="utf-8").strip() != RELEASE_VERSION:
        errors.append(f"VERSION: expected '{RELEASE_VERSION}'")

    changelog = repo_root / "CHANGELOG.md"
    if not changelog.is_file():
        errors.append("CHANGELOG.md: missing changelog")
    elif f"## [{RELEASE_VERSION}]" not in changelog.read_text(encoding="utf-8"):
        errors.append(
            f"CHANGELOG.md: missing release heading for {RELEASE_VERSION}"
        )

    return errors


def validate_pages_workflow(repo_root: Path) -> list[str]:
    errors: list[str] = []
    workflow = repo_root / ".github" / "workflows" / "pages.yml"
    if not workflow.is_file():
        return [".github/workflows/pages.yml: missing Pages workflow"]

    text = workflow.read_text(encoding="utf-8")
    for marker in REQUIRED_WORKFLOW_MARKERS:
        if marker not in text:
            errors.append(f".github/workflows/pages.yml: missing '{marker}'")
    if not re.search(r"branches:\s*\[\s*main\s*\]", text):
        errors.append(".github/workflows/pages.yml: push branch must be main")
    if "url: ${{ steps.deployment.outputs.page_url }}" not in text:
        errors.append(".github/workflows/pages.yml: deployment URL output is missing")

    return errors


def validate_dependency_free_site(repo_root: Path, site_root: Path) -> list[str]:
    errors: list[str] = []
    if (site_root / "package.json").exists():
        errors.append("site/package.json: promotional site must remain dependency-free")
    if (site_root / "node_modules").exists():
        errors.append("site/node_modules: generated dependencies must not be present")
    if not (site_root / "script.js").is_file():
        errors.append("site/script.js: missing progressive-enhancement script")
    return errors


def validate_repo(repo_root: Path) -> list[str]:
    repo_root = repo_root.resolve()
    site_root = repo_root / "site"
    errors: list[str] = []

    for filename in SITE_PAGES:
        errors.extend(validate_html_page(site_root / filename, site_root))
    errors.extend(validate_css(site_root))
    errors.extend(validate_skill_links(repo_root, site_root))
    errors.extend(validate_readmes(repo_root))
    errors.extend(validate_release_version(repo_root))
    errors.extend(validate_pages_workflow(repo_root))
    errors.extend(validate_dependency_free_site(repo_root, site_root))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of scripts/)",
    )
    args = parser.parse_args(argv)

    errors = validate_repo(args.repo)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"SITE VALIDATION FAIL ({len(errors)} errors)")
        return 1

    print("validated 2 HTML pages, 13 curated skill links, and Pages workflow")
    print("SITE VALIDATION PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
