#!/usr/bin/env python3
"""Fresh-copy replay of every deterministic output, with actual execution logs."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib,json,platform,shutil,subprocess,sys,time
BASE=Path(__file__).resolve().parents[1]
COMMANDS=['audit_selected_external.py','check_hereditary64.py','directed_terminal_search.py','large_block_obstruction.py','regressions.py','compact.py']
OUTPUTS=['external_selected_check.json','hereditary64_summary.json','terminal64_witness.json','directed_search_full.json','directed_search_summary.json','large_block_obstruction.json','regressions.json','NATIVE_CERTIFICATE.json']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources={str(p.relative_to(BASE)):sha(p) for p in sorted((BASE/'src').glob('*.py'))}
    inputs={str(p.relative_to(BASE)):sha(p) for p in sorted((BASE/'sources').glob('*.json'))}
    logs=BASE/'logs'; logs.mkdir(exist_ok=True); runs=[]; verified={}
    with TemporaryDirectory(prefix='erdos993-phase6-') as temp:
        fresh=Path(temp); (fresh/'src').mkdir(); (fresh/'sources').mkdir(); (fresh/'certificates').mkdir()
        for rel in [*sources,*inputs]: shutil.copyfile(BASE/rel,fresh/rel)
        for file in COMMANDS:
            cmd=[sys.executable,'-S','-B',str(fresh/'src'/file)]
            start=time.monotonic()
            proc=subprocess.run(cmd,cwd=fresh,capture_output=True,text=True,timeout=90)
            text=proc.stdout+'\nSTDERR:\n'+proc.stderr
            log=logs/(file+'.log'); log.write_text(text)
            runs.append({'command':['python','-S','-B','src/'+file], 'exit_code':proc.returncode,
                         'elapsed_seconds':round(time.monotonic()-start,3),'log_sha256':sha(log)})
            assert proc.returncode==0,(file,proc.stderr)
        for file in OUTPUTS:
            actual=fresh/'certificates'/file; reference=BASE/'certificates'/file
            assert actual.read_bytes()==reference.read_bytes(),file
            verified[file]={'sha256':sha(actual),'bytes':actual.stat().st_size,'comparison':'ALL_BYTES_NO_FIELDS_EXCLUDED'}
    result={'status':'PASS','python':sys.version,'platform':platform.platform(),
            'commands':runs,'outputs':verified,'source_sha256':sources,'input_sha256':inputs,
            'fresh_temporary_directory_removed':not Path(temp).exists(),
            'all_full_outputs_and_arrays_compared':True,'independent_external_review':False,
            'fresh_Lean_run':False,'original_math':'NOT_CLOSED'}
    (BASE/'certificates/CLEAN_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
