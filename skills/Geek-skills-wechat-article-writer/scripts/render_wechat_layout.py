#!/usr/bin/env python3
"""Render a safe, deterministic WeChat inline-HTML fragment.

Three image flows, all inline-style only:
- standalone Markdown image lines `![caption](relative/path.png)` -> real <img>;
- manifest items with provider_status "generated" and an existing local
  asset_ref -> real <img>;
- every other manifest item -> traceable dashed placeholder box.

Image sources must be local files resolved against the article's directory;
external http(s) URLs and missing files are hard failures (no broken or
external images). Unsupported Markdown and raw HTML are escaped as text. No
publication, network, clipboard, or image-provider action is performed.
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
MD_IMAGE_LINE = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)\)$")
EXTERNAL_SRC = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://|^//")

CONTAINER = (
    "max-width:100%;box-sizing:border-box;padding:0 8px;"
    "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',sans-serif;"
    "font-size:16px;line-height:1.8;color:#3f3f3f;word-break:break-word;"
)
P_STYLE = "font-size:16px;line-height:1.8;color:#3f3f3f;margin:0 0 20px 0;padding:0;"
IMG_SECTION = "max-width:100%;box-sizing:border-box;margin:4px 0 20px 0;"
IMG_STYLE = (
    "display:block;max-width:100%;height:auto;margin:0 auto;"
    "border-radius:6px;border:1px solid #eee;"
)
CAPTION_STYLE = "margin:8px 0 0 0;font-size:13px;line-height:1.6;color:#999;text-align:center;"


def inline_markdown(text: str) -> str:
    escaped = html.escape(text, quote=True)
    return re.sub(
        r"\*\*(.+?)\*\*",
        r'<strong style="font-weight:600;color:#1a1a1a;">\1</strong>',
        escaped,
    )


def resolve_local_image(src: str, article_dir: Path) -> Path:
    if EXTERNAL_SRC.match(src):
        raise ValueError(f"image src must be a local file, got external URL: {src}")
    path = Path(src)
    if not path.is_absolute():
        path = article_dir / path
    return path


def render_image_figure(
    src: str, alt: str, caption: str | None, data_attrs: str = ""
) -> list[str]:
    src_esc = html.escape(src, quote=True)
    alt_esc = html.escape(alt or "图片", quote=True)
    lines = [
        f'<section style="{IMG_SECTION}"{data_attrs}>',
        f'<img src="{src_esc}" alt="{alt_esc}" style="{IMG_STYLE}">',
    ]
    if caption:
        lines.append(f'<p style="{CAPTION_STYLE}">{html.escape(caption, quote=True)}</p>')
    lines.append("</section>")
    return lines


def render_manifest_image(item: dict, article_dir: Path, stats: dict) -> list[str]:
    if item.get("provider_status") == "generated":
        asset = item.get("asset_ref", "")
        if not asset:
            raise ValueError(f"generated image {item['id']} has no asset_ref")
        if not resolve_local_image(asset, article_dir).is_file():
            raise ValueError(f"generated image asset missing: {asset}")
        caption = item.get("caption") or item.get("alt") or "图片"
        attrs = f' data-image-id="{html.escape(item["id"], quote=True)}"'
        stats["embedded"] += 1
        return render_image_figure(asset, item.get("alt") or "图片", caption, attrs)
    stats["placeholders"] += 1
    return render_placeholder(item)


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


def render(article: str, manifest: dict | None, article_dir: Path) -> tuple[str, dict]:
    by_id = {item["id"]: item for item in manifest["images"]} if manifest else {}
    stats = {"embedded": 0, "placeholders": 0}
    lines = article.splitlines()
    out = [f'<section style="{CONTAINER}">']
    index = 0
    in_list = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    while index < len(lines):
        raw = lines[index].strip()
        anchor_match = ANCHOR_LINE.fullmatch(raw)
        if anchor_match:
            close_list()
            image_id = anchor_match.group(1)
            if image_id not in by_id:
                raise ValueError(
                    f"article contains placeholder {image_id} but no manifest item covers it; "
                    "supply a validated --manifest or remove the anchor"
                )
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
            out.extend(render_manifest_image(by_id[image_id], article_dir, stats))
            index = next_index + 1
            continue
        if not raw:
            close_list()
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
        close_list()
        image_match = MD_IMAGE_LINE.fullmatch(raw)
        if image_match:
            alt, src = image_match.group(1), image_match.group(2)
            if not resolve_local_image(src, article_dir).is_file():
                raise ValueError(f"markdown image not found next to the article: {src}")
            stats["embedded"] += 1
            out.extend(render_image_figure(src, alt, alt or None))
            index += 1
            continue
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
    close_list()
    out.append("</section>")
    return "\n".join(out) + "\n", stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--article", required=True, type=Path)
    parser.add_argument(
        "--manifest",
        required=False,
        type=Path,
        default=None,
        help="validated image-manifest.json; required only when the article "
        "contains {{IMAGE:...}} placeholders",
    )
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        article_bytes = args.article.read_bytes()
        article = canonical_utf8_lf(article_bytes).decode("utf-8")
        manifest = None
        if args.manifest is not None:
            manifest = load_manifest(args.manifest)
            errors = validate_manifest(manifest, article_bytes)
            if errors:
                raise ValueError("; ".join(errors))
        rendered, stats = render(article, manifest, args.article.parent)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"ERROR {exc}")
        return 1
    print(
        f"PASS rendered {stats['embedded']} embedded image(s), "
        f"{stats['placeholders']} placeholder(s) to {args.output}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
