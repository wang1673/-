# 10首数据集音乐 × 15项编辑示例


## 完整试听包下载

[下载完整试听包（约170 MiB）](https://github.com/wang1673/-/releases/download/polyphonia-10tracks-150-demos-20261102/polyphonia-10tracks-150-listening-20261102.tar.gz) · [GitHub Release](https://github.com/wang1673/-/releases/tag/polyphonia-10tracks-150-demos-20261102)

附件：`polyphonia-10tracks-150-listening-20261102.tar.gz`，178,738,249 bytes。

SHA-256：`5601f16075bb4c972055de0f66d0b09c831cf469d90b5e667f584bc9082cfb60`（已与GitHub附件digest核对一致）。

解压后打开 `Polyphonia_10首150项编辑对照/10首音乐试听对照.html`，保留整个目录和音频子目录。Release附件为完整音频包；下方代码/文本目录仍只保存记录、脚本和统计。

2026-11-02完成MUSDB18-HQ test原protocol前10首，共150项。每首只运行原中间10秒，不是整首推理。首首15项保留本聊天前一次新示例，其余9首新跑135项；没有复用旧750生成音频。

官方Polyphonia代码与固定AudioLDM2模型，原100steps/CFG3.5/maskbias2.5/fp16/seed928/energy/down层配置。150项音频、三指标和最终校验通过。

| 指标 | 均值 | 总体标准差 |
| --- | ---: | ---: |
| 原音对目标CLAP | 0.157981605 | 0.094639092 |
| 编辑后对目标CLAP | 0.353303259 | 0.081686869 |
| LPAPS | 4.824715422 | 0.490381729 |
| CQT1-PCC | 0.304219090 | 0.221274444 |

[实验记录](records/EXPERIMENT_RECORD.md) · [完整JSON](records/EXPERIMENT_RECORD.json) · [150项逐任务CSV](records/per_task.csv) · [最终校验](records/final.audit.json) · [选曲和裁剪](records/selected-protocol.json) · [脚本](scripts/)

按协议顺序预先选曲，全部结果保留，没有挑选听感最好案例。本次是原音与编辑后对照，没有其他方法基线或真人TTA/CTI/GAC评分；正CLAP变化不能代替听感结论。保留官方infer_edit_stem的任务名匹配行为，包括bass_guitar2默认other的异常，详见JSON。原750实验未改变。

服务器主副本：`/root/autodl-tmp/polyphonia_repro/demos/2026-11-02-ten-tracks`。完整本地试听包包含10首音乐试听对照.html、10个曲目页和全部150项音频。此GitHub目录保存文本记录、脚本、提示词、指标和哈希；不包含音频、数据集、模型或环境，故不提供缺失音频的空白试听页面。
