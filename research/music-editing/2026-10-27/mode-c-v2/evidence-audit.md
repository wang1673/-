# 来源与证据状态审计：Mode C v2

2026-10-27 · MODEC-20261027-MUSIC-PRESERVATION-v2

## 输入快照与沿革

- 读取提交 `b20076e135e9f9e7a09daa0e1ccbaf022cb055b9` 的当前10个分析包；原6篇v2，新增4篇v1。上游包全部为partial。
- 读取完整mode-c-v1/MODE_C_PACKAGE.json和evidence-audit.md，保留旧P/F/M/E/C编号指代和60格；新建mode-c-v2。
- 上游40个P/F候选全部重新归并或明确暂缓/保留为边界证据，不静默补齐缺失材料。
- PDF页码继承固定上游；HTML只核查相关内容，不假定不同版本逐字一致。本轮没有下载PDF、模型、数据或音频。

## 本轮原始材料核对

- MusicMagus arXiv v3 HTML：§4的CA梯度约束、Table3指标折中、§6.1真实录音caption/反演；固定p2p_pipeline.py L1159–1204再次阅读SGD与backward。
- Melodia arXiv v3 HTML：probe Tables1–2、源Q/K目标V、Table5层消融、Table3分项及Eqs11–12归一化。上游AAAI正式PDF的页码与数值保留，不称本轮重新下载正式版。
- PPAE arXiv v1 HTML：Guidance Bootstrapping、实验候选数、Replace表、反演模块；PMLR页码继承上游。
- SteerMusic arXiv v3 HTML：DDS、个性化PDM、结果与附录预算；固定SteerMusic_edit.py L55–119再次阅读源初始化、共享t/noise、SGD及冻结骨干。
- 原六篇本轮复核当前分析包与旧矩阵的来源/证据/边界；此前原文和代码审计不冒充本轮重新完成。
- 正式PDF的部分web入口返回不可访问/超时或不支持的内容类型；使用相关arXiv HTML作内容交叉核查，未把访问失败解释为论文/代码不存在。

## 三组需要拆开的命题

1. **注意力**：CA损失约束对latent求梯度 ≠ 直接替换CA图 ≠ 特定层SA源Q/K替换。MusicMagus与Melodia不构成同一种干预得出相反结果。低probe准确率不能证明该表示不含语义。
2. **评价**：CLAP从候选中选最大值的条件性分数提升，不是独立人类质量提升；ASB/AMB依比较集合归一化，不是成功率。两种依赖分别审计；本轮未测实际偏差或排序翻转。
3. **免训练/免反演**：SteerMusic基础版免反演仍优化latent，+版额外微调；DirectAudioEdit的位移差与DDS更新共享某些条件，但数学等价和统一预算效果未知。

## 直接证据与推断

- 直接材料支持的是源内报告、算法、定义或固定代码事实，不是本轮实测。
- 新增音乐代理指标/层消融没有直接证明同时发声的非目标声部保持，所以C01不升级为supported。
- 结构相似分较好可能来自目标编辑更弱；不把这种替代解释直接写成样本已失败。
- mask外轨迹回拉与声部身份保持不同；一般事件/语音只提供边界或类比。

## 证据独立性

- MusicDelta/MedleyMDPrompts在ZETA、DAE及新增音乐工作中复用；DAE只取前10秒，不能算独立长曲验证。
- Melodia与SteerMusic都使用ZoME，但子集和协议不同；前者的整表不与后者460例四子任务直接等价。
- 多篇用AudioLDM2、CLAP及其特征；同骨干/同评估器是共享依赖，不能按论文数计算机制证据强度。
- 多prompt、窗口、seed、同听者重复评分不是独立曲目或独立参与者。
- 预训练重叠、曲目级去重、逐样本输出、原始听测与代码参数完全对应仍UN。

## 状态分布

| 状态 | 格数 |
|---|---|
| supported | 19 |
| plausible | 49 |
| diagnostic-needed | 85 |
| unsupported | 27 |


supported仅限定单格关系；总体为partial。C01/C04为plausible，C02/C03/C05/C06为diagnostic-needed，没有把研究连接当作已验证方法。

## 本轮未执行

音频生成/编辑、训练、权重下载、统一预算计时、指标标定/敏感性重算、分轨诊断或听测均未执行；也未扩展查新。所有最低成本核验只是材料审计入口。
