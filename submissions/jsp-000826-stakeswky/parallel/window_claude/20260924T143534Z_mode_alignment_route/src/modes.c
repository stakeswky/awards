/* modes.c -- mode-alignment statistics over all free trees of order n (WROM generation as in wlc2.c).
 *
 * For a tree T and vertex v put A = I(T - v), C = I(T - N[v]), so I(T) = A + xC.
 * If A and C are unimodal with mode sets M(A), M(C) (intervals) and
 *     dist(M(A), M(C) + 1) <= 1,
 * then I(T) is unimodal (sum of two unimodal sequences whose modes are at most one apart).
 * We record, for every tree, which vertices v are "aligned" in this sense, and the shift of the
 * mode set under single-vertex deletion (mode(T - v) versus mode(T)).
 *
 * usage: modes n K id
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 34
typedef long long ll;
static int n;

/* ---- WROM free-tree generator (identical to wlc2.c) ---- */
static int next_rooted_tree(int *L, int p) {
    if (p < 0) { p = n - 1; while (L[p] == 1) p--; }
    if (p == 0) return 0;
    int q = p - 1;
    while (L[q] != L[p] - 1) q--;
    for (int i = p; i < n; i++) L[i] = L[i - p + q];
    return 1;
}
static int split_info(const int *L, int *lh, int *rh, int *leftlen, int *restlen) {
    int one_found = 0, m = -1;
    for (int i = 0; i < n; i++) if (L[i] == 1) { if (one_found) { m = i; break; } one_found = 1; }
    if (m < 0) m = n;
    int a = 0, b = 0;
    for (int i = 1; i < m; i++) if (L[i] - 1 > a) a = L[i] - 1;
    for (int i = m; i < n; i++) if (L[i] > b) b = L[i];
    *lh = a; *rh = b; *leftlen = m - 1; *restlen = 1 + (n - m);
    return m;
}
static int cmp_left_rest(const int *L, int m) {
    int len = m - 1;
    for (int i = 0; i < len; i++) {
        int x = L[1 + i] - 1;
        int y = (i == 0) ? 0 : L[m + i - 1];
        if (x != y) return x > y ? 1 : -1;
    }
    return 0;
}
static void next_tree(int *L) {
    int lh, rh, ll_, rl;
    int m = split_info(L, &lh, &rh, &ll_, &rl);
    int valid = rh >= lh;
    if (valid && rh == lh) {
        if (ll_ > rl) valid = 0;
        else if (ll_ == rl && cmp_left_rest(L, m) > 0) valid = 0;
    }
    if (valid) return;
    int p = ll_;
    int oldp = L[p];
    next_rooted_tree(L, p);
    if (oldp > 2) {
        int lh2, rh2, a2, b2;
        split_info(L, &lh2, &rh2, &a2, &b2);
        int slen = lh2 + 1;
        for (int i = 0; i < slen; i++) L[n - slen + i] = 1 + i;
    }
}

