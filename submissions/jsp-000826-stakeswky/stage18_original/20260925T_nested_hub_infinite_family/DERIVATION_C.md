# Stage 18 derivation, part C: derivative and order growth

At the first double level, h_1=1/16384, q_1=1/16385, d_1=16385 and s_1=1. The intermediate 14-child vertex has derivative 1-14/2=-6, so D_1=7.

For m>=2, part B gives

r_(m-1)/(1+r_(m-1)) >= 1/4.

It also gives h_m<=1/50, hence q_m<1/50. Nearest-integer rounding then gives |s_m-1|<1/100 and s_m>=99/100. Therefore, once D_(m-1)>=1,

D_m >= -1/100+14(99/100)(1/4)D_(m-1)
>= (69/20)D_(m-1).

Thus

D_m >= 7(69/20)^(m-1).

For the order, part B also gives

h_m >= (5/7)^14 > 1/128

for m>=2. Therefore 1/q_m=1+1/h_m<129, so d_m<=129. The order recurrence from part A yields

n_m <= 130+1806 n_(m-1) <= 1936 n_(m-1).

The first order is

n_1=1+16385(1+14)=245776.

Hence

n_m <= 245776*1936^(m-1).
