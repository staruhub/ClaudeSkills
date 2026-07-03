const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.defineLayout({name:"W",width:13.333,height:7.5}); p.layout="W";
const notes=[
 "开场不讲课程,先讲差距:把AI玩明白的人正在拉开差距。停两秒。",
 "三件事结构:为什么做、怎么做、怎么合作。",
 "痛点页让曲线说话:工具爆炸vs能力平线,差距在方法不在工具。",
 "三阶段各自有真实交付物,强调'不讲原理课'。",
 "对比页:和通识课的三行区别,重点讲'带走什么'。",
 "证据页数字全部真实可查:开源仓库19个skill、113条评测、CI。",
 "六周节奏:每周指着交付物讲,'没有产出的那一周不该存在'。",
 "三种合作方式,按对方身份着重讲其中一种。",
 "收尾:别再收藏教程了,来交付一次。留repo地址。"];
for(let i=1;i<=9;i++){const s=p.addSlide();s.addImage({path:`png/p${i}.png`,x:0,y:0,w:13.333,h:7.5});s.addNotes(notes[i-1]);}
p.writeFile({fileName:"chaogeek-bootcamp-proposal.pptx"}).then(f=>console.log("生成:",f));
