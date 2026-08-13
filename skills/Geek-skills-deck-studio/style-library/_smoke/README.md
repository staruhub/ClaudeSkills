# Smoke Test Covers

此目录包含 6 个新风格的 HTML 封面示例（1280×720），用于视觉验证。

## 文件列表

- huabu-stamp-cover.html - 画布彩章风格封面
- classic-desktop-cover.html - 经典桌面风格封面
- cobalt-brief-cover.html - 钴蓝简报风格封面
- coral-night-cover.html - 珊瑚夜色风格封面
- electric-grid-cover.html - 电光网格风格封面
- emerald-gazette-cover.html - 翡翠公报风格封面

## 身份验证示例（反模式修复）

以下 3 个文件展示风格身份的正确构图，避免"正交拆维执行成换皮"陷阱：

- coral-night-numbers-correct.html - 珊瑚夜色数字页：一个巨型数字占 40%+ 画面，≤15 词结论，无三栏 KPI
- yinghuang-numbers-correct.html - 荧黄工作室数字页：一个大数字 + 一句话（≤20 词），无多列布局
- huabu-stamp-cover-correct.html - 画布彩章封面：不规则印章色块在角落，不是 full-height sidebar

## 使用方法

在浏览器中直接打开任意 HTML 文件，查看该风格的核心色板、字体和版式。每个封面使用该风格的实际 token，展示视觉签名。

## 验证

运行 `python3 tests/test_deck_studio_smoke_verify.py` 验证所有封面文件存在。
