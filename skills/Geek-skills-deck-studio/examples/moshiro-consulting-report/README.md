# Example — 墨白咨询 · 成果汇报（HTML 渲染管线）

deck-studio 的**明色系**标杆样例：9 页咨询风成果汇报。三评委盲评击败上一代实现
（42.3 vs 29.7），沉淀了七条设计原则：视觉概念先行 / 极端对比 / 网格+破格 /
质感纵深 / 明暗节奏 / 文字主角 / 光学细节。

![封面预览](preview-cover.png)

## 管线（模式 B 视觉路线）

```bash
node generate.js          # 产出 html/p1..p9.html（1280×720，CSS 变量 token）
# 逐页截图(2×DPI,字体由渲染机的 Chrome 锁定,无 fallback 风险):
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for i in $(seq 1 9); do "$CHROME" --headless=new --screenshot=png/p$i.png \
  --window-size=1280,720 --force-device-scale-factor=2 --hide-scrollbars html/p$i.html; done
# 再用 pptxgenjs 把 png 全幅贴入 pptx(见 polar-night 样例的 assemble.js)
```

## 设计要点（改内容时不许破坏）

- **重锚点**：粗黑标题（800）+ 巨型幽灵字/数字英雄；细体（200-300）只做对比层——
  盲评证实"全盘细体"是退步（v4 教训，3:0 落败）
- 蓝图网格底纹是贯穿母题；强调色唯一（蓝），只标关键数据
- 明暗节奏：p3/p8 深色蓄力页，其余明色；数据页必须有真图形（19 格阵列）

## 已知坑

- JS 字符串里的中文引号用「」或全角，直引号会 `SyntaxError`
- 幽灵大字注意与标题的碰撞裁切（本例封面第一版就撞了，渲染自检抓出）
