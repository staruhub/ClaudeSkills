# Example — 英黄工作室 · 训练营合作提案（HTML 渲染管线）

deck-studio 的**黑金提案系**样例：9 页商业提案（ChaoGeek AI 实战训练营）。
独立评审绝对分 **6.6/10**（三轮循环最高：极夜 6.0 → 英黄 6.6），评审语：
"封面圆形图形与米白反转页有真设计意识，黑金系统纪律性很强"。

![封面预览](preview-cover.png)

## 管线

```bash
npm i pptxgenjs
node generate.js          # html/p1..p9.html
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for i in $(seq 1 9); do "$CHROME" --headless=new --screenshot=png/p$i.png \
  --window-size=1280,720 --force-device-scale-factor=2 --hide-scrollbars html/p$i.html; done
node assemble.js          # -> chaogeek-bootcamp-proposal.pptx(含 speaker notes)
```

## 设计要点

- 英黄 token：`#0D0D0D` 黑 / `#E8B004` 暖黄 / `#F5F0E6` 米白；宣言式短句大标题
- **明暗反转节奏**：p4/p8 米白亮页打破全黑（评审点名 p4 为最强页——"米白反转
  打破节奏，中间黑卡形成天然焦点"）
- 单点题视觉：封面暖黄大圆 + 斜切线，少图、暗底、留白
- 时间线页每周挂"交付物"行——填空间的同时强化提案说服力（评审修复项）

## 本例沉淀的教训

- 卡片"头重-空腹-脚轻"是复发性疾病：中段必须有内容层（列表/示意图）——本例
  p4 在送评前被渲染自检抓出并修复，随后被评审评为全场最强页
- 时间线节点样式不统一（实心/空心混用）会被读作"未完成"语义，慎用
