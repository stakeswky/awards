#!/usr/bin/env python3
"""Exact finite certificate for the k=3 log-concavity minor of forests.

This script uses NetworkX only for its documented nonisomorphic free-tree
generator. Every generated forest is then checked by two coefficient methods:
(1) rooted-tree dynamic programming plus component convolution;
(2) literal subset enumeration on the assembled graph.
It also checks the closed formulas for p2,p3,p4 used in the written proof.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import platform
from collections import Counter
from math import comb
from pathlib import Path

import networkx as nx

MAX_N = 11
EXPECTED_TREE_COUNTS = {1:1,2:1,3:1,4:2,5:3,6:6,7:11,8:23,9:47,10:106,11:235}
EXPECTED_FOREST_COUNTS = {1:1,2:2,3:3,4:6,5:10,6:20,7:37,8:76,9:153,10:329,11:710}


def conv(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def tree_poly_dp(G: nx.Graph):
    root = next(iter(G.nodes()))
    parent = {root: None}
    order = [root]
    for u in order:
        for v in G.neighbors(u):
            if v != parent[u] and v not in parent:
                parent[v] = u
                order.append(v)
    inc, exc = {}, {}
    for u in reversed(order):
        inc_u, exc_u = [0, 1], [1]
        for v in G.neighbors(u):
            if parent.get(v) == u:
                inc_u = conv(inc_u, exc[v])
                child_sum = [0] * max(len(inc[v]), len(exc[v]))
                for k in range(len(child_sum)):
                    child_sum[k] = (inc[v][k] if k < len(inc[v]) else 0) + (exc[v][k] if k < len(exc[v]) else 0)
                exc_u = conv(exc_u, child_sum)
        inc[u], exc[u] = inc_u, exc_u
    out = [0] * max(len(inc[root]), len(exc[root]))
    for k in range(len(out)):
        out[k] = (inc[root][k] if k < len(inc[root]) else 0) + (exc[root][k] if k < len(exc[root]) else 0)
    return out


def subset_poly(G: nx.Graph):
    nodes = list(G.nodes())
    n = len(nodes)
    index = {v:i for i,v in enumerate(nodes)}
    edge_masks = []
    for u,v in G.edges():
        edge_masks.append((1 << index[u]) | (1 << index[v]))
    out = [0] * (n+1)
    for mask in range(1 << n):
        if all((mask & e) != e for e in edge_masks):
            out[mask.bit_count()] += 1
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def tree_stats(G: nx.Graph):
    n = G.number_of_nodes()
    m = G.number_of_edges()
    s = sum(comb(d, 2) for _, d in G.degree())
    t = sum(comb(d, 3) for _, d in G.degree())
    t += sum((G.degree(u)-1)*(G.degree(v)-1) for u,v in G.edges())
    return n,m,s,t


def formulas(n,m,s,t):
    p2 = comb(n,2) - m if n >= 2 else 0
    p3 = comb(n,3) - m*(n-2) + s if n >= 3 else 0
    p4 = comb(n,4) - m*comb(n-2,2) + comb(m,2) + (n-4)*s - t if n >= 4 else 0
    return p2,p3,p4


def assemble_forest(tree_data, ids):
    G = nx.Graph()
    offset = 0
    for i in ids:
        T = tree_data[i]["graph"]
        mapping = {v: offset+j for j,v in enumerate(T.nodes())}
        H = nx.relabel_nodes(T, mapping, copy=True)
        G.add_nodes_from(H.nodes())
        G.add_edges_from(H.edges())
        offset += T.number_of_nodes()
    return G


def main(out_path: Path):
    tree_data = []
    tree_counts = Counter()
    tree_manifest = []
    for n in range(1, MAX_N+1):
        if n == 1:
            G = nx.Graph(); G.add_node(0); trees = [G]
        elif n == 2:
            G = nx.Graph(); G.add_edge(0,1); trees = [G]
        else:
            trees = list(nx.generators.nonisomorphic_trees(n))
        tree_counts[n] = len(trees)
        for j,G in enumerate(trees):
            edges = sorted(tuple(sorted(e)) for e in G.edges())
            stats = tree_stats(G)
            poly = tree_poly_dp(G)
            tree_data.append({"order":n,"index":j,"graph":G.copy(),"edges":edges,"stats":stats,"poly":poly})
            tree_manifest.append({"order":n,"index":j,"edges":edges})
    assert dict(tree_counts) == EXPECTED_TREE_COUNTS, (tree_counts, EXPECTED_TREE_COUNTS)

    forests = []
    def rec(rem, start, chosen):
        if rem == 0:
            forests.append(tuple(chosen)); return
        for i in range(start, len(tree_data)):
            order = tree_data[i]["order"]
            if order > rem:
                break
            chosen.append(i)
            rec(rem-order, i, chosen)
            chosen.pop()
    for n in range(1, MAX_N+1):
        rec(n, 0, [])

    forest_counts = Counter(sum(tree_data[i]["order"] for i in f) for f in forests)
    assert dict(forest_counts) == EXPECTED_FOREST_COUNTS, (forest_counts, EXPECTED_FOREST_COUNTS)

    minima = {}
    zero_cases = []
    checked_coefficients = 0
    manifest_hasher = hashlib.sha256()

    for ids in forests:
        n = sum(tree_data[i]["order"] for i in ids)
        m = sum(tree_data[i]["stats"][1] for i in ids)
        s = sum(tree_data[i]["stats"][2] for i in ids)
        t = sum(tree_data[i]["stats"][3] for i in ids)

        poly_dp = [1]
        for i in ids:
            poly_dp = conv(poly_dp, tree_data[i]["poly"])
        G = assemble_forest(tree_data, ids)
        poly_subset = subset_poly(G)
        assert poly_dp == poly_subset, (ids, poly_dp, poly_subset)
        checked_coefficients += len(poly_dp)

        p2,p3,p4 = formulas(n,m,s,t)
        actual = tuple(poly_dp[k] if k < len(poly_dp) else 0 for k in (2,3,4))
        assert actual == (p2,p3,p4), (ids, actual, (p2,p3,p4), (n,m,s,t))

        L3 = p3*p3 - p2*p4
        assert L3 >= 0, (ids, poly_dp, (n,m,s,t), L3)
        if n not in minima or L3 < minima[n]["L3"]:
            minima[n] = {"L3":L3,"component_type_ids":list(ids),"p":poly_dp,"invariants":{"n":n,"m":m,"s":s,"t":t}}
        if L3 == 0:
            zero_cases.append({"n":n,"component_type_ids":list(ids),"p":poly_dp})

        manifest_hasher.update((json.dumps({"ids":ids,"p":poly_dp,"inv":[n,m,s,t]}, separators=(",",":"), sort_keys=True)+"\n").encode())

    tree_manifest_sha = hashlib.sha256((json.dumps(tree_manifest, separators=(",",":"), sort_keys=True)+"\n").encode()).hexdigest()

    result = {
        "claim": "For every finite forest on at most 11 vertices, L3=p3^2-p2*p4 is nonnegative.",
        "scope": {"max_vertices":MAX_N,"unlabelled_forests":len(forests),"unlabelled_tree_types":len(tree_data)},
        "environment": {"python":platform.python_version(),"networkx":nx.__version__},
        "tree_counts": dict(sorted(tree_counts.items())),
        "forest_counts": dict(sorted(forest_counts.items())),
        "expected_tree_counts": EXPECTED_TREE_COUNTS,
        "expected_forest_counts": EXPECTED_FOREST_COUNTS,
        "verification": {
            "tree_dp_vs_literal_subset": "PASS",
            "p2_p3_p4_closed_form_vs_literal_subset": "PASS",
            "all_L3_nonnegative": "PASS",
            "coefficient_entries_compared": checked_coefficients,
            "tree_manifest_sha256": tree_manifest_sha,
            "forest_record_stream_sha256": manifest_hasher.hexdigest(),
        },
        "minimum_L3_by_n": {str(k):v for k,v in sorted(minima.items())},
        "zero_cases": zero_cases,
        "formal_status": "NOT_LEAN; exact Python finite certificate only",
        "generator_boundary": "NetworkX 3.6.1 nonisomorphic_trees supplies one representative of every free-tree isomorphism class; forests are all multisets of those representatives with total order <=11.",
    }
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps({"status":"PASS","forests":len(forests),"tree_types":len(tree_data),"coefficients":checked_coefficients,"stream_sha256":result["verification"]["forest_record_stream_sha256"]}, sort_keys=True))

if __name__ == "__main__":
    main(Path(__file__).resolve().parents[1] / "certificates" / "L3_SMALL_FORESTS.json")
