# Polyphonia 复现记录

更新日期：2026-10-26。目标：通过 SSH 先跑通官方样例，再复现论文实验。

## 当前状态

已通过 SSH 登录服务器，在独立 Python 3.8.20 环境中安装官方固定依赖，并成功运行官方 10 秒样例。官方仓库源码未修改。MUSDB18-HQ 前 200 个任务及阶段评测已完成，余下 550 个保持暂停；MusicDelta、其余基线和消融未运行。

服务器实测：RTX 3060 12GB，驱动 580.95.05，PyTorch 2.4.1+cu124，CUDA 运算正常；`pip check` 通过。系统 base/system 环境未修改。PyTorch 三个 wheel 从官方节点下载并按官方索引 SHA-256 验证；其余依赖通过平台预设的清华 PyPI 镜像安装。辅助 requirements 仅移除额外索引选项，所有版本约束保持不变。

### 本次样例结果

- 任务：`vocals2violin`，seed 928，fp16，100 steps，energy mask。
- 新输出：`/home/featurize/work/polyphonia_repro/results/smoke_official_01/`。
- 结果：成功 1 / 失败 0；进程退出码 0。
- WAV：16 kHz，160000 帧，10.0 秒；有限数值、非静音；峰值 0.58643，RMS 0.09801。
- GPU 最大 allocated 10.0236 GiB，最大 reserved 10.3574 GiB。
- 包含模型加载的运行区间 70.70 秒；进程总墙钟时间 74.11 秒，最大 RSS 7329392 KiB。以上不能直接与论文 RTX 3090 上的效率表作同硬件比较。
- 与仓库随附参考输出相比：长度与采样率一致，波形 Pearson 相关系数 0.99961984，RMSE 0.00270332；并非逐字节一致。该比较验证样例重现接近程度，不替代论文语义/保真度评测或人工试听。
- 生成 WAV SHA-256：`eb366531dc0f4c737cd7304ccfe47c48d4bde7eb3a4d7dedc29555a78d174db9`。
- 本地交付：`Polyphonia样例/vocals2violin.wav`、频谱 PNG、`validation.json`。

### 服务器布局与重跑

代码及辅助脚本：`/home/featurize/work/polyphonia_repro/`；环境、模型运行缓存：`/home/featurize/data/polyphonia/runtime/`；数据目录：`/home/featurize/data/polyphonia/`。

模型：`cvssp/audioldm2`，revision `c8e7e189d324425c05c4c2f81214041ef4107983`。运行时使用已缓存的 safetensors，并启用离线模式。

```bash
source /home/featurize/work/polyphonia_repro/scripts/env.sh
bash /home/featurize/work/polyphonia_repro/scripts/run_smoke.sh smoke_official_02
```

每次使用新的 run 名称。辅助脚本会检查输出音频与频谱，并记录 CUDA 峰值；目录已存在则拒绝覆盖。运行环境、模型缓存与预处理数据全部位于 data 下；代码、配置、校验记录、日志及生成结果位于 work 下。旧的 /home/featurize/polyphonia_runtime 已移除。按平台说明，data 是实例本地盘，实例销毁前需要保留必要数据。

数据进展：MUSDB18-HQ test 已下载至 `/home/featurize/data/polyphonia/musdb18hq/test`。50 首、250 WAV、10,999,435,708 bytes，44.1 kHz 双声道，混音总计 3.4642 小时。镜像为 `danjacobellis/musdb18HQ`，revision `7950781147516a3b1411310274175ff98ab8f062`，validation split 对应官方 test。全部文件长度和 CRC32 与官方 ZIP 索引一致，并记录 SHA-256 后重新读取磁盘校验。提示集完整匹配 50 首、750 个任务。未下载训练集，未宣称完成全 ZIP MD5 校验。

### 正在运行的 MUSDB18-HQ 实验

用户明确选择每首中间 10 秒，运行全部 750 个官方任务。run ID：`musdb_center10_htdemucs_01`。

