import json
from pathlib import Path
run=Path('/home/featurize/work/polyphonia_repro/results/musdb_center10_htdemucs_01')
g=json.loads((run/'status.json').read_text())
p=json.loads((run/'pipeline.json').read_text()) if (run/'pipeline.json').exists() else {}
c=json.loads((run/'control.json').read_text()) if (run/'control.json').exists() else {'max_tasks':750}
print('生成状态:',g['state'])
print('已验证任务: {}/{}'.format(g['validated_tasks'],g['total_tasks']))
print('本阶段目标: {}，其余 {} 个任务留待之后继续'.format(c['max_tasks'],750-c['max_tasks']))
print('已完成完整歌曲: {}/50'.format(sum(t['state']=='completed' for t in g['tracks'])))
if g['tracks']:
    last=g['tracks'][-1]
    print('当前歌曲:',last['track'],'阶段:',last['state'])
print('评测流水线:',p.get('state','not started'))
if 'error' in g:print('生成错误:',g['error'])
if 'error' in p:print('评测错误:',p['error'])
