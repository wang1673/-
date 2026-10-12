# 大纲 · MusicMagus: Zero-Shot Text-to-Music Editing via Diffusion Models

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L7 摘要
- L11–35 1 Introduction
- L36–53 2 Related Work
  - L38–43 2.1 Text-to-Music Generation
  - L44–53 2.2 Text-to-Music Editing
- L54–78 3 Background
- L79–197 4 Method
  - L85–145 4.1 Finding Editing Direction
  - L146–197 4.2 Adding Constraints Over Cross-Attention
- L198–351 5 Experiments
  - L202–211 5.1 Baselines
  - L212–227 5.2 Metrics
  - L228–241 5.3 Data Preparation
    - L230–237 5.3.1 Objective Experiments
    - L238–241 5.3.2 Subjective Experiments
  - L242–247 5.4 Experimental Setup
  - L248–351 5.5 Results
    - L250–303 5.5.1 Subjective Experiments
    - L304–351 5.5.2 Objective Experiments
- L352–380 6 Discussion
  - L354–370 6.1 Real Music Audio Editing
  - L371–380 6.2 Limitations
- L381–386 7 Conclusion
- L387–390 Ethical Statement
- L391–396 Acknowledgments

## 公式（13 个，按出现顺序；L 后面是所在小节）

- L59 §3 Background：z_{t} = \sqrt{\alpha_t} z_{t-1} + \sqrt{1 - \alpha_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I),
- L65 §3 Background `eq:denoise`：z_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( z_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\thet…
- L73 §3 Background：z_{t-1} = \text{Denoise}(z_t, \epsilon_\theta, t).
- L93 §4.1 Finding Editing Direction：\left\{ \begin{aligned} E_\text{T5} &= \text{T5}(y), \\ E_\text{CLAP} &= \text{CLAP}(y). \end{aligned} \right.
- L104 §4.1 Finding Editing Direction：E_\text{GPT} = \text{GPT-2}(\text{Proj}(E_\text{T5}, E_\text{CLAP})).
- L110 §4.1 Finding Editing Direction：\epsilon_\theta &= \epsilon_\theta(z_t, E, t), \\ z_{t-1} &= \text{Denoise}(z_t, \epsilon_\theta, E, t).
- L127 §4.1 Finding Editing Direction：E^\text{edit}_\text{T5} = E_\text{T5} + \Delta.
- L142 §4.1 Finding Editing Direction：E^\text{edit} = \{E_\text{T5} + \Delta, E'_{\text{GPT}}\}.
- L159 §4.2 Adding Constraints Over Cross-Attention：\begin{split} \text{Attention}(Q, K, V) &= M \cdot V, \\ \text{where } M &= \text{Softmax}\left(\frac{QK^T}{\s…
- L170 §4.2 Adding Constraints Over Cross-Attention：M^\text{origin} = \{M^\text{origin}_1, ..., M^\text{origin}_T\}.
- L178 §4.2 Adding Constraints Over Cross-Attention：L_t = \| M^\text{edit}_t - M^\text{origin}_t\|_2.
- L184 §4.2 Adding Constraints Over Cross-Attention：\epsilon^\text{edit}_\theta = \epsilon_\theta(z_t - \alpha\nabla_{z_t}L_t, E^\text{edit}, t).
- L190 §4.2 Adding Constraints Over Cross-Attention：z_{t-1} = \text{Denoise}(z_t, \epsilon^\text{edit}_\theta, E^\text{edit}, t).

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
