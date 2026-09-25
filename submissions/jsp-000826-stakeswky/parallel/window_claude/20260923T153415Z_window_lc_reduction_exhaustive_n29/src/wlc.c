/* Exhaustive check over all free trees of order n (WROM generation, port of the
 * networkx/Python generator validated against OEIS A000055):
 *   - unimodality of the independence sequence (plateaus allowed),
 *   - log-concavity at every interior index,
 *   - window log-concavity on [ceil(n/4), ceil((2a-1)/3)] and on [ceil(n/4), beta].
 * Parallel by residue: process `id` of `K` evaluates trees with index % K == id.
 * Output: one line of counts + up to MAXEX example non-LC trees.
 * Exact arithmetic: coefficients <= 2^n (n <= 32) in int64; products in __int128. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 34
#define MAXEX 40
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

/* split: left = L[1..m-1]-1, rest = [0] + L[m..n-1]; returns m, heights via pointers */
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

/* lexicographic compare of left=[L[1..m-1]-1] and rest=[0]+L[m..n-1] (same lengths) : returns >0 if left>rest */
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
        int slen = lh2 + 1;              /* suffix = 1..lh2+1 */
        for (int i = 0; i < slen; i++) L[n - slen + i] = 1 + i;
    }
}

/* independence polynomial via rooted DP; returns alpha; p[0..alpha] */
static int indep_poly(const int *L, ll *p) {
    static int par[MAXN], stackv[MAXN];
    static ll A[MAXN][MAXN + 1], B[MAXN][MAXN + 1];
    static int degA[MAXN], degB[MAXN];
    int sp = 0;
    for (int i = 0; i < n; i++) {
        while (sp && L[stackv[sp - 1]] >= L[i]) sp--;
        par[i] = sp ? stackv[sp - 1] : -1;
        stackv[sp++] = i;
    }
    for (int v = 0; v < n; v++) { A[v][0] = 1; degA[v] = 0; B[v][0] = 0; B[v][1] = 1; degB[v] = 1; }
    /* process in reverse preorder: children have larger index than parent */
    for (int v = n - 1; v >= 1; v--) {
        int u = par[v];
        /* S = A[v] + B[v] */
        static ll S[MAXN + 1], T[MAXN + 1];
        int dS = degA[v] > degB[v] ? degA[v] : degB[v];
        for (int k = 0; k <= dS; k++) S[k] = (k <= degA[v] ? A[v][k] : 0) + (k <= degB[v] ? B[v][k] : 0);
        /* A[u] *= S */
        int dA = degA[u];
        memset(T, 0, sizeof(ll) * (dA + dS + 1));
        for (int i = 0; i <= dA; i++) if (A[u][i]) for (int k = 0; k <= dS; k++) T[i + k] += A[u][i] * S[k];
        degA[u] = dA + dS; memcpy(A[u], T, sizeof(ll) * (degA[u] + 1));
        /* B[u] *= A[v] */
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

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: wlc n K id\n"); return 2; }
    n = atoi(argv[1]); int K = atoi(argv[2]), id = atoi(argv[3]);
    if (n < 2 || n > 32) { fprintf(stderr, "n out of range\n"); return 2; }
    int L[MAXN];
    int k0 = 0;
    for (int i = 0; i <= n / 2; i++) L[k0++] = i;
    for (int i = 1; i < (n + 1) / 2; i++) L[k0++] = i;
    ll idx = 0, trees = 0, nonuni = 0, nonlc = 0, win_lm = 0, win_beta = 0;
    unsigned long long checksum = 0;
    double minrel = 9.0; int examples = 0;
    ll p[MAXN + 2];
    for (;;) {
        next_tree(L);
        if (idx % K == id) {
            trees++;
            int a = indep_poly(L, p);
            for (int k = 0; k <= a; k++) checksum += (unsigned long long)p[k] * (unsigned long long)(k + 1) * 0x9E3779B97F4A7C15ULL;
            /* unimodality */
            int k = 0;
            while (k < a && p[k] <= p[k + 1]) k++;
            int uni = 1;
            for (int t = k; t < a; t++) if (p[t] < p[t + 1]) { uni = 0; break; }
            if (!uni) nonuni++;
            /* log-concavity */
            int first_bad = -1, inLM = 0, inB = 0;
            int q = (n + 3) / 4, LM = (2 * a + 1) / 3;
            ll beta = ((ll)a * (n - 1) + n + a - 1) / (n + a);
            for (int t = 1; t < a; t++) {
                if ((i128)p[t] * p[t] < (i128)p[t - 1] * p[t + 1]) {
                    if (first_bad < 0) first_bad = t;
                    if (t >= q && t <= LM) inLM = 1;
                    if (t >= q && t <= beta) inB = 1;
                }
            }
            if (first_bad >= 0) {
                nonlc++; win_lm += inLM; win_beta += inB;
                double rel = (double)first_bad / a; if (rel < minrel) minrel = rel;
                if (examples < MAXEX || inLM || inB || !uni) {
                    examples++;
                    printf("EX first_bad=%d alpha=%d rel=%.4f inLM=%d inBeta=%d unimodal=%d levels=", first_bad, a, rel, inLM, inB, uni);
                    for (int i = 0; i < n; i++) printf("%d%c", L[i], i + 1 < n ? ',' : ' ');
                    printf("p=");
                    for (int t = 0; t <= a; t++) printf("%lld%c", p[t], t < a ? ',' : '\n');
                }
            }
        }
        idx++;
        if (!next_rooted_tree(L, -1)) break;
    }
    printf("RESULT n=%d K=%d id=%d trees=%lld nonunimodal=%lld nonLC=%lld nonLC_in_window_LM=%lld nonLC_in_window_beta=%lld minrel=%.6f checksum=%llu total_generated=%lld\n",
           n, K, id, trees, nonuni, nonlc, win_lm, win_beta, minrel, checksum, idx);
    return 0;
}
