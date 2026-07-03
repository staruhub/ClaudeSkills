// deck-studio 第三风格实战:英黄工作室 · ChaoGeek AI 训练营提案
// 教训全带:重锚点+细体共存 / 内容即视觉 / 内部网格 / 全角标点 / 暖黄单点题母题
const fs = require("fs");

const T = {
  ink:"#0D0D0D", ink2:"#161616", card:"#1A1A1A",
  paper:"#F5F0E6", gold:"#E8B004", goldD:"#B8890A",
  txt:"#F5F0E6", dim:"#8F8A7E", faint:"#4A4740", line:"#2E2C28", lineL:"#DDD5C4",
  sans:'"PingFang SC","Hiragino Sans GB",sans-serif',
  mono:'"SF Mono","DIN Alternate",monospace',
};

const CSS = `
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}
html,body{width:1280px;height:720px;overflow:hidden;}
body{background:${T.ink};color:${T.txt};font-family:${T.sans};position:relative;}
.mono{font-family:${T.mono};font-feature-settings:"tnum";}
.top{position:absolute;left:88px;right:88px;top:50px;display:flex;justify-content:space-between;align-items:center;z-index:5;}
.kick{font-size:11px;letter-spacing:.34em;color:${T.dim};font-weight:600;text-transform:uppercase;display:flex;align-items:center;gap:12px;}
.kick::before{content:"";width:7px;height:7px;background:${T.gold};display:inline-block;}
.brand{font-size:10.5px;letter-spacing:.3em;color:${T.faint};}
.foot{position:absolute;left:88px;right:88px;bottom:42px;display:flex;justify-content:space-between;align-items:center;z-index:5;}
.src{font-size:10px;letter-spacing:.14em;color:${T.faint};text-transform:uppercase;}
.pg{font-size:11px;color:${T.dim};letter-spacing:.14em;}
.stage{position:absolute;left:88px;right:88px;top:118px;bottom:100px;z-index:2;display:flex;flex-direction:column;}
/* 重锚点 + 细体共存 */
.h{font-weight:800;letter-spacing:.01em;line-height:1.24;}
.thin{font-weight:200;}
.lead{font-weight:300;color:${T.dim};line-height:1.75;}
.body{font-weight:400;color:#CFC9BB;line-height:1.65;}
.au{color:${T.gold};}
.mark{width:44px;height:4px;background:${T.gold};}
.hair{height:1px;background:${T.line};}
/* 米白亮页 */
.light-bg{background:${T.paper};color:${T.ink};}
.light-bg .kick{color:#9A917D;} .light-bg .kick::before{background:${T.goldD};}
.light-bg .brand{color:#C9C0AC;} .light-bg .src{color:#C9C0AC;} .light-bg .pg{color:#9A917D;}
.light-bg .lead{color:#7A7361;} .light-bg .body{color:#3A362E;}
.light-bg .hair{background:${T.lineL};} .light-bg .au{color:${T.goldD};}
.ghost{position:absolute;font-family:${T.mono};font-weight:800;color:#171612;z-index:0;line-height:.8;letter-spacing:-.04em;}
.light-bg .ghost{color:#EAE3D2;}
`;

function P(section, inner, no, opt={}) {
  return `<!doctype html><meta charset="utf-8"><style>${CSS}</style><body class="${opt.light?"light-bg":""}">
<div class="top"><span class="kick">${section}</span><span class="brand">CHAOGEEK · PROPOSAL</span></div>
${opt.ghost||""}
<div class="stage">${inner}</div>
<div class="foot"><span class="src">ChaoGeek AI 实战训练营 · 合作提案</span><span class="pg mono">${String(no).padStart(2,"0")} — 09</span></div>
</body>`;
}
const pages = [];

/* 1 封面:宣言式短句 + 暖黄大圆单点视觉(风格:少图,大面积暗底+点题视觉) */
pages.push(P("提案 · Cover", `
  <svg style="position:absolute;right:-120px;top:-40px;width:560px;height:560px;z-index:0;" viewBox="0 0 560 560">
    <circle cx="300" cy="260" r="215" fill="${T.gold}"/>
    <circle cx="300" cy="260" r="215" fill="none" stroke="${T.ink}" stroke-width="0"/>
    <circle cx="140" cy="420" r="10" fill="${T.paper}"/>
    <line x1="60" y1="500" x2="530" y2="30" stroke="${T.ink}" stroke-width="3"/>
  </svg>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;max-width:760px;">
    <div class="mark" style="margin-bottom:38px;"></div>
    <div class="h" style="font-size:70px;">把 AI 玩明白的人，</div>
    <div class="h" style="font-size:70px;">正在<span class="au">悄悄拉开差距</span>。</div>
    <div class="lead" style="margin-top:34px;font-size:17px;">ChaoGeek AI 实战训练营 · 合作提案</div>
  </div>
  <div class="hair" style="margin-bottom:18px;"></div>
  <div style="display:flex;gap:48px;align-items:baseline;">
    <span class="mono" style="font-size:14px;font-weight:600;">2026.07</span>
    <span class="lead" style="font-size:12px;letter-spacing:.08em;">超极客 · 让每个人都能用上 AI 的生产力</span>
  </div>`, 1));

