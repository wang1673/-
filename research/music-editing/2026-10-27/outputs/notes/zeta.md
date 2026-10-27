# DDPM Inversion（ZETA；兼述ZEUS） — 音乐编辑研究分析笔记

> 日期：2026-10-27；分析 ID：ANALYSIS-20261027-ZETA-v2；来源 ID：S-ZETA；状态：partial  
> SC=作者主张；DE=本次直接核对的论文表格/算法/代码内容，不代表本次复现实验；AI=分析推断；UN=尚未核验。所有实验数字均为论文报告。PDF 页码从首页起算。  
> 范围：全文与相关附录阅读、LaTeX 对照、关键推理代码静态核对；没有下载模型权重、运行音频生成、独立重算指标或完成听测。

## 1. 一句话概述

对真实音频提取edit-friendly DDPM噪声序列，改变文本后重放实现ZETA；同文ZEUS通过后验主方向扰动探索无文本语义编辑。

## 2. 来源与版本

- 完整标题：Zero-Shot Unsupervised and Text-Based Audio Editing Using DDPM Inversion
- 作者：Hila Manor, Tomer Michaeli
- 机构：Technion – Israel Institute of Technology
- 文献版本：ICML2024/PMLR235正式PDF，内部页1–27（卷页34603–34629）；LaTeX辅助源为arXiv:2402.10009v4
- [原始 PDF（27页）](https://raw.githubusercontent.com/mlresearch/v235/main/assets/manor24a/manor24a.pdf)；[LaTeX 源码包](https://arxiv.org/src/2402.10009v4)
- 官方实现：https://github.com/HilaManor/AudioEditingCode
- 本次代码提交：`8dc937701a42f6fb53160912f8a96b42fe8261d8`。代码与论文版本分别记录，不能把后来发布的代码默认为论文实验原始版本。
- PDF SHA-256：`f8716ee1c353e4da969043256b01406855b3cb7740b17f6238104e4bfef5da1f`；完整来源及哈希见[来源清单](../source-manifest.json)。
- 配套机器可读包：[zeta.json](../packages/zeta.json)。

## 3. 研究问题与适用对象

冻结预训练音频扩散模型，能否在保留音乐结构时进行文本编辑，或无监督发现旋律/配器变化方向？

AudioLDM2（包括music与general检查点）；ZETA对照MusicGen-melody、DDIM、SDEdit；ZEUS对照源文本SDEdit。MusicDelta34首、107源提示、696目标提示，定量ZETA子采样324信号–文本对；有源和空源提示等设置。

预注册及预先指定唯一主要结果：UN，本次未核验，不将论文主表自动解释为预注册分析。

## 4. “无需训练”逐项审计

| 检查项 | 核对结论 |
|---|---|
| 生成骨干是否训练过 | 预训练AudioLDM2；并非无生成模型训练 |
| 编辑是否更新模型权重 | ZETA/ZEUS均不训练编辑模型 |
| 是否有逐输入推理优化 | ZETA无逐样本梯度拟合；ZEUS有额外主方向迭代计算，不能视为零成本 |
| 是否反演 | 有：提取每步DDPM噪声序列 |
| zero-shot成立范围 | 无编辑任务训练/个性化拟合；与未见过风格或无源音频条件不同 |

这里的分类针对实际更新对象与编辑阶段；不以论文标题中的 training-free/zero-shot 一词替代检查。

## 5. 方法、实现与测量

先构造源音频的加噪中间状态，再由反向均值解出每步噪声；以相同噪声在目标文本下反向采样。调Tstart和CFG控制编辑/保留。ZEUS额外做后验协方差主方向的子空间迭代，不等同于ZETA；用户mask可用轨迹回拉减少区域外影响。

CLAP目标相似；CLAP中间Swin特征构造LPAPS；CLAP特征FAD。长音频以重叠10秒窗口聚合。听测随机8秒片段，300人中277通过警觉题；图9给Wilson区间。

### 已访问的关键实现

| 文件 | 固定版本链接 |
|---|---|
| `code/main_run.py` | [查看源码](https://github.com/HilaManor/AudioEditingCode/blob/8dc937701a42f6fb53160912f8a96b42fe8261d8/code/main_run.py) |
| `code/ddm_inversion/inversion_utils.py` | [查看源码](https://github.com/HilaManor/AudioEditingCode/blob/8dc937701a42f6fb53160912f8a96b42fe8261d8/code/ddm_inversion/inversion_utils.py) |

本次只对下表所列机制做静态核对；没有声称完成整个仓库审计或端到端复现。

## 6. 主要结果与不确定性

| 结果／设置 | 论文方法 | 对照 | 不确定性与限制 | 证据 |
|---|---|---|---|---|
| 图9：ZETA听测偏好率 | 相对DDIM70.05%；MusicGen60.31%；SDEdit64.97% | 随机配对方法，目标兼顾文本与原曲精髓 | 图中Wilson区间；本次不从像素反推区间端点；277有效参与者 | ZETA-E03 |
| 图6：相近CLAP≈0.34时的LPAPS | 4.29 | SDEdit4.87；DDIM6.26；MusicGen5.74 | 这是单示例比较，不是全数据集平均 | ZETA-E02 |
| 30秒示例开销 | ZETA约37秒；噪声张量0.65GB，模型5.6GB | MusicGen35.5秒；无源prompt,Tstart100,总200步设置 | 论文环境点值；不是本机测量或硬件无关保证 | ZETA-E04 |

DE在本表只表示这些论文报告的数值已核对。尚未访问逐次运行数据，不将其表述为本次实测，也不从没有CI的均值推断统计显著。

## 7. 主张—证据—实现核对

| 主张 | 定位证据 | 结论边界 |
|---|---|---|
| SC：无需测试时优化即可文本编辑。 | ZETA-E01 / E06 | ZETA方法与关键代码一致；ZEUS的PC迭代应另列计算成本。 |
| SC：保留原曲结构并符合文本。 | ZETA-E02 / E03 | 支持该基准下的指标曲线/偏好；不是精确音符和全部声部的保证。 |
| SC：局部mask编辑。 | ZETA-E05 | 作者直接展示了区域外影响及软修正；不能将mask存在等同于无外溢。 |

## 8. 局限与可迁移性

- DE：作者承认骨干语言能力限制ZETA；ZEUS主方向不可预先命名，用户未必得到所需方向（PDF p.9 §5）。
- AI：324提示对来自34首，提示不是独立歌曲样本，统计汇总应考虑曲目聚类（ZETA-E02）。
- DE：mask外采用软轨迹约束，非严格恒等；文中data leakage指空间/时间影响外溢，不是训练测试污染（ZETA-E05）。
- AI：本文CLAP特征FAD/LPAPS不能直接和其他论文VGGish FAD或不同LPAPS作数值排行榜。
- UN：完整歌曲实时交互、所有反演随机性、公开当前分支与paper_code逐文件差异未全面实测。

AI：是音乐zero-shot扩散编辑的核心基线，适合优先复现；局部轨迹约束和Tstart/CFG折中可借鉴。若需要确定的音符级操作，ZEUS的无监督主方向仍缺乏可指定语义保证。

可复现性：中（静态审阅）：代码、提示集与评测实现可查；音乐数据需另取，paper_code与当前分支应分开固定；未跑实验。

涉及听测的审批、同意和全部原始记录尚未独立核验。音乐素材及模型权重的授权以原发布方说明为准；本记录只存分析与定位，不镜像论文、音频或权重。

## 9. 交给 deep-read 的候选素材

### 候选问题 P

- **ZETA-P01 [DE]**：局部编辑为何影响mask外音乐事件，回拉是否影响目标修改？ 证据：ZETA-E05。
- **ZETA-P02 [SC]**：无监督主方向如何对应用户指定的具体音乐语义？ 证据：ZETA-E01。

### 候选现象 F

- **ZETA-F01 [DE]**：Tstart/CFG改变源一致性与文本服从的折中。 证据：ZETA-E02。
- **ZETA-F02 [DE]**：在相同源和采样模型上，mask外轨迹回拉能缓解所展示例的编辑外溢。 证据：ZETA-E05。

这些只是来源分析候选，没有完成跨论文矩阵核验。下一阶段应补充机制条件、替代解释、证据强度与冲突，再筛选C连接点。

## 10. 证据索引

| 证据 ID | 类型 | 原始位置 | 本次核对内容 |
|---|---|---|---|
| ZETA-E01 | DE | PDF pp.3–5 §3.1–3.3，Eq.(1)–(5)，Fig.2；[PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/manor24a/manor24a.pdf#page=3) | DDPM提取噪声并复用；ZETA换文本，ZEUS沿后验主方向扰动；两条方法不能混名。 |
| ZETA-E02 | DE | PDF pp.6–8 §4.1–4.3，Figs.5–8；[PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/manor24a/manor24a.pdf#page=6) | 34首/324对及CLAP-LPAPS折中；Fig6的LPAPS数字只针对所展示例。 |
| ZETA-E03 | DE | PDF p.8 Fig.9；p.21 Appendix H；[PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/manor24a/manor24a.pdf#page=8) | 随机顺序8秒片段、排除唱歌prompt以对齐MusicGen；300→277有效参与者；偏好率与Wilson区间。 |
| ZETA-E04 | DE | PDF p.15 Appendix C；LaTeX App_InferenceMemoryCost.tex；[PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/manor24a/manor24a.pdf#page=15) | ZETA有source prompt时NFE更多；(3+S)Tstart；ZEUS额外K=50次子空间迭代；30秒开销与噪声内存。 |
| ZETA-E05 | DE | PDF p.17 Appendix D，Fig.14；LaTeX App_MaskFix.tex；[PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/manor24a/manor24a.pdf#page=17) | 模型结构会让局部编辑影响mask外；每步以δ=.025回拉mask外原轨迹，是软约束而非严格波形不变。 |
| ZETA-E06 | DE | code/ddm_inversion/inversion_utils.py L8–146、L147–280；code/main_run.py；README Change Log | 关键推理用no_grad并复用噪声；README明确paper_code分支为论文版本，当前固定commit为后续版本，不能宣称一比一论文复现。 |

SC/AI/UN 不能自动升级为 DE；跨域音乐推断与原始语音/事件结果分开保留。

## 11. 待补证据

- UN：所有曲目逐样本输出与独立重算
- UN：当前commit与论文分支全部差异
- UN：音符/和弦/声部级严格保持
- UN：音乐域外泛化与精确听测区间端点

下一技能：`deep-read Mode C`。本次没有设计最终新方法或实验方案。

## 本轮更新与历史来源

- v2替代`ANALYSIS-20261027-ZETA-v1`；原记录可从GitHub提交历史恢复。
- 固定PDF重新读取且SHA-256与旧清单相同；关键方法/结果重新核对。
- 本轮核对固定版本PDF的相关方法、实验及限制，复核所列关键代码；已有六篇的历史LaTeX审计保留并标明来源。未运行编辑模型、下载权重、重算指标或试听评价。
- 旧LaTeX审计与此前目视检查属于已有记录；本轮不重复声称完成全量LaTeX审计。
- 最新横向比较已扩展至10篇，见[comparison.md](../comparison.md)。
