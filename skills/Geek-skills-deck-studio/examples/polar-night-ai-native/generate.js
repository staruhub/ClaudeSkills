// deck-studio 实战:AI Native 主题 · 极夜科技风格
// 教训应用:重锚点(粗黑标题+数据英雄)保留,细体只做对比;母题=节点网格+发光青线(每页≤2处光效)
const fs = require("fs");

const T = {
  bg:"#0A0E1A", card:"#141B2E", card2:"#1C2333", line:"#232B42", line2:"#2E3852",
  txt:"#E6EDF3", dim:"#8B94A7", faint:"#525B70",
  cyan:"#00D4FF", violet:"#7B61FF",
  sans:'"PingFang SC","Hiragino Sans GB",sans-serif',
  mono:'"SF Mono","DIN Alternate",monospace',
};

const CSS = `
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}
html,body{width:1280px;height:720px;overflow:hidden;}
body{background:${T.bg};color:${T.txt};font-family:${T.sans};position:relative;
  background-image:linear-gradient(${T.card}55 1px,transparent 1px),linear-gradient(90deg,${T.card}55 1px,transparent 1px);
  background-size:48px 48px;}
.mono{font-family:${T.mono};font-feature-settings:"tnum";}
.top{position:absolute;left:88px;right:88px;top:50px;display:flex;justify-content:space-between;align-items:center;z-index:5;}
.kick{font-size:11px;letter-spacing:.34em;color:${T.dim};font-weight:600;text-transform:uppercase;display:flex;align-items:center;gap:12px;}
.kick::before{content:"";width:7px;height:7px;background:${T.cyan};display:inline-block;box-shadow:0 0 10px ${T.cyan};}
.brand{font-size:10.5px;letter-spacing:.3em;color:${T.faint};}
.foot{position:absolute;left:88px;right:88px;bottom:42px;display:flex;justify-content:space-between;align-items:center;z-index:5;}
.src{font-size:10px;letter-spacing:.14em;color:${T.faint};text-transform:uppercase;}
.pg{font-size:11px;color:${T.dim};letter-spacing:.14em;}
.stage{position:absolute;left:88px;right:88px;top:118px;bottom:100px;z-index:2;display:flex;flex-direction:column;}
/* 重锚点字阶(v4教训:标题回归 800,细体只做对比层) */
.h{font-weight:800;letter-spacing:.005em;line-height:1.22;}
.thin{font-weight:200;}
.lead{font-weight:300;color:${T.dim};line-height:1.7;}
.body{font-weight:400;color:#B8C0D0;line-height:1.62;}
.cy{color:${T.cyan};} .vi{color:${T.violet};}
.mark{width:44px;height:4px;background:${T.cyan};box-shadow:0 0 14px ${T.cyan}88;}
.hair{height:1px;background:${T.line};}
.card{background:${T.card};border:1px solid ${T.line};}
.ghost{position:absolute;font-family:${T.mono};font-weight:800;color:#10162A;z-index:0;line-height:.8;letter-spacing:-.04em;}
`;

function P(section, inner, no, opt={}) {
  return `<!doctype html><meta charset="utf-8"><style>${CSS}</style><body>
<div class="top"><span class="kick">${section}</span><span class="brand">AI NATIVE · GEEK SKILLS</span></div>
${opt.ghost||""}
<div class="stage">${inner}</div>
<div class="foot"><span class="src">keqian-method × xuefeng-method</span><span class="pg mono">${String(no).padStart(2,"0")} — 09</span></div>
</body>`;
}
const pages = [];