- 分轨：`demucs==4.0.1`，标准公开 `htdemucs` 权重，seed 928、shifts 1、overlap 0.25。输入整首混音，只使用估计分轨。
- 裁剪：起点 `floor((原始帧数 - 441000)/2)`，原始 44.1 kHz 下保留 441000 帧；混音及估计分轨时间完全一致。
- 编辑：未修改的官方源码，100 steps、CFG 3.5、mask bias 2.5、fp16、seed 928、energy mask、全部 down 层。辅助 wrapper 仅增加输出检查与进度记录。
- 差异：作者未公开准确裁剪清单和分离模型哈希；官方 energy mask 的分母与论文公式存在差异。本次保留代码基线，明确记录假设，不宣称精确重现表 1。
- 首首 `AM Contra - Heart Peripheral` 的 15 个任务全部成功；进程 443.15 秒，峰值 CUDA allocated 10.0234 GiB。仅该首预检均值：CLAP 0.328378、LPAPS 4.839647、CQT1-PCC 0.177948，不能代表全量最终结果。
- 评测模型为论文指定的 `music_audioset_epoch_15_esc_90.14.pt`（HTSAT-base），SHA-256 `fae3e9c087f2909c28a09dc31c8dfcdacbc42ba44c70e972b58c1bd1caf6dedd`。LPAPS 归约对齐引用的 DDPM 音频编辑代码，已用真实 Swin 特征与上游实现比较通过；恒等 LPAPS、CQT1-PCC、CLAP 自余弦检查通过。CQT2010 使用 16 kHz、128 bins、24 bins/octave，其余默认值写入 specification.json。
- 生成后自动计算 CLAP、LPAPS、CQT1-PCC，导出 CSV 和汇总。FAD/多项式 MMD² 仅按明确实现约定补充计算，尚未与作者评测代码核对。ASB/AMB 需跨方法归一化，MOS 需真人评价，本次未生成这些分数。

服务器结果根目录：`/home/featurize/work/polyphonia_repro/results/musdb_center10_htdemucs_01/`。其中 `protocol.json` 保存配置与全部裁剪起点，`audio/` 保存生成 WAV，`status.json` 保存生成进度，`pipeline.json` 保存评测状态。全部完成后生成 `metrics/summary.json`、`metrics/per_task.csv` 和 `RESULTS_zh.md`。

查看实时状态：

```bash
source /home/featurize/work/polyphonia_repro/scripts/env.sh
python /home/featurize/work/polyphonia_repro/scripts/status_benchmark.py
```

后台会话为 `polyphonia-benchmark` 和 `polyphonia-evaluation`。SSH 断开后继续运行；实例停止或销毁会中止计算。失败会记录错误并停止，恢复时可复用重新验证通过的输出。


- 论文：https://arxiv.org/html/2605.10203v1
- 官方仓库：https://github.com/Ltx-Leif/polyphonia
- 本次核查 main 提交：`26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc`

## 已核对的运行配置

| 项目 | 官方代码/论文设置 |
| --- | --- |
| Conda Python | README 推荐 3.8.20 |
| PyTorch / torchaudio | 2.4.1+cu124 |
| torchvision | 0.19.1+cu124 |
| diffusers | 0.32.0 |
| transformers | 4.46.3 |
| 模型加载路径 | `my_audioldm2.py` 使用 `cvssp/audioldm2` |
| 编辑参数 | 100 steps，CFG 3.5，mask_bias_strength 2.5，t_start 1000 |
| 注意力层 | 样例配置 self/cross down 1–18，up/mid 为空 |
| 样例随机种子 | 928 |
| 频谱处理 | 16 kHz，FFT/window 1024，hop 160，64 Mel bins |

PyTorch CUDA 构建需结合服务器 GPU 架构与驱动检查；不能仅凭本地 CUDA Toolkit 版本决定是否可用。

## 影响复现的源码细节

