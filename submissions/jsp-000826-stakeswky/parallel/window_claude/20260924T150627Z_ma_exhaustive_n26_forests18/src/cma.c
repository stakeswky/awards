/* cma.c -- mode-alignment (MA) check over all free trees of order n, centroid enumeration.
 *
 * Trees are generated exactly as in cwlc.c (each free tree once: centroid + multiset of rooted
 * subtrees, or a bicentroid pair). For every tree T with independence sequence p = I(T):
 *
 *   A vertex v is ALIGNED if dist(M(I(T-v)), M(I(T-N[v])) + 1) <= 1, where M(.) is the set of
 *   indices attaining the maximum. I(T) = I(T-v) + x I(T-N[v]), so one deletion DP for
 *   C = I(T-N[v]) gives A = I(T-v) = p - xC for free. For a leaf v with support u,
 *   I(T-u) = (1+x) I(T-u-v), so C = I(T-u)/(1+x): one DP per support vertex serves all its leaves.
 *
 * Per tree the program scans the leaves (grouped by support), then the other vertices in order
 * of increasing degree, and stops at the first aligned vertex. It records
 *   - whether some leaf is aligned, and otherwise which vertex is (degree),
 *   - the pendant-leaf statistic (S2): the signed shift of M(I(T-v)) relative to M(I(T)) for every
 *     leaf v (expected in {-1, 0}),
 *   - with -DFULL: the shift of M(I(T-w)) relative to M(I(T)) for EVERY vertex w (S1) and the
 *     alignment distance of every vertex (histograms by degree), at the cost of one DP per vertex.
 * Every tree without an aligned leaf, and every tree without any aligned vertex, is printed with its
 * parent array so that it can be re-verified independently.
 * Exact 64-bit integer arithmetic throughout (coefficients < 2^n, n <= 32).
 *
 * usage: cma n [threads]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>

#define MAXN 34
#define PL 36
typedef long long ll;
typedef unsigned long long u64;

static int n;
/* ---------- rooted trees (as in cwlc.c) ---------- */
static int NR = 0, CAP = 0;
static int *rsize, *chstart, *chcnt, *chpool; static int POOL = 0, POOLCAP = 0;
static ll (*RF)[PL], (*RG)[PL];
static int first_of_size[MAXN + 2];

static void polymul(const ll *a, int da, const ll *b, int db, ll *out) {
    for (int k = 0; k <= da + db; k++) out[k] = 0;
    for (int i = 0; i <= da; i++) { ll x = a[i]; if (!x) continue; for (int j = 0; j <= db; j++) out[i + j] += x * b[j]; }
}
static int deg_of(const ll *a, int d) { while (d > 0 && a[d] == 0) d--; return d; }
static void add_rooted(int s, const int *kids, int nk, const ll *F, const ll *G) {
    if (NR == CAP) {
        CAP = CAP ? 2 * CAP : 1024;
        rsize = realloc(rsize, sizeof(int) * CAP); chstart = realloc(chstart, sizeof(int) * CAP); chcnt = realloc(chcnt, sizeof(int) * CAP);
        RF = realloc(RF, sizeof(ll) * PL * CAP); RG = realloc(RG, sizeof(ll) * PL * CAP);
    }
    if (POOL + nk > POOLCAP) { POOLCAP = POOLCAP ? 2 * POOLCAP + nk : 4096; chpool = realloc(chpool, sizeof(int) * POOLCAP); }
    rsize[NR] = s; chstart[NR] = POOL; chcnt[NR] = nk;
    for (int i = 0; i < nk; i++) chpool[POOL++] = kids[i];
    memcpy(RF[NR], F, sizeof(ll) * PL); memcpy(RG[NR], G, sizeof(ll) * PL);
    NR++;
}
static int gk[MAXN]; static ll gPF[MAXN][PL], gPG[MAXN][PL]; static int gdF[MAXN], gdG[MAXN];
static void gen_rooted_rec(int s, int depth, int maxidx, int rem) {
    if (rem == 0) {
        ll F[PL] = {0}, G[PL] = {0};
        for (int k = 0; k <= gdF[depth]; k++) { F[k] += gPF[depth][k]; G[k] = gPF[depth][k]; }
        for (int k = 0; k <= gdG[depth]; k++) F[k + 1] += gPG[depth][k];
        add_rooted(s, gk, depth, F, G);
        return;
    }
    for (int j = maxidx; j >= 0; j--) {
        if (rsize[j] > rem) continue;
        gk[depth] = j;
        int dF = gdF[depth] + deg_of(RF[j], MAXN), dG = gdG[depth] + deg_of(RG[j], MAXN);
        polymul(gPF[depth], gdF[depth], RF[j], deg_of(RF[j], MAXN), gPF[depth + 1]);
        polymul(gPG[depth], gdG[depth], RG[j], deg_of(RG[j], MAXN), gPG[depth + 1]);
        gdF[depth + 1] = dF; gdG[depth + 1] = dG;
        gen_rooted_rec(s, depth + 1, j, rem - rsize[j]);
    }
}
static void build_rooted(int smax) {
    for (int s = 1; s <= smax; s++) {
        first_of_size[s] = NR;
        memset(gPF[0], 0, sizeof gPF[0]); memset(gPG[0], 0, sizeof gPG[0]);
        gPF[0][0] = 1; gPG[0][0] = 1; gdF[0] = 0; gdG[0] = 0;
        gen_rooted_rec(s, 0, NR - 1, s - 1);
    }
    first_of_size[smax + 1] = NR;
}

