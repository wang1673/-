# 运行说明

本目录归档的是已验证的 Featurize 服务器实验。脚本保留实际执行路径；移到其他机器时应调整路径并重建环境。

## 目录

| 内容 | 服务器路径 |
| --- | --- |
| 项目、脚本、日志 | `/home/featurize/work/polyphonia_repro` |
| 官方固定 commit 仓库 | `/home/featurize/work/polyphonia_repro/polyphonia` |
| Python 3.8.20 环境及缓存 | `/home/featurize/data/polyphonia/runtime` |
| 数据集 test | `/home/featurize/data/polyphonia/musdb18hq/test` |
| 估计分轨与中间 10 秒 | `/home/featurize/data/polyphonia/prepared/center10_htdemucs_01` |
| 750 任务输出 | `/home/featurize/work/polyphonia_repro/results/musdb_center10_htdemucs_01` |
| 当前 GitHub 归档副本 | `/home/featurize/work/model-reproductions/polyphonia` |

`data` 是平台实例本地盘；代码和重要记录放在 `work`。这里不包含 SSH 登录材料。

## 查询当前任务

```bash
source /home/featurize/work/polyphonia_repro/scripts/env.sh
python "$POLYPHONIA_ROOT/scripts/status_benchmark.py"
tmux list-sessions
```

当前后台会话：`polyphonia-benchmark`（分轨与生成），`polyphonia-evaluation`（等待全部生成完成后评测）。状态快照上传 GitHub 后不会自动更新。

## 官方样例

```bash
source /home/featurize/work/polyphonia_repro/scripts/env.sh
bash "$POLYPHONIA_ROOT/scripts/run_smoke.sh" smoke_official_02
```

必须使用新 run 名称；已有同名目录时脚本会拒绝覆盖。记录中的首轮样例为 smoke_official_01。

## 批量生成与恢复

`init_benchmark.py` 生成配置；当前 run 已初始化，请勿再次初始化。`prepare_benchmark.py` 对完整混音运行 htdemucs，然后同步裁剪；`benchmark_worker.py` 调用官方入口并验证每个输出。`benchmark_controller.py` 按 50 首顺序执行。

仅在确认生成后台作业已退出后，才能运行以下恢复命令，避免重复进程争用同一输出：

```bash
source /home/featurize/work/polyphonia_repro/scripts/env.sh
bash "$POLYPHONIA_ROOT/scripts/run_benchmark.sh"
```

恢复会复用哈希匹配的预处理文件，重新检查已有音频，隔离损坏文件并补跑缺失任务。随机数是每首 seed 928；若跳过已完成任务后补跑，不能保证与从零连续运行逐字节相同，需要保留恢复记录。

## 评测

已完成 15 任务的 CPU 预检，并对 LPAPS 归约、恒等特征检查通过。首次完整评测会在 750 个任务生成后自动执行。独立运行必须确认 GPU 无生成作业：

```bash
source /home/featurize/work/polyphonia_repro/scripts/env.sh
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
python "$POLYPHONIA_ROOT/scripts/evaluate_benchmark.py" --device cuda
python "$POLYPHONIA_ROOT/scripts/export_benchmark.py"
```

完成后生成 `metrics/summary.json`、`metrics/per_task.csv`、`RESULTS_zh.md`。CLAP 使用论文指定音乐检查点；LPAPS 参考引用代码的四层 Swin 特征归约；CQT 的缺省参数在 specification.json 中明确列出。

FAD 与多项式 MMD² 按显式实现约定补充计算，尚未对齐作者未公开的评测代码。ASB/AMB 需要跨方法归一化，主观 MOS 需要真人评价，本脚本不生成这些分数。

## 环境与来源

推理核心依赖固定为 PyTorch/torchaudio 2.4.1+cu124、torchvision 0.19.1+cu124、diffusers 0.32.0、transformers 4.46.3。额外安装 Demucs 4.0.1、laion-clap 1.1.6、nnAudio 0.3.3 和数据提取所需 PyArrow 15.0.2；pip check 通过。完整列表见 records/environment.freeze.txt。

`install.sh`、`download_torch.py` 等为当时平台的安装辅助，依赖 Featurize 的基础 Conda 与网络镜像，不能视为跨平台通用安装器。模型和数据下载的固定 revision、哈希均保存在 records 和 configs 中；重建时应按这些版本获取，不能静默换成 latest。

## 更新归档

`export_github_snapshot.py` 会在 work 下重新导出允许上传的记录。它不会推送 GitHub，也不会读取 SSH 或令牌文件。后续更新需重新检查快照状态并提交。
