"""Driver: run ./wlc n K id for id=0..K-1 in parallel subprocesses, aggregate, save examples."""
import subprocess, sys, os, json, re, time
HERE = os.path.dirname(os.path.abspath(__file__))
OEIS = {21: 2144505, 22: 5623756, 23: 14828074, 24: 39299897, 25: 104636890, 26: 279793450, 27: 751065460,
        28: 2023443032, 29: 5469566585, 30: 14830871802}
def run(n, K):
    t0 = time.time()
    procs = [subprocess.Popen([os.path.join(HERE, 'wlc'), str(n), str(K), str(i)], stdout=subprocess.PIPE, text=True) for i in range(K)]
    outs = [p.communicate()[0] for p in procs]
    rcs = [p.returncode for p in procs]
    agg = dict(n=n, K=K, trees=0, nonunimodal=0, nonLC=0, nonLC_in_window_LM=0, nonLC_in_window_beta=0, minrel=9.0, total_generated=set(), exit_codes=rcs)
    examples = []
    for o in outs:
        for line in o.splitlines():
            if line.startswith('RESULT'):
                d = dict(kv.split('=') for kv in line.split()[1:])
                for k in ('trees', 'nonunimodal', 'nonLC', 'nonLC_in_window_LM', 'nonLC_in_window_beta'): agg[k] += int(d[k])
                agg['minrel'] = min(agg['minrel'], float(d['minrel'])); agg['total_generated'].add(int(d['total_generated']))
            elif line.startswith('EX'):
                examples.append(line)
    agg['total_generated'] = sorted(agg['total_generated'])
    agg['OEIS_A000055'] = OEIS.get(n); agg['count_ok'] = (agg['trees'] == OEIS.get(n))
    agg['seconds'] = round(time.time() - t0, 1)
    json.dump(dict(summary=agg, examples=examples), open(os.path.join(HERE, 'wlc_c_n%d.json' % n), 'w'), indent=1)
    print('C-WLC n=%d trees=%d (OEIS ok=%s) nonunimodal=%d nonLC_trees=%d nonLC_in_window[ceil(n/4),LM]=%d in_window[ceil(n/4),beta]=%d min(first nonLC/alpha)=%s exits=%s time=%.0fs' % (
        n, agg['trees'], agg['count_ok'], agg['nonunimodal'], agg['nonLC'], agg['nonLC_in_window_LM'], agg['nonLC_in_window_beta'],
        agg['minrel'] if agg['nonLC'] else None, set(rcs), agg['seconds']), flush=True)
if __name__ == '__main__':
    K = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1): run(n, K)
