document.documentElement.classList.add("js");

async function copyText(text) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const fallback = document.createElement("textarea");
  fallback.value = text;
  fallback.setAttribute("readonly", "");
  fallback.style.position = "fixed";
  fallback.style.opacity = "0";
  document.body.append(fallback);
  fallback.select();
  const copied = document.execCommand("copy");
  fallback.remove();

  if (!copied) {
    throw new Error("Copy is not supported");
  }
}

for (const button of document.querySelectorAll("[data-copy-target]")) {
  button.addEventListener("click", async () => {
    const targetId = button.getAttribute("data-copy-target");
    const target = targetId ? document.getElementById(targetId) : null;
    const status = document.getElementById("copy-status");

    if (!target) {
      return;
    }

    const originalLabel = button.textContent;
    let resultLabel;

    try {
      await copyText(target.textContent.trim());
      resultLabel = document.documentElement.lang === "zh-CN" ? "已复制" : "Copied";
    } catch {
      resultLabel = document.documentElement.lang === "zh-CN" ? "复制失败" : "Copy failed";
    }

    button.textContent = resultLabel;
    if (status) {
      status.textContent = resultLabel;
    }

    window.setTimeout(() => {
      button.textContent = originalLabel;
    }, 1800);
  });
}
