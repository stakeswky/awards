"""Recreate all new C6 outputs from copied sources and compare every byte.
The separately saved C4/C5 replay receipts are NOT included in the new C6 totals.
"""
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--clean-dir',required=True);a=ap.parse_args()
    clean=Path(a.clean_dir).resolve()
    if clean==ROOT or ROOT in clean.parents or clean in ROOT.parents:
        raise ValueError('Clean directory must be outside the delivery tree')
    if clean.exists() and any(clean.iterdir()):raise ValueError('Clean directory must be empty')
    (clean/'sources').mkdir(parents=True,exist_ok=True);(clean/'certificates').mkdir(exist_ok=True)
    hashes={}
    for p in sorted((ROOT/'sources').glob('*.py')):
        shutil.copy2(p,clean/'sources'/p.name);hashes['sources/'+p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    cmds=[['sources/targeted_search.py','--out','certificates/TARGETED_SEARCH.json','--steps','250'],
      ['sources/verify_material.py','--outdir','certificates'],
      ['sources/verify_lcfree.py','--out','certificates/LCFREE_REGRESSION.json'],
      ['sources/verify_abstract.py','--out','certificates/ABSTRACT_ALGEBRA.json'],
      ['sources/audit_certificate.py','--outdir','certificates']]
    logs=[];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    for i,cmd in enumerate(cmds):
        t=time.monotonic();r=subprocess.run([sys.executable]+cmd,cwd=clean,capture_output=True,text=True,timeout=120,env=env)
        logs.append(dict(command=cmd,returncode=r.returncode,seconds=round(time.monotonic()-t,6),stdout=r.stdout,stderr=r.stderr))
        if r.returncode:raise RuntimeError(json.dumps(logs[-1]))
    names=sorted(p.name for p in (ROOT/'certificates').glob('*.json'))
    regenerated=sorted(p.name for p in (clean/'certificates').glob('*.json'))
    if names!=regenerated:raise RuntimeError('Output set differs')
    files=[]
    for name in names:
        before=(ROOT/'certificates'/name).read_bytes();after=(clean/'certificates'/name).read_bytes()
        if before!=after:raise RuntimeError('Byte mismatch: '+name)
        files.append(dict(path='certificates/'+name,bytes=len(after),sha256=hashlib.sha256(after).hexdigest()))
    record=dict(status='PASS_BYTE_IDENTICAL',scope='NEW_C6_ONLY',program_invocations=len(cmds),outputs=len(files),
      bytes_compared=sum(f['bytes'] for f in files),source_hashes=hashes,files=files,
      finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,
      commands=logs,Lean='NOT_RUN',axiom_audit='NOT_RUN',external_peer_review=False)
    (ROOT/'REPLAY.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print({k:record[k] for k in ['status','scope','program_invocations','outputs','bytes_compared']})
if __name__=='__main__':main()
