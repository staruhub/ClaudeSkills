#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const { chromium } = require("playwright");

const VIEWPORT = { width: 1280, height: 720 };
const BLEED_SELECTOR = '[data-deck-background-bleed="true"]';

async function inspectPageGeometry(page, label) {
  const report = await page.evaluate(
    ({ viewportWidth, viewportHeight, bleedSelector }) => {
      const rectData = rect => ({
        x: rect.x,
        y: rect.y,
        width: rect.width,
        height: rect.height,
        right: rect.right,
        bottom: rect.bottom,
      });
      const describe = element => {
        const testId = element.getAttribute("data-test-id");
        if (testId) return `[data-test-id="${testId}"]`;
        if (element.id) return `${element.tagName.toLowerCase()}#${element.id}`;
        const classes = Array.from(element.classList).slice(0, 3);
        return `${element.tagName.toLowerCase()}${classes.map(name => `.${name}`).join("")}`;
      };
      const outsideViewport = rect =>
        rect.left < 0 ||
        rect.top < 0 ||
        rect.right > viewportWidth ||
        rect.bottom > viewportHeight;
      const visible = (style, rect) =>
        style.display !== "none" &&
        style.visibility !== "hidden" &&
        style.visibility !== "collapse" &&
        Number.parseFloat(style.opacity || "1") > 0 &&
        rect.width > 0 &&
        rect.height > 0;

      const htmlStyle = getComputedStyle(document.documentElement);
      const bodyStyle = getComputedStyle(document.body);
      const allowedBackgroundBleeds = [];
      const invalidBackgroundBleeds = [];
      const foregroundOverflows = [];

      for (const element of document.body.querySelectorAll("*")) {
        const bleedRoot = element.closest(bleedSelector);
        if (bleedRoot) {
          if (bleedRoot !== element) continue;
          const style = getComputedStyle(element);
          const rect = element.getBoundingClientRect();
          const validMarker =
            (style.position === "absolute" || style.position === "fixed") &&
            style.zIndex === "0" &&
            style.pointerEvents === "none" &&
            element.getAttribute("aria-hidden") === "true";
          const item = {
            element: describe(element),
            rect: rectData(rect),
            position: style.position,
            zIndex: style.zIndex,
            pointerEvents: style.pointerEvents,
            ariaHidden: element.getAttribute("aria-hidden"),
          };
          if (!validMarker) {
            invalidBackgroundBleeds.push(item);
          } else if (outsideViewport(rect)) {
            allowedBackgroundBleeds.push(item);
          }
          continue;
        }
        const style = getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        if (visible(style, rect) && outsideViewport(rect)) {
          foregroundOverflows.push({
            element: describe(element),
            rect: rectData(rect),
            position: style.position,
            zIndex: style.zIndex,
          });
        }
      }

      return {
        viewport: {
          innerWidth,
          innerHeight,
          clientWidth: document.documentElement.clientWidth,
          clientHeight: document.documentElement.clientHeight,
        },
        documentElement: {
          rect: rectData(document.documentElement.getBoundingClientRect()),
          scrollWidth: document.documentElement.scrollWidth,
          scrollHeight: document.documentElement.scrollHeight,
          overflowX: htmlStyle.overflowX,
          overflowY: htmlStyle.overflowY,
        },
        body: {
          rect: rectData(document.body.getBoundingClientRect()),
          scrollWidth: document.body.scrollWidth,
          scrollHeight: document.body.scrollHeight,
          overflowX: bodyStyle.overflowX,
          overflowY: bodyStyle.overflowY,
        },
        allowedBackgroundBleeds,
        invalidBackgroundBleeds,
        foregroundOverflows: foregroundOverflows.slice(0, 20),
      };
    },
    {
      viewportWidth: VIEWPORT.width,
      viewportHeight: VIEWPORT.height,
      bleedSelector: BLEED_SELECTOR,
    }
  );

  const exactRect = rect =>
    rect.x === 0 &&
    rect.y === 0 &&
    rect.width === VIEWPORT.width &&
    rect.height === VIEWPORT.height &&
    rect.right === VIEWPORT.width &&
    rect.bottom === VIEWPORT.height;
  const issues = [];
  if (
    report.viewport.innerWidth !== VIEWPORT.width ||
    report.viewport.innerHeight !== VIEWPORT.height ||
    report.viewport.clientWidth !== VIEWPORT.width ||
    report.viewport.clientHeight !== VIEWPORT.height
  ) {
    issues.push("viewport is not exactly 1280x720");
  }
  if (!exactRect(report.documentElement.rect)) {
    issues.push("documentElement rect is not exactly 1280x720 at 0,0");
  }
  if (!exactRect(report.body.rect)) {
    issues.push("body rect is not exactly 1280x720 at 0,0");
  }
  if (
    report.documentElement.scrollWidth !== VIEWPORT.width ||
    report.documentElement.scrollHeight !== VIEWPORT.height
  ) {
    issues.push("documentElement scroll geometry is not exactly 1280x720");
  }
  for (const [name, value] of [
    ["html overflow-x", report.documentElement.overflowX],
    ["html overflow-y", report.documentElement.overflowY],
    ["body overflow-x", report.body.overflowX],
    ["body overflow-y", report.body.overflowY],
  ]) {
    if (value !== "hidden") issues.push(`${name} must be hidden, got ${value}`);
  }
  if (report.invalidBackgroundBleeds.length) {
    issues.push("background bleed marker contract violated");
  }
  if (report.foregroundOverflows.length) {
    issues.push("visible foreground element exceeds the viewport");
  }
  if (issues.length) {
    throw new Error(`${label} geometry contract failed: ${issues.join("; ")}: ${JSON.stringify(report)}`);
  }
  return report;
}

