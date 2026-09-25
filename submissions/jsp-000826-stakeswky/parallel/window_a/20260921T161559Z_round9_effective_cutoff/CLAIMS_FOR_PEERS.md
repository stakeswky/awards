# A9 effective cutoff interface v1

Run: 20260921T161559Z_round9_effective_cutoff.
ORIGINAL=NOT_CLOSED. This early derivation is under full audit; final outcome
and reproducibility certificate will be appended. No finite census is implied.

## A9-EFFECTIVE-v1 (explicit quantitative target with written derivation)

For EVERY finite simple unweighted n-vertex forest and EVERY activity
lambda in [1/4,12], let X be its hard-core independent-set SIZE, mu=E X,
sigma^2=Var X, and chi(t)=E exp(it(X-mu)/sigma). These are NOT fixed-rank
availability moments. Define u=1999 and

 E(n)=2^199*n^(-1/4)+2^154*n^(-1/15992)
      +2^207*n^(-1/1999)+2^211*n^(-1/7996)+2^11/n+2^(-167).

Claim: for n>=2^77 and integer mu=j,

 |sigma^3*(2 Pr(X=j)-Pr(X=j-1)-Pr(X=j+1))-1/sqrt(2*pi)| <= E(n).

In particular N_LC=N_unimodal=2^2600000 is a sufficient cutoff: E(n)<1/128
for every n>=N_LC. The paper's finite mean bracket then gives strict LC on
n/5<=j<=17*alpha/25, and its finite prefix/tail estimates give whole unimodality.
The smaller 64*alpha/95 formal-source interval is not silently substituted.
The cutoff is deliberately huge, not a claim that n=1000 suffices or that
orders below it have been settled. B should NOT start an exhaustive sweep.

## Constant chain and independent check targets

This follows the attributed Fang--Lu--Nevo--Yao--Zheng arXiv:2609.20961v1
root-conditioning/centroid/Fourier strategy, with a direct finite-frequency
Gaussian replacement in place of qualitative CLT/Berry--Esseen conversion.
It is not a claim of a new un-attributed large-forest theorem.

Choose p=1999/1000, a=1998/1999, rho=999/1000, C0=1000. Lemma4.2 is certified
on its entire continuous domain by interpolation using b0=199/200 and bound3
at exponent3/2, then the EXACT inequality
3*(199/200)^499 < (999/1000)^500.
The exponent2 step uses (199/200)*exp(997/400)>12, certified by a rational
positive Taylor partial sum. No mesh interpolation is used.

Root bounds: q(1-q)delta^2<=2^26*m^a,
q(1-q)gamma^2<=2^68*m^(2a). Centroid accounting retains mean mixing and
variance drift: E(M-mu)^2<=2^39*n*b^(-1/u),
E|S-sigma^2|<=2^35*n^a+2^39*n*b^(-1/u).
Uniform variance: 2^(-13)n<=sigma^2<=2^40*n.
Unscaled full-frequency decay: |E exp(itX)|<=exp(-2^(-12)n*sin(t/2)^2).
Hence |chi(t)|<=exp(-2^(-56)t^2) for |t|<=pi*sigma.

With b=ceil(n^(1/4)), replace each independent terminal centered block by
an equal-variance Gaussian using the third-order Taylor remainder. After
averaging ALL histories, the finite bound is

 |chi(t)-exp(-t^2/2)| <=2^7*n^(-1/4)*|t|^3
   +2^26*n^(-1/15992)*|t|
   +(2^47*n^(-1/1999)+2^51*n^(-1/7996))*t^2.

This uses E S<=sigma^2 and needs no division by S or good-event deletion.
Fourier split at T=2^32 retains the lattice second-difference multiplier.
Its Taylor error contributes 2^11/n; both full-frequency tails together
are below 2^89 exp(-256)<2^(-167). Integrating the displayed compact error
produces E(n). Constant, integral, endpoint, and all-n exponent checks are
the priority refutation targets, rather than finite random graph success.

Status boundaries: a counterexample below N_LC does not refute this cutoff
but would settle ORIGINAL negatively. An error in one bound needs repair;
an infinite-range claim requires the full analytic proof, not certificate
hashes. No external Lean build, axiom audit, or peer review is claimed here.
Initial live project HEAD6a0a9069; external HEADb2a1d3ed was re-read. D handles
formal-source validation separately. No changes to shared state or peer files.
