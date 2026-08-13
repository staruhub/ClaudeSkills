// deck-studio 实战: Q3 战略评审 · 钴蓝简报风格
// 风格参数: 奶油纸 #F6F1E8 + 电光钴蓝 #0047AB, 现代专业简报感
const fs = require("fs");
const path = require("path");

const T = {
  cream: "#F6F1E8",
  cobalt: "#0047AB",
  black: "#111111",
  gray: "#E8E8E8",
  dimGray: "#888888",
  sans: '"PingFang SC","Hiragino Sans GB",sans-serif',
  mono: '"DIN Alternate","SF Mono",monospace',
};

const CSS = `
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}
html,body{width:1280px;height:720px;overflow:hidden;}
body{background:${T.cream};color:${T.black};font-family:${T.sans};position:relative;}
.top{position:absolute;left:100px;right:100px;top:60px;display:flex;justify-content:space-between;align-items:center;z-index:5;}
.kick{font-size:12px;letter-spacing:.2em;color:${T.cobalt};font-weight:700;text-transform:uppercase;}
.brand{font-size:11px;letter-spacing:.18em;color:${T.dimGray};}
.foot{position:absolute;left:100px;right:100px;bottom:80px;border-top:2px solid ${T.cobalt};padding-top:16px;display:flex;justify-content:space-between;align-items:center;z-index:5;}
.date{font-size:14px;font-weight:700;color:${T.cobalt};}
.pg{font-size:13px;color:${T.dimGray};}
.stage{position:absolute;left:100px;right:100px;top:140px;bottom:160px;z-index:2;display:flex;flex-direction:column;}
.h{font-weight:900;letter-spacing:-.01em;line-height:1.15;color:${T.cobalt};}
.h-black{font-weight:900;letter-spacing:-.01em;line-height:1.15;color:${T.black};}
.subtitle{font-weight:400;color:${T.black};line-height:1.6;font-size:20px;margin-top:48px;}
.body{font-weight:400;color:${T.black};line-height:1.65;font-size:17px;}
.light{color:${T.dimGray};}
.line{height:2px;background:${T.gray};margin:24px 0;}
.card{background:#FFF;padding:28px 32px;border:1px solid ${T.gray};}
.number{font-family:${T.mono};font-weight:700;font-feature-settings:"tnum";}
`;

function P(section, inner, no, totalPages = 5) {
  return `<!doctype html><meta charset="utf-8"><style>${CSS}</style><body>
<div class="top"><span class="kick">${section}</span><span class="brand">Q3 STRATEGIC REVIEW</span></div>
<div class="stage">${inner}</div>
<div class="foot"><span class="date">Q3 2026</span><span class="pg">${String(no).padStart(2, "0")}</span></div>
</body>`;
}

const pages = [];

/* 1 封面 */
pages.push(P("战略评审 · Cover", `
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;max-width:1080px;">
    <div class="h" style="font-size:88px;">战略评审<br>简报</div>
    <div class="subtitle">高管简报 · 钴蓝简报风格</div>
  </div>
`, 1));

/* 2 议程 */
pages.push(P("议程 · Agenda", `
  <div class="h" style="font-size:52px;margin-bottom:48px;">四项关键议题</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:32px;">
    ${[
      ["01", "营收增长", "Q3 营收同比 +28%，连续三季度增速"],
      ["02", "市场份额", "核心市场份额提升至行业第二位"],
      ["03", "运营效率", "获客成本下降 15%，ROI 显著改善"],
      ["04", "下一步", "Q4 战略重点与资源配置建议"]
    ].map(([n, t, d]) => `
      <div style="display:flex;align-items:center;gap:40px;">
        <span class="h number" style="font-size:48px;width:100px;">${n}</span>
        <div style="flex:1;">
          <div class="h-black" style="font-size:24px;margin-bottom:8px;">${t}</div>
          <div class="body" style="font-size:16px;color:${T.dimGray};">${d}</div>
        </div>
      </div>
    `).join("")}
  </div>
`, 2));

