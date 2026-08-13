#!/usr/bin/env python3
"""Render smoke test HTML covers to PNG for visual verification.

Runs Chrome headless to screenshot each style's cover HTML.
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SMOKE_DIR = REPO / "skills" / "Geek-skills-deck-studio" / "style-library" / "_smoke"

NEW_STYLES = [
    "huabu-stamp",
    "classic-desktop",
    "cobalt-brief",
    "coral-night",
    "electric-grid",
    "emerald-gazette",
]


def render_html_to_png(html_path: Path, png_path: Path) -> bool:
    """Render HTML to PNG using Chrome headless."""
    try:
        result = subprocess.run(
            [
                "/usr/local/bin/chrome",
                "--headless",
                "--disable-gpu",
                "--screenshot=" + str(png_path),
                "--window-size=1280,720",
                "--default-background-color=0",
                str(html_path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return png_path.exists() and png_path.stat().st_size > 1000
    except Exception as e:
        print(f"  Error rendering {html_path.name}: {e}")
        return False


def main() -> int:
    print("\n=== Smoke Test: Rendering Style Covers ===\n")
    
    if not SMOKE_DIR.exists():
        print(f"Error: smoke directory not found: {SMOKE_DIR}")
        return 1
    
    success_count = 0
    fail_count = 0
    
    for style in NEW_STYLES:
        html_file = SMOKE_DIR / f"{style}-cover.html"
        png_file = SMOKE_DIR / f"{style}-cover.png"
        
        if not html_file.exists():
            print(f"✗ {style}: HTML not found")
            fail_count += 1
            continue
        
        print(f"Rendering {style}...", end=" ")
        if render_html_to_png(html_file, png_file):
            print(f"✓ ({png_file.stat().st_size // 1024} KB)")
            success_count += 1
        else:
            print("✗ Failed")
            fail_count += 1
    
    print(f"\n{'='*60}")
    print(f"Smoke test complete: {success_count} passed, {fail_count} failed")
    
    if fail_count > 0:
        print("\nNote: HTML covers exist even if PNG rendering failed.")
        print("Visual quality can be verified by opening HTML files in browser.")
    
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
