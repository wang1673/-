import csv,hashlib,html,json,shutil,datetime
from pathlib import Path
import numpy as np,soundfile as sf
from html.parser import HTMLParser
ROOT=Path('/root/autodl-tmp/polyphonia_repro');D=ROOT/'demos/2026-11-02-ten-tracks';T=D/'tracks';P=D/'delivery';P.mkdir(exist_ok=True)
R=ROOT/'results/musdb_center10_htdemucs_4090d_01';protocol=json.loads((R/'protocol.json').read_text())
rows=[];tracks=[];links=[];manifest={};mapping_notes=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for i in range(10):
 src=T/f'{i:02d}';status=json.loads((src/'status.json').read_text());rec=json.loads((src/'delivery/EXPERIMENT_RECORD.json').read_text())
 assert status['state']=='completed' and status['validated_tasks']==15
 assert rec['track']==protocol['tracks'][i]['track'] and len(rec['rows'])==15
 assert status['selected_tasks']==list(protocol['tracks'][i]['tasks'])
 dest=P/'tracks'/f'{i:02d}';assert not dest.exists(),'Do not overwrite completed delivery'
 shutil.copytree(src/'delivery',dest,ignore=shutil.ignore_patterns('.ipynb_checkpoints','._*'))
 for task in status['selected_tasks']:
  f=src/'output'/(task+'.wav');a,sr=sf.read(str(f),dtype='float32')
  assert sha(f)==status['files'][task]['sha256'] and sr==16000 and a.shape==(160000,) and np.isfinite(a).all() and np.sqrt(np.mean(a.astype('float64')**2))>1e-6
 for path,h in status['original_records_sha256'].items():assert sha(Path(path))==h
 prompts=json.loads((src/'input/prompt_multi.json').read_text())
 for row in rec['rows']:
  row=dict(row);task=row['task'];actual='vocals' if 'vocals2' in task else 'drums' if 'drums2' in task else 'bass' if 'bass2' in task else 'other'
  row.update(track_index=i,track=status['track'],official_edit_stem=actual,source_prompt=prompts[task]['Original Prompt'])
  rows.append(row)
  if task.startswith('bass_guitar2'):mapping_notes.append({'track':status['track'],'task':task,'actual_stem':actual,'note':'Official task name suggests bass_guitar but infer_edit_stem does not match bass2, defaults to other; retained unchanged.'})
 track={'index':i,'track':status['track'],'tasks':15,'input_duration_seconds':10,'input_hashes':status['input_sha256'],'output_hashes':status['files'],'new_or_prior_demo':'prior15demo_from_same_chat' if i==0 else 'new135generation','elapsed_inference_seconds':status['elapsed_seconds'],'peak_cuda_allocated_GiB':status['peak_cuda_allocated_GiB'],'aggregates':rec['aggregates']};tracks.append(track)
 shutil.copy2(src/'status.json',dest/'generation-status.json');shutil.copy2(src/'input/prompt_multi.json',dest/'prompt_multi.json')
 source_name=html.escape(status['track']);links.append(f'<article><h2>{i+1:02d} · {source_name}</h2><p>同一段中间10秒 · 15项编辑 · <a href="tracks/{i:02d}/试听对照.html">打开本曲15项完整对照 →</a></p><audio controls preload="none" src="tracks/{i:02d}/audio/original.wav"></audio><p class="metrics">目标CLAP：原音 {rec["aggregates"]["source_target_CLAP"]["mean"]:.4f} → 编辑 {rec["aggregates"]["edited_target_CLAP"]["mean"]:.4f}</p></article>')
assert len(rows)==150
metrics=['source_target_CLAP','edited_target_CLAP','CLAP_delta','LPAPS','CQT1_PCC']
aggregates={}
for key in metrics:
 vals=np.array([r[key] for r in rows if r[key] is not None],dtype='float64');assert np.isfinite(vals).all()
 aggregates[key]={'mean':float(vals.mean()),'std_population':float(vals.std()),'valid':len(vals),'undefined':150-len(vals)}
