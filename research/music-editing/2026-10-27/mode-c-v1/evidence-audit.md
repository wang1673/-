# 来源、状态与跨设置审计

日期：2026-10-27；矩阵：MODEC-20261027-MUSIC-PRESERVATION-v1。

## 输入与历史

- 用户指定的6个ANALYSIS_PACKAGE全部读取，固定于commit `64f8c5728df46c66e31d57434b754b233062de1f`。
- 输入路径：`research/music-editing/2026-10-27/outputs/ANALYSIS_PACKAGES.json`；Git blob：`3fbb049fde81879fc7bc56436ff391b44016d8ce`。
- 本轮没有覆盖原分析包或旧笔记；新增目录为`research/music-editing/2026-10-27/mode-c-v1`。
- 源ID S-DAE / S-AMX / S-AED / S-MF / S-ZETA / S-ETTS和各上游analysis_id均保留。
- 原候选P/F在新矩阵中重新分组并编号；origin_candidates给出沿革，未将候选原样升级为机制。
- 源论文PDF版本、页码及代码commit继承固定上游记录；本轮不另存论文、LaTeX、源码或音频副本。

## 本轮实际核对

- 原论文HTML：ZETA局部回拉Eq6/Fig14、§4.2指标、§4.4指标讨论、AppendixC成本；AudioMorphix重叠声音设定、AppendixB无mask、AppendixD优化算法；MelodyFlow Table1、Algorithm1、§3.2/3.4；DirectAudioEdit音乐主表、数据长度、动态CFG与计算设置；AudioEditor TableV和方法；EdiTTS限制。
- 固定GitHub代码：DAE main_run.py核心L271–310及默认L448–475；AED Null优化L129–161与条件embedding更新L110–132；EdiTTS diffusion.py双轨L286–336。
- HF固定版本原始/页面链接本轮重访未成功：AudioMorphix factory.py；MelodyFlow flow.py/renoise.py。相关代码细节标为继承上游静态核对，不伪称本轮重新访问成功；B类分类另由原文算法直接支持。
- 新增E18：ZETA §4.4关于LPAPS音乐意义的讨论。它是作者解释SC，不是本轮测量，没有扩展新论文来源。

## 标签与状态不混淆

| 项 | 解释 |
|---|---|
| SC | 作者提出/声称的解释；例如网络结构导致外溢、时频重叠的建模动机、LPAPS局限说明 |
| DE | 在原文表、公式、算法或代码中可直接定位的内容，经验数字依然来自作者实验 |
| AI | 本轮推断；例如时频位置保持不足以保证同时间其他声部保持、允许音色变化与整体距离混杂 |
| UN | 原始输出、声部级诊断、统一预算复现等缺失；不是不存在/无效 |
| supported | 只支持一个明确限定的矩阵联系，如已知软回拉公式和所展示例；不代表完整因果归因或新方法有效 |
| plausible | 有可追踪依据，但目标音乐场景、机制或替代解释尚未闭合 |
| diagnostic-needed | 有值得检查的问题，但直接证据不足 |
| unsupported | 本批材料未形成该联系；不是负面实验结论 |

矩阵60格中有8格supported、19格plausible、21格diagnostic-needed、12格unsupported。总体包为partial，推荐C01只是plausible；没有声部级的新结果。

## 哪些“跨论文一致”不能多计票

- DAE与ZETA复用MedleyMDPrompts/MusicDelta，且DAE只取前10秒；不是独立音乐集合上的重复。
- MF的跨骨干听测同时改变骨干、codec等；CON较低不等于反演算法导致旋律破坏，也不等于差异已统计显著。
- AMX与AED主要一般声音事件；它们的定量结果不与音乐声部实验等价。
- EdiTTS仅语音，依赖TTS对齐；共享噪声/软mask提供类比，不能视为音乐机制复验。
- 多prompt、随机种子、时间窗口都不自动等于独立曲目。
- VGGish/CLAP FAD、各自LPAPS与下混mono评价不是一个统一量纲。

## 关键保留/修正

1. 回拉mask外轨迹是已有操作；不能包装成新贡献。其当前步代数收缩不保证后续全部采样/解码严格不变。
2. DAE两骨干音乐代理量均值较好，AudioLDM2音乐FAD对DDPM在上游Table6未显著；不把“均值更低”写成“全都显著”。
3. MF Table1±误差未单独定义置信水平；不自动套用Table2生成任务CI95。
4. MF代码cfg_coef=0只说明实现中的guidance系数设置，不能不看公式/source文本就称为unconditional。
5. DAE公开默认cfg_tar=[8]与论文8→12不同；MF公开版处理数据不同；AED公式/代码符号有差异。影响量未知，不能直接断言作者结果错误。
6. AMX定量无mask；这限制局部性证据，不能反向断言有mask时一定失败。
7. 原始波形不变不适合作为合法音色替换的唯一成功标准；应先声明任务允许变化的属性。

## 新颖性与评分

没有进行扩展查新。C01新颖性1代表需比较相近工作；C02/C03为已知诊断问题，新颖性0。三个分数只用于当轮排序，不应写进论文作为创新性证据。

## 未做及待补

- 目标音乐任务联合声部/旋律/节奏/局部性标注与原始输出
- 相同骨干与条件信息下A/B方法等预算质量比较
- 新颖性扩展检索与相近工作核对
- 真实分轨或已知控制变化下的指标灵敏性诊断
- 长曲/立体声/域外曲目与失败案例
- 论文与公开checkpoint/配置的一致性及实际影响

所有最低成本核验都标记proposed_not_run。未知硬件、可用分轨、现成输出或授权材料时，不承诺具体耗时/费用。先核验材料和测量可行性，再考虑完整方法设计。
