// 完整测试:构成主义红 · 9页 · 主题「设计宪法」(内容全部来自仓库真实资产)
// 母题:红楔/黑圆/对角线/超大标点;节奏化(仅关键页用对角线,深色页做明暗节奏)
const fs = require("fs");
const T = { red:"#D32F2F", ink:"#111111", paper:"#F5F1E8", dim:"#5A544A", faint:"#9A9284", line:"#2A2620", gold:"#E8B004" };
const BASE = `*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}
html,body{width:1280px;height:720px;overflow:hidden;font-family:"PingFang SC","Hiragino Sans GB",sans-serif;}
.mono{font-family:"SF Mono","DIN Alternate",monospace;}`;

function frame(section, inner, no, opt={}) {
  const bg = opt.dark ? T.ink : (opt.red ? T.red : T.paper);
  const fg = opt.dark||opt.red ? T.paper : T.ink;
  const sub = opt.dark||opt.red ? "rgba(245,241,232,.55)" : T.faint;
  const foot = opt.dark||opt.red ? "rgba(245,241,232,.3)" : T.faint;
  const lc = opt.dark||opt.red ? "rgba(245,241,232,.25)" : T.ink;
  return `<!doctype html><meta charset="utf-8"><style>${BASE}</style>
<body style="background:${bg};color:${fg};position:relative;">
<div style="position:absolute;left:80px;top:52px;font-size:11px;letter-spacing:.32em;color:${sub};font-weight:600;display:flex;align-items:center;gap:12px;">
  <span style="width:8px;height:8px;background:${opt.dark||opt.red?T.paper:T.red};display:inline-block;"></span>${section}</div>
<div style="position:absolute;right:80px;top:50px;font-size:10.5px;letter-spacing:.28em;color:${foot};">DESIGN CONSTITUTION</div>
${inner}
<div style="position:absolute;left:80px;right:80px;bottom:44px;border-top:2px solid ${lc};padding-top:14px;display:flex;justify-content:space-between;">
  <span class="mono" style="font-size:12px;font-weight:600;color:${fg};">deck-studio · constructivist red</span>
  <span class="mono" style="font-size:12px;color:${foot};">${String(no).padStart(2,"0")} — 09</span></div>
</body>`;
}
const pages = [];

/* 1 封面:对角线爆发(种子语言) */
pages.push(frame("提案 · Cover", `
  <div style="position:absolute;right:130px;top:130px;width:370px;height:370px;border-radius:50%;background:#fff;border:3px solid ${T.ink};"></div>
  <svg style="position:absolute;left:430px;top:190px;z-index:2;" width="640" height="340"><polygon points="0,340 640,50 640,150 90,340" fill="${T.red}"/></svg>
  <div style="position:absolute;left:80px;top:210px;z-index:3;transform:rotate(-11deg);transform-origin:left top;">
    <div style="font-size:82px;font-weight:900;line-height:1.1;">好设计不是<span style="color:${T.red};">品味</span>，</div>
    <div style="font-size:82px;font-weight:900;line-height:1.1;">是<span style="color:${T.red};">纪律</span><span style="font-size:100px;color:${T.red};">。</span></div>
  </div>
  <div style="position:absolute;left:80px;bottom:120px;font-size:16px;color:${T.dim};">deck-studio 风格库设计宪法 · 构成主义红实测</div>`, 1));

/* 2 目录:正交稳 */
pages.push(frame("目录 · Contents", `
  <div style="position:absolute;left:80px;top:150px;">
    <div style="font-size:44px;font-weight:900;margin-bottom:10px;">三个问题</div>
    <div style="font-size:15px;color:${T.dim};font-weight:300;">什么是好模板 · 怎么判断 · 怎么避坑</div>
  </div>
  <div style="position:absolute;left:80px;right:80px;top:290px;">
  ${[["01","诊断","AI 生成的 PPT 为什么普遍丑",1],["02","标准","判断好模板的五条硬标准",0],["03","避坑","四个必须避开的信号",0]].map(([n,t,d,hot])=>`
    <div style="border-top:1px solid ${T.line}33;display:flex;align-items:center;padding:26px 4px;">
      <span class="mono" style="font-size:52px;font-weight:900;width:130px;color:${hot?T.red:T.faint};">${n}</span>
      <span style="font-size:25px;font-weight:800;width:200px;">${t}</span>
      <span style="font-size:15px;color:${T.dim};flex:1;">${d}</span></div>`).join("")}
    <div style="border-top:1px solid ${T.line}33;"></div>
  </div>`, 2));

