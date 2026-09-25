"""Rooted trees r(n) (OEIS A000081, Euler-transform recurrence) and free trees t(n) (OEIS A000055,
Otter's dissimilarity formula t(n) = r(n) - (sum_{i+j=n} r(i) r(j) - [n even] r(n/2)) / 2).
Independent of the enumerators; used to check their tree counts."""
N = 40
r = [0] * (N + 1); r[1] = 1
for m in range(1, N):
    s = 0
    for k in range(1, m + 1):
        s += sum(d * r[d] for d in range(1, k + 1) if k % d == 0) * r[m - k + 1]
    r[m + 1] = s // m


def free(n):
    s = sum(r[i] * r[n - i] for i in range(1, n))
    if n % 2 == 0:
        s -= r[n // 2]
    return r[n] - s // 2


if __name__ == '__main__':
    for n in range(1, 37):
        print(n, r[n], free(n))
