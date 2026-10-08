# 大纲 · Audio-to-Audio via Diffusion Warm Initialization

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L13 摘要
- L18–34 1 Introduction
- L35–64 2 Diffusion Warm Initialization
  - L37–47 2.1 Diffusion Models
  - L48–64 2.2 Warm Initialization
- L65–139 3 Audio-to-Audio via warm initialization
  - L69–114 3.1 Framework
  - L115–139 3.2 Metrics
    - L119–128 3.2.1 Fréchet Audio Distance (FAD)
    - L129–139 3.2.2 Jaccard Distance (JD)
- L140–192 4 Applications
  - L144–172 4.1 Timbre Transfer
  - L173–178 4.2 MIDI-to-Real
  - L179–192 4.3 Audio Enhancement
- L193–202 5 Discussion
- L203–213 6 Conclusion
- L214–233 7 Appendix: String-to-Clarinet Timbre Transfer

## 公式（3 个，按出现顺序；L 后面是所在小节）

- L53 §2.2 Warm Initialization `eq:warm_init`：\mathbf{x}^{(\mathrm g)}_{t_\text{init}} \sim \mathcal{N}(\alpha_{t_\text{init}}\mathbf{x}^{(\mathrm g)}, \sig…
- L121 §3.2.1 Fréchet Audio Distance (FAD)：\mathrm{FAD} = \lVert \mu_r - \mu_t \rVert^2 + \operatorname{tr}\left( \Sigma_r + \Sigma_t - 2\sqrt{\Sigma_r \…
- L132 §3.2.2 Jaccard Distance (JD)：\mathrm{JD}(A, B) = 1 - \frac{|A \cap B|}{|A \cup B|}

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
