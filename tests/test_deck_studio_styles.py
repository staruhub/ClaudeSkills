#!/usr/bin/env python3
"""Deck Studio style-library schema and integrity tests.

Tests:
1. Inventory: all styles in SKILL.md table exist on disk
2. Schema: every style has 10 required fields + Style Brief
3. Color validation: hex colors are well-formed
4. Uniqueness: no duplicate H1 titles
5. Negative: invalid styles fail validation
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

REPO = Path(__file__).resolve().parents[1]
DECK = REPO / "skills" / "Geek-skills-deck-studio"
STYLE_LIB = DECK / "style-library"

REQUIRED_FIELDS = [
    "一句话定位",
    "适用场景",
    "不适用场景",
    "色板",
    "字体气质",
    "版式特征",
    "图像倾向",
    "页面密度",
    "标题语气",
    "image2 适配",
    "直接导出 PPT",
]


class StyleMeta(NamedTuple):
    path: Path
    title: str
    fields: dict[str, str]
    has_style_brief: bool
    colors: list[str]


def parse_style_file(path: Path) -> StyleMeta:
    """Parse a style markdown file and extract metadata."""
    text = path.read_text(encoding="utf-8")
    
    # Extract H1 title
    title_match = re.match(r"^# (.+)$", text, re.MULTILINE)
    if not title_match:
        raise ValueError(f"{path.name}: missing H1 title")
    title = title_match.group(1).strip()
    
    # Extract fields (list items with **field**) - allow any text in parentheses after field name
    fields = {}
    for field in REQUIRED_FIELDS:
        # Match field name with optional note in parentheses (Chinese or English)
        pattern = rf"^- \*\*{re.escape(field)}(?:[（(][^)）]+[）)])?\*\*[：:]\s*(.+)$"
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            fields[field] = match.group(1).strip()
    
    # Check for Style Brief section - allow variants
    has_style_brief = bool(re.search(r"^## Style Brief[（(]注入生成器[）)]$", text, re.MULTILINE))
    
    # Extract hex colors
    colors = re.findall(r"`#([0-9A-Fa-f]{3,6})`", text)
    
    return StyleMeta(path, title, fields, has_style_brief, colors)


def validate_hex_color(color: str) -> bool:
    """Check if a color is a valid 3 or 6 digit hex."""
    return len(color) in (3, 6) and all(c in "0123456789ABCDEFabcdef" for c in color)


def test_inventory() -> None:
    """Test 1: Verify all styles in SKILL.md exist on disk."""
    print("\n=== Test 1: Inventory Check ===")
    
    skill_md = (DECK / "SKILL.md").read_text(encoding="utf-8")
    
    # Extract style paths from the table
    table_paths = re.findall(r"`((?:business|creative|education|tech|media|custom)/[^`]+\.md)`", skill_md)
    
    missing = []
    for rel_path in table_paths:
        full_path = STYLE_LIB / rel_path
        if not full_path.exists():
            missing.append(rel_path)
    
    if missing:
        raise AssertionError(f"Missing style files referenced in SKILL.md: {missing}")
    
    # Check that all actual style files are listed (exclude _smoke and other non-style files)
    actual_files = []
    for category in ["business", "creative", "education", "tech", "media", "custom"]:
        category_dir = STYLE_LIB / category
        if category_dir.exists():
            actual_files.extend(category_dir.glob("*.md"))
    
    actual_rel = [str(f.relative_to(STYLE_LIB)) for f in actual_files]
    
    unlisted = [f for f in actual_rel if f not in table_paths]
    if unlisted:
        raise AssertionError(f"Style files not listed in SKILL.md table: {unlisted}")
    
    print(f"✓ Inventory check passed: {len(table_paths)} styles referenced, all exist on disk")
    print(f"✓ No orphan style files found")


def test_schema() -> None:
    """Test 2: Verify every style has required fields and Style Brief."""
    print("\n=== Test 2: Schema Validation ===")
    
    # Only check actual style files in category directories
    style_files = []
    for category in ["business", "creative", "education", "tech", "media", "custom"]:
        category_dir = STYLE_LIB / category
        if category_dir.exists():
            style_files.extend(sorted(category_dir.glob("*.md")))
    
    errors = []
    
    for path in style_files:
        try:
            meta = parse_style_file(path)
            rel_path = path.relative_to(STYLE_LIB)
            
            # Check required fields
            missing_fields = [f for f in REQUIRED_FIELDS if f not in meta.fields]
            if missing_fields:
                errors.append(f"{rel_path}: missing fields {missing_fields}")
            
            # Check Style Brief
            if not meta.has_style_brief:
                errors.append(f"{rel_path}: missing Style Brief section")
            
        except Exception as e:
            errors.append(f"{path.relative_to(STYLE_LIB)}: {e}")
    
    if errors:
        raise AssertionError(f"Schema validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
    
    print(f"✓ Schema validation passed: {len(style_files)} styles, all have 10 fields + Style Brief")


def test_colors() -> None:
    """Test 3: Verify hex colors are well-formed."""
    print("\n=== Test 3: Color Validation ===")
    
    # Only check actual style files in category directories
    style_files = []
    for category in ["business", "creative", "education", "tech", "media", "custom"]:
        category_dir = STYLE_LIB / category
        if category_dir.exists():
            style_files.extend(sorted(category_dir.glob("*.md")))
    
    errors = []
    
    for path in style_files:
        meta = parse_style_file(path)
        rel_path = path.relative_to(STYLE_LIB)
        
        invalid_colors = [c for c in meta.colors if not validate_hex_color(c)]
        if invalid_colors:
            errors.append(f"{rel_path}: invalid hex colors {invalid_colors}")
        
        if not meta.colors:
            errors.append(f"{rel_path}: no hex colors found in 色板 field")
    
    if errors:
        raise AssertionError(f"Color validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
    
    total_colors = sum(len(parse_style_file(p).colors) for p in style_files)
    print(f"✓ Color validation passed: {len(style_files)} styles, {total_colors} total hex colors")


def test_uniqueness() -> None:
    """Test 4: Verify no duplicate H1 titles."""
    print("\n=== Test 4: Title Uniqueness ===")
    
    # Only check actual style files in category directories
    style_files = []
    for category in ["business", "creative", "education", "tech", "media", "custom"]:
        category_dir = STYLE_LIB / category
        if category_dir.exists():
            style_files.extend(sorted(category_dir.glob("*.md")))
    
    titles = {}
    
    for path in style_files:
        meta = parse_style_file(path)
        if meta.title in titles:
            raise AssertionError(
                f"Duplicate title '{meta.title}' in:\n"
                f"  - {titles[meta.title].relative_to(STYLE_LIB)}\n"
                f"  - {path.relative_to(STYLE_LIB)}"
            )
        titles[meta.title] = path
    
    print(f"✓ Uniqueness check passed: {len(titles)} unique style titles")


def test_negative() -> None:
    """Test 5: Invalid styles should fail validation."""
    print("\n=== Test 5: Negative Tests ===")
    
    # Test missing Style Brief
    invalid_no_brief = """# 测试风格