1. `sample/` 已包含 mixture、四个分轨、prompt，以及官方输出。脚本发现输出 WAV 已存在且大于 1024 bytes 会跳过该任务。首次验证必须使用新的输出目录。
2. `generate_soft_masks()` 从磁盘读取分轨，不会自动运行 Demucs。论文主实验使用 HT-Demucs 估计分轨；样例中已有分轨的来源不能仅凭文件名判断。正式实验需记录分轨来源，不能把真实分轨和估计分轨混用。
3. 默认 `energy` 掩码实际计算 `sqrt(Mel(|S_k|²) / (Mel(|X|²) + eps))` 并截断到 [0,1]。应保留该设置作为官方代码基线。
4. `Original Prompt` 存于 JSON，但样例反演实际传入空提示；生成使用 `Baseline Prompt` 和各分轨提示。不要擅自把反演提示替换为原始描述。
5. 任务键通过 vocals2、drums2、bass2 判断目标，其他键默认映射到 other。Softmask 提示短语应与目标完整提示的措辞对齐。
6. 多处异常会记录日志后直接返回，进程退出码可能仍为 0；音频保存函数也会吞掉异常。需同时检查成功/失败计数、文件是否新增、音频长度、有限数值与是否静音。
7. 反演中自注意力 Q/K 会保留在设备上，其他缓存有 CPU 存储。显存、内存与运行耗时以服务器实测为准，不能直接把论文效率表视为当前提交的保证。
8. 仓库提供样例编辑入口与 PolyEvalPrompts，但当前树中未发现完整批量评测、基线、消融入口。完整实验需要补充可追踪的运行与评测脚本。

## 阶段一：服务器与官方样例

连接后先检查系统、GPU/驱动、可用显存、Conda/Python、磁盘、GitHub 和 Hugging Face 连通性，再创建独立环境。保留原有项目与环境。记录 Git commit、模型 revision、依赖快照、命令、随机种子与日志。

环境安装成功后的样例命令（在仓库根目录执行；输出目录必须是本次新建目录）：

```bash
MPLBACKEND=Agg python run_sample_exp.py \
  --sample_dir ./sample \
  --output_dir ./runs/smoke_20261026_01 \
  --task_key vocals2violin \
  --device cuda \
  --precision fp16 \
  --seed 928 \
  --mask_type energy \
  --visualize
```

验收：日志报告成功 1 / 失败 0，确实生成本次 WAV/PNG；检查 WAV 采样率、时长、数值、峰值及试听，并记录峰值显存、内存与耗时。若需要修复，保存原始基线和差异。

## 阶段二：论文实验

论文使用 MUSDB18-HQ test 和 MusicDelta，PolyEvalPrompts 共 1170 个任务。音频需另行准备，不能把提示文件视为已包含数据集。

先用小批量核验音频与提示映射、裁剪策略、HT-Demucs 分轨、掩码及输出，再扩展批量。裁剪位置、长度、分离模型权重及具体评测实现须逐项确认和记录；未明确的项目作为复现假设标注。

指标包括 CLAP、CQT1-PCC、LPAPS、FAD、KAD、ASB、AMB；主观 MOS 需要另行组织。CLAP 与 LPAPS 的模型、特征提取方式应按论文附录 J 对齐。ASB/AMB 需核对跨方法归一化口径，不应对单个样例任意归一化后宣称复现论文结果。

最终输出应包括：环境与版本、数据与裁剪清单、全部任务状态、原音频与生成音频、逐任务指标与汇总、与论文表格差异，以及所有代码修改和未确定因素。

## 2026-10-26：先检查前 200 个任务

用户将当前阶段上限改为 200。配置保存在实验目录 `control.json`，整体 750 任务及裁剪清单不变。严格按原顺序选择前 13 首的全部任务（195 个），加第 14 首 Forkupines - Semantics 的前 5 个任务。200 个有效输出后，生成状态变为 paused_at_task_limit；不会继续生成第 201–750 个任务。