/* 1 封面:粗黑大标题(锚点回归)+ 节点网络母题 */
pages.push(P("AI Native · Cover", `
  <!-- 大尺度几何母题:同心环 + 主节点,与 p7 的巨型水印同语言 -->
  <svg style="position:absolute;right:-140px;top:30px;width:640px;height:640px;z-index:0;" viewBox="0 0 640 640">
    <circle cx="320" cy="320" r="290" fill="none" stroke="${T.line}" stroke-width="1.5"/>
    <circle cx="320" cy="320" r="210" fill="none" stroke="${T.line2}" stroke-width="1.5"/>
    <circle cx="320" cy="320" r="130" fill="none" stroke="${T.line2}" stroke-width="2"/>
    <line x1="320" y1="30" x2="320" y2="610" stroke="${T.line}" stroke-width="1"/>
    <line x1="30" y1="320" x2="610" y2="320" stroke="${T.line}" stroke-width="1"/>
    <circle cx="320" cy="190" r="10" fill="${T.cyan}" style="filter:drop-shadow(0 0 14px ${T.cyan})"/>
    <circle cx="450" cy="320" r="6" fill="${T.violet}"/>
    <circle cx="320" cy="450" r="6" fill="${T.line2}"/>
    <rect x="312" y="312" width="16" height="16" fill="${T.txt}"/>
  </svg>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;max-width:860px;">
    <div class="mark" style="margin-bottom:38px;"></div>
    <div class="h" style="font-size:76px;">AI Native：</div>
    <div class="h" style="font-size:76px;">当核心决策<span class="cy">交给模型</span></div>
    <div class="lead" style="margin-top:34px;font-size:17px;">两条经过实战的方法论路线 · 克谦式 × 雪峰式</div>
  </div>
  <div class="hair" style="margin-bottom:18px;"></div>
  <div style="display:flex;gap:48px;align-items:baseline;">
    <span class="mono" style="font-size:14px;font-weight:600;color:${T.txt};">2026.07</span>
    <span class="lead" style="font-size:12px;letter-spacing:.08em;">GEEK SKILLS 方法论分享</span>
  </div>`, 1));

/* 2 目录 */
pages.push(P("目录 · Agenda", `
  <div class="h" style="font-size:42px;margin-bottom:10px;">三个问题</div>
  <div class="lead" style="font-size:15px;">判断 → 方法 → 选择</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
  ${[["01","是什么","AI Native 与 +AI 的分界线在哪",1],
     ["02","怎么做","封闭走克谦式，开放走雪峰式",0],
     ["03","怎么选","第零步判型,选错方法比没有方法更危险",0]].map(([n,t,d,hot])=>`
    <div class="hair"></div>
    <div style="display:flex;align-items:center;padding:27px 4px;">
      <span class="mono" style="font-size:48px;font-weight:200;width:140px;color:${hot?T.cyan:T.faint};">${n}</span>
      <span class="h" style="font-size:25px;width:250px;font-weight:700;">${t}</span>
      <span class="lead" style="font-size:14.5px;flex:1;">${d}</span>
    </div>`).join("")}
  <div class="hair"></div>
  </div>`, 2));

/* 3 问题:分界线(左右分屏对比,重锚点) */
pages.push(P("01 是什么 · 分界", `
  <div class="h" style="font-size:44px;">分界线只有一条：<span class="cy">用户行为能否穷举</span></div>
  <div style="flex:1;display:flex;gap:1px;background:${T.line};margin-top:36px;">
    <!-- 三段网格(消灭空腹):① 标题头 ② 图形居中占中段固定高 ③ 正文贴中段 + 结论行 -->
    <div style="flex:1;background:${T.card};border-top:2px solid ${T.faint};padding:36px 40px;display:flex;flex-direction:column;">
      <div style="margin-bottom:8px;"><span class="mono" style="font-size:13px;letter-spacing:.2em;color:${T.dim};">TYPE A</span>
        <div class="h" style="font-size:29px;margin-top:12px;">＋AI<span class="thin" style="color:${T.dim};font-size:21px;">（场景依赖型）</span></div></div>
      <div style="flex:1;display:flex;align-items:center;justify-content:center;">
        <div style="display:grid;grid-template-columns:repeat(8,26px);gap:9px;">
          ${Array.from({length:24},()=>`<div style="width:26px;height:26px;background:${T.line2};"></div>`).join("")}
        </div>
      </div>
      <div class="body" style="font-size:14.5px;margin-bottom:16px;">行为可枚举——有限的格栅。AI 辅助执行<span style="color:${T.txt};font-weight:600;">确定性流程</span>：记账、OCR 归档、CRUD 后台。</div>
      <div class="mono" style="font-size:13px;color:${T.dim};border-top:1px solid ${T.line};padding-top:16px;">→ 克谦式：单 Agent · SDD · 质量门禁</div>
    </div>
    <div style="flex:1;background:${T.card2};border-top:2px solid ${T.cyan};padding:36px 40px;display:flex;flex-direction:column;">
      <div style="margin-bottom:8px;"><span class="mono" style="font-size:13px;letter-spacing:.2em;color:${T.cyan};">TYPE B</span>
        <div class="h" style="font-size:29px;margin-top:12px;">AI Native<span class="thin" style="color:${T.dim};font-size:21px;">（强模型依赖型）</span></div></div>
      <div style="flex:1;display:flex;align-items:center;justify-content:center;">
        <svg width="280" height="130" viewBox="0 0 280 130">
          <circle cx="40" cy="65" r="9" fill="${T.cyan}" style="filter:drop-shadow(0 0 10px ${T.cyan})"/>
          ${[[120,18],[160,50],[135,92],[200,30],[230,72],[195,112],[260,16],[268,58],[250,104]].map(([x,y])=>
            `<line x1="40" y1="65" x2="${x}" y2="${y}" stroke="${T.line2}" stroke-width="1"/><circle cx="${x}" cy="${y}" r="4" fill="${T.line2}"/>`).join("")}
        </svg>
      </div>
      <div class="body" style="font-size:14.5px;margin-bottom:16px;">行为开放——发散的节点。AI 驱动<span class="cy" style="font-weight:600;">核心决策</span>：AI 日历、对话助手、智能推荐。</div>
      <div class="mono" style="font-size:13px;color:${T.cyan};border-top:1px solid ${T.line2};padding-top:16px;">→ 雪峰式：多专精 Agent · 快速校准 · 行为审计</div>
    </div>
  </div>`, 3));

