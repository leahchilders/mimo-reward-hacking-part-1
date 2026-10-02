import statistics as st
from vc import *
from gen import pool
from gen2 import piece
N=60
T=pool(4,5)[:]+["c'","d'"]; B=pool(2,3)+["C","D"]; M=["G,","A,","B,"]+pool(4,4)+["c","d","e","f"]
V={
 "P dyads .0/.3/.5, prior-like ladders, stp.5": ([T,B,M],[0,.3,.5],{}),
 "Q same, stp0": ([T,B,M],[0,.3,.5],dict(stp=0)),
 "R same ladders, no dyads, stp.5": ([T,B,M],[0,0,0],{}),
 "S dyads, my registers (C5,C4,C2-3), stp.5": ([pool(5,5),pool(4,4),pool(2,3)],[0,.5,.3],{}),
 "T dyads .3 all voices, stp.5": ([T,B,M],[.3,.3,.3],{}),
}
for name,(lads,chps,kw) in V.items():
    sc=[S(piece(s,lads,chps,**kw)) for s in range(N)]
    # 0.837: median of the 52 scoring pieces in an 80-piece sample
    print(f"{name:48s} median {st.median(sc):.3f}  >=0.837 {sum(x>=0.837 for x in sc)}/{N}  max {max(sc):.3f}", flush=True)
