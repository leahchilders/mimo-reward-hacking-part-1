"""Random search over 200 generator configs (2-4 voices, ranges, note values, chords, rests, tempo; 32/48/64 bars).
`python search.py [seed=0] [N=200]`. Writes search_results.json (best first) and abc_best_random.abc (0.889)."""
import harness, random, json, time, sys
from gen import *
def piece(seed, prm, nbars):
    rng=random.Random(seed)
    nv=prm["nv"]; voices=[]
    ranges=[(prm["rh_lo"],prm["rh_lo"]+prm["rh_span"])]+[(prm["lh_lo"]+12*i,prm["lh_lo"]+12*i+prm["lh_span"]) for i in range(nv-1)]
    for vi,(lo,hi) in enumerate(ranges):
        pool=diatonic(lo,hi); w=[pool[len(pool)//2]]
        durs=prm["rh_durs"] if vi==0 else prm["lh_durs"]
        voices.append([rand_bar(rng,pool,durs=durs,walk=w,step=prm["step"] if vi==0 else 3,chord_p=0 if vi==0 else prm["chord_p"],rest_p=prm["rest_p"] if vi==0 else 0) for _ in range(nbars)])
    return assemble(header(bpm=prm["bpm"],title="rw",nvoice=nv),voices)
DUR_OPTS=[(1,),(1,1,2),(1,1,2,2,3,4),(2,),(2,4),(1,2,4,8),(4,8),(8,),(1,1,1,2)]
def sample(rng):
    return dict(nv=rng.choice([2,2,3,4]),rh_lo=rng.choice([55,60,65,67]),rh_span=rng.choice([12,17,24]),
                lh_lo=rng.choice([24,28,31,36,40]),lh_span=rng.choice([12,17,24]),
                rh_durs=rng.choice(DUR_OPTS),lh_durs=rng.choice(DUR_OPTS),step=rng.choice([1,2,3,5]),
                chord_p=rng.choice([0,0.2,0.5,0.9]),rest_p=rng.choice([0,0.05,0.15]),bpm=rng.choice([60,81,100,120,140]))
rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 0)
N=int(sys.argv[2]) if len(sys.argv)>2 else 200
best=[]; allr=[]; t0=time.time()
for i in range(N):
    prm=sample(rng); nbars=rng.choice([32,48,64])
    abc=piece(i,prm,nbars)
    r=harness.compute_score("music","```abc\n"+abc+"\n```")
    allr.append(r); best.append((r,i,prm,nbars,abc))
best.sort(key=lambda x:-x[0])
print("trials",N,"time %.0fs"%(time.time()-t0),"mean %.3f"%(sum(allr)/N))
for r,i,prm,nb,abc in best[:5]: print(round(r,3),nb,prm)
open("abc_best_random.abc","w").write(best[0][4])
json.dump([dict(r=r,prm=prm,nbars=nb) for r,i,prm,nb,abc in best],open("search_results.json","w"))
