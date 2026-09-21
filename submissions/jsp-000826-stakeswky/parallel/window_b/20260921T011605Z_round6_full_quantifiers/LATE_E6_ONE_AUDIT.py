"""Late E6-ONE-v1: enumerate the FULL widened relation, without C growth.
Run after the 16-command base replay; do not alter its receipt or counts.
Every source/target/old-load comes from the previously independently verified
complete pair-group ledger. Two adjacency enumerators are compared exactly.
Previously obtained feasible flows are independently validated under E6;
saturation proves the full-network optimum, so no new optimizer call is claimed.
"""
from pathlib import Path
import argparse, collections, gzip, hashlib, json, struct
import numpy as np

def digest(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  while b:=f.read(1024*1024):h.update(b)
 return h.hexdigest()

def run(base,out):
 out.mkdir(parents=True,exist_ok=False);reports=[]
 for label in ['network16_0','network16_2']:
  path=base/'certificates/networks'/f'{label}_JC.json'
  x=json.loads(path.read_text());sources=x['sources'];targets=x['targets']
  oldadj=x.pop('complete_adjacency');oldcount=sum(map(len,oldadj));del oldadj
  assert x['n']==16 and x['j']==6
  assert x['full_all_sources'] and x['full_all_targets'] and x['full_all_permitted_arcs']
  assert all(r['rule']=='E4_SINGLE' for r in x['reservations'])
  # Neither connected 16-vertex tree is one of the published exact Q13
  # extra-flow inputs. No unannounced matching is inserted in this ledger.
  hpath=base/'certificates/hereditary'/f'{label}_summary.json';hp=json.loads(hpath.read_text())
  assert hp['edges']==x['edges'] and hp['n']==16 and hp['proper_masks']==65535
  assert hp['HEREDITARY']=='PROVED_FINITE_ALL_PROPER_INDUCED' and not hp['bad_proper_masks']
  P=x['P'];n=x['n'];alpha=len(P)-1;h=n*(n-1)//(4*n-2)+1;beta=(alpha*(n-1)+n+alpha-1)//(n+alpha)
  k=x['j']-1;assert h<=k and k+1<beta and P[k]>P[k+1]
  posU=[r['C']|r['D'] for r in targets];vec=np.asarray(posU,dtype=np.uint32)
  full=(1<<n)-1;arc_count=0;changedC=0;zero_new=0
  apath=out/f'{label}_ALL_E6_ONE_ARCS.bin.gz'
  with apath.open('wb') as raw,gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=6) as gz:
   # uint32 LE: ns,nt, then for each source row [length,all target indices].
   gz.write(struct.pack('<II',len(sources),len(targets)))
   for si,src in enumerate(sources):
    U=src['C']|src['D'];free=full^U
    idx=np.flatnonzero(np.bitwise_count(vec&np.uint32(free))<=1)
    # Independent Python scalar enumerator, no C-increasing restriction.
    expect=[ti for ti,u in enumerate(posU) if (u&free).bit_count()<=1]
    assert idx.tolist()==expect
    for ti in expect:
     target=targets[ti];changedC+=bool(src['C']&target['C']!=src['C'])
     zero_new+=not bool(posU[ti]&free)
    arc_count+=len(expect);gz.write(struct.pack('<I',len(expect)));gz.write(idx.astype('<u4').tobytes())
  demand=sum(s['demand'] for s in sources);flow_checks=[]
  for key in ['primary_flow','secondary_flow']:
   sol=x[key];loadS=collections.Counter();loadT=collections.Counter()
   for si,ti,amount in sol['assignment']:
    assert isinstance(amount,int) and amount>0
    s=sources[si];t=targets[ti]
    assert ((t['C']|t['D'])&~(s['C']|s['D'])).bit_count()<=1
    loadS[si]+=amount;loadT[ti]+=amount
   assert all(loadS[i]==s['demand'] for i,s in enumerate(sources))
   assert all(loadT[i]<=t['remaining'] for i,t in enumerate(targets))
   assert sum(loadS.values())==demand==sol['flow']
   flow_checks.append({'inherited_algorithm':sol['method'],'validated_flow':demand,
                       'new_optimizer_call':False,'assignment_rows':len(sol['assignment'])})
  x['claim_id']='E6-ONE-v1';x['permitted_relation']='at most one new union vertex; NO C-growth restriction'
  x['all_permitted_arcs_file']=apath.name;x['arc_format']='gzip of uint32 LE: ns,nt; for each source, row length and all target indices'
  x['arc_count']=arc_count;x['previous_C_growing_arc_count']=oldcount
  x['flow_scope']='Previously computed assignments freshly checked under E6; saturation establishes optimum without a new optimization call'
  npath=out/f'{label}_E6_ONE_NETWORK.json';npath.write_text(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n')
  r={'label':label,'claim_id':'E6-ONE-v1','n':n,'j':x['j'],'h':h,'beta':beta,
     'sources':len(sources),'positive_targets':len(targets),'demand':demand,'flow':demand,
     'arcs':arc_count,'previous_C_growing_arcs':oldcount,'new_C_nongrowing_arcs':changedC,
     'zero_new_arcs':zero_new,'complete_all_sources':True,'complete_all_targets':True,'complete_all_E6_arcs':True,
     'full_H_proper_masks':65535,'independent_adjacency_enumerators':['numpy bitwise count','Python scalar bit_count'],
     'flows':flow_checks,'input_sha256':digest(path),'H_input_sha256':digest(hpath),
     'arc_file':apath.name,'arc_file_sha256':digest(apath),'arc_bytes':apath.stat().st_size,
     'network_file':npath.name,'network_file_sha256':digest(npath),'network_bytes':npath.stat().st_size,
     'ORIGINAL':'NOT_CLOSED','full_network_deficient_cut':False}
  assert arc_count>=oldcount and changedC==arc_count-oldcount
  reports.append(r);print(json.dumps(r,sort_keys=True),flush=True)
 (out/'LATE_E6_ONE_SUMMARY.json').write_text(json.dumps({'status':'PASS','instances':reports,'phase':'LATE_AFTER_BASE_REPLAY','does_not_change_base_16_commands':True},indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--base',required=True,type=Path);ap.add_argument('--output',required=True,type=Path);a=ap.parse_args();run(a.base.resolve(),a.output.resolve())
