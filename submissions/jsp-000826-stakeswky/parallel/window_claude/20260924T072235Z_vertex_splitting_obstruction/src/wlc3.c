/* Threaded exhaustive checker: one producer thread runs the WROM generator (same code as wlc.c,
 * validated against OEIS and Python), NW worker threads evaluate batches.
 * Per tree: unimodality, all LC breaks, window [ceil(n/4), ceil((2a-1)/3)] strict LC (equalities
 * counted), beta-window, minimal normalised window margin n*(1 - p_{k-1}p_{k+1}/p_k^2),
 * and a coefficient checksum identical to wlc.c for cross-validation.
 * Usage: wlc3 n NW  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>

#define MAXN 34
#define BATCH 8192
#define NBUF 64
typedef long long ll;
typedef __int128 i128;

static int n;

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
static int indep_poly(const unsigned char *L, ll *p) {
    int par[MAXN], stackv[MAXN];
    ll A[MAXN][MAXN + 1], B[MAXN][MAXN + 1];
    int degA[MAXN], degB[MAXN];
    ll S[MAXN + 1], T[MAXN + 1];
    int sp = 0;
    for (int i = 0; i < n; i++) {
        while (sp && L[stackv[sp - 1]] >= L[i]) sp--;
        par[i] = sp ? stackv[sp - 1] : -1;
        stackv[sp++] = i;
    }
    for (int v = 0; v < n; v++) { A[v][0] = 1; degA[v] = 0; B[v][0] = 0; B[v][1] = 1; degB[v] = 1; }
    for (int v = n - 1; v >= 1; v--) {
        int u = par[v];
        int dS = degA[v] > degB[v] ? degA[v] : degB[v];
        for (int k = 0; k <= dS; k++) S[k] = (k <= degA[v] ? A[v][k] : 0) + (k <= degB[v] ? B[v][k] : 0);
        int dA = degA[u];
        memset(T, 0, sizeof(ll) * (dA + dS + 1));
        for (int i = 0; i <= dA; i++) if (A[u][i]) for (int k = 0; k <= dS; k++) T[i + k] += A[u][i] * S[k];
        degA[u] = dA + dS; memcpy(A[u], T, sizeof(ll) * (degA[u] + 1));
        int dB = degB[u], dv = degA[v];
        memset(T, 0, sizeof(ll) * (dB + dv + 1));
        for (int i = 0; i <= dB; i++) if (B[u][i]) for (int k = 0; k <= dv; k++) T[i + k] += B[u][i] * A[v][k];
        degB[u] = dB + dv; memcpy(B[u], T, sizeof(ll) * (degB[u] + 1));
    }
    int d = degA[0] > degB[0] ? degA[0] : degB[0];
    for (int k = 0; k <= d; k++) p[k] = (k <= degA[0] ? A[0][k] : 0) + (k <= degB[0] ? B[0][k] : 0);
    while (d > 0 && p[d] == 0) d--;
    return d;
}

/* ring of batches */
typedef struct { int count; unsigned char seq[BATCH][MAXN]; } batch_t;
static batch_t *bufs;
static int full_q[NBUF], free_q[NBUF];
static int full_head = 0, full_tail = 0, full_cnt = 0, free_head = 0, free_tail = 0, free_cnt = 0, done = 0;
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t cv_full = PTHREAD_COND_INITIALIZER, cv_free = PTHREAD_COND_INITIALIZER;
static ll generated = 0;

