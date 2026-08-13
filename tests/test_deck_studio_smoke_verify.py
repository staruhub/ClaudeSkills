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

IDENTITY_EXAMPLES = {
    "coral-night-numbers-correct": "珊瑚夜色数字页正确示例 - 一个巨型数字",
    "yinghuang-numbers-correct": "荧黄工作室数字页正确示例 - 一句话结论",
    "huabu-stamp-cover-correct": "画布彩章封面正确示例 - 不规则印章",
}


def main() -> int:
    print("\n=== Smoke Test: New Style Cover Verification ===\n")
    
    if not SMOKE_DIR.exists():
        print(f"Error: smoke directory not found: {SMOKE_DIR}")
        return 1
    
    html_count = 0
    
    print("Style Covers (6):")
    for style, description in NEW_STYLES.items():
        html_file = SMOKE_DIR / f"{style}-cover.html"
        
        if html_file.exists():
            size_kb = html_file.stat().st_size / 1024
            print(f"✓ {description}")
            print(f"  HTML: {html_file.name} ({size_kb:.1f} KB)")
            html_count += 1
        else:
            print(f"✗ {description}: HTML not found")
    
    print("\nIdentity Verification Examples (3):")
    identity_count = 0
    for basename, description in IDENTITY_EXAMPLES.items():
        html_file = SMOKE_DIR / f"{basename}.html"
        
        if html_file.exists():
            size_kb = html_file.stat().st_size / 1024
            print(f"✓ {description}")
            print(f"  HTML: {html_file.name} ({size_kb:.1f} KB)")
            identity_count += 1
        else:
            print(f"✗ {description}: HTML not found")
    
    total_expected = len(NEW_STYLES) + len(IDENTITY_EXAMPLES)
    total_found = html_count + identity_count
    
    print(f"\n{'='*60}")
    print(f"Smoke test summary: {total_found}/{total_expected} HTML files verified")
    
    print("\nVisual verification:")
    print("  - Open HTML files in browser to verify style tokens")
    print("  - Each cover uses the style's core palette, fonts, and layout")
    print("  - Identity examples demonstrate correct vs incorrect layouts")
    print("  - PNG rendering via Playwright requires additional setup")
    print(f"\nSmoke directory: {SMOKE_DIR.relative_to(REPO)}")
    
    return 0 if total_found == total_expected else 1


if __name__ == "__main__":
    sys.exit(main())
