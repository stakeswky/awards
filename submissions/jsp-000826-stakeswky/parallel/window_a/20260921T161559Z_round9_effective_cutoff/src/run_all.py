"""Run every A9 exact audit into a NEW output directory; fail closed."""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,json,subprocess,sys

def main()->None:
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    if any(a.output.iterdir()):raise SystemExit('Output directory must be empty')
    src=Path(__file__).resolve().parent
    scripts=['verify_constants_fraction.py','verify_constants_fixedpoint.py','verify_graph_identities.py']
    for name in scripts:
        raw=(src/name).read_bytes();compile(raw,str(src/name),'exec')
        subprocess.run([sys.executable,str(src/name),'--output',str(a.output)],check=True)
    x=json.loads((a.output/'CONSTANTS_FRACTION.json').read_text())
    y=json.loads((a.output/'CONSTANTS_FIXEDPOINT.json').read_text())
    g=json.loads((a.output/'GRAPH_IDENTITIES.json').read_text())
    comparisons=[]
    for name in x['intervals']:
        a1,b1=x['intervals'][name],y['intervals'][name]
        lo=max(Fraction(a1['lower_numerator'],a1['denominator']),Fraction(b1['lower_numerator'],b1['denominator']))
        hi=min(Fraction(a1['upper_numerator'],a1['denominator']),Fraction(b1['upper_numerator'],b1['denominator']))
        assert lo<=hi
        comparisons.append({'name':name,'intervals_overlap':True})
    assert x['cutoff']['decimal_digits']==y['cutoff_decimal_digits']==782678
    outputs=[]
    for f in sorted(a.output.glob('*.json')):
        raw=f.read_bytes();outputs.append({'path':f.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    summary={'status':'PASS_EXACT_FINITE_AUDITS','cutoff':'2^2600000','decimal_digits':782678,
        'analytic_proof':'PROOF.md; checks do not substitute for the all-forest proof',
        'rational_checks':x['finite_check_count'],'interval_cross_checks':comparisons,
        'graph_counts':g['counts'],'outputs':outputs,
        'source_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(src.glob('*.py'))},
        'full_forest_search':False,'cutoff_order_graphs_computed':0,'all_lower_orders_closed':False,
        'old_author_programs_replayed':False,'Lean':'NOT_RUN','axiom_audit':'NOT_RUN','external_review':'NOT_PERFORMED'}
    (a.output/'SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print('A9 PASS; explicit upper cutoff, not ORIGINAL closure')
if __name__=='__main__':main()
