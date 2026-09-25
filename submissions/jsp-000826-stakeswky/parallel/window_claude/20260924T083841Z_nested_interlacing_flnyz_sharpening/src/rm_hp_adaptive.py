"""High-precision adaptive nested-hub construction.  The child count d at each gather level is chosen from the
HIGH-PRECISION state (d = round(y_t / ln(1+R_hub))), so the exact trajectory is steered along the unstable orbit.
M = q(1-q) delta^2 at the root after each double level; exponent estimate = slope of log M vs log n over the last
levels.  Each configuration is run at two precisions (P and P+150 digits); results must agree."""
import sys
from decimal import Decimal as Dec, getcontext, localcontext

def run(l, k, yt, levels, prec):
    with localcontext() as ctx:
        ctx.prec = prec
        L = Dec(l); R = L; D = Dec(1); n = Dec(1); Y = Dec(yt); out = []
        for _ in range(levels):
            q = R/(1 + R); D = 1 - k*q*D; R = L*(-(k*(1 + R).ln())).exp(); n = 1 + k*n
            lg = (1 + R).ln(); d = max(1, int((Y/lg).to_integral_value()))
            q = R/(1 + R); D = 1 - d*q*D; R = L*(-(d*lg)).exp(); n = 1 + d*n
            qr = R/(1 + R); M = qr*(1 - qr)*D*D
            out.append((float(n.ln()), float(M.ln()) if M > 0 else float('-inf'), float(qr), d))
        return out

def slope(h, a, b):
    (n1, m1, _, _), (n2, m2, _, _) = h[a], h[b]
    return (m2 - m1)/(n2 - n1)

if __name__ == '__main__':
    import math
    cfg = {0.25: (450, 3.95), 0.5: (260, 3.517), 1.0: (70, 3.146), 2.0: (28, 2.894), 2.6: (20, 2.836), 3.0: (18, 2.814), 5.0: (10, 2.783), 7.0: (8, 2.8), 12.0: (6, 2.877)}
    levels = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    for l, (k, yt) in cfg.items():
        h1 = run(l, k, yt, levels, 250); h2 = run(l, k, yt, levels, 400)
        agree = max(abs(a[1] - b[1]) for a, b in zip(h1, h2)) < 1e-9
        s = slope(h1, levels//2, levels - 1)
        last = h1[-1]
        print('l=%-5s k=%-3d y_t=%-6s levels=%d: precisions agree=%s | final n~10^%.1f, M~10^%.1f, q_root=%.3f | exponent slope (levels %d..%d) = %.4f' % (
            l, k, yt, levels, agree, last[0]/math.log(10), last[1]/math.log(10), last[2], levels//2, levels, s), flush=True)
