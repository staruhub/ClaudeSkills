#!/usr/bin/env node
// Chrome headless 渲染器（不依赖 Playwright）
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const htmlDir = path.join(__dirname, "html");
const pngDir = path.join(__dirname, "png");
const chromePath = "/usr/local/bin/chrome";

async function renderWithChrome(htmlPath, pngPath) {
  return new Promise((resolve, reject) => {
    const args = [
      "--headless",
      "--disable-gpu",
      "--disable-dev-shm-usage",
      "--no-sandbox",
      `--screenshot=${pngPath}`,
      "--window-size=1280,720",
      "--default-background-color=0",
      "--hide-scrollbars",
      `file://${htmlPath}`,
    ];

    const proc = spawn(chromePath, args, { stdio: "pipe" });
    let stderr = "";

    proc.stderr.on("data", data => {
      stderr += data.toString();
    });

    proc.on("close", code => {
      if (code === 0 && fs.existsSync(pngPath)) {
        resolve();
      } else {
        reject(new Error(`Chrome exited with code ${code}: ${stderr}`));
      }
    });

    proc.on("error", reject);

    // Timeout after 15 seconds
    setTimeout(() => {
      proc.kill();
      reject(new Error("Chrome rendering timeout"));
    }, 15000);
  });
}

async function render() {
  if (!fs.existsSync(pngDir)) fs.mkdirSync(pngDir, { recursive: true });

  const htmlFiles = fs.readdirSync(htmlDir).filter(f => f.endsWith(".html")).sort();
  console.log(`Found ${htmlFiles.length} HTML files to render`);

  let success = 0;
  let failed = 0;

  for (const file of htmlFiles) {
    const htmlPath = path.join(htmlDir, file);
    const pngPath = path.join(pngDir, file.replace(".html", ".png"));

    try {
      console.log(`Rendering ${file}...`);
      await renderWithChrome(htmlPath, pngPath);
      const size = (fs.statSync(pngPath).size / 1024).toFixed(0);
      console.log(`  ✓ ${file.replace(".html", ".png")} (${size} KB)`);
      success++;
    } catch (error) {
      console.error(`  ✗ ${file}: ${error.message}`);
      failed++;
    }
  }

  console.log(`\n✓ Rendered ${success} pages successfully`);
  if (failed > 0) console.log(`✗ Failed: ${failed} pages`);

  return failed === 0 ? 0 : 1;
}

render().then(code => process.exit(code));
