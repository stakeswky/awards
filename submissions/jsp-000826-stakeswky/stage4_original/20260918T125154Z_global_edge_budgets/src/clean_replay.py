"""Fresh-directory, full-byte replay of all final deterministic outputs."""
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',default=str(Path(__file__).resolve().parents[1]));a=ap.parse_args()
    root=Path(a.root).resolve();cert=root/'certificates'
    outputs=['material.json','checks_summary.json','search_records.json','search_material.json','search_summary.json',
             'material_compact.json','material_compact.json.gz.b64','EVIDENCE.json']
    receipt=dict(status='PASS',python=sys.version,platform=platform.platform(),
                 source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root/'src').glob('*.py'))},
                 commands=[],outputs=[],review='SAME_MODEL_SELF_REVIEW; different algorithms are not external peer review',
                 original_proved=False,formal_build='NOT_RUN')
    with tempfile.TemporaryDirectory(prefix='erdos993-global-replay-') as tmp:
        work=Path(tmp);shutil.copytree(root/'src',work/'src',ignore=shutil.ignore_patterns('__pycache__'))
        for script in ('check.py','search.py','compact.py'):
            command=[sys.executable,'-S','-B','src/'+script,'--out','certificates']
            p=subprocess.run(command,cwd=work,capture_output=True,text=True,timeout=90)
            (cert/('replay_'+script+'.log')).write_text(p.stdout+p.stderr)
            receipt['commands'].append(dict(argv=command,exit_code=p.returncode,log='certificates/replay_'+script+'.log'))
            if p.returncode:raise RuntimeError('replay failed: '+script+'\n'+p.stdout+p.stderr)
        for name in outputs:
            before=(cert/name).read_bytes();after=(work/'certificates'/name).read_bytes()
            assert before==after,name
            parsed=None
            if name.endswith('.json'):
                parsed=json.loads(before)==json.loads(after);assert parsed
            receipt['outputs'].append(dict(file=name,bytes=len(before),full_bytes_equal=True,
                                           full_parsed_JSON_equal=parsed,sha256=hashlib.sha256(before).hexdigest()))
    receipt['temporary_directory_removed']=not Path(tmp).exists()
    (cert/'CLEAN_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
