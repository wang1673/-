# 大纲 · Melodia: Training-Free Music Editing Guided by Attention Probing in Diffusion Models

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L7 摘要
- L19–38 1 INTRODUCTION
- L39–52 2 Related Work
  - L41–43 2.1 Text-to-music generation
  - L44–52 2.2 Text-to-music editing
- L53–223 3 METHOD
  - L54–129 3.1 Preliminary
  - L130–161 3.2 Probing Analysis on Attention Maps
  - L162–174 3.3 Overview of Our Approach
  - L175–184 3.4 DDIM Inversion with Attention Repository
  - L185–223 3.5 Attention-based Structure Retention
- L224–374 4 Experiments
  - L226–229 4.1 Baselines
  - L230–262 4.2 Metrics
  - L263–266 4.3 Dataset
  - L267–350 4.4 Objective Evaluation
  - L351–353 4.5 Subjective Evaluation
  - L354–374 4.6 Additional Analysis
- L375–379 5 CONCLUSION
- L380–382 6 Acknowledgments

## 公式（6 个，按出现顺序；L 后面是所在小节）

- L58 §3.1 Preliminary：\phi^{\rm c} = \text{Cross-Attent}&\text{ion}(Q^{\rm c},K^{\rm c},V^{\rm c}) = M^{\rm c}\cdot V^{\rm c} \\ M^{…
- L66 §3.1 Preliminary：\phi^{\rm s} = \text{Self-Attent}&\text{ion}(Q^{\rm s},K^{\rm s},V^{\rm s}) = M^{\rm s}\cdot V^{\rm s} \\ M^{\…
- L178 §3.4 DDIM Inversion with Attention Repository：\mathbf{c}\sim \mathbb{P}_\mathbf{c},\ \mathbf{s}^{(n)}\sim\mathbb{P}_{\mathbf{s}^{(n)}},\ x^{(n)}=\mathbf{g}(…
- L186 §3.5 Attention-based Structure Retention：\phi'^{\rm s}_t = M'^{\rm s}_t& \cdot V'^s_t \\ M'^{\rm s}_t = {\rm Softm}&{\rm ax} \Big( \frac{Q^{\rm s}_t{K^…
- L247 §4.2 Metrics：\text{ASB} = \frac{2 \cdot \mathcal{S}(\mathcal{N}(s_\text{CLAP})) \cdot \mathcal{S}(\mathcal{N}(-s_\text{LPAP…
- L256 §4.2 Metrics：\text{AMB} = \frac{2 \cdot \mathcal{S}(\mathcal{N}(s_\text{CLAP})) \cdot \mathcal{S}(\mathcal{N}(s_\text{Chrom…

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
