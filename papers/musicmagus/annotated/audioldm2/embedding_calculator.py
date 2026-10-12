# 中文精读注释版：只添加注释，原始语句与文档字符串保持不变。
# 上游：https://github.com/ldzhangyx/MusicMagus  commit=ef69ef6955a963955015c05e3a021a6b31f80b16
# 原文对应：§4.1 Finding Editing Direction；§4.2 Adding Constraints Over Cross-Attention；§6.1 Real Music Audio Editing。
# 原始行号请看 code-used/；注释会使本文件行号发生偏移。
from diffusers import DDIMScheduler, DiffusionPipeline
import torch
import openai
import os

openai.api_key = ""

# 【中文精读｜原文件 L8】§4.1：生成属性描述集并求平均 embedding，减弱单句语义和长度差异。
class EmbeddingCalculator(object):
    def __init__(self, embedding_model=None, prompt_length=10):
        if embedding_model is None:
            embedding_model = DiffusionPipeline.from_pretrained("cvssp/audioldm2-large")
        self.embedding_model = embedding_model.to("cuda")
        self.embedding_tokenizer = embedding_model.tokenizer
        self.prompt_length = prompt_length

    @staticmethod
    # 【中文精读｜原文件 L17】通过旧版 OpenAI Completion 接口生成 captions；此处只阅读，不实际请求外部服务。当前接口兼容性未测试。
    # 【深入注释｜原文件 L17】为属性词扩展多条 caption，减少单句表述偶然性；生成器输出仍需筛选/长度对齐。
    def generate_captions(input_prompt, number=24):
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=input_prompt,
            temperature=1.0,
            max_tokens=100,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            n=number,
        )
        return [item.text.strip() for item in response.choices]

    @staticmethod
    def postprocessing_caption(caption, keyword):
        input_prompt = (f"Please shorten the music caption, and include genre, main instrument, and mood. "
                        f"Then, please replace the main instrument to {keyword}. Caption: {caption}. Result: ")
        output = EmbeddingCalculator.generate_captions(input_prompt, number=1)
        return output[0]

    @torch.no_grad()
    # 【中文精读｜原文件 L37】冻结编码，沿 caption batch 维平均；保持 token 维，得到同形方向而非单一全局句向量。
    # 【深入注释｜原文件 L37】两条条件链经 AudioLDM2.encode_prompt 编码，返回 T5 与生成语义嵌入。
    def embed_captions(self, l_sentences, fix_length=None):
        prompt_embeds, _, generated_prompt_embeds = self.embedding_model.encode_prompt(
            prompt=l_sentences,
            device="cuda",
            do_classifier_free_guidance=False,
            num_waveforms_per_prompt=1,
            fix_length=fix_length,
        )

        # average
        # 【深入注释｜原文件 L47】对 caption 维求平均后得到属性中心；目标减源才是编辑语义方向。
        prompt_embeds = prompt_embeds.mean(dim=0, keepdim=True)
        generated_prompt_embeds = generated_prompt_embeds.mean(dim=0, keepdim=True)

        return prompt_embeds, generated_prompt_embeds

    # 【中文精读｜原文件 L52】主 pipeline 或 attention processor。pipeline 先参考去噪缓存，再编辑去噪；每步 SGD latent 后重算 noise。
    def __call__(self, source_concept, target_concept, verbose=True):
        source_text = (f"Generate one sentence capturing keywords of {source_concept} music around {self.prompt_length} words. "
                       f"Answer: ")
        target_text = source_text.replace(source_concept, target_concept)

        # text -> captions
        source_captions = self.generate_captions(source_text)
        target_captions = self.generate_captions(target_text)

        if verbose:
            print(f"source: {source_captions}")
            print(f"target: {target_captions}")

        fix_length = self.prompt_length + 2

        # captions -> embeddings
        # 【深入注释｜原文件 L68】同时返回源/目标两路条件，供 pipeline 构造方向并更新目标语义分支。
        source_embeddings, generated_source_embeddings = self.embed_captions(source_captions, fix_length=fix_length)
        target_embeddings, generated_target_embeddings = self.embed_captions(target_captions, fix_length=fix_length)

        return source_embeddings, generated_source_embeddings, target_embeddings, generated_target_embeddings
