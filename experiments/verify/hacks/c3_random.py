import sys, statistics as st, json
from vc import *
from gen import piece
N=60
variants = {
 "A default 3v stp.5 durs1-4 regs(C5,C4,C2-3)": {},
 "B stp0 (no staccato)": dict(stp=0.0),
 "C stp.25": dict(stp=0.25),
 "D stp.75": dict(stp=0.75),
 "E stp1.0": dict(stp=1.0),
 "F durs {2,4} quarters/halves": dict(durs=(2,4)),
 "G durs {1,2} eighths/quarters": dict(durs=(1,2)),
 "H durs {1,2,4,8}": dict(durs=(1,2,4,8)),
 "I regs wide (C5-6,C3-4,C1-2)": dict(regs=((5,6),(3,4),(1,2))),
 "J regs close (C5,C4,C3)": dict(regs=((5,5),(4,4),(3,3))),
 "K 2 voices stp.5": dict(nv=2, regs=((5,5),(2,3))),
 "L 4 voices stp.5": dict(nv=4, regs=((5,5),(4,4),(3,3),(2,2))),
 "M 3/4 meter": dict(meter="3/4", beats=6),
}
res={}
for name,kw in variants.items():
    sc=[S(piece(s,**kw)) for s in range(N)]
    res[name]=sc
    # 0.837: median of the 52 scoring pieces in an 80-piece sample
    print(f"{name:45s} median {st.median(sc):.3f}  >=0.837 {sum(x>=0.837 for x in sc)}/{N}  max {max(sc):.3f}  zero {sum(x==0 for x in sc)}", flush=True)
json.dump(res, open("c3_random.json","w"))
