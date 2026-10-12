# 大纲 · High Fidelity Text-Guided Music Editing via Single-Stage Flow Matching

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L16 摘要
- L26–53 1 Introduction
- L54–168 2 Method
  - L70–75 2.1 Latent audio representation
  - L76–88 2.2 Conditional flow matching model
  - L89–102 2.3 Text-guided editing through latent inversion
  - L103–153 2.4 Regularized latent inversion
  - L154–168 2.5 Improving Flow Matching for text-to-music generation
    - L156–164 2.5.1 Codec bottleneck
    - L165–168 2.5.2 Minibatch coupling
- L169–218 3 Experimental setup
  - L170–180 3.1 Model
  - L181–188 3.2 Generation and editing
  - L189–205 3.3 Datasets
  - L206–218 3.4 Metrics
- L219–443 4 Results
  - L221–247 4.1 Text-guided music editing
  - L248–281 4.2 Text-to-music generation
  - L282–348 4.3 Latent Inversion
    - L283–318 4.3.1 Inversion methods
    - L319–348 4.3.2 Target inversion flow step
  - L349–379 4.4 Codec bottleneck regularizer
  - L380–443 4.5 FM design
    - L382–432 4.5.1 Model training
    - L433–443 4.5.2 Music editing quality/efficiency
- L444–465 5 Related work
  - L445–449 5.1 Audio representation
  - L450–456 5.2 Text-to-music generation
  - L457–465 5.3 Music editing
- L466–488 6 Discussion
- L488 —— 附录 ——
- L489–658 A Appendix
  - L491–532 A.1 Experimental setup
    - L493–500 A.1.1 Audio latent representation
    - L501–514 A.1.2 Flow matching model
    - L515–521 A.1.3 LLM-assisted editing prompt generation
    - L522–532 A.1.4 Subjective evaluation form
  - L533–658 A.2 Additional experiments
    - L535–542 A.2.1 Stereo codec
    - L543–589 A.2.2 Length generalization
    - L590–645 A.2.3 Text-to-music generation efficiency
    - L646–658 A.2.4 Classifier-free guidance

## 公式（4 个，按出现顺序；L 后面是所在小节）

- L79 §2.2 Conditional flow matching model：\mathbf{z}_t=t\mathbf{x} + (1-t)\mathbf{\epsilon}, t \in [0,1]\label{eq:fm_mixture}
- L81 §2.2 Conditional flow matching model：d\mathbf{z}_t/dt=v_{\Theta}(\mathbf{z}_t,t,c)=\mathbf{x}-\mathbf{\epsilon}
- L84 §2.2 Conditional flow matching model：\mathbf{x}_{generated}=\textbf{ODE}_{0\xrightarrow{}1}(\epsilon,c)
- L94 §2.3 Text-guided editing through latent inver：\mathbf{x}_{edit}=\textbf{ODE}_{t_{edit}\xrightarrow{}1}(\textbf{ODE}_{t_{edit}\xleftarrow{}1}(\mathbf{x}_{src…

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
