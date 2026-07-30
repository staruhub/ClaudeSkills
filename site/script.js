document.documentElement.classList.add("js");

for (const button of document.querySelectorAll("[data-copy-target]")) {
  button.addEventListener("click", async () => {
    const targetId = button.getAttribute("data-copy-target");
    const target = targetId ? document.getElementById(targetId) : null;

    if (!target || !navigator.clipboard) {
      return;
    }

    const originalLabel = button.textContent;

    try {
      await navigator.clipboard.writeText(target.textContent.trim());
      button.textContent = document.documentElement.lang === "zh-CN" ? "已复制" : "Copied";
    } catch {
      button.textContent = document.documentElement.lang === "zh-CN" ? "复制失败" : "Copy failed";
    }

    window.setTimeout(() => {
      button.textContent = originalLabel;
    }, 1800);
  });
}
