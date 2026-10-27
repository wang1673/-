# 音乐编辑科研工作流：六篇论文分析

2026-10-27 · analyze-paper · research-pipeline-contract v1.0

研究方向：音乐音频编辑，重点关注training-free、zero-shot及无新增编辑训练的方法。

本目录是一次新的、版本固定的来源分析。仓库原有papers/directaudioedit、papers/melodyflow等材料保留，不覆盖，也不把旧笔记当作新的直接证据。

## 从这里开始

- [六篇方法的定义、比较与证据边界](outputs/comparison.md)
- [6个ANALYSIS_PACKAGE合并包](outputs/ANALYSIS_PACKAGES.json)
- [代码与论文核对说明](outputs/code-audit.md)
- [来源、版本、哈希清单](outputs/source-manifest.json)
- [交付核验记录](outputs/validation.md)

## 各篇分析

| 论文 | 分析笔记 | ANALYSIS_PACKAGE |
|---|---|---|
| DirectAudioEdit | [阅读](outputs/notes/directaudioedit.md) | [JSON](outputs/packages/directaudioedit.json) |
| AudioMorphix | [阅读](outputs/notes/audiomorphix.md) | [JSON](outputs/packages/audiomorphix.json) |
| AudioEditor | [阅读](outputs/notes/audioeditor.md) | [JSON](outputs/packages/audioeditor.json) |
| MelodyFlow | [阅读](outputs/notes/melodyflow.md) | [JSON](outputs/packages/melodyflow.json) |
| DDPM Inversion（ZETA；兼述ZEUS） | [阅读](outputs/notes/zeta.md) | [JSON](outputs/packages/zeta.json) |
| EdiTTS | [阅读](outputs/notes/editts.md) | [JSON](outputs/packages/editts.json) |

## 证据标签

SC=作者主张；DE=本次直接核对的论文表格/算法/代码内容，不代表本次复现实验；AI=分析推断；UN=尚未核验。所有实验数字均为论文报告。PDF 页码从首页起算。

- SC不能自动视为DE；AI必须保留推断属性；UN既不等于否定也不等于已验证。
- 当前包的evidence_status均为partial：方法/表格/关键代码有定位，但未独立运行模型或重算结果。
- 所有页码以每篇固定PDF第一页为1；ZETA用PMLR PDF的内部页，不用卷页。
- 本次阅读全文、相关附录及LaTeX，并静态核对列出的核心代码；没有声称完成全部代码审计。
- “training-free”重点分成不更新模型权重、无逐输入梯度拟合与免反演三个维度。
- 这里只形成来源分析包与候选P/F；没有跳过deep-read生成研究方案。

## 如何继续

下一轮读取outputs/ANALYSIS_PACKAGES.json与各笔记，调用deep-read Mode C，围绕“无需新增训练的音乐编辑如何兼顾目标修改与非目标音乐结构保持”构建P/F/M/E及交叉矩阵。先核验来源和边界，再筛选C连接点。

最终记录以GitHub为准。仓库不镜像论文全文、LaTeX全文、第三方源码、音频、数据集或模型权重；用原始链接、固定版本和哈希支持追溯。临时下载仅供本轮核对。
