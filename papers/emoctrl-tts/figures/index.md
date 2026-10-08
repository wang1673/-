# 图表索引

来源 `paper.pdf`（8 页）：图 1 张、表 7 张。全部裁剪拼在 `figures/_contact.png`，一次看完。

> 讲到哪张图就把那个 PNG 发给用户；讲之前自己先看一眼——caption 不会告诉你图是怎么排的。
> 裁得不对：`crop.py paper.pdf --page P --grid` 看带刻度的整页，再 `crop.py paper.pdf --page P x0 y0 x1 y1 -o figures/fig-NN.png` 重裁（坐标是页面比例 0–1）。

## 图 1 · 第 2 页 · `figures/fig-01.png`
**caption**：Fig. 1. An overview of (a) training and (b) inference of the audio model of EmoCtrl-TTS.
· label `fig:overview` · paper.tex L36 · 源文件 `figures/Overview-v3.png` · 正文引用：§3.1.1 Model training (L150)；§3.1.2 Inference (L164)

## 表 1 · 第 1 页 · `figures/tab-01.png`
**caption**：Table 1. Comparison of TTS models based on emotion capabilities.
· label `tab:tts_comparison` · paper.tex L53 · 正文引用：§2.1 Controlling emotion in TTS (L90)；§2.1 Controlling emotion in TTS (L92)

## 表 2 · 第 4 页 · `figures/tab-02.png`
**caption**：Table 2. Summary of evaluation datasets. S2ST: Speech-to-speech translation.
· label `table:eval_datasets` · paper.tex L266 · 正文引用：§4.1.2 Evaluation data (L264)

## 表 3 · 第 5 页 · `figures/tab-03.png`
**caption**：Table 3. Objective evaluation results for various models on JVNV S2ST and EMO-change test sets. A model with (+) was fine-tuned with 200k steps with more exposure to the IH-EMO. LL: Libri-light.
· label `tab:jvnv_results` · paper.tex L354 · 正文引用：§4.3 Model configuration (L443)；§4.5.1 Objective evaluation (L553)

## 表 4 · 第 5 页 · `figures/tab-04.png`
**caption**：Table 4. Subjective evaluation results on the JVNV S2ST test set are presented. The group with the top score (scores within the 95% confidence interval of the highest score) is displayed in bold font.
· label `tab:subj_results_jvnv` · paper.tex L408 · 正文引用：§4.5.2 Subjective evaluation (L587)

## 表 5 · 第 6 页 · `figures/tab-05.png`
**caption**：Table 5. Impact of training configurations on the EmoCtrl-TTS on JVNV S2ST test set.
· label `tab:ablation_study` · paper.tex L464 · 正文引用：§4.5.1 Objective evaluation (L577)；§4.5.3 Impact of training configurations (L610)；§4.5.3 Impact of training configurations (L618)

## 表 6 · 第 6 页 · `figures/tab-06.png`
**caption**：Table 6. Results of Laughter-test dataset.
· label `tab:laughter_test_results` · paper.tex L498 · 正文引用：§4.5.4 Results on real laughter and crying data (L630)

## 表 7 · 第 6 页 · `figures/tab-07.png`
**caption**：Table 7. Results of Crying-test dataset.
· label `tab:crying_test_results` · paper.tex L522 · 正文引用：§4.5.4 Results on real laughter and crying data (L630)
