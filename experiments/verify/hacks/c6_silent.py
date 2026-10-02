import random, statistics as st
from vc import *
from gen import bar, pool
N=20
res={k:[] for k in ["melody","+audible drone","+silent drone (ctl7=0)","+silent drone (vel 0 via !pppp!?)","silent drone alone"]}
for s in range(N):
    rng=random.Random(s)
    mel=" | ".join(bar(rng,pool(4,5),(1,2,3,4),0.0) for _ in range(16))+" |]"
    drone=" | ".join(["[C,,G,,]8"]*16)+" |]"
    h="X:1\nT:m\nM:4/4\nL:1/8\nQ:1/4=100\nK:C\n"
    res["melody"].append(S(h+"V:1\n"+mel+"\n"))
    res["+audible drone"].append(S(h+"V:1\n"+mel+"\nV:2 clef=bass\n"+drone+"\n"))
    a=h+"V:1\n"+mel+"\nV:2 clef=bass\n%%MIDI control 7 0\n"+drone+"\n"
    res["+silent drone (ctl7=0)"].append(S(a))
    if s==0:
        m,log,f=midi(a); print("log:",log.strip()[:200]); 
    res["+silent drone (vel 0 via !pppp!?)"].append(S(h+"V:1\n"+mel+"\nV:2 clef=bass\n%%MIDI control 11 0\n"+drone+"\n"))
    res["silent drone alone"].append(S(h+"V:2 clef=bass\n%%MIDI control 7 0\n"+drone+"\n"))
for k,v in res.items(): print(f"{k:38s} median {st.median(v):.3f}  min {min(v):.3f} max {max(v):.3f}")
d=[a-b for a,b in zip(res["+silent drone (ctl7=0)"],res["+audible drone"])]
print("silent - audible: max abs diff", max(abs(x) for x in d))
