# WeChat article pipeline contract

This contract keeps writing, image prompting, image generation, layout, and
publishing as separate capabilities. The skill implements the first, second,
and layout handoff only. It never publishes.

## Modes

### `article`

Input: source material and writing brief.

Output: UTF-8 `article.md`. Do not create a manifest unless the user requests
image prompts or the full pipeline.

### `image-prompts`

Input: final or draft `article.md`.

Output:

1. the same article with deterministic image anchor/placeholder pairs;
2. `image-manifest.json` conforming to
   `schemas/image-manifest.schema.json`.

Stop after prompt generation. Set `provider_status` to `prompt-only`. Do not
call an image provider and do not claim an image exists.

### `layout`

Input: `article.md` and, when placeholders exist,
`image-manifest.json`.

Output: a single `<section>` fragment in `layout.html` using inline styles.
Every manifest item becomes one traceable placeholder block unless a verified
generated asset was explicitly supplied.

### `full-pipeline`

Run `article` → `image-prompts` → `layout`. Emit the three artifacts and stop.
This mode still does not generate images or publish the article.

## Deterministic image mapping

For an image ID `img-agent-contract`:

- anchor: `<!-- image:img-agent-contract -->`
- placeholder: `{{IMAGE:img-agent-contract}}`

Place the two lines together at the intended insertion point. The manifest must
repeat both strings exactly. IDs are stable across reruns when purpose and
placement have not changed. Use semantic IDs; never use array indexes or random
UUIDs.

`article_sha256` is calculated over canonical article text bytes: decode as
strict UTF-8, replace CRLF and bare CR with LF, encode as UTF-8, then hash with
SHA-256. No other Unicode or whitespace normalization is allowed. Mapping is
then checked on that canonical text: the anchor line must be immediately
followed by its placeholder line, with exactly one LF separator and no blank
line. This gives Windows and Unix the same digest without weakening adjacency.

The manifest validator rejects:

- duplicate or unstable IDs;
- missing fields or dimensions;
- aspect ratio inconsistent with width/height;
- anchor/placeholder strings that do not derive from the ID;
- article/manifest hash mismatch;
- missing, duplicate, or extra article mappings;
- `generated` status without an explicit asset reference.

## Provider-neutral boundary

`positive_prompt` and `negative_prompt` describe the desired result without
provider-specific flags, model names, account IDs, API parameters, or secrets.
`provider_status` records lifecycle only:

- `not-requested`
- `prompt-only`
- `generating`
- `generated`
- `failed`
- `blocked`

The skill itself may emit only `not-requested` or `prompt-only`. A separate image
provider adapter may update status and `asset_ref` after real execution and
verification.

## Layout Skill handoff

Preferred host interface:

- capability: `排版输出` / WeChat inline layout;
- inputs: exact `article.md`, optional validated manifest, theme ID or default;
- outputs: `layout.html`, consumed image IDs, unresolved image IDs, warnings;
- required behavior: preserve mapping, escape raw HTML, use inline styles only,
  enforce mobile width, and perform no publishing.

Do not couple this prompt skill to a desktop UI, clipboard, image host, account,
or Tauri command. If the host layout capability is absent, run:

`python3 scripts/render_wechat_layout.py --article article.md --manifest image-manifest.json --output layout.html`

The fallback renderer is deliberately small and deterministic. It supports the
core Markdown needed by the example and safely escapes unsupported raw HTML.

## Failure behavior

- Missing manifest with article placeholders: stop and request or rebuild the
  manifest.
- Invalid manifest: show the validator errors; do not render partial HTML.
- Layout adapter unavailable: use the deterministic fallback and disclose the
  reduced Markdown feature set.
- Image provider unavailable or denied: keep prompt-only placeholders.
- Publication request: return files and say publication requires a separate,
  explicit user-controlled action.

## Validation

Run:

`python3 scripts/validate_image_manifest.py image-manifest.json --article article.md`

Then render. Treat any non-zero exit as a hard failure.