/* ---- independence polynomial of T minus a deleted vertex set (bitmask) ---- */
static int par[MAXN], deg[MAXN];
static void parents_from_levels(const int *L) {
    int stackv[MAXN], sp = 0;
    for (int i = 0; i < n; i++) {
        while (sp && L[stackv[sp - 1]] >= L[i]) sp--;
        par[i] = sp ? stackv[sp - 1] : -1;
        stackv[sp++] = i;
    }
    for (int i = 0; i < n; i++) deg[i] = 0;
    for (int i = 1; i < n; i++) { deg[i]++; deg[par[i]]++; }
}
/* returns degree a; p[0..a] */
static int indep_poly_del(uint32_t del, ll *p) {
    static ll A[MAXN][MAXN + 1], B[MAXN][MAXN + 1];
    static int dA[MAXN], dB[MAXN];
    for (int v = 0; v < n; v++) {
        A[v][0] = 1; dA[v] = 0;
        if (del >> v & 1) { B[v][0] = 0; dB[v] = 0; } else { B[v][0] = 0; B[v][1] = 1; dB[v] = 1; }
    }
    static ll S[MAXN + 1], T[MAXN + 1];
    for (int v = n - 1; v >= 1; v--) {
        int u = par[v];
        int dS = dA[v] > dB[v] ? dA[v] : dB[v];
        for (int k = 0; k <= dS; k++) S[k] = (k <= dA[v] ? A[v][k] : 0) + (k <= dB[v] ? B[v][k] : 0);
        /* A[u] *= S  (u excluded or deleted: child unconstrained) */
        int da = dA[u];
        memset(T, 0, sizeof(ll) * (da + dS + 1));
        for (int i = 0; i <= da; i++) if (A[u][i]) for (int k = 0; k <= dS; k++) T[i + k] += A[u][i] * S[k];
        dA[u] = da + dS; memcpy(A[u], T, sizeof(ll) * (dA[u] + 1));
        /* B[u] *= A[v]  (u included: child excluded); if u deleted B[u] stays 0 */
        if (!(del >> u & 1)) {
            int db = dB[u], dv = dA[v];
            memset(T, 0, sizeof(ll) * (db + dv + 1));
            for (int i = 0; i <= db; i++) if (B[u][i]) for (int k = 0; k <= dv; k++) T[i + k] += B[u][i] * A[v][k];
            dB[u] = db + dv; memcpy(B[u], T, sizeof(ll) * (dB[u] + 1));
        }
    }
    int d = dA[0] > dB[0] ? dA[0] : dB[0];
    for (int k = 0; k <= d; k++) p[k] = (k <= dA[0] ? A[0][k] : 0) + (k <= dB[0] ? B[0][k] : 0);
    while (d > 0 && p[d] == 0) d--;
    return d;
}
/* mode set of a sequence; returns 1 if unimodal (plateaus allowed) */
static int mode_set(const ll *p, int a, int *m1, int *m2) {
    ll mx = 0; for (int k = 0; k <= a; k++) if (p[k] > mx) mx = p[k];
    int lo = -1, hi = -1;
    for (int k = 0; k <= a; k++) if (p[k] == mx) { if (lo < 0) lo = k; hi = k; }
    *m1 = lo; *m2 = hi;
    for (int k = 0; k < lo; k++) if (p[k] > p[k + 1]) return 0;
    for (int k = hi; k < a; k++) if (p[k] < p[k + 1]) return 0;
    for (int k = lo; k < hi; k++) if (p[k] != p[k + 1]) return 0;
    return 1;
}
static int interval_dist(int a1, int a2, int b1, int b2) {  /* 0 if overlap, else gap */
    if (b1 > a2) return b1 - a2;
    if (a1 > b2) return a1 - b2;
    return 0;
}
/* signed shift of [b1,b2] relative to [a1,a2]: 0 overlap, + if b right of a, - if left */
static int signed_shift(int a1, int a2, int b1, int b2) {
    if (b1 > a2) return b1 - a2;
    if (a1 > b2) return -(a1 - b2);
    return 0;
}