/* ---------- per-tree work: parent array, deletion DP, mode sets ---------- */
typedef struct { int par[MAXN], deg[MAXN], cnt; } Tree;
static void emit_parent(int t, int parent, Tree *T) {
    int me = T->cnt++; T->par[me] = parent;
    for (int i = 0; i < chcnt[t]; i++) emit_parent(chpool[chstart[t] + i], me, T);
}
static void build_tree(const int *kids, int nk, int bic, Tree *T) {
    T->cnt = 0;
    if (bic) { emit_parent(kids[0], -1, T); emit_parent(kids[1], 0, T); }
    else { T->par[T->cnt++] = -1; for (int i = 0; i < nk; i++) emit_parent(kids[i], 0, T); }
    for (int i = 0; i < n; i++) T->deg[i] = 0;
    for (int i = 1; i < n; i++) { T->deg[i]++; T->deg[T->par[i]]++; }
}
/* I(T - S) for a deleted set S (bitmask); parent index < child index; returns degree */
typedef struct { ll A[MAXN][PL], B[MAXN][PL]; int dA[MAXN], dB[MAXN]; ll S[PL], Tm[PL]; } DPW;
static int poly_del(const Tree *T, uint32_t del, ll *p, DPW *W) {
    for (int v = 0; v < n; v++) {
        W->A[v][0] = 1; W->dA[v] = 0; W->B[v][0] = 0;
        if (del >> v & 1) { W->dB[v] = 0; } else { W->B[v][1] = 1; W->dB[v] = 1; }
    }
    for (int v = n - 1; v >= 1; v--) {
        int u = T->par[v];
        int dS = W->dA[v] > W->dB[v] ? W->dA[v] : W->dB[v];
        for (int k = 0; k <= dS; k++) W->S[k] = (k <= W->dA[v] ? W->A[v][k] : 0) + (k <= W->dB[v] ? W->B[v][k] : 0);
        int da = W->dA[u];
        for (int k = 0; k <= da + dS; k++) W->Tm[k] = 0;
        for (int i = 0; i <= da; i++) if (W->A[u][i]) for (int k = 0; k <= dS; k++) W->Tm[i + k] += W->A[u][i] * W->S[k];
        W->dA[u] = da + dS; memcpy(W->A[u], W->Tm, sizeof(ll) * (W->dA[u] + 1));
        if (!(del >> u & 1)) {
            int db = W->dB[u], dv = W->dA[v];
            for (int k = 0; k <= db + dv; k++) W->Tm[k] = 0;
            for (int i = 0; i <= db; i++) if (W->B[u][i]) for (int k = 0; k <= dv; k++) W->Tm[i + k] += W->B[u][i] * W->A[v][k];
            W->dB[u] = db + dv; memcpy(W->B[u], W->Tm, sizeof(ll) * (W->dB[u] + 1));
        }
    }
    int d = W->dA[0] > W->dB[0] ? W->dA[0] : W->dB[0];
    for (int k = 0; k <= d; k++) p[k] = (k <= W->dA[0] ? W->A[0][k] : 0) + (k <= W->dB[0] ? W->B[0][k] : 0);
    return deg_of(p, d);
}
static int mode_set(const ll *p, int a, int *m1, int *m2) {   /* returns 1 if unimodal */
    ll mx = 0; for (int k = 0; k <= a; k++) if (p[k] > mx) mx = p[k];
    int lo = -1, hi = -1;
    for (int k = 0; k <= a; k++) if (p[k] == mx) { if (lo < 0) lo = k; hi = k; }
    *m1 = lo; *m2 = hi;
    for (int k = 0; k < lo; k++) if (p[k] > p[k + 1]) return 0;
    for (int k = hi; k < a; k++) if (p[k] < p[k + 1]) return 0;
    for (int k = lo; k < hi; k++) if (p[k] != p[k + 1]) return 0;
    return 1;
}
static int idist(int a1, int a2, int b1, int b2) { if (b1 > a2) return b1 - a2; if (a1 > b2) return a1 - b2; return 0; }
static int sshift(int a1, int a2, int b1, int b2) { if (b1 > a2) return b1 - a2; if (a1 > b2) return -(a1 - b2); return 0; }
/* A = p - x C ; returns degree of A */
static int a_from_c(const ll *p, int a, const ll *c, int dc, ll *A) {
    int d = a; for (int k = 0; k <= a; k++) A[k] = p[k] - (k >= 1 && k - 1 <= dc ? c[k - 1] : 0);
    return deg_of(A, d);
}