/* 3 问题:红楔指向 */
pages.push(frame("01 诊断 · 问题", `
  <div style="position:absolute;left:80px;top:150px;font-size:44px;font-weight:900;max-width:900px;line-height:1.25;">
    AI 生成的 PPT，<span style="color:${T.red};">为什么一眼就廉价</span>？</div>
  <svg style="position:absolute;right:80px;top:150px;" width="120" height="380"><polygon points="60,0 120,60 75,60 75,380 45,380 45,60 0,60" fill="${T.red}"/></svg>
  <div style="position:absolute;left:80px;top:300px;right:280px;">
  ${[["每次现场发挥","没有冻结的模板，构图、留白、配色每次重掷骰子"],["形容词驱动","「高端简约」给不出一个色值，模型只能回归均值"],["装饰堆砌","紫粉渐变＋圆角阴影＋emoji——模板感三件套"]].map(([t,d],i)=>`
    <div style="display:flex;gap:24px;padding:18px 0;border-top:1px solid ${T.line}22;">
      <span class="mono" style="font-size:20px;font-weight:900;color:${T.red};">0${i+1}</span>
      <div><div style="font-size:19px;font-weight:800;margin-bottom:6px;">${t}</div>
      <div style="font-size:14px;color:${T.dim};line-height:1.5;">${d}</div></div></div>`).join("")}
  </div>`, 3));

/* 4 转折:红底爆发 + 对角楔母题;强调词改黑底白字锐块(修对比度) */
pages.push(frame("01 诊断 · 论点", `
  <svg style="position:absolute;left:0;bottom:0;z-index:1;" width="1280" height="360"><polygon points="0,360 1280,120 1280,360" fill="rgba(0,0,0,.14)"/></svg>
  <div style="position:absolute;left:80px;top:200px;z-index:2;">
    <div style="width:60px;height:8px;background:#fff;margin-bottom:36px;"></div>
    <div style="font-size:76px;font-weight:900;line-height:1.2;color:#fff;">美不是 <span style="background:${T.ink};color:#fff;padding:0 14px;">生成</span> 的，</div>
    <div style="font-size:76px;font-weight:900;line-height:1.2;color:#fff;margin-top:8px;">是 <span style="background:${T.ink};color:#fff;padding:0 14px;">继承</span> 的。</div>
    <div style="font-size:17px;color:rgba(255,255,255,.85);margin-top:36px;max-width:820px;font-weight:300;">
      有品味的人把设计系统一次性冻结成模板与约束，之后 AI 只填内容、不发明设计。</div>
  </div>
  <div class="mono" style="position:absolute;right:70px;top:150px;font-size:280px;font-weight:900;color:rgba(0,0,0,.16);line-height:.75;z-index:1;">"</div>`, 4, { red:true }));

/* 5 五标准:正交表格 */
pages.push(frame("02 标准 · 五条", `
  <div style="position:absolute;left:80px;top:140px;font-size:42px;font-weight:900;">判断好模板的<span style="color:${T.red};">五条硬标准</span></div>
  <div style="position:absolute;left:80px;right:80px;top:240px;">
  ${[["可量化","能写出 token 表和版式坐标，不是只有形容词"],["约束完备","字重/配色/密度/节奏都有硬规则，无自由发挥的口子"],["内容普适","换任何主题都能填，不绑死某类内容"],["可渲染","HTML/CSS 能 100% 还原，不依赖手绘质感"],["有母题","一个贯穿的、可识别的视觉记忆点"]].map(([t,d],i)=>`
    <div style="display:flex;align-items:baseline;padding:16px 0;border-top:1px solid ${T.line}22;">
      <span class="mono" style="font-size:15px;font-weight:900;color:${T.red};width:44px;">0${i+1}</span>
      <span style="font-size:19px;font-weight:800;width:200px;">${t}</span>
      <span style="font-size:15px;color:${T.dim};flex:1;">${d}</span></div>`).join("")}
    <div style="border-top:2px solid ${T.ink};"></div>
  </div>`, 5));

