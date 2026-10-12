# 音乐与音频编辑论文精读

本仓库收录十篇 flow/diffusion 音频或音乐编辑论文的中文精读、代码树注解和论文章节/源码对应关系。精读文档区分论文报告、代码观察与研究建议；没有公开算法实现的论文明确说明，不以伪代码代替源码。

| 顺序 | 论文 | 年份 / venue | 精读 | 代码树与论文对应 | 官方代码情况 |
|---|---|---|---|---|---|
| 1 | MelodyFlow | 2024 | [完整精读](melodyflow/完整精读.md) | [代码树](melodyflow/代码树.md) · [源码定位](melodyflow/代码原文对应.md) · [逐行详注](melodyflow/代码精读详注.md) | [官方模型与推理](https://huggingface.co/spaces/facebook/MelodyFlow) |
| 2 | FlowEdit | ICCV 2025 | [完整精读](flowedit/完整精读.md) | [代码树](flowedit/代码树.md) · [源码定位](flowedit/代码原文对应.md) · [逐行详注](flowedit/代码精读详注.md) | [fallenshock/FlowEdit](https://github.com/fallenshock/FlowEdit) |
| 3 | DirectAudioEdit | 2026 | [完整精读](directaudioedit/完整精读.md) | [代码树](directaudioedit/代码树.md) · [源码定位](directaudioedit/代码原文对应.md) · [逐行详注](directaudioedit/代码精读详注.md) | [NiuTrans/DirectAudioEdit](https://github.com/NiuTrans/DirectAudioEdit) |
| 4 | EchoEdit / EchoEdit+ | 2026 | [完整精读](echoedit/完整精读.md) | [代码状态](echoedit/代码树.md) · [原文对应](echoedit/代码原文对应.md) | 截至 2026-10-12，论文称代码将发布，未核验到官方实现 |
| 5 | Melodia | AAAI 2026 | [完整精读](melodia-aaai2026/完整精读.md) | [代码树](melodia-aaai2026/代码树.md) · [源码定位](melodia-aaai2026/代码原文对应.md) | [官方仓库](https://github.com/YiYang-SCUT/Melodia)，固定提交未含编辑算法实现 |
| 6 | SteerMusic | AAAI 2026 | [完整精读](steermusic-aaai2026/完整精读.md) | [代码树](steermusic-aaai2026/代码树.md) · [源码定位](steermusic-aaai2026/代码原文对应.md) · [逐行详注](steermusic-aaai2026/代码精读详注.md) | [sony/steermusic](https://github.com/sony/steermusic) |
| 7 | Virtual Consistency | 2025 | [完整精读](virtual-consistency/完整精读.md) | [代码树](virtual-consistency/代码树.md) · [源码定位](virtual-consistency/代码原文对应.md) · [逐行详注](virtual-consistency/代码精读详注.md) | [VCI_Editing](https://github.com/matthieu-cervera/VCI_Editing) |
| 8 | FlowAlign | 2025 | [完整精读](flowalign/完整精读.md) | [代码树](flowalign/代码树.md) · [源码定位](flowalign/代码原文对应.md) · [逐行详注](flowalign/代码精读详注.md) | [FlowAlign/FlowAlign](https://github.com/FlowAlign/FlowAlign) |
| 9 | FreeSonic | 2026 | [完整精读](freesonic/完整精读.md) | [代码状态](freesonic/代码树.md) · [原文对应](freesonic/代码原文对应.md) | 项目页公开；截至 2026-10-12 未核验到官方算法代码 |
| 10 | MusicMagus | IJCAI 2024 | [完整精读](musicmagus/完整精读.md) | [代码树](musicmagus/代码树.md) · [源码定位](musicmagus/代码原文对应.md) · [逐行详注](musicmagus/代码精读详注.md) | [ldzhangyx/MusicMagus](https://github.com/ldzhangyx/MusicMagus) |

有官方算法源码的七篇本次又为 21 个关键文件增加了 187 条中文行内注释，并补上逐步状态、公式、数字例子及原始行号索引；源码 AST 与原版一致，原始行号映射也逐项核验。

每篇目录还包括 arXiv 元数据、章节与公式定位、论文 LaTeX 源、抽取文本、讲解关键图、源码快照和中文注释版（若有官方代码）、代码许可证与行号映射。论文 PDF 可从每篇精读稿所链接的 arXiv 页面获取；原始 PDF 未重复镜像进本仓库。

方法脉络：FlowEdit 用源/目标速度差构造直接编辑 ODE；DirectAudioEdit 与 EchoEdit 将这种思路带到真实音频；Melodia、SteerMusic 与 MusicMagus关注结构/旋律保留；Virtual Consistency、FlowAlign 和 FreeSonic 分别从采样一致性、轨迹约束与时间/注意力控制补齐编辑能力。

另有早期专题对比：[五篇论文的统一对比与阅读建议](五篇论文对比.md)。