typedef struct {
    ll trees, nonuni, nonlc, win_lm, win_beta, eq_win;
    unsigned long long checksum;
    double minrel, minmargin;
    char ex[64][400]; int nex;
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
            bt->count++; generated++;
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

static void *worker(void *arg) {
    stats_t *st = (stats_t *)arg;
    ll p[MAXN + 2];
    for (;;) {
        pthread_mutex_lock(&mu);
        while (full_cnt == 0 && !done) pthread_cond_wait(&cv_full, &mu);
        if (full_cnt == 0 && done) { pthread_mutex_unlock(&mu); break; }
        int b = full_q[full_head]; full_head = (full_head + 1) % NBUF; full_cnt--;
        pthread_mutex_unlock(&mu);
        batch_t *bt = &bufs[b];
        for (int t = 0; t < bt->count; t++) {
            const unsigned char *L = bt->seq[t];
            int a = indep_poly(L, p);
            st->trees++;
            for (int k = 0; k <= a; k++) st->checksum += (unsigned long long)p[k] * (unsigned long long)(k + 1) * 0x9E3779B97F4A7C15ULL;
            int k = 0;
            while (k < a && p[k] <= p[k + 1]) k++;
            int uni = 1;
            for (int s = k; s < a; s++) if (p[s] < p[s + 1]) { uni = 0; break; }
            if (!uni) st->nonuni++;
            int first_bad = -1, inLM = 0, inB = 0;
            int q = (n + 3) / 4, LM = (2 * a + 1) / 3;
            ll beta = ((ll)a * (n - 1) + n + a - 1) / (n + a);
            for (int s = 1; s < a; s++) {
                i128 lhs = (i128)p[s] * p[s], rhs = (i128)p[s - 1] * p[s + 1];
                if (s >= q && s <= LM) {
                    if (lhs == rhs) st->eq_win++;
                    double m = (double)n * (1.0 - (double)rhs / (double)lhs);
                    if (m < st->minmargin) st->minmargin = m;
                }
                if (lhs < rhs) {
                    if (first_bad < 0) first_bad = s;
                    if (s >= q && s <= LM) inLM = 1;
                    if (s >= q && s <= beta) inB = 1;
                }
            }
            if (first_bad >= 0) {
                st->nonlc++; st->win_lm += inLM; st->win_beta += inB;
                double rel = (double)first_bad / a; if (rel < st->minrel) st->minrel = rel;
                if (st->nex < 64 && (st->nex < 24 || inLM || inB || !uni)) {
                    int off = snprintf(st->ex[st->nex], 400, "EX first_bad=%d alpha=%d rel=%.4f inLM=%d inBeta=%d unimodal=%d levels=", first_bad, a, rel, inLM, inB, uni);
                    for (int i = 0; i < n && off < 390; i++) off += snprintf(st->ex[st->nex] + off, 400 - off, "%d%c", L[i], i + 1 < n ? ',' : ' ');
                    st->nex++;
                }
            }
        }
        pthread_mutex_lock(&mu);
        free_q[free_tail] = b; free_tail = (free_tail + 1) % NBUF; free_cnt++;
        pthread_cond_signal(&cv_free);
        pthread_mutex_unlock(&mu);
    }
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: wlc3 n NW\n"); return 2; }
    n = atoi(argv[1]); int NW = atoi(argv[2]);
    if (n < 4 || n > 32 || NW < 1 || NW > 64) { fprintf(stderr, "bad args\n"); return 2; }
    bufs = (batch_t *)malloc(sizeof(batch_t) * NBUF);
    for (int i = 0; i < NBUF; i++) { free_q[i] = i; } free_cnt = NBUF; free_tail = 0;
    stats_t *st = (stats_t *)calloc(NW, sizeof(stats_t));
    for (int w = 0; w < NW; w++) { st[w].minrel = 9.0; st[w].minmargin = 1e18; }
    pthread_t prod, *wk = (pthread_t *)malloc(sizeof(pthread_t) * NW);
    pthread_create(&prod, NULL, producer, NULL);
    for (int w = 0; w < NW; w++) pthread_create(&wk[w], NULL, worker, &st[w]);
    pthread_join(prod, NULL);
    for (int w = 0; w < NW; w++) pthread_join(wk[w], NULL);
    stats_t tot; memset(&tot, 0, sizeof(tot)); tot.minrel = 9.0; tot.minmargin = 1e18;
    for (int w = 0; w < NW; w++) {
        tot.trees += st[w].trees; tot.nonuni += st[w].nonuni; tot.nonlc += st[w].nonlc; tot.win_lm += st[w].win_lm;
        tot.win_beta += st[w].win_beta; tot.eq_win += st[w].eq_win; tot.checksum += st[w].checksum;
        if (st[w].minrel < tot.minrel) tot.minrel = st[w].minrel;
        if (st[w].minmargin < tot.minmargin) tot.minmargin = st[w].minmargin;
        for (int e = 0; e < st[w].nex; e++) printf("%s\n", st[w].ex[e]);
    }
    printf("RESULT n=%d trees=%lld generated=%lld nonunimodal=%lld nonLC=%lld nonLC_in_window_LM=%lld nonLC_in_window_beta=%lld window_equalities=%lld minrel=%.6f min_window_margin_times_n=%.6f checksum=%llu\n",
           n, tot.trees, generated, tot.nonuni, tot.nonlc, tot.win_lm, tot.win_beta, tot.eq_win, tot.minrel, tot.minmargin, tot.checksum);
    return 0;
}