fields=['track_index','track','index','task','label','official_edit_stem','source_target_CLAP','edited_target_CLAP','CLAP_delta','LPAPS','CQT1_PCC','source_prompt','target_prompt','sha256']
with (P/'150项逐任务对照.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
record={'package_type':'EXPERIMENT_RECORD','package_version':'research-pipeline-contract v1.0','experiment_id':'polyphonia-ten-tracks-150-demos-20261102','source_idea_id':'none','plan_version':str(R/'protocol.json'),'execution_status':'completed','research_question':'Expand dataset-based listening examples to10tracks,15official edits per same10sclip; source-versus-edited comparison.','hypothesis':'Exploratory demonstration, no new confirmatory hypothesis.','design':{'dataset':'MUSDB18-HQ test','tracks':10,'tasks_per_track':15,'total_tasks':150,'clip_duration_seconds':10,'selection':'First10tracks in original protocol order, before running, no outcome selection','new_generation_this_request':135,'retained_prior_demo_from_same_chat':15,'old750outputs_reused':0,'control':'Original source clip with each target text; no other-method inference','source_software_protocol':str(R/'protocol.json')},'configuration':{'code_commit':'26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc','AudioLDM2_revision':'c8e7e189d324425c05c4c2f81214041ef4107983','steps':100,'cfg':3.5,'mask_bias_strength':2.5,'seed':928,'precision':'fp16','mask_type':'energy','down_layers':list(range(1,19)),'OPENBLAS_CORETYPE':'Haswell','OPENBLAS_NUM_THREADS':'1','gpu':'RTX4090D49140MiB'},'data_provenance':'Existing SHA-verified original center10s mixtures and regenerated whole-mixture HTDemucs estimated stems; not oracle stems, no new whole-song processing.','tracks':tracks,'results_with_uncertainty':aggregates,'task_mapping_anomalies_retained':mapping_notes,'observations_and_deviations':['First15demo retained unchanged rather than rerun; nine additional tracks newly run with seed reset928 pertrack and independent new output directories','Official infer_edit_stem task-name fallback retained; any bass_guitar2 anomaly listed explicitly','Haswell BLAS dispatch follows previous validated supplement/demo fix; no dependency upgrades; main750outputs,metrics,andRNG untouched'],'validation':{'150_output_sha256_verified':True,'150_wav_16k_mono_10s_finite_non_silent':True,'main750_summary_csv_audit_sha256_unchanged':True},'known_limits_and_missing_evidence':['First10protocol tracks are a deterministic convenience sample, not representative random selection or new fullbenchmark','No other-method baseline inference or human TTA/CTI/GAC ratings; do not infer perceptual success solely fromCLAP','CLAP improvement against no-edit target text is semantic evidence only; LPAPS andCQT quantify structure tradeoff','Per-taskFAD/KAD and ASB/AMB are not fabricated for theseexamples; prior750supplement remains separate','Original author crop manifest and kernel details unpublished; old3060RNG and rebuiltDemucs comparison limits retained'],'evidence_locations':[str(D),str(R)],'next_routes':['Human listening to all150examples'],'next_skill':'squeeze-experiment'}
(P/'EXPERIMENT_RECORD.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
(P/'summary.json').write_text(json.dumps({'state':'completed','tracks':10,'generated_tasks':150,'evaluated_tasks':150,'new_generated_this_request':135,'retained_prior_demo':15,'aggregates':aggregates},indent=2))
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Polyphonia · 10首 × 15项编辑试听</title><style>body{font:16px/1.7 system-ui,sans-serif;background:#f2f5f9;color:#1b2940;margin:0}main{max-width:950px;margin:auto;padding:26px 18px}header,article{background:#fff;border:1px solid #dae2ec;border-radius:14px;padding:24px;margin-bottom:18px}h1{font-size:30px;line-height:1.3}h2{font-size:21px}audio{width:100%}a{color:#1856a2}.metrics{font-size:14px;color:#52637a}</style><main><header><h1>10首数据集音乐 × 15项编辑</h1><p>MUSDB18-HQ test，共150项。每首只编辑原复现实验的中间10秒；没有整首推理。第一首保留刚完成的15项，其余9首新跑135项，均非复用旧750生成音频。</p><p>点击曲目进入15项“原音→编辑后”对照。页内播放为独立试听副本，模型原始输出也可下载。目标描述与指标帮助比较，实际音色和伴奏保留请自行试听判断。</p><p><a href="150项逐任务对照.csv">150项指标CSV</a> · <a href="实验记录.md">实验记录</a> · <a href="EXPERIMENT_RECORD.json">完整JSON</a></p></header>'''+''.join(links)+'''</main><script>document.querySelectorAll('audio').forEach(a=>a.addEventListener('play',()=>document.querySelectorAll('audio').forEach(b=>{if(b!==a)b.pause()})))</script></html>'''
(P/'10首音乐试听对照.html').write_text(page)
table='\n'.join(f"| {t['index']+1} | {t['track']} | 15 | {t['aggregates']['source_target_CLAP']['mean']:.4f} | {t['aggregates']['edited_target_CLAP']['mean']:.4f} |" for t in tracks)
metric_table='\n'.join(f"| {k} | {v['mean']:.9f} | {v['std_population']:.9f} | {v['valid']}/{v['undefined']} |" for k,v in aggregates.items())
text=f'''# Polyphonia：10首数据集音乐 × 15项编辑试听记录

日期：2026-11-02，Asia/Shanghai。状态：10首×15=150项生成、三指标与音频校验完成。原750实验保持不变。

## 设计与来源

沿用MUSDB18-HQ test原protocol顺序的前10首，运行前确定，不按结果挑选。每首只用原中间10秒混音及同一时间估计HTDemucs分轨，无整首再处理。每首完整官方15任务、顺序不变。第一首为本聊天刚完成的15项新示例，保留并入本集合；本请求另新跑9首135项。没有复用旧750生成WAV或随机状态，没有补跑7种基线。对照为同一源音与编辑结果，不是跨方法实验。

官方代码commit26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc，AudioLDM2 revision c8e7e189d324425c05c4c2f81214041ef4107983。100steps、CFG3.5、maskbias2.5、fp16、seed928（每首新进程重置）、energy mask、原down1–18层；RTX4090D49140MiB。环境不升级，新进程沿用已验证Haswell BLAS和1线程设置。每首一次反演后生成15项。

| 序号 | 曲目 | 任务数 | 原音对目标CLAP均值 | 编辑后对目标CLAP均值 |
|--:|:--|--:|--:|--:|
{table}

## 汇总与不确定性

| 指标 | 均值 | 总体标准差 | 有效/未定义 |
|:--|--:|--:|--:|
{metric_table}

三指标实现及检查点与原750评测相同，原音对目标CLAP是无编辑对照；正CLAP差值只支持向目标语义移动。LPAPS/CQT1-PCC反映结构保留，不是编辑成功率。标准差为此150任务的总体离散程度，不是置信区间，未做显著性或因果检验。10首为固定顺序便利样本，不外推整体性能。FAD/KAD为集合分布量，ASB/AMB需方法群归一化，本次不伪造逐任务值；原750七指标补充单独存档。

## 官方任务映射及限制

保留官方infer_edit_stem实现：仅vocals2/drums2/bass2子串匹配，其余都映射other。因此bass_guitar2upright等任务键虽意指贝斯，官方实际映射other，未为示例静默改代码。具体异常共{len(mapping_notes)}项，列在EXPERIMENT_RECORD.json的task_mapping_anomalies_retained和逐任务official_edit_stem列。中文标签只辅助阅读，原任务键与目标文本完整保留。个别任务guitar前缀可能只是官方命名，不断言实际原音一定是吉他。

没有人工TTA/CTI/GAC问卷分数，未声称150项都听感成功。论文精确裁剪清单未公开，HTDemucs估计分轨为重建数据，旧3060续跑随机流限制继续保留；不能把新旧差异全部归因GPU。

## 试听和校验

打开10首音乐试听对照.html进入每首15项页面。每段before_after为原音10秒+0.5秒停顿+编辑10秒，总20.5秒仅用于对照；模型每次输入输出各10秒。试听副本目标RMS0.1且峰值限制0.95，raw输出字节不变。150输出全部16kHz、单声道、160000采样、有限且非静音，文件SHA逐项核验；原750summary、CSV、audit哈希未变。完整协议、原输入哈希、输出哈希、逐任务值与偏差记录在EXPERIMENT_RECORD.json。所有输出均保留，不挑选最好案例。

服务器主副本：{D}。原数据和模型仍在/root/autodl-tmp。GitHub仅上传实验文本记录、脚本、提示词、指标、哈希与状态，不上传音频、数据集、权重、环境或SSH材料；本地试听包与服务器保留完整音频。
'''
(P/'实验记录.md').write_text(text)
class Check(HTMLParser):
 def __init__(self,base):super().__init__();self.base=base
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='audio':assert (self.base/a['src']).exists(),a['src']
for f in P.rglob('*.html'):
 c=Check(f.parent);c.feed(f.read_text());assert '{TRACK_NAME}' not in f.read_text()
for f in P.rglob('*'):
 if f.is_file():manifest[str(f.relative_to(P))]=sha(f)
(P/'manifest.sha256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(D/'final.audit.json').write_text(json.dumps({'status':'passed','tracks':10,'generated':150,'evaluated':150,'all_output_hashes_verified':True,'all150_audio_valid':True,'main750_records_unchanged':True,'all_html_audio_targets_exist':True,'delivery_files':len(manifest),'task_mapping_notes':mapping_notes},ensure_ascii=False,indent=2))
print(json.dumps({'state':'completed','tracks':10,'tasks':150,'files':len(manifest),'aggregates':aggregates},indent=2))
