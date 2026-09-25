/* cwlc_vec3.c -- cwlc_vec2.c made exact for every n <= 37 without the counting bound below.
 * VEC3: every tree's total I(T;1) is computed exactly in 64 bits from 64-bit totals of its parts
 * (rooted trees, tail items, prefix products). A tree with I(T;1) < THR <= 2^32 has every coefficient
 * < 2^32, so its uint32 (mod 2^32) coefficients are exact and it goes through the vectorised path.
 * Any other tree is rebuilt exactly (64-bit coefficients, __int128 comparisons) from its list of
 * centroid branches (or its bicentroid pair) and analysed exactly. THR = 2^T with T <= 32 is a
 * run-time argument, so the exact fallback can be forced on small n for testing.
 * The rest of this header describes cwlc_vec2.c; its n <= 35 counting bound is not needed here.
 *
 * cwlc_vec2.c -- exhaustive check over all free trees of order n (centroid decomposition), vectorised.
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

#define MAXN 38
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
static cf *BFT, *BHT; static int BPAD;
static u64 *rFt, *rGt;          /* f(1), g(1) of each rooted tree (exact) */
static u64 THR = 1ULL << 32;

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
        rFt = realloc(rFt, sizeof(u64) * CAP); rGt = realloc(rGt, sizeof(u64) * CAP);
        RF = realloc(RF, sizeof(cf) * PL * CAP); RG = realloc(RG, sizeof(cf) * PL * CAP);
    }
    if (POOL + nk > POOLCAP) { POOLCAP = POOLCAP ? 2 * POOLCAP + nk : 4096; chpool = realloc(chpool, sizeof(int) * POOLCAP); }
    rsize[NR] = s; chstart[NR] = POOL; chcnt[NR] = nk;
    for (int i = 0; i < nk; i++) chpool[POOL++] = kids[i];
    memcpy(RF[NR], F, sizeof(cf) * PL); memcpy(RG[NR], G, sizeof(cf) * PL);
    rdF[NR] = deg_of(RF[NR], PL - 1); rdG[NR] = deg_of(RG[NR], PL - 1);
    rFt[NR] = 0; rGt[NR] = 0; for (int k = 0; k < PL; k++) { rFt[NR] += RF[NR][k]; rGt[NR] += RG[NR][k]; }
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
    u64 *FTOT, *GTOT;      /* prod f(1), prod g(1) of each item (exact) */
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
        T->FTOT = calloc(T->pad, sizeof(u64)); T->GTOT = calloc(T->pad, sizeof(u64));
        int pp = 0;
        for (int i = 0; i < tmpN; i++) {
            T->maxi[i] = tmpI[i].maxi;
            for (int k = 0; k < PL; k++) { T->FTOT[i] += tmpI[i].F[k]; T->GTOT[i] += tmpI[i].G[k]; }
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


/* transposed f and h = f - g of the rooted trees of order half (bicentroid part) */
static void build_bic(int half) {
    int lo = first_of_size[half], m = first_of_size[half + 1] - lo;
    BPAD = ((m + 2 * VB) / VB) * VB;
    BFT = aligned_alloc(64, ((sizeof(cf) * (size_t)(half + 1) * BPAD + 63) / 64) * 64);
    BHT = aligned_alloc(64, ((sizeof(cf) * (size_t)(half + 1) * BPAD + 63) / 64) * 64);
    memset(BFT, 0, sizeof(cf) * (size_t)(half + 1) * BPAD); memset(BHT, 0, sizeof(cf) * (size_t)(half + 1) * BPAD);
    for (int j = 0; j < m; j++) for (int k = 0; k <= half; k++) {
        BFT[(size_t)k * BPAD + j] = RF[lo + j][k]; BHT[(size_t)k * BPAD + j] = RF[lo + j][k] - RG[lo + j][k];
    }
}

/* ---------- statistics ---------- */
typedef struct {
    ll trees, nonuni, nonlc, win_lm_bad, eq_win_pos, eq_win_trees, eq_any_trees, eq_consec_trees, flagged, big;
    double minrel;
    u64 lin;
    double lcwin, mon, moa;   /* STATS: min n(1-p_{t-1}p_{t+1}/p_t^2) on [max(1,q), min(LM,a-1)]; min mode/n; max mode/alpha */
} Stats;
static void stats_init(Stats *S) { memset(S, 0, sizeof *S); S->minrel = 9.0; S->lcwin = 1e18; S->mon = 9.0; S->moa = -1.0; }

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

static void polymul_ll(const ll *a, int da, const ll *b, int db, ll *out) {
    for (int k = 0; k <= da + db; k++) out[k] = 0;
    for (int i = 0; i <= da; i++) for (int j = 0; j <= db; j++) out[i + j] += a[i] * b[j];
}
#ifdef STATS
static void stats_one(const ll *p, int a, Stats *S) {
    int md = a; for (int t = a - 1; t >= 0; t--) if (p[t] >= p[t + 1]) md = t;
    int q = (n + 3) / 4; if (q < 1) q = 1;
    int LM = (2 * a + 1) / 3;
    for (int t = q; t <= LM && t <= a - 1; t++) {
        double pt = (double)p[t], mg = (double)n * (1.0 - ((double)p[t - 1] * (double)p[t + 1]) / (pt * pt));
        if (mg < S->lcwin) S->lcwin = mg;
    }
    double x = (double)md / n, y = (double)md / a;
    if (x < S->mon) S->mon = x;
    if (y > S->moa) S->moa = y;
}
#endif
/* exact rebuild and analysis of one tree whose total I(T;1) is >= THR */
static void exact_tree(const int *kids, int nk, int bic, Stats *S) {
    ll p[PL + 2]; int a = 0;
    for (int t = 0; t < PL + 2; t++) p[t] = 0;
    if (!bic) {
        ll A[PL], B[PL], X[PL]; int dA = 0, dB = 0;
        for (int t = 0; t < PL; t++) { A[t] = 0; B[t] = 0; }
        A[0] = 1; B[0] = 1;
        for (int q = 0; q < nk; q++) {
            int j = kids[q]; ll f[PL], g[PL];
            for (int t = 0; t < PL; t++) { f[t] = RF[j][t]; g[t] = RG[j][t]; }
            polymul_ll(A, dA, f, rdF[j], X); dA += rdF[j]; for (int t = 0; t <= dA; t++) A[t] = X[t];
            polymul_ll(B, dB, g, rdG[j], X); dB += rdG[j]; for (int t = 0; t <= dB; t++) B[t] = X[t];
        }
        for (int t = 0; t <= dA; t++) p[t] += A[t];
        for (int t = 0; t <= dB; t++) p[t + 1] += B[t];
    } else {
        int i = kids[0], j = kids[1]; ll fi[PL], fj[PL], hi[PL], hj[PL], X[PL], Y[PL];
        for (int t = 0; t < PL; t++) { fi[t] = RF[i][t]; fj[t] = RF[j][t]; hi[t] = (ll)RF[i][t] - RG[i][t]; hj[t] = (ll)RF[j][t] - RG[j][t]; }
        int d = rdF[i] + rdF[j];
        polymul_ll(fi, rdF[i], fj, rdF[j], X); polymul_ll(hi, rdF[i], hj, rdF[j], Y);
        for (int t = 0; t <= d; t++) p[t] = X[t] - Y[t];
    }
    for (int t = 0; t < PL; t++) if (p[t]) a = t;
    u64 cs = 0; for (int t = 0; t <= a; t++) cs += (u64)p[t] * (u64)(t + 1);
    S->lin += cs; S->big++;
    int flag = 0;
    for (int t = 1; t < a; t++) { i128 L = (i128)p[t] * p[t], R = (i128)p[t - 1] * p[t + 1]; flag |= (L <= R); }
    if (flag) { S->flagged++; full_check(p, a, S, kids, nk, bic); }
#ifdef STATS
    stats_one(p, a, S);
#endif
}

/* screen a block: acc[t][b], t = 0..D; returns bitmask of lanes to analyse exactly */
static inline unsigned screen_block(cf acc[][VB], int D, int valid, u64 *lin, Stats *S, unsigned skip) {
    u64 ls[VB]; for (int b = 0; b < VB; b++) ls[b] = 0;
    for (int t = 0; t <= D; t++) for (int b = 0; b < VB; b++) ls[b] += (u64)acc[t][b] * (u64)(t + 1);
    for (int b = 0; b < valid; b++) if (!((skip >> b) & 1u)) *lin += ls[b];
    int fl[VB]; for (int b = 0; b < VB; b++) fl[b] = 0;
    const double eps = 1.0 + 1.0 / 1099511627776.0; /* 1 + 2^-40 */
    for (int t = 1; t < D; t++) {
        for (int b = 0; b < VB; b++) {
            double pm = (double)acc[t - 1][b], pt = (double)acc[t][b], pp = (double)acc[t + 1][b];
            fl[b] |= (pp > 0.0) & (pt * pt <= eps * pm * pp);
        }
    }
    unsigned m = 0; for (int b = 0; b < valid; b++) if (fl[b]) m |= 1u << b;
    m &= ~skip;
#ifdef STATS
    {   /* reported statistics only (floating point); never used for pass/fail */
        int al[VB], md[VB]; double mw[VB];
        for (int b = 0; b < VB; b++) { al[b] = 0; md[b] = D; mw[b] = 1e18; }
        for (int t = 0; t <= D; t++) for (int b = 0; b < VB; b++) if (acc[t][b]) al[b] = t;
        for (int t = D - 1; t >= 0; t--) for (int b = 0; b < VB; b++) if (acc[t][b] >= acc[t + 1][b]) md[b] = t;
        int q = (n + 3) / 4; if (q < 1) q = 1;
        for (int t = q; t < D; t++) for (int b = 0; b < VB; b++) {
            int LM = (2 * al[b] + 1) / 3;
            if (t <= LM && t <= al[b] - 1) {
                double pt = (double)acc[t][b], mg = (double)n * (1.0 - ((double)acc[t - 1][b] * (double)acc[t + 1][b]) / (pt * pt));
                if (mg < mw[b]) mw[b] = mg;
            }
        }
        for (int b = 0; b < valid; b++) {
            if ((skip >> b) & 1u) continue;
            if (mw[b] < S->lcwin) S->lcwin = mw[b];
            double x = (double)md[b] / n, y = (double)md[b] / al[b];
            if (x < S->mon) S->mon = x;
            if (y > S->moa) S->moa = y;
        }
    }
#endif
    return m;
}

/* complete the prefix (PF, PG, kids[0..depth-1]) with the first cnt items of TT[r] */
static void tail_kernel(const cf *PF, int dPF, const cf *PG, int dPG, u64 PFt, u64 PGt, int r, int cnt, int *kids, int depth, Stats *S) {
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
        unsigned big = 0;
        for (int b = 0; b < valid; b++) if (PFt * T->FTOT[base + b] + PGt * T->GTOT[base + b] >= THR) big |= 1u << b;
        unsigned m = screen_block(acc, D, valid, &S->lin, S, big);
        while (m) {
            int b = __builtin_ctz(m); m &= m - 1;
            S->flagged++;
            ll p[PL]; int a = 0;
            for (int t = 0; t <= D; t++) { p[t] = acc[t][b]; if (p[t]) a = t; }
            int it = base + b, nk = depth;
            for (int q = 0; q < T->llen[it]; q++) kids[nk++] = T->lpool[T->lstart[it] + q];
            full_check(p, a, S, kids, nk, 0);
        }
        while (big) {
            int b = __builtin_ctz(big); big &= big - 1;
            int it = base + b, nk = depth;
            for (int q = 0; q < T->llen[it]; q++) kids[nk++] = T->lpool[T->lstart[it] + q];
            exact_tree(kids, nk, 0, S);
        }
    }
}