/* ---------- statistics ---------- */
#define SH 9
typedef struct {
    ll trees, nonuni_pieces, leaf_aligned, no_aligned_leaf, no_aligned_vertex, leaf_supp2_aligned_trees, trees_with_supp2;
    ll first_aligned_deg[MAXN];       /* degree of the aligned vertex found (leaves counted as 1) */
    ll s2_hist[SH];                   /* per leaf: shift of M(T-v) vs M(T), -4..4 */
    ll s2_by_suppdeg[MAXN][SH];       /* same by degree of the support */
    ll leafalign_by_suppdeg[MAXN][SH];/* per leaf: signed shift of M(C)+1 vs M(A), by support degree */
    ll s1_by_deg[MAXN][SH];           /* FULL: shift of M(T-w) vs M(T) by deg w */
    ll align_by_deg[MAXN][SH];        /* FULL: signed shift of M(C)+1 vs M(A) by deg v */
    int worst_best_dist;
} Stats;
static void stats_init(Stats *S) { memset(S, 0, sizeof *S); }
static void merge(Stats *T, const Stats *S) {
    T->trees += S->trees; T->nonuni_pieces += S->nonuni_pieces; T->leaf_aligned += S->leaf_aligned; T->no_aligned_leaf += S->no_aligned_leaf;
    T->no_aligned_vertex += S->no_aligned_vertex; T->leaf_supp2_aligned_trees += S->leaf_supp2_aligned_trees; T->trees_with_supp2 += S->trees_with_supp2;
    for (int d = 0; d < MAXN; d++) { T->first_aligned_deg[d] += S->first_aligned_deg[d];
        for (int s = 0; s < SH; s++) { T->s2_by_suppdeg[d][s] += S->s2_by_suppdeg[d][s]; T->leafalign_by_suppdeg[d][s] += S->leafalign_by_suppdeg[d][s];
            T->s1_by_deg[d][s] += S->s1_by_deg[d][s]; T->align_by_deg[d][s] += S->align_by_deg[d][s]; } }
    for (int s = 0; s < SH; s++) T->s2_hist[s] += S->s2_hist[s];
    if (S->worst_best_dist > T->worst_best_dist) T->worst_best_dist = S->worst_best_dist;
}
static int clamp4(int s) { return s < -4 ? -4 : (s > 4 ? 4 : s); }

