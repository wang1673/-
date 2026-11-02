import csv,json,datetime
from pathlib import Path
ROOT=Path('/root/autodl-tmp/polyphonia_repro');R=ROOT/'results/musdb_center10_htdemucs_4090d_01';O=R/'metrics-supplement-v1';D=ROOT/'demos/2026-11-02'
old=json.loads((R/'metrics/summary.json').read_text());s=json.loads((O/'summary.json').read_text());v=json.loads((O/'independent-validation.json').read_text());demo=json.loads((D/'validation.json').read_text())
rows=[]
for key in ['CLAP','LPAPS','CQT1_PCC']:
 r=old[key];rows.append([key,r['mean'],r['std_population'],r['valid'],r['undefined'],'original750_task_metric'])
for key in ['FAD','KAD','ASB','AMB']:rows.append([key,s[key]['value'],None,None,None,s[key].get('status','empirical_distribution_distance_existing_CLAP_features')])
with (O/'all-metrics.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['metric','value','std_population','valid_tasks','undefined_tasks','status']);w.writerows(rows)
record={'package_type':'EXPERIMENT_RECORD','package_version':'research-pipeline-contract v1.0','experiment_id':'polyphonia750-supplement-2026-11-02','source_idea_id':'none','plan_version':str(R/'protocol.json'),'execution_status':'completed_with_explicit_reproduction_limits','research_question':'Complete seven objective metric fields on unchanged750generated clips and create music/animal editing listening examples.','hypothesis':'No new inferential hypothesis; supplementary measurement and exploratory examples.','planned_vs_actual_design_and_controls':{'original750_unchanged':True,'ASB_AMB':'User approved published baseline reference approximation, no new baseline inference','animal_examples':'Out-of-domain exploratory; isolated cat signal used as target other stem; no background separation claim'},'actual_configuration':demo['settings'],'samples_materials_or_data_provenance':{'benchmark':'50MUSDB18-HQtest tracks,15edits each, original protocol and hashes retained','distribution_reference':50,'distribution_generated':750,'feature_dimensions':512,'animal':json.loads((D/'cat-to-dog/source-provenance.json').read_text())},'results_with_uncertainty':{'main_metrics':old,'supplement':s,'demo':demo,'note':'Only original3metrics have per-task populationSD. FAD/KAD are set-level distances and ASB/AMB derived aggregate scores; no artificial per-taskSD or confidence interval. Original3 all750valid0undefined.'},'all_runs_or_repetitions':{'benchmark':'No repeated main generation or evaluation','music':'Two newly generated prompts one inversion seed928','cat':'Two generated prompts; retained two failed deep attempts and corrected-mirror retry; no cherry-picked exclusion'},'observations_and_deviations':[v['runtime_anomaly'],demo['failures_and_retries']],'evidence_locations':[str(R),str(O),str(D),str(ROOT/'supplement-metrics-v1'),str(ROOT/'logs/supplement-metrics-v1.log'),str(ROOT/'logs/supplement-metrics-v1-resumed.log')],'known_limits_and_missing_evidence':['Authors exact crop/CLAP preprocessing and polynomial kernel parameters unpublished; no claim of exact Table1 replication','ASB/AMB from rounded paper baseline means, not same-crop baseline reruns','No human TTA/CTI/GAC ratings; no claim of perceptual success based solely on CLAP','Old3060 resumption RNG and regenerated Demucs estimates limit GPU-only causal comparisons'],'next_routes':['Human listening to supplied examples; author clarification needed for exactKAD'],'next_skill':'squeeze-experiment'}
(O/'EXPERIMENT_RECORD.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
table='\n'.join('| '+str(k)+' | '+f'{value:.9f}'+' | '+('—' if std is None else f'{std:.9f}')+' | '+status+' |' for k,value,std,valid,undef,status in rows)
scores='\n'.join(f"| {name} | {r['cat_prompt_cosine']:.6f} | {r['dog_prompt_cosine']:.6f} | {r['dog_minus_cat']:.6f} |" for name,r in demo['cat_dog_CLAP_diagnostic'].items())
text=f'''# Polyphonia750 补充指标与试听实验记录

记录日期：2026-11-02（Asia/Shanghai）；状态：七项客观指标字段已补齐，复现限制如下。原750生成音频、逐任务指标和最终审计未修改；全部750音频与50参考音频SHA核验通过。

## 指标结果

| 指标 | 数值/均值 | 总体标准差 | 状态 |
|:--|--:|--:|:--|
{table}

原CLAP、LPAPS、CQT1-PCC各750有效、0未定义。新增FAD/KAD为50个参考与750个生成片段之间的集合指标，不存在逐任务标准差；ASB/AMB为聚合分数，未估计置信区间。

## 阅读与实现核对

已核对[Polyphonia论文附录J、表1](https://arxiv.org/html/2605.10203v1)和[官方代码](https://github.com/Ltx-Leif/polyphonia/tree/26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc)。官方仓库提供编辑与提示词代码，未提供完整指标评测实现。论文要求CLAP音乐检查点、CLAP-Swin LPAPS、CQT2010、CLAP特征的FAD及多项式核无偏MMD。不能将引用工具包的默认设置直接当作作者全部实验设置。

FAD：固定[microsoft/fadtk](https://github.com/microsoft/fadtk/tree/ec74b1f96d5576ec04e721985fa0f0d14d965d9b)的原函数体，用样本协方差与Fréchet高斯距离。复用旧实验逐文件哈希核验的512维归一化CLAP音乐特征，每个10秒片段一个向量；没有改用当前fadtk默认的尾部填充多窗、int16往返量化和fp16存储抽取。故是当前实验特征协议下的FAD，不是声称作者精确流水线结果。独立PSD计算值{s['FAD']['independent_psd_check']:.12f}；独立torch CUDA float64值{v['independent_torch_cuda_float64_fad']:.12f}，差异小于1e-5；未做无限样本外推。

KAD：遵循原实验早已记录的补充约定 k(x,y)=(xᵀy/512+1)^3，用去除同集合对角项的无偏MMD²。论文没有公开degree/gamma/coef0/缩放；这些是显式复现假设，不能与论文表中数值直接排名。[原kadtk](https://github.com/YoonjinXD/kadtk/tree/7373161f2e0e4da1c25e5f67d979eab10a828d33)实际采用Gaussian核，和Polyphonia正文描述不同。作为敏感性诊断另存gamma=1多项式值{s['KAD']['sensitivity_gamma_1']:.9f}、原kadtk Gaussian×100值{s['KAD']['diagnostic_cited_kadtk_gaussian_x100']:.9f}，均不冒充论文精确KAD。

ASB/AMB：按用户确认，采用论文7种基线的已发表且经过四舍五入的均值，替换Polyphonia一行为本次复现结果。8方法逐指标Z-score后MinMax；ASB=H(CLAPnorm,(-LPAPS)norm)，AMB=H(CLAPnorm,CQT1-PCCnorm)，H为调和平均。该流水线的Z-score与随后MinMax合并在代数上等价于直接MinMax。论文原8行回放最大绝对差{s['composite_reference']['paper_table_replay_max_abs_error']:.6f}，所以标注“论文基线参照近似值”，不当作同裁剪严格基线实测。

论文TTA、CTI、GAC属于真人主观评分，需要参与者试听问卷；本次没有捏造这三项分数。

## 数值异常及处理

{v['runtime_anomaly']}

此次仅选择现有OpenBLAS的Haswell内核与1线程，没有升级任何Python包。恢复后特征分解残差{v['numpy_eigen_residual']:.3g}，正交性误差{v['numpy_eigen_orthogonality_error']:.3g}；FAD与KAD另用torch CUDA float64独立验证通过。失败日志保留，负FAD尝试值无效且不作为结果。原实验指标未被重新写入。

## 新生成试听示例

音乐：AM Contra - Heart Peripheral的同一中间10秒，用官方未修改脚本新生成vocals2violin、vocals2saxophone两个任务。均为100步、CFG3.5、maskbias2.5、fp16、seed928、energy mask、原down层配置；独立新进程，不读写原750随机状态。

猫叫：ESC-50的1-47819-A-5.wav，44100Hz单声道5秒真实录音，来源[ESC-50](https://github.com/karolpiczak/ESC-50)，Freesound原始src_file=47819，保留CC BY-NC数据集署名。重采样16k并重复一次为10秒；因是孤立动物事件，直接将同一信号作为mixture与other目标轨，非目标轨不存在，没有假称Demucs动物分离。两个目标描述分别为普通狗叫、深沉大狗叫，仍用原官方编辑配置。它是域外扩展示例，不计入750音乐评测。

初次深沉狗叫任务的softmask短语不是baseline的连续子串，触发官方回退分支CPU/CUDA错误；新进程重试仍失败。随后仅按官方mirror规则把短语改为“a large dog barking”，保留失败输入与日志，未改模型源码或编辑超参，重新单独运行成功。

辅助CLAP诊断（不是人工听感评分，不据此宣称狗叫已逼真）：

| 文件 | 猫叫文本余弦 | 狗叫文本余弦 | 狗减猫 |
|:--|--:|--:|--:|
{scores}

每个before_after.wav按“原音10秒→静音0.5秒→编辑10秒”排列。试听副本单声道16k，单独调整至RMS0.1且峰值不超过0.95；原输入与模型输出不改。全部输出检查有限、非静音、160000采样，哈希在validation.json。未进行人工听感成功判定，两个版本都交付。

## 保存位置与证据

- 原实验与补充：{R}
- 补充指标、输入哈希、原论文基线表、独立校验：{O}
- 新示例、原始输出、试听副本、失败和重跑日志：{D}
- 补算源码和固定参考实现：{ROOT/'supplement-metrics-v1'}
- 完整机器记录：{O/'EXPERIMENT_RECORD.json'}

本次为补充测量与探索性示例，无新基线推理、无真人主观实验、无统计因果假设。旧裁剪作者清单未公开、估计分轨重建、旧3060续跑随机流等比较限制继续保留。没有上传新的GitHub内容或删除已有文件。
'''
(O/'补充指标与试听实验记录.md').write_text(text)
print(json.dumps({'report':str(O/'补充指标与试听实验记录.md'),'state':'written'},ensure_ascii=False))
