# 大纲 · Emo-DPO: Controllable Emotional Speech Synthesis through Direct Preference Optimization

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L34 摘要
- L44–73 1 Introduction
- L74–156 2 Methodology
  - L79–83 2.1 Emo-DPO Overview
  - L84–99 2.2 Instruction Tuning
  - L100–156 2.3 Emo-Direct Preference Optimization Training
    - L104–116 2.3.1 Beyond One Emotion - DPO Training
    - L117–156 2.3.2 Emo-DPO Training Objective
- L157–174 3 Experiments
  - L159–163 3.1 Datasets and Experimental Setup
  - L164–174 3.2 Evaluation Metrics
- L175–229 4 Results and Discussion
  - L179–192 4.1 Effectiveness of Emo-DPO training on LLM-TTS
  - L193–229 4.2 Ablation Study
- L230–236 5 Conclusion

## 公式（5 个，按出现顺序；L 后面是所在小节）

- L88 §2.2 Instruction Tuning：d_j \in D_\texttt{sft} = E. \texttt{<endofprompt>} x_j \texttt{</s>} y_j^{+} \texttt{</s>}
- L94 §2.2 Instruction Tuning：\mathcal{L}_{KL} = KL(P_{\pi}||P) = \mathbb{E}_{d_j\sim D_\texttt{sft}} \left[ p(y^+_j | E, x_j) \log \frac{p(…
- L108 §2.3.1 Beyond One Emotion - DPO Training：\begin{aligned} \mathcal{L}_{\texttt{DPO}}(\pi; \pi_{\texttt{sft}}) = -\mathbb{E}_{(d_j^+, d_j^-) \sim D_\text…
- L120 §2.3.2 Emo-DPO Training Objective：\begin{aligned} &\text{(1) logits} = logratio_{\texttt{chosen}} - logratio_{\texttt{reject}} \\ &= \log \left(…
- L135 §2.3.2 Emo-DPO Training Objective：\mathcal{L} = \alpha \mathcal{L}_{\texttt{DPO}} + \gamma \mathcal{L}_{\texttt{KL}} + \theta \mathcal{L}_{\text…

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
