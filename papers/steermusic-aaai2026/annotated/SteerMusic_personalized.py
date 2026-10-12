# 中文精读注释版：只添加注释，原始语句与文档字符串保持不变。
# 上游：https://github.com/sony/steermusic  commit=9d2008b8515f9c8a83c956ddb23ab83b55e19709
# 原文对应：§3 DDS（eqn:dds）；§4.1 g(θ)=θ；§4.2 PDS-O（eqn:psd_0）与 PCon（eqn:patch_personal）。
# 原始行号请看 code-used/；注释会使本文件行号发生偏移。
# %%
import torch
from tqdm import tqdm
import steermusic_utils
import numpy as np
import pdb
import os
import yaml
from scipy.io.wavfile import write
import torch.nn.functional as F
import re
from preprocessor import Preprocessor
import torchaudio
from diffusers.utils.torch_utils import randn_tensor
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--audio_path', type=str)
parser.add_argument('--prompt_ref', default='', type=str)
parser.add_argument('--concept', default='', type=str)
parser.add_argument('--output_dir', default='./SteerMusic+_output/', type=str)
parser.add_argument('--personalized_ckpt', default='', type=str)
parser.add_argument('--guidance_scale', default=15, type=int)
parser.add_argument('--validation_step', default=400, type=int)
parser.add_argument('--add_reg',default=True,type=bool)
parser.add_argument('--lambd',default=0.05,type=float)
opt = parser.parse_args()

device = "cuda:0"

prompt_ref = opt.prompt_ref
concept = opt.concept
audio_name = opt.audio_path
# Find content inside square brackets
match = re.search(r"\[(.*?)\]", prompt_ref)
if match:
    detected = match.group(1)  

    # Replace the content inside the brackets
    prompt = re.sub(r"\[.*?\]", f"sks {concept}", prompt_ref)
    prompt_tgt = re.sub(r"\[.*?\]", f"{concept}", prompt_ref)
print("[INFO] Target prompt:", prompt)

guidance_scale = opt.guidance_scale
validation_step = opt.validation_step
lambd = opt.lambd
## Personalized diffusion ckpt
hf_key = opt.personalized_ckpt
add_reg = opt.add_reg
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

# Load guidance model phi
guidance_model = steermusic_utils.AudioLDM2_pipe(device, fp16=False, vram_O=False)
guidance_model.eval()

# Load personalized model phi'
personalized_model = steermusic_utils.AudioLDM2_pipe(device, fp16=False, vram_O=False, hf_key=hf_key)
personalized_model.eval()

for p in guidance_model.parameters():
    p.requires_grad = False

for p in personalized_model.parameters():
    p.requires_grad = False


# Define PCon loss
pcon_loss = steermusic_utils.PConLoss(256, [1])

