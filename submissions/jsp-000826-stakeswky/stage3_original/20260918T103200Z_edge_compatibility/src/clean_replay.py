#!/usr/bin/env python3
"""Fresh standard-library replay, comparing complete bytes and parsed JSON."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    root=Path(__file__).resolve().parent.parent
    logdir=root/'logs'/'clean_replay'
    logdir.mkdir(parents=True,exist_ok=True)
    commands=[['src/edge_diagnostics.py','--controls','inputs/controls.json','--out','certificates'],
      ['src/hereditary.py','--inputs','certificates/inputs.json','--out','certificates'],
      ['src/coverage_regression.py','--inputs','certificates/inputs.json','--out','certificates'],
      ['src/integrate.py','--out','certificates']]
    runs=[];comparisons=[]
    with tempfile.TemporaryDirectory(prefix='erdos993-phase3-clean-') as tmp:
        work=Path(tmp)
        shutil.copytree(root/'src',work/'src',ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(root/'inputs',work/'inputs')
        env=dict(os.environ,PYTHONHASHSEED='0',PYTHONDONTWRITEBYTECODE='1')
        for number,args in enumerate(commands,1):
            cmd=[sys.executable,'-S','-B',*args]
            start=time.monotonic()
            completed=subprocess.run(cmd,cwd=work,env=env,text=True,capture_output=True,timeout=180)
            log=logdir/f'{number:02d}.log'
            log.write_text(completed.stdout+completed.stderr)
            runs.append({'command':cmd,'exit_code':completed.returncode,
                         'elapsed_seconds':round(time.monotonic()-start,6),
                         'log':str(log.relative_to(root))})
            if completed.returncode:
                raise RuntimeError(f'clean command failed: {args[0]}; see {log}')
        for p in sorted((work/'certificates').glob('*.json')):
            other=root/'certificates'/p.name
            assert other.exists(), ('missing baseline output',p.name)
            assert json.loads(p.read_text())==json.loads(other.read_text()),('JSON differs',p.name)
            assert p.read_bytes()==other.read_bytes(),('bytes differ',p.name)
            comparisons.append({'file':p.name,'complete_parsed_JSON_equal':True,
                                'all_bytes_equal':True,'bytes':p.stat().st_size,'sha256':digest(p)})
        temporary_path=tmp
    report={'status':'PASS','python':sys.version,'python_executable':sys.executable,
       'flags':['-S','-B'],'commands':runs,'outputs':comparisons,
       'temporary_path':temporary_path,'temporary_directory_removed':not Path(temporary_path).exists(),
       'source_sha256':{p.name:digest(p) for p in sorted((root/'src').glob('*.py'))},
       'input_sha256':{p.name:digest(p) for p in sorted((root/'inputs').glob('*')) if p.is_file()},
       'fresh_replay_scope':'Only this Phase-3 fixed batch, complete hereditary compression, direct coverage regression and integration; no B59 or historical full replay',
       'independent_external_review':False,'top_level_Lean_build':False}
    (root/'certificates'/'CLEAN_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
