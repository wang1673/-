# 大纲 · SteerMusic: Enhanced Musical Consistency for Zero-shot Text-guided and Personalized Music Editing

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L7 摘要
- L16–61 1 Introduction
- L62–75 2 Related work
  - L64–68 2.1 Text-guided Music Generation and Editing
  - L69–75 2.2 Personalized Music Generation and Editing
- L76–97 3 Preliminaries
- L98–189 4 Method
  - L101–117 4.1 SteerMusic: Zero-shot Text-guided Music Editing
  - L118–189 4.2 SteerMusic+: Personalized Music Editing
- L190–353 5 Experiments
  - L208–228 5.1 Evaluation Metrics
  - L229–282 5.2 Zero-shot Text-guided Music Editing
  - L283–353 5.3 Personalized Music Editing
- L354–356 6 Conclusion

## 公式（6 个，按出现顺序；L 后面是所在小节）

- L90 §3 Preliminaries `eqn:dds`：\nabla_\theta \mathcal{L}_{\text{DDS}}(\phi,x=g(\theta),y^{\text{tgt}},x^{\text{src}},y^{\text{src}}) \\ = \ma…
- L135 §4.2 SteerMusic+: Personalized Music Editing `eqn:pdm`：\phi ' \in \text{arg min}_{\hat{\phi}} \mathbb{E}_{(x^{\text{ref}},y^{\text{ref}})\sim\mathcal{D}^{\text{ref}}…
- L154 §4.2 SteerMusic+: Personalized Music Editing：\begin{aligned} \min_{\theta}\;& \mathcal{L}_{\text{PDS}}(\phi ',\phi,x=g(\theta),y^{\text{tgt}},x^{\text{src}…
- L167 §4.2 SteerMusic+: Personalized Music Editing `eqn:psd_0`：~ \nabla_\theta \mathcal{L}_{\text{PDS-O}}(\phi ',\phi,x=g(\theta),y,x^{\text{src}},y^{\text{src}}) \\ = \unde…
- L179 §4.2 SteerMusic+: Personalized Music Editing `eqn:patch_personal`：\mathcal{L}_{\text{PCon}}(x,x^{\text{src}}) = \mathbb{E}_{h} [\sum_l \sum_{t'} \ell(h_l^{t'},h_l^{\text{src},t…
- L182 §4.2 SteerMusic+: Personalized Music Editing：\ell(h,h^+,h^-) = -\text{log}(\frac{\text{exp}(h\cdot h^+/\tau)}{\text{exp}(h\cdot h^+/\tau)+ \text{exp}(h\cdo…

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
