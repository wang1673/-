# 图表索引

来源 `paper.pdf`（8 页）：图 7 张、表 0 张。全部裁剪拼在 `figures/_contact.png`，一次看完。

> 讲到哪张图就把那个 PNG 发给用户；讲之前自己先看一眼——caption 不会告诉你图是怎么排的。
> 裁得不对：`crop.py paper.pdf --page P --grid` 看带刻度的整页，再 `crop.py paper.pdf --page P x0 y0 x1 y1 -o figures/fig-NN.png` 重裁（坐标是页面比例 0–1）。

## 图 1 · 第 4 页 · `figures/fig-01.png`
**caption**：Figure 1: Diffusion generation compared with warm initialization. Dashed arrows indicate reverse diffusion steps. Top: Standard genera- tion from Gaussian noise gradually produces piano audio. Bottom: Warm initialization from x(g) (Oboe) preserves the melody while the diffusion process shifts the timbre toward the piano distribution.
· label `fig:warm_init_vs_generation` · paper.tex L92 · 源文件 `Figures/denoising_spectrograms.pdf` · 正文引用：§3.1 Framework (L87)；§3.1 Framework (L89)

## 图 2 · 第 4 页 · `figures/fig-02.png`
**caption**：Figure 2: Spectrograms of oboe-to-piano timbre transfer for dif- ferent initialization times tinit. A diffusion schedule with T = 100 steps is used, with reverse diffusion starting at tinit. Smaller tinit leads to stronger deviation from the input, while larger values pre- serve more of the original melodic structure.
· label `fig:init_time_spectrograms` · paper.tex L102 · 源文件 `Figures/example_spectrograms.pdf` · 正文引用：§3.1 Framework (L100)

## 图 3 · 第 4 页 · `figures/fig-03.png`
**caption**：Figure 3: JD as a function of τinit for oboe-to-piano timbre transfer for λ = 0 and λ = 1. τinit = 0 denotes that the model performs all reverse steps, while τinit = 1 denotes that no reverse steps are performed. Lower values indicate greater melodic similarity to the guide signal x(g).
· label `fig:jaccard_vs_t_Oboe2Piano` · paper.tex L152 · 源文件 `Figures/jaccard_vs_t_mono_melody_Oboe2Piano.pdf` · 正文引用：§4.1 Timbre Transfer (L150)；§4.1 Timbre Transfer (L165)

## 图 4 · 第 5 页 · `figures/fig-04.png`
**caption**：Figure 4: FAD as a function of τinit for oboe-to-piano timbre trans- fer for λ = 0 and λ = 1. τinit = 0 denotes that the model performs all reverse steps, while τinit = 1 denotes that no reverse steps are performed. Lower values indicate closer alignment with the piano reference distribution.
· label `fig:fad_vs_t_Oboe2Piano` · paper.tex L158 · 源文件 `Figures/fad_vs_t_Oboe2Piano.pdf` · 正文引用：§4.1 Timbre Transfer (L150)；§4.1 Timbre Transfer (L165)

## 图 5 · 第 5 页 · `figures/fig-05.png`
**caption**：Figure 5: Spectrograms of enhanced audio signals. Left: de- graded guide signals x(g). Right: corresponding outputs obtained via warm initialization.
· label `fig:enhancemnet_spectrograms` · paper.tex L186 · 源文件 `Figures/enhancemnet_spectrograms.pdf` · 正文引用：§4.3 Audio Enhancement (L184)

## 图 6 · 第 8 页 · `figures/fig-06.png`
**caption**：Figure 6: JD as a function of τinit for string-to-clarinet timbre transfer for λ = 0 and λ = 1. τinit = 0 denotes that the model performs all reverse steps, while τinit = 1 denotes that no reverse steps are performed.
· label `fig:jaccard_vs_t_mono_melody_String2Clarinet` · paper.tex L218 · 源文件 `Figures/jaccard_vs_t_mono_melody_String2Clarinet.pdf` · 正文引用：§7 Appendix: String-to-Clarinet Timbre Tran (L216)

## 图 7 · 第 8 页 · `figures/fig-07.png`
**caption**：Figure 7: FAD as a function of τinit for string-to-clarinet timbre transfer for λ = 0 and λ = 1. τinit = 0 denotes that the model performs all reverse steps, while τinit = 1 denotes that no reverse steps are performed.
· label `fig:fad_vs_t_String2Clarinet` · paper.tex L225 · 源文件 `Figures/fad_vs_t_String2Clarinet.pdf` · 正文引用：§7 Appendix: String-to-Clarinet Timbre Tran (L216)
