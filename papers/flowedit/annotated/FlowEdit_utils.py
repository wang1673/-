# 中文精读注释版：只添加注释，原始语句与文档字符串保持不变。
# 上游：https://github.com/fallenshock/FlowEdit  commit=2620a9364f0f9c21368c36266e6200ff250273ec
# 原文对应：§3.1 RF 时间约定；§4 反演重写；§5 直接编辑与 §5.1 实用设置；附录 Full Algorithm。
# 原始行号请看 code-used/；注释会使本文件行号发生偏移。
from typing import Optional, Tuple, Union
import torch
from diffusers import FlowMatchEulerDiscreteScheduler
from tqdm import tqdm
import numpy as np

from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion import retrieve_timesteps



# 【中文精读｜原文件 L11】RF 解析前向核：(1−sigma)sample+sigma·noise。它不需要 UNet 反演。
def scale_noise(
    scheduler,
    sample: torch.FloatTensor,
    timestep: Union[float, torch.FloatTensor],
    noise: Optional[torch.FloatTensor] = None,
) -> torch.FloatTensor:
    """
    Foward process in flow-matching

    Args:
        sample (`torch.FloatTensor`):
            The input sample.
        timestep (`int`, *optional*):
            The current timestep in the diffusion chain.

    Returns:
        `torch.FloatTensor`:
            A scaled input sample.
    """
    # if scheduler.step_index is None:
    scheduler._init_step_index(timestep)

    # 【深入注释｜原文件 L33】scheduler.step_index 指向当前噪声级；sigma 是插值系数，式 (1−sigma)x+sigmaε 不调用反演网络。
    sigma = scheduler.sigmas[scheduler.step_index]
    sample = sigma * noise + (1.0 - sigma) * sample

    return sample


# for flux
def calculate_shift(
    image_seq_len,
    base_seq_len: int = 256,
    max_seq_len: int = 4096,
    base_shift: float = 0.5,
    max_shift: float = 1.16,
):
    m = (max_shift - base_shift) / (max_seq_len - base_seq_len)
    b = base_shift - m * base_seq_len
    mu = image_seq_len * m + b
    return mu



# 【中文精读｜原文件 L54】源/目标各带一个无条件分支，合计四份 batch。一次批量 transformer 前向后分别计算两组 CFG。
def calc_v_sd3(pipe, src_tar_latent_model_input, src_tar_prompt_embeds, src_tar_pooled_prompt_embeds, src_guidance_scale, tar_guidance_scale, t):
    # broadcast to batch dimension in a way that's compatible with ONNX/Core ML
    timestep = t.expand(src_tar_latent_model_input.shape[0])
    # joint_attention_kwargs = {}
    # # add timestep to joint_attention_kwargs
    # joint_attention_kwargs["timestep"] = timestep[0]
    # joint_attention_kwargs["timestep_idx"] = i


    with torch.no_grad():
        # # predict the noise for the source prompt
        noise_pred_src_tar = pipe.transformer(
            hidden_states=src_tar_latent_model_input,
            timestep=timestep,
            encoder_hidden_states=src_tar_prompt_embeds,
            pooled_projections=src_tar_pooled_prompt_embeds,
            joint_attention_kwargs=None,
            return_dict=False,
        )[0]

        # perform guidance source
        # 【深入注释｜原文件 L75】SD3 的 batch 次序为源无条件、源文字、目标无条件、目标文字；下面的 chunk(4) 必须与这个顺序一致。
        if pipe.do_classifier_free_guidance:
            src_noise_pred_uncond, src_noise_pred_text, tar_noise_pred_uncond, tar_noise_pred_text = noise_pred_src_tar.chunk(4)
            noise_pred_src = src_noise_pred_uncond + src_guidance_scale * (src_noise_pred_text - src_noise_pred_uncond)
            noise_pred_tar = tar_noise_pred_uncond + tar_guidance_scale * (tar_noise_pred_text - tar_noise_pred_uncond)

    return noise_pred_src, noise_pred_tar



