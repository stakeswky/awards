/* stepf.c -- FOREST variant of stepc.c: enumerates trees T of order N = n+1 and all vertices r, and checks the
 * forest F = T - r (order n = N-1); every forest of order n arises this way. Edgeless F (T a star centred at r) is
 * skipped (Q_c for nK1 is proved directly). Usage: stepf N CN CD NW.
 * Based on stepc.c -- second (C) implementation of the c/n vertex-splitting scheme of quant_scheme_lm.py.
 * For every free tree of order n (WROM generator, same code as wlc.c / wlc3.c) with c = CN/CD:
 *   Q_c : CD*n*(p_k^2 - p_{k-1}p_{k+1}) >= CN*p_k^2 for every k in [1, min(top, alpha-1)], top = (2alpha+1)/3.
 *   STEP: for every such k some vertex v satisfies  LB_A(k) + LB_C(k-1) - X_k(v) >= (c/n) p_k^2, where
 *         A = I(T-v) (order n-1), C = I(T-N[v]) (order n-1-deg v), X_k = a_{k-1}c_k + a_{k+1}c_{k-2} - 2a_k c_{k-1},
 *         LB_P(i) = P_0^2 (i<=0), 0 (i>alpha_P), P_i^2 (i=alpha_P), else max of
 *                   (c/n_P) P_i^2 [if i <= top(alpha_P)]  and  P_i^2 - P_{i-1}P_i [if i >= top(alpha_P)].
 * All comparisons are exact (__int128, common denominator D = CD*n*nA*max(nC,1)).
 * Usage: stepc n CN CD NW      Output: failing examples + RESULT line (checksum identical to wlc.c). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

#define MAXN 34
#define BATCH 4096
#define NBUF 64
typedef long long ll;
typedef __int128 i128;

static int n; static ll CN, CD; static int NESTED = 0; /* 1: only nested witnesses, IH-only bounds */

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

/* independence polynomial of the forest T - {removed}; par[] from level sequence (par[v] < v). Returns degree. */
static int forest_poly(const int *par, const unsigned char *rem, ll *out) {
    ll A[MAXN][MAXN + 1], B[MAXN][MAXN + 1], T[MAXN + 1], S[MAXN + 1];
    int dA[MAXN], dB[MAXN];
    for (int v = 0; v < n; v++) {
        A[v][0] = 1; dA[v] = 0;
        if (rem[v]) dB[v] = -1; else { B[v][0] = 0; B[v][1] = 1; dB[v] = 1; }
    }
    for (int v = n - 1; v >= 1; v--) {
        int u = par[v];
        int dS = dA[v] > dB[v] ? dA[v] : dB[v];
        for (int k = 0; k <= dS; k++) S[k] = (k <= dA[v] ? A[v][k] : 0) + (k <= dB[v] ? B[v][k] : 0);
        int d0 = dA[u];
        memset(T, 0, sizeof(ll) * (d0 + dS + 1));
        for (int i = 0; i <= d0; i++) if (A[u][i]) for (int k = 0; k <= dS; k++) T[i + k] += A[u][i] * S[k];
        dA[u] = d0 + dS; memcpy(A[u], T, sizeof(ll) * (dA[u] + 1));
        if (dB[u] >= 0) {
            int d1 = dB[u], dv = dA[v];
            memset(T, 0, sizeof(ll) * (d1 + dv + 1));
            for (int i = 0; i <= d1; i++) if (B[u][i]) for (int k = 0; k <= dv; k++) T[i + k] += B[u][i] * A[v][k];
            dB[u] = d1 + dv; memcpy(B[u], T, sizeof(ll) * (dB[u] + 1));
        }
    }
    int d = dA[0] > dB[0] ? dA[0] : dB[0];
    for (int k = 0; k <= d; k++) out[k] = (k <= dA[0] ? A[0][k] : 0) + (k <= dB[0] ? B[0][k] : 0);
    while (d > 0 && out[d] == 0) d--;
    return d;
}

static inline ll gg(const ll *P, int aP, int i) { return (i >= 0 && i <= aP) ? P[i] : 0; }

/* LB_P(i) scaled by D; nP = order of the piece; D divisible by CD*nP whenever the IH branch is used */
static i128 LBs(const ll *P, int aP, int i, ll nP, i128 D) {
    if (i <= 0) return D * (i128)P[0] * P[0];
    if (i > aP) return 0;
    if (i == aP) return D * (i128)P[i] * P[i];
    int t = (2 * aP + 1) / 3, have = 0; i128 best = 0;
    if (i <= t) { best = (D / (CD * nP)) * (i128)CN * ((i128)P[i] * P[i]); have = 1; }
    if (i >= t && !(NESTED && have)) { i128 lm = D * ((i128)P[i] * P[i] - (i128)P[i - 1] * P[i]); if (!have || lm > best) best = lm; }
    if (NESTED && !have) { fprintf(stderr, "nested mode reached a gap-zone index\n"); exit(3); }
    return best;
}

