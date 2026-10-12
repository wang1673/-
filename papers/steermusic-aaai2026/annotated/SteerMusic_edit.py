# 中文精读注释版：只添加注释，原始语句与文档字符串保持不变。
# 上游：https://github.com/sony/steermusic  commit=9d2008b8515f9c8a83c956ddb23ab83b55e19709
# 原文对应：§3 DDS（eqn:dds）；§4.1 g(θ)=θ；§4.2 PDS-O（eqn:psd_0）与 PCon（eqn:patch_personal）。
# 原始行号请看 code-used/；注释会使本文件行号发生偏移。
# %%
import torch
from tqdm import tqdm
import steermusic_utils
import numpy as np
import os
import yaml
from scipy.io.wavfile import write
import torch.nn.functional as F
from preprocessor import Preprocessor
import argparse

device = "cuda:0"

parser = argparse.ArgumentParser()
parser.add_argument('--audio_path', type=str)
parser.add_argument('--prompt', type=str)
parser.add_argument('--prompt_ref', default='', type=str)
parser.add_argument('--output_dir', default='./SteerMusic_output/', type=str)
parser.add_argument('--validation_step', default=400, type=int)
parser.add_argument('--guidance_scale', default=30, type=int)
parser.add_argument('--weight_aug', default=2, type=int)
opt = parser.parse_args()

audio_name = opt.audio_path
prompt_ref = opt.prompt_ref
prompt = opt.prompt
weight_aug = opt.weight_aug
guidance_scale = opt.guidance_scale
validation_step = opt.validation_step
# Result store path
output_dir = opt.output_dir
os.makedirs(output_dir, exist_ok=True)


# Read config
config_yaml = f"config/autoencoder/16k_64.yaml"
exp_name = os.path.basename(config_yaml.split(".")[0])
exp_group_name = os.path.basename(os.path.dirname(config_yaml))

config_yaml = os.path.join(config_yaml)
config_yaml = yaml.load(open(config_yaml, "r"), Loader=yaml.FullLoader)

# Obtain preprocessor
preprocessor = Preprocessor(config_yaml)

# Load guidance model
guidance_model = steermusic_utils.AudioLDM2_pipe(device, fp16=False, vram_O=False, t_range=[0.02, 0.98]) # You can adjust t_range
guidance_model.eval()


# 【中文精读｜原文件 L52】§4.1：只更新 latent；源 latent 与模型参数冻结。每轮随机 t/noise 与源分支共享。
# 【中文精读｜原文件 L52】注意保存发生在 optim.step 前：默认最后保存对应 400 次更新，循环实际执行 401 次。
def SteerMusic_editing(audio_name,prompt_ref,prompt,weight_aug,validation_step,guidance_model=guidance_model, preprocessor=preprocessor,guidance_scale = 15, device = "cuda:7"):
    # 【深入注释｜原文件 L53】源音频读为 log-mel，再加 batch/channel 轴送入 AudioLDM2 VAE。
    log_mel_spec, _, _, _  = preprocessor.read_audio_file(filename=audio_name)
    log_mel_spec = log_mel_spec.unsqueeze(0).unsqueeze(0).to(device)

    for p in guidance_model.parameters():
        p.requires_grad = False

    log_mel_spec.requires_grad = False

    # Obtain latent size at first 
    lt = guidance_model.encode_audio(log_mel_spec)
    as_latent = True
    latent_size = 16 # need to adjust!
    # 【中文精读｜原文件 L65】可优化变量形状 [1,8,T,16]；后面复制源 latent 初始化，而非从随机噪声开始编辑。
    # 【深入注释｜原文件 L65】创建可训练 latent；随后用源音频编码覆盖初值，优化变量只有这份 latent。
    latent = torch.randn(1, 8, lt.shape[2], latent_size, requires_grad=True, device=device)

    with torch.no_grad():
        print(f'[INFO] Encode text prompt...')
        # 【深入注释｜原文件 L69】预先编码参考/目标 prompt；DDS 会反复用同一条件而改变 latent。
        text_z_ref, text_z_ref_gen,z_attention_mask_ref = guidance_model.get_text_embeds(prompt_ref)
        text_z,text_z_gen,z_attention_mask = guidance_model.get_text_embeds(prompt)
        print(f'[INFO] Encoding audio into latent...')
        latent_ref = guidance_model.encode_audio(log_mel_spec) 
        latent[:] = latent_ref


    # 【深入注释｜原文件 L76】SGD 只持有 latent，不更新 guidance_model 的参数；StepLR 调整测试时优化步长。
    optim = torch.optim.SGD([latent], lr=0.02)
    scheduler = torch.optim.lr_scheduler.StepLR(optim, 20, 0.9)


    print(f'[INFO] Delta denoising score...')
    for i in tqdm(range(validation_step+1)):
        optim.zero_grad()
        x = latent


        # 【深入注释｜原文件 L86】目标条件在当前 latent 上预测 ε；抽出的 t、ε 要传给参考分支构成公平差分。
        noise_pred, t, noise = guidance_model.predict_noise(prompt_embds=text_z,
                                                            generated_prompt_embds=text_z_gen,
                                                            attention_mask = z_attention_mask,
                                                            mel_spec = x,
                                                            guidance_scale=guidance_scale, 
                                                            as_latent=as_latent)

        with torch.no_grad():
            # 【深入注释｜原文件 L94】参考条件在固定源 latent 上使用相同 t、相同 ε，隔离文本条件差。
            noise_pred_ref, _, _ = guidance_model.predict_noise(prompt_embds=text_z_ref,
                                                        generated_prompt_embds=text_z_ref_gen,
                                                        attention_mask = z_attention_mask_ref,
                                                        mel_spec = latent_ref,
                                                        guidance_scale=guidance_scale, 
                                                        as_latent=as_latent,
                                                        t=t,
                                                        noise=noise)
        # validation
        if i % validation_step == 0:
            with torch.no_grad():
                # print("cos sim at step", i, " :", F.cosine_similarity(noise_pred - noise, noise_pred_ref - noise).mean().item())
                if as_latent:
                    audio = guidance_model.latents_to_audios(x)
                    basename = os.path.basename(audio_name)
                    write(f"./{output_dir}/{basename}",16000, audio[0].detach().cpu().numpy())
        
        # 【中文精读｜原文件 L111】时间权重随 scheduler 的累计信号系数变化；base 还乘 weight_aug。
        # 【深入注释｜原文件 L111】w_t 随扩散噪声日程改变，越靠近某些时间点权重越不同。
        w =  weight_aug*(1 - guidance_model.alphas[t])
        # 【中文精读｜原文件 L112】DDS/PDS 目标预测减源预测；随后 SGD 执行负梯度更新。
        # 【深入注释｜原文件 L112】DDS 梯度近似 w_t(ε_target−ε_ref)；这不是显式训练损失的普通 autograd。
        grad = w * (noise_pred - noise_pred_ref)
        grad = torch.nan_to_num(grad)

        # 【中文精读｜原文件 L115】注入指定梯度，不将占位 forward 常数解释为优化目标的数值。
        # 【深入注释｜原文件 L115】SpecifyGradient 把外部指定的梯度注入到 latent；反传后 SGD 更新。
        loss = steermusic_utils.SpecifyGradient.apply(x, grad)
        loss.backward()
        # 【中文精读｜原文件 L117】只更新优化器持有的 latent；模型参数已冻结。
        optim.step()
        scheduler.step()



SteerMusic_editing(audio_name,prompt_ref,prompt,weight_aug,validation_step,guidance_model= guidance_model,
                   preprocessor= preprocessor,guidance_scale= guidance_scale,device=device)
