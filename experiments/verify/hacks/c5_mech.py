# Is the 1-tick-late sampling THE mechanism of the staccato gain? Compare stp .5 vs 0 under
# (a) original scorer, (b) sonority sampling at nominal onsets (grid tick + 1).
import statistics as st, collections
from vc import *
import mscorer.feats as F
from gen import pool
from gen2 import piece
orig=F._sonorities
def patched(notes, div, grid=0.5):
    step=max(1,int(div*grid)); end=max(n[0]+n[1] for n in notes); out=[]
    for t in range(1, end+2, step):
        cur=[(p,v) for (o,d,ch,p,v) in notes if ch!=9 and o<=t<o+max(d,1)]
        if cur: out.append((t,cur))
    return out
T=pool(4,5)+["c'","d'"]; B=pool(2,3)+["C","D"]; M=["G,","A,","B,"]+pool(4,4)+["c","d","e","f"]
N=40
def run(stp):
    tot=[]; grp=collections.defaultdict(list)
    for s in range(N):
        r=rec(piece(s,[T,B,M],[0,.3,.5],stp=stp))
        tot.append(r["total"]/100)
        for g,v in r["groups"].items(): grp[g].append(v)
    return tot,grp
for label,fn in [("original",orig),("nominal-onset sampling",patched)]:
    F._sonorities=fn
    a,ga=run(0.5); b,gb=run(0.0)
    print(f"{label}: stp.5 median {st.median(a):.3f}  stp0 median {st.median(b):.3f}  gain {st.median(a)-st.median(b):+.3f}  paired median gain {st.median([x-y for x,y in zip(a,b)]):+.3f}")
    print("   group medians stp.5 / stp0:", {g:(round(st.median(ga[g]),1),round(st.median(gb[g]),1)) for g in ga})
F._sonorities=orig
