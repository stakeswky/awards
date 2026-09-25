"""C6 signed ratio-cut compensation. Exact arithmetic, complete support.
No forest-wide automatic entrance is asserted. Sequences are read from graphs.
"""
from fractions import Fraction as Q

def at(a,i):
    return a[i] if 0<=i<len(a) else 0

def convolution(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def last_mode(b):
    if not b or any(x<=0 for x in b):raise ValueError('positive interval support required')
    m=max(i for i,x in enumerate(b) if x==max(b))
    if any(b[j]<b[j-1] for j in range(1,m+1)) or any(b[j]>b[j-1] for j in range(m+1,len(b))):
        raise ValueError('B must be whole-unimodal')
    return m

def cut_record(a,b,z,*,pair_audit=False):
    """z is difference index: present loss a*b[z-1]-a*b[z]."""
    if len(a)<2 or any(x<=0 for x in a):raise ValueError('A must have positive interval support of degree >=1')
    degree=len(a)-1;m=last_mode(b);pivot=z-m-1
    if not 0<=pivot<degree:raise ValueError('z outside last-mode band')
    d=[at(b,j)-at(b,j-1) for j in range(len(b)+1)]
    pos=[(j,d[j]) for j in range(m+1) if d[j]>0]
    neg=[(t,-d[t]) for t in range(m+1,len(d)) if d[t]<0]
    def gains(v):return sum(x*at(a,v-j) for j,x in pos)
    def losses(v):return sum(x*at(a,v-t) for t,x in neg)
    P,N=gains(z),losses(z);P1,N1=gains(z+1),losses(z+1)
    assert N>0 and N1>0
    ratios=[Q(a[i+1],a[i]) for i in range(degree)]+[Q(0)]
    curvature=[ratios[i]-ratios[i+1] for i in range(degree)]
    w=[];bounds=[]
    for ell in range(degree):
        gain_tail=sum(v*at(a,z-j) for j,v in pos if z-j>ell)
        loss_head=sum(v*at(a,z-t) for t,v in neg if 0<=z-t<=ell)
        wl=gain_tail*loss_head
        if ell<pivot:
            ub=P*min(N,max(a[:ell+1])*at(b,z-ell-1))
        else:
            ub=N*min(P,max(a[ell+1:])*at(b,z-ell-1))
        assert 0<=wl<=ub<=P*N
        w.append(wl);bounds.append(ub)
    birth=P*a[0]*max(0,-at(d,z+1))
    H=P*N1-P1*N
    exact_terms=[c*wi for c,wi in zip(curvature,w)]
    assert sum(exact_terms,Q(0))+birth==H
    donors=[(x,i) for i,x in enumerate(exact_terms) if x>0]
    donor_value,donor=max(donors,default=(Q(0),None))
    exact_negative=sum((-v for v in exact_terms if v<0),Q(0))
    upper_negative=sum((-c*wb for c,wb in zip(curvature,bounds) if c<0),Q(0))
    lower_H=birth+donor_value-upper_negative
    assert lower_H<=H
    loss=N-P
    nextloss=N1-P1
    payment=N1*loss+lower_H
    assert Q(payment,N)<=nextloss
    out=dict(z=z,k=z-1,m=m,pivot=pivot,P=P,N=N,P_next=P1,N_next=N1,
        present_loss=loss,next_loss=nextloss,curvature=curvature,cut_weights=w,
        negative_cut_upper_weights=bounds,birth=birth,H=H,
        exact_negative_cut_mass=exact_negative,negative_cut_upper_budget=upper_negative,
        donor_cut=donor,donor_budget=donor_value,lower_H=lower_H,
        payment=payment,next_loss_lower_bound=payment/N,
        eligible_nonincrease=loss>=0,gate=payment>=0)
    if pair_audit:
        hp=hn=0;np=nn=0;negative_pairs=[]
        for j,u in pos:
            for t,v in neg:
                det=at(a,z-j)*at(a,z+1-t)-at(a,z+1-j)*at(a,z-t)
                value=u*v*det
                if value>0:hp+=value;np+=1
                elif value<0:
                    hn-=value;nn+=1;negative_pairs.append([j,t,det,u*v,value])
        assert hp-hn==H
        out.update(pair_positive=hp,pair_negative=hn,positive_pairs=np,negative_pairs=nn,
                   negative_pair_rows=negative_pairs)
    return out

def jsonable(obj):
    if isinstance(obj,Q):return {'num':str(obj.numerator),'den':str(obj.denominator)}
    if isinstance(obj,dict):return {k:jsonable(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):return [jsonable(x) for x in obj]
    return obj
