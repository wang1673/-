# Melodia — 音乐编辑研究分析笔记

> 2026-10-27 · ANALYSIS-20261027-MLD-v1 · evidence_status: partial
> SC=作者主张；DE=可定位并已阅读的论文/代码内容，不代表独立重复实验；AI=分析推断；UN=未知。论文表格中的数字统一标为作者报告。
> 本轮核对固定版本PDF的相关方法、实验及限制，复核所列关键代码；已有六篇的历史LaTeX审计保留并标明来源。未运行编辑模型、下载权重、重算指标或试听评价。

## 来源与定位

- 标题：Melodia: Training-Free Music Editing Guided by Attention Probing in Diffusion Models
- 作者：Yi Yang, Haowen Li, Tianxiang Li, Boyu Cao, Xiaohan Zhang, Liqun Chen, Qi Liu
- 版本：AAAI 2026正式PDF，9页，卷页2209–2217
- [正式发表信息](https://ojs.aaai.org/index.php/AAAI/article/view/37204)；[本次引用PDF](https://ojs.aaai.org/index.php/AAAI/article/download/37204/41166)
- PDF SHA-256：`3a4e0939b873459482cbdd5f79b6280f58067cc37c43abe4421e13790774c107`
- 开源状态：固定commit完整目录树仅见数据、说明和图示，未找到核心编辑/评价实现。仓库存在不能等同于方法完整开源。
- [固定代码版本](https://github.com/YiYang-SCUT/Melodia/tree/3ff1ab915261b61cc9763e690753f27aebe69fc5)：`3ff1ab915261b61cc9763e690753f27aebe69fc5`。
- [机器可读ANALYSIS_PACKAGE](../packages/melodia.json)

## 研究问题与设计

不提供源音乐文本描述，能否通过选择性self-attention结构保留实现音乐属性编辑？

AudioLDM2，200 inference steps，目标CFG5.5；MusicDelta、ZoME-Bench及MelodiaEdit。后者2015对：1090合成、925源自真实数据的重建样本。听测100招募、77有效，每数据集10测试样本。

## 无需训练审计

| 检查项 | 结论 |
|---|---|
| backbone | 预训练AudioLDM2；另报告Stable Audio Open迁移 |
| edit_weight_update | False |
| per_input_gradient | 论文算法不需要；核心代码未公开核验 |
| gradient_target | 无论文指定的逐输入梯度拟合；probe实验训练分类器另计 |
| inversion | 部分DDIM反演并缓存Q/K |
| zero_shot_scope | 无额外编辑微调；source-prompt-free；不是免反演 |

## 方法与测量

部分DDIM反演时缓存源self-attention的Q/K；目标去噪时在AudioLDM2层8–14用源Q/K形成的注意力图乘目标V。无额外编辑微调；论文编辑算法未列逐输入梯度优化。属性probe分类器训练属于研究诊断，不是部署编辑器训练。

CLAP、LPAPS、Chroma、源/编辑FAD；ASB/AMB把比较方法内归一化分数取调和均值；听测REL/CON/MEB。

## 作者主张与直接证据

| SC作者主张 | DE定位内容 | 分析边界 | 证据 |
|---|---|---|---|
| SA保留结构、CA编码属性 | probe分类准确率差异及Fig2换层实验 | 支持该骨干/探针下的操作证据；低probe准确率不能证明SA不含语义 | MLD-E01 |
| 无需源描述、无需额外训练 | 反演+Q/K repository+目标V的ASR公式 | 论文算法支持；代码缺失使实现与资源开销仍为UN | MLD-E02 |

## 论文报告结果

| 结果/设置 | 方法结果 | 对照 | 不确定性/边界 | 证据 |
|---|---|---|---|---|
| MelodiaEdit：CLAP / LPAPS / Chroma / FAD | 0.39 / 3.11 / 0.68 / 0.65 | DDPM-Friendly 0.34 / 4.06 / 0.70 / 0.67；MusicMagus 0.27 / 3.32 / 0.73 / 0.57 | Table3未给CI；CLAP/LPAPS领先，不是所有结构指标第一 | MLD-E03 |
| MelodiaEdit听测REL / CON / MEB | 3.38 / 3.65 / 3.81 | DDPM-Friendly 2.58 / 2.92 / 2.78 | Table4未报CI；77有效回答，试题/曲目不是独立参与者 | MLD-E03 |

## 局限、推断与未知

- AI/审计限制：对CA与SA的功能分工不能从单一probe/层替换推广到所有音乐模型。
- AI/审计限制：2015提示对不是2015首独立歌曲；合成与真实来源重建部分应分层看。
- AI/审计限制：ASB/AMB相对于所比较方法归一化；1.00不是100%成功率，加入方法可能改变归一化。
- AI/审计限制：层8–14是AudioLDM2经验设置；不能直接照搬到DiT/其他采样率。
- AI/审计限制：核心实现未找到，未独立复现指标和Stable Audio Open迁移。

- UN：核心编辑和评价代码未找到
- UN：未访问所有原始运行/听测评分
- UN：探针训练与骨干、采样步、缓存成本未完整复现

## 对音乐编辑的可迁移性

AI：与音乐结构保留和严格无输入梯度路线高度相关，但当前更适合作为机制与基准参考。先复核Q/K缓存的时序、层选择及代码可得性。

## 下游候选P/F

- **MLD-P01 [AI]** 在其他骨干或复杂多声部中，Q/K替换是否仍保持结构而不锁死目标属性？ 证据：MLD-E01, MLD-E02, MLD-E03。
- **MLD-P02 [AI]** 相对归一化综合分数是否掩盖目标服从与音乐结构的真实折中？ 证据：MLD-E03。
- **MLD-F01 [DE]** 扩大SA替换至全部层会残留源音色，选择层8–14能改善编辑与结构折中。 证据：MLD-E01, MLD-E03。
- **MLD-F02 [DE]** MelodiaEdit上CLAP/LPAPS改善，但Chroma和FAD并未全胜MusicMagus。 证据：MLD-E03。

## 证据索引

| ID | 稳定位置 | 核对内容 |
|---|---|---|
| MLD-E01 | [PDF pp.3–4 Tables1–2，Fig.2](https://ojs.aaai.org/index.php/AAAI/article/download/37204/41166#page=3) | CA/SA probe与注意力替换；是经验性诊断，不是结构语义完全解耦证明。 |
| MLD-E02 | [PDF pp.4–5 Fig.3，Eqs.(8)–(10)](https://ojs.aaai.org/index.php/AAAI/article/download/37204/41166#page=4) | 部分DDIM inversion，源Q/K、目标V，层8–14，source-prompt-free。 |
| MLD-E03 | [PDF p.6 Tables3–4，Eqs.(11)–(12)；p.7听测与Tables5–6](https://ojs.aaai.org/index.php/AAAI/article/download/37204/41166#page=6) | 三数据集比较、相对归一化ASB/AMB、77有效听测和层选择/跨模型实验。 |
| MLD-E04 | [官方仓库固定commit递归目录树及README](https://github.com/YiYang-SCUT/Melodia/tree/3ff1ab915261b61cc9763e690753f27aebe69fc5) | 检查了全部文件类型：未见核心.py或.ipynb编辑器；公开内容主要为MelodiaEdit数据。 |

页码从PDF首页算起；卷页与PDF页分开。所有数值为论文报告，未独立重复。下一阶段为deep-read Mode C。