/* 2 目录 */
pages.push(P("目录 · Agenda", `
  <div class="h" style="font-size:42px;margin-bottom:10px;">三件事</div>
  <div class="lead" style="font-size:15px;">为什么做 · 怎么做 · 怎么合作</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
  ${[["01","为什么","工具在爆炸，能力没跟上——差距在方法不在工具",1],
     ["02","怎么做","三阶段实战路径 + 一套真实资产库",0],
     ["03","怎么合作","六周一期，三种合作方式",0]].map(([n,t,d,hot])=>`
    <div class="hair"></div>
    <div style="display:flex;align-items:center;padding:27px 4px;">
      <span class="mono" style="font-size:48px;font-weight:200;width:140px;color:${hot?T.gold:T.faint};">${n}</span>
      <span class="h" style="font-size:25px;width:250px;font-weight:700;">${t}</span>
      <span class="lead" style="font-size:14.5px;flex:1;">${d}</span>
    </div>`).join("")}
  <div class="hair"></div>
  </div>`, 2));

/* 3 痛点(内容即视觉:工具爆炸曲线 vs 能力平线) */
pages.push(P("01 为什么 · 痛点", `
  <div class="h" style="font-size:44px;">工具在爆炸，<span class="thin" style="color:${T.dim};">能力没跟上。</span></div>
  <div style="flex:1;display:flex;align-items:center;gap:60px;">
    <svg width="640" height="300" viewBox="0 0 640 300">
      <line x1="40" y1="260" x2="600" y2="260" stroke="${T.line}" stroke-width="1"/>
      <line x1="40" y1="260" x2="40" y2="30" stroke="${T.line}" stroke-width="1"/>
      <path d="M 40 250 Q 300 240 430 160 T 600 40" fill="none" stroke="${T.gold}" stroke-width="4"/>
      <path d="M 40 252 L 600 228" fill="none" stroke="${T.dim}" stroke-width="2.5" stroke-dasharray="7 7"/>
      <text x="440" y="80" font-size="15" fill="${T.gold}" font-weight="600">AI 工具数量</text>
      <text x="440" y="215" font-size="15" fill="${T.dim}">普通人的驾驭能力</text>
      <circle cx="600" cy="40" r="6" fill="${T.gold}"/>
      <circle cx="600" cy="228" r="5" fill="${T.dim}"/>
    </svg>
    <div style="flex:1;">
      <div class="hair" style="margin-bottom:20px;"></div>
      <div class="body" style="font-size:16px;line-height:1.9;">
        订阅了一堆工具，收藏了一堆教程，<br>真正改变工作方式的人<span class="au" style="font-weight:700;">寥寥无几</span>。<br><br>
        <span style="color:${T.txt};font-weight:600;">差距不在工具，在方法——<br>在有没有人带着把 AI 真正用进生产。</span></div>
    </div>
  </div>`, 3));

