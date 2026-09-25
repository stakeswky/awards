/* ulc_vec.c -- cwlc_vec.c (run 20260925T090935Z) with the screen and the exact recheck changed to
 * ultra-log-concavity: a tree is reported (ULC line) if t p_t^2 <= (t+1) p_{t-1} p_{t+1} at some
 * interior t (equality counted separately). RESULT's nonLC field counts ULC-failing trees.
 * The per-tree LC analysis of cwlc_vec.c is not run. Exact for n <= 35 as cwlc_vec.c. */
/* cwlc_vec.c -- exhaustive check over all free trees of order n (centroid decomposition), vectorised.
 *
 * Same enumeration and the same exact per-tree statistics as cwlc.c / cwlc_lean.c:
 *   - rooted trees of order <= n/2 are generated once, as a root plus a multiset of smaller rooted
 *     trees (indices nonincreasing), with f = I(tau) and g = I(tau - root);
 *   - a unicentroid free tree is the centroid plus a multiset of rooted trees of order <= (n-1)/2
 *     summing to n-1:  I = prod f_c + x prod g_c;
 *   - a bicentroid free tree (n even) is an unordered pair of rooted trees of order n/2 joined at
 *     their roots:  I = f1 f2 - (f1-g1)(f2-g2).
 *
 * What is new (speed only, the mathematics is unchanged):
 *   - "tail tables": for every r <= R, all multisets of rooted trees of total order r (rooted forests
 *     of order r) with prod f and prod g, sorted by their largest index. When the recursion has r <= R
 *     vertices left and largest allowed index M, the allowed completions are exactly the table items
 *     whose largest index is <= M, i.e. a prefix of the sorted table. The prefix is processed in
 *     blocks of VB trees with loops the compiler vectorises.
 *   - coefficients are stored as unsigned 32-bit integers. This is exact for n <= 35: every value
 *     formed is a coefficient of I(F) for a forest F of order <= n, or a partial sum of nonnegative
 *     terms of such a coefficient; for a forest of order m <= 34, p_k <= C(34,17) < 2^32; for a tree
 *     of order n <= 35 with a leaf l adjacent to s, p_k = p_k(T-l) + p_{k-1}(T-l-s)
 *     <= C(34,17) + C(33,16) < 2^32; and in the bicentroid formula f1 f2 is a coefficient of a forest
 *     of order n <= 34, while (f1-g1)(f2-g2) <= f1 f2 coefficientwise. The program refuses n > 35 and
 *     n = 35 is unicentroid.
 *   - log-concavity is screened in double precision (every coefficient < 2^32 is exact as a double,
 *     products are within relative 2^-52), flagging any index with p_t^2 <= (1 + 2^-40) p_{t-1} p_{t+1};
 *     flagged trees (and only they) are analysed exactly (__int128) by full_check. A tree that is not
 *     flagged is strictly log-concave at every interior index, hence (positive coefficients up to its
 *     degree) unimodal with no interior equality, so it contributes nothing to any counter except
 *     trees and checksum.
 *   - the checksum sum_k p_k (k+1) 0x9E3779B97F4A7C15 mod 2^64 is linear in the coefficients, so
 *     sum_k p_k (k+1) is accumulated and multiplied by the constant at the end (identical value).
 * usage: cwlc_vec n [threads] [R]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>

#define MAXN 36
#define PL 40
#define VB 16
typedef long long ll;
typedef __int128 i128;
typedef unsigned long long u64;
typedef uint32_t cf;

static int n, RT = 12;
/* rooted trees */
static int NR = 0, CAP = 0;
static int *rsize, *chstart, *chcnt, *chpool; static int POOL = 0, POOLCAP = 0;
static cf (*RF)[PL], (*RG)[PL];
static int *rdF, *rdG;
static int first_of_size[MAXN + 2];

static inline void polymul(const cf *a, int da, const cf *b, int db, cf *out) {
    for (int k = 0; k <= da + db; k++) out[k] = 0;
    for (int i = 0; i <= da; i++) { cf x = a[i]; for (int j = 0; j <= db; j++) out[i + j] += x * b[j]; }
}
static int deg_of(const cf *a, int d) { while (d > 0 && a[d] == 0) d--; return d; }

