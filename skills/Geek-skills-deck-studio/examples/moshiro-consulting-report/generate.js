// deck-studio v3 · 墨白咨询「设计系统」版
// 七原则:概念先行/极端对比/网格+破格/质感纵深/明暗节奏/文字主角/光学细节
const fs = require("fs");

const CSS = `
:root{
  --ink:#111214; --g1:#3A3D42; --g2:#6B6F76; --g3:#A2A6AD; --g4:#D2D5DA;
  --line:#E7E9ED; --mist:#F4F5F7; --blue:#0B5CD6; --blued:#0842A0; --bg:#FFFFFF;
  --dark:#111214; --dg:#8A9099; --dmist:#1C1F24;
  --m:80px;
}
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}
html,body{width:1280px;height:720px;overflow:hidden;}
body{background:var(--bg);color:var(--ink);position:relative;
  font-family:"PingFang SC","Hiragino Sans GB",sans-serif;
  /* 质感层:极淡网格底纹 */
  background-image:linear-gradient(var(--mist) 1px,transparent 1px),linear-gradient(90deg,var(--mist) 1px,transparent 1px);
  background-size:40px 40px;}
.num{font-family:"DIN Alternate","Helvetica Neue",sans-serif;font-feature-settings:"tnum";}
.top{position:absolute;left:var(--m);right:var(--m);top:46px;display:flex;
  justify-content:space-between;align-items:baseline;z-index:5;}
.kick{font-size:11px;letter-spacing:.34em;color:var(--g3);font-weight:600;}
.brand{font-size:11px;letter-spacing:.28em;color:var(--g4);}
.foot{position:absolute;left:var(--m);right:var(--m);bottom:38px;display:flex;
  justify-content:space-between;align-items:center;z-index:5;}
.src{font-size:10.5px;letter-spacing:.06em;color:var(--g4);}
.pg{font-size:12px;color:var(--g3);letter-spacing:.08em;}
.stage{position:absolute;left:var(--m);right:var(--m);top:118px;bottom:98px;z-index:2;}
/* 极端字重对比 */
.h{font-weight:800;letter-spacing:-.01em;line-height:1.18;}
.thin{font-weight:300;}
.hl{color:var(--blue);}
.tag{width:44px;height:4px;background:var(--ink);}
/* 深色页 */
.dark-bg{background:var(--dark)!important;background-image:linear-gradient(#191c21 1px,transparent 1px),linear-gradient(90deg,#191c21 1px,transparent 1px)!important;background-size:40px 40px!important;color:#F5F6F8;}
.dark-bg .kick{color:var(--dg);} .dark-bg .brand{color:#3A3D42;}
.dark-bg .src{color:#3A3D42;} .dark-bg .pg{color:var(--dg);}
.dark-bg .tag{background:var(--blue);}
.ghost{position:absolute;font-family:"DIN Alternate",sans-serif;font-weight:800;
  color:var(--mist);z-index:0;line-height:.8;letter-spacing:-.04em;user-select:none;}
.dark-bg .ghost{color:#181b20;}
.cap{color:var(--g2);line-height:1.65;}
.chip{display:inline-block;padding:5px 12px;border:1px solid var(--line);border-radius:2px;
  font-size:12px;color:var(--g2);margin-right:8px;}
`;

// 骨架
function P(section, inner, no, opt = {}) {
  return `<!doctype html><meta charset="utf-8"><style>${CSS}</style>
<body class="${opt.dark ? "dark-bg" : ""}">
<div class="top"><span class="kick">${section}</span><span class="brand">GEEK SKILLS · FABLE 5</span></div>
${opt.ghost || ""}
<div class="stage">${inner}</div>
<div class="foot"><span class="src">github.com/staruhub/ClaudeSkills</span><span class="pg num">${String(no).padStart(2, "0")} · 09</span></div>
</body>`;
}
const CK = `<svg width="18" height="18" viewBox="0 0 16 16" style="vertical-align:-3px;margin-right:10px"><path d="M2 8.5 6.5 13 14 3" fill="none" stroke="#0B5CD6" stroke-width="2.6"/></svg>`;
const pages = [];

