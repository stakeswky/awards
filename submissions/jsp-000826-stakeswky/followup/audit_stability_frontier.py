#!/usr/bin/env python3
"""Do not confuse a root/hub gap with a gap over every vertex.
Only root/hub failures from the frozen outside-palette probes are selected.
All vertices use packed messages; the selected U/D witnesses are independently
reconstructed by deletion recursion. This is not independent all-vertex replay.
"""
import argparse,json
from pathlib import Path
from hashlib import sha256
from branch_study import splits,modes,add
from audit_study import checker,unimodal
from stability_certificate import require,encode


def main(log,out):
    dest=Path(out);dest.mkdir(parents=True,exist_ok=False)
    rows=[];messages=0;rebuilds=0;coeffs=0;hist={};bad=[]
    for line in Path(log).read_text().splitlines():
        original=json.loads(line)
        if original['kind']!='outside-palette-probe' or original['D']-original['U']<2:continue
        p=original['parents'];pairs=splits(p);messages+=len(p)
        good=[v for v,(a,b) in enumerate(pairs) if unimodal(a) and unimodal(b)]
        failures=[v for v in range(len(p)) if v not in good]
        for a,b in pairs:require(add(a,b)==original['coefficients'],'message total mismatch')
        require(good,'no valid split; extract conditionals before continuing')
        lo={v:min(modes(pairs[v][0])[1],modes(pairs[v][1])[1]) for v in good}
        hi={v:max(modes(pairs[v][0])[0],modes(pairs[v][1])[0]) for v in good}
        vU=max(good,key=lambda v:lo[v]);vD=min(good,key=lambda v:hi[v]);U=lo[vU];D=hi[vD]
        rec,adj=checker(p);mask=(1<<len(p))-1
        for v in sorted(set([vU,vD]+failures)):
            A=list(rec(mask&~(1<<v)));B=[0]+list(rec(mask&~((1<<v)|adj[v])))
            require((A,B)==pairs[v],'selected split deletion disagreement')
            rebuilds+=1;coeffs+=len(A)+len(B)
        record={'index':original['index'],'n':len(p),'root_hub_U':original['U'],
                'root_hub_D':original['D'],'all_vertex_U':U,'all_vertex_D':D,
                'up_vertex':vU,'down_vertex':vD,'nonunimodal_conditional_vertices':failures,
                'all_vertex_gap':D-U}
        rows.append(record);hist[D-U]=hist.get(D-U,0)+1
        if failures or D-U>=2:
            bad.append({'record':original,'frontier':record,
                        'failed_conditionals':{v:pairs[v] for v in failures}})
    require(rows,'empty frontier audit')
    data=b''.join(encode(r) for r in rows);(dest/'frontier_rows.jsonl').write_bytes(data)
    summary={'status':'PASS_SELECTED_FRONTIER_AUDIT' if not bad else 'WITNESS_REQUIRES_REVIEW',
             'selected_graphs':len(rows),'packed_message_vertex_splits':messages,
             'independently_rebuilt_selected_splits':rebuilds,'selected_split_coefficients':coeffs,
             'all_vertex_gap_histogram':hist,'unresolved_witness_records':len(bad),
             'source_log_sha256':sha256(Path(log).read_bytes()).hexdigest(),
             'rows_sha256':sha256(data).hexdigest(),
             'limits':'All-vertex statistics use packed messages. Only selected certificate or failure vertices are independently recounted. No Lean, external review, original-problem solution or whole-probe all-vertex replay claim.'}
    (dest/'frontier_summary.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
    (dest/'witnesses.json').write_text(json.dumps(bad,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--log',required=True);ap.add_argument('--out',required=True)
    a=ap.parse_args();main(a.log,a.out)
