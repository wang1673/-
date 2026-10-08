# 图表索引

来源 `paper.pdf`（13 页）：图 11 张、表 2 张。全部裁剪拼在 `figures/_contact.png`，一次看完。

> 讲到哪张图就把那个 PNG 发给用户；讲之前自己先看一眼——caption 不会告诉你图是怎么排的。
> 裁得不对：`crop.py paper.pdf --page P --grid` 看带刻度的整页，再 `crop.py paper.pdf --page P x0 y0 x1 y1 -o figures/fig-NN.png` 重裁（坐标是页面比例 0–1）。

## 图 5 · 第 2 页 · `figures/fig-05.png`
**caption**：Figure 5. Chroma visualizations under different tmax and tmin conﬁgurations. Varying tmax produces minimal change, while changes in tmin strongly affect harmonic structure and melodic preservation.

## 图 6 · 第 3 页 · `figures/fig-06.png`
**caption**：Figure 6. Distribution of the 16 annotated musical genres in our multimodal dataset ( about 15k samples). The corpus is relatively balanced, with Folk, Electronic, and Classical containing slightly more samples and the remaining categories distributed evenly.

## 图 7 · 第 4 页 · `figures/fig-07.png`
**caption**：Figure 7. Effect of text length on multimodal conditioning. The orange curve (“txt cap + img cap”) uses the full textual input, meaning the model is conditioned on both the music-description caption and the image-description caption, while the gray dashed line corresponds to conditioning on the music prompt together with the image.

## 图 8 · 第 6 页 · `figures/fig-08.png`
**caption**：Figure 8. Participants are presented with the conditioning prompts (image, text, or both), along with the source audio and the generated audio. They rate each sample along three dimensions – Overall Audio Quality (OVL), Style Relevance (REL), and Melodic Consistency – using 0–10 sliders. A participant ID dropdown ensures proper tracking before submission.

## 图 9 · 第 7 页 · `figures/fig-09.png`
**caption**：Figure 9. The Classical to Jazz style transfer. The ﬁgure shows the visual–text prompt with the source classical mel-spectrogram, followed by the same prompt paired with the generated jazz mel-spectrogram.

## 图 10 · 第 7 页 · `figures/fig-10.png`
**caption**：Figure 10. The Traditional to Blues style transfer.

## 图 11 · 第 8 页 · `figures/fig-11.png`
**caption**：Figure 11. The Blues to Classical style transfer.

## 图 12 · 第 8 页 · `figures/fig-12.png`
**caption**：Figure 12. The Rock to Classical style transfer.

## 图 13 · 第 9 页 · `figures/fig-13.png`
**caption**：Figure 13. The Folk to Latin style transfer.

## 图 14 · 第 9 页 · `figures/fig-14.png`
**caption**：Figure 14. The Jazz to Blues style transfer.

## 图 15 · 第 10 页 · `figures/fig-15.png`
**caption**：Figure 15. The Folk to New Age style transfer.

## 表 5 · 第 5 页 · `figures/tab-05.png`
**caption**：Table 5. Comparison of different encoder conﬁgurations.

## 表 6 · 第 5 页 · `figures/tab-06.png`
**caption**：Table 6. Variability across genre-to-genre transfers. Embedding similarity indicates stylistic similarity; lower values suggest closer styles and easier transfer.