/* 1 封面 — 概念:标题撞出血 + 巨型幽灵年号,极端字重 */
pages.push(P("成果汇报 / COVER", `
  <div class="ghost num" style="right:-30px;top:150px;font-size:420px;">5</div>
  <div style="position:absolute;top:70px;left:0;width:920px;">
    <div class="tag" style="margin-bottom:34px;"></div>
    <div class="h" style="font-size:82px;">把个人收藏夹，</div>
    <div class="h" style="font-size:82px;">重构成<span class="hl">可验证</span>的</div>
    <div class="h" style="font-size:82px;">Skills 仓库<span class="thin" style="font-size:82px;color:var(--g4);">。</span></div>
    <div style="margin-top:40px;font-size:17px;color:var(--g2);font-weight:300;letter-spacing:.02em;">
      Fable 5 重构 <span style="color:var(--g4);">/</span> 自审报告 <span style="color:var(--g4);">/</span> Skill Quality Standard v1.0</div>
  </div>
  <div style="position:absolute;bottom:0;left:0;display:flex;gap:44px;align-items:baseline;">
    <span class="num" style="font-size:15px;font-weight:700;">2026.07.03</span>
    <span class="cap" style="font-size:13px;">19 skills · 113 evals · CI green</span>
  </div>`, 1));

/* 2 目录 — 概念:超大序号做视觉主体,极端疏密 */
pages.push(P("目录 / CONTENTS", `
  <div class="h" style="font-size:40px;margin-bottom:12px;">三条主线</div>
  <div class="thin" style="font-size:15px;color:var(--g3);margin-bottom:44px;">从标准，到成果，到延续</div>
  ${[["01","标准","质量标准与两道可复现的 L1 校验门",1],
     ["02","成果","19 个 skill 达标背后的关键数字",0],
     ["03","延续","产品化安装链路与下一步视觉闭环",0]].map(([n,t,d,hot])=>`
  <div style="display:flex;align-items:center;padding:22px 0;border-top:1px solid var(--line);">
    <span class="num h" style="font-size:56px;width:150px;color:${hot?"var(--blue)":"var(--g4)"};">${n}</span>
    <span class="h" style="font-size:26px;width:240px;font-weight:700;">${t}</span>
    <span class="cap" style="font-size:15px;flex:1;">${d}</span>
    <span style="color:var(--g4);font-size:20px;">→</span>
  </div>`).join("")}`, 2));

/* 3 问题 — 深色蓄力页 + 巨型幽灵字,极端对比 */
pages.push(P("01 标准 / 问题", `
  <div class="ghost num" style="right:0;bottom:-60px;font-size:300px;color:#181b20;">?</div>
  <div class="tag" style="margin-bottom:30px;"></div>
  <div class="h" style="font-size:52px;">重构前：能用，</div>
  <div class="h" style="font-size:52px;color:var(--dg);">但松散、无法验证。</div>
  <div style="position:absolute;bottom:0;left:0;display:flex;gap:56px;width:100%;">
    ${[["17","/21","个 skill 无可判定验收标准"],
       ["6","处","CVE·年份·路径硬编码，会过期"],
       ["0","","自动化校验，全靠人肉 review"]].map(([n,u,c])=>`
    <div style="flex:1;border-top:2px solid #2A2E34;padding-top:18px;">
      <span class="num h" style="font-size:68px;">${n}</span><span class="num" style="font-size:26px;color:var(--dg);">${u}</span>
      <div style="font-size:13.5px;color:#9AA0A8;margin-top:10px;line-height:1.5;">${c}</div>
    </div>`).join("")}
  </div>`, 3, { dark: true }));

/* 4 框架 — bento 卡片网格,质感层 */
pages.push(P("01 标准 / 框架", `
  <div class="h" style="font-size:40px;margin-bottom:32px;">Skill Quality Standard <span class="num hl">v1.0</span></div>
  <div style="display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:16px;height:400px;">
    <div style="background:var(--ink);color:#fff;border-radius:6px;padding:32px;display:flex;flex-direction:column;justify-content:space-between;">
      <div class="num h" style="font-size:60px;">D0</div>
      <div><div style="font-size:20px;font-weight:700;margin-bottom:10px;">门槛 · 一票否决</div>
      <div style="font-size:13.5px;color:#A2A6AD;line-height:1.6;">frontmatter 规范 / 行数上限 / 孤儿文件 / 平台路径与 CVE 硬编码</div></div>
    </div>
    <div style="background:#fff;border:1px solid var(--line);border-radius:6px;padding:32px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 1px 3px rgba(0,0,0,.04);">
      <div class="num h hl" style="font-size:44px;">D1–D8</div>
      <div><div style="font-size:19px;font-weight:700;margin-bottom:10px;">评分 · 100 分</div>
      <div class="cap" style="font-size:13px;">触发/边界/主流程/结构/evals/治理，六维打分</div></div>
    </div>
    <div style="background:var(--mist);border-radius:6px;padding:32px;display:flex;flex-direction:column;justify-content:space-between;">
      <div class="num h" style="font-size:44px;">×3</div>
      <div><div style="font-size:19px;font-weight:700;margin-bottom:10px;">三件套 · 必备</div>
      <div class="cap" style="font-size:13px;">验收标准 · 不做什么 · 已知陷阱，缺一不可</div></div>
    </div>
  </div>`, 4));