/* 4 方案:三阶段(米白亮页,节奏切换) */
pages.push(P("02 怎么做 · 路径", `
  <div class="h" style="font-size:42px;">三阶段实战路径</div>
  <div class="lead" style="font-size:15px;margin-top:10px;">不讲原理课——每一阶段交付你自己的真实产出</div>
  <div style="flex:1;display:flex;gap:20px;margin-top:32px;">
    ${[["壹","上手","从对话到工作流：把日常任务改造成 AI 流水线",["提示词到流水线的改造方法","文档 / 数据 / 内容三类高频场景","效率基线测量：改造前 vs 改造后"],"写出你的第一个可复用工作流",0],
       ["贰","进阶","Agent 与 Skill：让 AI 记住你的方法论",["把重复判断沉淀为 skill","触发边界与验收标准怎么写","用评测防止 skill 退化"],"沉淀 3 个属于你的专属 skill",1],
       ["叁","实战","真实项目交付：从需求到成品全程 AI 协作",["用自己的真实需求立项","多 skill 协作的完整交付","作品路演与同行互评"],"带走一个完整的 AI 交付项目",0]].map(([num,t,d,items,out,hot])=>`
    <div style="flex:1;background:${hot?T.ink:"#EDE6D6"};${hot?"":`border:1px solid ${T.lineL};`}padding:30px 32px;display:flex;flex-direction:column;">
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:14px;">
        <span class="h" style="font-size:40px;color:${hot?T.gold:T.goldD};font-weight:800;">${num}</span>
        <span class="mono" style="font-size:11px;letter-spacing:.2em;color:${hot?T.dim:"#9A917D"};">PHASE</span></div>
      <div class="h" style="font-size:23px;font-weight:700;color:${hot?T.txt:T.ink};margin-bottom:10px;">${t}</div>
      <div style="font-size:13px;line-height:1.6;color:${hot?"#CFC9BB":"#5A5546"};margin-bottom:18px;">${d}</div>
      <div style="flex:1;border-top:1px solid ${hot?T.line:T.lineL};padding-top:16px;">
        ${items.map(it=>`<div style="display:flex;gap:10px;padding:7px 0;font-size:12.5px;line-height:1.5;color:${hot?"#A8A296":"#6A6455"};">
          <span style="color:${hot?T.gold:T.goldD};">·</span><span>${it}</span></div>`).join("")}
      </div>
      <div style="border-top:1px solid ${hot?T.line:T.lineL};padding-top:14px;font-size:12.5px;color:${hot?T.gold:T.goldD};font-weight:600;">✓ ${out}</div>
    </div>`).join("")}
  </div>`, 4, { light:true }));

/* 5 差异化 */
pages.push(P("02 怎么做 · 差异", `
  <div class="ghost mono" style="right:-16px;bottom:-60px;font-size:300px;">≠</div>
  <div class="h" style="font-size:44px;">不是又一门<span class="thin" style="color:${T.dim};">「AI 通识课」</span></div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
    <table style="width:100%;border-collapse:collapse;">
      <tr><th style="width:190px;border-bottom:1px solid ${T.txt};"></th>
        <th style="text-align:left;font-size:11px;letter-spacing:.16em;color:${T.dim};font-weight:600;text-transform:uppercase;padding-bottom:15px;border-bottom:1px solid ${T.txt};">通识课</th>
        <th style="text-align:left;font-size:11px;letter-spacing:.16em;color:${T.gold};font-weight:600;text-transform:uppercase;padding-bottom:15px;border-bottom:1px solid ${T.txt};">ChaoGeek 训练营</th></tr>
      ${[["教什么","工具功能演示","把你的真实工作改造成 AI 工作流"],
         ["用什么练","课堂示例","学员自己的项目 + 开源实战资产库"],
         ["带走什么","一堆笔记","可复用的 skill、工作流与交付成品"]].map(r=>`
      <tr><td class="h" style="font-size:17px;font-weight:700;padding:24px 0;border-bottom:1px solid ${T.line};">${r[0]}</td>
          <td class="lead" style="font-size:15px;padding:24px 24px 24px 0;border-bottom:1px solid ${T.line};">${r[1]}</td>
          <td class="body" style="font-size:15px;padding:24px 0;border-bottom:1px solid ${T.line};"><span class="au" style="margin-right:10px;font-weight:700;">—</span>${r[2]}</td></tr>`).join("")}
    </table>
  </div>`, 5));

/* 6 证据:真实教学资产(仓库真实数字) */
pages.push(P("02 怎么做 · 资产", `
  <div class="h" style="font-size:42px;">教学资产是<span class="au">真的</span>：一座开源实战库</div>
  <div class="lead" style="font-size:14.5px;margin-top:10px;">github.com/staruhub/ClaudeSkills · 全部可安装、可验证、有评测</div>
  <div style="flex:1;display:flex;align-items:center;gap:56px;">
    ${[["19","个实战 skill","深度研究 / PPT 生产 / 产品方法论 / 安全审计……",1],
       ["113","条评测用例","每个 skill 何时该用、何时不该用，有回归测试",0],
       ["2","道质量门禁","CI 每次提交自动校验,不是随缘维护",0]].map(([n,t,d,hot])=>`
    <div style="flex:1;">
      <div style="height:3px;background:${hot?T.gold:T.line};margin-bottom:24px;"></div>
      <span class="mono" style="font-size:96px;font-weight:800;line-height:.9;${hot?`color:${T.gold};`:""}">${n}</span>
      <div class="h" style="font-size:19px;margin-top:14px;font-weight:700;">${t}</div>
      <div class="lead" style="font-size:13px;margin-top:10px;">${d}</div>
    </div>`).join("")}
  </div>`, 6));

