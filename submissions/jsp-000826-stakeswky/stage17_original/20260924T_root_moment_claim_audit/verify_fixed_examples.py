from decimal import Decimal, getcontext
import math

getcontext().prec = 200

C1 = [14,16385,14,81,14,80,14,81,14,80,14,80]
C3 = [18,64458869180,18,20,18,18,18,23,18,22,18,21,18,23,18,22,18,21,18,20,18,17,18,18,18,19,18,19,18,17,18,17,18,24,18,21,18,20,18,21,18,21,18,18,18,16,18,22]

def compute(counts, lam):
    L = Decimal(lam)
    R = L
    D = Decimal(1)
    n = 1
    for c in counts:
        q = R / (1 + R)
        D = 1 - Decimal(c) * q * D
        R = L / ((1 + R) ** c)
        n = 1 + c * n
    q = R / (1 + R)
    M = q * (1 - q) * D * D
    return n, M

def report(name, counts, lam):
    n, M = compute(counts, lam)
    ln_n = Decimal(str(math.log(n)))
    ratio = M / (ln_n * ln_n)
    exponent = Decimal(str(math.log(float(M)))) / ln_n
    print(name)
    print('n=', n)
    print('digits=', len(str(n)))
    print('M=', format(M, '.40E'))
    print('M_over_ln2=', format(ratio, '.40E'))
    print('logM_over_logn=', format(exponent, '.20E'))
    return n, M, ratio, exponent

n1, m1, r1, e1 = report('lambda=1', C1, '1')
n3, m3, r3, e3 = report('lambda=3', C3, '3')

assert len(str(n1)) == 21
assert m1 > Decimal('5.254278e6')
assert r1 > Decimal('2324')
assert len(str(n3)) == 71
assert m3 > Decimal('4.562449e41')
assert r3 > Decimal('1e37')
assert e3 > Decimal('0.588')
print('FIXED_EXAMPLES_CORROBORATED')
print('LOGICAL_SCOPE=finite examples lower-bound any universal C; they do not by themselves prove the ratio is unbounded as n grows')
