# AudioMorphix — 音乐编辑研究分析笔记

> 日期：2026-10-27；分析 ID：ANALYSIS-20261027-AMX-v2；来源 ID：S-AMX；状态：partial  
> SC=作者主张；DE=本次直接核对的论文表格/算法/代码内容，不代表本次复现实验；AI=分析推断；UN=尚未核验。所有实验数字均为论文报告。PDF 页码从首页起算。  
> 范围：全文与相关附录阅读、LaTeX 对照、关键推理代码静态核对；没有下载模型权重、运行音频生成、独立重算指标或完成听测。

## 1. 一句话概述

用参考音频、时频掩码、球面潜变量混合/分解、梯度能量引导和注意力KV缓存完成编辑，不训练新编辑权重。

## 2. 来源与版本

- 完整标题：AudioMorphix: Training-free audio editing with diffusion probabilistic models
- 作者：Jinhua Liang, Yuanzhe Chen, Yi Yuan, Dongya Jia, Xiaobin Zhuang, Zhuo Chen, Yuping Wang, Yuxuan Wang
- 机构：Queen Mary University of London、University of Surrey、ByteDance
- 文献版本：arXiv:2505.16076v1，2025-05-21；本次采用该预印本，不混用匿名投稿版
- [原始 PDF（13页）](https://arxiv.org/pdf/2505.16076v1)；[LaTeX 源码包](https://arxiv.org/src/2505.16076v1)
- 官方实现：https://huggingface.co/spaces/JinhuaL1ANG/AudioMorphix
- 本次代码提交：`08008095c5a3f417b0bcfc397f9b73042faf6eee`。代码与论文版本分别记录，不能把后来发布的代码默认为论文实验原始版本。
- PDF SHA-256：`f8931bb0937e6c1a5a2a24abd59f293ec5050d91de3c2d3c87cbfbc2dfe4cb92`；完整来源及哈希见[来源清单](../source-manifest.json)。
- 配套机器可读包：[audiomorphix.json](../packages/audiomorphix.json)。

## 3. 研究问题与适用对象

在混合声音中，如何按参考音频只修改指定的时频区域并保持其余内容？

AudioSet-E 合成声音编辑基准：addition 1442、removal 1426、replacement 1870；比较DDIM、DDPM和AUDIT；AudioLDM/Tango 两种骨干。移位、拉伸、音高任务主要定性。

预注册及预先指定唯一主要结果：UN，本次未核验，不将论文主表自动解释为预注册分析。

## 4. “无需训练”逐项审计

| 检查项 | 核对结论 |
|---|---|
| 生成骨干是否训练过 | 使用预训练 AudioLDM/Tango 系列，不代表从零无训练 |
| 编辑是否更新模型权重 | 论文不更新骨干；已审代码的优化目标是潜变量而非新模型参数 |
| 是否有逐输入推理优化 | 有：removal的SGD潜变量优化，以及逐步能量梯度引导 |
| 是否反演 | 有：DDIM反演，亦用来缓存参考轨迹KV |
| zero-shot成立范围 | 无需任务特定训练数据来拟合新编辑器；仍依赖参考音频、掩码/条件和测试时计算 |

这里的分类针对实际更新对象与编辑阶段；不以论文标题中的 training-free/zero-shot 一词替代检查。

## 5. 方法、实现与测量

反演源与参考音频；addition 用SLERP；removal 对潜在扰动做SGD，论文100次、lr=1e-4；replacement串联去除与添加。采样时用特征一致/对比能量的梯度引导，缓存/替换自注意力KV。

FAD、KL；主观5维：fidelity、perceptual quality、consistency、region specificity、instruction adherence。Appendix C 每样本至少20名评分者，未给出这些均值的CI。Appendix B 定量比较对本法不提供mask。

### 已访问的关键实现

| 文件 | 固定版本链接 |
|---|---|
| `src/audio_morphix.py` | [查看源码](https://huggingface.co/spaces/JinhuaL1ANG/AudioMorphix/blob/08008095c5a3f417b0bcfc397f9b73042faf6eee/src/audio_morphix.py) |
| `src/model/sampler.py` | [查看源码](https://huggingface.co/spaces/JinhuaL1ANG/AudioMorphix/blob/08008095c5a3f417b0bcfc397f9b73042faf6eee/src/model/sampler.py) |
| `src/model/pipeline.py` | [查看源码](https://huggingface.co/spaces/JinhuaL1ANG/AudioMorphix/blob/08008095c5a3f417b0bcfc397f9b73042faf6eee/src/model/pipeline.py) |
| `src/utils/factory.py` | [查看源码](https://huggingface.co/spaces/JinhuaL1ANG/AudioMorphix/blob/08008095c5a3f417b0bcfc397f9b73042faf6eee/src/utils/factory.py) |

本次只对下表所列机制做静态核对；没有声称完成整个仓库审计或端到端复现。

## 6. 主要结果与不确定性

| 结果／设置 | 论文方法 | 对照 | 不确定性与限制 | 证据 |
|---|---|---|---|---|
| AudioLDM：Addition FAD / KL | 5.58 / 0.83 | DDIM 5.61 / 1.72；DDPM 19.18 / 2.27；AUDIT 5.81 / 3.17 | Table1点估计；CI/多随机种子差异未知 | AMX-E03 |
| AudioLDM：Removal；Replacement FAD / KL | 2.83 / 1.29；2.67 / 2.28 | DDIM 6.24 / 1.86；8.29 / 2.05 | replacement KL并非优于DDIM，不能概括成该配置所有指标最优 | AMX-E03 |
| Tango：Addition / Removal / Replacement KL | 0.57 / 0.77 / 0.62 | 相应FAD=6.62 / 6.29 / 7.27，均不如AudioLDM配置的FAD | 跨骨干优势不同；非音乐专项测试 | AMX-E03 |

DE在本表只表示这些论文报告的数值已核对。尚未访问逐次运行数据，不将其表述为本次实测，也不从没有CI的均值推断统计显著。

## 7. 主张—证据—实现核对

| 主张 | 定位证据 | 结论边界 |
|---|---|---|
| SC：training-free、zero-shot、局部区域编辑。 | AMX-E01 / E02 / E06 | 不训练新模型与有梯度的推理编辑同时成立；定量局部控制主张需结合AMX-E04的无mask设置。 |
| SC：全面优于比较方法。 | AMX-E03 | 须按骨干和指标限定；AudioLDM配置的replacement KL=2.28不如DDIM2.05。 |
| SC：consistency可超过ground truth。 | AMX-E03 | 聚合Table2中并非如此；只有region specificity高于GT。分任务Fig8可能不同，不能混写。 |

## 8. 局限与可迁移性

- AI：AudioSet-E为合成事件混合，不等价于真实录音多乐器谐波重叠与编曲编辑（AMX-E04）。
- DE：定量不提供mask，因此该实验不能独立量化mask条件下的局部保留能力（AMX-E04）。
- AI：SLERP的几何合理性不自动保证声源可加性或可辨识分离；机制前提还需独立对照（AMX-E01）。
- DE：Table3切空间投影对多个指标更差；不能把默认启用投影等同于已验证最佳配置。
- UN：尚未跑通HF实现、取得同版权重、核对每个比较方法骨干/预算及逐运行数据。

AI：适合参考音频驱动的乐器/音色局部编辑研究；若要求完全无逐样本优化应单独列出。时频mask不能自动隔离重叠的多个乐器，移调精度与旋律保持需音乐数据验证。

可复现性：中（静态审阅）：作者项目链接的HF Space有源码，页面暂停不等于代码不可得；已读关键函数，但未跑模型/复算指标。

涉及听测的审批、同意和全部原始记录尚未独立核验。音乐素材及模型权重的授权以原发布方说明为准；本记录只存分析与定位，不镜像论文、音频或权重。

## 9. 交给 deep-read 的候选素材

### 候选问题 P

- **AMX-P01 [AI]**：无mask定量结果如何支持mask条件下的局部保留能力？ 证据：AMX-E04。
- **AMX-P02 [AI]**：潜在球面分解在同频重叠乐器中是否仍能分离目标且保持其他声部？ 证据：AMX-E01、AMX-E05。

### 候选现象 F

- **AMX-F01 [DE]**：相同算法骨干切换时，FAD与KL优势并不集中在同一配置。 证据：AMX-E03。
- **AMX-F02 [DE]**：论文与公开代码均明确包含潜变量优化；无新模型训练并非无优化。 证据：AMX-E02、AMX-E06。

这些只是来源分析候选，没有完成跨论文矩阵核验。下一阶段应补充机制条件、替代解释、证据强度与冲突，再筛选C连接点。

## 10. 证据索引

| 证据 ID | 类型 | 原始位置 | 本次核对内容 |
|---|---|---|---|
| AMX-E01 | DE | PDF pp.4–6 §3–4；Fig.2–4；Eq.(8)–(14)；[PDF](https://arxiv.org/pdf/2505.16076v1#page=4) | 潜在空间一致性作为前提而非定理；SLERP与能量引导；透明重叠声音使时频格点不是单一声源。 |
| AMX-E02 | DE | PDF p.5 §3.2；p.11 Appendix D Algorithm1；[PDF](https://arxiv.org/pdf/2505.16076v1#page=5) | 梯度优化100次、1e-4、SGD；training-free不排除测试时优化。 |
| AMX-E03 | DE | PDF p.6 Tables1–2；p.7 Table3；LaTeX main.tex；[PDF](https://arxiv.org/pdf/2505.16076v1#page=6) | AudioLDM较优FAD、Tango较优KL；主观consistency 56.73低于GT60.25，region specificity58.76高于GT56.57。 |
| AMX-E04 | DE | PDF p.7 §5.1；p.11 Appendix A–C；[PDF](https://arxiv.org/pdf/2505.16076v1#page=7) | 数据规模、合成混合、参考样本来源；定量无mask；本法/DDIM50步 vs DDPM200步；每音频至少20位评分者。 |
| AMX-E05 | DE | PDF p.7 Fig.5；pp.12–13 Figs.6–8；[PDF](https://arxiv.org/pdf/2505.16076v1#page=7) | 音高、时间平移与拉伸展示主要定性，不能作为多声部音乐精确控制的定量证明。 |
| AMX-E06 | DE | src/utils/factory.py L357–413；src/audio_morphix.py L615–625；src/model/sampler.py L1278、L1380–1383 | 公开HF代码确认潜变量SGD与autograd梯度；removal调用显式enable_tangent_proj=True，需与论文ablation及运行配置对照。 |

SC/AI/UN 不能自动升级为 DE；跨域音乐推断与原始语音/事件结果分开保留。

## 11. 待补证据

- UN：独立运行与听测
- UN：真实音乐、多声部、音符/半音级定量验证
- UN：各对照完整配置公平性和权重版本
- UN：掩码条件下局部误差、失败与不确定性

下一技能：`deep-read Mode C`。本次没有设计最终新方法或实验方案。

## 本轮更新与历史来源

- v2替代`ANALYSIS-20261027-AMX-v1`；原记录可从GitHub提交历史恢复。
- 固定PDF重新读取且SHA-256与旧清单相同；关键方法/结果重新核对。
- 本轮核对固定版本PDF的相关方法、实验及限制，复核所列关键代码；已有六篇的历史LaTeX审计保留并标明来源。未运行编辑模型、下载权重、重算指标或试听评价。
- 旧LaTeX审计与此前目视检查属于已有记录；本轮不重复声称完成全量LaTeX审计。
- 最新横向比较已扩展至10篇，见[comparison.md](../comparison.md)。
