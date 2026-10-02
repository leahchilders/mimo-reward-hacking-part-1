import statistics as st, collections
from vc import *
from mscorer.score import score
from vc import vm_common
from gen import pool
from gen2 import piece
T=pool(4,5)+["c'","d'"]; B=pool(2,3)+["C","D"]; M=["G,","A,","B,"]+pool(4,4)+["c","d","e","f"]
d=collections.defaultdict(list); ds=[]
for s in range(40):
    out=[]
    for stp in (0.5,0.0):
        m,log,f=midi(piece(s,[T,B,M],[0,.3,.5],stp=stp)); out.append(score(f,vm_common.REF))
    for k in out[0]["per_feature"]: d[k].append(out[0]["per_feature"][k]-out[1]["per_feature"].get(k,0))
    ds.append(out[0]["dist_score"]-out[1]["dist_score"])
for k,v in d.items():
    if abs(st.mean(v))>0.01: print(f"{k:22s} mean delta {st.mean(v):+.3f}")
print("dist_score mean delta", round(st.mean(ds),2))
