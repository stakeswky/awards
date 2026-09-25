"""Lossless root/vertex occupancy profiles and actual external completion."""
from forest import validate,add,mul,pad,PackedForest,deletion_counter,components
from multi_edge import product,difference,shift


def joint_profiles(n,edges,root=0):
    adj=validate(n,edges)
    if not n or len(components(adj,(1<<n)-1))!=1:raise ValueError('nonempty rooted tree required')
    def go(r,parent):
        children=[go(w,r) for w in adj[r] if w!=parent]
        X=product([add(c[0],c[1]) for c in children]);Y=mul((0,1),product([c[0] for c in children]))
        profiles={r:(X,(0,),(0,),Y)}
        for j,child in enumerate(children):
            outsideM=product([add(c[0],c[1]) for i,c in enumerate(children) if i!=j])
            outsideX=product([c[0] for i,c in enumerate(children) if i!=j])
            for v,(q00,q01,q10,q11) in child[2].items():
                profiles[v]=(mul(add(q00,q10),outsideM),mul(add(q01,q11),outsideM),
                             mul((0,1),mul(q00,outsideX)),mul((0,1),mul(q01,outsideX)))
        return X,Y,profiles
    X,Y,table=go(root,-1)
    return pad(X,n),pad(Y,n),{v:tuple(pad(q,n) for q in qs) for v,qs in table.items()}


def verify_profiles(n,edges,root=0):
    X,Y,table=joint_profiles(n,edges,root)
    f=PackedForest(n,edges);count=deletion_counter(n,edges);P=count()
    assert X==count(f.full&~(1<<root)) and Y==shift(count(f.full&~f.closed[root]),1,n)
    for v,qs in table.items():
        if v==root:expected=(X,(0,)*(n+1),(0,)*(n+1),Y)
        else:
            Bv=shift(count(f.full&~f.closed[v]),1,n)
            both=(0,)*(n+1) if v in f.adj[root] else shift(count(f.full&~(f.closed[v]|f.closed[root])),2,n)
            q01=difference(Bv,both);q10=difference(Y,both)
            q00=difference(difference(difference(P,both),q01),q10)
            expected=q00,q01,q10,both
        assert tuple(qs)==expected
        assert min(z for q in qs for z in q)>=0
    return dict(X=X,Y=Y,vertices={str(v):qs for v,qs in table.items()})


def complete_profile(qs,externalX,externalY,R,n):
    q00,q01,q10,q11=qs
    L=mul(R,add(externalX,externalY));M=mul(R,externalX)
    return (pad(add(mul(L,q00),mul(M,q10)),n),
            pad(add(mul(L,q01),mul(M,q11)),n))
