# 大纲 · DirectAudioEdit: Inversion-Free Text-Guided Audio Editing via Diffusion Prediction Contrast

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L7 摘要
- L19–57 1 Introduction
- L58–114 2 Preliminary
  - L60–67 2.1 Content Editing
  - L68–89 2.2 Inversion-based Editing
  - L90–102 2.3 Inversion-free Editing with Direct Path
  - L103–114 2.4 Clean-State Editing Path
- L115–259 3 Methodology
  - L124–156 3.1 Shared-Noise Re-noising
  - L157–201 3.2 Diffusion Prediction Contrast
  - L202–259 3.3 Dynamic Guidance Schedule
- L260–512 4 Experiments
  - L326–360 4.1 Experimental Setup
  - L361–384 4.2 Main Results
  - L385–412 4.3 Human Evaluation
  - L413–512 4.4 Inference Cost
- L513–661 5 Ablation Studies and Analysis
  - L604–611 5.1 Why Target-State Re-noising?
  - L612–618 5.2 Why Reverse-Dynamics Contrast?
  - L619–654 5.3 Why Dynamic Guidance?
  - L655–661 5.4 Qualitative Analysis
- L662–689 6 Related Work
  - L664–678 6.1 Text-guided Audio Editing
  - L679–683 6.2 Training-free Audio Editing
  - L684–689 6.3 Inversion-free Generative Editing
- L690–695 7 Conclusion
- L696–701 Limitations
- L700 —— 附录 ——
- L702–703 Appendix
- L704–717 A Implementation Details
- L718–760 B Event-level Editing Benchmark
- L761–908 C Statistical Results
- L909–926 D Mel-Spectrogram Comparison

## 公式（13 个，按出现顺序；L 后面是所在小节）

- L62 §2.1 Content Editing：X^{\text{tgt}} = \mathcal{M}_\theta(X^{\text{src}}, c^{\text{src}}, c^{\text{tgt}}),
- L72 §2.2 Inversion-based Editing：dZ^{\text{src}}_t = V^{\text{src}}(Z^{\text{src}}_t, t)dt\\ dZ^{\text{tgt}}_t = V^{\text{tgt}}(Z^{\text{tgt}}_…
- L93 §2.3 Inversion-free Editing with Direct Path `eq:velocity`：Z^{\text{DP}}_t = Z^{\text{src}}_0 + Z^{\text{tgt}}_t -Z^{\text{src}}_t\\ dZ^{\text{DP}}_t = V^{\Delta}(Z^{\te…
- L109 §2.4 Clean-State Editing Path：Z_T^{\text{DP}} = Z^{\text{src}}_0,
- L129 §3.1 Shared-Noise Re-noising：\mathcal{R}_t(x;\epsilon) = \sqrt{\alpha_t}x + \sqrt{1-\alpha_t}\epsilon,
- L140 §3.1 Shared-Noise Re-noising：\hat{Z}^{\mathrm{src}}_t = \mathcal{R}_t(Z^{\mathrm{src}}_0;\epsilon_t).
- L150 §3.1 Shared-Noise Re-noising：\hat{Z}^{\mathrm{tgt}}_t = \mathcal{R}_t(Z_t^{\text{DP}};\epsilon_t).
- L162 §3.2 Diffusion Prediction Contrast：\hat{Z}^{\mathrm{src}}_{t-1} = \Phi_\theta \left( \hat{Z}^{\mathrm{src}}_t, t, c^{\mathrm{src}}; w^{\mathrm{sr…
- L174 §3.2 Diffusion Prediction Contrast：\Delta^{\mathrm{src}}_t = \hat{Z}^{\mathrm{src}}_{t-1} - \hat{Z}^{\mathrm{src}}_t .
- L184 §3.2 Diffusion Prediction Contrast：\Delta^{\mathrm{edit}}_t = \Delta^{\mathrm{tgt}}_t - \Delta^{\mathrm{src}}_t .
- L193 §3.2 Diffusion Prediction Contrast：Z_{t-1}^{\text{DP}} = Z_t^{\text{DP}} + \Delta^{\mathrm{edit}}_t .
- L238 §3.3 Dynamic Guidance Schedule：w^{\mathrm{src}}(t)=w^{\mathrm{src}} .
- L242 §3.3 Dynamic Guidance Schedule：w^{\mathrm{tgt}}(t) = w^{\min} + s_t \left( w^{\max}-w^{\min} \right),

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
