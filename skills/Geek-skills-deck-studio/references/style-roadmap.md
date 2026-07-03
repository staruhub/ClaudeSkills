# Style Roadmap — 风格库路线图（带证据的扩张策展）

> 依据:T6 全景普查（26 来源,含 MoMA/Cooper-Hewitt/NN|g/Material 官方）。
> 元原则:**策展制,非堆量**——归藏 2 套 8.8k★ vs 商业库 10 万套无人叫好。终态 ≤14 套。
> 每个候选按五条硬标准评级:可量化 / 约束完备 / 内容普适 / HTML-CSS 可渲染 / 有母题。

## 评级「高」——已批准揽入

| 流派/大师 | 可抄参数 | 落库名 |
|-----------|---------|--------|
| Bauhaus | 三原色+黑白灰;母题限圆/方/三角;无衬线;平衡的不对称 | `creative/bauhaus-geometric` |
| 俄国构成主义 | 红黑白;**对角线构图**签名;粗字+超大标点;红楔白圆范式 | `creative/constructivist-red` |
| Neubrutalism | 自带 CSS 配方:3px 黑描边 + 8px 硬阴影(零模糊)+ 圆角 0 + 高饱和撞色 | `media/neubrutalism-pop` |
| Otl Aicher 慕尼黑系统 | Univers 系字体;功能分色编码;像素网格图标;史上最可参数化系统 | `business/aicher-system` |
| Material Design 3 | 唯一官方 token 全公开(26 色彩角色+30 字阶);照抄成 CSS 变量 | 作 **token 工程参照系**,不单独成风格(平台感>风格感) |

## 评级「中高」——排队,特定场景启动

- **De Stijl/Mondrian**:规则最严(三原色+黑粗线正交网格)但装长文勉强 → **只做封面/章节页专用版式**,注册进 layout-registry 而非独立风格
- **Art Deco**:中轴对称+金黑+母题清单(旭日纹/之字纹/阶梯形)→ 高端庆典/年报域
- **Saul Bass/Paul Rand**:单色底+剪纸剪影+负空间 → 构图骨架可模板化,剪影素材按主题生成
- **田中一光**:12 格模数网格+几何拼贴(Nihon Buyo 范式)→ 东方几何变体
- 前两轮已批:Apple Bento / 学术蓝灰(Tufte 载体)/ Kinfolk 明色编辑 / 原研哉留白(需先自定量化标准,定不出就不做)

## 明确不揽入(有依据否决)

| 候选 | 否决理由 |
|------|---------|
| David Carson/Grunge | 本质反规则,每张都是一次性艺术品,不可模板化 |
| Y2K/Frutiger Aero | 铬质感/光晕依赖位图,CSS 难高保真;梗图化严重 |
| Flat/Metro | 与瑞士派同构 ~70%,无独立价值 |
| Wim Crouwel | 与墨白重叠七成 → 并入墨白变体 |
| 佐藤可士和 | 品牌策略>版式系统,单页素材密度不足 |
| Brutalism 原教旨 | "故意难看"与内容普适冲突;取 Neubrutalism 即可 |

## 反面清单(公认廉价化,永不收)

1. **Corporate Memphis/Alegria 扁平小人插画**——WIRED"互联网视觉大规模同质化",已发讣告级批评
2. **Memphis 稀释版**——要收只收 1981 原教旨浓度(Bacterio/水磨石),不收派对彩纸版
3. **紫粉渐变 + emoji 图标 + 默认字体**——AI 模板感三件套
4. **做旧 Grunge 滤镜 / Y2K 铬字**——脱离语境只剩廉价感

## 终态蓝图(≤14 套)

已有 3(墨白/极夜/英黄)+ 高评级 4(Bauhaus/构成主义/Neubrutalism/Aicher)+ 前轮优先 3(Bento/学术蓝灰/ChaoGeek 像素)+ 场景补充 3-4(Kinfolk/Art Deco/田中一光/中文正式)+ 单页特例(De Stijl 封面版式)。Glassmorphism 只作卡片级点缀。

## 待补功课(做对应模板包前)

- Aicher 奥运色板精确色值:从 otlaicher.de 档案或 1972 设计手册扫描件确认
- Plakatstil(Lucian Bernhard 单物件海报)15 分钟快查,可能是"中高"遗珠
- 证据全文:scratchpad ppt-research/notes/T6-canon-styles.md(26 来源)
