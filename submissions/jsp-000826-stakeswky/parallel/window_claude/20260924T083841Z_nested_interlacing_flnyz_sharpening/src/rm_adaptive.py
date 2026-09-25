"""Adaptive nested-hub trees (spherically symmetric, exact level recursion):
   hub level: every vertex has k children;  gather level: every vertex has d_i children, d_i = round(y_t / log(1+R_hub)),
so that y = d_i log(1+R_hub) ~ y_t at every gather level (keeps the R-trajectory near an unstable orbit).
Root = a gather vertex, so q_root ~ l e^{-y_t}/(1+l e^{-y_t}) stays bounded below.  M = q(1-q) delta^2.
Estimate the asymptotic exponent from the increments of log M and log n over the last double levels."""
import math, sys

def build(l, k, yt, levels):
    counts = []; R = l
    for _ in range(levels):
        counts.append(k); R = l*math.exp(-k*math.log1p(R))
        d = max(1, round(yt/math.log1p(R))); counts.append(d); R = l*math.exp(-d*math.log1p(R))
    return counts

def run(counts, l):
    R, D, logn = l, 1.0, 0.0
    hist = []
    for i, c in enumerate(counts):
        q = R/(1 + R); D = 1 - c*q*D; R = l*math.exp(-c*math.log1p(R))
        logn = math.log(c) + logn + math.log1p(math.exp(-(math.log(c) + logn))) if logn else math.log(1 + c)
        if i % 2 == 1:
            qq = R/(1 + R); hist.append((logn, math.log(qq*(1 - qq)*D*D), qq))
    return hist

if __name__ == '__main__':
    for l in (0.25, 0.5, 1.0, 2.0, 2.6, 3.0, 7.0, 12.0):
        best = None
        for k in list(range(2, 41)) + [50, 60, 80, 100, 130, 170, 220, 300]:
            for yt in (0.3, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0):
                h = run(build(l, k, yt, 30), l)
                if len(h) < 30: continue
                (n1, m1, _), (n2, m2, q2) = h[19], h[29]
                if m2 <= 0: continue
                slope = (m2 - m1)/(n2 - n1)                 # asymptotic exponent estimate
                if best is None or slope > best[0]: best = (slope, k, yt, q2, h[29][0]/math.log(10), h[29][1]/math.log(10))
        print('l=%-5s best adaptive nested hubs: k=%d, y_target=%.2f -> asymptotic exponent a >= %.3f (at 30 double levels: n~10^%.0f, M~10^%.0f, q_root=%.3f)' % (
            l, best[1], best[2], best[0], best[4], best[5], best[3]), flush=True)
