const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.defineLayout({ name:"W", width:13.333, height:7.5 }); p.layout = "W";
const notes = [
  "开场:AI Native 不是加个聊天框,是核心决策权交给模型。今天讲两条实战方法论。",
  "三个问题的结构:先分清是什么,再给两条路线,最后教怎么选。",
  "全场最重要的一页:分界线是用户行为能否穷举。左边+AI,右边AI Native。",
  "第零步永远是判型。强调:选错方法论比没有方法论更危险。",
  "两条路线各管一半世界:克谦管确定性,雪峰管开放性。不是竞争关系。",
  "雪峰三原则,重点讲'多养专精虾'——每只虾只干一种活,出错能定位。",
  "概率乘让观众记住数字:0.99的51次方=0.59,不及格。停顿两秒。",
  "落地三步,给出时间预期:判型本周能做,选法一次评审定。",
  "收尾金句:穷举是死循环,唯快不破。指向仓库地址。"
];
for (let i=1;i<=9;i++){ const s=p.addSlide(); s.addImage({path:`png/p${i}.png`,x:0,y:0,w:13.333,h:7.5}); s.addNotes(notes[i-1]); }
p.writeFile({fileName:"ai-native-methodology.pptx"}).then(f=>console.log("生成:",f));
