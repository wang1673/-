# 图表索引

来源 `paper.pdf`（21 页）：图 10 张、表 16 张。全部裁剪拼在 `figures/_contact.png`，一次看完。

> 讲到哪张图就把那个 PNG 发给用户；讲之前自己先看一眼——caption 不会告诉你图是怎么排的。
> 裁得不对：`crop.py paper.pdf --page P --grid` 看带刻度的整页，再 `crop.py paper.pdf --page P x0 y0 x1 y1 -o figures/fig-NN.png` 重裁（坐标是页面比例 0–1）。

## 图 1 · 第 1 页 · `figures/fig-01.png`
**caption**：Figure 1. We present MELFUSION, a music diffusion model equipped with a novel “visual synapse”, that can effectively in- fuse image semantics into a text-to-music diffusion model. This task indeed requires a detailed understanding of the concepts in the image. An alternate approach like using a caption generator to convert image to text space to be further used with existing text-to- music methods leads to a sub-optimal overall audio quality (OVL) score. Our approach can knit together complementary information from both modalities to synthesize high-quality music.
· label `fig:teaser` · paper.tex L31 · 源文件 `Figures/mainfig.pdf` · 正文引用：§1 Introduction (L47)

## 图 2 · 第 4 页 · `figures/fig-02.png`
**caption**：Figure 2. Our approach MELFUSION generates music waveform w conditioned on an image I and a given textual instruction Y . Visual semantics from I is instilled into a text-to-music diffusion model (bottom green box) using a pre-trained and frozen text-to-image diffusion model (top blue box). The image I is first DDIM inverted into a noisy latent zI the text-to-image LDM that consumes zI T is infused into the cross-attention features of text-to-music LDM decoder layers, modulated by
· label `fig:main-figure` · paper.tex L95 · 源文件 `Figures/MelFusion_Mainfig_Updated.pdf` · 正文引用：§3 Synthesizing Music from Image and Text (L107)

## 图 3 · 第 5 页 · `figures/fig-03.png`
**caption**：Figure 3. The distribution of different genres in MeLBench.
· label `fig:dataset_pie_chart` · paper.tex L230 · 源文件 `Figures/Dataset_pie_chart.png` · 正文引用：§4.1 Datasets (L228)

## 图 4 · 第 5 页 · `figures/fig-04.png`
**caption**：Figure 4. Some image and text pairs from MeLBench. We include more examples in the Appendix.
· label `fig:dataset_main_paper` · paper.tex L236 · 源文件 `Figures/Dataset_examples.png` · 正文引用：§4.1 Datasets (L228)

## 图 5 · 第 13 页 · `figures/fig-05.png`
**caption**：Figure 5. A mock-up of a social media post that contains an image and associated textual content. Our approach MELFUSION, can consume such image-textual pairs as input and synthesize music that can go well with them.
· label `fig:problem-motivation` · paper.tex L537 · 源文件 `Figures/problem-motivation.jpg` · 正文引用：§B Problem Motivation Revisited (L544)

## 图 6 · 第 16 页 · `figures/fig-06.png`
**caption**：Figure 6. Frequency of top 90 words from MeLBench
· label `fig:dataset_word_frequency` · paper.tex L731 · 源文件 `Figures/MelBench_dataset_word_frequency_50.png` · 正文引用：§F.1 MeLBench Statistics (L915)

## 图 7 · 第 18 页 · `figures/fig-07.png`
**caption**：Figure 7. Samples from MeLBench.
· label `fig:dataset_examples_supp` · paper.tex L886 · 源文件 `Figures/Sanjoy_MMGEN_dataset_Supplementary_part_2_compressed.png` · 正文引用：§F.2 Dataset Hierarchy and Samples (L920)

## 图 8 · 第 20 页 · `figures/fig-08.png`
**caption**：Figure 8. User study interface to collect OVL and REL scores.
· label `fig:user-study_ovl_rel` · paper.tex L925 · 源文件 `Figures/Sanjoy_MMGEN_dataset_Supplementary_OVL_REL.png` · 正文引用：§G User Study Details (L949)

## 图 9 · 第 20 页 · `figures/fig-09.png`
**caption**：Figure 9. User study interface for comparison against prior text- to-music methods
· label `fig:user-study-comparison` · paper.tex L932 · 源文件 `Figures/Sanjoy_MMGEN_dataset_Supplementary_user_study_3.png` · 正文引用：§G User Study Details (L951)

## 图 10 · 第 20 页 · `figures/fig-10.png`
**caption**：Figure 10. User study interface to obtain IMSM scores
· label `fig:user-study_imsm` · paper.tex L939 · 源文件 `Figures/Sanjoy_MMGEN_dataset_Supplementary_IMSM.png` · 正文引用：§G User Study Details (L953)

