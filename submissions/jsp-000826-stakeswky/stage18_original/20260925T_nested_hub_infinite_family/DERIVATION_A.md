# Stage 18 derivation, part A

At activity 1 define T_0 as one vertex. From T_(m-1), make a new vertex with 14 copies of T_(m-1) below it. Call the resulting ratio h_m and occupancy q_m. Set d_m to the nearest integer to 1/q_m, and make T_m by putting d_m copies of this intermediate tree below another new vertex.

For a rooted tree, let R be its occupied/unoccupied partition-function ratio, q=R/(1+R), and D the logarithmic derivative of R with respect to the activity. If a new root has c identical child subtrees, direct differentiation gives

R_new=(1+R)^(-c),
D_new=1-c q D.

For the quantity studied in the external large-forest argument, the root moment is

M=q(1-q)D^2.

Writing r_m,D_m,n_m for T_m and s_m=d_m q_m gives

r_m=(1+h_m)^(-d_m),
D_m=1-s_m+14s_m[r_(m-1)/(1+r_(m-1))]D_(m-1),
n_m=1+d_m(1+14n_(m-1)).

Nearest-integer rounding gives |s_m-1|<=q_m/2.
