# Polyphonia 750 任务最终实验记录

## 记录元数据

- 包类型：EXPERIMENT_RECORD；包版本：research-pipeline-contract v1.0。
- 实验/记录 ID：EXP-20261027-polyphonia-4090d-750。
- 日期：2026-10-27；最终检查：2026-10-27T12:46:42.560562+00:00（UTC，北京时间加 8 小时）。
- 领域与类型：音频生成、计算复现。操作者：本聊天自动执行流程；来源 Idea ID：none。
- 协议：原 protocol.json，加用户授权的新服务器重部署及全部 750 任务范围。
- 状态：**completed**。750 个生成、750 条三指标评测、最终音频与统计校验全部通过。

## 研究目标与设计

在 RTX 4090 D 上按原 Polyphonia 配置完成 MUSDB18-HQ test 的 50 首 × 15 个官方编辑任务，记录 CLAP、LPAPS、CQT1-PCC；未预设指标变化方向。实验单位是嵌套于 50 首歌曲中的 750 个任务。仅一次 seed 928 运行，无独立重复、无盲法人工评分。本次范围由旧前 200 个扩展至原有全部 750 个，未重新抽样或改变任务顺序。

主结果为全 750 任务三指标的均值与总体标准差。旧 RTX 3060 只完成前 200 个，因此全量 750 均值不能直接当作与旧 200 均值的同样本 GPU 对照；下面另列相同前 200 子集。

## 实际配置与版本

- GPU NVIDIA GeForce RTX 4090 D，49140 MiB，驱动 580.105.08。
- 官方代码 commit：26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc；参考归档 commit：5c179a266ff461b00c040410c4e0b8caf5675623。8 个官方源码文件哈希核对通过。
- AudioLDM2：cvssp/audioldm2，revision c8e7e189d324425c05c4c2f81214041ef4107983。
- Python 3.8.20；torch/torchaudio 2.4.1+cu124；torchvision 0.19.1+cu124；diffusers 0.32.0；transformers 4.46.3。原 freeze 共 107 项逐项匹配，pip check 与 CUDA fp16 矩阵运算通过。
- 对整首原始混音运行 HT-Demucs 4.0.1，shifts 1、overlap 0.25、seed 928，然后同步裁剪中间 10 秒；不是用数据集真实分轨作为生成输入。
- 编辑参数：100 steps、CFG 3.5、mask bias 2.5、fp16、seed 928、energy mask、原 down 1–18 层配置。每首按官方入口从 seed 928 开始，保留原任务顺序。
- CLAP 音乐检查点 SHA256：fae3e9c087f2909c28a09dc31c8dfcdacbc42ba44c70e972b58c1bd1caf6dedd。RoBERTa 固定 revision e2da8e2f811d1448a5b465c236feacd80ffbac7b。
- 只计算原三指标，未补 FAD、MMD、MOS、ASB/AMB；声道处理与掩码公式保持原实现。

## 数据与证据血缘

原 MUSDB18-HQ test 全长混音 → 与旧记录一致的 SHA256/原 ZIP CRC 验证 → 新 GPU 整首 HT-Demucs 估计分轨 → 同步中间 10 秒裁剪 → 750 个新编辑 WAV → 三指标逐任务记录与汇总 → 独立最终校验。

50 首原始混音全部与旧实验 SHA256 一致。旧前 200 任务涉及的 14 首混音裁剪文件也全部与旧文件 SHA256 一致。原服务器不可用，旧估计分轨无法取回，因此新估计分轨重新生成，**没有证据证明新旧估计分轨逐字节一致**。未复用旧生成 WAV、旧 RNG 或旧评测缓存。

服务器主副本均位于 /root/autodl-tmp：

- 项目、脚本、来源记录：/root/autodl-tmp/polyphonia_repro。
- 原始混音：/root/autodl-tmp/polyphonia/musdb18hq/test。
- 新裁剪与估计分轨：/root/autodl-tmp/polyphonia/prepared/center10_htdemucs_01。
- 环境、模型与新随机状态：/root/autodl-tmp/polyphonia/runtime；新 RNG 子目录 rng-musdb_center10_htdemucs_4090d_01。
- 结果：/root/autodl-tmp/polyphonia_repro/results/musdb_center10_htdemucs_4090d_01。
- 关键证据：结果内 protocol.json、status.json、pipeline.json、full750.audit.json、completion-receipt.json、metrics/summary.json、metrics/per_task.csv；项目 logs 下 environment-comparison.json、source-checksums.json、all-data.manifest.json、crop-comparison.json、evaluation-tokenizer-repair.json。

