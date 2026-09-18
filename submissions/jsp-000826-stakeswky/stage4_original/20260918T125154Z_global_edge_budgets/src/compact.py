"""Lossless polynomial-table certificate; roundtrip compares all original data."""
import argparse
import base64
import copy
import gzip
import hashlib
import json
from pathlib import Path

FIELDS={'P','A','B','C','H','Z','W','K','K_from_identity','endpoint_slack','star_excess',
        'edge_deleted_P','contracted_P','available_pairs','edge_residual_sum','star_two_or_more'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out)
    inputs=['material.json','search_material.json']
    originals={name:json.loads((out/name).read_text()) for name in inputs}
    polys=[];lookup={}
    def intern(q):
        k=tuple(q)
        if k not in lookup:lookup[k]=len(polys);polys.append(q)
        return {'polynomial_id':lookup[k]}
    def encode(obj,field=None):
        if isinstance(obj,dict):return {k:encode(v,k) for k,v in obj.items()}
        if isinstance(obj,list):
            if field in FIELDS and all(type(x)==int for x in obj):return intern(obj)
            return [encode(x,field) for x in obj]
        return obj
    def decode(obj):
        if isinstance(obj,dict):
            if set(obj)=={'polynomial_id'}:return polys[obj['polynomial_id']]
            return {k:decode(v) for k,v in obj.items()}
        if isinstance(obj,list):return [decode(x) for x in obj]
        return obj
    encoded=encode(originals)
    assert decode(encoded)==originals
    compact=dict(format='exact-polynomial-table-v1',description='Lossless full material arrays including zero padding; no hash-only verification',
                 polynomials=polys,documents=encoded)
    data=(json.dumps(compact,sort_keys=True,separators=(',',':'))+'\n').encode()
    (out/'material_compact.json').write_bytes(data)
    compressed=gzip.compress(data,mtime=0)
    text=base64.encodebytes(compressed)
    (out/'material_compact.json.gz.b64').write_bytes(text)
    assert gzip.decompress(base64.decodebytes(text))==data
    evidence=dict(material_records=sum(len(x) for x in originals.values()),unique_polynomials=len(polys),
                  full_decoded_material_equal=True,full_gzip_bytes_equal=True,
                  sha256={name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in inputs+['material_compact.json','material_compact.json.gz.b64']},
                  discovery_records='search_records.json contains each full P and edge set; reproducible by search.py and included in the delivery archive',
                  compression_is_not_a_mathematical_proof=True)
    (out/'EVIDENCE.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence,indent=2))

if __name__=='__main__':main()
