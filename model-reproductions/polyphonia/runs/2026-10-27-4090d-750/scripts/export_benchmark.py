import csv
import json
import os
from pathlib import Path
root=Path(os.environ['POLYPHONIA_ROOT'])
run=root/'results/musdb_center10_htdemucs_4090d_01'
summary=json.loads((run/'metrics/summary.json').read_text())
rows=[]
for p in sorted((run/'metrics').glob('*/*.json')):
    record=json.loads(p.read_text())
    if 'task' in record:rows.append(record)
assert len(rows)==750
fields=['track','task','CLAP','LPAPS','CQT1_PCC','target_prompt','audio_sha256','source_sha256']
with (run/'metrics/per_task.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
    writer.writeheader();writer.writerows(rows)
lines=['# MUSDB18-HQ test / Polyphonia 复现结果','',
       '50 首歌曲，每首中间 10 秒，750 个官方任务。分轨来自对整首混音运行 HT-Demucs。',
       '生成与评测均已完成。准确裁剪起点、配置、模型哈希及逐任务结果见同目录清单。','',
       '作者未公开准确裁剪清单；本次为明确记录假设的复现，不能宣称逐项重现论文表 1。','',
       '| 指标 | 均值 | 总体标准差 | 有效任务 |','| --- | ---: | ---: | ---: |']
for name in ['CLAP','LPAPS','CQT1_PCC']:
    m=summary[name]
    lines.append('| {} | {:.6f} | {:.6f} | {} |'.format(name,m['mean'],m['std_population'],m['valid']))
lines+=['','本轮仅评测 CLAP、LPAPS、CQT1-PCC。原服务器不可用，HT-Demucs 分轨在新卡重新生成。',
        'ASB/AMB 需要跨方法归一化，主观 MOS 需要真人评价，本次未生成这些分数。',
        '本次只运行 Polyphonia 的 MUSDB18-HQ 部分，未运行 MusicDelta、其余基线和消融。']
(run/'RESULTS_zh.md').write_text('\n'.join(lines)+'\n')
print('Exported 750 task rows and RESULTS_zh.md',flush=True)
