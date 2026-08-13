const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const p = new pptxgen();
p.defineLayout({ name: "W", width: 13.333, height: 7.5 });
p.layout = "W";

const pngDir = path.join(__dirname, "png");
const outputPath = path.join(__dirname, "cobalt-brief-q3-review.pptx");

const notes = [
  "封面：Q3 战略评审简报，钴蓝简报风格。奶油纸底色搭配电光钴蓝标题，展现现代专业简报感。",
  "议程：四项关键议题——营收增长、市场份额、运营效率和下一步计划。清晰的结构化汇报框架。",
  "核心洞察：Q3 营收同比增长 28%，增速连续三季度加速。大客户续约率 94%，交叉销售成功率从 18% 提升至 31%。",
  "市场份额：行业排名从第三提升至第二位，市占率 18.4%，新增 312 个客户账户。NPS 从 42 上升至 51。",
  "下一步：Q4 四大战略重点——巩固市场地位、扩张新市场、产品迭代、成本优化。董事会批准 8,500 万元投入，预期增速保持在 25%+。"
];

console.log(`开始组装 PPTX: ${outputPath}`);
console.log(`PNG 目录: ${pngDir}`);

for (let i = 1; i <= 5; i++) {
  const imagePath = path.join(pngDir, `p${i}.png`);
  
  if (!fs.existsSync(imagePath)) {
    throw new Error(`missing rendered page: ${imagePath}`);
  }
  
  const s = p.addSlide();
  s.addImage({ path: imagePath, x: 0, y: 0, w: 13.333, h: 7.5 });
  s.addNotes(notes[i - 1]);
  
  console.log(`  ✓ 第 ${i} 页: ${path.basename(imagePath)} (${(fs.statSync(imagePath).size / 1024).toFixed(0)} KB)`);
}

p.writeFile({ fileName: outputPath })
  .then(() => {
    const size = fs.statSync(outputPath).size;
    console.log(`\n✓ PPTX 生成成功:`);
    console.log(`  文件: ${outputPath}`);
    console.log(`  大小: ${(size / 1024).toFixed(0)} KB (${size} bytes)`);
    console.log(`  页数: 5`);
    console.log(`  格式: 全屏图片 + speaker notes`);
  })
  .catch(error => {
    console.error("生成失败:", error);
    process.exitCode = 1;
  });
