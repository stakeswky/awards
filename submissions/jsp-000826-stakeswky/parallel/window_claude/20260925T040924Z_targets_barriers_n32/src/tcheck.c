/* cwlc.c -- exhaustive check over all free trees of order n, by centroid decomposition.
 *
 * Independent of the WROM level-sequence checkers (wlc.c / wlc2.c) of earlier runs:
 *   - every rooted tree of order <= n/2 is generated once, as a root plus a multiset of smaller
 *     rooted trees (indices sorted by order), with f = I(tau) and g = I(tau - root);
 *   - a free tree of order n with a unique centroid is the centroid plus a multiset of rooted
 *     trees of order <= (n-1)/2 summing to n-1:  I = prod f_c + x prod g_c;
 *   - a free tree with two centroids (n even) is an unordered pair of rooted trees of order n/2
 *     joined at their roots:  I = f1 f2 - (f1-g1)(f2-g2).
 * Each free tree therefore occurs exactly once (Jordan's centroid theorem); the total is checked
 * against OEIS A000055, and the rooted counts against A000081.
 *
 * Per tree (exact integer arithmetic, __int128 products):
 *   unimodality (plateaus allowed); log-concavity at every interior index; strict log-concavity on
 *   the window [ceil(n/4), ceil((2a-1)/3)] (and on [ceil(n/4), beta] as in wlc2.c); interior
 *   log-concavity equalities anywhere (and two consecutive ones); the drift condition
 *   M1_r: (r+2) p_r p_{r+2} <= (r+1) p_{r+1}^2 + p_r p_{r+1}  (m_{r+1} <= m_r + 1, m_r=(r+1)p_{r+1}/p_r)
 *   everywhere and on [ceil(n/4), top-2]; and the checksum sum_k p_k (k+1) 0x9E3779B97F4A7C15 mod 2^64
 *   used by wlc.c / wlc2.c (order independent, so directly comparable).
 * Floating point is used only for reported extremal statistics, never for pass/fail decisions.
 *
 * usage: cwlc n [threads]      (OpenMP, dynamic schedule over the largest centroid branch)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>
#include <math.h>

#define MAXN 34
#define PL 36
typedef long long ll;
typedef __int128 i128;
typedef unsigned long long u64;

static int n;
/* rooted trees */
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
/* build rooted trees of order s: root + multiset (nonincreasing indices) of rooted trees, total s-1 */
static int gk[MAXN]; static ll gPF[MAXN][PL], gPG[MAXN][PL]; static int gdF[MAXN], gdG[MAXN];
static void gen_rooted_rec(int s, int depth, int maxidx, int rem) {
    if (rem == 0) {
        ll F[PL] = {0}, G[PL] = {0};
        /* f = prod f_c + x prod g_c ; g = prod f_c */
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
        int before = NR;
        gen_rooted_rec(s, 0, NR - 1, s - 1);
        (void)before;
    }
    first_of_size[smax + 1] = NR;
}

/* ---------- statistics ---------- */
typedef struct {
    ll trees, nonuni, nonlc, win_lm_bad, win_beta_bad, eq_win_pos, eq_win_trees;
    ll eq_any_trees, eq_consec_trees, m1_bad_any_trees, m1_bad_win_trees;
    double minrel;              /* min first-nonLC-index / alpha over non-LC trees */
    double m1_win_max; ll m1_win_arg_tree;  /* max drift d_r over r in [q, top-2] */
    double m1_any_max;          /* max drift over all r */
    double lc_win_min;          /* min n*(1 - p_{k-1}p_{k+1}/p_k^2) over k in [q, top] */
    double lc_q_min;            /* same over k in [1, min(top, a-1)] */
    double mode_over_n_min, mode_over_alpha_max;
    u64 checksum;
    char m1_win_ex[512];
} Stats;

static void stats_init(Stats *S) {
    memset(S, 0, sizeof *S);
    S->minrel = 9.0; S->m1_win_max = -1e18; S->m1_any_max = -1e18; S->lc_win_min = 1e18; S->lc_q_min = 1e18;
    S->mode_over_n_min = 9.0; S->mode_over_alpha_max = -1.0;
}

