import hashlib
import json
import os
from pathlib import Path
from huggingface_hub import HfApi, hf_hub_download, snapshot_download
root=Path(os.environ['POLYPHONIA_ROOT'])
api=HfApi()
model_id='lukewys/laion_clap'
revision=api.model_info(model_id).sha
filename='music_audioset_epoch_15_esc_90.14.pt'
checkpoint=hf_hub_download(model_id,filename,revision=revision)
# CLAP's constructor loads Roberta pretrained weights before loading the music checkpoint.
roberta_revision=api.model_info('roberta-base').sha
roberta=snapshot_download('roberta-base',revision=roberta_revision,
                         allow_patterns=['config.json','merges.txt','vocab.json','tokenizer.json',
                                         'tokenizer_config.json','model.safetensors'],max_workers=3)
# Ensure model-name lookup in CLAP works offline too.
from transformers import RobertaModel, RobertaTokenizer
RobertaTokenizer.from_pretrained('roberta-base',revision=roberta_revision)
RobertaModel.from_pretrained('roberta-base',revision=roberta_revision)
record={'checkpoint':checkpoint,'repo':model_id,'revision':revision,'filename':filename,
        'sha256':hashlib.sha256(Path(checkpoint).read_bytes()).hexdigest(),
        'roberta_repo':'roberta-base','roberta_revision':roberta_revision,'roberta_snapshot':roberta}
(root/'logs/evaluation-model.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record,indent=2),flush=True)
