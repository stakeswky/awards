"""Core library for the independent colour-mass audit of Erdos #993 entrance criteria.

Independent implementation (Anthropic Claude via Claude Code), written from the
definitions in the project hand-off (technical notes, C10/E10 formulas); it is
not a replay of any window's author program.

* free trees: Wright-Richmond-Odlyzko-McKay generation (counts checked against
  OEIS A000055 by the cross-validation step);
* independence polynomials: rooted tree DP with Kronecker big-integer packing
  (all coefficients are nonnegative, so packing is carry-free);
* rows[r][l] = number of independent r-sets with l vertices in colour class L
  (colour 0, the class of the root);
* N_t=(f_{j-1}*f_{j+1})_t, P_t=(f_j*f_j)_t, Dmass=sum_t max(N_t-P_t,0);
* delta_e = exact leaf-edge cut deficit of C10 via a two-state DP over masses;
* domain(): h+1<=j<beta and History(F,j-1), with
  h=floor(M(n-1)/(4M-2))+1 and beta=ceil(alpha(n-1)/(n+alpha)).
"""

# ---------- free tree generation (Wright-Richmond-Odlyzko-McKay, as in networkx) ----------
def _next_rooted_tree(pred, p=None):
    if p is None:
        p = len(pred) - 1
        while pred[p] == 1:
            p -= 1
    if p == 0:
        return None
    q = p - 1
    while pred[q] != pred[p] - 1:
        q -= 1
    res = list(pred)
    for i in range(p, len(res)):
        res[i] = res[i - p + q]
    return res

def _split_tree(layout):
    one_found = False; m = None
    for i in range(len(layout)):
        if layout[i] == 1:
            if one_found:
                m = i; break
            one_found = True
    if m is None:
        m = len(layout)
    left = [layout[i] - 1 for i in range(1, m)]
    rest = [0] + [layout[i] for i in range(m, len(layout))]
    return left, rest

def _next_tree(cand):
    left, rest = _split_tree(cand)
    lh, rh = max(left), max(rest)
    valid = rh >= lh
    if valid and rh == lh:
        if len(left) > len(rest):
            valid = False
        elif len(left) == len(rest) and left > rest:
            valid = False
    if valid:
        return cand
    p = len(left)
    new = _next_rooted_tree(cand, p)
    if cand[p] > 2:
        nl, nr = _split_tree(new)
        suffix = list(range(1, max(nl) + 2))
        new[-len(suffix):] = suffix
    return new

