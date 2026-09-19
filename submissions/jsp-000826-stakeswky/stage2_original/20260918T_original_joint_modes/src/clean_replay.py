#!/usr/bin/env python3
"""Replay all current evidence from uncached copied sources, compare full output."""
import hashlib,json,shutil,subprocess,sys,tempfile,time
from pathlib import Path


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    root=Path(__file__).resolve().parents[1]
    records=[];compares={}
    with tempfile.TemporaryDirectory(prefix='erdos993-stage2-clean-') as temp:
        clean=Path(temp)
        for d in ['src','inputs','certificates']:(clean/d).mkdir()
        sources={}
        for p in sorted((root/'src').glob('*.py')):
            shutil.copyfile(p,clean/'src'/p.name)
            sources[p.name]=sha(p)
        specs=[('diagnostics',['src/run_diagnostics.py','--inputs','inputs/stress.json',
                    '--generate','--out','certificates']),
               ('material',['src/verify_material.py','--inputs','inputs/stress.json',
                    '--out','certificates/material.json']),
               ('reductions',['src/verify_reductions.py','--material','certificates/material.json',
                    '--out','certificates/reductions.json']),
               ('compact',['src/check_compact.py','--material','certificates/material.json',
                    '--out','certificates/material_compact.json'])]
        for name,tail in specs:
            command=[sys.executable,'-S','-B']+tail;t=time.monotonic()
            proc=subprocess.run(command,cwd=clean,capture_output=True,text=True,timeout=150)
            log=root/'logs'/('clean-'+name+'.log')
            log.write_text('cwd='+str(clean)+'\ncommand='+json.dumps(command)+'\n'+
                           proc.stdout+'\nSTDERR:\n'+proc.stderr+'\nexit_code='+str(proc.returncode)+'\n')
            records.append({'name':name,'command':command,'exit_code':proc.returncode,
                            'elapsed_seconds':round(time.monotonic()-t,6),'log':str(log.relative_to(root))})
            if proc.returncode:raise RuntimeError('Clean command failed; retained log: '+str(log))
        for rel in ['inputs/stress.json','certificates/diagnostics.json',
                    'certificates/material.json','certificates/reductions.json',
                    'certificates/material_compact.json']:
            a,b=root/rel,clean/rel
            # Full structural comparison is the primary check; hashes are provenance only.
            assert json.loads(a.read_text())==json.loads(b.read_text()),('full output differs',rel)
            assert a.read_bytes()==b.read_bytes(),('deterministic serialization differs',rel)
            compares[rel]={'full_parsed_equality':True,'byte_equality':True,
                           'bytes':a.stat().st_size,'sha256':sha(a)}
        a=json.loads((root/'certificates/summary.json').read_text())
        b=json.loads((clean/'certificates/summary.json').read_text())
        old_elapsed=a.pop('elapsed_seconds');new_elapsed=b.pop('elapsed_seconds')
        assert a==b,'Summary differs beyond elapsed wall time'
        assert a['completed']==a['input_records']==193 and not a['excluded'] and not a['original_candidates']
        compares['certificates/summary.json']={'full_equality_except':['elapsed_seconds'],
                            'original_elapsed_seconds':old_elapsed,'clean_elapsed_seconds':new_elapsed}
    receipt={'status':'PASS_WITH_SCOPE','python':sys.version,'source_sha256':sources,
             'commands':records,'output_comparisons':compares,'temporary_directory_removed':True,
             'fresh_lean_build':False,'original_proof':False,
             'review':'Algorithmic replay, not independent mathematical peer review.'}
    out=root/'certificates/CLEAN_REPLAY.json';out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
