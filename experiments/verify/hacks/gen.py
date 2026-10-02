import random
DIA = ["C","D","E","F","G","A","B"]
def oct_names(o):  # o: 4 -> C..B (C4), 5 -> c..b, 3 -> C,..B,, 6 -> c'..
    if o==4: return DIA[:]
    if o==5: return [x.lower() for x in DIA]
    if o<4: return [x+","*(4-o) for x in DIA]
    return [x.lower()+"'"*(o-5) for x in DIA]
def pool(lo,hi):
    out=[]
    for o in range(lo,hi+1): out+=oct_names(o)
    return out
def bar(rng, pl, durs, stp, beats=8):
    left=beats; toks=[]
    while left>0:
        d=rng.choice([x for x in durs if x<=left] or [left]); left-=d
        pre="." if rng.random()<stp else ""
        toks.append(f"{pre}{rng.choice(pl)}{'' if d==1 else d}")
    return " ".join(toks)
def piece(seed, nv=3, bars=16, durs=(1,2,3,4), stp=0.5, regs=((5,5),(4,4),(2,3)), meter="4/4", beats=8):
    rng=random.Random(seed)
    h=["X:1","T:r",f"M:{meter}","L:1/8","Q:1/4=100","K:C"]
    clefs=["treble","treble","bass","bass"]
    for v in range(nv):
        pl=pool(*regs[v])
        h.append(f"V:{v+1} clef={clefs[v]}")
        h.append(" | ".join(bar(rng,pl,durs,stp,beats) for _ in range(bars))+" |]")
    return "\n".join(h)+"\n"
