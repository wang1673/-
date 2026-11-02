import csv,hashlib,html,json,shutil
from pathlib import Path
import numpy as np,soundfile as sf,torch,julius,laion_clap
from laion_clap.clap_module.factory import load_state_dict
from nnAudio.features import CQT2010
ROOT=Path('/root/autodl-tmp/polyphonia_repro');D=ROOT/'demos/2026-11-02-full15';R=ROOT/'results/musdb_center10_htdemucs_4090d_01'
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--dir',required=True);args=parser.parse_args();D=Path(args.dir)
status=json.loads((D/'status.json').read_text());assert status['state']=='completed' and status['validated_tasks']==15
prompts=json.loads((D/'input/prompt_multi.json').read_text())
P=D/'delivery';A=P/'audio';A.mkdir(parents=True,exist_ok=True)
weights=json.loads((ROOT/'logs/evaluation-model.json').read_text())
model=laion_clap.CLAP_Module(enable_fusion=False,amodel='HTSAT-base',device='cuda')
state=load_state_dict(weights['checkpoint'],skip_params=True);state.pop('text_branch.embeddings.position_ids',None);model.model.load_state_dict(state,strict=True);model.eval()
captured={}
for index,layer in enumerate(model.model.audio_branch.layers):
    def hook(module,inputs,output,key=index):captured[key]=output[0].detach().cpu()
    layer.register_forward_hook(hook)
cqt=CQT2010(sr=16000,n_bins=128,bins_per_octave=24,hop_length=512,fmin=32.7,verbose=False).cuda().eval()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    x,sr=sf.read(str(p),dtype='float32',always_2d=True);assert len(x)/sr==10 and np.isfinite(x).all()
    return torch.tensor(x.mean(1)).unsqueeze(0),sr
@torch.inference_mode()
def features(p):
    x,sr=read(p);captured.clear();e=model.get_audio_embedding_from_data(julius.resample_frac(x,sr,48000).cuda(),use_tensor=True).detach().cpu()
    assert set(captured)==set(range(4));layers=[captured[i].clone() for i in range(4)]
    a=julius.resample_frac(x,sr,16000);top=cqt(a.cuda()).argmax(dim=1).squeeze(0).cpu().numpy().astype('float64')
    return {'embedding':e,'layers':layers,'top1':top,'audio':a.numpy()[0]}
def lpaps(a,b):
    total=0.
    for x,y in zip(a['layers'],b['layers']):
        x=x/(torch.sqrt(torch.sum(x*x,dim=1,keepdim=True))+1e-10);y=y/(torch.sqrt(torch.sum(y*y,dim=1,keepdim=True))+1e-10)
        total+=float(((x-y)**2).sum(dim=1,keepdim=True).mean([1,2]).item())
    return total
