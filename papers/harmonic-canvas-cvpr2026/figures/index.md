# 图表索引

来源 `paper.pdf`（11 页）：图 4 张、表 4 张。全部裁剪拼在 `figures/_contact.png`，一次看完。

> 讲到哪张图就把那个 PNG 发给用户；讲之前自己先看一眼——caption 不会告诉你图是怎么排的。
> 裁得不对：`crop.py paper.pdf --page P --grid` 看带刻度的整页，再 `crop.py paper.pdf --page P x0 y0 x1 y1 -o figures/fig-NN.png` 重裁（坐标是页面比例 0–1）。

## 图 1 · 第 1 页 · `figures/fig-01.png`
**caption**：Figure 1. Overview of our Music Style Transfer workflow. Our model transforms a source clip (e.g., classical) into a target style (e.g., rock) via multimodal guidance. While the framework na- tively supports textual captions (strikethrough in figure to empha- size independence), it could leverages visual cues for non-verbal style and melodic guidance for pitch preservation.

## 图 2 · 第 4 页 · `figures/fig-02.png`
**caption**：Figure 2. Overview of the proposed multimodal music style transfer framework. (Left) We build upon the Make-An-Audio 3 backbone and perform inversion-free flow editing in latent space. (Middle) Visual Conditioning: text and image features are encoded separately and injected into each DiT block via a cross-adapter attention mechanism, enabling the model to interpret non-verbal aesthetics such as ambience, color tone, and scene mood. (Right) Melodic Guidance: a normalized chroma loss constrains pitch-class structure, and its gradient corrects the flow trajectory, ensuring that stylistic transformation preserves melodic identity.

## 图 3 · 第 7 页 · `figures/fig-03.png`
**caption**：Figure 3. (Left) Visualization of music style transfer results across three multimodal prompts. For each prompt, source/target images are shown on the left, followed by Mel-spectrograms of the Source, MeLFusion, and Ours outputs. (Right) Counterfactual test: changing only the image while keeping text fixed leads to different outputs, demonstrating the influence of visual cues on generated musical style.

## 图 4 · 第 8 页 · `figures/fig-04.png`
**caption**：Figure 4. Comparison of normalized chroma energy curves across four settings: (a) source audio, (b) target style reference, (c) transfer without melody constraint, and (d) our chroma-guided method. The chroma distributions clearly illustrate how our approach maintains melodic consistency while achieving stylistic transformation.

## 表 1 · 第 6 页 · `figures/tab-01.png`
**caption**：Table 1. Objective and subjective evaluation results. Two modality indicators (Text/Image) are shown for each method. Bold number denotes the best metric value.

## 表 2 · 第 8 页 · `figures/tab-02.png`
**caption**：Table 2. Ablation on modality conditioning. Checkmarks indicate which modalities are provided; Caption denotes a BLIP-generated caption from the image.

## 表 3 · 第 8 页 · `figures/tab-03.png`
**caption**：Table 3. Comparison of Inversion Strategies. Lower is better for FAD/FD; higher is better for others.

## 表 4 · 第 8 页 · `figures/tab-04.png`
**caption**：Table 4. Sensitivity analysis of the guidance rate (GR) and the number of chroma-guided correction steps.
