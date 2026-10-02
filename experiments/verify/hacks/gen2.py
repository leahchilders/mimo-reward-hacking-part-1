# variant generator: per-voice ladders + optional dyads (third/fifth above) with per-voice probability
import random
from gen import pool
def bar(rng, lad, durs, stp, chp, beats=8):
    left=beats; toks=[]
    while left>0:
        d=rng.choice([x for x in durs if x<=left]); left-=d
        i=rng.randrange(len(lad))
        if rng.random()<chp:
            j=min(len(lad)-1,i+rng.choice((2,4))); n="["+lad[i]+lad[j]+"]"
        else: n=lad[i]
        toks.append(("." if rng.random()<stp else "")+n+("" if d==1 else str(d)))
    return " ".join(toks)
def piece(seed, ladders, chps, bars=16, durs=(1,2,3,4), stp=0.5, rep=False):
    rng=random.Random(seed)
    h=["X:1","T:r","M:4/4","L:1/8","Q:1/4=100","K:C"]
    for v,(lad,chp) in enumerate(zip(ladders,chps)):
        h.append(f"V:{v+1}")
        body=" | ".join(bar(rng,lad,durs,stp,chp) for _ in range(bars))
        h.append(("|: "+body+" :|") if rep else body+" |]")
    return "\n".join(h)+"\n"