/* 4 第零步判型表 */
pages.push(P("01 是什么 · 判型", `
  <div class="h" style="font-size:42px;">第零步：先判型，再选法</div>
  <div class="lead" style="font-size:15px;margin-top:10px;">选错方法论，比没有方法论更危险</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
    <table style="width:100%;border-collapse:collapse;">
      <tr>${["产品类型","关键判断","推荐方法"].map((h,i)=>`<th style="text-align:left;font-size:12px;letter-spacing:.16em;color:${i===2?T.cyan:T.dim};font-weight:600;text-transform:uppercase;padding-bottom:16px;border-bottom:1px solid ${T.line2};">${h}</th>`).join("")}</tr>
      ${[["＋AI 场景依赖","能列出所有合法输入输出组合","克谦式（单 Agent + SDD）",0],
         ["AI Native 强模型依赖","用户的下一步操作无法预测","雪峰式（多专精 Agent）",1],
         ["混合型","核心流程确定，部分环节开放","两者结合，按模块选用",0]].map(([a,b,c,hot])=>`
      <tr><td class="h" style="font-size:19px;font-weight:700;padding:24px 24px 24px 0;border-bottom:1px solid ${T.line};">${a}</td>
          <td class="body" style="font-size:15px;padding:24px 24px 24px 0;border-bottom:1px solid ${T.line};">${b}</td>
          <td class="body" style="font-size:15px;padding:24px 0;border-bottom:1px solid ${T.line};${hot?`color:${T.cyan};font-weight:600;`:""}">${c}</td></tr>`).join("")}
    </table>
  </div>`, 4));

/* 5 两条路线对比(双卡,重锚点) */
pages.push(P("02 怎么做 · 路线", `
  <div class="h" style="font-size:42px;">两条路线，各管一半世界</div>
  <div style="flex:1;display:flex;gap:24px;margin-top:34px;">
    ${[["克谦式","确定性交付","单 Agent 极致论","文档驱动开发 SDD","质量门禁闭环","概率乘：环节越少越可靠",T.violet,"KEQIAN"],
       ["雪峰式","开放性生存","多养专精虾：每只只干一种活","唯快不破：快速上线快速校准","行为审计替代质量门禁","穷举是死循环",T.cyan,"XUEFENG"]].map(([name,tag,p1,p2,p3,p4,color,en])=>`
    <div class="card" style="flex:1;padding:36px;display:flex;flex-direction:column;border-top:2px solid ${color};">
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;">
        <span class="h" style="font-size:28px;">${name}</span>
        <span class="mono" style="font-size:11px;letter-spacing:.2em;color:${T.faint};">${en}</span></div>
      <div class="mono" style="font-size:13px;color:${color};margin-bottom:24px;">${tag}</div>
      ${[p1,p2,p3,p4].map((p,pi)=>`<div style="display:flex;gap:14px;padding:12px 0;border-top:1px solid ${T.line};align-items:baseline;">
        <span class="mono" style="color:${color};font-weight:600;font-size:13px;min-width:24px;">0${pi+1}</span><span class="body" style="font-size:14.5px;">${p}</span></div>`).join("")}
    </div>`).join("")}
  </div>`, 5));

