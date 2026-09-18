"""Fresh source directory; full deterministic output comparisons."""
import hashlib,json,platform,shutil,subprocess,sys,tempfile
from datetime import datetime,timezone
from pathlib import Path


def main():
    root=Path(__file__).resolve().parent.parent;cert=root/'certificates';logs=root/'logs'
    logs.mkdir(exist_ok=True);start=datetime.now(timezone.utc).isoformat()
    sources=sorted(p for p in (root/'src').iterdir() if p.suffix in ('.py','.json'))
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    outputs=['interaction_material.json','checks_summary.json','mode_witness.json','boundary_witness.json','boundary_summary.json',
             'discovery_records.json','discovery_attempts.json','discovery_material.json','incidents.json','search_summary.json',
             'regression_summary.json','NATIVE_EVIDENCE.json','native_summary.json']
    commands=[];comparisons=[]
    with tempfile.TemporaryDirectory(prefix='erdos993-phase5-') as td:
        work=Path(td);(work/'src').mkdir();(work/'certificates').mkdir()
        for p in sources:shutil.copy2(p,work/'src'/p.name)
        for script in ['checks.py','boundary.py','search.py','regressions.py','compact.py']:
            cmd=[sys.executable,'-S','-B','src/'+script,'--out','certificates']
            result=subprocess.run(cmd,cwd=work,text=True,capture_output=True,timeout=120)
            logname='replay_'+script+'.log';(logs/logname).write_text(result.stdout+result.stderr)
            commands.append(dict(argv=cmd,exit_code=result.returncode,log='logs/'+logname))
            if result.returncode:raise RuntimeError('Fresh replay failed: '+script+'; see '+logname)
        assert sorted(p.name for p in (work/'certificates').iterdir())==sorted(outputs)
        for name in outputs:
            original=(cert/name).read_bytes();fresh=(work/'certificates'/name).read_bytes()
            assert original==fresh, ('BYTE_MISMATCH',name)
            assert json.loads(original)==json.loads(fresh), ('ARRAY_MISMATCH',name)
            comparisons.append(dict(file=name,bytes=len(fresh),sha256=hashlib.sha256(fresh).hexdigest(),
                                    full_bytes_equal=True,full_parsed_JSON_equal=True))
    receipt=dict(status='PASS',started_utc=start,finished_utc=datetime.now(timezone.utc).isoformat(),
                 python=sys.version,platform=platform.platform(),source_sha256=hashes,commands=commands,outputs=comparisons,
                 excluded_output_fields=[],temporary_directory_removed=True,review='SAME_MODEL_SELF_REVIEW',
                 independent_external_review=False,original_proved=False,formal_build='NOT_RUN')
    (cert/'CLEAN_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
