# 大纲 · MeLFusion: Synthesizing Music from Image and Language Cues using Diffusion Models

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L16 摘要
- L28–67 1 Introduction
- L68–91 2 Related Works
- L92–217 3 Synthesizing Music from Image and Text
  - L110–120 3.1 Extracting Visual Guidance
  - L121–158 3.2 Text-to-Music LDM with Visual Synapse
  - L159–217 3.3 Overall Framework
- L218–323 4 Experiments and Results
  - L222–277 4.1 Datasets
  - L278–306 4.2 Evaluation Metrics
  - L307–316 4.3 Baseline Methods
  - L317–323 4.4 Results
- L324–488 5 Discussions and Analysis
- L489–522 6 Conclusion and Future Works
- L504 —— 附录 ——
- L523–534 A More Details on TANGO++
- L535–545 B Problem Motivation Revisited
- L546–552 C Other Baseline Approaches
- L553–555 D Implementation Details
- L556–892 E More Experimental Analysis
  - L559–580 E.1 Choice of Text-to-Image Diffusion Model
  - L581–604 E.2 Performance with Different Text Encoders
  - L605–628 E.3 Variation Across Genres
  - L629–649 E.4 Ablating choice of layers
  - L650–653 E.5 On conditioning image
  - L654–675 E.6 Alternate visual conditioning
  - L676–704 E.7 Subjective analysis
  - L705–892 E.8 Learnable versus Fixed α Parameters
- L893–945 F Dataset Details
  - L896–916 F.1 MeLBench Statistics
  - L917–921 F.2 Dataset Hierarchy and Samples
  - L922–945 F.3 Extended MusicCaps Data Collection
- L946–954 G User Study Details
- L955–960 H Inspiration from Conditional Image Generation
- L961–971 I Related Audio Concepts

## 公式（7 个，按出现顺序；L 后面是所在小节）

- L112 §3.1 Extracting Visual Guidance `eqn:attn`：\text{Attention}(\bm{Q}, \bm{K}, \bm{V}) = \text{Softmax}\left(\frac{\bm{Q} \bm{K}^T}{\sqrt{d_k}}\right)\bm{V}…
- L129 §3.2 Text-to-Music LDM with Visual Synapse：q(\bm{z}_{t}^M | \bm{z}_{t-1}^M) = \mathcal{N}(\bm{z}_t^M; \sqrt{1 - \beta_t}\bm{z}_{t-1}^M, \beta_t \textbf{I…
- L134 §3.2 Text-to-Music LDM with Visual Synapse `eqn:noise`：q(\bm{z}_{t}^{M} | \bm{z}_{1}^{M}) &= \mathcal{N}(\bm{z}_{t}^{M}; \sqrt{\bar{\gamma}_t}\bm{z}_{1}^{M}, (1 - \b…
- L144 §3.2 Text-to-Music LDM with Visual Synapse `eqn:synapse`：\bm{K}^M_l &= \alpha_l \bm{K}^I_l + (1 - \alpha_l) \bm{K}^M_l \\ \bm{V}^M_l &= \alpha_l \bm{V}^I_l + (1 - \alp…
- L154 §3.2 Text-to-Music LDM with Visual Synapse `eqn:loss`：\mathcal{L} = \mathbb{E}_{t\sim[1,T], \bm{z}_1^M, \bm{\epsilon}^M_t \sim \mathcal{N}(\boldsymbol{0}, \textbf{I…
- L300 §4.2 Evaluation Metrics：\mathcal{A}_{\text{\imagemusicmetric}} = \mathcal{A}_{\text{CLIP}}\;\mathcal{A}_{\text{CLAP}}^{T}
- L529 §A More Details on TANGO++ `eq:clip`：\mathcal{L}_{\text{ITC}} = -\frac{1}{2\mathcal{N}}\sum_{j = 1}^{\mathcal{N}}\log\underbrace{\left[\frac{\exp\l…

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
