#!/usr/bin/env python3
"""Render a safe, deterministic WeChat inline-HTML fragment.

Unsupported Markdown and raw HTML are escaped as text. No publication, network,
clipboard, or image-provider action is performed.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

from validate_image_manifest import canonical_utf8_lf, load_manifest, validate_manifest

ANCHOR_LINE = re.compile(r"^<!-- image:(img-[a-z0-9][a-z0-9-]{2,63}) -->$")
PLACEHOLDER_LINE = re.compile(r"^\{\{IMAGE:(img-[a-z0-9][a-z0-9-]{2,63})\}\}$")

CONTAINER = (
    "max-width:100%;box-sizing:border-box;padding:0 8px;"
    "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',sans-serif;"
    "font-size:16px;line-height:1.8;color:#3f3f3f;word-break:break-word;"
)
P_STYLE = "font-size:16px;line-height:1.8;color:#3f3f3f;margin:0 0 20px 0;padding:0;"


def inline_markdown(text: str) -> str:
    escaped = html.escape(text, quote=True)
    return re.sub(
        r"\*\*(.+?)\*\*",
        r'<strong style="font-weight:600;color:#1a1a1a;">\1</strong>',
        escaped,
    )


def render_placeholder(item: dict) -> list[str]:
    image_id = html.escape(item["id"], quote=True)
    anchor = html.escape(item["placement_anchor"], quote=True)
    alt = html.escape(item["alt"], quote=True)
    caption = html.escape(item["caption"], quote=True)
    size = f"{item['width']}×{item['height']} · {item['aspect_ratio']}"
    return [
        item["placement_anchor"],
        (
            f'<section data-image-id="{image_id}" data-placement-anchor="{anchor}" '
            'style="max-width:100%;box-sizing:border-box;margin:20px 0;">'
        ),
        (
            f'<p data-placeholder="{html.escape(item["placeholder"], quote=True)}" '
            'style="max-width:100%;box-sizing:border-box;margin:0;padding:28px 16px;'
            'border:1px dashed #9aa6b2;background:#f7f9fc;color:#58616b;'
            f'text-align:center;font-size:14px;line-height:1.6;">图片提示词已准备（未生成）：{alt}'
            f'<br><span style="font-size:12px;color:#8a949e;">{size}</span></p>'
        ),
        (
            f'<p style="margin:6px 0 0 0;font-size:13px;line-height:1.6;'
            f'color:#999;text-align:center;">{caption}</p>'
        ),
        "</section>",
    ]


def render(article: str, manifest: dict) -> str:
    by_id = {item["id"]: item for item in manifest["images"]}
    lines = article.splitlines()
    out = [f'<section style="{CONTAINER}">']
    index = 0
    in_list = False
    while index < len(lines):
        raw = lines[index].strip()
        anchor_match = ANCHOR_LINE.fullmatch(raw)
        if anchor_match:
            if in_list:
                out.append("</ul>")
                in_list = False
            image_id = anchor_match.group(1)
            next_index = index + 1
            while next_index < len(lines) and not lines[next_index].strip():
                next_index += 1
            placeholder = (
                PLACEHOLDER_LINE.fullmatch(lines[next_index].strip())
                if next_index < len(lines)
                else None
            )
            if not placeholder or placeholder.group(1) != image_id:
                raise ValueError(f"anchor {image_id} is not followed by its placeholder")
            out.extend(render_placeholder(by_id[image_id]))
            index = next_index + 1
            continue
        if not raw:
            if in_list:
                out.append("</ul>")
                in_list = False
            index += 1
            continue
        if raw.startswith("- "):
            if not in_list:
                out.append(
                    '<ul style="margin:16px 0;padding-left:24px;max-width:100%;box-sizing:border-box;">'
                )
                in_list = True
            out.append(
                f'<li style="margin:8px 0;font-size:16px;line-height:1.7;color:#3f3f3f;">'
                f"{inline_markdown(raw[2:])}</li>"
            )
            index += 1
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        if raw == "---":
            out.append('<hr style="border:none;border-top:1px solid #eee;margin:32px 0;">')
        elif raw.startswith("### "):
            out.append(
                '<h3 style="font-size:18px;font-weight:600;color:#2c2c2c;'
                f'line-height:1.4;margin:24px 0 12px 0;">{inline_markdown(raw[4:])}</h3>'
            )
        elif raw.startswith("## "):
            out.append(
                '<h2 style="font-size:20px;font-weight:700;color:#1a1a1a;line-height:1.4;'
                'margin:32px 0 16px 0;padding-left:12px;border-left:4px solid #4A90D9;">'
                f"{inline_markdown(raw[3:])}</h2>"
            )
        elif raw.startswith("# "):
            out.append(
                '<h1 style="font-size:24px;font-weight:700;color:#1a1a1a;line-height:1.4;'
                f'margin:0 0 16px 0;padding:0;">{inline_markdown(raw[2:])}</h1>'
            )
        elif raw.startswith("> "):
            out.append(
                '<blockquote style="margin:20px 0;padding:16px 20px;background:#f7f9fc;'
                'border-left:3px solid #4A90D9;font-size:15px;color:#555;line-height:1.7;">'
                f'<p style="margin:0;">{inline_markdown(raw[2:])}</p></blockquote>'
            )
        else:
            out.append(f'<p style="{P_STYLE}">{inline_markdown(raw)}</p>')
        index += 1
    if in_list:
        out.append("</ul>")
    out.append("</section>")
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--article", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        article_bytes = args.article.read_bytes()
        article = canonical_utf8_lf(article_bytes).decode("utf-8")
        manifest = load_manifest(args.manifest)
        errors = validate_manifest(manifest, article_bytes)
        if errors:
            raise ValueError("; ".join(errors))
        rendered = render(article, manifest)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"ERROR {exc}")
        return 1
    print(f"PASS rendered {len(manifest['images'])} mapped placeholders to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