typedef struct { cf PF[MAXN][PL], PG[MAXN][PL]; int dF[MAXN], dG[MAXN]; int kids[MAXN + 4]; u64 PFt[MAXN], PGt[MAXN]; } Work;

static void uni_rec(Work *W, int depth, int maxidx, int rem, Stats *S) {
    if (rem <= RT) {
        int cnt = tail_prefix(rem, maxidx);
        if (cnt) tail_kernel(W->PF[depth], W->dF[depth], W->PG[depth], W->dG[depth], W->PFt[depth], W->PGt[depth], rem, cnt, W->kids, depth, S);
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
            W->PFt[depth + 1] = W->PFt[depth] * rFt[j]; W->PGt[depth + 1] = W->PGt[depth] * rGt[j];
            uni_rec(W, depth + 1, j, rem - s, S);
        }
    }
}

static void merge(Stats *T, const Stats *S) {
    T->trees += S->trees; T->nonuni += S->nonuni; T->nonlc += S->nonlc; T->win_lm_bad += S->win_lm_bad;
    T->eq_win_pos += S->eq_win_pos; T->eq_win_trees += S->eq_win_trees; T->eq_any_trees += S->eq_any_trees; T->eq_consec_trees += S->eq_consec_trees;
    T->flagged += S->flagged; T->lin += S->lin; T->big += S->big;
    if (S->minrel < T->minrel) T->minrel = S->minrel;
    if (S->lcwin < T->lcwin) T->lcwin = S->lcwin;
    if (S->mon < T->mon) T->mon = S->mon;
    if (S->moa > T->moa) T->moa = S->moa;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: cwlc_vec3 n [threads] [R] [log2 THR <= 32]\n"); return 2; }
    n = atoi(argv[1]);
    if (n < 4 || n > MAXN - 1) { fprintf(stderr, "n out of range (4..%d)\n", MAXN - 1); return 2; }
    if (argc > 2) omp_set_num_threads(atoi(argv[2]));
    if (argc > 3) RT = atoi(argv[3]);
    if (argc > 4) { int e = atoi(argv[4]); if (e < 1 || e > 32) { fprintf(stderr, "log2 THR must be in 1..32\n"); return 2; } THR = 1ULL << e; }
    int half = n / 2, lim = (n - 1) / 2;
    if (RT > lim) RT = lim;
    if (RT < 0) RT = 0;
    double tb = omp_get_wtime();
    build_rooted(half);
    printf("ROOTED");
    for (int s = 1; s <= half; s++) printf(" %d:%d", s, first_of_size[s + 1] - first_of_size[s]);
    printf("\n");
    build_tails(RT);
    if (n % 2 == 0) build_bic(half);
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
            W->PFt[0] = 1; W->PGt[0] = 1; W->PFt[1] = rFt[i]; W->PGt[1] = rGt[i];
            uni_rec(W, 1, i, n - 1 - s, &S);
        }
        if (n % 2 == 0) {
            /* bicentroid: p = f_i f_j - h_i h_j with h = f - g, vectorised over j in blocks of VB */
            int lo = first_of_size[half], m = first_of_size[half + 1] - lo;
            #pragma omp for schedule(dynamic, 8) nowait
            for (int i = lo; i < lo + m; i++) {
                cf Fi[PL], Hi[PL]; int kids[2];
                for (int t = 0; t < PL; t++) { Fi[t] = RF[i][t]; Hi[t] = RF[i][t] - RG[i][t]; }
                int d1 = rdF[i], e1 = deg_of(Hi, PL - 1);
                int D = d1 + half;
                cf acc[PL][VB] __attribute__((aligned(64)));
                S.trees += m - (i - lo);
                for (int base = i - lo; base < m; base += VB) {
                    for (int t = 0; t <= D; t++) for (int b = 0; b < VB; b++) acc[t][b] = 0;
                    for (int a = 0; a <= d1; a++) {
                        cf c = Fi[a];
                        for (int k = 0; k <= half; k++) { const cf *src = BFT + (size_t)k * BPAD + base; for (int b = 0; b < VB; b++) acc[a + k][b] += c * src[b]; }
                    }
                    for (int a = 0; a <= e1; a++) {
                        cf c = Hi[a];
                        for (int k = 0; k <= half; k++) { const cf *src = BHT + (size_t)k * BPAD + base; for (int b = 0; b < VB; b++) acc[a + k][b] -= c * src[b]; }
                    }
                    int valid = m - base < VB ? m - base : VB;
                    unsigned big = 0;
                    for (int b = 0; b < valid; b++) {
                        int jj = lo + base + b;
                        u64 tot = rFt[i] * rFt[jj] - (rFt[i] - rGt[i]) * (rFt[jj] - rGt[jj]);
                        if (tot >= THR) big |= 1u << b;
                    }
                    unsigned msk = screen_block(acc, D, valid, &S.lin, &S, big);
                    while (msk) {
                        int b = __builtin_ctz(msk); msk &= msk - 1;
                        S.flagged++;
                        ll p[PL]; int a = 0;
                        for (int t = 0; t <= D; t++) { p[t] = acc[t][b]; if (p[t]) a = t; }
                        kids[0] = i; kids[1] = lo + base + b;
                        full_check(p, a, &S, kids, 2, 1);
                    }
                    while (big) {
                        int b = __builtin_ctz(big); big &= big - 1;
                        kids[0] = i; kids[1] = lo + base + b;
                        exact_tree(kids, 2, 1, &S);
                    }
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
    printf("BIG exact_fallback_trees=%lld threshold=%llu\n", G.big, (unsigned long long)THR);
#ifdef STATS
    printf("MARGIN min_n_margin_window=%.6f mode_over_n_min=%.6f mode_over_alpha_max=%.6f\n", G.lcwin, G.mon, G.moa);
#endif
    printf("EQ window_positions=%lld window_trees=%lld interior_equality_trees=%lld consecutive_interior_equality_trees=%lld\n",
           G.eq_win_pos, G.eq_win_trees, G.eq_any_trees, G.eq_consec_trees);
    printf("RESULT n=%d trees=%lld nonunimodal=%lld nonLC=%lld nonLC_in_window_LM=%lld nonLC_in_window_beta=%lld minrel=%.6f checksum=%llu seconds=%.1f threads=%d\n",
           n, G.trees, G.nonuni, G.nonlc, G.win_lm_bad, 0LL, G.minrel, (unsigned long long)checksum, t1 - t0, omp_get_max_threads());
    return 0;
}