/* 7 六周安排(横向时间线) */
pages.push(P("03 怎么合作 · 节奏", `
  <div class="h" style="font-size:42px;">六周一期，每周一个里程碑</div>
  <div class="lead" style="font-size:15px;margin-top:10px;">每周都有可检验的交付物——没有产出的那一周不该存在</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
    <div style="position:relative;">
      <div style="position:absolute;left:8px;right:8px;top:7px;height:2px;background:${T.gold};"></div>
      <div style="display:flex;justify-content:space-between;">
        ${[["W1","开营诊断","盘点每个人的 AI 现状与目标","现状诊断卡"],
           ["W2","工作流","第一条流水线跑通","可复用工作流 ×1"],
           ["W3","Skill 化","方法论沉淀为 skill","专属 skill ×3"],
           ["W4","项目启动","用真实需求立项","项目立项书"],
           ["W5","交付冲刺","AI 协作产出成品","项目成品"],
           ["W6","路演结营","作品互评与后续路径","路演 + 互评报告"]].map(([w,t,d,out])=>`
        <div style="width:15.2%;">
          <div style="width:16px;height:16px;background:${T.gold};margin-bottom:22px;"></div>
          <div class="mono" style="font-size:14px;color:${T.gold};font-weight:700;margin-bottom:12px;">${w}</div>
          <div class="h" style="font-size:17px;font-weight:700;margin-bottom:8px;">${t}</div>
          <div class="body" style="font-size:13px;min-height:64px;">${d}</div>
          <div style="border-top:1px solid ${T.line};padding-top:12px;">
            <div class="mono" style="font-size:10px;letter-spacing:.14em;color:${T.dim};margin-bottom:6px;">交付物</div>
            <div style="font-size:12.5px;color:${T.gold};font-weight:600;">${out}</div>
          </div>
        </div>`).join("")}
      </div>
    </div>
  </div>`, 7));

/* 8 合作方式(米白亮页收束前的爆发) */
pages.push(P("03 怎么合作 · 方式", `
  <div class="h" style="font-size:42px;">三种合作方式</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
  ${[["企业内训","为团队定制六周训练营，用贵司真实业务做项目制实战","按期定价"],
     ["联合开课","与平台/社区联名开班，ChaoGeek 出内容与教学，共担共分","分成模式"],
     ["资产授权","开源实战库 + 方法论课件授权给培训机构使用","年度授权"]].map(([t,d,tag],i)=>`
    <div class="hair"></div>
    <div style="display:flex;align-items:center;padding:24px 4px;">
      <span class="mono" style="width:96px;font-size:15px;font-weight:700;color:${T.goldD};">0${i+1}</span>
      <span class="h" style="width:250px;font-size:22px;font-weight:800;">${t}</span>
      <span class="body" style="flex:1;font-size:14.5px;">${d}</span>
      <span class="mono" style="font-size:12px;color:#9A917D;border:1px solid ${T.lineL};padding:6px 14px;">${tag}</span></div>`).join("")}
  <div class="hair"></div>
  </div>`, 8, { light:true }));

/* 9 封底 */
pages.push(P("ChaoGeek", `
  <svg style="position:absolute;right:-100px;bottom:-140px;width:460px;height:460px;z-index:0;" viewBox="0 0 460 460">
    <circle cx="230" cy="230" r="180" fill="none" stroke="${T.gold}" stroke-width="2"/>
    <circle cx="230" cy="230" r="180" fill="${T.gold}" opacity=".08"/>
  </svg>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;">
    <div class="mark" style="margin-bottom:36px;"></div>
    <div class="h" style="font-size:62px;">别再收藏教程了，</div>
    <div class="h" style="font-size:62px;">来<span class="au">交付一次</span>。</div>
    <div class="lead" style="font-size:16px;margin-top:36px;">ChaoGeek · 超极客<br>
    <span class="mono" style="font-size:13px;">github.com/staruhub/ClaudeSkills</span></div>
  </div>`, 9));

fs.mkdirSync("html",{recursive:true});
pages.forEach((h,i)=>fs.writeFileSync(`html/p${i+1}.html`,h));
console.log(pages.length+" 页英黄提案生成");
