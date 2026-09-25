## 5. Uniform numerical variance bounds

Conditioning on one bipartition class makes the available vertices in the
other class independent Bernoulli(lambda/(1+lambda)). Each neighbor is absent
with conditional probability at least 1/(1+lambda), so averaging the two
bipartition-side estimates and using Jensen with average forest degree<=2 gives

 sigma^2 >= lambda n/[2(1+lambda)^4].                         (5.1)

The function lambda/(2(1+lambda)^4) increases up to 1/3 and decreases thereafter.
Its endpoint values on K are 32/625 and 6/28561, both larger than 2^(-13).
For the upper bound set b=1 in (4.3). All terminal components are singletons,
so S<=n/4, and total variance proves

              2^(-13)n <=sigma^2<=2^40 n.                   (5.2)

These bounds hold for every n>=1. No test order supplies their constants.

## 6. A finite characteristic-function comparison, replacing Berry--Esseen

Here we avoid the paper's qualitative CDF convergence and its subsequent
compact-frequency limit. No Berry--Esseen constant is assumed to be zero or
left implicit: that theorem is NOT USED. The following elementary replacement
is enough for the Fourier argument and is proved directly.

Conditional on all centroid reveals, X is a known integer plus independent
block counts X_l with 0<=X_l<=b. Set Y_l=X_l-E X_l and v_l=Var X_l;
let Z_l be independent centered Gaussians with variances v_l. Taylor's integral
remainder gives |exp(ix)-1-ix+x^2/2|<=|x|^3/6. Also

 E|Y_l|^3<=b v_l,  E|Z_l|^3=2 sqrt(2/pi) v_l^(3/2)<=2b v_l.

The last bound uses pi>2 and v_l<=b^2. Zero variances cause no division.
The first two moments cancel when comparing the two characteristic functions.
Telescoping their products (all factors have modulus<=1) gives, at theta=t/sigma,

 |E(exp(it(X-M)/sigma) | reveals)-exp(-S t^2/(2sigma^2))|
                    <= b S |t|^3/(2 sigma^3).                (6.1)

Average over ALL reveal histories, including S=0. Since E S<=sigma^2,
the unconditional error in (6.1) is at most b|t|^3/(2sigma).
Use |exp(ix)-1|<=|x| and, for r>=0,
|exp(-r t^2/2)-exp(-t^2/2)|<=(t^2/2)|r-1| to obtain

 |chi(t)-exp(-t^2/2)|
 <= b |t|^3/(2sigma)+|t| E|M-mu|/sigma
                      +(t^2/(2sigma^2)) E|S-sigma^2|.       (6.2)

Thus neither a small-variance bad event nor a random-mean shift is discarded.
Taking b=ceil(n^(1/4)), so n^(1/4)<=b<=2n^(1/4), and applying (4.3),(5.2),
proves, for EVERY real t and n>=1,

 |chi(t)-exp(-t^2/2)|
 <=2^7 n^(-1/4)|t|^3+2^26 n^(-1/15992)|t|
                +(2^47 n^(-1/1999)+2^51 n^(-1/7996))t^2.    (6.3)

For example E|M-mu|/sigma<=2^26 b^(-1/(2u)), which is the slow term.
All numerical coefficients are checked independently by exact exponent
arithmetic. This is a finite-n estimate, not an invocation of convergence.

## 7. The full-frequency bound with its numerical constant

We repeat the argument of [FLNYZ, Lemma 6.1] with constants exposed.
Given the occupied set in bipartition class R, let B be the number of available
vertices in L. Set

 b_f=min(lambda/(1+lambda), 2lambda/(1+lambda)^2),
 h_f=1-b_f sin(t/2)^2,   lambda'=(1+lambda)h_f-1.

