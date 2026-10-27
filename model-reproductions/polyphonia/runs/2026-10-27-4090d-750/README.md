# Polyphonia：RTX 4090 D 全 750 任务

2026-10-27，MUSDB18-HQ test 50首各15个官方任务，生成、原三指标评测与最终校验全部完成。

| 指标 | 均值 | 总体标准差 | 有效/未定义 |
| --- | ---: | ---: | ---: |
| CLAP | 0.350376 | 0.081902 | 750/0 |
| LPAPS | 4.678991 | 0.489502 | 750/0 |
| CQT1-PCC | 0.333473 | 0.230453 | 750/0 |

[完整实验记录](records/EXPERIMENT_RECORD.md) · [750任务逐项CSV](records/metrics/per_task.csv) · [精确汇总](records/metrics/summary.json) · [最终独立校验](records/full750.audit.json) · [完成回执](records/completion-receipt.json)

[原协议与裁剪清单](records/protocol.json) · [750任务控制配置](records/control.json) · [环境逐项核对](provenance/environment-comparison.json) · [源混音哈希](provenance/all-data.manifest.json) · [14首旧裁剪对照](provenance/crop-comparison.json) · [相同前200任务对照](records/metrics/matched_first200_comparison.json)

每首中间10秒；对整首原混音运行HT-Demucs再裁剪估计分轨；100steps、CFG3.5、maskbias2.5、fp16、seed928、energy mask、原down层。新生成目录与随机状态独立，无旧生成音频或评测缓存复用。

原服务器不可用，用户授权重新部署；全部50首源混音SHA与旧记录一致，旧前200涉及的14首混音裁剪也逐字节一致，但估计分轨重新生成。旧3060轮存在中断续跑，因此分数差异不能全部归因于GPU；本次也不是精确复现论文表1的裁剪。只计算CLAP、LPAPS、CQT1-PCC。

生成控制器耗时7896.45秒（约2小时12分）。首首15任务新卡146.65秒、旧3060记录443.15秒，约3.02倍，仅为该批实测。

首次评测在导入CLAP时因缺少初始化BERT/BART分词器缓存失败，尚未评分；补齐固定revision缓存后仅恢复评测与审计，未改软件、参数、实际CLAP/RoBERTa权重或音频。原失败状态保留在[history](records/history/evaluation-tokenizer-repair/)，[恢复记录](provenance/evaluation-tokenizer-repair.json)和[恢复脚本](scripts/resume_evaluation_only.sh)可追溯。最终750任务全部有效、无未定义指标。

服务器主副本在`/root/autodl-tmp/polyphonia_repro/results/musdb_center10_htdemucs_4090d_01`。音频、模型、原始数据、环境和RNG二进制不上传GitHub；本目录只归档文本代码、来源、配置、哈希与统计。官方源码仍见上层`upstream/polyphonia/`固定commit快照，脚本为本轮执行版本。原始代码、CLAP与引用代码许可见上层[third_party](../../third_party/AudioEditingCode/)及官方LICENSE。
