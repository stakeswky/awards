"""Explicit tree constructions used by the family checks.

All constructions return parent arrays in which every parent index is smaller than
its child index (vertex 0 is the centre / root). The proper 2-colouring used
everywhere puts the root in colour class L (colour 0).
"""


def hub_tree(groups, s=0, q=0):
    """Centre 0; for every (count, leaves) in `groups`, `count` hubs adjacent to the
    centre, each carrying `leaves` pendant leaves; then `s` pendant leaves on the
    centre and `q` pendant paths of length two (centre-m-e).

    Returns (parents, vertex_types). Leaves of the same type are equivalent under
    a tree automorphism, so leaf-edge quantities only need one representative.
    """
    par = [-1]
    types = ['centre']
    for gi, (cnt, leaves) in enumerate(groups):
        for _ in range(cnt):
            h = len(par)
            par.append(0)
            types.append(f'hub{gi}')
            for _ in range(leaves):
                par.append(h)
                types.append(f'hubleaf{gi}')
    for _ in range(s):
        par.append(0)
        types.append('centreleaf')
    for _ in range(q):
        m = len(par)
        par.append(0)
        types.append('p2mid')
        par.append(m)
        types.append('p2end')
    return par, types


def hubs(t, leaves):
    """hubs(t,l): centre joined to t hubs, each hub carrying l pendant leaves.
    hubs(5,10) is the project's F56; hubs(2,l) is the subdivided double star."""
    return hub_tree(((t, leaves),))[0]


def core_tree(arms, centre_leaves=0):
    """Centre 0; hub i adjacent to the centre carries arms[i] pendant paths hub-m-e.
    core_tree((3,4,4)) is the project's 26-vertex tree T26 (Kadrawi-Levit)."""
    par = [-1]
    for s in arms:
        h = len(par)
        par.append(0)
        for _ in range(s):
            m = len(par)
            par.append(h)
            par.append(m)
    for _ in range(centre_leaves):
        par.append(0)
    return par


def edges(par):
    return [(p, v) for v, p in enumerate(par) if p >= 0]