# 【中文精读｜原文件 L84】对给定条件和时间查询 FLUX 速度；t/1000 是模型接口归一化，不是 Euler 步长。
def calc_v_flux(pipe, latents, prompt_embeds, pooled_prompt_embeds, guidance, text_ids, latent_image_ids, t):
    # broadcast to batch dimension in a way that's compatible with ONNX/Core ML
    timestep = t.expand(latents.shape[0])
    # joint_attention_kwargs = {}
    # # add timestep to joint_attention_kwargs
    # joint_attention_kwargs["timestep"] = timestep[0]
    # joint_attention_kwargs["timestep_idx"] = i


    with torch.no_grad():
        # # predict the noise for the source prompt
        noise_pred = pipe.transformer(
            hidden_states=latents,
            timestep=timestep / 1000,
            guidance=guidance,
            encoder_hidden_states=prompt_embeds,
            txt_ids=text_ids,
            img_ids=latent_image_ids,
            pooled_projections=pooled_prompt_embeds,
            joint_attention_kwargs=None,
            return_dict=False,
        )[0]

    return noise_pred



@torch.no_grad()
# 【中文精读｜原文件 L112】§5 / Full Algorithm 的 SD3 实现。x_src 固定、zt_edit 为编辑状态，源查询解析加噪，目标查询加完整编辑位移。
# 【中文精读｜原文件 L112】n_max 跳过高噪声早期；n_avg 平均预测差；n_min 触发普通目标采样末段。
def FlowEditSD3(pipe,
    scheduler,
    x_src,
    src_prompt,
    tar_prompt,
    negative_prompt,
    T_steps: int = 50,
    n_avg: int = 1,
    src_guidance_scale: float = 3.5,
    tar_guidance_scale: float = 13.5,
    n_min: int = 0,
    n_max: int = 15,):
    
    device = x_src.device

    # 【深入注释｜原文件 L127】取实际 scheduler 时间表；T_steps 是离散查询数，后面的 t/1000 才是此实现使用的连续时间。
    timesteps, T_steps = retrieve_timesteps(scheduler, T_steps, device, timesteps=None)

    num_warmup_steps = max(len(timesteps) - T_steps * scheduler.order, 0)
    pipe._num_timesteps = len(timesteps)
    pipe._guidance_scale = src_guidance_scale
    
    # src prompts
    (
        src_prompt_embeds,
        src_negative_prompt_embeds,
        src_pooled_prompt_embeds,
        src_negative_pooled_prompt_embeds,
    ) = pipe.encode_prompt(
        prompt=src_prompt,
        prompt_2=None,
        prompt_3=None,
        negative_prompt=negative_prompt,
        do_classifier_free_guidance=pipe.do_classifier_free_guidance,
        device=device,
    )

    # tar prompts
    # 【深入注释｜原文件 L149】编码目标描述前暂时切换 guidance，源/目标 CFG 可独立调节；这里仍使用同一套冻结模型。
    pipe._guidance_scale = tar_guidance_scale
    (
        tar_prompt_embeds,
        tar_negative_prompt_embeds,
        tar_pooled_prompt_embeds,
        tar_negative_pooled_prompt_embeds,
    ) = pipe.encode_prompt(
        prompt=tar_prompt,
        prompt_2=None,
        prompt_3=None,
        negative_prompt=negative_prompt,
        do_classifier_free_guidance=pipe.do_classifier_free_guidance,
        device=device,
    )
 
    # CFG prep
    # 【深入注释｜原文件 L165】两个文字条件和两个无条件嵌入按速度查询 batch 次序拼接，不能把源和目标 prompt 交换。
    src_tar_prompt_embeds = torch.cat([src_negative_prompt_embeds, src_prompt_embeds, tar_negative_prompt_embeds, tar_prompt_embeds], dim=0)
    src_tar_pooled_prompt_embeds = torch.cat([src_negative_pooled_prompt_embeds, src_pooled_prompt_embeds, tar_negative_pooled_prompt_embeds, tar_pooled_prompt_embeds], dim=0)
    
    # initialize our ODE Zt_edit_1=x_src
    # 【深入注释｜原文件 L169】编辑变量 y₁ 初始化为原图 latent；它是累积编辑位移的状态，不是需要反演出的噪声端点。
    zt_edit = x_src.clone()

    for i, t in tqdm(enumerate(timesteps)):
        
        # 【深入注释｜原文件 L173】n_max 让最早的高噪声时间点跳过更新；改变它会同时影响编辑强度和源结构保留。
        if T_steps - i > n_max:
            continue
        
        # 【深入注释｜原文件 L176】SD3 的整数时间戳缩放到 [0,1]；Euler 更新用的是相邻连续时间之差。
        t_i = t/1000
        if i+1 < len(timesteps): 
            t_im1 = (timesteps[i+1])/1000
        else:
            t_im1 = torch.zeros_like(t_i).to(t_i.device)
        
        # 【深入注释｜原文件 L182】只有剩余步数大于 n_min 时执行源/目标速度差 ODE；末 n_min 步切换目标单流采样。
        if T_steps - i > n_min:

            # Calculate the average of the V predictions
            V_delta_avg = torch.zeros_like(x_src)
            for k in range(n_avg):

                # 【深入注释｜原文件 L188】每个时间点重新取同形高斯 ε；源与目标查询共享这一份 ε，n_avg 会重复此配对并平均。
                fwd_noise = torch.randn_like(x_src).to(x_src.device)
                
                # 【中文精读｜原文件 L190】源查询 q=(1−t)x_src+tε，每个 Monte Carlo 样本重新构造。
                # 【深入注释｜原文件 L190】q_t=(1−t)x_src+tε 是源样本的解析加噪状态；x_src 在全部迭代中固定。
                zt_src = (1-t_i)*x_src + (t_i)*fwd_noise

                # 【中文精读｜原文件 L192】目标 p=y+q−x_src；完整编辑位移不乘 (1−t)。
                # 【深入注释｜原文件 L192】p_t=y_t+q_t−x_src；把当前编辑位移 y_t−x_src 加到同噪声源查询上，是论文直接 ODE 的关键耦合。
                zt_tar = zt_edit + zt_src - x_src

                # 【深入注释｜原文件 L194】四个 latent 的 batch 排序与上面的条件嵌入排序配对；此处非 CFG 分支的容器类型也应单独核查。
                src_tar_latent_model_input = torch.cat([zt_src, zt_src, zt_tar, zt_tar]) if pipe.do_classifier_free_guidance else (zt_src, zt_tar) 

                Vt_src, Vt_tar = calc_v_sd3(pipe, src_tar_latent_model_input,src_tar_prompt_embeds, src_tar_pooled_prompt_embeds, src_guidance_scale, tar_guidance_scale, t)

                # 【中文精读｜原文件 L198】平均目标速度减源速度；CFG 后再求差。
                # 【深入注释｜原文件 L198】Δv=平均(v_target(p_t)−v_source(q_t))；平均的是速度差，不是先平均两个独立图像。
                V_delta_avg += (1/n_avg) * (Vt_tar - Vt_src) # - (hfg-1)*( x_src))

            # propagate direct ODE
            zt_edit = zt_edit.to(torch.float32)

            # 【中文精读｜原文件 L203】时间下降，因此括号内 dt 为负；切勿额外再手动取负。
            # 【深入注释｜原文件 L203】Euler 步：y_{i+1}=y_i+(t_{i+1}−t_i)Δv；时间向数据端下降，所以增量通常为负。
            zt_edit = zt_edit + (t_im1 - t_i) * V_delta_avg
            
            zt_edit = zt_edit.to(V_delta_avg.dtype)

        else: # i >= T_steps-n_min # regular sampling for last n_min steps

            if i == T_steps-n_min:
                # initialize SDEDIT-style generation phase
                fwd_noise = torch.randn_like(x_src).to(x_src.device)
                # 【深入注释｜原文件 L212】切换普通采样时只在边界重新加噪一次，然后以目标条件继续积分。
                xt_src = scale_noise(scheduler, x_src, t, noise=fwd_noise)
                xt_tar = zt_edit + xt_src - x_src
                
            src_tar_latent_model_input = torch.cat([xt_tar, xt_tar, xt_tar, xt_tar]) if pipe.do_classifier_free_guidance else (xt_src, xt_tar)

            _, Vt_tar = calc_v_sd3(pipe, src_tar_latent_model_input,src_tar_prompt_embeds, src_tar_pooled_prompt_embeds, src_guidance_scale, tar_guidance_scale, t)

            xt_tar = xt_tar.to(torch.float32)

            # 【深入注释｜原文件 L221】目标单流末段的 Euler 候选；原码下一行引用本函数未定义的 noise_pred_tar，n_min>0 需先修复。
            prev_sample = xt_tar + (t_im1 - t_i) * (Vt_tar)

            # 【中文精读｜原文件 L223】静态问题：SD3 该分支 noise_pred_tar 未定义；n_min>0 时可能报错。此注释不修复上游。
            prev_sample = prev_sample.to(noise_pred_tar.dtype)

            xt_tar = prev_sample
        
    return zt_edit if n_min == 0 else xt_tar



