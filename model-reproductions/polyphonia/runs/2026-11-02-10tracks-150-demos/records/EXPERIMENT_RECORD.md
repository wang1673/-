# Polyphonia：10首数据集音乐 × 15项编辑试听记录

日期：2026-11-02，Asia/Shanghai。状态：10首×15=150项生成、三指标与音频校验完成。原750实验保持不变。

## 设计与来源

沿用MUSDB18-HQ test原protocol顺序的前10首，运行前确定，不按结果挑选。每首只用原中间10秒混音及同一时间估计HTDemucs分轨，无整首再处理。每首完整官方15任务、顺序不变。第一首为本聊天刚完成的15项新示例，保留并入本集合；本请求另新跑9首135项。没有复用旧750生成WAV或随机状态，没有补跑7种基线。对照为同一源音与编辑结果，不是跨方法实验。

官方代码commit26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc，AudioLDM2 revision c8e7e189d324425c05c4c2f81214041ef4107983。100steps、CFG3.5、maskbias2.5、fp16、seed928（每首新进程重置）、energy mask、原down1–18层；RTX4090D49140MiB。环境不升级，新进程沿用已验证Haswell BLAS和1线程设置。每首一次反演后生成15项。

| 序号 | 曲目 | 任务数 | 原音对目标CLAP均值 | 编辑后对目标CLAP均值 |
|--:|:--|--:|--:|--:|
| 1 | AM Contra - Heart Peripheral | 15 | 0.1518 | 0.3288 |
| 2 | Al James - Schoolboy Facination | 15 | 0.1369 | 0.3589 |
| 3 | Angels In Amplifiers - I'm Alright | 15 | 0.0664 | 0.2816 |
| 4 | Arise - Run Run Run | 15 | 0.1854 | 0.3858 |
| 5 | BKS - Bulldozer | 15 | 0.2450 | 0.4482 |
| 6 | BKS - Too Much | 15 | 0.1380 | 0.4146 |
| 7 | Ben Carrigan - We'll Talk About It All Tonight | 15 | 0.1674 | 0.2976 |
| 8 | Bobby Nobody - Stitch Up | 15 | 0.1097 | 0.3061 |
| 9 | Buitraker - Revo X | 15 | 0.2776 | 0.3520 |
| 10 | Carlos Gonzalez - A Place For Us | 15 | 0.1016 | 0.3594 |

## 汇总与不确定性

| 指标 | 均值 | 总体标准差 | 有效/未定义 |
|:--|--:|--:|--:|
| source_target_CLAP | 0.157981605 | 0.094639092 | 150/0 |
| edited_target_CLAP | 0.353303259 | 0.081686869 | 150/0 |
| CLAP_delta | 0.195321654 | 0.091026225 | 150/0 |
| LPAPS | 4.824715422 | 0.490381729 | 150/0 |
| CQT1_PCC | 0.304219090 | 0.221274444 | 150/0 |

三指标实现及检查点与原750评测相同，原音对目标CLAP是无编辑对照；正CLAP差值只支持向目标语义移动。LPAPS/CQT1-PCC反映结构保留，不是编辑成功率。标准差为此150任务的总体离散程度，不是置信区间，未做显著性或因果检验。10首为固定顺序便利样本，不外推整体性能。FAD/KAD为集合分布量，ASB/AMB需方法群归一化，本次不伪造逐任务值；原750七指标补充单独存档。

## 官方任务映射及限制

保留官方infer_edit_stem实现：仅vocals2/drums2/bass2子串匹配，其余都映射other。因此bass_guitar2upright等任务键虽意指贝斯，官方实际映射other，未为示例静默改代码。具体异常共1项，列在EXPERIMENT_RECORD.json的task_mapping_anomalies_retained和逐任务official_edit_stem列。中文标签只辅助阅读，原任务键与目标文本完整保留。个别任务guitar前缀可能只是官方命名，不断言实际原音一定是吉他。

没有人工TTA/CTI/GAC问卷分数，未声称150项都听感成功。论文精确裁剪清单未公开，HTDemucs估计分轨为重建数据，旧3060续跑随机流限制继续保留；不能把新旧差异全部归因GPU。

## 试听和校验

打开10首音乐试听对照.html进入每首15项页面。每段before_after为原音10秒+0.5秒停顿+编辑10秒，总20.5秒仅用于对照；模型每次输入输出各10秒。试听副本目标RMS0.1且峰值限制0.95，raw输出字节不变。150输出全部16kHz、单声道、160000采样、有限且非静音，文件SHA逐项核验；原750summary、CSV、audit哈希未变。完整协议、原输入哈希、输出哈希、逐任务值与偏差记录在EXPERIMENT_RECORD.json。所有输出均保留，不挑选最好案例。

服务器主副本：/root/autodl-tmp/polyphonia_repro/demos/2026-11-02-ten-tracks。原数据和模型仍在/root/autodl-tmp。GitHub仅上传实验文本记录、脚本、提示词、指标、哈希与状态，不上传音频、数据集、权重、环境或SSH材料；本地试听包与服务器保留完整音频。

## 打包异常与恢复

Generation/evaluation already complete. Original first demo had Jupyter auto-created .ipynb_checkpoints HTML snapshot without nearby audio. Aggregation now excludes checkpoint and AppleDouble metadata copies; no actual task audio or scores changed. Prior failure status/log retained under history.