#define SH 9   /* shifts -4..4 */
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: modes n K id\n"); return 2; }
    n = atoi(argv[1]); int K = atoi(argv[2]), id = atoi(argv[3]);
    int L[MAXN]; int k0 = 0;
    for (int i = 0; i <= n / 2; i++) L[k0++] = i;
    for (int i = 1; i < (n + 1) / 2; i++) L[k0++] = i;
    ll idx = 0, trees = 0, nonuni = 0;
    ll any_aligned = 0, leaf_aligned = 0, rule_minsupp = 0, deg23_aligned = 0, deg123_aligned = 0, all_leaves_aligned = 0;
    ll shift_by_deg[MAXN][SH]; memset(shift_by_deg, 0, sizeof shift_by_deg);      /* mode(T-v) vs mode(T) */
    ll align_by_deg[MAXN][SH]; memset(align_by_deg, 0, sizeof align_by_deg);      /* signed shift of M(C)+1 vs M(A) */
    ll leafsplit_shift[SH]; memset(leafsplit_shift, 0, sizeof leafsplit_shift);   /* for leaf v: M(T-v-u) vs M(T-v) (support u), signed */
    ll leafsplit_by_suppdeg[MAXN][SH]; memset(leafsplit_by_suppdeg, 0, sizeof leafsplit_by_suppdeg);
    int worst_min_dist = 0;
    ll p[MAXN + 2], pa[MAXN + 2], pc[MAXN + 2];
    for (;;) {
        next_tree(L);
        if (idx % K == id) {
            trees++;
            parents_from_levels(L);
            int a = indep_poly_del(0, p);
            int t1, t2; int uni = mode_set(p, a, &t1, &t2);
            if (!uni) nonuni++;
            int min_dist = 1000, leaf_min = 1000, d23_min = 1000, d123_min = 1000, all_leaf_ok = 1;
            int min_supp_deg = 1000;
            for (int v = 0; v < n; v++) if (deg[v] == 1) {
                int u = -1;
                if (v > 0) u = par[v]; else { for (int w = 1; w < n; w++) if (par[w] == 0) { u = w; break; } }
                if (deg[u] < min_supp_deg) min_supp_deg = deg[u];
            }
            int rule_ok = 0;
            for (int v = 0; v < n; v++) {
                uint32_t Nv = 1u << v;
                if (v > 0) Nv |= 1u << par[v];
                for (int w = 1; w < n; w++) if (par[w] == v) Nv |= 1u << w;
                int aa = indep_poly_del(1u << v, pa);
                int ac = indep_poly_del(Nv, pc);
                int a1, a2, c1, c2;
                int ua = mode_set(pa, aa, &a1, &a2), uc = mode_set(pc, ac, &c1, &c2);
                if (!ua || !uc) { fprintf(stderr, "non-unimodal piece n=%d\n", n); }
                int dist = interval_dist(a1, a2, c1 + 1, c2 + 1);
                int ssh = signed_shift(a1, a2, c1 + 1, c2 + 1);
                if (ssh < -4) ssh = -4; if (ssh > 4) ssh = 4;
                align_by_deg[deg[v]][ssh + 4]++;
                int sh = signed_shift(t1, t2, a1, a2);       /* mode(T - v) relative to mode(T) */
                if (sh < -4) sh = -4; if (sh > 4) sh = 4;
                shift_by_deg[deg[v]][sh + 4]++;
                if (dist < min_dist) min_dist = dist;
                if (deg[v] == 1) {
                    if (dist < leaf_min) leaf_min = dist;
                    if (dist > 1) all_leaf_ok = 0;
                    /* support vertex */
                    int u = -1;
                    if (v > 0) u = par[v]; else { for (int w = 1; w < n; w++) if (par[w] == 0) { u = w; break; } }
                    int ss = signed_shift(a1, a2, c1, c2); if (ss < -4) ss = -4; if (ss > 4) ss = 4;
                    leafsplit_shift[ss + 4]++;
                    leafsplit_by_suppdeg[deg[u]][ss + 4]++;
                    if (deg[u] == min_supp_deg && dist <= 1) rule_ok = 1;
                }
                if (deg[v] == 2 || deg[v] == 3) { if (dist < d23_min) d23_min = dist; }
                if (deg[v] >= 1 && deg[v] <= 3) { if (dist < d123_min) d123_min = dist; }
            }
            if (min_dist <= 1) any_aligned++;
            if (leaf_min <= 1) leaf_aligned++;
            if (rule_ok) rule_minsupp++;
            if (d23_min <= 1) deg23_aligned++;
            if (d123_min <= 1) deg123_aligned++;
            if (all_leaf_ok) all_leaves_aligned++;
            if (min_dist > worst_min_dist) worst_min_dist = min_dist;
            if (min_dist > 1 || leaf_min > 1) {
                printf("EX n=%d min_dist=%d leaf_min=%d levels=", n, min_dist, leaf_min);
                for (int i = 0; i < n; i++) printf("%d%c", L[i], i + 1 < n ? ',' : ' ');
                printf("p=");
                for (int t = 0; t <= a; t++) printf("%lld%c", p[t], t < a ? ',' : '\n');
            }
        }
        idx++;
        if (!next_rooted_tree(L, -1)) break;
    }
    printf("SUMMARY n=%d trees=%lld nonunimodal=%lld any_aligned=%lld leaf_aligned=%lld rule_leaf_at_min_degree_support=%lld deg2or3_aligned=%lld deg1to3_aligned=%lld all_leaves_aligned=%lld worst_min_dist=%d\n",
           n, trees, nonuni, any_aligned, leaf_aligned, rule_minsupp, deg23_aligned, deg123_aligned, all_leaves_aligned, worst_min_dist);
    printf("SHIFT_MODE_TminusV_vs_T (rows: degree of v; cols: signed shift -4..4)\n");
    for (int d = 1; d < n; d++) { int any = 0; for (int s = 0; s < SH; s++) if (shift_by_deg[d][s]) any = 1; if (!any) continue;
        printf("SHIFT deg=%d", d); for (int s = 0; s < SH; s++) printf(" %lld", shift_by_deg[d][s]); printf("\n"); }
    printf("ALIGN_MC1_vs_MA (rows: degree of v; cols: signed shift of M(C)+1 relative to M(A), -4..4)\n");
    for (int d = 1; d < n; d++) { int any = 0; for (int s = 0; s < SH; s++) if (align_by_deg[d][s]) any = 1; if (!any) continue;
        printf("ALIGN deg=%d", d); for (int s = 0; s < SH; s++) printf(" %lld", align_by_deg[d][s]); printf("\n"); }
    printf("LEAFSPLIT M(T-v-u) relative to M(T-v), rows: degree of support u; cols -4..4\n");
    for (int d = 1; d < n; d++) { int any = 0; for (int s = 0; s < SH; s++) if (leafsplit_by_suppdeg[d][s]) any = 1; if (!any) continue;
        printf("LEAFSPLIT suppdeg=%d", d); for (int s = 0; s < SH; s++) printf(" %lld", leafsplit_by_suppdeg[d][s]); printf("\n"); }
    return 0;
}