@torch.no_grad()
# 【中文精读｜原文件 L232】同一差分 ODE 的 FLUX 适配：latent 先打包，时间取 scheduler sigma，最后 unpack。
# 【中文精读｜原文件 L232】FLUX guidance embedding 不等价于 SD3 的四分支外部 CFG；不能直接对比数值。
def FlowEditFLUX(pipe,
    scheduler,
    x_src,
    src_prompt,
    tar_prompt,
    negative_prompt,
    T_steps: int = 28,
    n_avg: int = 1,
    src_guidance_scale: float = 1.5,
    tar_guidance_scale: float = 5.5,
    n_min: int = 0,
    n_max: int = 24,):

    device = x_src.device
    orig_height, orig_width = x_src.shape[2]*pipe.vae_scale_factor//2, x_src.shape[3]*pipe.vae_scale_factor//2
    num_channels_latents = pipe.transformer.config.in_channels // 4

    pipe.check_inputs(
        prompt=src_prompt,
        prompt_2=None,
        height=orig_height,
        width=orig_width,
        callback_on_step_end_tensor_inputs=None,
        max_sequence_length=512,
    )

    x_src, latent_src_image_ids = pipe.prepare_latents(batch_size= x_src.shape[0], num_channels_latents=num_channels_latents, height=orig_height, width=orig_width, dtype=x_src.dtype, device=x_src.device, generator=None,latents=x_src)
    x_src_packed = pipe._pack_latents(x_src, x_src.shape[0], num_channels_latents, x_src.shape[2], x_src.shape[3])
    latent_tar_image_ids = latent_src_image_ids

    # 5. Prepare timesteps
    # 【深入注释｜原文件 L263】FLUX 自建 sigma 网格并交给 scheduler；与 SD3 的 t/1000 约定不能混用。
    sigmas = np.linspace(1.0, 1 / T_steps, T_steps)
    image_seq_len = x_src_packed.shape[1]
    mu = calculate_shift(
        image_seq_len,
        scheduler.config.base_image_seq_len,
        scheduler.config.max_image_seq_len,
        scheduler.config.base_shift,
        scheduler.config.max_shift,
    )
    timesteps, T_steps = retrieve_timesteps(
        scheduler,
        T_steps,
        device,
        timesteps=None,
        sigmas=sigmas,
        mu=mu,
        )
    
    num_warmup_steps = max(len(timesteps) - T_steps * pipe.scheduler.order, 0)
    pipe._num_timesteps = len(timesteps)

    
    # src prompts
    (
        src_prompt_embeds,
        src_pooled_prompt_embeds,
        src_text_ids,

    ) = pipe.encode_prompt(
        prompt=src_prompt,
        prompt_2=None,
        device=device,
    )

    # tar prompts
    pipe._guidance_scale = tar_guidance_scale
    (
        tar_prompt_embeds,
        tar_pooled_prompt_embeds,
        tar_text_ids,
    ) = pipe.encode_prompt(
        prompt=tar_prompt,
        prompt_2=None,
        device=device,
    )

    # handle guidance
    # 【深入注释｜原文件 L310】FLUX 使用模型内部 guidance embedding，此值不能直接当作 SD3 外部四分支 CFG 系数。
    if pipe.transformer.config.guidance_embeds:
        src_guidance = torch.tensor([src_guidance_scale], device=device)
        src_guidance = src_guidance.expand(x_src_packed.shape[0])
        tar_guidance = torch.tensor([tar_guidance_scale], device=device)
        tar_guidance = tar_guidance.expand(x_src_packed.shape[0])
    else:
        src_guidance = None
        tar_guidance = None

    # initialize our ODE Zt_edit_1=x_src
    zt_edit = x_src_packed.clone()

    for i, t in tqdm(enumerate(timesteps)):
        
        if T_steps - i > n_max:
            continue
        
        scheduler._init_step_index(t)
        # 【深入注释｜原文件 L328】真正用于 FLUX 数值更新的是 scheduler.sigmas[step_index]，而非仅看循环变量 t 的字面值。
        t_i = scheduler.sigmas[scheduler.step_index]
        if i < len(timesteps):
            t_im1 = scheduler.sigmas[scheduler.step_index + 1]
        else:
            t_im1 = t_i
        
        if T_steps - i > n_min:

            # Calculate the average of the V predictions
            V_delta_avg = torch.zeros_like(x_src_packed)

            for k in range(n_avg):
                                    

                fwd_noise = torch.randn_like(x_src_packed).to(x_src_packed.device)
                
                # 【中文精读｜原文件 L344】源查询 q=(1−t)x_src+tε，每个 Monte Carlo 样本重新构造。
                # 【深入注释｜原文件 L344】FLUX 的源查询也用共享噪声 q_t=(1−sigma)x_src+sigmaε，latent 已打包成 token。
                zt_src = (1-t_i)*x_src_packed + (t_i)*fwd_noise

                # 【中文精读｜原文件 L346】目标 p=y+q−x_src；完整编辑位移不乘 (1−t)。
                # 【深入注释｜原文件 L346】目标查询加上完整编辑位移；不是把 y_t 再做一次普通前向加噪。
                zt_tar = zt_edit + zt_src - x_src_packed

                # Merge in the future to avoid double computation
                Vt_src = calc_v_flux(pipe,
                                                    latents=zt_src,
                                                    prompt_embeds=src_prompt_embeds, 
                                                    pooled_prompt_embeds=src_pooled_prompt_embeds, 
                                                    guidance=src_guidance,
                                                    text_ids=src_text_ids, 
                                                    latent_image_ids=latent_src_image_ids, 
                                                    t=t)
                
                Vt_tar = calc_v_flux(pipe,
                                                    latents=zt_tar,
                                                    prompt_embeds=tar_prompt_embeds, 
                                                    pooled_prompt_embeds=tar_pooled_prompt_embeds, 
                                                    guidance=tar_guidance,
                                                    text_ids=tar_text_ids, 
                                                    latent_image_ids=latent_tar_image_ids, 
                                                    t=t)

                # 【中文精读｜原文件 L367】平均目标速度减源速度；CFG 后再求差。
                # 【深入注释｜原文件 L367】多个随机耦合得到的速度差求平均；n_avg 增大增加模型查询与计算成本。
                V_delta_avg += (1/n_avg) * (Vt_tar - Vt_src) # - (hfg-1)*( x_src))

            # propagate direct ODE
            zt_edit = zt_edit.to(torch.float32)

            # 【中文精读｜原文件 L372】时间下降，因此括号内 dt 为负；切勿额外再手动取负。
            # 【深入注释｜原文件 L372】打包 latent 上直接做差分 Euler 步；t_next−t 由 sigma 网格决定。
            zt_edit = zt_edit + (t_im1 - t_i) * V_delta_avg

            zt_edit = zt_edit.to(V_delta_avg.dtype)

        else: # i >= T_steps-n_min # regular sampling last n_min steps

            if i == T_steps-n_min:
                # initialize SDEDIT-style generation phase
                fwd_noise = torch.randn_like(x_src_packed).to(x_src_packed.device)
                xt_src = scale_noise(scheduler, x_src_packed, t, noise=fwd_noise)
                xt_tar = zt_edit + xt_src - x_src_packed
                
            Vt_tar = calc_v_flux(pipe,
                                    latents=xt_tar,
                                    prompt_embeds=tar_prompt_embeds, 
                                    pooled_prompt_embeds=tar_pooled_prompt_embeds, 
                                    guidance=tar_guidance,
                                    text_ids=tar_text_ids, 
                                    latent_image_ids=latent_tar_image_ids, 
                                    t=t)


            xt_tar = xt_tar.to(torch.float32)

            prev_sample = xt_tar + (t_im1 - t_i) * (Vt_tar)

            prev_sample = prev_sample.to(Vt_tar.dtype)
            xt_tar = prev_sample
    # 【深入注释｜原文件 L400】返回前将 FLUX token latent 解包给 VAE；输出仍是图像 latent，而不是波形或音乐 latent。
    out = zt_edit if n_min == 0 else xt_tar
    unpacked_out = pipe._unpack_latents(out, orig_height, orig_width, pipe.vae_scale_factor)
    return unpacked_out