/* 6 七步:巨型衬底数字消化死区 + 粗红对角楔接回母题(修 B4+断线) */
pages.push(frame("02 标准 · 方法", `
  <div style="position:absolute;left:80px;top:130px;font-size:42px;font-weight:900;">从<span style="color:${T.red};">流派</span>到<span style="color:${T.red};">模板</span>，七步</div>
  <div style="position:absolute;left:80px;right:80px;top:250px;bottom:150px;display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:1fr 1fr;gap:14px 18px;z-index:2;">
  ${["流派锚定","逆向成参数","Token 封闭","版式注册","节奏母题","双重校验","盲评定生死"].map((t,i)=>`
    <div style="border-left:3px solid ${T.red};padding:8px 0 8px 18px;display:flex;flex-direction:column;justify-content:center;position:relative;overflow:hidden;">
      <span class="mono" style="position:absolute;right:8px;bottom:-18px;font-size:88px;font-weight:900;color:${T.ink};opacity:.06;line-height:.8;z-index:0;">${String(i+1).padStart(2,"0")}</span>
      <div class="mono" style="font-size:20px;font-weight:900;color:${T.red};z-index:1;">${String(i+1).padStart(2,"0")}</div>
      <div style="font-size:17px;font-weight:800;margin-top:8px;line-height:1.25;z-index:1;">${t}</div></div>`).join("")}
    <div style="display:flex;align-items:center;justify-content:flex-start;padding-left:18px;">
      <svg width="130" height="64"><polygon points="0,24 96,24 96,8 130,32 96,56 96,40 0,40" fill="${T.red}"/></svg></div>
  </div>
  <div style="position:absolute;left:80px;bottom:100px;font-size:15px;color:${T.dim};font-weight:300;z-index:2;">
    不发明美学——每步都锚定有历史检验的流派，个人直觉会翻车，流派不会。</div>`, 6));

/* 7 反面:黑底(明暗节奏) */
pages.push(frame("03 避坑 · 反面", `
  <div style="position:absolute;left:80px;top:150px;font-size:42px;font-weight:900;color:#fff;">
    四个信号，<span style="color:${T.red};">命中即淘汰</span></div>
  <div style="position:absolute;left:80px;right:80px;top:270px;display:grid;grid-template-columns:1fr 1fr;gap:1px;background:${T.line};">
  ${[["形容词堆砌","「高端大气」却给不出色值"],["装饰依赖","去掉渐变阴影就什么都不剩"],["自由度过大","每次填出来都不一样"],["模板感三件套","居中＋彩虹渐变＋圆角滥用"]].map(([t,d])=>`
    <div style="background:${T.ink};padding:30px 34px;">
      <div style="font-size:20px;font-weight:800;color:${T.red};margin-bottom:10px;">✕ ${t}</div>
      <div style="font-size:14px;color:rgba(255,255,255,.6);line-height:1.5;">${d}</div></div>`).join("")}
  </div>
  <div style="position:absolute;left:80px;bottom:110px;font-size:14px;color:rgba(255,255,255,.5);font-weight:300;">
    元判据：归藏 2 套 8.8k★ vs 商业库 10 万套无人叫好——数量是坏信号，策展是好信号。</div>`, 7, { dark:true }));

/* 8 行动:正交 */
pages.push(frame("03 避坑 · 落地", `
  <div style="position:absolute;left:80px;top:150px;font-size:42px;font-weight:900;">17 套风格，<span style="color:${T.red};">一套宪法</span></div>
  <div style="position:absolute;left:80px;right:80px;top:280px;display:flex;gap:56px;">
  ${[["17","个风格已入库，每套锚定一个公认流派"],["26","来源普查，评级表＋反面清单存档"],["6/6","首次实战审计的违例全部修复"]].map(([n,d],i)=>`
    <div style="flex:1;border-top:3px solid ${i===0?T.red:T.ink};padding-top:16px;">
      <span class="mono" style="font-size:64px;font-weight:900;color:${i===0?T.red:T.ink};line-height:.9;">${n}</span>
      <div style="font-size:14px;color:${T.dim};margin-top:14px;line-height:1.5;">${d}</div></div>`).join("")}
  </div>`, 8));

/* 9 封底:实红锐角楔收在页脚线以上(不压页脚)+ 实黑楔指向标题 */
pages.push(frame("Design Constitution", `
  <svg style="position:absolute;right:0;top:120px;z-index:0;" width="520" height="440"><polygon points="520,0 520,440 60,440" fill="${T.red}"/></svg>
  <svg style="position:absolute;right:400px;top:300px;z-index:1;" width="220" height="120"><polygon points="220,0 220,120 0,60" fill="${T.ink}"/></svg>
  <div style="position:absolute;left:80px;top:220px;transform:rotate(-8deg);transform-origin:left;z-index:2;">
    <div style="width:60px;height:8px;background:${T.red};margin-bottom:34px;"></div>
    <div style="font-size:70px;font-weight:900;line-height:1.15;"><span style="color:${T.red};">纪律</span>，是</div>
    <div style="font-size:70px;font-weight:900;line-height:1.15;">自由的前提<span style="color:${T.red};">。</span></div>
  </div>
  <div style="position:absolute;left:80px;bottom:110px;font-size:15px;color:${T.dim};z-index:2;">github.com/staruhub/ClaudeSkills · deck-studio</div>`, 9));

fs.mkdirSync("html",{recursive:true});
pages.forEach((h,i)=>fs.writeFileSync(`html/p${i+1}.html`,h));
console.log(pages.length+" 页构成主义 deck 生成");
