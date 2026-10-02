# Own hill-climber for claims 1/2: nbar-bar 3-voice cell inside |: :|, scored by compute_score.
import random, sys, json, copy
from vc import S
from gen import pool
LAD=[pool(4,5)+["c'"], pool(3,4), pool(2,3)]   # treble, mid, bass ladders (diatonic C)
def rbar(rng,v):
    left=8; ev=[]
    while left:
        d=rng.choice([x for x in (1,2,3,4) if x<=left]); left-=d
        ev.append([rng.randrange(len(LAD[v])), d, rng.random()<0.5, False])
    return ev
def render(cell, nbar):
    h=["X:1","T:c","M:4/4","L:1/8","Q:1/4=100","K:C"]
    for v in range(3):
        bars=[]
        for b in cell[v]:
            toks=[]
            for i,d,st,dy in b:
                lad=LAD[v]; n=lad[i] if not dy else "["+lad[i]+lad[min(len(lad)-1,i+2)]+"]"
                toks.append(("." if st else "")+n+("" if d==1 else str(d)))
            bars.append(" ".join(toks))
        h+=[f"V:{v+1}", "|: "+" | ".join(bars)+" :|"]
    return "\n".join(h)
def mutate(rng,cell):
    c=copy.deepcopy(cell); v=rng.randrange(3); b=rng.randrange(len(c[v])); bar=c[v][b]
    r=rng.random(); e=rng.randrange(len(bar))
    if r<0.4: bar[e][0]=max(0,min(len(LAD[v])-1,bar[e][0]+rng.choice((-3,-2,-1,1,2,3))))
    elif r<0.6: bar[e][2]=not bar[e][2]
    elif r<0.75: bar[e][3]=not bar[e][3]
    elif r<0.9 and len(bar)>1:  # merge e with neighbour
        j=e+1 if e+1<len(bar) else e-1; a,bb=sorted((e,j))
        if bar[a][1]+bar[bb][1]<=4: bar[a][1]+=bar[bb][1]; del bar[bb]
    else:  # split
        if bar[e][1]>=2:
            d=bar[e][1]; k=rng.randrange(1,d); bar[e][1]=k; bar.insert(e+1,[bar[e][0],d-k,bar[e][2],False])
    return c
def climb(seed,nbar,iters):
    rng=random.Random(seed)
    cell=[[rbar(rng,v) for _ in range(nbar)] for v in range(3)]
    best=S(render(cell,nbar)); start=best; traj=[]
    for it in range(iters):
        c=mutate(rng,cell); s=S(render(c,nbar))
        if s>=best: cell,best=c,s
        if it%100==0: traj.append(round(best,3))
    abc=render(cell,nbar)
    return dict(seed=seed,nbar=nbar,start=start,best=best,chars=len(abc),abc=abc,traj=traj)
if __name__=="__main__":
    seed,nbar,iters=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
    r=climb(seed,nbar,iters)
    json.dump(r,open(f"climb_n{nbar}_s{seed}.json","w"),indent=1)
    print(r["seed"],r["nbar"],"start %.3f best %.3f chars %d"%(r["start"],r["best"],r["chars"]),r["traj"])
