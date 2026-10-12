# 音乐与音频编辑论文精读

本仓库收录十篇 flow/diffusion 音频或音乐编辑论文的中文精读、代码树注解和论文章节/源码对应关系。精读文档标注论文事实、代码观察与研究建议；代码树对没有公开代码的论文明确标注为“无官方代码”，不把伪代码当作真实实现。

| 顺序 | 论文 | 年份 / venue | 精读 | 代码树 | 原文对应 |
|---|---|---|---|---|---|
| 1 | MelodyFlow | 2024 | [完整精读](melodyflow/完整精读.md) | [代码树](melodyflow/代码树.md) | [源码对应](melodyflow/代码原文对应.md) |
| 2 | FlowEdit | ICCV 2025 | [完整精读](flowedit/完整精读.md) | [代码树](flowedit/代码树.md) | [源码对应](flowedit/代码原文对应.md) |
| 3 | DirectAudioEdit | 2026 | [完整精读](directaudioedit/完整精读.md) | [代码树](directaudioedit/代码树.md) | [源码对应](directaudioedit/代码原文对应.md) |
| 4 | EchoEdit / EchoEdit+ | 2026 | [完整精读](echoedit/完整精读.md) | [代码树](echoedit/代码树.md) | [源码对应](echoedit/代码原文对应.md) |
| 5 | Melodia | AAAI 2026 | [完整精读](melodia-aaai2026/完整精读.md) | [代码树](melodia-aaai2026/代码树.md) | [源码对应](melodia-aaai2026/代码原文对应.md) |
| 6 | SteerMusic | AAAI 2026 | [完整精读](steermusic-aaai2026/完整精读.md) | [代码树](steermusic-aaai2026/代码树.md) | [源码对应](steermusic-aaai2026/代码原文对应.md) |
| 7 | Virtual Consistency | 2025 | [完整精读](virtual-consistency/完整精读.md) | [代码树](virtual-consistency/代码树.md) | [源码对应](virtual-consistency/代码原文对应.md) |
| 8 | FlowAlign | 2025 | [完整精读](flowalign/完整精读.md) | [代码树](flowalign/代码树.md) | [源码对应](flowalign/代码原文对应.md) |
| 9 | FreeSonic | 2026 | [完整精读](freesonic/完整精读.md) | [代码树](freesonic/代码树.md) | [源码对应](freesonic/代码原文对应.md) |
| 10 | MusicMagus | IJCAI 2024 | [完整精读](musicmagus/完整精读.md) | [代码树](musicmagus/代码树.md) | [源码对应](musicmagus/代码原文对应.md) |

精读内容按动机、架构、训练、数据、信息流、数字例子与源码讲解组织；另有实验与局限总结。每篇链接至原论文及作者公开代码仓库。主要方法脉络：FlowEdit 用源/目标速度差构造直接编辑 ODE；音频方法进一步讨论共享噪声、轨迹耦合、注意力/时间定位与音乐结构保持。
