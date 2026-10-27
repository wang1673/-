# 关键代码与论文核对

日期：2026-10-27。只做静态检查；未安装实验环境、运行模型或重算指标。未将第三方代码上传到本仓库。

| 方法 | 核对位置 | 观察 | 论文对应与限制 |
|---|---|---|---|
| DirectAudioEdit | main_run.py L271–310、L359–363、L448–475 | no_grad；共享噪声；源/目标一步scheduler位移差；默认目标CFG=[8] | PDF p.4 Algorithm1；pp.10–11论文目标CFG8→12，运行须显式传多个值 |
| AudioMorphix | factory.py L357–413；audio_morphix.py L615–625；sampler.py L1278、L1380–1383 | SGD更新潜变量扰动；能量梯度；removal中显式启用切空间投影 | PDF pp.5,11；Table3中的投影消融不支持“投影在各指标都最优” |
| AudioEditor | null_text_inversion.py L129–161；run_and_display.py L14–25、L110–132 | Adam更新null embedding；attention loss更新条件embedding | PDF pp.2–3；不训练骨干并不排除逐输入拟合 |
| AudioEditor | wo_utils.py L23–35 | SVD奇异值乘负指数；删除与添加/替换有不同配置 | PDF p.3 Eq5打印正指数，符号不一致；待作者/实际复现澄清 |
| MelodyFlow | melodyflow.py L99–128、L191–247；flow.py L331–455；renoise.py L9–42 | Euler25/K4；反演CFG关闭额外guidance；detach速度预测后KL梯度，不回传训练DiT | PDF p.4 Algorithm1；默认时间sway及模型卡训练小时与论文不同；官方卡明确公开版HT-Demucs预处理使指标不同 |
| ZETA | inversion_utils.py L8–146、L147–280；main_run.py | no_grad、提取/复用逐步噪声、换目标条件；本次未做完整ZEUS核心PC代码审计 | PDF pp.3–5；README提示论文版本在paper_code分支，当前commit不是默认为论文原版 |
| EdiTTS | tts.py L208–282；diffusion.py L286–336、L338–393 | 文本token先验、共享eps、no_grad双轨；软mask混合更新 | PDF pp.2–3 Algorithms1–2；不支持直接声称任意音乐波形编辑 |

## 冻结权重、梯度和score的区别

AudioEditor优化文本embedding；AudioMorphix优化潜变量并用能量对latent求导；MelodyFlow对detach后的速度预测作KL梯度修正。三者都可不更新骨干权重，但不能统称为“没有测试时梯度计算”。

EdiTTS中的score是模型输出的密度梯度场；使用它执行采样，不等于对每个输入训练或拟合新参数。ZEUS的主方向迭代也应单独计费，不能与ZETA文本路径混算。

## 版本核对

所有GitHub代码的文件blob已与所固定commit的目录树匹配；HF源码文件计算了SHA-256和Git blob哈希。完整链接见各篇笔记和source-manifest.json。官方HF Space暂停不妨碍读取其源码。

LaTeX用于消除PDF抽取时的表格错列，并核对公式、图的原始坐标和附录；未重编译、未上传全文。标为DE的数值指“在论文材料里能直接定位”，不代表本次重现实测。

## 没有完成的验证

- 未证明所有公开checkpoint就是论文评测checkpoint；MelodyFlow模型卡已明确公开模型的数据处理与指标不同。
- 未安装依赖、下载权重或执行音频编辑。
- 未重建所有数据、原始运行、听测样本及统计检验。
- 未完成全部代码路径、全部消融参数与硬件成本审计。
- 未对EdiTTS做音乐迁移实验，也未把这种迁移写成实证结论。
