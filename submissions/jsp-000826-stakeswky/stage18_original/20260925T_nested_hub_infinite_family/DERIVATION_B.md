# Stage 18 derivation, part B: ratio invariant

Claim: for every m>=1,

1/3 < r_m < 2/5.

It is enough to prove a one-step estimate. Suppose 0<h<=1/50, q=h/(1+h), d is the nearest integer to 1/q, and r'=(1+h)^(-d). Since 1/q=1+1/h,

1/h+1/2 <= d <= 1/h+3/2.

Thus 1+h/2<=dh<=1+3h/2<=103/100.

For the lower bound on r', use (1+h)^d<=exp(dh). The exponential series gives e<11/4, and exp(x)<=1/(1-x) for 0<=x<1. Hence

exp(103/100)<(11/4)(100/97)=275/97<3,

so r'>1/3.

For the upper bound, set A=dh, B=(d-1)h, C=(d-2)h. Then A>=1, B>=99/100, C>=97/100. The first four binomial terms give

(1+h)^d >= 1+A+AB/2+ABC/6
>= 2+99/200+(99*97)/(100*100*6)
=53101/20000>5/2.

So r'<2/5.

For m=1, h_1=2^(-14)<1/50. If 1/3<r_(m-1)<2/5, then h_m<=(3/4)^14<1/50. Induction proves the invariant.
