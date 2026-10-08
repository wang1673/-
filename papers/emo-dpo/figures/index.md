# 图表索引

来源 `paper.pdf`（5 页）：图 3 张、表 2 张。全部裁剪拼在 `figures/_contact.png`，一次看完。

> 讲到哪张图就把那个 PNG 发给用户；讲之前自己先看一眼——caption 不会告诉你图是怎么排的。
> 裁得不对：`crop.py paper.pdf --page P --grid` 看带刻度的整页，再 `crop.py paper.pdf --page P x0 y0 x1 y1 -o figures/fig-NN.png` 重裁（坐标是页面比例 0–1）。

## 图 1 · 第 2 页 · `figures/fig-01.png`
**caption**：Fig. 1. Overview of the proposed Emo-DPO approach: (a) instruction tuning, (b) Emo-DPO training, and (c) the inference process.
· label `overall` · paper.tex L57 · 源文件 `icassp2.pdf` · 正文引用：§2 Methodology (L76)；§2.1 Emo-DPO Overview (L81)；§2.2 Instruction Tuning (L87)；§2.3.1 Beyond One Emotion - DPO Training (L104)

## 图 2 · 第 4 页 · `figures/fig-02.png`
**caption**：Fig. 2. Comparison of subjective evaluation results for MOS and Emotion MOS tests across cosyvoice, emospeech, and the proposed Emo-DPO models.
· label `mos` · paper.tex L183 · 源文件 `mos.png` · 正文引用：§4 Results and Discussion (L177)；§4.1 Effectiveness of Emo-DPO training on LLM (L180)

## 图 3 · 第 4 页 · `figures/fig-03.png`
**caption**：Fig. 3. Comparison of subjective evaluation results from AB preference tests: 1) left: cosyvoice vs. Emo-DPO and 2) right: emospeech vs. Emo-DPO. TABLE II ABLATION STUDY ON THE PROPOSED EMO-DPO WITH DIFFERENT COMPONENTS REMOVED W.R.T SPEECH SYNTHESIS PERFORMANCES. SYMBOL ”−” IS REMOVAL OPERATION.
· label `AB` · paper.tex L197 · 源文件 `AB.png` · 正文引用：§4 Results and Discussion (L177)；§4.1 Effectiveness of Emo-DPO training on LLM (L182)

## 表 I · 第 4 页 · `figures/tab-I.png`
**caption**：TABLE I OBJECTIVE EVALUATION RESULTS COMPARISON OF THE PROPOSED EMO-DPO WITH BASELINES ON EMOTION SIMILARITY, PROSODY SIMILARITY, INTELLIGIBILITY AND SPEECH EMOTION RECOGNITION ACCURACY.
· label `objective` · paper.tex L140 · 正文引用：§4 Results and Discussion (L177)；§4.1 Effectiveness of Emo-DPO training on LLM (L180)

## 表 II · 第 4 页 · `figures/tab-II.png`
**caption**：TABLE II ABLATION STUDY ON THE PROPOSED EMO-DPO WITH DIFFERENT COMPONENTS REMOVED W.R.T SPEECH SYNTHESIS PERFORMANCES. SYMBOL ”−” IS REMOVAL OPERATION.
· label `ablation` · paper.tex L207 · 正文引用：§4 Results and Discussion (L177)；§4.2 Ablation Study (L194)