/* 5 数据 — 前后对比叙事(B2):重构前 21 格(4 实心+17 空心) → 重构后 19 实心;指标下移(B4) */
const cell=(bg,bd)=>`<div style="width:38px;height:38px;background:${bg};border:${bd};border-radius:3px;"></div>`;
const rowBefore = Array.from({length:21},(_,i)=>i<4?cell("var(--g3)","none"):cell("transparent","1.5px solid var(--g4)")).join("");
const rowAfter  = Array.from({length:21},(_,i)=>i<19?cell("var(--blue)","none"):cell("transparent","1.5px solid var(--g4)")).join("");
pages.push(P("02 成果 / 数据", `
  <div class="h" style="font-size:40px;margin-bottom:6px;">达标：从 <span class="num" style="color:var(--g3);">4/21</span> 到 <span class="num hl">19/21</span></div>
  <div class="thin" style="font-size:14px;color:var(--g3);margin-bottom:4px;">同样 21 个槽位——灰=重构前已合格 4 个，蓝=本次新达标至 19 个，空=尚未覆盖的窄工具</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:34px;">
    <div>
      <div class="cap" style="font-size:12px;letter-spacing:.14em;margin-bottom:12px;">重构前 · 4 / 21</div>
      <div style="display:grid;grid-template-columns:repeat(21,38px);gap:10px;">${rowBefore}</div>
    </div>
    <div>
      <div style="font-size:12px;letter-spacing:.14em;margin-bottom:12px;color:var(--blue);font-weight:700;">重构后 · 19 / 21</div>
      <div style="display:grid;grid-template-columns:repeat(21,38px);gap:10px;">${rowAfter}</div>
    </div>
  </div>
  <div style="display:flex;gap:64px;margin-top:20px;">
    ${[["113","routing evals · 覆盖 14 个 skill",0],["100%","硬编码清零 · 平台路径 + 时效",0],["2","L1 gate · CI 每次 push 跑",1]].map(([n,c,hot])=>`
    <div style="flex:1;border-top:2px solid ${hot?"var(--blue)":"var(--ink)"};padding-top:16px;">
      <span class="num h" style="font-size:52px;color:${hot?"var(--blue)":"var(--ink)"};">${n}</span>
      <div class="cap" style="font-size:13.5px;margin-top:8px;">${c}</div></div>`).join("")}
  </div>`, 5));

/* 6 案例 — 三段流程,箭头连接,破格:动作段加深 */
pages.push(P("02 成果 / 案例", `
  <div class="h" style="font-size:40px;margin-bottom:14px;">两个 PPT skill，合并成一条生产线</div>
  <div class="thin" style="font-size:15px;color:var(--g3);margin-bottom:50px;">notion-infographic + ppt-designer → <span class="num" style="color:var(--ink);font-weight:700;">deck-studio</span></div>
  <div style="display:flex;align-items:stretch;gap:0;height:280px;">
    ${[["背景","地盘重叠，互相误触发。用户不知该用哪个","light"],
       ["动作","合并为四层架构，v2 资产无损迁移","dark"],
       ["结果","13 风格库 · 三条铁律 · 10 条 evals","blue"]].map(([t,d,kind],i)=>{
      const bg=kind==="dark"?"background:var(--ink);color:#fff;":kind==="blue"?"background:var(--blue);color:#fff;":"background:var(--mist);";
      const cc=kind==="light"?"var(--g2)":"rgba(255,255,255,.75)";
      return `${i?`<div style="width:52px;display:flex;align-items:center;justify-content:center;color:var(--g4);font-size:26px;">→</div>`:""}
      <div style="flex:1;${bg}border-radius:6px;padding:34px;display:flex;flex-direction:column;justify-content:space-between;">
        <span class="num" style="font-size:15px;opacity:.7;">0${i+1}</span>
        <div><div style="font-size:22px;font-weight:800;margin-bottom:12px;">${t}</div>
        <div style="font-size:14px;line-height:1.6;color:${cc};">${d}</div></div>
      </div>`;}).join("")}
  </div>`, 6));