## 全 750 任务结果

| 指标 | 均值 | 总体标准差 | 有效 | 未定义 |
| --- | ---: | ---: | ---: | ---: |
| CLAP | 0.350376 | 0.081902 | 750 | 0 |
| LPAPS | 4.678991 | 0.489502 | 750 | 0 |
| CQT1_PCC | 0.333473 | 0.230453 | 750 | 0 |

标准差表示该任务集合的离散程度，不是独立重复运行的标准误或置信区间；同一歌曲的任务相关。本轮没有排除任务、未定义指标或最终失败任务。750 个新 WAV 均为 16kHz、单声道、10 秒，有限且非静音，哈希与逐任务评测匹配；本地副本又独立核对了 750 条 CSV 的唯一性、任务集合、均值与总体标准差。

## 与旧卡相同前 200 任务的描述性对照

| 指标 | 旧 3060 均值 | 新 4090 D 相同前 200 均值 | 新子集总体标准差 |
| --- | ---: | ---: | ---: |
| CLAP | 0.366880 | 0.367105 | 0.079640 |
| LPAPS | 4.785495 | 4.786999 | 0.464934 |
| CQT1_PCC | 0.312406 | 0.312900 | 0.216361 |

这是同样本的描述性对照，不是纯 GPU 因果实验：新 Demucs 分轨重新生成，旧轮还曾中断后续跑，随机流不能保证一致。不据此认定全部分数差异都由 GPU 导致，不做显著性推断。

## 时间、异常与恢复

- 生成控制器从 2026-10-27 18:13:13（北京时间）启动，分轨与生成总耗时 7896.45 秒，约 2 小时 11 分 36 秒。50 首的分轨和编辑子进程均退出 0，750 个生成输出全部校验通过；未发生生成断点恢复。
- 首首 15 任务的生成工作进程新卡用时 146.65 秒，旧 RTX 3060 记录为 443.15 秒，约 3.02 倍加速；这是单批端到端观测，包含模型加载/反演等开销，不推广为所有场景的 GPU 理论性能。
- 首次评测在导入 laion_clap 时失败，原因是新服务器离线缓存缺少其初始化时要求的 BERT/BART 分词器。当时尚未计算指标，原失败状态和日志保存在 history/evaluation-tokenizer-repair/ 及运行日志中。
- 补齐 bert-base-uncased revision 86b5e0934494bd15c9632b12f734a8a67f723594 与 facebook/bart-base revision aadd2ab0ae0c8268c7c9693540e9904811f36177 的分词器缓存并记录哈希。旧实验没有记录这两套初始化用分词器 revision；它们不是本次 CLAP 实际使用的 RoBERTa 文本分支。没有升级依赖、改变指标公式、替换 CLAP/RoBERTa 权重或重生成音频。
- 确认原流程退出后，仅执行 resume_evaluation_only.sh 恢复评测与最终校验。评测程序日志计时 21.26 秒，含导出流程计时 30.24 秒；最终 full-pipeline.exit=0、pipeline.state=completed、full750.audit.json=passed。
- 部署曾更换目标服务器：上一 RTX 2080 Ti 的下载/等待进程已停止；本轮没有在那里进行生成。下载通道与分块方式曾为解决网络中断而调整，所有入选文件仍经过完整哈希校验。
- 平台费用未记录，不推断实际账单。没有人工试听、MOS 或其他主观评测记录。

## 结论边界与下一步

当前证据支持：按本次记录的协议，在新卡上完成全部 750 任务、原三指标与最终校验，获得可追溯结果。

当前证据不支持：精确复现论文表格（作者未公开同样裁剪清单）、纯 GPU 导致分数变化、跨数据集泛化、主观音质结论或独立重复的统计置信度。

数据已齐全，后续若需要误差与异质性分析，可由 squeeze-experiment 消费本记录；本次没有自动追加实验、改参数或上传 GitHub。
