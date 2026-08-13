# 钴蓝简报 Q3 评审示例

真实的 5 页高管简报 deck，使用钴蓝简报风格（`business/cobalt-brief.md`）。

## 风格参数

- **色板**：奶油纸 `#F6F1E8` + 电光钴蓝 `#0047AB`
- **字体**：思源黑体 + DIN 等宽数字
- **版式**：充足留白，钴蓝标题高对比，细线分隔
- **场景**：高管简报、战略评审

## 文件结构

```
.
├── generate.js          # 生成 HTML (1280×720)
├── render.sh            # Chrome headless 渲染 PNG
├── assemble.js          # PptxGenJS 组装 PPTX
├── html/                # 5 页 HTML 源文件
├── png/                 # 渲染的 PNG (2x, ~30-75KB/页)
├── preview-cover.png    # 封面预览
└── cobalt-brief-q3-review.pptx  # 最终 PPTX (359 KB)
```

## 重建方法

```bash
# 1. 生成 HTML
node generate.js

# 2. 渲染 PNG (需要 Chrome)
bash render.sh

# 3. 组装 PPTX (需要 pptxgenjs)
npm install pptxgenjs
node assemble.js
```

## 页面内容

1. **封面** - 战略评审简报标题
2. **议程** - 四项关键议题（营收、市场、运营、下一步）
3. **核心洞察** - Q3 营收同比 +28%，大数据卡片展示
4. **数据页** - 市场份额提升至行业第二，3 个指标卡片
5. **下一步** - Q4 战略重点与预算批准

## 验证结果

- ✅ 所有页面 1280×720, `overflow:hidden`
- ✅ 钴蓝简报色板严格遵循（奶油纸 + 电光钴蓝）
- ✅ PNG 渲染成功，视觉质量验证通过
- ✅ PPTX 包含 speaker notes
- ✅ 文件大小：367,524 bytes (359 KB)