/* 7 对比 — 真表格,强调收敛 */
pages.push(P("02 成果 / 对比", `
  <div class="h" style="font-size:40px;margin-bottom:44px;">校验，从人肉变自动</div>
  <table style="width:100%;border-collapse:collapse;">
    <tr>
      <th style="text-align:left;width:190px;font-size:12px;letter-spacing:.1em;color:var(--g3);font-weight:600;padding-bottom:14px;border-bottom:2px solid var(--ink);"></th>
      <th style="text-align:left;font-size:13px;color:var(--g3);font-weight:500;padding-bottom:14px;border-bottom:2px solid var(--ink);">重构前</th>
      <th style="text-align:left;font-size:13px;color:var(--blue);font-weight:700;padding-bottom:14px;border-bottom:2px solid var(--ink);">重构后</th>
    </tr>
    ${[["验收标准","多为空缺，无法判定「做完了吗」","19/19 可判定，写进每个 SKILL.md"],
       ["时效硬编码","CVE / 年份散落多处","清零，改为实时搜索指令"],
       ["校验方式","手动 review，无回归","CI + 两道 L1 gate，push 即跑"]].map(r=>`
    <tr><td style="font-size:16px;font-weight:700;padding:22px 0;border-bottom:1px solid var(--line);">${r[0]}</td>
        <td style="font-size:15px;color:var(--g3);padding:22px 24px 22px 0;border-bottom:1px solid var(--line);">${r[1]}</td>
        <td style="font-size:15px;padding:22px 0;border-bottom:1px solid var(--line);">${CK}${r[2]}</td></tr>`).join("")}
  </table>`, 7));

/* 8 行动 — 深色页,呼应第3页,节奏收束 */
pages.push(P("03 延续 / 行动", `
  <div class="tag" style="margin-bottom:30px;"></div>
  <div class="h" style="font-size:46px;margin-bottom:6px;">下一步：从</div>
  <div class="h" style="font-size:46px;"><span class="thin" style="color:var(--dg);">「路由更准」</span> 到 <span class="hl">「产出更强」</span></div>
  <div style="position:absolute;bottom:0;left:0;width:100%;">
    ${[["01","task-level evals","评产出质量而非路由命中，对比 baseline"],
       ["02","视觉闭环","风格库 24+，HTML 渲染，render→自检→修"],
       ["03","对标验证","同 brief 与竞品盲评，用数据说「超过」"]].map(([n,t,d])=>`
    <div style="display:flex;align-items:baseline;padding:20px 0;border-top:1px solid #2A2E34;">
      <span class="num hl" style="width:70px;font-size:18px;font-weight:700;">${n}</span>
      <span style="width:320px;font-size:21px;font-weight:700;">${t}</span>
      <span style="flex:1;font-size:14px;color:#9AA0A8;">${d}</span></div>`).join("")}
  </div>`, 8, { dark: true }));

/* 9 封底 — 极简爆发,一句话+命令 */
pages.push(P("GEEK SKILLS", `
  <div class="ghost num" style="left:-20px;bottom:-80px;font-size:340px;color:var(--mist);">/</div>
  <div style="position:absolute;top:130px;left:0;">
    <div class="tag" style="margin-bottom:34px;"></div>
    <div class="h" style="font-size:64px;">可安装、可维护、</div>
    <div class="h" style="font-size:64px;"><span class="hl">可升级</span>。</div>
    <div style="margin-top:48px;display:inline-flex;align-items:center;background:var(--ink);color:#E8EAED;
      padding:18px 26px;border-radius:5px;font-family:Menlo,monospace;font-size:15px;">
      <span style="color:#5A6069;margin-right:12px;">$</span>python3 scripts/install_skill.py deck-studio</div>
    <div class="cap" style="margin-top:22px;font-size:14px;">github.com/staruhub/ClaudeSkills</div>
  </div>`, 9));

fs.mkdirSync("html", { recursive: true });
pages.forEach((h, i) => fs.writeFileSync(`html/p${i + 1}.html`, h));
console.log(pages.length + " 页 v3 HTML 生成");
