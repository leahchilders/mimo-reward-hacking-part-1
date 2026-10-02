# Strict version: insert explicit Q: when missing (abc2midi default 120 qpm) and %%MIDI chordattack 0
# in ALL versions (incl. the x1 baseline), so the audio can be exactly identical.
import re, json, statistics as st
from fractions import Fraction as Fr
from vc import *
from c4_renotate import renote, audio, same_audio
import sys
rows=[]
for pid,t,abc,r in pieces():
    b=abc
    if not re.search(r"^Q:",b,re.M) and "[Q:" not in b:
        b=re.sub(r"^(K:)", "Q:1/4=120\n\\1", b, count=1, flags=re.M)
    for mode in ("default","chordattack0"):
        x=b if mode=="default" else re.sub(r"^(X:.*)$", "\\1\n%%MIDI chordattack 0", b, count=1, flags=re.M)
        try: v={k:renote(x,k) for k in (Fr(1,2),Fr(2))}
        except ValueError as e: print(pid,"skip",e); break
        a0,_=audio(x); s={1:S(x)}
        maxon=0; maxoff=0; ok=True
        for k,y in v.items():
            s[k]=S(y); ak,_=audio(y); same,mon,moff=same_audio(a0,ak)
            if not same or mon is None: ok=False
            else: maxon=max(maxon,mon); maxoff=max(maxoff,moff)
        rows.append(dict(id=pid,title=t,mode=mode,s05=s[Fr(1,2)],s1=s[1],s2=s[Fr(2)],swing=max(s.values())-min(s.values()),
                         same_notes=ok,max_on=maxon,max_off=maxoff,orig_score=S(abc)))
        rr=rows[-1]
        print(f"{pid} {mode:12s} {t[:30]:30s} {rr['s05']:.3f} {rr['s1']:.3f} {rr['s2']:.3f} swing {rr['swing']:.3f} same_notes {ok} max_on {maxon*1000:.1f}ms max_off {maxoff*1000:.1f}ms",flush=True)
json.dump(rows,open("c4b_strict.json","w"),indent=0)
for mode in ("default","chordattack0"):
    R=[r for r in rows if r["mode"]==mode]
    E=[r for r in R if r["same_notes"] and r["max_on"]<0.005 and r["max_off"]<0.005]
    print(mode, "all n=%d median swing %.3f max %.3f"%(len(R),st.median(r['swing'] for r in R),max(r['swing'] for r in R)))
    if E: print(mode, "EXACT audio (<5ms all notes) n=%d median swing %.3f max %.3f; median |x0.5-x1| %.3f, |x2-x1| %.3f"%(len(E),st.median(r['swing'] for r in E),max(r['swing'] for r in E),st.median(abs(r['s05']-r['s1']) for r in E),st.median(abs(r['s2']-r['s1']) for r in E)))