def free_trees(order):
    """Yield level sequences of all non-isomorphic free trees with `order`>=2 vertices."""
    layout = list(range(order // 2 + 1)) + list(range(1, (order + 1) // 2))
    while layout is not None:
        layout = _next_tree(layout)
        if layout is not None:
            yield layout
            layout = _next_rooted_tree(layout)

def parents_from_levels(lv):
    par = [-1] * len(lv); stack = []
    for i, l in enumerate(lv):
        while stack and lv[stack[-1]] >= l:
            stack.pop()
        par[i] = stack[-1] if stack else -1
        stack.append(i)
    return par

# ---------- generic forest given by parent array (parent index < child index) ----------
def children_of(par):
    ch = [[] for _ in par]
    for v, p in enumerate(par):
        if p >= 0:
            ch[p].append(v)
    return ch

def colours(par):
    c = [0] * len(par)
    for v, p in enumerate(par):
        if p >= 0:
            c[v] = 1 - c[p]
    return c

def uni_poly(par, ch, removed=frozenset(), W=None):
    """Univariate independence polynomial coefficients of forest par minus `removed`."""
    n = len(par); W = W or n + 2
    A = [0] * n; B = [0] * n; extra = 1
    for v in range(n - 1, -1, -1):
        a = 1; b = 1
        for c in ch[v]:
            a *= A[c] + B[c]; b *= A[c]
        if v in removed:
            extra *= a; A[v] = 1; B[v] = 0
        else:
            A[v] = a; B[v] = b << W
    tot = extra
    for v in range(n):
        if par[v] < 0:
            tot *= A[v] + B[v]
    mask = (1 << W) - 1; out = []
    while tot:
        out.append(tot & mask); tot >>= W
    return out

def biv_rows(par, ch, col, removed=frozenset()):
    """Return rows[r][l] = #independent r-sets with l vertices of colour 0 (L) in forest minus removed."""
    n = len(par); W = n + 2; D = n + 1
    X = W; Y = W * D  # bit shifts for x (L) and y (R)
    A = [0] * n; B = [0] * n; extra = 1
    for v in range(n - 1, -1, -1):
        a = 1; b = 1
        for c in ch[v]:
            a *= A[c] + B[c]; b *= A[c]
        if v in removed:
            extra *= a; A[v] = 1; B[v] = 0
        else:
            A[v] = a; B[v] = b << (X if col[v] == 0 else Y)
    tot = extra
    for v in range(n):
        if par[v] < 0:
            tot *= A[v] + B[v]
    mask = (1 << W) - 1
    rows = [[0] * (r + 1) for r in range(n + 1)]
    pos = 0; maxr = 0
    while tot:
        chunk = tot & mask
        if chunk:
            l = pos % D; m = pos // D
            rows[l + m][l] = chunk
            if l + m > maxr: maxr = l + m
        tot >>= W; pos += 1
    return rows[:maxr + 1]

def row(rows, r):
    if 0 <= r < len(rows):
        return rows[r]
    return [0]

def conv(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for k, y in enumerate(b):
                if y: c[i + k] += x * y
    return c

def pad(v, L):
    return v + [0] * (L - len(v)) if len(v) < L else v

def mass_arrays(rows, j):
    L = 2 * j + 3
    N = pad(conv(row(rows, j - 1), row(rows, j + 1)), L)
    P = pad(conv(row(rows, j), row(rows, j)), L)
    return N, P

def leaf_caps(par, ch, col, rows_unused, j, u, v, L):
    K = biv_rows(par, ch, col, frozenset((u, v)))
    nbr = set(ch[v]) | ({par[v]} if par[v] >= 0 else set())
    J = biv_rows(par, ch, col, frozenset(nbr | {v}))
    cp = [0] * L; cm = [0] * L
    vL = 1 if col[v] == 0 else 0; uL = 1 if col[u] == 0 else 0
    # type 1: (I,H) with v in H, I subset K size j-1, H-v subset J size j  -> (I+u, H-v)
    q1 = conv(row(K, j - 1), row(J, j))
    # type 2: (I,H) with u in H, I subset J size j-1, H-u subset K size j -> (I+v, H-u)
    q2 = conv(row(J, j - 1), row(K, j))
    for q, start, delta in ((q1, vL, uL - vL), (q2, uL, vL - uL)):
        for s, cnt in enumerate(q):
            if cnt:
                t = s + start
                (cp if delta == 1 else cm)[t] += cnt
    return cp, cm

def cut_deficit(N, P, cp, cm):
    """max_U sum_{t in U}(N_t-P_t) - sum_{t in U,t+1 notin U} cp_t - sum_{t in U,t-1 notin U} cm_t."""
    out_best = 0; in_best = None
    for t in range(len(N)):
        w = N[t] - P[t]
        new_out = out_best if in_best is None else max(out_best, in_best - (cp[t - 1] if t else 0))
        cand = out_best - cm[t]
        if in_best is not None and in_best > cand:
            cand = in_best
        in_best = w + cand
        out_best = new_out
    return max(out_best, in_best - cp[-1])

def params(p, n, M):
    alpha = len(p) - 1
    h = M * (n - 1) // (4 * M - 2) + 1
    beta = -(-alpha * (n - 1) // (n + alpha))
    return alpha, h, beta

def domain(p, n, M):
    """j with h+1<=j<beta and History(F,j-1): a strict descent at i<=j-1 and no rise from i to j."""
    alpha, h, beta = params(p, n, M)
    get = lambda i: p[i] if 0 <= i < len(p) else 0
    first = next((k for k in range(len(p) - 1) if p[k] > p[k + 1]), None)
    out = []
    if first is None:
        return out, (alpha, h, beta, first)
    for j in range(max(h + 1, 1), beta):
        if first <= j - 1 and all(get(k) >= get(k + 1) for k in range(first, j)):
            out.append(j)
    return out, (alpha, h, beta, first)

def is_unimodal(p):
    first = next((k for k in range(len(p) - 1) if p[k] > p[k + 1]), None)
    if first is None:
        return True
    return all(p[k] >= p[k + 1] for k in range(first, len(p) - 1))

def analyse(par, want_leaves=True):
    """Return list of domain records for the forest given by parent array."""
    n = len(par); ch = children_of(par); col = colours(par)
    p = uni_poly(par, ch)
    # component sizes
    comp = [0] * n; size = {}
    for v in range(n):
        comp[v] = v if par[v] < 0 else comp[par[v]]
        size[comp[v]] = size.get(comp[v], 0) + 1
    M = max(size.values())
    js, meta = domain(p, n, M)
    recs = []
    if not js:
        return p, meta, recs
    rows = biv_rows(par, ch, col)
    assert [sum(r) for r in rows] == p, (p, [sum(r) for r in rows])
    deg = [len(ch[v]) + (1 if par[v] >= 0 else 0) for v in range(n)]
    leaves = [u for u in range(n) if deg[u] == 1]
    for j in js:
        b, a = p[j - 1], p[j]; c = p[j + 1] if j + 1 < len(p) else 0
        S = a * (b - a)
        N, P = mass_arrays(rows, j)
        assert sum(N) == b * c and sum(P) == a * a
        Dm = sum(max(x - y, 0) for x, y in zip(N, P))
        mind = None; best_leaf = None
        if want_leaves:
            L = len(N)
            for u in leaves:
                v = par[u] if par[u] >= 0 else ch[u][0]
                cp, cm = leaf_caps(par, ch, col, rows, j, u, v, L)
                d = cut_deficit(N, P, cp, cm)
                assert 0 <= d <= Dm
                if mind is None or d < mind:
                    mind = d; best_leaf = u
        recs.append(dict(j=j, b=b, a=a, c=c, S=S, Dmass=Dm, min_delta=mind, best_leaf=best_leaf,
                         LC=a * a - b * c))
    return p, meta, recs
