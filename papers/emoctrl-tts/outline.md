# 大纲 · Laugh Now Cry Later: Controlling Time-Varying Emotional States of Flow-Matching-Based Zero-Shot Text-to-Speech

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L8 摘要
- L17–45 1 Introduction
- L46–140 2 Related Work
  - L50–102 2.1 Controlling emotion in TTS
  - L103–140 2.2 Flow-matching-based TTS
    - L105–120 2.2.1 Conditional flow matching
    - L121–128 2.2.2 Voicebox
    - L129–140 2.2.3 ELaTE
- L141–237 3 EmoCtrl-TTS
  - L145–187 3.1 Overview
    - L149–162 3.1.1 Model training
    - L163–187 3.1.2 Inference
  - L188–196 3.2 NV embeddings
  - L197–226 3.3 Emotion embeddings
  - L227–237 3.4 Collecting large-scale emotional data with pseudo-labeling
- L238–634 4 Experiments
  - L243–318 4.1 Data
    - L246–260 4.1.1 Training data
    - L261–318 4.1.2 Evaluation data
  - L319–437 4.2 Evaluation metrics
    - L322–343 4.2.1 Objective evaluation metrics
    - L344–437 4.2.2 Subjective evaluation metrics
  - L438–454 4.3 Model configuration
  - L455–545 4.4 S2ST pipeline
  - L546–634 4.5 Results and discussion
    - L550–579 4.5.1 Objective evaluation
    - L580–605 4.5.2 Subjective evaluation
    - L606–626 4.5.3 Impact of training configurations
    - L627–634 4.5.4 Results on real laughter and crying data
- L635–642 5 Conclusions

## 公式（1 个，按出现顺序；L 后面是所在小节）

- L114 §2.2.1 Conditional flow matching：\mathcal{L}^{\rm CFM}(\theta)=\mathbb{E}_{t,q(x_1), p_t(x|x_1)}||u_t(x|x_1)-v_t(x;\theta)||^2,

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