static void add_rooted(int s, const int *kids, int nk, const cf *F, const cf *G) {
    if (NR == CAP) {
        CAP = CAP ? 2 * CAP : 1024;
        rsize = realloc(rsize, sizeof(int) * CAP); chstart = realloc(chstart, sizeof(int) * CAP); chcnt = realloc(chcnt, sizeof(int) * CAP);
        rdF = realloc(rdF, sizeof(int) * CAP); rdG = realloc(rdG, sizeof(int) * CAP);
        RF = realloc(RF, sizeof(cf) * PL * CAP); RG = realloc(RG, sizeof(cf) * PL * CAP);
    }
    if (POOL + nk > POOLCAP) { POOLCAP = POOLCAP ? 2 * POOLCAP + nk : 4096; chpool = realloc(chpool, sizeof(int) * POOLCAP); }
    rsize[NR] = s; chstart[NR] = POOL; chcnt[NR] = nk;
    for (int i = 0; i < nk; i++) chpool[POOL++] = kids[i];
    memcpy(RF[NR], F, sizeof(cf) * PL); memcpy(RG[NR], G, sizeof(cf) * PL);
    rdF[NR] = deg_of(RF[NR], PL - 1); rdG[NR] = deg_of(RG[NR], PL - 1);
    NR++;
}
static int gk[MAXN]; static cf gPF[MAXN][PL], gPG[MAXN][PL]; static int gdF[MAXN], gdG[MAXN];
static void gen_rooted_rec(int s, int depth, int maxidx, int rem) {
    if (rem == 0) {
        cf F[PL] = {0}, G[PL] = {0};
        for (int k = 0; k <= gdF[depth]; k++) { F[k] += gPF[depth][k]; G[k] = gPF[depth][k]; }
        for (int k = 0; k <= gdG[depth]; k++) F[k + 1] += gPG[depth][k];
        add_rooted(s, gk, depth, F, G);
        return;
    }
    for (int j = maxidx; j >= 0; j--) {
        if (rsize[j] > rem) { j = first_of_size[rsize[j]]; continue; }  /* skip the whole (too large) size class */
        gk[depth] = j;
        polymul(gPF[depth], gdF[depth], RF[j], rdF[j], gPF[depth + 1]);
        polymul(gPG[depth], gdG[depth], RG[j], rdG[j], gPG[depth + 1]);
        gdF[depth + 1] = gdF[depth] + rdF[j]; gdG[depth + 1] = gdG[depth] + rdG[j];
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

/* ---------- tail tables: rooted forests of order r, sorted by largest index ---------- */
typedef struct {
    int cnt, pad;          /* items, padded count (multiple of VB) */
    int *maxi;             /* largest index of each item (nondecreasing) */
    cf *FT, *GT;           /* transposed: FT[k * pad + item], k = 0..r */
    int *lstart, *llen, *lpool;  /* index multiset of each item (nonincreasing) */
} Tail;
static Tail TT[MAXN];
typedef struct { int maxi; int start, len; cf F[PL], G[PL]; } Item;
static Item *tmpI; static int tmpN, tmpCap; static int *tmpPool, tmpPoolN, tmpPoolCap;
static int tk[MAXN];
static void gen_forest_rec(int r, int depth, int maxidx, int rem, const cf *PF, const cf *PG) {
    if (rem == 0) {
        if (tmpN == tmpCap) { tmpCap = tmpCap ? 2 * tmpCap : 1024; tmpI = realloc(tmpI, sizeof(Item) * tmpCap); }
        if (tmpPoolN + depth > tmpPoolCap) { tmpPoolCap = 2 * tmpPoolCap + depth + 1024; tmpPool = realloc(tmpPool, sizeof(int) * tmpPoolCap); }
        Item *it = &tmpI[tmpN++];
        it->maxi = depth ? tk[0] : -1; it->start = tmpPoolN; it->len = depth;
        for (int i = 0; i < depth; i++) tmpPool[tmpPoolN++] = tk[i];
        memcpy(it->F, PF, sizeof(cf) * PL); memcpy(it->G, PG, sizeof(cf) * PL);
        return;
    }
    if (maxidx < 0) return;
    int smax = rsize[maxidx] < rem ? rsize[maxidx] : rem;
    int dF = deg_of(PF, PL - 1), dG = deg_of(PG, PL - 1);
    for (int s = smax; s >= 1; s--) {
        int lo = first_of_size[s], hi = first_of_size[s + 1] - 1;
        if (hi > maxidx) hi = maxidx;
        for (int j = hi; j >= lo; j--) {
            tk[depth] = j;
            cf NF[PL], NG[PL];
            memset(NF, 0, sizeof NF); memset(NG, 0, sizeof NG);
            polymul(PF, dF, RF[j], rdF[j], NF); polymul(PG, dG, RG[j], rdG[j], NG);
            gen_forest_rec(r, depth + 1, j, rem - s, NF, NG);
        }
    }
}
static int cmp_item(const void *a, const void *b) {
    const Item *x = a, *y = b;
    if (x->maxi != y->maxi) return x->maxi < y->maxi ? -1 : 1;
    return x->start < y->start ? -1 : (x->start > y->start);
}
static void build_tails(int R) {
    for (int r = 0; r <= R; r++) {
        tmpN = 0; tmpPoolN = 0;
        cf one[PL]; memset(one, 0, sizeof one); one[0] = 1;
        gen_forest_rec(r, 0, first_of_size[r + 1 > MAXN ? MAXN : r + 1] - 1, r, one, one);
        qsort(tmpI, tmpN, sizeof(Item), cmp_item);
        Tail *T = &TT[r];
        T->cnt = tmpN; T->pad = (tmpN + VB - 1) / VB * VB;
        T->maxi = malloc(sizeof(int) * T->pad);
        T->FT = aligned_alloc(64, ((sizeof(cf) * (size_t)(r + 1) * T->pad + 63) / 64) * 64);
        T->GT = aligned_alloc(64, ((sizeof(cf) * (size_t)(r + 1) * T->pad + 63) / 64) * 64);
        memset(T->FT, 0, sizeof(cf) * (size_t)(r + 1) * T->pad); memset(T->GT, 0, sizeof(cf) * (size_t)(r + 1) * T->pad);
        T->lstart = malloc(sizeof(int) * T->pad); T->llen = malloc(sizeof(int) * T->pad);
        T->lpool = malloc(sizeof(int) * (tmpPoolN + 1));
        int pp = 0;
        for (int i = 0; i < tmpN; i++) {
            T->maxi[i] = tmpI[i].maxi;
            for (int k = 0; k <= r; k++) { T->FT[(size_t)k * T->pad + i] = tmpI[i].F[k]; T->GT[(size_t)k * T->pad + i] = tmpI[i].G[k]; }
            T->lstart[i] = pp; T->llen[i] = tmpI[i].len;
            for (int q = 0; q < tmpI[i].len; q++) T->lpool[pp++] = tmpPool[tmpI[i].start + q];
        }
        for (int i = tmpN; i < T->pad; i++) { T->maxi[i] = 1 << 30; T->lstart[i] = 0; T->llen[i] = 0; }
    }
}
/* number of items of TT[r] with largest index <= M */
static inline int tail_prefix(int r, int M) {
    const Tail *T = &TT[r]; int lo = 0, hi = T->cnt;
    while (lo < hi) { int mid = (lo + hi) >> 1; if (T->maxi[mid] <= M) lo = mid + 1; else hi = mid; }
    return lo;
}

/* ---------- statistics ---------- */
typedef struct {
    ll trees, nonuni, nonlc, win_lm_bad, eq_win_pos, eq_win_trees, eq_any_trees, eq_consec_trees, flagged;
    double minrel;
    u64 lin;
} Stats;
static void stats_init(Stats *S) { memset(S, 0, sizeof *S); S->minrel = 9.0; }

static void emit_parent(int t, int parent, int *par, int *cnt) {
    int me = (*cnt)++; par[me] = parent;
    for (int i = 0; i < chcnt[t]; i++) emit_parent(chpool[chstart[t] + i], me, par, cnt);
}
static void describe(const int *kids, int nk, int bic, char *buf, size_t bl) {
    int par[MAXN + 4], cnt = 0;
    if (bic) { emit_parent(kids[0], -1, par, &cnt); emit_parent(kids[1], 0, par, &cnt); }
    else { par[cnt++] = -1; for (int i = 0; i < nk; i++) emit_parent(kids[i], 0, par, &cnt); }
    size_t o = 0; o += snprintf(buf + o, bl - o, "parents=");
    for (int i = 0; i < cnt && o < bl; i++) o += snprintf(buf + o, bl - o, "%d%s", par[i], i + 1 < cnt ? "," : "");
}

/* exact analysis (i128) of one flagged tree; identical logic and output format to cwlc_lean.c */
static void full_check(const ll *p, int a, Stats *S, const int *kids, int nk, int bic) {
    /* ULC variant: count trees with some t in [1, a-1] where t p_t^2 <= (t+1) p_{t-1} p_{t+1} */
    int first = -1, eq = 0;
    for (int t = 1; t < a; t++) {
        i128 L = (i128)t * p[t] * p[t], R = (i128)(t + 1) * p[t - 1] * p[t + 1];
        if (L < R && first < 0) first = t;
        if (L == R) eq = 1;
    }
    if (first >= 0) { S->nonlc++; }
    if (eq) S->eq_any_trees++;
    if (first >= 0 || eq) {
        char buf[512]; describe(kids, nk, bic, buf, sizeof buf);
        #pragma omp critical
        {
            printf("ULC first_bad=%d alpha=%d eq=%d %s p=", first, a, eq, buf);
            for (int t = 0; t <= a; t++) printf("%lld%c", p[t], t < a ? ',' : '\n');
            fflush(stdout);
        }
    }
    return;
    int k = 0; while (k < a && p[k] <= p[k + 1]) k++;
    int uni = 1; for (int t = k; t < a; t++) if (p[t] < p[t + 1]) { uni = 0; break; }
    int q = (n + 3) / 4, LM = (2 * a + 1) / 3;
    int first_bad = -1, inLM = 0, eqw = 0, eqany = 0, eqcons = 0, preveq = 0;
    for (int t = 1; t < a; t++) {
        i128 L2 = (i128)p[t] * p[t], R2 = (i128)p[t - 1] * p[t + 1];
        if (L2 == R2) { eqany = 1; if (preveq) eqcons = 1; preveq = 1; if (t >= q && t <= LM) { S->eq_win_pos++; eqw = 1; } }
        else preveq = 0;
        if (L2 < R2) { if (first_bad < 0) first_bad = t; if (t >= q && t <= LM) inLM = 1; }
    }
    S->eq_win_trees += eqw; S->eq_any_trees += eqany; S->eq_consec_trees += eqcons;
    if (!uni) S->nonuni++;
    if (first_bad >= 0) { S->nonlc++; S->win_lm_bad += inLM; double rel = (double)first_bad / a; if (rel < S->minrel) S->minrel = rel; }
    if (first_bad >= 0 || !uni || eqw || eqany) {
        char buf[512]; describe(kids, nk, bic, buf, sizeof buf);
        #pragma omp critical
        {
            printf("EX first_bad=%d alpha=%d inLM=%d unimodal=%d eqwin=%d eqany=%d eqcons=%d %s p=", first_bad, a, inLM, uni, eqw, eqany, eqcons, buf);
            for (int t = 0; t <= a; t++) printf("%lld%c", p[t], t < a ? ',' : '\n');
            fflush(stdout);
        }
    }
}

/* screen a block: acc[t][b], t = 0..D; returns bitmask of lanes to analyse exactly */
static inline unsigned screen_block(cf acc[][VB], int D, int valid, u64 *lin) {
    u64 ls[VB]; for (int b = 0; b < VB; b++) ls[b] = 0;
    for (int t = 0; t <= D; t++) for (int b = 0; b < VB; b++) ls[b] += (u64)acc[t][b] * (u64)(t + 1);
    for (int b = 0; b < valid; b++) *lin += ls[b];
    int fl[VB]; for (int b = 0; b < VB; b++) fl[b] = 0;
    const double eps = 1.0 + 1.0 / 1099511627776.0; /* 1 + 2^-40 */
    for (int t = 1; t < D; t++) {
        for (int b = 0; b < VB; b++) {
            double pm = (double)acc[t - 1][b], pt = (double)acc[t][b], pp = (double)acc[t + 1][b];
            fl[b] |= (pp > 0.0) & ((double)t * pt * pt <= eps * (double)(t + 1) * pm * pp);
        }
    }
    unsigned m = 0; for (int b = 0; b < valid; b++) if (fl[b]) m |= 1u << b;
    return m;
}

/* complete the prefix (PF, PG, kids[0..depth-1]) with the first cnt items of TT[r] */
static void tail_kernel(const cf *PF, int dPF, const cf *PG, int dPG, int r, int cnt, int *kids, int depth, Stats *S) {
    const Tail *T = &TT[r];
    int D = dPF + r; if (dPG + r + 1 > D) D = dPG + r + 1;
    cf acc[PL][VB] __attribute__((aligned(64)));
    S->trees += cnt;
    for (int base = 0; base < cnt; base += VB) {
        for (int t = 0; t <= D; t++) for (int b = 0; b < VB; b++) acc[t][b] = 0;
        for (int i = 0; i <= dPF; i++) {
            cf c = PF[i];
            for (int k = 0; k <= r; k++) {
                const cf *src = T->FT + (size_t)k * T->pad + base;
                for (int b = 0; b < VB; b++) acc[i + k][b] += c * src[b];
            }
        }
        for (int i = 0; i <= dPG; i++) {
            cf c = PG[i];
            for (int k = 0; k <= r; k++) {
                const cf *src = T->GT + (size_t)k * T->pad + base;
                for (int b = 0; b < VB; b++) acc[i + k + 1][b] += c * src[b];
            }
        }
        int valid = cnt - base < VB ? cnt - base : VB;
        unsigned m = screen_block(acc, D, valid, &S->lin);
        while (m) {
            int b = __builtin_ctz(m); m &= m - 1;
            S->flagged++;
            ll p[PL]; int a = 0;
            for (int t = 0; t <= D; t++) { p[t] = acc[t][b]; if (p[t]) a = t; }
            int it = base + b, nk = depth;
            for (int q = 0; q < T->llen[it]; q++) kids[nk++] = T->lpool[T->lstart[it] + q];
            full_check(p, a, S, kids, nk, 0);
        }
    }
}

typedef struct { cf PF[MAXN][PL], PG[MAXN][PL]; int dF[MAXN], dG[MAXN]; int kids[MAXN + 4]; } Work;

static void uni_rec(Work *W, int depth, int maxidx, int rem, Stats *S) {
    if (rem <= RT) {
        int cnt = tail_prefix(rem, maxidx);
        if (cnt) tail_kernel(W->PF[depth], W->dF[depth], W->PG[depth], W->dG[depth], rem, cnt, W->kids, depth, S);
        return;
    }
    int smax = rsize[maxidx] < rem ? rsize[maxidx] : rem;
    for (int s = smax; s >= 1; s--) {
        int lo = first_of_size[s], hi = first_of_size[s + 1] - 1;
        if (hi > maxidx) hi = maxidx;
        for (int j = hi; j >= lo; j--) {
            W->kids[depth] = j;
            polymul(W->PF[depth], W->dF[depth], RF[j], rdF[j], W->PF[depth + 1]);
            polymul(W->PG[depth], W->dG[depth], RG[j], rdG[j], W->PG[depth + 1]);
            W->dF[depth + 1] = W->dF[depth] + rdF[j]; W->dG[depth + 1] = W->dG[depth] + rdG[j];
            uni_rec(W, depth + 1, j, rem - s, S);
        }
    }
}

static void merge(Stats *T, const Stats *S) {
    T->trees += S->trees; T->nonuni += S->nonuni; T->nonlc += S->nonlc; T->win_lm_bad += S->win_lm_bad;
    T->eq_win_pos += S->eq_win_pos; T->eq_win_trees += S->eq_win_trees; T->eq_any_trees += S->eq_any_trees; T->eq_consec_trees += S->eq_consec_trees;
    T->flagged += S->flagged; T->lin += S->lin;
    if (S->minrel < T->minrel) T->minrel = S->minrel;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: cwlc_vec n [threads] [R]\n"); return 2; }
    n = atoi(argv[1]);
    if (n < 4 || n > 35) { fprintf(stderr, "n out of range (4..35)\n"); return 2; }
    if (argc > 2) omp_set_num_threads(atoi(argv[2]));
    if (argc > 3) RT = atoi(argv[3]);
    int half = n / 2, lim = (n - 1) / 2;
    if (RT > lim) RT = lim;
    if (RT < 0) RT = 0;
    double tb = omp_get_wtime();
    build_rooted(half);
    printf("ROOTED");
    for (int s = 1; s <= half; s++) printf(" %d:%d", s, first_of_size[s + 1] - first_of_size[s]);
    printf("\n");
    build_tails(RT);
    printf("TAILS R=%d", RT);
    for (int r = 0; r <= RT; r++) printf(" %d:%d", r, TT[r].cnt);
    printf(" build_seconds=%.1f\n", omp_get_wtime() - tb); fflush(stdout);
    Stats G; stats_init(&G);
    int nfirst = first_of_size[lim + 1];
    double t0 = omp_get_wtime();
    #pragma omp parallel
    {
        Stats S; stats_init(&S);
        Work *W = aligned_alloc(64, ((sizeof(Work) + 63) / 64) * 64);
        #pragma omp for schedule(dynamic, 1) nowait
        for (int i = nfirst - 1; i >= 0; i--) {
            int s = rsize[i];
            memset(W->PF[0], 0, sizeof W->PF[0]); memset(W->PG[0], 0, sizeof W->PG[0]);
            W->PF[0][0] = 1; W->PG[0][0] = 1; W->dF[0] = 0; W->dG[0] = 0;
            W->kids[0] = i;
            polymul(W->PF[0], 0, RF[i], rdF[i], W->PF[1]); polymul(W->PG[0], 0, RG[i], rdG[i], W->PG[1]);
            W->dF[1] = rdF[i]; W->dG[1] = rdG[i];
            uni_rec(W, 1, i, n - 1 - s, &S);
        }
        if (n % 2 == 0) {
            int lo = first_of_size[half], hi = first_of_size[half + 1];
            #pragma omp for schedule(dynamic, 16) nowait
            for (int i = lo; i < hi; i++) {
                cf f1g1[PL], A[PL], B[PL]; ll p[PL]; int kids[2];
                int d1 = rdF[i];
                for (int t = 0; t < PL; t++) f1g1[t] = RF[i][t] - RG[i][t];
                int e1 = deg_of(f1g1, half);
                for (int j = i; j < hi; j++) {
                    cf f2g2[PL]; for (int t = 0; t < PL; t++) f2g2[t] = RF[j][t] - RG[j][t];
                    int d2 = rdF[j], e2 = deg_of(f2g2, half);
                    polymul(RF[i], d1, RF[j], d2, A);
                    polymul(f1g1, e1, f2g2, e2, B);
                    int d = d1 + d2;
                    S.trees++;
                    u64 cs = 0; int a = 0;
                    for (int t = 0; t <= d; t++) { cf v = A[t] - (t <= e1 + e2 ? B[t] : 0); p[t] = v; cs += (u64)v * (u64)(t + 1); if (v) a = t; }
                    S.lin += cs;
                    int flag = 0;
                    for (int t = 1; t < a; t++) { i128 L = (i128)t * p[t] * p[t], R = (i128)(t + 1) * p[t - 1] * p[t + 1]; flag |= (L <= R); }
                    if (flag) { S.flagged++; kids[0] = i; kids[1] = j; full_check(p, a, &S, kids, 2, 1); }
                }
            }
        }
        #pragma omp critical
        merge(&G, &S);
        free(W);
    }
    double t1 = omp_get_wtime();
    u64 checksum = G.lin * 0x9E3779B97F4A7C15ULL;
    printf("FLAGGED %lld\n", G.flagged);
    printf("EQ window_positions=%lld window_trees=%lld interior_equality_trees=%lld consecutive_interior_equality_trees=%lld\n",
           G.eq_win_pos, G.eq_win_trees, G.eq_any_trees, G.eq_consec_trees);
    printf("RESULT n=%d trees=%lld nonunimodal=%lld nonLC=%lld nonLC_in_window_LM=%lld nonLC_in_window_beta=%lld minrel=%.6f checksum=%llu seconds=%.1f threads=%d\n",
           n, G.trees, G.nonuni, G.nonlc, G.win_lm_bad, 0LL, G.minrel, (unsigned long long)checksum, t1 - t0, omp_get_max_threads());
    return 0;
}