# 【中文精读｜原文件 L84】§4.2：目标用个性化模型，源用基础模型；加入 shift 正则与 PCon。
# 【中文精读｜原文件 L84】PDS/shift 用自定义梯度；PCon 通过目标特征对 latent 反传；个性化模型准备阶段需要微调。
def SteerMusic_plus(audio_name,prompt_ref,prompt,prompt_tgt,
                   guidance_model,personalized_model, pcon_loss, device, validation_step = 40, lambd=0.25,add_reg =True):
    sa_attn = {}
    log_mel_spec, _, _, _  = preprocessor.read_audio_file(filename=audio_name)
    log_mel_spec = log_mel_spec.unsqueeze(0).unsqueeze(0).to(device)

    log_mel_spec.requires_grad = False
    lt = guidance_model.encode_audio(log_mel_spec)
    as_latent = True
    latent_size = 16
    # 【中文精读｜原文件 L94】可优化变量形状 [1,8,T,16]；后面复制源 latent 初始化，而非从随机噪声开始编辑。
    latent = torch.randn(1, 8, lt.shape[2], latent_size, requires_grad=True, device=device)

    with torch.no_grad():
        print(f'[INFO] Encode text prompt...')
        text_z_ref, text_z_ref_gen,z_attention_mask_ref = guidance_model.get_text_embeds(prompt_ref)
        text_z,text_z_gen,z_attention_mask = guidance_model.get_text_embeds(prompt)
        text_z_tgt,text_z_gen_tgt,z_attention_mask_tgt = guidance_model.get_text_embeds(prompt_tgt)
        print(f'[INFO] Encoding audio into latent...')
        latent_ref = guidance_model.encode_audio(log_mel_spec) 
        latent[:] = latent_ref

    optim = torch.optim.SGD([latent], lr=0.1)
    scheduler = torch.optim.lr_scheduler.StepLR(optim, 20, 0.9)
    import torch.nn.functional as F

    print(f'[INFO] Delta denoising score...')
    for i in tqdm(range(validation_step+1)):
        optim.zero_grad()
        x = latent

        # \eps_{\phi'} (z,y,t)
        noise_pred, t, noise = personalized_model.predict_noise(prompt_embds=text_z,
                                                            generated_prompt_embds=text_z_gen,
                                                            attention_mask = z_attention_mask,
                                                            mel_spec = x,
                                                            guidance_scale=guidance_scale, 
                                                            as_latent=as_latent)


        with torch.no_grad():
            # \eps_{\phi}(\hat_z,\hat_y,t)
            noise_pred_ref, _, _ = guidance_model.predict_noise(prompt_embds=text_z_ref,
                                                        generated_prompt_embds=text_z_ref_gen,
                                                        attention_mask = z_attention_mask_ref,
                                                        mel_spec = latent_ref,
                                                        guidance_scale=guidance_scale, 
                                                        as_latent=as_latent,
                                                        t=t,
                                                        noise=noise)                
        
        # 【中文精读｜原文件 L134】时间权重随 scheduler 的累计信号系数变化；base 还乘 weight_aug。
        w =   (1 - personalized_model.alphas[t])
        if add_reg==True:
            with torch.no_grad():
                noise_pred_hat_z_phi0, _, _ = guidance_model.predict_noise(prompt_embds=text_z_tgt,
                                                            generated_prompt_embds=text_z_gen_tgt,
                                                            attention_mask = z_attention_mask_tgt,
                                                            mel_spec = x,
                                                            guidance_scale=guidance_scale, 
                                                            as_latent=as_latent,
                                                            t=t,
                                                            noise = noise)
            # 【中文精读｜原文件 L145】同一当前 latent 上比较个性化与基础目标预测，是分布偏移项。
            reg = lambd* w * (noise_pred - noise_pred_hat_z_phi0)
            reg = torch.nan_to_num(reg)

        # 【中文精读｜原文件 L148】DDS/PDS 目标预测减源预测；随后 SGD 执行负梯度更新。
        grad = w * (noise_pred  - noise_pred_ref)
        grad = torch.nan_to_num(grad)

        sa_attn[t.item()] = {}

        for name, module in guidance_model.unet.named_modules(): 
            module_name = type(module).__name__
            if module_name == "Attention":
                if "attn1" in name and "up" in name: 
                    hidden_state = module.hs
                    sa_attn[t.item()][name] = hidden_state.detach().cpu()

        if add_reg == True:
            # 【中文精读｜原文件 L161】注入指定梯度，不将占位 forward 常数解释为优化目标的数值。
            loss = steermusic_utils.SpecifyGradient.apply(x, grad+reg)
        else:
            # 【中文精读｜原文件 L163】注入指定梯度，不将占位 forward 常数解释为优化目标的数值。
            loss = steermusic_utils.SpecifyGradient.apply(x, grad)
        loss.backward()

        # calculate Pcon loss
        with torch.enable_grad():
            noise_pred, _ , _ = personalized_model.predict_noise(prompt_embds=text_z,
                                                        generated_prompt_embds=text_z_gen,
                                                        attention_mask = z_attention_mask,
                                                        mel_spec = x,
                                                        guidance_scale=guidance_scale, 
                                                        as_latent=as_latent,
                                                        t=t,
                                                        noise = noise,
                                                        cfg=False,
                                                        disable_grad=False)
            
            pconloss = 0
            for name, module in personalized_model.unet.named_modules(): 
                module_name = type(module).__name__
                if module_name == "Attention":
                    if "attn1" in name and "up" in name: #  
                        curr = module.hs
                        ref = sa_attn[t.item()][name].detach().to(device)
                        pconloss += pcon_loss.get_attn_pcon_loss(ref, curr)
            (pconloss*3).backward()

        
        # 【中文精读｜原文件 L190】只更新优化器持有的 latent；模型参数已冻结。
        optim.step()
        scheduler.step()
        if i % validation_step == 0:
            with torch.no_grad():
                # print("cos sim at step", i, " :", F.cosine_similarity(noise_pred - noise, noise_pred_ref - noise).mean().item())
                if as_latent:
                    audio = guidance_model.latents_to_audios(x)
                    basename = os.path.basename(audio_name)
                    write(f"./{output_dir}/{basename}",16000, audio[0].detach().cpu().numpy())

SteerMusic_plus(audio_name,prompt_ref,prompt,prompt_tgt,guidance_model,personalized_model,pcon_loss, device,
                       validation_step = validation_step, lambd=lambd, add_reg=add_reg)
