# ClaudeSkills acceptance record — 2026-07-30

This record captures the reproducible local acceptance evidence for the README,
GitHub Pages site, and the Deck Studio, Deep Research, Product Manager, and
WeChat Article Writer skill upgrades. It does not represent a production LLM,
image-provider, publishing, or external-research run.

## Baseline and external engineering handoff

- Repository: `staruhub/ClaudeSkills`
- Baseline commit: `3d4045d6af94504f30e4a21f154fea62bb8242c7`
- Skills Work conversation:
  <https://chatgpt.com/c/6a6b7531-368c-83ea-be03-84bd7a254054>
- README/Pages Work conversation:
  <https://chatgpt.com/c/6a6b7cf1-5de8-83ea-bdc4-de7d91a2589c>
- Source handoff ZIP: `1,125,484` bytes,
  SHA-256 `0D3BCADFF5631889CD6F2AB43AA4BF1FECA232D086843DA86E59D9A42459164D`
- README/Pages delivery ZIP: `1,214,792` bytes,
  SHA-256 `469C1307510DD8899FAEB75B9444206B94F64C08CA02A8477B0DE63732FF1897`
- Skills r3 delivery ZIP: `1,504,046` bytes,
  SHA-256 `5067CAF8B68742728BEF909CE68657E061B46C62CEC223D203380A6A0DA45200`
- Deck r4 delivery ZIP: `47,138` bytes,
  SHA-256 `F4A344F90A1D6130FE6D4993D3E5851B06FC25DD82253278943BFF71F2DFB81C`

The source handoff archive contained 283 entries and no denylisted credential,
browser-state, database, `.git`, `node_modules`, or environment files. Gitleaks
reported one reviewed false positive: the repository's private-key detection
regular expression itself. The r4 archive contained 42 entries, no unsafe or
denylisted paths, and 27 manifest entries whose SHA-256 digests were all
independently verified.

## Coordinator corrections

The first Skills response used an incomplete supplement and introduced
WorkBuddy/Publisher scope. It was rejected. The corrected delivery restored the
repository's `pm-04 -> keqian-method` routing and removed the unrelated scope.

The r2 delivery then failed on Windows because PM and WeChat hashes depended on
CRLF bytes and subprocess output used the default code page. r3 normalized only
CRLF/CR to LF before strict UTF-8 SHA-256, added fixture-integrity checks, and
decoded subprocess output explicitly as UTF-8.

The r3 Deck contract still produced `16 PASS / 0 BLOCKED / 1 FAIL`: it treated
an intentionally clipped, z-index-0 decorative SVG as visible overflow. r4
replaced that heuristic with a viewport/content geometry contract, an explicit
`data-deck-background-bleed` marker, and paired browser regressions proving that
marked decorative bleed passes while ordinary foreground overflow fails.

## Implemented scope

- Reworked the English and Chinese READMEs around purpose, installability,
  capability boundaries, honest evidence, the 13-skill catalog, contribution,
  and the project website.
- Added a dependency-free bilingual static website plus an accessibility-aware
  progressive-enhancement script and project-site-safe assets.
- Added a GitHub Pages workflow and a fail-closed site validator with positive
  and intentionally invalid fixtures.
- Added Deck Studio composition guards, local-only rendering, raster-PPTX
  assembly checks, and explicit non-editability disclosure.
- Made Deep Research citation verification fail closed and source evaluation
  deterministic with an explicit `--as-of` date.
- Added Product Manager's evidence-first, one-question-at-a-time
  `grill-me-to-doc` state machine, resume integrity, document completion gate,
  and unconditional implementation hard stop.
- Added WeChat article, image-prompts, layout, and full-pipeline modes with a
  versioned provider-neutral manifest, deterministic adjacent mapping, raw HTML
  escaping, and explicit no-generation/no-publishing boundaries.

## Independent automated results

All commands below ran on Windows in the isolated worktree.

| Gate | Result |
| --- | --- |
| `python scripts/validate.py` | PASS — 13 skills |
| `python scripts/run_routing_evals.py` | PASS — 91 cases across 10 skills |
| `python -m py_compile` over every `skills/**/*.py` | PASS — 13 files |
| `node --check` over Deck/task-b JavaScript | PASS — 7 files |
| `python tests/task_b/verify_fixture_integrity.py` | PASS — PM/WeChat hashes; 9 negative errors |
| `python scripts/validate_site.py` | PASS — 2 pages, 13 curated skill links, Pages workflow |
| `python -m unittest tests.test_site_validation` | PASS — 2 tests |
| Invalid site fixture | Expected FAIL — 35 errors, exit 1 |
| `git diff --check` | PASS |

With Google Chrome and the bundled Playwright/PptxGenJS runtime configured:

```text
PASS 17 passed, 0 blocked, 0 failed
```

The 17 cases cover static/reference checks; Product Manager positive, resume,
single-question failure, and implementation-stop failure; all four WeChat
modes, CRLF portability, raw HTML escaping, and invalid manifest rejection;
Deep Research citation/as-of, delta/resume, and invented-URL rejection; Deck
generation, missing-page rejection, real 1280x720 Chrome rendering, background
bleed acceptance, foreground overflow rejection, 9 PNGs, and PPTX assembly;
and a credential-pattern scan over 127 files.

The resulting nine-slide PPTX is `710,925` bytes with SHA-256
`936D3FBFD65A5BB27F44A65C1F7C1F57786DCAE83DCC63D328AC9E3CAFDB596F`.
The independent presentation overflow checker passed. Slides are full-slide
raster images and are therefore not editable.

The JSON contract summary is `29,488` bytes with SHA-256
`63D35563C33DF86A4985CFC9FE92AEA026197311ECA1F2C5A19670BFADAEEA7B`.

## Real browser site review

The final local site was checked in Google Chrome at 1440x900, 390x844, and
320x720. English and Chinese pages returned 200, kept exactly one H1, exposed
all 13 skill links and 91 routing definitions, and had no horizontal overflow,
page exceptions, or console errors. The skip link was first in the tab order;
copy feedback, FAQ mouse/keyboard activation, hash navigation, language
switching, and external repository links were exercised.

## Boundaries still requiring honest disclosure

- The deterministic contracts exercise the skill workflows and their
  fail-closed boundaries, not the subjective quality of an arbitrary future
  model response.
- No real image provider, WeChat publishing account, production user data, or
  external research reachability was used.
- The Deck PPTX passed structural and overflow checks, but Office/LibreOffice
  rendering fidelity was not separately verified.
- Publication evidence is recorded only after the GitHub Pages workflow and
  live URL have been independently checked.