Then 0<=lambda'<=lambda, 0<h_f<=1 and the conditional characteristic-function
modulus is at most h_f^B, using sqrt(1-z)<=1-z/2. Put activity s on L and
lambda on R. The exact partition ratio is

 E h_f^B=Z_F(lambda',lambda)/Z_F(lambda,lambda).

At these inhomogeneous activities every R-vertex still has occupation probability
at most lambda/(1+lambda), including after specifying other R-vertices absent.
Hence logarithmic differentiation, followed by integration s from lambda'
to lambda (by continuity if lambda'=0), gives

 |E exp(itX)| <= exp(-b_f sin(t/2)^2 sum_(v in L)(1+lambda)^(-deg v)).

Choose a bipartition with |L|>=n/2. Its total degree is at most n, so Jensen
makes the last sum at least n/[2(1+lambda)^2]>=n/338.
On K, b_f>=1/8: the relevant endpoint lower bounds are 1/5,8/25,24/169.
Consequently

 |E exp(itX)|<=exp(-n sin(t/2)^2/2704)
             <=exp(-2^(-12)n sin(t/2)^2).                    (7.1)

For |t|<=pi sigma, sin(|t|/(2sigma))>=|t|/(pi sigma) and pi^2<16. By (5.2),

       |chi(t)|<=exp(-eta t^2),       eta=2^(-56).           (7.2)

This includes all medium and high frequencies in the lattice inversion
interval. The constants hold uniformly over the entire continuous K.

## 8. Effective Fourier second difference and all tails

Suppose mu=j is an integer and put T=2^32. For n>=2^77, (5.2) ensures
T<=sigma<pi sigma, so the split point lies within the Fourier interval.
Lattice inversion, including the exact second-difference multiplier, gives

 D_n:=sigma^3(2 pi_j-pi_(j-1)-pi_(j+1))
     =(1/(2pi)) integral_(-pi sigma)^(pi sigma)
                  2sigma^2(1-cos(t/sigma)) chi(t) dt.        (8.1)

Write m_sigma(t)=2sigma^2(1-cos(t/sigma)). Globally,

 0<=m_sigma(t)<=t^2,
 |m_sigma(t)-t^2|<=t^4/(12sigma^2).                          (8.2)

The Gaussian comparison integral equals
(1/(2pi)) integral_R t^2 exp(-t^2/2)dt=1/sqrt(2pi).
Split (8.1) at |t|=T. Inside use (6.3), and keep the multiplier correction
in (8.2); outside use (7.2) for chi and the Gaussian itself for the comparison.
The compact-frequency contribution is at most

 2^7 T^6 n^(-1/4)+2^26 T^4 n^(-1/15992)
                  +(2^47 n^(-1/1999)+2^51 n^(-1/7996))T^5,  (8.3)

where the dropped denominators are the FAVORABLE factors 6pi,4pi,5pi from
integrating |t|^5,|t|^3,t^4. These are upper estimates, not exact equalities.
The multiplier error over the whole Gaussian line is at most

 (1/(24pi sigma^2)) integral_R t^4 exp(-t^2/2)dt
        =1/(4sqrt(2pi)sigma^2)<=2^11/n.                     (8.4)

For every eta,T>0, integration by parts and the elementary Gaussian tail
bound give

 integral_T^infinity t^2 exp(-eta t^2)dt
 <=exp(-eta T^2)(T/(2eta)+1/(4eta^2 T)).                    (8.5)

Since eta T^2=256>=1/2, this is at most (T/eta)exp(-eta T^2).
Both tails together are at most

 (1/pi) integral_T^infinity t^2[exp(-eta t^2)+exp(-t^2/2)]dt
 <=(2T/eta)exp(-eta T^2)=2^89 exp(-256)<2^(-167),             (8.6)

using eta<=1/2, pi>1 and e>2. This upper bound includes the Gaussian beyond
pi sigma, where the lattice integral itself has stopped. It does not only
estimate a subinterval of the high-frequency domain.
Substitution of T=2^32 in (8.3)--(8.6) proves precisely (1.1).