typedef struct { int count; unsigned char seq[BATCH][MAXN]; } batch_t;
static batch_t *bufs;
static int full_q[NBUF], free_q[NBUF];
static int full_head = 0, full_tail = 0, full_cnt = 0, free_head = 0, free_tail = 0, free_cnt = 0, done = 0;
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t cv_full = PTHREAD_COND_INITIALIZER, cv_free = PTHREAD_COND_INITIALIZER;

typedef struct {
    ll trees, qfail, stepfail, vtried, unique; unsigned long long checksum; double minmargin;
    char ex[16][300]; int nex;
} stats_t;

static void *producer(void *arg) {
    (void)arg;
    int L[MAXN]; int k0 = 0;
    for (int i = 0; i <= n / 2; i++) L[k0++] = i;
    for (int i = 1; i < (n + 1) / 2; i++) L[k0++] = i;
    int more = 1;
    while (more) {
        pthread_mutex_lock(&mu);
        while (free_cnt == 0) pthread_cond_wait(&cv_free, &mu);
        int b = free_q[free_head]; free_head = (free_head + 1) % NBUF; free_cnt--;
        pthread_mutex_unlock(&mu);
        batch_t *bt = &bufs[b]; bt->count = 0;
        while (bt->count < BATCH) {
            next_tree(L);
            for (int i = 0; i < n; i++) bt->seq[bt->count][i] = (unsigned char)L[i];
            bt->count++;
            if (!next_rooted_tree(L, -1)) { more = 0; break; }
        }
        pthread_mutex_lock(&mu);
        full_q[full_tail] = b; full_tail = (full_tail + 1) % NBUF; full_cnt++;
        pthread_cond_signal(&cv_full);
        pthread_mutex_unlock(&mu);
    }
    pthread_mutex_lock(&mu); done = 1; pthread_cond_broadcast(&cv_full); pthread_mutex_unlock(&mu);
    return NULL;
}


static void check_forest(const int *par, const int *degT, const unsigned long long *nbm, int r, stats_t *st, const unsigned char *L) {
    int N = n;               /* tree order */
    int nf = N - 1;          /* forest order */
    if (degT[r] == N - 1) return;          /* F = T - r edgeless: handled directly */
    unsigned char rem[MAXN]; memset(rem, 0, sizeof rem); rem[r] = 1;
    ll p[MAXN + 2];
    int a = forest_poly(par, rem, p);
    st->trees++;
    for (int k = 0; k <= a; k++) st->checksum += (unsigned long long)p[k] * (unsigned long long)(k + 1) * 0x9E3779B97F4A7C15ULL;
    int top = (2 * a + 1) / 3, kmax = top < a - 1 ? top : a - 1;
    if (kmax < 1) return;
    int qok = 1;
    for (int k = 1; k <= kmax; k++) {
        i128 s = (i128)p[k] * p[k] - (i128)p[k - 1] * p[k + 1];
        if ((i128)CD * nf * s < (i128)CN * ((i128)p[k] * p[k])) qok = 0;
        double m = (double)nf * (double)s / ((double)p[k] * (double)p[k]);
        if (m < st->minmargin) st->minmargin = m;
    }
    if (!qok) st->qfail++;
    unsigned int unresolved = 0; int nested_seen = 0;
    for (int k = 1; k <= kmax; k++) unresolved |= 1u << k;
    ll Ap[MAXN + 2], Cp[MAXN + 2];
    for (int v = 0; v < N && unresolved; v++) {
        if (v == r) continue;
        st->vtried++;
        memset(rem, 0, sizeof rem); rem[r] = 1; rem[v] = 1;
        int aA = forest_poly(par, rem, Ap);
        for (int w = 0; w < N; w++) rem[w] = ((nbm[v] >> w) & 1) | (w == r);
        int degF = degT[v] - (int)((nbm[v] >> r) & 1);
        ll nA = nf - 1, nC = nf - 1 - degF;
        int aC;
        if (nC == 0) { Cp[0] = 1; aC = 0; } else aC = forest_poly(par, rem, Cp);
        if (NESTED && !(aA == a && aC == a - 1)) continue;
        nested_seen = 1;
        ll nCm = nC > 0 ? nC : 1, nAm = nA > 0 ? nA : 1;
        i128 D = (i128)CD * nf * nAm * nCm;
        for (int k = 1; k <= kmax; k++) {
            if (!((unresolved >> k) & 1)) continue;
            i128 X = (i128)gg(Ap, aA, k - 1) * gg(Cp, aC, k) + (i128)gg(Ap, aA, k + 1) * gg(Cp, aC, k - 2)
                   - 2 * (i128)gg(Ap, aA, k) * gg(Cp, aC, k - 1);
            i128 lhs = LBs(Ap, aA, k, nAm, D) + LBs(Cp, aC, k - 1, nCm, D) - D * X;
            i128 need = (i128)CN * nAm * nCm * ((i128)p[k] * p[k]);
            if (lhs >= need) unresolved &= ~(1u << k);
        }
    }
    if (NESTED && !nested_seen) { st->unique++; return; }
    if (unresolved) {
        st->stepfail++;
        if (st->nex < 16) {
            int off = snprintf(st->ex[st->nex], 300, "STEPFAIL forest=T-r r=%d alpha=%d top=%d k:", r, a, top);
            for (int k = 1; k <= kmax; k++) if ((unresolved >> k) & 1) off += snprintf(st->ex[st->nex] + off, 300 - off, " %d", k);
            off += snprintf(st->ex[st->nex] + off, 300 - off, " T_levels=");
            for (int i = 0; i < N && off < 290; i++) off += snprintf(st->ex[st->nex] + off, 300 - off, "%d%c", L[i], i + 1 < N ? ',' : ' ');
            st->nex++;
        }
    }
}

