# Stage 18 derivation, part D: polynomial lower bound

By part B, the final root ratio r_m is between 1/3 and 2/5. Therefore its occupancy q=r_m/(1+r_m) lies between 1/4 and 2/7, so

q(1-q) >= 3/16.

Using part C,

M_m=q(1-q)D_m^2
>= (147/16)*(4761/400)^(m-1).

Let

alpha=log(4761/400)/log(1936)
=0.327249517292562... >0.

Part C also gives

n_m<=245776*1936^(m-1).

Therefore

M_m >= C*n_m^alpha,

where

C=(147/16)*245776^(-alpha)
=0.158177938799633... .

A positive power of n eventually dominates every fixed power of log n. Thus, for every fixed real d>=0 and constant K>0,

M_m/(log n_m)^d -> infinity.

So there is no universal fixed-degree polylogarithmic upper bound M<=K(log n)^d for this root-moment quantity over all finite unweighted trees, already at activity 1.

This supplies the analytic infinite-family argument missing from Stage 17. It does not establish the sharper numerical exponent from the parallel work, does not prove WindowLC, does not prove Erdős #993, and gives no non-unimodal forest.
