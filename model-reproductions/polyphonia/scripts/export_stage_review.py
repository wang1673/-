"""Export the selected task prefix and diverse listening examples; no later generation."""
import argparse
import csv
import json
import os
from pathlib import Path
import shutil

parser=argparse.ArgumentParser();parser.add_argument('--limit',type=int,required=True);args=parser.parse_args()
root=Path(os.environ['POLYPHONIA_ROOT']);run=root/'results/musdb_center10_htdemucs_01'
protocol=json.loads((run/'protocol.json').read_text())
summary=json.loads((run/'metrics'/('summary.first{}.json'.format(args.limit))).read_text())
rows=[]
for track in protocol['tracks']:
    for task in track['tasks']:
        if len(rows)==args.limit:break
        path=run/'metrics'/track['track']/(task+'.json')
        assert path.exists(),str(path)
        rows.append(json.loads(path.read_text()))
    if len(rows)==args.limit:break
assert len(rows)==args.limit==summary['evaluated_tasks']
fields=['track','task','CLAP','LPAPS','CQT1_PCC','target_prompt','audio_sha256','source_sha256']
with (run/'metrics'/('per_task.first{}.csv'.format(args.limit))).open('w',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
review=run/('review_first{}'.format(args.limit));review.mkdir(exist_ok=True)
def kind(task):
    for stem in ['vocals','drums','bass']:
        if stem+'2' in task:return stem
    return 'other'
examples=[]
for stem in ['vocals','drums','bass','other']:
    group=[r for r in rows if kind(r['task'])==stem]
    choices=[]
    if group:
        choices=[group[0]]
        later=next((r for r in reversed(group) if r['track']!=group[0]['track']),None)
        if later:choices.append(later)
    for row in choices:
        folder=review/('{:02d}-{}-{}'.format(len(examples)+1,stem,row['task']));folder.mkdir(exist_ok=True)
        source=Path(protocol['prepared_root'])/row['track']/'mixture.wav'
        edited=run/'audio'/row['track']/(row['task']+'.wav')
        shutil.copyfile(source,folder/'source.wav');shutil.copyfile(edited,folder/'edited.wav')
        detail={k:v for k,v in row.items() if k!='audio_embedding'}
        detail.update(source=str(folder/'source.wav'),edited=str(folder/'edited.wav'))
        (folder/'task.json').write_text(json.dumps(detail,indent=2));examples.append(detail)
(review/'listening-manifest.json').write_text(json.dumps(examples,indent=2))
lines=['# 前 {} 个任务：阶段结果'.format(args.limit),'',
       '已完成当前阶段的生成与客观评测，余下 {} 个任务保持暂停。'.format(750-args.limit),
       '任务按原配置顺序选取：13 首完整歌曲和第 14 首的前 5 个任务（当上限为 200 时）。',
       '这是便于检查效果的顺序子集，不代表全部 750 个任务的最终表现。','',
       '| 指标 | 均值 | 总体标准差 | 有效任务 |','| --- | ---: | ---: | ---: |']
for key in ['CLAP','LPAPS','CQT1_PCC']:
    m=summary[key]
    lines.append('| {} | {:.6f} | {:.6f} | {} |'.format(key,m['mean'],m['std_population'],m['valid']))
lines+=['','## 试听对比','',
        '以下按编辑分轨选取不同歌曲的例子，未按客观分数筛选。比较原混音和编辑结果时，留意目标音色、非目标伴奏、旋律节奏和伪影。','']
for row in examples:
    folder=Path(row['source']).parent.relative_to(run)
    lines+=['- {} / {}：{}'.format(row['track'],row['task'],row['target_prompt']),
            '  [原混音]({}/source.wav) · [编辑结果]({}/edited.wav)'.format(folder.as_posix(),folder.as_posix())]
lines+=['','裁剪为每首中间 10 秒；作者未公开准确裁剪清单。本阶段不能宣称精确重现论文表 1。',
        '全部已生成音频仍保存在 audio/；逐任务分数见 metrics/per_task.first{}.csv。'.format(args.limit)]
(run/('RESULTS_first{}_zh.md'.format(args.limit))).write_text('\n'.join(lines)+'\n')
print('Stage review exported:',len(rows),'tasks;',len(examples),'listening pairs',flush=True)