static void check_tree(const unsigned char *L, stats_t *st) {
    int par[MAXN], stackv[MAXN], sp = 0, deg[MAXN];
    unsigned long long nbm[MAXN];
    for (int i = 0; i < n; i++) {
        while (sp && L[stackv[sp - 1]] >= L[i]) sp--;
        par[i] = sp ? stackv[sp - 1] : -1;
        stackv[sp++] = i;
    }
    for (int v = 0; v < n; v++) { deg[v] = 0; nbm[v] = 1ULL << v; }
    for (int v = 1; v < n; v++) { deg[v]++; deg[par[v]]++; nbm[v] |= 1ULL << par[v]; nbm[par[v]] |= 1ULL << v; }
    for (int r = 0; r < n; r++) check_forest(par, deg, nbm, r, st, L);
}

static void *worker(void *arg) {
    stats_t *st = (stats_t *)arg;
    for (;;) {
        pthread_mutex_lock(&mu);
        while (full_cnt == 0 && !done) pthread_cond_wait(&cv_full, &mu);
        if (full_cnt == 0 && done) { pthread_mutex_unlock(&mu); break; }
        int b = full_q[full_head]; full_head = (full_head + 1) % NBUF; full_cnt--;
        pthread_mutex_unlock(&mu);
        batch_t *bt = &bufs[b];
        for (int t = 0; t < bt->count; t++) check_tree(bt->seq[t], st);
        pthread_mutex_lock(&mu);
        free_q[free_tail] = b; free_tail = (free_tail + 1) % NBUF; free_cnt++;
        pthread_cond_signal(&cv_free);
        pthread_mutex_unlock(&mu);
    }
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: stepf N CN CD NW\n"); return 2; }
    n = atoi(argv[1]); CN = atoll(argv[2]); CD = atoll(argv[3]); int NW = atoi(argv[4]); if (argc > 5 && !strcmp(argv[5], "nested")) NESTED = 1;
    if (n < 4 || n > 32 || CN < 1 || CD < 1 || NW < 1 || NW > 64) { fprintf(stderr, "bad args\n"); return 2; }
    bufs = (batch_t *)malloc(sizeof(batch_t) * NBUF);
    for (int i = 0; i < NBUF; i++) free_q[i] = i;
    free_cnt = NBUF; free_tail = 0;
    stats_t *st = (stats_t *)calloc(NW, sizeof(stats_t));
    for (int w = 0; w < NW; w++) st[w].minmargin = 1e18;
    pthread_t prod, *wk = (pthread_t *)malloc(sizeof(pthread_t) * NW);
    pthread_create(&prod, NULL, producer, NULL);
    for (int w = 0; w < NW; w++) pthread_create(&wk[w], NULL, worker, &st[w]);
    pthread_join(prod, NULL);
    for (int w = 0; w < NW; w++) pthread_join(wk[w], NULL);
    stats_t tot; memset(&tot, 0, sizeof tot); tot.minmargin = 1e18;
    for (int w = 0; w < NW; w++) {
        tot.trees += st[w].trees; tot.qfail += st[w].qfail; tot.stepfail += st[w].stepfail; tot.vtried += st[w].vtried; tot.unique += st[w].unique;
        tot.checksum += st[w].checksum;
        if (st[w].minmargin < tot.minmargin) tot.minmargin = st[w].minmargin;
        for (int e = 0; e < st[w].nex; e++) printf("%s\n", st[w].ex[e]);
    }
    printf("RESULT forests_of_order=%d (from trees N=%d, edgeless skipped) c=%lld/%lld forest_instances=%lld Qc_fail=%lld STEP_fail=%lld avg_v_tried=%.3f min_n_margin_on_1_top=%.6f nested_mode=%d uniqueMIS=%lld checksum=%llu\n",
           n - 1, n, CN, CD, tot.trees, tot.qfail, tot.stepfail, (double)tot.vtried / (double)tot.trees, tot.minmargin, NESTED, tot.unique, tot.checksum);
    return 0;
}