static void print_tree(const char *tag, const Tree *T, const ll *p, int a, const char *extra) {
    #pragma omp critical
    {
        printf("%s %s parents=", tag, extra);
        for (int i = 0; i < n; i++) printf("%d%s", T->par[i], i + 1 < n ? "," : "");
        printf(" p=");
        for (int t = 0; t <= a; t++) printf("%lld%c", p[t], t < a ? ',' : '\n');
        fflush(stdout);
    }
}

static void check(const ll *p, int a, Stats *S, const int *kids, int nk, int bic, DPW *W) {
    Tree T; build_tree(kids, nk, bic, &T);
    S->trees++;
    int t1, t2; mode_set(p, a, &t1, &t2);
    ll C[PL], A[PL], Cu[PL];
    int best = 1000, best_deg = -1;
    int leaf_ok = 0, supp2_present = 0, supp2_ok = 0;
    /* ---- leaves, grouped by support u ---- */
    for (int u = 0; u < n; u++) {
        if (T.deg[u] < 2) continue;                /* a support vertex has degree >= 2 (n >= 3) */
        /* leaves adjacent to u: children of u of degree 1 (the root is never a leaf for n >= 4) */
        int nleaves = 0;
        for (int v = 1; v < n; v++) if (T.par[v] == u && T.deg[v] == 1) nleaves++;
        if (T.par[u] >= 0 && T.deg[T.par[u]] == 1) nleaves++;
        if (nleaves == 0) continue;
        int dcu = poly_del(&T, 1u << u, Cu, W);      /* I(T - u) = (1+x) C */
        int dc = dcu - 1; C[0] = Cu[0]; for (int k = 1; k <= dc; k++) C[k] = Cu[k] - C[k - 1];
        int da = a_from_c(p, a, C, dc, A);
        int a1, a2, c1, c2;
        if (!mode_set(A, da, &a1, &a2)) S->nonuni_pieces++;
        if (!mode_set(C, dc, &c1, &c2)) S->nonuni_pieces++;
        int dist = idist(a1, a2, c1 + 1, c2 + 1);
        int s2 = clamp4(sshift(t1, t2, a1, a2));            /* M(T - leaf) relative to M(T) */
        int la = clamp4(sshift(a1, a2, c1 + 1, c2 + 1));
        S->s2_hist[s2 + 4] += nleaves; S->s2_by_suppdeg[T.deg[u]][s2 + 4] += nleaves; S->leafalign_by_suppdeg[T.deg[u]][la + 4] += nleaves;
        if (T.deg[u] == 2) { supp2_present = 1; if (dist <= 1) supp2_ok = 1; }
        if (dist <= 1) leaf_ok = 1;
        if (dist < best) { best = dist; best_deg = 1; }
#ifdef FULL
        S->align_by_deg[1][la + 4] += nleaves;
        S->s1_by_deg[1][s2 + 4] += nleaves;
#endif
    }
    if (supp2_present) { S->trees_with_supp2++; if (supp2_ok) S->leaf_supp2_aligned_trees++; }
    if (leaf_ok) S->leaf_aligned++; else S->no_aligned_leaf++;
    /* ---- other vertices, by increasing degree; stop at the first aligned one unless FULL ---- */
    int found = leaf_ok;
    for (int dgt = 2; dgt < n && (!found ||
#ifdef FULL
        1
#else
        0
#endif
        ); dgt++) {
        for (int v = 0; v < n; v++) {
            if (T.deg[v] != dgt) continue;
            uint32_t Nv = 1u << v; if (v > 0) Nv |= 1u << T.par[v];
            for (int w = 1; w < n; w++) if (T.par[w] == v) Nv |= 1u << w;
            int dc = poly_del(&T, Nv, C, W);
            int da = a_from_c(p, a, C, dc, A);
            int a1, a2, c1, c2;
            if (!mode_set(A, da, &a1, &a2)) S->nonuni_pieces++;
            if (!mode_set(C, dc, &c1, &c2)) S->nonuni_pieces++;
            int dist = idist(a1, a2, c1 + 1, c2 + 1);
#ifdef FULL
            S->align_by_deg[dgt][clamp4(sshift(a1, a2, c1 + 1, c2 + 1)) + 4]++;
            S->s1_by_deg[dgt][clamp4(sshift(t1, t2, a1, a2)) + 4]++;
#endif
            if (dist <= 1 && !found) { found = 1; best = dist; best_deg = dgt; }
            if (dist < best) best = dist;
#ifndef FULL
            if (found) break;
#endif
        }
    }
    if (found) S->first_aligned_deg[best_deg]++; else S->no_aligned_vertex++;
    if (best > S->worst_best_dist) S->worst_best_dist = best;
    if (!found) print_tree("EX_NOALIGN", &T, p, a, "");
    else if (!leaf_ok) { char buf[64]; snprintf(buf, sizeof buf, "aligned_vertex_degree=%d", best_deg); print_tree("EX_NOLEAF", &T, p, a, buf); }
}

