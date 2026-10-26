"""Create an allowlisted text snapshot for GitHub; never traverses credentials/audio caches."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import shutil
root=Path('/home/featurize/work/polyphonia_repro')
run=root/'results/musdb_center10_htdemucs_01'
out=Path('/home/featurize/work/model-reproductions/polyphonia')
out.mkdir(parents=True,exist_ok=True)

def copy(src,dst):
    target=out/dst
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(src,target)

copy(root/'README_zh.md','REPRODUCTION_LOG.md')
script_names=['env.sh','install.sh','download_file.py','download_torch.py','model_download.py',
              'download_musdb_hf.py','download_musdb_hf.sh','audit_musdb.py','prepare_benchmark.py',
              'benchmark_worker.py','benchmark_controller.py','init_benchmark.py','run_benchmark.sh',
              'prepare_evaluation.py','evaluate_benchmark.py','verify_metric_implementation.py',
              'run_evaluation_after_generation.py','export_benchmark.py','status_benchmark.py',
              'run_smoke.sh','smoke.py','requirements.pypi.txt','inference.constraints.txt',
              'export_github_snapshot.py','export_stage_review.py','audit_stage200.py']
for name in script_names:copy(root/'scripts'/name,'scripts/'+name)
for name in ['audio_utils.py','edit.py','my_audioldm2.py','run_sample_exp.py','utils.py','requirements.txt','LICENSE','README.md']:
    copy(root/'polyphonia'/name,'upstream/polyphonia/'+name)
# Reproduction scripts refer to the exact upstream prompt collection. Pin source instead of copying 750 descriptions.
for name in ['musdb_test_plan.json']:
    copy(root/'scripts'/name,'configs/'+name)
for name in ['protocol.json','scripts.sha256.json']:
    copy(run/name,'configs/'+name)
for name in ['environment.freeze.txt','code.commit.txt','benchmark-prompts.json',
             'model.snapshot.json','demucs-model.json','evaluation-model.json',
             'musdb18hq.manifest.json','musdb18hq.audit.json','metric-verification.json']:
    copy(root/'logs'/name,'records/'+name)
for name in ['validation.json','reference_comparison.json']:
    copy(root/'results/smoke_official_01'/name,'records/official-sample/'+name)
copy(run/'metrics/specification.json','records/metrics/specification.json')
copy(run/'metrics/summary.first15.json','records/metrics/first-track.summary.json')
for name in ['control.json','limit200-change.json']:
    copy(run/name,'configs/'+name)
for name in ['summary.first200.json','per_task.first200.csv']:
    copy(run/'metrics'/name,'records/metrics/'+name)
copy(run/'stage200.audit.json','records/stage200.audit.json')
copy(run/'RESULTS_first200_zh.md','STAGE200_RESULTS.md')
copy(run/'review_first200/listening-manifest.json','records/listening-manifest.json')
for name in ['status.before_limit200.json']:
    copy(run/name,'records/history/'+name)
for source in (run/'revisions/before-limit200').glob('*.py'):
    copy(source,'records/history/before-limit200/'+source.name)
for name in ['status.json','pipeline.json']:
    copy(run/name,'records/snapshot-'+name)
# Preserve completed-track validation records and compact logs, dropping tqdm carriage-return progress.
status=json.loads((run/'status.json').read_text())
for item in status['tracks']:
    if item['state'] not in ['completed','completed_subset']:continue
    copy(run/'audio'/item['track']/'validation.json','records/completed-tracks/'+item['track']+'.json')
    for stage in ['separating','editing']:
        name='{:02d}-{}.log'.format(item['index'],stage)
        src=run/'logs'/name
        if src.exists():
            text=src.read_text(errors='replace')
            lines=[line for line in text.splitlines() if not re.match(r'^\s*\d+%\|',line)]
            target=out/'records/logs'/name
            target.parent.mkdir(exist_ok=True)
            target.write_text('\n'.join(lines)+'\n')
# License/credit for the referenced LPAPS computation, not the entire unrelated baseline checkout.
for name in ['LICENSE_LPAPS','LICENSE_CLAP-WEIGHTS','LICENSE']:
    copy(root/'references/AudioEditingCode/evals'/name,'third_party/AudioEditingCode/'+name)
manifest={'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'experiment_state':status['state'],'validated_tasks_at_capture':status['validated_tasks'],
          'total_tasks':750,'stage_task_limit':200,'evaluated_tasks':200,'remaining_tasks_paused':550,
          'pipeline_state':json.loads((run/'pipeline.json').read_text())['state'],
          'completed_tracks_at_capture':sum(x['state']=='completed' for x in status['tracks']),
          'partial_tracks_at_capture':sum(x['state']=='completed_subset' for x in status['tracks']),
          'snapshot_notice':'Point-in-time record. Files do not automatically update on GitHub as server jobs continue.',
          'excluded':['SSH keys and login material','tokens and credentials','audio datasets and derived WAVs',
                      'model checkpoints','runtime environment binaries and caches','incomplete download archives'],
          'upstream':{'url':'https://github.com/Ltx-Leif/polyphonia','commit':'26a5fca9f3ee2465ff3ee9b59a3411bfe1f1b0dc'},
          'LPAPS_reference':{'url':'https://github.com/HilaManor/AudioEditingCode','commit':'8dc937701a42f6fb53160912f8a96b42fe8261d8'}}
(out/'SNAPSHOT.json').write_text(json.dumps(manifest,indent=2))
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (out/'scripts').iterdir() if p.is_file() and not p.name.startswith('._')}
(out/'records/scripts-at-stage200.sha256.json').write_text(json.dumps(hashes,indent=2))
print(json.dumps(manifest,indent=2))
