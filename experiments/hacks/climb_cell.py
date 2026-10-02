"""Hill-climb only a K-bar cell (3 voices). mode: loopK (cell played verbatim to 16 bars, written out),
tinyK (cell written once inside |: :|, i.e. abc2midi plays it twice). usage: climb_cell.py MODE K SEED ITERS"""
import sys, random, json
import hc, degen
mode, K, seed, iters = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed)
def build(cell):
    if mode == "loop":
        vb = [[degen.render_bar(b, degen.LAD[degen.VO[v][0]]) for b in cell[v]] * (16 // K) for v in range(3)]
        return degen.piece(vb, 3)
    vb = [[degen.render_bar(b, degen.LAD[degen.VO[v][0]]) for b in cell[v]] for v in range(3)]
    return degen.piece(vb, 3, rep=True)
def nb(v): return degen.rbar(rng, degen.LAD[degen.VO[v][0]], degen.VO[v][2], 0.5)
cell = [[nb(v) for _ in range(K)] for v in range(3)]
best = hc.reward(build(cell)); start = best
for _ in range(iters):
    v, i = rng.randrange(3), rng.randrange(K); old = cell[v][i]; cell[v][i] = nb(v)
    s = hc.reward(build(cell))
    if s >= best: best = s
    else: cell[v][i] = old
a = build(cell)
open(f"pieces/cell_{mode}{K}_s{seed}.abc", "w").write(a)
print(json.dumps(dict(mode=mode, K=K, seed=seed, iters=iters, start=start, best=best, chars=len(a), reward_check=hc.reward(a))))
