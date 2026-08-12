#!/usr/bin/env bash
# Idempotent Cloud Agent bootstrap for ClaudeSkills.
#
# The Python L1 gates (scripts/validate.py, scripts/run_routing_evals.py) and the
# pure-Python contract cases rely only on the standard library, so they need no
# setup. This script prepares the two pieces that do:
#   1. the Vite/React/TypeScript website under website/, and
#   2. the Node tooling the deck-studio contract tests use to render HTML with a
#      headless browser and assemble a PPTX (playwright + pptxgenjs + Chromium).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1) Website dependencies.
npm --prefix "$REPO_ROOT/website" ci

# 2) Node tooling for tests/task_b/run_contract_tests.py (deck-studio).
#    Installed outside the repository and exposed through Node's ~/.node_modules
#    resolution fallback, so `require("playwright")` / `require("pptxgenjs")`
#    resolve from the skill and test scripts without an env var or a committed
#    root node_modules tree.
NODE_TOOLS_DIR="$HOME/.cache/claudeskills-node-tools"
mkdir -p "$NODE_TOOLS_DIR"
cat > "$NODE_TOOLS_DIR/package.json" <<'JSON'
{
  "name": "claudeskills-node-tools",
  "private": true,
  "dependencies": {
    "playwright": "1.62.1",
    "pptxgenjs": "4.0.1"
  }
}
JSON
npm --prefix "$NODE_TOOLS_DIR" install --no-audit --no-fund
rm -rf "$HOME/.node_modules"
ln -sfn "$NODE_TOOLS_DIR/node_modules" "$HOME/.node_modules"

# 3) Chromium browser plus its OS libraries for the headless renderer.
"$NODE_TOOLS_DIR/node_modules/.bin/playwright" install --with-deps chromium
