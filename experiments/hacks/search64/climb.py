"""Hill-climb from the best search config: new random bars, 600 steps, rng seed 7, keeping any change
that doesn't lower the reward. `python climb.py` writes abc_hillclimb.abc (= examples/hack_hillclimb.abc)."""
import harness, random, json
from gen import *
import search  # importing it reruns the 200-config search (seed 0), which rewrites search_results.json
res=json.load(open("search_results.json"))
prm=res[0]["prm"]; prm["rh_durs"]=tuple(prm["rh_durs"]); prm["lh_durs"]=tuple(prm["lh_durs"]); nb=res[0]["nbars"]
rng=random.Random(7)
nv=prm["nv"]
ranges=[(prm["rh_lo"],prm["rh_lo"]+prm["rh_span"])]+[(prm["lh_lo"]+12*i,prm["lh_lo"]+12*i+prm["lh_span"]) for i in range(nv-1)]
def newbar(vi):
    lo,hi=ranges[vi]; pool=diatonic(lo,hi)
    durs=rng.choice([(1,),(1,1,2),(1,1,2,2,3,4),(2,),(2,4),(1,2,4,8),(4,8),(8,)])
    return rand_bar(rng,pool,durs=durs,walk=[rng.choice(pool)],step=rng.choice([1,2,3,5]),chord_p=0 if vi==0 else rng.choice([0,.3,.8]),rest_p=0)
voices=[[newbar(v) for _ in range(nb)] for v in range(nv)]
H=header(bpm=60,title="climb",nvoice=nv)
def sc(v): return harness.compute_score("music","```abc\n"+assemble(H,v)+"\n```")
cur=sc(voices); traj=[cur]
for step in range(600):
    v=[list(x) for x in voices]
    for _ in range(rng.choice([1,2,4])):
        vi=rng.randrange(nv); v[vi][rng.randrange(nb)]=newbar(vi)
    s=sc(v)
    if s>=cur: voices, cur = v, s
    if step%100==99: traj.append(cur)
print("hill-climb trajectory (every 100 steps):",[round(x,3) for x in traj])
abc=assemble(H,voices); open("abc_hillclimb.abc","w").write(abc)
r,rec,f,s=harness.score_abc(abc)
print("final",r,s["groups"],"key",f["key_tonic"],f["key_minor"],"nchan",f["n_chan"])
print(s["per_feature"])
