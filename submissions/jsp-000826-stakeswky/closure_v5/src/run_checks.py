#!/usr/bin/env python3
"""Reconstruct all finite proof certificates in a new directory, from clean sources.
Usage: python src/run_checks.py --out /new/empty/path
Python 3.10+ standard library only. Does not install or claim to run Lean.
"""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path

def main(out):
    if out.exists() and any(out.iterdir()):raise SystemExit('Output directory must be new or empty')
    out.mkdir(parents=True,exist_ok=True);(out/'logs').mkdir();(out/'certificates').mkdir()
    here=Path(__file__).resolve().parent;package=here.parent
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(here.glob('*.py'))}
    (out/'source-sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
    receipt=[]
    with tempfile.TemporaryDirectory(prefix='erdos993-clean-') as tmp:
        clean=Path(tmp)
        for p in here.glob('*.py'):shutil.copy2(p,clean/p.name)
        shutil.copy2(package/'certificates/graph-inputs.json',out/'certificates/graph-inputs.json')
        cert=out/'certificates'
        jobs=[('checker-tests',['test_checker.py'])]
        for m in ['primary','replay']:
            jobs.append((f'blocks-{m}',['verify_blocks.py','--method',m,'--out',str(cert/f'blocks-{m}.json')]))
            for t in range(4,24):
                jobs.append((f'envelope-{m}-{t:02}',['verify_envelope.py','--method',m,'--start',str(t),
                       '--end',str(t),'--out',str(cert)]))
        jobs += [('tail',['verify_tail.py','--out',str(cert/'tail.json')]),
                 ('graphs',['verify_graphs.py','--inputs',str(cert/'graph-inputs.json'),'--out',str(cert/'graphs.json')]),
                 ('summary',['verify_summary.py','--certificates',str(cert),'--out',str(cert/'FULL_CHECK.json')])]
        for name,args in jobs:
            cmd=[sys.executable,'-S','-B',str(clean/args[0]),*args[1:]]
            r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            (out/'logs'/f'{name}.log').write_text(r.stdout)
            receipt.append({'name':name,'command':cmd,'exit_code':r.returncode})
            (out/'RUN_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
            print(name,r.returncode,flush=True)
            if r.returncode:raise SystemExit(r.returncode)
    print('COMPLETE_EXACT_CERTIFICATES_PASS; formal verification NOT_ESTABLISHED',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);main(p.parse_args().out.resolve())
