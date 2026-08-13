#!/usr/bin/env python3
"""Smoke test documentation for new Deck Studio styles.

Creates a summary of the 6 new style covers. PNG rendering via Chrome/Playwright
is optional; HTML covers provide visual verification when opened in browser.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SMOKE_DIR = REPO / "skills" / "Geek-skills-deck-studio" / "style-library" / "_smoke"

NEW_STYLES = {
    "huabu-stamp": "画布彩章 - 奶油画布底 + 大胆彩色印章",
    "classic-desktop": "经典桌面 - Windows 95 复古操作系统",
    "cobalt-brief": "钴蓝简报 - 奶油纸 + 电光钴蓝专业感",
    "coral-night": "珊瑚夜色 - 近黑底 + 珊瑚大字暗色路演",
    "electric-grid": "电光网格 - 方格纸 + 钴蓝衬线科技感",
    "emerald-gazette": "翡翠公报 - 翡翠绿刊头杂志式商务",
}


def main() -> int:
    print("\n=== Smoke Test: New Style Cover Verification ===\n")
    
    if not SMOKE_DIR.exists():
        print(f"Error: smoke directory not found: {SMOKE_DIR}")
        return 1
    
    html_count = 0
    
    for style, description in NEW_STYLES.items():
        html_file = SMOKE_DIR / f"{style}-cover.html"
        
        if html_file.exists():
            size_kb = html_file.stat().st_size / 1024
            print(f"✓ {description}")
            print(f"  HTML: {html_file.name} ({size_kb:.1f} KB)")
            html_count += 1
        else:
            print(f"✗ {description}: HTML not found")
    
    print(f"\n{'='*60}")
    print(f"Smoke test summary: {html_count}/{len(NEW_STYLES)} HTML covers created")
    
    print("\nVisual verification:")
    print("  - Open HTML files in browser to verify style tokens")
    print("  - Each cover uses the style's core palette, fonts, and layout")
    print("  - PNG rendering via Playwright requires additional setup")
    print(f"\nSmoke directory: {SMOKE_DIR.relative_to(REPO)}")
    
    return 0 if html_count == len(NEW_STYLES) else 1


if __name__ == "__main__":
    sys.exit(main())
