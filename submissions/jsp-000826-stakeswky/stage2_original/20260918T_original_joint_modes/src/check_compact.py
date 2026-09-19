#!/usr/bin/env python3
"""Lossless deduplication of every material graph's whole and A/B polynomial."""
import argparse,json
from pathlib import Path


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--material',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    material=json.loads(args.material.read_text());polynomials=[];ids={}
    def key(p):
        k=tuple(p)
        if k not in ids:ids[k]=len(polynomials);polynomials.append(p)
        return ids[k]
    rows=[]
    for g in material['graph_witnesses']:
        row={k:g[k] for k in ['id','n','edges','unimodal','U','D','good_vertices']}
        row['counts_id']=key(g['counts']);row['vertices']=[]
        for v in g['vertices']:
            row['vertices'].append({'v':v['v'],'A_id':key(v['A']),'B_id':key(v['B']),
                                    'M_A':v['M_A'],'M_B':v['M_B']})
        rows.append(row)
    out={'description':'Full zero-padded polynomials of all four material graphs and all A/B splits, deduplicated by exact tuple equality. No counts are dropped.',
         'polynomials':polynomials,'graphs':rows}
    args.out.write_text(json.dumps(out,separators=(',',':'))+'\n')
    saved=json.loads(args.out.read_text());table=saved['polynomials']
    for original,encoded in zip(material['graph_witnesses'],saved['graphs'],strict=True):
        assert original['counts']==table[encoded['counts_id']]
        for a,b in zip(original['vertices'],encoded['vertices'],strict=True):
            assert a['v']==b['v'] and a['M_A']==b['M_A'] and a['M_B']==b['M_B']
            assert a['A']==table[b['A_id']] and a['B']==table[b['B_id']]
    print(json.dumps({'status':'FULL_COEFFICIENT_ROUNDTRIP_EQUAL','graphs':len(rows),
        'vertices':sum(len(r['vertices']) for r in rows),'unique_padded_polynomials':len(polynomials)}))

if __name__=='__main__':main()
