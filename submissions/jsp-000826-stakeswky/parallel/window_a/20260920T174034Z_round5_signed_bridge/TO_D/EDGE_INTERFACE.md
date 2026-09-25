# A5 to D: actual adjacent-root coupling, not a same-total tautology

Read PROOF.md Sections6 and8. For each actual tree edge uv,
 C=P_(T-{u,v}), D=P_(T-(N[u] union N[v])),
 B_u=xP_(T-N[u]), B_v=xP_(T-N[v]), A_u=P_(T-u), A_v=P_(T-v).
The shared adjacency enforces B_u*B_v=x^2*C*D and P=C+B_u+B_v.
For every s>=1, with zero padding,

 L_s(P)=L_s(A_u)+L_s(A_v)-L_s(C)+3(B_u)_s(B_v)_s
       -[x^(2s-2)]CD
       +sum_(|t-s|>=2) (B_u)_t(B_v)_(2s-t).

This gives a coupled signed interface from two genuine deleted forests and
one common edge neighborhood. Every remaining branch is in C,D,B_u,B_v.
It does not prove your ADMC or J_H, and does not transfer global History to
any one proper forest. The final nonnegative sum cannot safely be discarded
in a universal entrance theorem: P128,k36,HEREDITARY defeats that entrance
at all127 edges. It does not defeat A4-R (all128 roots there pass it).

The direct two-end determinant remains the old RSM obstruction. No new
relative loss/gain monotonicity is asserted. Full masks, arrays and signed
edge records can be regenerated from the supplied A5 verification source.
