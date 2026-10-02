"""Own bar-level hill-climber (3 voices, block V: layout so per-voice %%MIDI lines can be inserted).
usage: climb.py SEED STACC(0|1) ITERS NBARS"""
import sys, random, json, hc
seed, stacc, iters, nbars = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed)
MID = ["C","D","E","F","G","A","B","c","d","e","G,","A,","B,"]
pools = [hc.TRE, hc.BAS, MID]; chp = [0.0, 0.3, 0.5]
def build(bars):
    h = ["X:1","T:climb","M:4/4","L:1/8","Q:1/4=100","K:C"]
    for v,(clef,bs) in enumerate(zip(["treble","bass","treble"], bars)):
        h += [f"V:{v+1} clef={clef}", " | ".join(bs) + " |]"]
    return "\n".join(h)
bars = [[hc.rand_bar(rng, pools[v], stacc*0.5, chp[v]) for _ in range(nbars)] for v in range(3)]
best = hc.reward(build(bars)); start = best
for it in range(iters):
    v = rng.randrange(3); i = rng.randrange(nbars); old = bars[v][i]
    bars[v][i] = hc.rand_bar(rng, pools[v], stacc*0.5, chp[v])
    s = hc.reward(build(bars))
    if s >= best: best = s
    else: bars[v][i] = old
open(f"pieces/climb_s{seed}_st{int(stacc)}_b{nbars}.abc","w").write(build(bars))
print(json.dumps(dict(seed=seed, stacc=stacc, nbars=nbars, iters=iters, start=start, best=best)))
