# 六篇论文：音乐编辑中的 training-free 与 zero-shot

日期：2026-10-27。范围：来源分析，不是独立实验、系统综述或创新方案。

## 分类规则

- **编辑无权重训练**：编辑阶段不更新骨干权重；允许模型本身事先训练。
- **无逐样本梯度拟合**：输入样本上不运行embedding、latent或prediction的梯度优化。需与前项分开。
- **免反演**：不显式求取源信号的生成噪声/轨迹；不代表没有VAE编码、加噪、迭代或多次前向。
- **zero-shot**：本批文献主要指不以编辑配对数据训练/微调新编辑器；不是已验证的未见过音乐风格、未见过曲目或无任何训练数据。
- 表格的“DE”指已核对论文/代码内容；并非本次独立验证了音乐效果。

## 方法定位

| 方法 | 编辑更新权重 | 逐输入优化/额外计算 | 显式反演 | 原论文音乐证据 | 对本课题的作用 |
|---|---|---|---|---|---|
| DirectAudioEdit | 无 | 核心路径无梯度拟合；双分支前向 | 无 | MedleyMDPrompts前10秒，5 seeds | 免反演扩散主线 |
| AudioMorphix | 无新增编辑训练 | 潜变量SGD、能量梯度、KV缓存 | 有 | 主要AudioSet-E事件；音高/时间操作主要定性 | 参考音频+局部时频编辑 |
| AudioEditor | 无 | null embedding Adam、条件embedding梯度 | 有 | 300段AudioCaps事件，非音乐专项 | 含测试时优化的文本控制对照 |
| MelodyFlow | 编辑时无；骨干与codec经过训练 | 正则化反演重复预测、KL梯度更新 | 有 | 音乐专项、48kHz立体声/30秒骨干 | 高保真音乐FM参照 |
| DDPM Inversion / ZETA | 无 | ZETA不逐样本拟合；同文ZEUS另有PC迭代 | 有 | MusicDelta/MedleyMDPrompts、偏好听测 | 核心音乐zero-shot扩散基线 |
| EdiTTS | 无新增训练 | 无任务特定优化；1000步双轨采样 | 不是ZETA式真实音乐反演 | 仅语音LJ Speech | 先验扰动和边界软化的机制参考 |

以上均依赖已训练的生成先验。没有一篇能被解释为“整个系统从未训练过”。

## 对你的方向，哪些结论目前站得住

1. **若你要求既不更新权重，也不做逐样本梯度拟合**：DirectAudioEdit和ZETA最直接；ZEUS仍需记录PC计算成本。EdiTTS符合局部无任务优化的机制定义，但缺少音乐证据，不能直接纳入音乐排行榜。
2. **若允许测试时优化，只排除模型微调**：AudioMorphix、AudioEditor、MelodyFlow正则化编辑都可纳入，但需单独报告优化对象、迭代数、耗时、显存和是否反传网络。
3. **研究局部乐器/声部编辑时**：AudioMorphix的时频操作和ZETA的mask外回拉值得读；一个时频格点不只属于一个乐器，因此mask不能代替声源分离证据。
4. **研究音乐FM时**：MelodyFlow是直接相关的已训练骨干与正则反演参照；整篇包含训练贡献，不妨碍其编辑过程作为冻结骨干方法使用。
5. **严格音符、半音、节拍、和弦保持**：六篇现有结果不足以统一证明这些能力。EdiTTS明确不能指定精确移调量；其他聚合分布指标也不能替代音乐结构验证。

这些是AI分类判断，依据各篇笔记中的DE/SC；不是已完成Mode C机制矩阵或新颖性判断。

## 必须保留的证据边界

| 事项 | 核对结果 | 来源定位 |
|---|---|---|
| DirectAudioEdit音乐结果 | 两骨干音乐FAD/KL/SSIM均值更好；AudioLDM2音乐FAD相对DDPM并非显著 | [笔记](notes/directaudioedit.md)，PDF pp.6,12 Tables1,5,6 |
| DirectAudioEdit64.5% | 相对DDPM、特定AudioLDM2设置的耗时降低，不是相对全部方法 | PDF p.7 Fig3及fig/cost.tex |
| DirectAudioEdit公开默认 | cfg_tar=[8]固定；论文8→12要显式设置 | main_run.py L448–475 |
| AudioMorphix局部性 | 定量比较未给本法mask；音高/时移/拉伸主要定性 | [笔记](notes/audiomorphix.md)，PDF p.7、p.11 AppendixB |
| AudioEditor“无需训练” | 仍有两种embedding优化 | [笔记](notes/audioeditor.md)，PDF pp.2–3；NullInversion L129–161 |
| AudioEditor公式 | 论文Eq5正指数与代码负指数不一致，未自行消除该冲突 | wo_utils.py L23–35；PDF p.3 |
| MelodyFlow一致性 | Table1的CON并未优于AudioLDM2-music | [笔记](notes/melodyflow.md)，PDF p.6 Table1 |
| MelodyFlow版本 | 论文20k小时，公开卡16k小时且明确公开版用HT-Demucs处理数据、指标不同；代码有默认sway调度 | PDF p.5,14；官方HF模型卡、flow.py |
| ZETA vs ZEUS | 同一论文的文本编辑和无监督主方向编辑；不可混用效果/计算量 | [笔记](notes/zeta.md)，PDF pp.4–5,15 |
| ZETA局部“泄漏” | 指编辑影响mask外，不是训练测试数据污染；软回拉非波形严格不变 | PDF p.17 AppendixD Fig14 |
| EdiTTS领域 | 语音和文本先验；未验证任意音乐波形或多声部编辑 | [笔记](notes/editts.md)，PDF pp.2–4；tts.py |

## 为什么不把六篇的FAD数字直接排序

它们的音频来源、长度、骨干、声道、目标分布与特征提取不同。例如ZETA用CLAP特征评估音乐FAD，而MelodyFlow明确采用VGGish FAD并将立体声自动评价下混。AudioEditor还使用目标文本重生成作为一类参照。跨论文数值差异不能直接归因于编辑算法。

真正可比较的证据是相同论文内已明确固定骨干/数据/评价协议的对照；跨骨干对比应保留混杂说明。

## 下一阶段的输入

[合并ANALYSIS_PACKAGE](ANALYSIS_PACKAGES.json)含6个独立包，所有P/F均为候选，不是最终研究空白。

可要求deep-read Mode C围绕以下已有问题组织证据，而不是立即生成新方案：

- 哪些保留约束在多声部音乐中有直接证据，哪些只有图示或一般声音实验？
- 哪些改进来自反演/采样控制，哪些与骨干或codec改变混杂？
- 允许梯度优化与不允许梯度优化的路线，各自的质量—成本边界是什么？
