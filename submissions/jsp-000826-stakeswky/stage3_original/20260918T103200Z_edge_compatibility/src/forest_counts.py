"""Actual finite forest independent-set counts; no theorem inferred from tests."""
from functools import lru_cache
from math import comb


def vertices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def add(a, b):
    return tuple((a[k] if k < len(a) else 0) +
                 (b[k] if k < len(b) else 0) for k in range(max(len(a), len(b))))


def convolution(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return tuple(out)


def positional_product(a, b):
    # No carry: each convolution coefficient <= sum(a)*sum(b) < 2**width.
    width = max(1, (sum(a) * sum(b)).bit_length())
    x = sum(t << (width * j) for j, t in enumerate(a))
    y = sum(t << (width * j) for j, t in enumerate(b))
    z = x * y
    digit_mask = (1 << width) - 1
    return tuple((z >> (width * j)) & digit_mask
                 for j in range(len(a) + len(b) - 1))


def pad(p, order):
    assert len(p) <= order + 1
    return tuple(p) + (0,) * (order + 1 - len(p))


def valley(p):
    first = None
    for k, (a, b) in enumerate(zip(p, p[1:])):
        if a > b and first is None:
            first = k
        if a < b and first is not None:
            return first, k
    return None


def modes(p):
    if valley(p) is not None:
        raise ValueError('Mode-interval lemma requires unimodality')
    peak = max(p)
    assert peak > 0
    indices = [j for j, x in enumerate(p) if x == peak]
    assert indices == list(range(indices[0], indices[-1] + 1))
    return indices[0], indices[-1]


def interval_distance(a, b):
    return max(0, a[0] - b[1], b[0] - a[1])


class Forest:
    def __init__(self, n, edges, checkpoint=lambda: None):
        if not isinstance(n, int) or n < 0:
            raise ValueError('Invalid vertex count')
        self.n, self.edges, self.checkpoint = n, [], checkpoint
        self.adj = [0] * n
        parent = list(range(n))
        def root(v):
            while parent[v] != v:
                v = parent[v]
            return v
        seen = set()
        for a, b in edges:
            if not (isinstance(a, int) and isinstance(b, int) and 0 <= a < n and
                    0 <= b < n and a != b):
                raise ValueError('Loop or invalid endpoint')
            a, b = sorted((a, b))
            if (a, b) in seen:
                raise ValueError('Repeated edge')
            seen.add((a, b))
            ra, rb = root(a), root(b)
            if ra == rb:
                raise ValueError('Cycle')
            parent[ra] = rb
            self.edges.append((a, b))
            self.adj[a] |= 1 << b
            self.adj[b] |= 1 << a
        self.edges.sort()
        self.full = (1 << n) - 1
        self._deletion = lru_cache(None)(self._delete_compute)

    def dp(self, mask):
        self.checkpoint()
        visited = 0
        result = (1,)
        def visit(v, parent):
            nonlocal visited
            visited |= 1 << v
            z0, z1 = (1,), (0, 1)
            for w in vertices(self.adj[v] & mask):
                if w == parent:
                    continue
                a, b = visit(w, v)
                z0 = convolution(z0, add(a, b))
                z1 = convolution(z1, a)
            return z0, z1
        for v in vertices(mask):
            if not (visited & (1 << v)):
                a, b = visit(v, -1)
                result = convolution(result, add(a, b))
        return pad(result, mask.bit_count())

    def _delete_compute(self, mask):
        self.checkpoint()
        if mask == 0:
            return (1,)
        pivot = max(vertices(mask), key=lambda j: (self.adj[j] & mask).bit_count())
        if not (self.adj[pivot] & mask):
            return tuple(comb(mask.bit_count(), k) for k in range(mask.bit_count() + 1))
        remaining, components = mask, []
        while remaining:
            stack = [next(vertices(remaining))]
            comp = 0
            while stack:
                v = stack.pop()
                if comp & (1 << v):
                    continue
                comp |= 1 << v
                stack.extend(vertices(self.adj[v] & mask & ~comp))
            remaining &= ~comp
            components.append(comp)
        if len(components) > 1:
            ans = (1,)
            for comp in components:
                ans = positional_product(ans, self._deletion(comp))
            return ans
        # Recurrence side uses list accumulation, not the DP add/convolution.
        a = self._deletion(mask & ~(1 << pivot))
        b = self._deletion(mask & ~((1 << pivot) | self.adj[pivot]))
        ans = list(a) + [0] * max(0, len(b) + 1 - len(a))
        for j, value in enumerate(b):
            ans[j + 1] += value
        return tuple(ans)

    def deletion(self, mask):
        return pad(self._deletion(mask), mask.bit_count())

    def brute(self, mask):
        p = [0] * (mask.bit_count() + 1)
        sub = mask
        while True:
            if all(not (sub & (1 << a) and sub & (1 << b)) for a, b in self.edges):
                p[sub.bit_count()] += 1
            if sub == 0:
                break
            sub = (sub - 1) & mask
        return tuple(p)

    def recount(self, mask, brute=False):
        a, b = self.dp(mask), self.deletion(mask)
        assert a == b, ('full coefficient mismatch', mask, a, b)
        if brute:
            assert a == self.brute(mask)
        n = mask.bit_count()
        assert a[0] == 1
        if n:
            assert a[1] == n
        if n >= 2:
            edge_count = sum(bool(mask & (1 << u) and mask & (1 << v)) for u, v in self.edges)
            assert a[2] == comb(n, 2) - edge_count
        return a


def analyze(row, checkpoint=lambda: None, brute=False):
    g = Forest(row['n'], row['edges'], checkpoint)
    p = g.recount(g.full, brute)
    records, candidates = [], []
    if valley(p) is not None:
        candidates.append({'mask':g.full, 'counts':p, 'valley':valley(p)})
    for v in range(g.n):
        ma = g.full & ~(1 << v)
        mq = g.full & ~((1 << v) | g.adj[v])
        a0, q = g.recount(ma, brute), g.recount(mq, brute)
        a, b = pad(a0, g.n), pad((0,) + q, g.n)
        assert add(a, b) == p
        for mask, seq in ((ma, a0), (mq, q)):
            if valley(seq) is not None:
                candidates.append({'mask':mask,'counts':seq,'valley':valley(seq)})
        r = {'v':v,'degree':g.adj[v].bit_count(),'delete_mask':ma,'closed_mask':mq,
             'A':a,'B':b, 'A_unimodal':valley(a) is None, 'B_unimodal':valley(b) is None}
        if r['A_unimodal'] and r['B_unimodal']:
            am, bm = modes(a), modes(b)
            r.update({'M_A':am,'M_B':bm,'distance':interval_distance(am,bm),
                      'u':min(am[1],bm[1]),'d':max(am[0],bm[0])})
        records.append(r)
    delta = [p[k+1]-p[k] for k in range(g.n)]
    local = all(r['A_unimodal'] and r['B_unimodal'] for r in records)
    result = {'id':row['id'],'n':g.n,'edges':g.edges,'counts':p,'delta':delta,
              'unimodal':valley(p) is None,'local_deletions_unimodal':local,
              'vertices':records,'candidates':candidates}
    if g.n and local:
        U = max(r['u'] for r in records)
        D = min(r['d'] for r in records)
        result.update({'U':U,'D':D,'joint_condition':D<=U+1,
                       'good_vertices':[r['v'] for r in records if r['distance']<=1],
                       'residual_indices':list(range(U,D)),
                       'residual_delta':delta[U:D]})
        assert all(delta[k]>=0 for k in range(min(U,g.n)))
        assert all(delta[k]<=0 for k in range(D,g.n))
        if D<=U+1:
            assert valley(p) is None
        if result['good_vertices']:
            assert D<=U+1
    for k in range(g.n+1):
        assert sum(r['B'][k] for r in records) == k*p[k]
        assert sum(r['A'][k] for r in records) == (g.n-k)*p[k]
    g._deletion.cache_clear()
    return result