/* 6 雪峰三原则(三卡片,一个点亮) */
pages.push(P("02 怎么做 · 心法", `
  <div class="h" style="font-size:42px;">开放世界的三条生存法则</div>
  <div class="lead" style="font-size:15px;margin-top:10px;">来自雪峰式方法论 · AI 日历等产品的实战沉淀</div>
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;margin-top:32px;">
    ${[["穷举是死循环","试图列出所有用户行为,是在和无限对赌。接受不可穷举,设计兜底。",0],
       ["多养专精虾","每只虾只干一种活:路由、执行、校验、表达分开,出错能定位,升级不牵连。",1],
       ["唯快不破","校准到 95% 再上线 = 永远不上线。快速上线,用行为审计追漂移,边跑边修。",0]].map(([t,d,hot],i)=>`
    <div class="card" style="padding:34px;display:flex;flex-direction:column;${hot?`border-color:${T.cyan};box-shadow:0 0 24px ${T.cyan}22;`:""}">
      <span class="mono" style="font-size:40px;font-weight:200;color:${hot?T.cyan:T.faint};">0${i+1}</span>
      <div class="h" style="font-size:22px;margin:18px 0 14px;">${t}</div>
      <div class="body" style="font-size:14px;flex:1;">${d}</div>
    </div>`).join("")}
  </div>`, 6));

/* 7 数据页:概率乘(数据英雄,占屏大) */
pages.push(P("02 怎么做 · 铁律", `
  <div class="ghost mono" style="right:-20px;bottom:-50px;font-size:280px;">×</div>
  <div class="h" style="font-size:42px;">克谦铁律：概率乘</div>
  <div style="flex:1;display:flex;align-items:center;gap:56px;">
    <div>
      <div style="display:flex;align-items:baseline;">
        <span class="mono" style="font-size:120px;font-weight:800;line-height:.9;">0.99</span
        ><span class="mono" style="font-size:48px;font-weight:300;color:${T.dim};position:relative;top:-44px;margin-left:4px;">51</span>
        <span class="mono" style="font-size:56px;font-weight:200;color:${T.dim};margin:0 24px;">=</span>
        <span class="mono" style="font-size:120px;font-weight:800;line-height:.9;color:${T.cyan};text-shadow:0 0 30px ${T.cyan}55;">0.59</span>
      </div>
      <div class="lead" style="font-size:16px;margin-top:30px;max-width:900px;line-height:1.85;">
        每个环节 99% 可靠，51 个环节相乘后只剩 59 分——不及格。<br>
        <span style="color:${T.txt};font-weight:600;">所以：链条越短越好，每个环节都要过门禁，能用确定性代码就不用模型。</span></div>
    </div>
  </div>
  <div style="display:flex;gap:64px;">
    ${[["≤5","关键链路环节数目标"],["100%","每环节过质量门禁"],["0","能写 if 就不调模型的例外"]].map(([n,c])=>`
    <div style="flex:1;"><div class="hair" style="margin-bottom:14px;"></div>
      <span class="mono h" style="font-size:40px;">${n}</span>
      <div class="body" style="font-size:13px;margin-top:6px;color:${T.dim};">${c}</div></div>`).join("")}
  </div>`, 7));

/* 8 行动三步 */
pages.push(P("03 怎么选 · 行动", `
  <div class="h" style="font-size:42px;">落地三步</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
  ${[["判型","用第零步表格给产品定性:＋AI / AI Native / 混合","本周就能做"],
     ["选法","封闭模块走克谦式流水线,开放模块交给雪峰式专精 Agent","架构评审一次定"],
     ["上线校准","AI Native 部分不等 95%,上线 + 行为审计 + 快速迭代","每周一个校准循环"]].map(([t,d,tag],i)=>`
    <div class="hair"></div>
    <div style="display:flex;align-items:center;padding:24px 4px;">
      <span class="mono" style="width:110px;font-size:17px;font-weight:600;color:${T.cyan};">STEP ${i+1}</span>
      <span class="h" style="width:200px;font-size:22px;font-weight:700;">${t}</span>
      <span class="body" style="flex:1;font-size:14.5px;">${d}</span>
      <span class="mono" style="font-size:12px;color:${T.faint};">${tag}</span></div>`).join("")}
  <div class="hair"></div>
  </div>`, 8));

/* 9 封底 */
pages.push(P("AI Native", `
  <div class="ghost mono" style="left:-20px;bottom:-80px;font-size:330px;">→</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
    <div class="mark" style="margin-bottom:36px;"></div>
    <div class="h" style="font-size:64px;">穷举是死循环，</div>
    <div class="h" style="font-size:64px;"><span class="cy">唯快不破</span>。</div>
    <div class="lead" style="font-size:16px;margin-top:36px;">完整方法论:keqian-method · xuefeng-method<br>
    <span class="mono" style="font-size:13px;">github.com/staruhub/ClaudeSkills</span></div>
  </div>`, 9));

fs.mkdirSync("html",{recursive:true});
pages.forEach((h,i)=>fs.writeFileSync(`html/p${i+1}.html`,h));
console.log(pages.length+" 页 AI Native deck 生成");
