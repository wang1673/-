# 大纲 · FlowAlign: Trajectory-Regularized, Inversion-Free Flow-based Image Editing

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L31 摘要
- L40–66 1 Introduction
- L67–118 2 Backgrounds
- L119–290 3 FlowAlign
  - L120–162 3.1 Text-based Image Editing using Pre-trained Flow Models
  - L163–184 3.2 Trajectory Errors from Inversion-Free Approaches
  - L185–290 3.3 Trajectory Regularization using Similarity at Terminal Point
- L291–385 4 Experimental Results
- L386–406 5 Conclusion
- L399 —— 附录 ——
- L407–510 A Optimal Control Formulation to Prove Proposition \refprop:rectflow
- L511–547 B Implementation details
- L548–572 C Human preference test protocol
- L573–599 D Run-time comparison
- L600–655 E Additional evaluation results on PIEBench
  - L602–642 E.1 Quantitative and qualitative results
  - L643–655 E.2 Ablation
- L656–811 F Additional results
  - L660–684 F.1 Further Applications - Video Editing
  - L685–796 F.2 Further Applications - Gaussian Splatting Editing
  - L797–811 F.3 Further Variants - FLUX

## 公式（43 个，按出现顺序；L 后面是所在小节）

- L72 §2 Backgrounds `eqn:flowode`：d\psi_t(\vx) = \vv_t(\psi_t(\vx))dt
- L79 §2 Backgrounds `eq:fm`：\mathcal{L}_{FM} = \mathbb{E}_{t\in [0,1], \vx_t \sim p_t} \| \vv_t(\vx_t) - \vv_t^\theta(\vx_t) \|^2.
- L84 §2 Backgrounds `eq:cfm`：\mathcal{L}_{CFM} = \mathbb{E}_{t\in [0,1], \vx_0 \sim q} \| \vv_t(\vx_t|\vx_0) - \vv_t^\theta(\vx_t) \|^2
- L88 §2 Backgrounds `eq:condv`：\vv_t(\vx_t|\vx_0) = \dot\psi_t(\psi_t^{-1}(\vx_t|\vx_0)|\vx_0) = \dot\psi_t(\vx_1 |\vx_0) ,
- L96 §2 Backgrounds `eq:flowode`：d\vx = \vv_t^\theta(\vx_t) dt.
- L100 §2 Backgrounds：\vv_t(\vx_t|\vx_0) = \dot \psi_t(\psi_t^{-1}(\vx_t|\vx_0)|\vx_0) = \dot a_t \vx_0 + \dot b_t \vx_1.
- L123 §3.1 Text-based Image Editing using Pre-train `eqn:target_flow`：\psi_t(\vx_{src}|\vx_{tgt}) :=\vx_t = (1-t) \vx_{tgt} + t \vx_{src} \quad .
- L133 §3.1 Text-based Image Editing using Pre-train `eqn:forward_q, eqn:forward_p`：\psi_t^{src}(\epsilonb|\vx_{src}):=\vq_t &= (1-t) \vx_{src} + t \epsilonb, \\ \psi_t^{tgt}(\epsilonb|\vx_{tgt}…
- L140 §3.1 Text-based Image Editing using Pre-train `eq:aODE`：d\vq_t = \vv_t^{src}(\vq_t) dt ,\quad d\vq_t = \vv_t^{tgt}(\vp_t) dt
- L148 §3.1 Text-based Image Editing using Pre-train `eqn:constraint`：\vx_t = \vp_t -\vq_t + \vx_{src}, \quad \mbox{where}\quad \vx_1=\vx_{src}, \vx_0=\vx_{tgt}
- L153 §3.1 Text-based Image Editing using Pre-train `eqn:target_ode`：d\vx_t = d\vp_t - d\vq_t = [\vv_t^{tgt}(\vp_t) -\vv_t^{src}(\vq_t)]dt, \quad \mbox{where}\quad \vp_t:= \vq_t+\…
- L158 §3.1 Text-based Image Editing using Pre-train `eqn:simulation`：d\vx_t = [\vv_t^\theta(\vp_t, c_{tgt}) - \vv_t^\theta(\vq_t, c_{src})]dt.
- L166 §3.2 Trajectory Errors from Inversion-Free Ap `eq:pq`：d\vq_t = \vv_t^\theta(\vq_t,c_{src}) dt,\quad d\vp_t = \vv_t^\theta(\vp_t,c_{tgt}) dt
- L174 §3.2 Trajectory Errors from Inversion-Free Ap `eq:flowedit`：\vq_t = (1-t)\vx_{src} + t \epsilonb, \quad d\vp_t = \vv_t^\theta(\vq_t+\vx_t-\vx_{src},c_{tgt}) dt
- L188 §3.3 Trajectory Regularization using Similari `eq:ocx, eq:ocv`：\dot\vx_t &= \vu(\vx_t),\quad \vx_1 =\vx_{src} \\ V(\vu_t) &= \int_{0}^1 \ell (\vx_t,\vu_t,t) dt + m (\vx_0)
- L193 §3.3 Trajectory Regularization using Similari `eq:ell`：\ell (\vx_t,\vu_t,t) & := \frac{1}{2}\|\vu_t-\left(v_t^\theta(\vp_t, c_{tgt}) - \vv_t^\theta(\vq_t, c_{src})\r…
- L205 §3.3 Trajectory Regularization using Similari `eq:m`：\m(\vx_0)=\frac{\eta}{2}\|\vx_0-\vx_{{src}}\|^2 \quad
- L221 §3.3 Trajectory Regularization using Similari：d \vx_t &= \vv_t^\vx(\vp_t,\vq_t,\vp_0, \vq_0) dt
- L225 §3.3 Trajectory Regularization using Similari：\vv_t^\vx(\vp_t,\vq_t,\vp_0, \vq_0) &:\simeq \vv_t(\vp_t, c_{tgt}) - \vv_t(\vq_t, c_{src}) + \gamma \left(\mat…
- L232 §3.3 Trajectory Regularization using Similari `eqn:edit_reg`：\vv_t^\vx(\vp_t,\vq_t,\vp_0, \vq_0) := \underbrace{[\vv_t(\vp_t, c_{tgt}) - \vv_t(\vq_t, c_{src})]}_{\text{Sem…
- L248 §3.3 Trajectory Regularization using Similari `eqn:our_cfg`：\vv^\theta(\vp_t,c_{src},c_{tgt}) = \vv^\theta(\vp_t, c_{src}) + \omega\left[\vv^\theta(\vp_t, c_{tgt}) - \vv^…
- L255 §3.3 Trajectory Regularization using Similari `eqn:final`：d\vx_t = [\vv_t(\vp_t, c_{tgt}, c_{src}) - \vv_t(\vq_t, c_{src})]dt - \gamma dt (\mathbb{E}[\vq_0|\vq_t]-\math…
- L413 §A Optimal Control Formulation to Prove Pro：V(\vu_t) = \int_{0}^1 \ell (\vx_t,\vu_t,t) dt + m (\vx_1), & \quad \dot\vx_t = \vu(\vx_t) ,\quad \vx_{t_0} = \…
- L417 §A Optimal Control Formulation to Prove Pro：\ell (\vx_t,\vu_t,t) & := \frac{1}{2}\|\vu_t-\va_t \|^2 \\ m(\vx_1) &:= \frac{\eta}{2}\|\vx_0-\vx_{src}\|^2
- L422 §A Optimal Control Formulation to Prove Pro：\dot \vx_t = -\pb_t +\va_t
- L426 §A Optimal Control Formulation to Prove Pro：\pb_t = \frac{-\eta}{1-\eta t} \left(\vx_{t}+\vv_{t} -\vx_{src} \right) &\quad \mbox{where} \quad \vv_t:= \int…
- L434 §A Optimal Control Formulation to Prove Pro：H(\vx_t,\vu_t,\pb_t,t):= \frac{1}{2}\|\vu_t-\va_t \|^2 + \pb_t^T\ub_t
- L438 §A Optimal Control Formulation to Prove Pro：\vu_t^*=\va_t-\pb_t
- L442 §A Optimal Control Formulation to Prove Pro：H(\vx_t,\vu^*_t,\pb_t,t) := & -\frac{1}{2}\|\vp_t\|^2+ \pb_t^T\va_t
- L446 §A Optimal Control Formulation to Prove Pro `eq:pb`：\dot \vx_t &= \vu_t^*=\va_t-\pb_t \\ \dot \pb_t &= - \frac{\partial H(\vx_t,\vu^*_t,\pb_t,t) }{\partial \vx} =…
- L452 §A Optimal Control Formulation to Prove Pro `eq:pb1`：\vx_{t_0} = \vx_{start}, &\quad \pb_0 = \left. \frac{\partial m(\vx_t,t)}{\partial \vx_t}\right|_{t=0} = \eta …
- L457 §A Optimal Control Formulation to Prove Pro：\vx_0 &= \vx_{t_0} + \int_{t_0}^0 -\pb +\va_tdt \\ &= t_0 \pb + \vx_{t_0} +\vv_{t_0}
- L462 §A Optimal Control Formulation to Prove Pro：\vv_{t_0}:= \int_{t_0}^0 \va_t dt
- L466 §A Optimal Control Formulation to Prove Pro：\pb = \eta\left( t_0 \pb + \vx_{t_0} +\vv_{t_0}-\vx_{src} \right) &\quad \Rightarrow \pb = \frac{\eta(\vx_{t_0…
- L470 §A Optimal Control Formulation to Prove Pro：\vu_t^* &= \va_t + \frac{-\eta}{1-\eta t} \left(\vx_{t}+\vv_{t} -\vx_{src} \right)
- L480 §A Optimal Control Formulation to Prove Pro：\va_t := \vv_t^\theta(\vp_t, \vc_{tgt}) - \vv_t^\theta(\vq_t, \vc_{src})
- L484 §A Optimal Control Formulation to Prove Pro：\vv_{t} &= \int_t^0 \va_t dt = \int_t^0 \vv_t(\vp_t) -\vv_t(\vq_t) dt \\ &\simeq -t \vv_t(\vp_t) + t \vv_t (\v…
- L489 §A Optimal Control Formulation to Prove Pro：\vx_{t}+\vv_{t} -\vx_{src} &= \vp_t-\vq_t +\vv_t \notag\\ &\simeq \vp_t-\vq_t + (-t \vv_t(\vp_t) + t \vv_t (\v…
- L497 §A Optimal Control Formulation to Prove Pro：\vu_t^* &= \va_t + \frac{-\eta}{1-\eta t} \left(\vx_{t}+\vv_{t} -\vx_{src} \right) \notag\\ &\simeq \va_t +\fr…
- L503 §A Optimal Control Formulation to Prove Pro `eqn:final_drift`：\dot \vx_t &= \vv_t(\vp_t, \vc_{tgt}) - \vv_t(\vq_t, \vc_{src}) +\frac{-\eta}{1-\eta t} \left(\mathbb{E}[\vp_0…
- L692 §F.2 Further Applications - Gaussian Splattin：\nabla_{\vx_t} \mathcal{L}_{FA} := \vv_t(\vp_t, \vc_{tgt}) - \vv_t (\vq_t, \vc_{src}) + \gamma (\mathbb{E}[\vp…
- L703 §F.2 Further Applications - Gaussian Splattin `eqn:gauss_grad`：\nabla_{\psi} \mathcal{L}_{FA} &:=\left[ \nabla_{\vx_t}\mathcal{L}_{FA}\right]\frac{\partial \vx_t}{\partial \…
- L710 §F.2 Further Applications - Gaussian Splattin：\psi = \psi - \eta_t \nabla_\psi \mathcal{L}_{FA}.

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
