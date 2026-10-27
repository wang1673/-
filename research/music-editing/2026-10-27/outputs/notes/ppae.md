# PPAE — 音乐编辑研究分析笔记

> 2026-10-27 · ANALYSIS-20261027-PPAE-v1 · evidence_status: partial
> SC=作者主张；DE=可定位并已阅读的论文/代码内容，不代表独立重复实验；AI=分析推断；UN=未知。论文表格中的数字统一标为作者报告。
> 本轮核对固定版本PDF的相关方法、实验及限制，复核所列关键代码；已有六篇的历史LaTeX审计保留并标明来源。未运行编辑模型、下载权重、重算指标或试听评价。

## 来源与定位

- 标题：Prompt-guided Precise Audio Editing with Diffusion Models
- 作者：Manjie Xu, Chenxing Li, Duzhen Zhang, Dan Su, Wei Liang, Dong Yu
- 版本：ICML 2024/PMLR235正式PDF，18页，卷页55126–55143
- [正式发表信息](https://proceedings.mlr.press/v235/xu24p.html)；[本次引用PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/xu24p/xu24p.pdf)
- PDF SHA-256：`3e812bf4e897c87eeda6a195bb285c51cd2b4909b61f4a0fd6d57342f31385ea`
- 开源状态：官方论文/项目页可定位；本轮未找到可确认的完整官方编辑代码，不能写成已完整开源。
- [机器可读ANALYSIS_PACKAGE](../packages/ppae.json)

## 研究问题与设计

冻结TTA扩散模型，用注意力融合和自适应引导实现事件级替换、修饰和重加权，能否减少非目标内容变化？

主要Tango骨干；cleaned FSD50K，每任务100个编辑测试；100 inference steps，cross-replace0.8/self-replace0/skip50，guidance候选n=5。14参与者，每任务30个编辑对听测。

## 无需训练审计

| 检查项 | 结论 |
|---|---|
| backbone | 预训练Tango等TTA扩散模型 |
| edit_weight_update | False |
| per_input_gradient | 取决于反演模块；不能统称gradient-free |
| gradient_target | null-text反演可优化unconditional embedding；核心attention fuser无新增权重训练 |
| inversion | 有；Appendix B提供null-text/DDIM设置 |
| zero_shot_scope | 无编辑配对训练；n=5候选筛选仍有额外推理成本 |

## 方法与测量

先反演源音频，再以Fuser在源/目标cross-attention间平滑过渡；跨样本使用不同CFG候选生成，用CLAP Filter挑选目标相关性最高的结果。反演模块依骨干可用DDIM/null-text等，附录明确null-text优化。

Replace：FAD/LSD/FD/KL；Refine部分参照为目标文本重生成，非严格同结构真值；Reweight用CLAP识别事件强弱。CLAP在文中部分设置经softmax，不能直接与其他论文原始cosine比。

## 作者主张与直接证据

| SC作者主张 | DE定位内容 | 分析边界 | 证据 |
|---|---|---|---|
| training-free精准局部编辑 | 算法1、Fuser及guidance bootstrapping | 无新增权重训练；多候选、反演优化和数据域需单独标注 | PPAE-E01 |
| 能保持非目标事件 | Table3 unrelated分数、Figs3–6示例 | 仅支持该事件任务代理测量；不证明音乐和弦/声部不变 | PPAE-E03 |

## 论文报告结果

| 结果/设置 | 方法结果 | 对照 | 不确定性/边界 | 证据 |
|---|---|---|---|---|
| Replace：FAD / LSD / FD / KL / CLAP | 2.15 / 1.51 / 27.53 / 1.30 / 0.62 | PTP 2.95 / 2.83 / 45.91 / 4.42 / 0.57 | Table1未给CI；不是音乐专用测试 | PPAE-E03 |
| Refine：FAD / KL / CLAP | 6.86 / 1.92 / 0.63 | PTP 9.35 / 1.17 / 0.32 | Table2 KL并未优于PTP；重生成参照与源结构混杂 | PPAE-E03 |

## 局限、推断与未知

- AI/审计限制：一般事件证据为主，音乐refine有示例但没有系统多声部结构评价。
- AI/审计限制：用CLAP选择输出又以CLAP衡量目标服从，可能放大同评估器优势；需独立指标/听测。
- AI/审计限制：候选n=5改变预算；与单候选基线比较须记录NFE和端到端耗时。
- AI/审计限制：Replace的未编辑音频FAD1.86低于PPAE2.15，但CLAP0.12；单看FAD会偏向不编辑。
- AI/审计限制：正文引用null-text并非每个配置都必然使用该优化；代码未核验，不强行指定统一梯度结论。

- UN：完整官方编辑代码与固定commit未确认
- UN：各骨干具体反演配置未独立运行
- UN：音乐专项和精确声部保持证据不足

## 对音乐编辑的可迁移性

AI：适合作为一般音频注意力控制与CFG筛选参考，不应把FSD50K结果当音乐专项优胜。若严格排除输入优化，要明确选择的反演配置。

## 下游候选P/F

- **PPAE-P01 [AI]** 音乐叠加声部在cross-attention控制下能否保持非目标音符与和弦？ 证据：PPAE-E01, PPAE-E03。
- **PPAE-P02 [AI]** CLAP候选筛选带来的收益有多少来自额外搜索预算及评估器耦合？ 证据：PPAE-E01, PPAE-E02, PPAE-E03。
- **PPAE-F01 [DE]** 未编辑音频在Replace任务FAD更低，但目标CLAP远低，显示单指标与编辑成功可脱钩。 证据：PPAE-E03。
- **PPAE-F02 [DE]** guidance候选数设为5，逐样本选择最高CLAP结果。 证据：PPAE-E01, PPAE-E02。

## 证据索引

| ID | 稳定位置 | 核对内容 |
|---|---|---|
| PPAE-E01 | [PDF pp.4–5 §3.3–3.6，Eq.(5)，Algorithm1](https://raw.githubusercontent.com/mlresearch/v235/main/assets/xu24p/xu24p.pdf#page=4) | Fuser平滑注意力注入，guidance候选生成及CLAP选择。 |
| PPAE-E02 | [PDF p.5 §4.2–4.4；p.15 Appendix B/Algorithm2](https://raw.githubusercontent.com/mlresearch/v235/main/assets/xu24p/xu24p.pdf#page=5) | FSD50K每任务100；n=5；null-text反演含embedding优化，依骨干配置而异。 |
| PPAE-E03 | [PDF pp.6–8 Tables1–6；p.17 Tables7–8](https://raw.githubusercontent.com/mlresearch/v235/main/assets/xu24p/xu24p.pdf#page=6) | 替换/修饰/重加权结果、14人30对听测及误差条；主表和附录分开读。 |
| PPAE-E04 | [官方PMLR论文页及论文p.2脚注项目地址](https://raw.githubusercontent.com/mlresearch/v235/main/assets/xu24p/xu24p.pdf#page=2) | 正式ICML发表可确认；完整官方代码可得性本轮仍UN。 |

页码从PDF首页算起；卷页与PDF页分开。所有数值为论文报告，未独立重复。下一阶段为deep-read Mode C。
