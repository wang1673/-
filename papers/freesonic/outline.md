# 大纲 · FreeSonic: Training-Free Temporal-Aware Decoupled Attention for Precise Audio Editing

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L7 摘要
- L12–31 1 Introduction
- L32–165 2 Method
  - L34–63 2.1 Preliminaries
    - L36–39 2.1.1 Inversion-based Audio Editing
    - L40–52 2.1.2 TangoFlux Base Model
    - L53–63 2.1.3 Attention Mechanism in MM-DiT-based TTA
  - L64–165 2.2 Temporal-Aware Decoupled Attention
    - L66–72 2.2.1 Text-Audio Attention for Temporal Extraction
    - L73–102 2.2.2 Scheduled Attention Decoupling
    - L103–165 2.2.3 Task-Oriented Noise Injection
- L166–236 3 Experiments
  - L168–178 3.1 Experimental Settings
    - L170–172 3.1.1 Datasets and Baselines
    - L173–178 3.1.2 Evaluation Metrics
  - L179–182 3.2 Quantitative Results
  - L183–186 3.3 Subjective Results
  - L187–236 3.4 Ablation Study and Efficiency Analysis
- L237–240 4 Conclusion
- L241–243 5 Acknowledgments
- L244–246 6 Generative AI Use Disclosure

## 公式（8 个，按出现顺序；L 后面是所在小节）

- L43 §2.1.2 TangoFlux Base Model：x_t = (1 - t)x_1 + t\tilde{x}_0, \quad v_t = \frac{dx_t}{dt} = \tilde{x}_0 - x_1,
- L47 §2.1.2 TangoFlux Base Model：\mathcal{L}_{\text{FM}} = \mathbb{E}_{x_1, \tilde{x}_0, t} || u(x_t, t; \theta) - v_t ||^2 .
- L55 §2.1.3 Attention Mechanism in MM-DiT-based TTA：Q = [Q_a; Q_t], \quad K = [K_a; K_t], \quad V = [V_a; V_t],
- L59 §2.1.3 Attention Mechanism in MM-DiT-based TTA：\mathrm{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V.
- L79 §2.2.2 Scheduled Attention Decoupling `eq:mix`：\begin{aligned} \hat{K}_{tg}^l &= \delta K_{tg}^l + (1-\delta)K_s^l, \\ \hat{V}_{tg}^l &= \delta V_{tg}^l + (1…
- L87 §2.2.2 Scheduled Attention Decoupling `eq:mask`：\begin{aligned} \tilde{K}_{tg}^l &= M \odot \hat{K}_{tg}^l + (1-M)\odot K_s^l, \\ \tilde{V}_{tg}^l &= M \odot …
- L95 §2.2.2 Scheduled Attention Decoupling：z^{l+1} = \mathrm{Attention}(Q_{tg}^l, \tilde{K}_{tg}^l, \tilde{V}_{tg}^l).
- L107 §2.2.3 Task-Oriented Noise Injection：z'_t = (1 - M) \odot z_t + M \odot ((1 - \lambda_t) z_t + \lambda_t \eta),

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
