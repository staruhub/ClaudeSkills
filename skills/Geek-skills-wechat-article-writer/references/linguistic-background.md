# 反翻译腔的语言学根因

本文不影响执行——agent 不需要读这个文件。它给维护者和用户提供"为什么要做翻译腔检查"的理论支撑。

---

## 1. 形合 vs 意合：两套不兼容的句法操作系统

**英语**是形合（hypotaxis）——靠显性连接词（which/that/because/although）焊接逻辑，每个分句必须有主语，关系严格标记。

**汉语**是意合（parataxis）——靠语序和语义自然流动。"山高月小，水落石出"没有连词，逻辑自明。

翻译腔的核心症状——被动语气泛滥、"的"字堆叠、抽象名词做主语、连词堆砌——**几乎每一条都是英语结构穿透到汉语骨架里**。

> 奈达："就汉语和英语而言，也许在语言学上最重要的一个区别，就是形合和意合的对比。"（1983《Translating Meaning》）

## 2. LLM 翻译腔的三层机制

**预训练语料污染**：中文互联网、学术期刊、新闻报道、翻译著作——这些大规模语料本身已被翻译腔渗透。LLM 训练时见到的"自然中文"，并不完全自然。

**SFT 监督微调偏差**：Li et al. (ACL 2025) 发现超过 34% 的 SFT 训练数据本身带翻译腔。模型学到的"标准答案"就是翻译腔。更反直觉的是：**base model 的中文比微调后的更自然**——SFT 把它教坏了。即便是 GPT-4 直译，翻译腔率超过 40%。

**English pivot**：多语言模型内部常以英语做推理轴心。输出中文时底层语义结构是英语的，最后一步只换了词。

## 3. Accuracy-Naturalness Tradeoff

2025 年有理论论文证明：**翻译不存在一个同时最大化准确性和自然度的最优点，这两者的权衡是数学必然**。

示例：德语 "Meine Lehrerin ist nett"（我的老师[女性]人很好）翻译到英语：
- 自然版：My teacher is nice（丢失性别信息）
- 准确版：My female teacher is nice（保留信息但不自然）

这就是 skill 里"准确性优先（保守模式）"的理论基础——不同场景需要在这条曲线上选不同的点。

## 4. 为什么 LLM 翻译腔和人译翻译腔不同

Kong & Macken (2025) 的英汉新闻语料研究发现：LLM 已经自己学会了规避余光中九病的大部分（"的"、"被"、"进行"不再是首要问题），但产出了新一代翻译腔：
- 英文思维的物理隐喻（击穿论证、拆解问题）
- 英文学术风格的形容词起手式
- 英文技术写作的抽象名词骨架
- 段落内句长均匀、缺乏长短交错的节奏

这就是本 skill 的五类标记（§2.3）针对的病情。

## 参考文献

- Li et al. (2025). Lost in Literalism: How Supervised Training Shapes Translationese in LLMs. ACL 2025. arXiv:2503.04369
- Guo et al. (2024). Do LLMs Have an English "Accent"? arXiv:2410.15956
- Kong & Macken (2025). Decoding Machine Translationese in English-Chinese News. arXiv:2506.22050
- 余光中 (1987). 怎样改进英式中文？——论中文的常态与变态. 明报月刊
- 余光中 (1996). 论的的不休
- Nida & Taber (1964/1982). The Theory and Practice of Translation
- 连淑能 (2001). 英汉对比研究. 高等教育出版社
- 王力. 中国语法理论 / 汉语语法纲要
