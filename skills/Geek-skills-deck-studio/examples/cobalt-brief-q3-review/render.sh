#!/bin/bash
# 简单的批量渲染脚本
set -e

EXAMPLE_DIR="/workspace/skills/Geek-skills-deck-studio/examples/cobalt-brief-q3-review"
HTML_DIR="$EXAMPLE_DIR/html"
PNG_DIR="$EXAMPLE_DIR/png"
CHROME="/usr/local/bin/chrome"

mkdir -p "$PNG_DIR"

echo "Rendering 5 HTML pages to PNG..."

for i in 1 2 3 4 5; do
    HTML_FILE="$HTML_DIR/p$i.html"
    PNG_FILE="$PNG_DIR/p$i.png"
    TMP_DIR="/tmp/chrome-render-$$-$i"
    
    echo -n "  p$i.html... "
    
    $CHROME \
        --headless \
        --disable-gpu \
        --no-sandbox \
        --disable-dev-shm-usage \
        --user-data-dir="$TMP_DIR" \
        --screenshot="$PNG_FILE" \
        --window-size=1280,720 \
        --hide-scrollbars \
        "file://$HTML_FILE" >/dev/null 2>&1
    
    if [ -f "$PNG_FILE" ]; then
        SIZE=$(ls -lh "$PNG_FILE" | awk '{print $5}')
        echo "✓ ($SIZE)"
    else
        echo "✗ FAILED"
    fi
    
    rm -rf "$TMP_DIR"
done

echo
echo "PNG files:"
ls -lh "$PNG_DIR"
