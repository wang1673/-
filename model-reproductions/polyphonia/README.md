# Polyphonia 复现

论文：[Polyphonia: Zero-Shot Timbre Transfer in Polyphonic Music with Acoustic-Informed Attention Calibration](https://arxiv.org/abs/2605.10203)

官方代码：[Ltx-Leif/polyphonia](https://github.com/Ltx-Leif/polyphonia)，固定 commit `26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc`。

## 当前状态

官方 10 秒样例已成功运行。MUSDB18-HQ test 的 50 首歌曲、250 个 WAV 全部通过大小、CRC32、SHA-256 重读和音频格式检查，官方提示集对应 750 个任务。

**本次归档是运行中的快照：已验证 40/750 个任务、完成 2/50 首。** 准确采集时间见 [SNAPSHOT.json](SNAPSHOT.json)。服务器继续运行不代表 GitHub 文件会自动更新。

经用户确认，每首取中间 10 秒；先对整首混音运行 HT-Demucs，再对估计分轨和混音同步裁剪。作者未公开准确裁剪清单，故这是明确记录假设的复现，不能宣称精确重现论文表 1。MusicDelta、其他方法基线、消融及真人 MOS 尚未运行。

## 阅读入口

- [完整复现记录](REPRODUCTION_LOG.md)：环境、官方样例、数据、实现差异、阶段结果。
- [运行说明](RUNBOOK.md)：当前服务器目录、查询、恢复和评测。
- [实验配置与全部裁剪起点](configs/protocol.json)。
- [数据检查](records/musdb18hq.audit.json)与[逐文件哈希清单](records/musdb18hq.manifest.json)。
- [官方样例验证](records/official-sample/validation.json)与[参考输出比较](records/official-sample/reference_comparison.json)。
- [首首 15 个任务评测](records/metrics/first-track.summary.json)：局部预检，不能代表全量均值。
- [评测实现约定](records/metrics/specification.json)与[实现核验](records/metric-verification.json)。
- [生成进度快照](records/snapshot-status.json)与[后续评测状态](records/snapshot-pipeline.json)。
- [环境依赖](records/environment.freeze.txt)、[编辑模型版本](records/model.snapshot.json)、[Demucs 哈希](records/demucs-model.json)、[评测模型版本](records/evaluation-model.json)。

## 文件范围

`scripts/` 保存本次使用的辅助脚本；`upstream/polyphonia/` 保存固定 commit 的官方 Python 源码和 MIT 许可证。官方提示集及样例音频需从原仓库的上述 commit 获取。`records/logs/` 保存已完成歌曲的日志，已去掉逐步进度条。

SSH 密钥、凭据、数据集、派生音频、大型模型权重和二进制环境不在本仓库。它们位于已授权的服务器 `data`/`work` 目录，仓库保留校验与来源信息。

原始源码遵循 [官方 MIT 许可证](upstream/polyphonia/LICENSE)。LPAPS 参考代码及 CLAP 权重的来源、commit 与许可见 [third_party](third_party/AudioEditingCode/) 和 SNAPSHOT.json。下载数据或权重时仍需遵守各自许可。