async function runOverflowContractRegression(page, fixtureDir) {
  const allowedPath = path.join(fixtureDir, "background-bleed-allowed.html");
  const rejectedPath = path.join(fixtureDir, "foreground-overflow-rejected.html");
  for (const fixture of [allowedPath, rejectedPath]) {
    if (!fs.existsSync(fixture)) throw new Error(`missing overflow fixture ${fixture}`);
  }
  await page.goto(pathToFileURL(allowedPath).href, { waitUntil: "load" });
  const allowed = await inspectPageGeometry(page, "background bleed fixture");
  if (allowed.allowedBackgroundBleeds.length !== 1) {
    throw new Error(`background bleed fixture did not exercise one allowed bleed: ${JSON.stringify(allowed)}`);
  }

  await page.goto(pathToFileURL(rejectedPath).href, { waitUntil: "load" });
  let rejected = false;
  try {
    await inspectPageGeometry(page, "foreground overflow fixture");
  } catch (error) {
    const message = String(error && error.message ? error.message : error);
    if (
      message.includes("visible foreground element exceeds the viewport") &&
      message.includes('data-test-id=\\"foreground-overflow\\"')
    ) {
      rejected = true;
    } else {
      throw error;
    }
  }
  if (!rejected) throw new Error("foreground overflow fixture unexpectedly passed");
  process.stdout.write("PASS overflow contract: marked background bleed accepted; foreground overflow rejected\n");
}

async function main() {
  const inputIndex = process.argv.indexOf("--input-dir");
  const outputIndex = process.argv.indexOf("--output-dir");
  if (inputIndex < 0 || outputIndex < 0) {
    throw new Error(
      "usage: render_deck_html.cjs --input-dir DIR --output-dir DIR " +
      "[--overflow-fixture-dir DIR] [--executable-path FILE]"
    );
  }
  const inputDir = path.resolve(process.argv[inputIndex + 1]);
  const outputDir = path.resolve(process.argv[outputIndex + 1]);
  const overflowFixtureIndex = process.argv.indexOf("--overflow-fixture-dir");
  const overflowFixtureDir =
    overflowFixtureIndex >= 0
      ? path.resolve(process.argv[overflowFixtureIndex + 1])
      : null;
  const executableIndex = process.argv.indexOf("--executable-path");
  const executablePath =
    executableIndex >= 0
      ? path.resolve(process.argv[executableIndex + 1])
      : process.env.PLAYWRIGHT_EXECUTABLE_PATH;
  if (executablePath && !fs.existsSync(executablePath)) {
    throw new Error(`browser executable does not exist: ${executablePath}`);
  }
  fs.mkdirSync(outputDir, { recursive: true });
  const launchOptions = { headless: true };
  if (executablePath) launchOptions.executablePath = executablePath;
  const browser = await chromium.launch(launchOptions);
  try {
    const page = await browser.newPage({ viewport: VIEWPORT });
    const externalRequests = [];
    page.on("request", request => {
      const url = request.url();
      if (!url.startsWith("file:") && !url.startsWith("data:")) externalRequests.push(url);
    });
    if (overflowFixtureDir) {
      await runOverflowContractRegression(page, overflowFixtureDir);
    }
    for (let index = 1; index <= 9; index += 1) {
      const htmlPath = path.join(inputDir, `p${index}.html`);
      if (!fs.existsSync(htmlPath)) throw new Error(`missing input ${htmlPath}`);
      await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "load" });
      await inspectPageGeometry(page, `page ${index}`);
      await page.screenshot({
        path: path.join(outputDir, `p${index}.png`),
        type: "png",
        fullPage: false,
      });
    }
    if (externalRequests.length) {
      throw new Error(`external requests detected: ${externalRequests.join(", ")}`);
    }
  } finally {
    await browser.close();
  }
  process.stdout.write(`PASS rendered 9 local pages with geometry contract to ${outputDir}\n`);
}

main().catch(error => {
  process.stderr.write(`ERROR ${error.stack || error}\n`);
  process.exitCode = 1;
});