## 表 1 · 第 7 页 · `figures/tab-01.png`
**caption**：Table 1. Our proposed approach MELFUSION offers significant gains over state-of-the-art text-to-music methods (first section), and our adapted text-and-image conditioned baselines (second section) across multiple objective and subjective metrics on two datasets. IMSM is applicable only when the model is conditioned on visual modality. We skip comparison with MuBERT, Noise2Music, and MeLoDy on MeLBench dataset as their codebases are not public. Please refer to Sec. 4.4 for more details.
· label `tab:main_table` · paper.tex L246 · 正文引用：§4.4 Results (L318)；§4.4 Results (L322)

## 表 2 · 第 7 页 · `figures/tab-02.png`
**caption**：Table 2. We systematically analyze our design choice of learnable α parameters. We vary the position of the synapse: encoder or decoder and also study whether we need the same or different α parameters for each block within them.
· label `tab:role_of_alpha` · paper.tex L331 · 正文引用：§5 Discussions and Analysis (L327)

## 表 3 · 第 7 页 · `figures/tab-03.png`
**caption**：Table 3. Sensitivity analysis on the learning rate for α parameters.
· label `tab:alpha_lr` · paper.tex L360 · 正文引用：§5 Discussions and Analysis (L329)

## 表 4 · 第 7 页 · `figures/tab-04.png`
**caption**：Table 4. Conditioning independently on each of the modalities leads to inferior music generation performance in this experiment.
· label `tab:input_conditioning` · paper.tex L385 · 正文引用：§5 Discussions and Analysis (L382)

## 表 5 · 第 8 页 · `figures/tab-05.png`
**caption**：Table 5. Sensitivity analysis on the number of denoising steps T, and the strength of classifier-free guidance.
· label `tab:steps_and_guidance` · paper.tex L409 · 正文引用：§5 Discussions and Analysis (L407)

## 表 6 · 第 8 页 · `figures/tab-06.png`
**caption**：Table 6. Performance of MELFUSION with varying verbosity of text prompts collected from MeLBench.
· label `tab:varying text prompt` · paper.tex L435 · 正文引用：§5 Discussions and Analysis (L457)

## 表 7 · 第 8 页 · `figures/tab-07.png`
**caption**：Table 7. While comparing MELFUSION with state-of-the-art text- to-audio approaches, we see significant improvement in quality.
· label `tab:comparison_against_text_to_audio` · paper.tex L463 · 正文引用：§5 Discussions and Analysis (L461)

## 表 8 · 第 14 页 · `figures/tab-08.png`
**caption**：Table 8. MELFUSION with different versions of Stable Diffusion.
· label `tab:sd_version` · paper.tex L561 · 正文引用：§E.1 Choice of Text-to-Image Diffusion Model (L579)

## 表 9 · 第 14 页 · `figures/tab-09.png`
**caption**：Table 9. Performance of MELFUSION with different text encoders
· label `tab:text_encoders` · paper.tex L583 · 正文引用：§E.2 Performance with Different Text Encoders (L603)

## 表 10 · 第 14 页 · `figures/tab-10.png`
**caption**：Table 10. A study on the diversity analysis of MELFUSION. We evaluate the performance of our model on generating musi- cal tracks of five different genres on MeLBench.
· label `tab:genre_wise_performance` · paper.tex L607 · 正文引用：§E.3 Variation Across Genres (L627)

## 表 11 · 第 15 页 · `figures/tab-11.png`
**caption**：Table 11. Ablation of different decoder blocks
· label `tab:decoder_block_ablation_rebuttal` · paper.tex L632 · 正文引用：§E.4 Ablating choice of layers (L630)

## 表 12 · 第 15 页 · `figures/tab-12.png`
**caption**：Table 12. Comparison against different visual conditioning
· label `tab:comparisons_rebuttal` · paper.tex L657 · 正文引用：§E.6 Alternate visual conditioning (L655)

## 表 13 · 第 15 页 · `figures/tab-13.png`
**caption**：Table 13. Subjective analysis on generated samples
· label `tab:subjective_rebuttal` · paper.tex L680 · 正文引用：§E.7 Subjective analysis (L678)

## 表 14 · 第 15 页 · `figures/tab-14.png`
**caption**：Table 14. Analyzing the effect of having fixed versus learnable α.
· label `tab:fixed_vs_learnable_alpha` · paper.tex L707 · 正文引用：§E.8 Learnable versus Fixed α Parameters (L729)

## 表 15 · 第 19 页 · `figures/tab-15.png`
**caption**：Table 15. Genre and sub-genre-wise division of the collected samples. Our dataset encompasses samples from 15 different genres each further divided into 22 sub-genres
· label `tab:dataset_genre_division` · paper.tex L738 · 正文引用：§F.2 Dataset Hierarchy and Samples (L918)

## 表 16 · 第 19 页 · `figures/tab-16.png`
**caption**：Table 16. Image categories in MeLBench.
· label `tab:dataset` · paper.tex L897 · 正文引用：§F.1 MeLBench Statistics (L913)