/* ---------- enumeration (as in cwlc.c) ---------- */
typedef struct { ll PF[MAXN][PL], PG[MAXN][PL]; int dF[MAXN], dG[MAXN]; int kids[MAXN]; } Work;
static void uni_rec(Work *Wk, int depth, int maxidx, int rem, Stats *S, DPW *W) {
    int smax = rsize[maxidx] < rem ? rsize[maxidx] : rem;
    for (int s = smax; s >= 1; s--) {
        int lo = first_of_size[s], hi = first_of_size[s + 1] - 1;
        if (hi > maxidx) hi = maxidx;
        for (int j = hi; j >= lo; j--) {
            Wk->kids[depth] = j;
            int df = deg_of(RF[j], s), dg = deg_of(RG[j], s);
            if (s == rem) {
                ll A[PL], B[PL], p[PL];
                polymul(Wk->PF[depth], Wk->dF[depth], RF[j], df, A);
                polymul(Wk->PG[depth], Wk->dG[depth], RG[j], dg, B);
                int dA = Wk->dF[depth] + df, dB = Wk->dG[depth] + dg;
                int d = dA > dB + 1 ? dA : dB + 1;
                for (int t = 0; t <= d; t++) p[t] = (t <= dA ? A[t] : 0) + (t >= 1 && t - 1 <= dB ? B[t - 1] : 0);
                d = deg_of(p, d);
                check(p, d, S, Wk->kids, depth + 1, 0, W);
            } else {
                polymul(Wk->PF[depth], Wk->dF[depth], RF[j], df, Wk->PF[depth + 1]);
                polymul(Wk->PG[depth], Wk->dG[depth], RG[j], dg, Wk->PG[depth + 1]);
                Wk->dF[depth + 1] = Wk->dF[depth] + df; Wk->dG[depth + 1] = Wk->dG[depth] + dg;
                uni_rec(Wk, depth + 1, j, rem - s, S, W);
            }
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: cma n [threads]\n"); return 2; }
    n = atoi(argv[1]);
    if (n < 4 || n > 32) { fprintf(stderr, "n out of range (4..32)\n"); return 2; }
    if (argc > 2) omp_set_num_threads(atoi(argv[2]));
    int half = n / 2, lim = (n - 1) / 2;
    build_rooted(half);
    printf("ROOTED"); for (int s = 1; s <= half; s++) printf(" %d:%d", s, first_of_size[s + 1] - first_of_size[s]); printf("\n"); fflush(stdout);
    Stats G; stats_init(&G);
    int nfirst = first_of_size[lim + 1];
    double t0 = omp_get_wtime();
    #pragma omp parallel
    {
        Stats S; stats_init(&S);
        Work *Wk = malloc(sizeof(Work)); DPW *W = malloc(sizeof(DPW));
        #pragma omp for schedule(dynamic, 1) nowait
        for (int i = nfirst - 1; i >= 0; i--) {
            int s = rsize[i];
            memset(Wk->PF[0], 0, sizeof Wk->PF[0]); memset(Wk->PG[0], 0, sizeof Wk->PG[0]);
            Wk->PF[0][0] = 1; Wk->PG[0][0] = 1; Wk->dF[0] = 0; Wk->dG[0] = 0;
            int df = deg_of(RF[i], s), dg = deg_of(RG[i], s);
            Wk->kids[0] = i;
            polymul(Wk->PF[0], 0, RF[i], df, Wk->PF[1]); polymul(Wk->PG[0], 0, RG[i], dg, Wk->PG[1]);
            Wk->dF[1] = df; Wk->dG[1] = dg;
            uni_rec(Wk, 1, i, n - 1 - s, &S, W);
        }
        if (n % 2 == 0) {
            int lo = first_of_size[half], hi = first_of_size[half + 1];
            #pragma omp for schedule(dynamic, 16) nowait
            for (int i = lo; i < hi; i++) {
                ll f1g1[PL], A[PL], B[PL], p[PL]; int kids[2];
                int d1 = deg_of(RF[i], half);
                for (int t = 0; t < PL; t++) f1g1[t] = RF[i][t] - RG[i][t];
                int e1 = deg_of(f1g1, half);
                for (int j = i; j < hi; j++) {
                    ll f2g2[PL]; for (int t = 0; t < PL; t++) f2g2[t] = RF[j][t] - RG[j][t];
                    int d2 = deg_of(RF[j], half), e2 = deg_of(f2g2, half);
                    polymul(RF[i], d1, RF[j], d2, A);
                    polymul(f1g1, e1, f2g2, e2, B);
                    int d = d1 + d2;
                    for (int t = 0; t <= d; t++) p[t] = A[t] - (t <= e1 + e2 ? B[t] : 0);
                    d = deg_of(p, d);
                    kids[0] = i; kids[1] = j;
                    check(p, d, &S, kids, 2, 1, W);
                }
            }
        }
        #pragma omp critical
        merge(&G, &S);
        free(Wk); free(W);
    }
    double t1 = omp_get_wtime();
    printf("S2 leaf_shift_hist(-4..4):"); for (int s = 0; s < SH; s++) printf(" %lld", G.s2_hist[s]); printf("\n");
    for (int d = 2; d < n; d++) { int any = 0; for (int s = 0; s < SH; s++) if (G.s2_by_suppdeg[d][s]) any = 1; if (!any) continue;
        printf("S2_BY_SUPPDEG deg=%d", d); for (int s = 0; s < SH; s++) printf(" %lld", G.s2_by_suppdeg[d][s]); printf("\n"); }
    for (int d = 2; d < n; d++) { int any = 0; for (int s = 0; s < SH; s++) if (G.leafalign_by_suppdeg[d][s]) any = 1; if (!any) continue;
        printf("LEAFALIGN_BY_SUPPDEG deg=%d", d); for (int s = 0; s < SH; s++) printf(" %lld", G.leafalign_by_suppdeg[d][s]); printf("\n"); }
#ifdef FULL
    for (int d = 1; d < n; d++) { int any = 0; for (int s = 0; s < SH; s++) if (G.s1_by_deg[d][s]) any = 1; if (!any) continue;
        printf("S1_BY_DEG deg=%d", d); for (int s = 0; s < SH; s++) printf(" %lld", G.s1_by_deg[d][s]); printf("\n"); }
    for (int d = 1; d < n; d++) { int any = 0; for (int s = 0; s < SH; s++) if (G.align_by_deg[d][s]) any = 1; if (!any) continue;
        printf("ALIGN_BY_DEG deg=%d", d); for (int s = 0; s < SH; s++) printf(" %lld", G.align_by_deg[d][s]); printf("\n"); }
#endif
    printf("FIRST_ALIGNED_DEGREE"); for (int d = 1; d < n; d++) if (G.first_aligned_deg[d]) printf(" %d:%lld", d, G.first_aligned_deg[d]); printf("\n");
    printf("RESULT n=%d trees=%lld leaf_aligned=%lld no_aligned_leaf=%lld no_aligned_vertex=%lld trees_with_degree2_support=%lld of_which_leaf_at_degree2_support_aligned=%lld nonunimodal_pieces=%lld worst_best_dist=%d seconds=%.1f threads=%d\n",
           n, G.trees, G.leaf_aligned, G.no_aligned_leaf, G.no_aligned_vertex, G.trees_with_supp2, G.leaf_supp2_aligned_trees, G.nonuni_pieces, G.worst_best_dist, t1 - t0, omp_get_max_threads());
    return 0;
}