- **一句话定位**：测试
- **适用场景**：测试
- **不适用场景**：测试
- **色板**：`#FFFFFF` / `#000000`
- **字体气质**：测试
- **版式特征**：测试
- **图像倾向**：测试
- **页面密度**：测试
- **标题语气**：测试
- **image2 适配**：测试
- **直接导出 PPT**：测试
"""
    
    temp_path = STYLE_LIB / "_test_invalid.md"
    try:
        temp_path.write_text(invalid_no_brief, encoding="utf-8")
        meta = parse_style_file(temp_path)
        if meta.has_style_brief:
            raise AssertionError("Should have detected missing Style Brief")
        print("✓ Negative test 1 passed: missing Style Brief detected")
    finally:
        if temp_path.exists():
            temp_path.unlink()
    
    # Test missing required field
    invalid_missing_field = """# 测试风格

- **一句话定位**：测试
- **适用场景**：测试
- **不适用场景**：测试
- **字体气质**：测试
- **版式特征**：测试
- **图像倾向**：测试
- **页面密度**：测试
- **标题语气**：测试
- **image2 适配**：测试
- **直接导出 PPT**：测试

## Style Brief（注入生成器）

测试风格描述
"""
    
    try:
        temp_path.write_text(invalid_missing_field, encoding="utf-8")
        meta = parse_style_file(temp_path)
        missing = [f for f in REQUIRED_FIELDS if f not in meta.fields]
        if not missing or "色板" not in missing:
            raise AssertionError("Should have detected missing 色板 field")
        print("✓ Negative test 2 passed: missing required field detected")
    finally:
        if temp_path.exists():
            temp_path.unlink()


def test_existing_styles() -> None:
    """Test 6: Verify the 3 existing styles still parse correctly."""
    print("\n=== Test 6: Existing Styles ===")
    
    existing = [
        "creative/yinghuang-studio.md",
        "business/heibai-ledger.md",
        "creative/tanghe-frame.md",
    ]
    
    for rel_path in existing:
        path = STYLE_LIB / rel_path
        if not path.exists():
            raise AssertionError(f"Existing style missing: {rel_path}")
        
        meta = parse_style_file(path)
        
        # Verify all required fields present
        missing = [f for f in REQUIRED_FIELDS if f not in meta.fields]
        if missing:
            raise AssertionError(f"{rel_path}: missing fields {missing}")
        
        # Verify Style Brief
        if not meta.has_style_brief:
            raise AssertionError(f"{rel_path}: missing Style Brief")
    
    print(f"✓ Existing styles check passed: {len(existing)} pre-existing styles validated")


def main() -> int:
    """Run all tests."""
    print("Deck Studio Style Library Tests")
    print("=" * 60)
    
    try:
        test_inventory()
        test_schema()
        test_colors()
        test_uniqueness()
        test_negative()
        test_existing_styles()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        return 0
        
    except AssertionError as e:
        print("\n" + "=" * 60)
        print(f"✗ TEST FAILED:\n{e}")
        return 1
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ UNEXPECTED ERROR:\n{e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
