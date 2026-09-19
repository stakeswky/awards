#!/usr/bin/env python3
"""Transcription-only consistency checks for the pinned external closure summary.

This does not enumerate trees or forests and does not recompute any independence
polynomial. It only checks integer relations copied into this package.
"""
import json
import sys

data = {
    "non_lc_tree_counts_by_order": {"26": 2, "28": 19, "29": 7, "30": 121},
    "non_lc_tree_total": 149,
    "pair_multisets": 11175,
    "pair_lc": 11078,
    "pair_non_lc": 97,
    "triple_candidates": 10823,
    "triple_hereditary_lc": 111,
    "triple_hereditary_non_lc": 0,
    "triple_nonhereditary": 10712,
    "products_checked_levels_2_3": 21998,
    "external_direct_forests_le_30": 52068524664,
}
assert sum(data["non_lc_tree_counts_by_order"].values()) == data["non_lc_tree_total"]
n = data["non_lc_tree_total"]
assert n * (n + 1) // 2 == data["pair_multisets"]
assert data["pair_lc"] + data["pair_non_lc"] == data["pair_multisets"]
assert (data["triple_hereditary_lc"] + data["triple_hereditary_non_lc"]
        + data["triple_nonhereditary"]) == data["triple_candidates"]
assert data["pair_multisets"] + data["triple_candidates"] == data["products_checked_levels_2_3"]
assert data["triple_hereditary_non_lc"] == 0

payload = {
    "kind": "TRANSCRIPTION_ONLY",
    "status": "PASS",
    "scope": "integer relations in imported external summary; no graph enumeration",
    "checks": data,
}
sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
