# 大纲 · FlowEdit: Inversion-Free Text-Based Editing Using Pre-Trained Flow Models

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L21 摘要
- L28–39 1 Introduction
- L40–63 2 Related work
- L64–101 3 Preliminaries
  - L67–82 3.1 Rectified Flow models
  - L83–101 3.2 Image editing using ODE inversion
- L102–139 4 Reinterpretation of editing by inversion
- L140–235 5 \ours
  - L184–217 5.1 Practical considerations
  - L218–224 5.2 Relation to optimization based methods
  - L225–235 5.3 Comparison to editing by (exact) inversion
- L236–287 6 Experiments
- L288–314 7 Conclusion and limitations
- L315–326 8 Additional results
- L327–474 9 Comparisons
  - L329–340 9.1 Additional qualitative comparisons
  - L341–428 9.2 Additional details on the experiment settings
    - L349–368 9.2.1 Stable Diffusion 3 hyperparameters
    - L369–428 9.2.2 FLUX hyperparameters
  - L429–474 9.3 Metrics comparisons
- L475–488 10 Effect of n_\textmax
- L489–522 11 Text-based style editing
- L523–548 12 Hyperparmeters used for Fig. \reffig:teaser
- L549–583 13 Full Algorithm
- L584–597 14 Limitations
- L598–621 15 Effect of random noise on the results
- L622–643 16 Effect of source prompt on the results
- L644–708 17 Illustration of the noise-free path between the source and target distributions
- L709–725 18 Effect of n_\textavg
- L726–806 19 Further discussion on the relation to optimization based methods
  - L735–757 19.1 Delta denoising loss
  - L758–773 19.2 \ours with different step sizes
  - L774–806 19.3 Mathematical discrepancies between the \ours, DDS, PDS update steps
- L807–833 20 Additional details about the Cats-Dogs experiment

## 公式（13 个，按出现顺序；L 后面是所在小节）

- L69 §3.1 Rectified Flow models `eq:flow_orig`：dZ_t=V(Z_t, t) \,dt.
- L75 §3.1 Rectified Flow models `eq:linear_interpolant`：Z_t \sim (1-t) X_0 + t X_1.
- L87 §3.2 Image editing using ODE inversion `eq:inv_edit_fwd`：dZ^{\text{src}}_t= V^{\text{src}}(Z^{\text{src}}_t,t)\,dt,
- L93 §3.2 Image editing using ODE inversion `eq:inv_edit_rev`：dZ^{\text{tar}}_t = V^{\text{tar}}(Z^{\text{tar}}_t,t)\,dt,
- L110 §4 Reinterpretation of editing by inversion `eq:direct_coupling`：Z^{\text{inv}}_t=Z^{\text{src}}_0+Z^{\text{tar}}_t-Z^{\text{src}}_t.
- L118 §4 Reinterpretation of editing by inversion `eq:direct_coupling_ODE`：dZ^{\text{inv}}_t= V^{\Delta}_{t}(Z^{\text{src}}_{t},Z^{\text{tar}}_{t})\,dt,
- L123 §4 Reinterpretation of editing by inversion `eq:direct_coupling_ODE_combined`：dZ^{\text{inv}}_t= V^{\Delta}_{t}(Z^{\text{src}}_{t},Z^{\text{inv}}_t+Z^{\text{src}}_t-Z^{\text{src}}_0)\,dt
- L150 §5 \ours `eq:our_marginals`：\hat{Z}^{\text{src}}_{t} =(1-t)Z_0^{\text{src}}+tN_{t},
- L155 §5 \ours `eq:our_ODE`：dZ^{\text{FE}}_t= \mathbb{E}\left[V^{\Delta}_{t}(\hat{Z}^{\text{src}}_{t},Z^{\text{FE}}_t+\hat{Z}^{\text{src}}…
- L739 §19.1 Delta denoising loss `eq:ddloss`：\mathcal{L}_{\text{DD}}(\phi,\mathbf{z},y,\mathbf{\hat{z}},\hat{y},\epsilon)= \int_0^1\| \epsilon^\omega(\math…
- L778 §19.3 Mathematical discrepancies between the \：V(x_t,t)&= \mathbb{E}[\epsilon-X_0|X_t=x_t] \nonumber \\ &= \frac{1}{1-t}\mathbb{E}[(1-t)\epsilon-(1-t)X_0|X_t…
- L786 §19.3 Mathematical discrepancies between the \：V^{\Delta}_{t}(\hat{Z}^{\text{src}}_{t},\hat{Z}^{\text{tar}}_{t}) &= V^{\text{tar}}(\hat{Z}^{\text{tar}}_{t},t…
- L798 §19.3 Mathematical discrepancies between the \：\nabla\mathcal{L}_{\text{PDS}}=\psi(t)(Z^{\text{PDS}}_t -X^{\text{src}}_0)+\chi(t)(\hat{\epsilon}(Z^{\text{tar…

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
