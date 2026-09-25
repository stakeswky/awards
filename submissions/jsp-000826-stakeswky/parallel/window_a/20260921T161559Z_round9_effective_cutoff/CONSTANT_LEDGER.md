# A9 effective-constant dependency ledger

All graph quantifiers are uniform over ordinary forests, all roots, all
component sizes and all activities lambda in [1/4,12]. See PROOF.md for
proofs, not merely the inequalities in this table. X is total selected size;
none of its moments is a fixed-rank availability moment.

| Stage in the attributed FLNYZ proof | Explicit replacement used here | Proof location / finite premise |
|---|---|---|
| Fixed activity interval | [1/4,12], unchanged | Sections 1,2,10 |
| Lemma4.2: choose b near1 | b0=199/200; b0 exp(997/400)>12 | Sec2; positive rational Taylor partial sum through degree20 |
| Choose p<2, contraction rho<1 | p=1999/1000, rho=999/1000 | 3(199/200)^499<(999/1000)^500, exact powers |
| Root path weight constant | C0=(1-rho)^(-1)=1000 | Exact recurrence and Holder in Sec3 |
| Sublinear root exponent | a=1998/1999; u=1999 | a=2-2/p, u=1/(1-a), 2/3<a<1 |
| Mean-perturbation weighted square | q(1-q)delta^2<=2^26 m^a | 12*10^6*4<2^26; global exp-polynomial bound |
| Variance recurrence: choose G,L | G=1, L=1/2 | q*^(u-1)+rho q*^(u-p)<1/2 via (12/13)^26<1/4 |
| Variance forcing supremum H | H=(384000)^1999 suffices | H^(1/u)<=12*2000*16; derivative extremum for exp(-y/2)(1+y)^2 |
| Choose C1 to absorb forcing | C1=2^32 | 1-2^(-1/u)>=1/(4u); 4u*384000<2^32 |
| Variance-perturbation weighted square | q(1-q)gamma^2<=2^68 m^(2a) | 12*2^64<2^68 and log(1+y)<=y |
| Centroid path charge | sum m^a <=n b^(-1/u)/(1-2^(-1/u)) | Sec4, every possible reveal history |
| Centroid depth charge | sum m^(2a)<=n^(2a)/(1-2^(-(2a-1))) | Sec4; inverse denominator <4 |
| Conditional mean mixing | E(M-mu)^2<=2^39 n b^(-1/u) | 4u*2^26<2^39; martingale orthogonality |
| Conditional variance drift + mixing | E abs(S-sigma^2)<=2^35 n^a+2^39 n b^(-1/u) | Full gamma martingale and negative drift retained |
| Linear variance lower bound | sigma^2>=2^-13 n | Finite bipartition bound; minimum on continuous interval at an endpoint |
| Linear variance upper bound | sigma^2<=2^40 n | Centroid stop b=1, S<=n/4, total variance |
| Berry--Esseen constant | **Not used** | Sec6 replaces the CDF/CLT route by a direct Gaussian characteristic-function telescoping estimate |
| Finite independent-block replacement | b S abs(t)^3/(2sigma^3) conditionally | Third-order Taylor remainder and exact Gaussian third absolute moment |
| Block size | b=ceil(n^(1/4)) | No activity- or shape-dependent selection |
| Compact-frequency error | 2^7 n^-1/4 abs(t)^3 + 2^26 n^-1/15992 abs(t) + (2^47 n^-1/1999+2^51 n^-1/7996)t^2 | Sec6; holds for every real t, including zero conditional variance |
| Raw all-frequency bound | exp(-2^-12 n sin^2(t/2)) | Sec7; occupation factor >=1/8 and side sum >=n/338 |
| Standardized all-frequency bound | exp(-eta t^2), eta=2^-56 | Variance upper bound and pi^2<16, for abs(t)<=pi sigma |
| Fourier splitting radius | T=2^32 | n>=2^77 ensures T<=sigma |
| Exact lattice multiplier | 2sigma^2(1-cos(t/sigma)) | Retained in inversion, not replaced without an error |
| Multiplier Gaussian error | <=2^11/n | Exact fourth Gaussian moment and variance lower bound |
| Both medium/high frequency tails | <=2^89 exp(-256)<2^-167 | eta*T^2=256, integration by parts and Gaussian tail |
| Total finite-n error | E(n) in Sec1 | Sec8 integrates each term with explicit constants |
| Numerical cutoff | N_LC=2^2600000 | Sec9: slow exponent <-8, other five <-12 |
| Strict sign margin | E<21/4096<1/128; D_n>125/384 | No approximate arithmetic at N is used |
| Mean endpoint at1 | logZ(1)<=3log2*mu(1) | Rooted odds and full-forest marginals, Sec10 |
| Mean endpoint at12 | mu(12)>=c*alpha, c>680891044148/10^12>17/25 | Two different strict interval-arithmetic implementations |
| Activity tuned to each integer rank | mu continuous, lambda mu'=sigma^2>0 | Intermediate value theorem; no compactness threshold |
| Finite prefix/tail joins | n>=1000 is sufficient **only for these joins** | Sec11; prefix ceil(n/4), tail ceil((2alpha-1)/3) |
| Whole-sequence cutoff | N_unimodal=N_LC | Central LC and finite endpoints cover the entire sequence |

No row depends on an unquantified C, a numerical mesh covering a continuum,
a claim that a finite graph is above the unknown external threshold, or the
assumption that the next coefficient has already decreased. The original
external formal theorem's existential N1 is not evaluated or assumed small.
The present number follows from the new explicit chain above.

## Why the bound is large

The slow term is 2^154 n^(-1/15992). Its exponent denominator is 8u; u is
large because the conservative contraction chooses p close to2. No attempt
at optimizing that chain is made. The cutoff has exactly782678 decimal digits.
A valid finite cutoff does not make a forest enumeration beneath it feasible.