def listen(a):return a*min(0.1/np.sqrt(np.mean(a.astype('float64')**2)),0.95/max(float(abs(a).max()),1e-8))
names={'vocals':'人声','guitar':'其他旋律声部','piano':'钢琴','harmonica':'口琴','acoustic_guitar':'原声吉他','bass_guitar':'贝斯','synth_lead':'合成器主音','synthpad':'合成器铺底','drums':'鼓','bass':'贝斯','violin':'小提琴','cello':'大提琴','flute':'长笛','trumpet':'小号','choir':'合唱','saxophone':'萨克斯','trombone':'长号','harp':'竖琴','marimba':'马林巴','banjo':'班卓琴','organ':'管风琴','upright':'低音提琴','electronic':'电子鼓','jazz':'爵士鼓','viola':'中提琴','clarinet':'单簧管','oboe':'双簧管','englishhorn':'英国管','frenchhorn':'圆号','doublebass':'低音提琴','piccolo':'短笛','electricguitar':'电吉他','accordion':'手风琴','synth':'合成器','acoustic':'原声鼓','sitar':'西塔琴','synthlead':'合成器主音','tribal':'部落鼓','orchestral':'管弦打击乐','vibraphone':'颤音琴','ukulele':'尤克里里','strings':'弦乐'}
labels={t:'→'.join(names.get(part,part) for part in t.split('2',1)) for t in prompts}
source=features(D/'input/mixture.wav');sf.write(str(A/'original.wav'),listen(source['audio']),16000)
rows=[];cards=[];hashes={}
for i,(task,cfg) in enumerate(prompts.items(),1):
    path=D/'output'/(task+'.wav');assert sha(path)==status['files'][task]['sha256'];f=features(path)
    with torch.inference_mode():
        t=model.get_text_embedding([cfg['Baseline Prompt']],use_tensor=True).detach().cpu()
        before=float(torch.nn.functional.cosine_similarity(source['embedding'],t).item());after=float(torch.nn.functional.cosine_similarity(f['embedding'],t).item())
    corr=None if np.std(source['top1'])==0 or np.std(f['top1'])==0 else float(np.corrcoef(source['top1'],f['top1'])[0,1])
    row={'official_edit_stem':('vocals' if 'vocals2' in task else 'drums' if 'drums2' in task else 'bass' if 'bass2' in task else 'other'),'index':i,'task':task,'label':labels[task],'source_target_CLAP':before,'edited_target_CLAP':after,'CLAP_delta':after-before,'LPAPS':lpaps(source,f),'CQT1_PCC':corr,'target_prompt':cfg['Baseline Prompt'],'sha256':sha(path)};rows.append(row)
    assert np.isfinite([before,after,row['LPAPS']]).all()
    prefix=f'{i:02d}_{task}';raw=A/(prefix+'_raw.wav');shutil.copy2(path,raw)
    sf.write(str(A/(prefix+'_edited.wav')),listen(f['audio']),16000)
    sf.write(str(A/(prefix+'_before_after.wav')),np.concatenate([listen(source['audio']),np.zeros(8000),listen(f['audio'])]),16000)
    e=html.escape
    cards.append(f'''<article><h2>{i:02d} · {e(labels[task])}</h2><p class="target">{e(cfg['Baseline Prompt'])}</p><div class="scores">目标CLAP：原音 {before:.4f} → 编辑 {after:.4f}　|　LPAPS {row['LPAPS']:.4f}　|　CQT1-PCC {corr if corr is None else round(corr,4)}</div><p>原音10秒 → 停顿0.5秒 → 编辑后10秒</p><audio controls preload="none" src="audio/{prefix}_before_after.wav"></audio><details><summary>单独试听编辑结果 / 下载原始输出</summary><audio controls preload="none" src="audio/{prefix}_edited.wav"></audio><p><a href="audio/{prefix}_raw.wav" download>下载模型原始10秒输出</a></p></details></article>''')
    print('Packaged',i,task,flush=True)
with (P/'per-task-comparison.csv').open('w') as out:
    writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
