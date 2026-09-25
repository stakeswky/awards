# Explicit families with genuine interior equality

These constructions fill a real equality premise. They do not provide original counterexamples or a general no-rebound theorem. No novelty claim.

## 1. Paths and a parameter recurrence

For the n-vertex path, an independent k-set has ordered vertices a_1<...<a_k with a_(j+1)>=a_j+2. The transformation b_j=a_j-(j-1) is a bijection to ordinary k-subsets of {1,...,n-k+1}. Thus

    p_k = binom(n-k+1,k).

Consequently p_k=p_(k+1) is equivalent, on positive support, to

    (n-2k+1)(n-2k)=(k+1)(n-k+1),
    E(n,k)=n^2-5nk+5k^2-2k-1=0.

The pair (19,5) satisfies E=0. Define

    n'=11n-15k+8,      k'=3n-4k+2.

Expanding both sides gives E(n',k')=E(n,k) exactly. Starting at (19,5), this gives (142,39), (985,272), and infinitely many further integer pairs. To check growth and interval placement, maintain 3k+4<=n<=4k. Then

    k'>=5k+14>k,
    n'-3k'-4=2n-3k-2>0,
    n'-4k'=k-n<0.

Both inequalities are preserved. The pairs remain in positive support. For n=M and n<=4k, n(n-1)<k(4n-2), hence h<=k. Since alpha=ceil(n/2),

    alpha(n-1)/(n+alpha) >= (n-1)/3.

For every pair after the first, n>3k+4 gives beta>k+1. For the first pair, beta=ceil(180/29)=7>6 directly. Therefore every pair gives a qualified actual middle equality.

The path coefficient ratio is the product

    p_(j+1)/p_j = [(n-2j)/(j+1)] * [(n-2j+1)/(n-j+1)].

Both positive factors strictly decrease over the interior support. Hence the sequence is strictly log-concave: it increases before the equal central pair and decreases afterward. There is no earlier descent or subsequent rebound.

The first three actual paths (orders 19,142,985) were independently counted with both graph algorithms; their complete arrays also match the binomial formula. The general equality conclusion above follows from the algebraic argument, not those three samples.

## 2. A disconnected symmetric family

Take a isolated vertices, with a>=1 odd, and r disjoint three-vertex paths, with r>=5. The actual forest polynomial is

    P=(1+x)^a(1+3x+x^2)^r.

It is symmetric of odd degree alpha=a+2r=2k+1, so p_k=p_(k+1). Here n=a+3r=2k+r+1 and M=3. Since r<=k, h=floor((6k+3r)/10)+1<=k. Direct subtraction gives

    (2k+1)(2k+r)-(k+1)(4k+r+2)=k(r-4)-2>0.

Thus alpha(n-1)/(n+alpha)>k+1 and beta>k+1. These are actual interior equalities, not tail plateaus or artificial sequences.

For completeness the sequence is unimodal without using the false rule that arbitrary unimodal products are unimodal. A nonnegative symmetric unimodal finite sequence is a nonnegative sum of indicators of nested centered integer intervals: its coefficients in this decomposition are its successive increases up to the center. Convolution of two such interval indicators counts overlap of intervals as one is shifted, giving a symmetric trapezoidal, hence unimodal, sequence. A nonnegative sum preserves symmetric unimodality. Both (1,1) and (1,3,1) have this property, so their indicated product is symmetric unimodal. Thus the family cannot supply an original valley.

Five explicit members were dual-counted: (a,r)=(1,5),(3,5),(1,6),(1,10),(5,12). Every computed middle equality is followed by a strict decrease. One member, of order 16, overlaps the small equality census and is not counted twice.
