# 大纲 · Virtual Consistency for Audio Editing

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L10 摘要
- L20–52 1 Introduction
- L53–118 2 Inversion-free Audio Editing
  - L55–88 2.1 Diffusion and Consistency Models
  - L89–118 2.2 Virtual Consistency Inversion
- L119–182 3 Experiments
  - L154–161 3.1 Evaluation Metrics
  - L162–164 3.2 Datasets
  - L165–178 3.3 Reference Methods
  - L179–182 3.4 Qualitative evaluation.
- L183–223 4 Results
  - L185–205 4.1 Quantitative Results
  - L206–209 4.2 Text-Audio Alignment Trade-off
  - L210–223 4.3 Qualitative Results
- L224–229 5 Conclusion

## 公式（10 个，按出现顺序；L 后面是所在小节）

- L57 §2.1 Diffusion and Consistency Models `eq:forward`：\x_t &= \sqrt{\alpha_t}\,\x_{t-1} + \sqrt{\beta_t}\,\eps_t,
- L61 §2.1 Diffusion and Consistency Models：\x_t &= \sqrt{\bar\alpha_t}\,\x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon, \qquad \bar\alpha_t \defeq \prod_{s=1}^t …
- L68 §2.1 Diffusion and Consistency Models `eq:x0hat`：\hat \x_0(\x_t,t) \;=\; \frac{\x_t - \sqrt{1-\bar\alpha_t}\,\eps_\theta(\x_t,t,c)}{\sqrt{\bar\alpha_t}}.
- L72 §2.1 Diffusion and Consistency Models：p_\theta(\x_{t-1}\mid \x_t) &= \mathcal{N}\parens*{\x_{t-1};\,\mu_\theta(\x_t,t),\,\sigma_t^2\mathbf I},\\ \mu…
- L78 §2.1 Diffusion and Consistency Models `eq:denoising`：\x_{t-1} &= \sqrt{\bar\alpha_{t-1}}\,\frac{\x_t - \sqrt{1-\bar\alpha_t}\,\eps_\theta(\x_t,t,c)}{\sqrt{\bar\alp…
- L94 §2.2 Virtual Consistency Inversion：\x_{t-1} \;=\; \sqrt{\bar\alpha_{t-1}}\,f(\x_t,t;\x_0) \;+\; \sqrt{1-\bar\alpha_{t-1}}\,\epsilon_t,
- L98 §2.2 Virtual Consistency Inversion `eq:cons-fn`：f(\x_t,t;\x_0) \;=\; \frac{\x_t - \sqrt{1-\bar\alpha_t}\,\eps_\theta(\x_t,t,c)}{\sqrt{\bar\alpha_t}}.
- L103 §2.2 Virtual Consistency Inversion：\eps_t^{\mathrm{cons}}(\x_t, \x_0) \;=\; \frac{\x_t - \sqrt{\bar\alpha_t}\,\x_0}{\sqrt{1-\bar\alpha_t}}.
- L109 §2.2 Virtual Consistency Inversion：\eps_t^{\mathrm{src}} = \eps_\theta(\x_t^{\mathrm{src}}, t, c_{\mathrm{src}}), \qquad \eps_t^{\mathrm{tgt}} = …
- L114 §2.2 Virtual Consistency Inversion `eq:controlvci`：\eps_t^{\mathrm{edit}}\defeq\frac{\varphi}{\sqrt{2}}\Delta\eps_t+\sqrt{1-\varphi^2}\:\eps_t^{\mathrm{cons}}(\x…

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
