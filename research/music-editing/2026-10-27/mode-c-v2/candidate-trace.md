# 40个上游P/F候选的增量去向

原候选仍不是已验证研究空白；映射只说明本轮如何保留、归并、作为边界或暂缓。boundary_only不代表该论文结果无效，deferred不代表方向无价值。

| 上游来源/包 | 原ID | 原候选 | 标签 | 处理 | 对应v2 | 理由 |
|---|---|---|---|---|---|---|
| S-AED / ANALYSIS-20261027-AED-v2 | AED-P01 | 不微调权重的事件编辑方法，迁移音乐后是否能保持节拍与其他声部？ | AI | merged | P02, P05 | 事件到音乐的外推边界保留 |
| S-AED / ANALYSIS-20261027-AED-v2 | AED-P02 | 论文SVD重加权指数符号与代码不一致，哪一设置生成了报告结果？ | DE | retained | P06 | 配置身份/符号差异保留 |
| S-AED / ANALYSIS-20261027-AED-v2 | AED-F01 | 去除Null优化后FAD从4.95变5.33；去除EOT后CLAP从57.6降56.5%，体现不同组件的指标权衡。 | DE | retained | F06 | 源内消融事实保留 |
| S-AED / ANALYSIS-20261027-AED-v2 | AED-F02 | 冻结骨干也可以通过两种embedding梯度优化进行逐输入编辑。 | DE | merged | F05 | 合并到优化对象事实 |
| S-AMX / ANALYSIS-20261027-AMX-v2 | AMX-P01 | 无mask定量结果如何支持mask条件下的局部保留能力？ | AI | merged | P01, P02, P05 | 无mask定量不能确认局部音乐任务 |
| S-AMX / ANALYSIS-20261027-AMX-v2 | AMX-P02 | 潜在球面分解在同频重叠乐器中是否仍能分离目标且保持其他声部？ | AI | retained | P02 | 时频位置与声源身份边界 |
| S-AMX / ANALYSIS-20261027-AMX-v2 | AMX-F01 | 相同算法骨干切换时，FAD与KL优势并不集中在同一配置。 | DE | boundary_only | P03, M03 | 不同骨干指标偏好仅作比较边界，原事实留在源包，不增独立音乐现象票数 |
| S-AMX / ANALYSIS-20261027-AMX-v2 | AMX-F02 | 论文与公开代码均明确包含潜变量优化；无新模型训练并非无优化。 | DE | merged | F05 | latent优化并入定义事实 |
| S-DAE / ANALYSIS-20261027-DAE-v2 | DAE-P01 | 局部或结构编辑的提升是否仍存在于完整音乐片段，而不是仅10秒和代理指标？ | AI | retained | P05 | 前10秒与完整音乐外推 |
| S-DAE / ANALYSIS-20261027-DAE-v2 | DAE-P02 | 公开默认参数与论文动态引导配置不同，可能造成复现偏差。 | DE | retained | P06 | 默认/论文CFG差异 |
| S-DAE / ANALYSIS-20261027-DAE-v2 | DAE-F01 | 两骨干音乐行中共享噪声直接编辑的FAD/KL/SSIM均值优于DDPM对照；显著性须逐项看Table6。 | DE | retained | F04 | 限定两骨干代理量 |
| S-DAE / ANALYSIS-20261027-DAE-v2 | DAE-F02 | 移除显式反演减少相对DDPM的实测RTF，但并非快于SDEdit。 | DE | merged | F07 | 只保留各论文内部成本事实 |
| S-ETTS / ANALYSIS-20261027-ETTS-v2 | ETTS-P01 | 粗频轴先验扰动如何转为精确音乐音高控制而不改变其他声部？ | AI | boundary_only | P02, P05 | 不能从语音粗先验扰动推出精确音乐控制 |
| S-ETTS / ANALYSIS-20261027-ETTS-v2 | ETTS-P02 | 没有TTS文本对齐时如何定位真实音乐中的目标事件？ | AI | merged | P07, P05 | 语音对齐不是音乐目标定位的直接证据 |
| S-ETTS / ANALYSIS-20261027-ETTS-v2 | ETTS-F01 | 在语音评测中，先验扰动后的去噪比只做mel shift有更高MOS。 | DE | boundary_only | F08, M06 | 原MOS事实保留源包，只作为语音边界而非音乐现象 |
| S-ETTS / ANALYSIS-20261027-ETTS-v2 | ETTS-F02 | 同一噪声加原/编辑先验配合软mask可实现所展示语音中的局部变化。 | DE | boundary_only | F08, M01, M06 | 共享噪声/soft mask是类比，不计音乐重复 |
| S-MLD / ANALYSIS-20261027-MLD-v1 | MLD-P01 | 在其他骨干或复杂多声部中，Q/K替换是否仍保持结构而不锁死目标属性？ | AI | retained | P09, P02 | 层和操作边界单列 |
| S-MLD / ANALYSIS-20261027-MLD-v1 | MLD-P02 | 相对归一化综合分数是否掩盖目标服从与音乐结构的真实折中？ | AI | retained | P08 | 相对综合分定义单列 |
| S-MLD / ANALYSIS-20261027-MLD-v1 | MLD-F01 | 扩大SA替换至全部层会残留源音色，选择层8–14能改善编辑与结构折中。 | DE | retained | F12 | 源内层消融保留限定 |
| S-MLD / ANALYSIS-20261027-MLD-v1 | MLD-F02 | MelodiaEdit上CLAP/LPAPS改善，但Chroma和FAD并未全胜MusicMagus。 | DE | retained | F20 | 保留完整分项折中 |
| S-MF / ANALYSIS-20261027-MF-v2 | MF-P01 | 在相同骨干/codec下，正则反演如何权衡局部音乐结构保持与文本修改？ | AI | merged | P02, P03 | 结构保持与测量有效性分开 |
| S-MF / ANALYSIS-20261027-MF-v2 | MF-P02 | mono代理指标能否刻画立体声编辑后的声像保留？ | AI | merged | P05, P03 | mono自动指标/长音乐范围 |
| S-MF / ANALYSIS-20261027-MF-v2 | MF-F01 | 主观OVL/REL提升时CON可降低，说明编辑服从与源一致性不是同一目标。 | DE | retained | F02 | 跨骨干听测不可归因单因素 |
| S-MF / ANALYSIS-20261027-MF-v2 | MF-F02 | 冻结FM权重仍使用patch-KL梯度正则；公开代码与论文的若干默认配置存在差异。 | DE | merged | F05, F09 | 预测梯度与公开模型版本差异分开 |
| S-MG / ANALYSIS-20261027-MG-v1 | MG-P01 | 真实录音反演误差是否使合成音乐的结构保留优势失效？ | AI | merged | P05, P06 | 合成主实验到真实录音/反演版本范围 |
| S-MG / ANALYSIS-20261027-MG-v1 | MG-P02 | 外部captioning/API和语义方向采样对可重复性有多大影响？ | AI | retained | P07, P06 | caption条件与外部服务依赖 |
| S-MG / ANALYSIS-20261027-MG-v1 | MG-F01 | 音色任务加入L2注意力约束后Chroma由0.69升至0.76，CLAP由0.34变0.33。 | DE | retained | F11 | 音乐源内约束消融 |
| S-MG / ANALYSIS-20261027-MG-v1 | MG-F02 | 主方法冻结骨干但每个去噪步仍对latent做梯度更新。 | DE | merged | F05 | latent梯度而非权重训练 |
| S-PPAE / ANALYSIS-20261027-PPAE-v1 | PPAE-P01 | 音乐叠加声部在cross-attention控制下能否保持非目标音符与和弦？ | AI | merged | P02, P05 | 一般事件不能作为音乐复音证据 |
| S-PPAE / ANALYSIS-20261027-PPAE-v1 | PPAE-P02 | CLAP候选筛选带来的收益有多少来自额外搜索预算及评估器耦合？ | AI | retained | P08, P04 | 候选筛选评价及预算分列 |
| S-PPAE / ANALYSIS-20261027-PPAE-v1 | PPAE-F01 | 未编辑音频在Replace任务FAD更低，但目标CLAP远低，显示单指标与编辑成功可脱钩。 | DE | retained | F18 | 不编辑距离更优/对齐差 |
| S-PPAE / ANALYSIS-20261027-PPAE-v1 | PPAE-F02 | guidance候选数设为5，逐样本选择最高CLAP结果。 | DE | retained | F15 | 候选数事实 |
| S-STM / ANALYSIS-20261027-STM-v1 | STM-P01 | 潜变量优化的结构收益，在相同NFE/耗时预算下是否仍优于免优化路线？ | AI | retained | P04 | 统一信息/计算预算仍缺 |
| S-STM / ANALYSIS-20261027-STM-v1 | STM-P02 | 显著单频轨迹保持能否掩盖伴奏、和声和非目标声部变化？ | AI | merged | P02, P03 | top1轨迹不等于完整复音保持 |
| S-STM / ANALYSIS-20261027-STM-v1 | STM-F01 | 基础版无需显式反演，但仍以SGD迭代更新latent。 | DE | retained | F16 | 免反演不等于免优化 |
| S-STM / ANALYSIS-20261027-STM-v1 | STM-F02 | 同骨干ZoME表中CQT1和LPAPS优于ZETA，但CLAP不优于DDIM。 | DE | retained | F20 | 同表指标折中 |
| S-ZETA / ANALYSIS-20261027-ZETA-v2 | ZETA-P01 | 局部编辑为何影响mask外音乐事件，回拉是否影响目标修改？ | DE | retained | P01 | 局部外溢源内例子保留 |
| S-ZETA / ANALYSIS-20261027-ZETA-v2 | ZETA-P02 | 无监督主方向如何对应用户指定的具体音乐语义？ | SC | deferred | P07 | 无监督PC命名问题保留源包，但不扩张为本轮指定乐器编辑主连接 |
| S-ZETA / ANALYSIS-20261027-ZETA-v2 | ZETA-F01 | Tstart/CFG改变源一致性与文本服从的折中。 | DE | retained | F03 | CFG/Tstart曲线事实 |
| S-ZETA / ANALYSIS-20261027-ZETA-v2 | ZETA-F02 | 在相同源和采样模型上，mask外轨迹回拉能缓解所展示例的编辑外溢。 | DE | retained | F01 | 仅所示ZEUS鼓声外溢例子 |