/* tree description for examples: centroid children (rooted-tree indices) or bicentroid pair */
static void emit_parent(int t, int parent, int *par, int *cnt) {
    int me = (*cnt)++; par[me] = parent;
    for (int i = 0; i < chcnt[t]; i++) emit_parent(chpool[chstart[t] + i], me, par, cnt);
}
static void describe(const int *kids, int nk, int bic, char *buf, size_t bl) {
    int par[MAXN + 2], cnt = 0;
    if (bic) { emit_parent(kids[0], -1, par, &cnt); int c0 = cnt; emit_parent(kids[1], 0, par, &cnt); (void)c0; }
    else { par[cnt++] = -1; for (int i = 0; i < nk; i++) emit_parent(kids[i], 0, par, &cnt); }
    size_t o = 0; o += snprintf(buf + o, bl - o, "parents=");
    for (int i = 0; i < cnt && o < bl; i++) o += snprintf(buf + o, bl - o, "%d%s", par[i], i + 1 < cnt ? "," : "");
}

static long double tmean(const ll *p, int a, long double lam) {
    long double num = 0, den = 0, pw = 1;
    for (int k = 0; k <= a; k++) { num += k * (long double)p[k] * pw; den += (long double)p[k] * pw; pw *= lam; }
    return num / den;
}
static void check(const ll *p, int a, Stats *S, const int *kids, int nk, int bic) {
    S->trees++;
    for (int k = 0; k <= a; k++) S->checksum += (u64)p[k] * (u64)(k + 1) * 0x9E3779B97F4A7C15ULL;
    int q = (n + 3) / 4, LM = (2 * a + 1) / 3;
    for (int k = q > 1 ? q : 1; k <= LM && k <= a - 1; k++) {
        long double lo = 1e-6L, hi = 1e6L;
        for (int it = 0; it < 90; it++) { long double mid = sqrtl(lo * hi); if (tmean(p, a, mid) < k) lo = mid; else hi = mid; }
        long double lam = sqrtl(lo * hi);
        long double sl = (2.0L * p[k] - p[k - 1] / lam - lam * p[k + 1]) / (2.0L * p[k]);
        double ns = (double)(n * sl);
        S->eq_win_pos++;                                   /* window positions tested */
        if (ns < S->lc_win_min) { S->lc_win_min = ns; describe(kids, nk, bic, S->m1_win_ex, sizeof S->m1_win_ex); }
        if ((double)lam > S->lc_q_min || S->lc_q_min > 1e17) S->lc_q_min = (double)lam;   /* reused: max lambda_k */
        if (sl < 1e-12L) { S->win_lm_bad++;
            char buf[512]; describe(kids, nk, bic, buf, sizeof buf);
            #pragma omp critical
            { printf("TCFAIL k=%d lam=%.12Lf slack=%.3Le %s\n", k, lam, sl, buf); }
        }
    }
}

/* ---------- unicentroid enumeration ---------- */
typedef struct { ll PF[MAXN][PL], PG[MAXN][PL]; int dF[MAXN], dG[MAXN]; int kids[MAXN]; } Work;

static void uni_rec(Work *W, int depth, int maxidx, int rem, Stats *S) {
    /* choose next child j <= maxidx with rsize[j] <= rem */
    int smax = rsize[maxidx] < rem ? rsize[maxidx] : rem;
    for (int s = smax; s >= 1; s--) {
        int lo = first_of_size[s], hi = first_of_size[s + 1] - 1;
        if (hi > maxidx) hi = maxidx;
        for (int j = hi; j >= lo; j--) {
            W->kids[depth] = j;
            int df = deg_of(RF[j], s), dg = deg_of(RG[j], s);
            if (s == rem) {
                ll A[PL], B[PL], p[PL];
                polymul(W->PF[depth], W->dF[depth], RF[j], df, A);
                polymul(W->PG[depth], W->dG[depth], RG[j], dg, B);
                int dA = W->dF[depth] + df, dB = W->dG[depth] + dg;
                int d = dA > dB + 1 ? dA : dB + 1;
                for (int t = 0; t <= d; t++) p[t] = (t <= dA ? A[t] : 0) + (t >= 1 && t - 1 <= dB ? B[t - 1] : 0);
                d = deg_of(p, d);
                check(p, d, S, W->kids, depth + 1, 0);
            } else {
                polymul(W->PF[depth], W->dF[depth], RF[j], df, W->PF[depth + 1]);
                polymul(W->PG[depth], W->dG[depth], RG[j], dg, W->PG[depth + 1]);
                W->dF[depth + 1] = W->dF[depth] + df; W->dG[depth + 1] = W->dG[depth] + dg;
                uni_rec(W, depth + 1, j, rem - s, S);
            }
        }
    }
}

