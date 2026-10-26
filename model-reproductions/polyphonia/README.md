# Polyphonia 复现

论文：[Polyphonia](https://arxiv.org/abs/2605.10203) · [官方代码](https://github.com/Ltx-Leif/polyphonia)

固定官方 commit：`26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc`。

## 当前结果：前 200 个任务已完成

MUSDB18-HQ test 的顺序前 **200/750** 个任务已生成并完成阶段评测：前 13 首各 15 个，加第 14 首的前 5 个任务。剩余 **550 个保持暂停**；没有第 201 个以后的生成输出。官方样例此前已成功。

| 指标 | 均值 | 总体标准差 | 有效 / 未定义 |
| --- | ---: | ---: | ---: |
| CLAP ↑ | 0.366880 | 0.079560 | 200 / 0 |
| LPAPS ↓ | 4.785495 | 0.465056 | 200 / 0 |
| CQT1-PCC ↑ | 0.312406 | 0.216796 | 200 / 0 |

200 个 WAV 的格式、长度、数值及 SHA-256 与记录匹配，逐任务 CSV 与 JSON 一致，均值/标准差独立重算通过。最终失败任务数 0；控制器切换时一次未保存生成被中断后已续跑，不能说所有尝试均未中断。详见 [独立校验](records/stage200.audit.json)。

每首取中间 10 秒，整首混音经 HT-Demucs 估计分轨，100 steps、CFG 3.5、mask bias 2.5、fp16、seed 928。这是明确假设的阶段性复现，不代表 750 个任务的最终表现，也不能宣称精确重现论文表 1。作者未公开准确裁剪清单，分离模型的确切权重、部分指标细节及官方掩码与论文公式差异均见记录。控制器切换时的随机流变化已保留说明；未做人工试听或 MOS。MusicDelta、其他基线、消融未运行。

## 文件入口

- [阶段结果与8组试听索引](STAGE200_RESULTS.md)；音频保留在服务器和本机，公开仓库只含索引。
- [完整复现记录](REPRODUCTION_LOG.md) · [运行与恢复说明](RUNBOOK.md)。
- [200任务逐项CSV](records/metrics/per_task.first200.csv) · [精确汇总](records/metrics/summary.first200.json) · [评测约定](records/metrics/specification.json)。
- [配置及全部750任务裁剪清单](configs/protocol.json) · [当前200任务上限](configs/control.json) · [交接记录](configs/limit200-change.json)。
- [生成状态](records/snapshot-status.json) · [评测状态](records/snapshot-pipeline.json) · [归档信息](SNAPSHOT.json)。汇总JSON中的 `state: partial` 表示仅评测全部750任务中的200个；本阶段确已完成。
- [数据审核](records/musdb18hq.audit.json) · [逐文件哈希](records/musdb18hq.manifest.json) · [依赖](records/environment.freeze.txt)。
- [官方样例验证](records/official-sample/validation.json) · [参考输出比较](records/official-sample/reference_comparison.json) · [历史首首15任务评测](records/metrics/first-track.summary.json)。
- [模型版本](records/model.snapshot.json) · [Demucs哈希](records/demucs-model.json) · [评测权重](records/evaluation-model.json) · [评测实现核验](records/metric-verification.json)。

`scripts/` 为辅助脚本，`upstream/polyphonia/` 为固定 commit 的官方源码。`configs/scripts.sha256.json` 为较早运行记录，当前辅助脚本哈希见 `records/scripts-at-stage200.sha256.json`。

最初40任务时的快照见历史 commit `37c8a7677165f1a051076ccb0c2c1d44fd88056f` 与 [snapshot40.json](records/history/snapshot40.json)；这里的当前记录已更新为200任务阶段完成。

数据集、音频、大型权重、二进制环境、缓存、SSH密钥和凭据不在本仓库。原始代码保留 [MIT许可证](upstream/polyphonia/LICENSE)；LPAPS引用及CLAP权重许可见 [third_party](third_party/AudioEditingCode/) 和 SNAPSHOT.json。
