import re, statistics as st, collections
from fractions import Fraction as Fr
from vc import *
from vc import vm_common
from mscorer.score import score
from c4_renotate import renote
dR=collections.defaultdict(list); dC=collections.defaultdict(list)
for pid,t,abc,r in pieces():
    b=abc if re.search(r"^Q:",abc,re.M) or "[Q:" in abc else re.sub(r"^(K:)","Q:1/4=120\n\\1",abc,count=1,flags=re.M)
    ca=re.sub(r"^(X:.*)$","\\1\n%%MIDI chordattack 0",b,count=1,flags=re.M)
    try: h=renote(ca,Fr(1,2))
    except ValueError: continue
    p=[score(midi(x)[2],vm_common.REF)["per_feature"] for x in (b,ca,h)]
    for k in p[0]:
        dC[k].append(p[1][k]-p[0][k]); dR[k].append(p[2][k]-p[1][k])
print("feature: mean |delta| for chordattack0 vs default | for x0.5 renotation vs x1 (both chordattack0)")
for k in dR: print(f"{k:22s} {st.mean(abs(x) for x in dC[k]):.3f}   {st.mean(abs(x) for x in dR[k]):.3f}")
