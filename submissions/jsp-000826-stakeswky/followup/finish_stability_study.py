#!/usr/bin/env python3
"""Join completed nonoverlapping chunks and bind exact coverage and evidence."""
import argparse,json
from pathlib import Path
from hashlib import sha256
from small_palette_study import audit_coverage
from branch_study import canonical
from stability_certificate import require


def finish(chunks,out):
    dest=Path(out);dest.mkdir(parents=True,exist_ok=False)
    records=0;coeffs=0;splits=0;splitcoeffs=0;shapes=set();parts=[];by_stage={}
    with (dest/'trials.jsonl').open('wb') as f:
        for path in map(Path,chunks):
            summary=json.loads((path/'summary.json').read_text())
            blob=(path/'trials.jsonl').read_bytes()
            require(sha256(blob).hexdigest()==summary['raw_log_sha256'],'chunk hash mismatch')
            count=0
            for line in blob.splitlines():
                row=json.loads(line);records+=1;count+=1
                require(row['index']==records,'incomplete/overlapping chunks')
                shapes.add(canonical(row['parents']))
            require(count==summary['actual_records'],'chunk count mismatch')
            f.write(blob)
            coeffs+=summary['full_coefficients_compared'];splits+=summary['independently_rebuilt_splits']
            splitcoeffs+=summary['split_coefficients_compared']
            parts.append({'range':summary['requested_range'],'records':count,'sha256':summary['raw_log_sha256']})
            for key,v in summary['by_stage'].items():
                if key not in by_stage:by_stage[key]=dict(v)
                else:
                    for k,n in v.items():
                        if k=='min_n':by_stage[key][k]=min(by_stage[key][k],n)
                        elif k in ('max_n','max_root_hub_corridor'):by_stage[key][k]=max(by_stage[key][k],n)
                        else:by_stage[key][k]+=n
    coverage=audit_coverage(dest/'trials.jsonl')
    for t in range(1,5):
        stat=by_stage['palette-t'+str(t)]
        require(stat['not_LC']==0 and stat['E_not_LC']==0 and stat['conditional_witness_records']==0,
                'finite prefix theorem is not supported')
        require(stat['max_root_hub_corridor']<=1,'finite corridor prefix failed')
    result={'status':'PASS_EXACT_COMPLETE_PALETTE_T1_T4_AND_BOUNDED_PROBES',
            'records':records,'within_batch_unlabelled_structures':len(shapes),'by_stage':by_stage,
            'full_coefficients_compared':coeffs,'independently_rebuilt_splits':splits,
            'split_coefficients_compared':splitcoeffs,'coverage':coverage,'completed_chunks':parts,
            'raw_log_sha256':sha256((dest/'trials.jsonl').read_bytes()).hexdigest(),
            'new_lean_build':False,'external_peer_review':False,
            'scope':'Counts include rechecked prior palette choices and four controls. Selected root/hub corridor statistics are not all-vertex corridor statistics.'}
    (dest/'study_summary.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',required=True);a.add_argument('chunks',nargs='+')
    x=a.parse_args();finish(x.chunks,x.out)
