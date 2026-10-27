# Polyphonia 复现

论文：[Polyphonia](https://arxiv.org/abs/2605.10203) · [官方代码](https://github.com/Ltx-Leif/polyphonia)

固定官方commit：`26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc`。

## 当前结果：RTX 4090 D 全750任务完成

2026-10-27按原protocol的50首×15任务从头运行，750个生成音频、CLAP/LPAPS/CQT1-PCC和最终审计全部通过。

| 指标 | 均值 | 总体标准差 | 有效/未定义 |
| --- | ---: | ---: | ---: |
| CLAP | 0.350376 | 0.081902 | 750/0 |
| LPAPS | 4.678991 | 0.489502 | 750/0 |
| CQT1-PCC | 0.333473 | 0.230453 | 750/0 |

[全750任务目录](runs/2026-10-27-4090d-750/) · [完整实验记录](runs/2026-10-27-4090d-750/records/EXPERIMENT_RECORD.md) · [逐任务CSV](runs/2026-10-27-4090d-750/records/metrics/per_task.csv) · [精确汇总](runs/2026-10-27-4090d-750/records/metrics/summary.json) · [最终校验](runs/2026-10-27-4090d-750/records/full750.audit.json)

原服务器不可用，按用户授权重新部署；50首全长源混音SHA与旧实验一致，旧前200任务涉及的14首混音裁剪也一致，HT-Demucs估计分轨重新生成。旧轮另有中断续跑，不能把指标差异全部归因于GPU。每首中间10秒是本次约定，不能宣称精确复现论文表1。参数与原三项评测保持，未做人工试听或MOS；未运行MusicDelta、其他基线和消融。

首次评测的导入缓存缺失已修复，完整失败与恢复记录保留在新轮目录。分轨与生成约2小时12分；首首15任务约比旧3060快3倍，仅为该批实测。

## 历史与复现入口

- [运行说明](RUNBOOK.md) · [追加复现日志](REPRODUCTION_LOG.md) · [当前归档信息](SNAPSHOT.json)。
- [旧RTX3060前200任务](STAGE200_RESULTS.md) · [原200任务首页](records/history/README.stage200.md) · [原200归档元数据](records/history/snapshot200.json)。这些历史文件保留原值，不代表新750均值。
- 顶层`configs/`、`scripts/`和原`records/`仍是旧Featurize阶段的历史版本；新轮权威配置、运行脚本和结果均位于`runs/2026-10-27-4090d-750/`。
- [固定官方源码](upstream/polyphonia/) · [许可证与引用](third_party/AudioEditingCode/)。

仓库只保存文本来源、代码、配置、日志、哈希和统计，不包含音频、数据集、模型权重、环境缓存、RNG二进制、SSH连接材料或凭据。