/* 3 核心洞察 */
pages.push(P("01 营收增长 · Insight", `
  <div class="h" style="font-size:56px;margin-bottom:56px;">Q3 营收同比增长 28%，<br>增速连续三季度加速</div>
  <div style="display:flex;gap:48px;">
    <div class="card" style="flex:1;">
      <div class="h number" style="font-size:72px;color:${T.cobalt};">28<span style="font-size:48px;">%</span></div>
      <div class="body" style="margin-top:20px;font-size:16px;">同比增长率</div>
      <div class="light" style="margin-top:8px;font-size:14px;">vs Q2: +24%, Q1: +19%</div>
    </div>
    <div class="card" style="flex:1;">
      <div class="h number" style="font-size:72px;color:${T.cobalt};">3.2<span style="font-size:48px;">亿</span></div>
      <div class="body" style="margin-top:20px;font-size:16px;">Q3 营收（人民币）</div>
      <div class="light" style="margin-top:8px;font-size:14px;">超出预算 12%</div>
    </div>
  </div>
  <div style="margin-top:40px;">
    <div class="body" style="font-size:17px;line-height:1.8;">
      <strong>驱动因素：</strong>大客户续约率达 94%，新客户获客效率提升，产品线交叉销售成功率从 18% 提升至 31%。
    </div>
  </div>
`, 3));

/* 4 数据页 */
pages.push(P("02 市场份额 · Data", `
  <div class="h" style="font-size:52px;margin-bottom:56px;">市场份额提升至行业第二位</div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:32px;margin-bottom:40px;">
    ${[
      ["行业排名", "#2", "from #3 in Q2"],
      ["市场份额", "18.4%", "+2.7 pts vs Q2"],
      ["客户数量", "1,847", "+312 new accounts"]
    ].map(([label, value, note]) => `
      <div class="card">
        <div class="body" style="font-size:15px;color:${T.dimGray};margin-bottom:16px;">${label}</div>
        <div class="h number" style="font-size:56px;color:${T.cobalt};">${value}</div>
        <div class="light" style="font-size:13px;margin-top:12px;">${note}</div>
      </div>
    `).join("")}
  </div>
  <div class="body" style="font-size:16px;line-height:1.75;">
    <div style="margin-bottom:12px;"><strong>关键进展：</strong></div>
    <div>• 核心产品线市占率从 15.7% 提升至 18.4%，超越 CompetitorB</div>
    <div>• 三个战略行业（金融、制造、零售）的渗透率均实现双位数增长</div>
    <div>• NPS（净推荐值）从 42 上升至 51，客户满意度显著提升</div>
  </div>
`, 4));

/* 5 结论与下一步 */
pages.push(P("04 下一步 · Next Steps", `
  <div class="h" style="font-size:52px;margin-bottom:56px;">Q4 战略重点</div>
  <div style="display:flex;flex-direction:column;gap:36px;">
    ${[
      {
        title: "1. 巩固市场地位",
        desc: "重点投入大客户成功团队，目标续约率 ≥95%，深化产品集成度"
      },
      {
        title: "2. 扩张新市场",
        desc: "启动华南区扩张计划，Q4 新增 3 个城市办公室，招聘 45 人"
      },
      {
        title: "3. 产品迭代",
        desc: "11 月发布 v3.0，主打 AI 增强功能，内测 NPS 已达 67"
      },
      {
        title: "4. 成本优化",
        desc: "持续优化获客渠道，目标 Q4 CAC 再降 8%，LTV/CAC 比提升至 4.2"
      }
    ].map(({ title, desc }) => `
      <div>
        <div class="h-black" style="font-size:22px;margin-bottom:12px;">${title}</div>
        <div class="body" style="font-size:16px;color:${T.dimGray};">${desc}</div>
      </div>
    `).join("")}
  </div>
  <div class="line"></div>
  <div class="body" style="font-size:16px;text-align:center;color:${T.cobalt};font-weight:600;">
    董事会批准预算：Q4 投入 8,500 万元，预期 Q4 营收增速保持在 25%+
  </div>
`, 5));

// 写入文件
const htmlDir = path.join(__dirname, "html");
if (!fs.existsSync(htmlDir)) fs.mkdirSync(htmlDir, { recursive: true });

pages.forEach((html, i) => {
  fs.writeFileSync(path.join(htmlDir, `p${i + 1}.html`), html, "utf-8");
});

console.log(`✓ 已生成 ${pages.length} 页 HTML (钴蓝简报风格)`);
console.log(`  目录: ${htmlDir}`);
console.log(`  尺寸: 1280×720, overflow:hidden`);
console.log(`  色板: 奶油纸 ${T.cream} + 电光钴蓝 ${T.cobalt}`);
