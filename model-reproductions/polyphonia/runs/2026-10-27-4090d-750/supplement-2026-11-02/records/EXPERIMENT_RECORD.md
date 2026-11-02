# Polyphonia750 补充指标与试听实验记录

记录日期：2026-11-02（Asia/Shanghai）；状态：七项客观指标字段已补齐，复现限制如下。原750生成音频、逐任务指标和最终审计未修改；全部750音频与50参考音频SHA核验通过。

## 指标结果

| 指标 | 数值/均值 | 总体标准差 | 状态 |
|:--|--:|--:|:--|
| CLAP | 0.350375737 | 0.081901637 | original750_task_metric |
| LPAPS | 4.678991292 | 0.489502186 | original750_task_metric |
| CQT1_PCC | 0.333473234 | 0.230453299 | original750_task_metric |
| FAD | 0.779795870 | — | empirical_distribution_distance_existing_CLAP_features |
| KAD | 0.003024635 | — | polynomial_family_matches_paper_but_exact_author_parameters_unpublished |
| ASB | 0.861230564 | — | paper_baseline_reference_approximation_user_authorized |
| AMB | 0.930290454 | — | paper_baseline_reference_approximation_user_authorized |

原CLAP、LPAPS、CQT1-PCC各750有效、0未定义。新增FAD/KAD为50个参考与750个生成片段之间的集合指标，不存在逐任务标准差；ASB/AMB为聚合分数，未估计置信区间。

## 阅读与实现核对

已核对[Polyphonia论文附录J、表1](https://arxiv.org/html/2605.10203v1)和[官方代码](https://github.com/Ltx-Leif/polyphonia/tree/26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc)。官方仓库提供编辑与提示词代码，未提供完整指标评测实现。论文要求CLAP音乐检查点、CLAP-Swin LPAPS、CQT2010、CLAP特征的FAD及多项式核无偏MMD。不能将引用工具包的默认设置直接当作作者全部实验设置。

FAD：固定[microsoft/fadtk](https://github.com/microsoft/fadtk/tree/ec74b1f96d5576ec04e721985fa0f0d14d965d9b)的原函数体，用样本协方差与Fréchet高斯距离。复用旧实验逐文件哈希核验的512维归一化CLAP音乐特征，每个10秒片段一个向量；没有改用当前fadtk默认的尾部填充多窗、int16往返量化和fp16存储抽取。故是当前实验特征协议下的FAD，不是声称作者精确流水线结果。独立PSD计算值0.779795920129；独立torch CUDA float64值0.779795913792，差异小于1e-5；未做无限样本外推。

KAD：遵循原实验早已记录的补充约定 k(x,y)=(xᵀy/512+1)^3，用去除同集合对角项的无偏MMD²。论文没有公开degree/gamma/coef0/缩放；这些是显式复现假设，不能与论文表中数值直接排名。[原kadtk](https://github.com/YoonjinXD/kadtk/tree/7373161f2e0e4da1c25e5f67d979eab10a828d33)实际采用Gaussian核，和Polyphonia正文描述不同。作为敏感性诊断另存gamma=1多项式值3.024498119、原kadtk Gaussian×100值27.112049646，均不冒充论文精确KAD。

ASB/AMB：按用户确认，采用论文7种基线的已发表且经过四舍五入的均值，替换Polyphonia一行为本次复现结果。8方法逐指标Z-score后MinMax；ASB=H(CLAPnorm,(-LPAPS)norm)，AMB=H(CLAPnorm,CQT1-PCCnorm)，H为调和平均。该流水线的Z-score与随后MinMax合并在代数上等价于直接MinMax。论文原8行回放最大绝对差0.002636，所以标注“论文基线参照近似值”，不当作同裁剪严格基线实测。

论文TTA、CTI、GAC属于真人主观评分，需要参与者试听问卷；本次没有捏造这三项分数。

## 数值异常及处理

Default OpenBLAS CPU dispatch produced invalid eigenvectors (orthogonality error3596.56), causing previous negative FAD and failed assertions. Haswell dispatch restored eigenvector checks without changing packages, source embeddings or main750data. Default-dispatch attempted values are invalid and excluded; original failure log retained. Applied only to new supplement and demo processes.

此次仅选择现有OpenBLAS的Haswell内核与1线程，没有升级任何Python包。恢复后特征分解残差2.12e-16，正交性误差3.72e-14；FAD与KAD另用torch CUDA float64独立验证通过。失败日志保留，负FAD尝试值无效且不作为结果。原实验指标未被重新写入。

## 新生成试听示例

音乐：AM Contra - Heart Peripheral的同一中间10秒，用官方未修改脚本新生成vocals2violin、vocals2saxophone两个任务。均为100步、CFG3.5、maskbias2.5、fp16、seed928、energy mask、原down层配置；独立新进程，不读写原750随机状态。

猫叫：ESC-50的1-47819-A-5.wav，44100Hz单声道5秒真实录音，来源[ESC-50](https://github.com/karolpiczak/ESC-50)，Freesound原始src_file=47819，保留CC BY-NC数据集署名。重采样16k并重复一次为10秒；因是孤立动物事件，直接将同一信号作为mixture与other目标轨，非目标轨不存在，没有假称Demucs动物分离。两个目标描述分别为普通狗叫、深沉大狗叫，仍用原官方编辑配置。它是域外扩展示例，不计入750音乐评测。

初次深沉狗叫任务的softmask短语不是baseline的连续子串，触发官方回退分支CPU/CUDA错误；新进程重试仍失败。随后仅按官方mirror规则把短语改为“a large dog barking”，保留失败输入与日志，未改模型源码或编辑超参，重新单独运行成功。

辅助CLAP诊断（不是人工听感评分，不据此宣称狗叫已逼真）：

| 文件 | 猫叫文本余弦 | 狗叫文本余弦 | 狗减猫 |
|:--|--:|--:|--:|
| cat_original | 0.436324 | 0.174900 | -0.261424 |
| cat_to_dog | 0.132450 | 0.505612 | 0.373162 |
| cat_to_dog_deep | 0.096916 | 0.509609 | 0.412693 |

每个before_after.wav按“原音10秒→静音0.5秒→编辑10秒”排列。试听副本单声道16k，单独调整至RMS0.1且峰值不超过0.95；原输入与模型输出不改。全部输出检查有限、非静音、160000采样，哈希在validation.json。未进行人工听感成功判定，两个版本都交付。

## 保存位置与证据

- 原实验与补充：/root/autodl-tmp/polyphonia_repro/results/musdb_center10_htdemucs_4090d_01
- 补充指标、输入哈希、原论文基线表、独立校验：/root/autodl-tmp/polyphonia_repro/results/musdb_center10_htdemucs_4090d_01/metrics-supplement-v1
- 新示例、原始输出、试听副本、失败和重跑日志：/root/autodl-tmp/polyphonia_repro/demos/2026-11-02
- 补算源码和固定参考实现：/root/autodl-tmp/polyphonia_repro/supplement-metrics-v1
- 完整机器记录：/root/autodl-tmp/polyphonia_repro/results/musdb_center10_htdemucs_4090d_01/metrics-supplement-v1/EXPERIMENT_RECORD.json

本次为补充测量与探索性示例，无新基线推理、无真人主观实验、无统计因果假设。旧裁剪作者清单未公开、估计分轨重建、旧3060续跑随机流等比较限制继续保留。没有上传新的GitHub内容或删除已有文件。