means={key:{'mean':float(np.mean([r[key] for r in rows if r[key] is not None])),'std_population':float(np.std([r[key] for r in rows if r[key] is not None])),'valid':sum(r[key] is not None for r in rows)} for key in ['source_target_CLAP','edited_target_CLAP','CLAP_delta','LPAPS','CQT1_PCC']}
record={'package_type':'EXPERIMENT_RECORD','experiment_id':'polyphonia-musdb-10s-full15-20261102-'+D.name,'state':'completed','track':status['track'],'duration_per_inference_seconds':10,'tasks':15,'source':str(D/'input/mixture.wav'),'scope':'One fixed center10second dataset clip ×15official prompts, new official inference; original-versus-edited comparison, no seven-method baseline rerun.','model_commit':'26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc','AudioLDM2_revision':'c8e7e189d324425c05c4c2f81214041ef4107983','configuration':status['configuration'],'task_mapping_note':'Official infer_edit_stem uses substring vocals2/drums2/bass2; all others default to other. Retained unmodified even when a task prefix such as bass_guitar2 does not match bass2. Labels follow official task names, not manual correction.','elapsed_inference_seconds':status['elapsed_seconds'],'peak_cuda_allocated_GiB':status['peak_cuda_allocated_GiB'],'features':'Same original music CLAP checkpoint, sample mean stereo downmix, Julius resampling, exact original LPAPS reduction and CQT2010 trajectory PCC. New example outputs evaluated; old750metrics untouched.','aggregates':means,'rows':rows,'listening_note':'Listening copies targetRMS0.1 withpeak0.95 limit; raw output copies are byteidentical. Before-after concatenations are20.5s only for comparison; inference clips each10s.','limits':['Single-track demonstration, not a new750benchmark or cross-method test','Source targetCLAP is a no-edit semantic control; preserving original exactly would giveLPAPS0 andselfCQT1, but does not perform requested editing','No human subjective success ratings; metrics do not guarantee convincing instrument timbre','Author precise crop manifest unpublished; HTDemucs stems from existing reproduction, no oracle stems','FAD/KAD are set-level distances, not appropriate per-task sound-quality scores; ASB/AMB require methods cohort, not computed perexample'],'original_records_unchanged':all(sha(Path(p))==h for p,h in status['original_records_sha256'].items())}
assert record['original_records_unchanged']
(P/'EXPERIMENT_RECORD.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Polyphonia · 10秒音乐 × 15项编辑对照</title><style>body{font:16px/1.65 system-ui,sans-serif;margin:0;background:#f3f5f8;color:#182335}main{max-width:940px;margin:auto;padding:28px 20px}header,article{background:white;border:1px solid #dce2eb;border-radius:14px;padding:24px;margin:18px 0}h1{font-size:30px;line-height:1.25}h2{font-size:21px}.target{color:#334c70}.scores{font-size:14px;background:#edf3fa;padding:10px;border-radius:8px}audio{width:100%;margin:10px 0}a{color:#1958a5}summary{cursor:pointer}small{color:#5a6575}</style><main><header><h1>同一段10秒音乐，15项编辑对照</h1><p>数据集：MUSDB18-HQ test<br>曲目：{TRACK_NAME}<br>片段：原复现实验的中间10秒，无整首推理。</p><p>官方Polyphonia / AudioLDM2；100步、CFG3.5、maskbias2.5、seed928、fp16。15项任务按官方顺序新生成。</p><p><b>原始10秒音乐</b></p><audio controls preload="none" src="audio/original.wav"></audio><p>每项对照：原音10秒 → 0.5秒停顿 → 编辑后10秒。试听副本调整音量便于比较；原始输出可单独下载。</p><small>本页比较原音与编辑结果，没有补跑其他方法基线。请结合目标描述判断音色是否改变、伴奏是否保留。自动指标不能代替人工听感。</small><p><a href="per-task-comparison.csv">逐任务指标CSV</a> · <a href="EXPERIMENT_RECORD.json">完整实验记录JSON</a></p></header>'''+''.join(cards)+'''</main><script>document.querySelectorAll('audio').forEach(a=>a.addEventListener('play',()=>document.querySelectorAll('audio').forEach(b=>{if(b!==a)b.pause()})))</script></html>'''
(P/'试听对照.html').write_text(page.replace('{TRACK_NAME}',html.escape(status['track'])))
table='\n'.join(f"| {r['index']} | {r['label']} | {r['source_target_CLAP']:.4f} | {r['edited_target_CLAP']:.4f} | {r['LPAPS']:.4f} | {r['CQT1_PCC']:.4f} |" for r in rows)
report=f'''# Polyphonia 数据集10秒 × 15项编辑对照

日期：2026-11-02。状态：15/15新生成并校验通过。数据集MUSDB18-HQ test，曲目{status['track']}，原复现实验中间10秒裁剪。同一段音频执行官方15条任务，非15首曲目，无整首推理。采用官方未改动代码与固定AudioLDM2检查点、原100steps/CFG3.5/maskbias2.5/fp16/seed928/energy/down层配置。新进程一次反演后按原顺序生成15项，不复用原750输出或随机状态，不修改原750结果。输入混音与估计HTDemucs分轨来自原prepared目录。

推理总耗时{status['elapsed_seconds']:.2f}秒，CUDA峰值分配{status['peak_cuda_allocated_GiB']:.2f}GiB。新进程沿用此前已记录的OPENBLAS_CORETYPE=Haswell及1线程，软件包未变。

打开同目录“试听对照.html”可逐项播放；保留audio目录与HTML的相对位置。每个before_after音频20.5秒为原10秒+停顿0.5秒+编辑10秒，推理单段仍是10秒。试听副本目标RMS0.1且峰值限制0.95；raw文件为未修改模型输出，SHA保存在JSON。播放原音与编辑结果构成无编辑对照，未补跑其他7种方法。

| 编号 | 编辑任务 | 原音对目标CLAP | 编辑后对目标CLAP | LPAPS↓ | CQT1-PCC↑ |
|--:|:--|--:|--:|--:|--:|
{table}

指标使用原音乐CLAP检查点、原LPAPS归约和CQT2010参数；输入评测双声道取均值，与官方推理读取第一声道的原行为区别继续保留。源音对目标CLAP表示不编辑时与同一目标描述的语义匹配；它不是真实完成编辑的基线。单首示例不做跨数据集性能结论、不推断统计显著、不声称人工音色评测通过。FAD/KAD为分布指标，ASB/AMB需方法群归一化，本15例不构造逐任务数值。

所有输出均16kHz单声道160000采样、有限非静音；原750汇总、CSV和audit哈希未变。机器记录见EXPERIMENT_RECORD.json，逐任务表见per-task-comparison.csv；日志、原始输入与输出在服务器{D}。原实验协议、数据和软件比较限制均保留。官方代码固定commit26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc；AudioLDM2 revision c8e7e189d324425c05c4c2f81214041ef4107983。
'''
(P/'实验记录.md').write_text(report)
for f in P.rglob('*'):
    if f.is_file():hashes[str(f.relative_to(P))]=sha(f)
(P/'manifest.sha256.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2))
print(json.dumps({'state':'completed','tasks':len(rows),'aggregates':means},indent=2))