static void merge(Stats *T, const Stats *S) {
    T->trees += S->trees; T->nonuni += S->nonuni; T->nonlc += S->nonlc; T->win_lm_bad += S->win_lm_bad; T->win_beta_bad += S->win_beta_bad;
    T->eq_win_pos += S->eq_win_pos; T->eq_win_trees += S->eq_win_trees; T->eq_any_trees += S->eq_any_trees; T->eq_consec_trees += S->eq_consec_trees;
    T->m1_bad_any_trees += S->m1_bad_any_trees; T->m1_bad_win_trees += S->m1_bad_win_trees;
    if (S->minrel < T->minrel) T->minrel = S->minrel;
    if (S->m1_win_max > T->m1_win_max) { T->m1_win_max = S->m1_win_max; memcpy(T->m1_win_ex, S->m1_win_ex, sizeof T->m1_win_ex); }
    if (S->m1_any_max > T->m1_any_max) T->m1_any_max = S->m1_any_max;
    if (S->lc_win_min < T->lc_win_min) T->lc_win_min = S->lc_win_min;
    if (S->lc_q_min < T->lc_q_min) T->lc_q_min = S->lc_q_min;
    if (S->mode_over_n_min < T->mode_over_n_min) T->mode_over_n_min = S->mode_over_n_min;
    if (S->mode_over_alpha_max > T->mode_over_alpha_max) T->mode_over_alpha_max = S->mode_over_alpha_max;
    T->checksum += S->checksum;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: cwlc n [threads]\n"); return 2; }
    n = atoi(argv[1]);
    if (n < 4 || n > 32) { fprintf(stderr, "n out of range (4..32)\n"); return 2; }
    if (argc > 2) omp_set_num_threads(atoi(argv[2]));
    int half = n / 2, lim = (n - 1) / 2;
    build_rooted(half);
    printf("ROOTED");
    for (int s = 1; s <= half; s++) printf(" %d:%d", s, first_of_size[s + 1] - first_of_size[s]);
    printf("\n"); fflush(stdout);
    Stats G; stats_init(&G);
    int nfirst = first_of_size[lim + 1];   /* candidate largest branches: all rooted trees of order <= lim */
    double t0 = omp_get_wtime();
    #pragma omp parallel
    {
        Stats S; stats_init(&S);
        Work *W = malloc(sizeof(Work));
        #pragma omp for schedule(dynamic, 1) nowait
        for (int i = nfirst - 1; i >= 0; i--) {
            int s = rsize[i];
            if (s > n - 1) continue;
            memset(W->PF[0], 0, sizeof W->PF[0]); memset(W->PG[0], 0, sizeof W->PG[0]);
            W->PF[0][0] = 1; W->PG[0][0] = 1; W->dF[0] = 0; W->dG[0] = 0;
            /* first child fixed to i: treat as depth-0 choice restricted to j == i */
            int df = deg_of(RF[i], s), dg = deg_of(RG[i], s);
            W->kids[0] = i;
            if (s == n - 1) continue; /* impossible for n >= 4 since s <= lim < n-1 */
            polymul(W->PF[0], 0, RF[i], df, W->PF[1]); polymul(W->PG[0], 0, RG[i], dg, W->PG[1]);
            W->dF[1] = df; W->dG[1] = dg;
            uni_rec(W, 1, i, n - 1 - s, &S);
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
                    check(p, d, &S, kids, 2, 1);
                }
            }
        }
        #pragma omp critical
        merge(&G, &S);
        free(W);
    }
    double t1 = omp_get_wtime();
    printf("TC n=%d trees=%lld window_positions=%lld TC_failures(slack<1e-12)=%lld min_n_slack=%.6f max_lambda_k=%.4f argmin %s checksum=%llu seconds=%.1f\n",
           n, G.trees, G.eq_win_pos, G.win_lm_bad, G.lc_win_min, G.lc_q_min, G.m1_win_ex, (unsigned long long)G.checksum, t1 - t0);
    return 0;
}