已将等待全量评测的流程改为阶段评测：生成到 200 后计算这 200 个结果的 CLAP、LPAPS、CQT1-PCC，保存 `metrics/summary.first200.json`、`metrics/per_task.first200.csv`、`RESULTS_first200_zh.md`，并生成 `review_first200/` 的原混音/编辑音频对比。阶段选择是顺序子集，不代表完整数据集的最终指标。

控制器交接时一次尚未保存的生成被中断；70 个已通过检查的输出保留并重新验证，缺失任务已续跑。此前任务没有保存完整随机流状态，因此不能保证这次断点续跑与不中断运行逐字节相同；从此次更新起，每个成功任务后保存 Python、NumPy、PyTorch CPU/CUDA 随机状态，在合适的断点恢复。旧版脚本和状态保存在 run/revisions/before-limit200 与 status.before_limit200.json。

剩余 550 个任务需用户之后明确继续时再恢复，不会由本阶段自动启动。

## 前 200 个任务：已完成的阶段结果

实际生成并验证 200 个 WAV，完成 200 行客观评测：前 13 首各 15 个任务，加第 14 首的前 5 个任务。生成状态为 paused_at_task_limit，流水线状态为 stage_completed_remaining_paused，控制器退出码 0，GPU 已空闲。未发现第 201 个以后的生成输出。

| 指标 | 均值 | 总体标准差 | 有效 / 未定义 |
| --- | ---: | ---: | ---: |
| CLAP ↑ | 0.366880 | 0.079560 | 200 / 0 |
| LPAPS ↓ | 4.785495 | 0.465056 | 200 / 0 |
| CQT1-PCC ↑ | 0.312406 | 0.216796 | 200 / 0 |

最终失败任务数为 0，但控制器交接时中断过一次未保存的生成，已续跑；不能称所有尝试都从未中断。200 个 WAV 的 SHA-256 与生成及评测记录一致，均为 16 kHz 单声道、10 秒、有限且非静音；CSV 与 JSON 数值一致，均值及标准差独立重算通过。8 组试听对的源音频和编辑音频哈希也通过校验。详见 stage200.audit.json。

配置为每首中间 10 秒、整首混音经 HT-Demucs 估计分轨、100 steps、CFG 3.5、mask bias 2.5、fp16、seed 928。裁剪、分离权重、评测默认参数、官方掩码代码与论文公式差异以及中途随机流变化仍是复现限制。这是顺序选取的 200 任务子集，不代表全部 750 个任务，不能宣称精确重现论文表 1；尚未做人工试听或 MOS。

服务器结果目录内的 RESULTS_first200_zh.md、metrics/summary.first200.json、metrics/per_task.first200.csv 和 review_first200/ 已生成。本机仅下载阶段报告、指标、校验记录和 8 组短试听对，不下载完整数据集。剩余 550 个任务及恢复点继续保留。


## 2026-10-27：新服务器RTX4090 D完整750任务

用户将旧200上限明确改为全750。原服务器不可用，授权重部署；目标最终改至RTX4090 D，前一2080Ti实例的下载和等待进程停止，未在那里生成。50首全长混音SHA与旧记录一致，原前200涉及的14首混音裁剪一致，估计分轨在新GPU重新生成。107项环境及官方源码、模型哈希核对通过。

750个新WAV与原三指标全部完成，最终审计通过；均值/总体标准差为CLAP 0.3503757368971904/0.08190163749915376，LPAPS 4.67899129152298/0.48950218590868355，CQT1-PCC 0.3334732335597876/0.23045329872748305，均750有效、0未定义。分轨与生成7896.45秒。生成未中断；首次评测因CLAP导入初始化分词器缓存缺失失败，补齐缓存后只恢复评测和校验，原失败保留。

完整事实记录、逐任务CSV、状态、协议、依赖、来源哈希、实际脚本与修复证据见[runs/2026-10-27-4090d-750/](runs/2026-10-27-4090d-750/)。这是本轮全部750任务结果，不覆盖旧200历史，也不是纯GPU因果或精确论文裁剪复现。
