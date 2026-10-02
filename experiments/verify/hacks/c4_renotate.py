# Claim 4: same audio, different notation -> different score?
import re, struct, statistics as st, json, os, tempfile, subprocess as sp
from fractions import Fraction as Fr
from vc import *

def tempo_map(data):
    """Own minimal scan: returns (div, [(tick, usec_per_q)], notes[(on_tick, off_tick, ch, pitch)])."""
    div=struct.unpack(">H",data[12:14])[0]; ntrk=struct.unpack(">H",data[10:12])[0]
    i=14; tempos=[]; notes=[]
    for _ in range(ntrk):
        ln=struct.unpack(">I",data[i+4:i+8])[0]; j=i+8; end=j+ln; t=0; run=None; on={}
        def vlq():
            nonlocal j
            v=0
            while True:
                b=data[j]; j+=1; v=(v<<7)|(b&0x7f)
                if not b&0x80: return v
        while j<end:
            t+=vlq(); s=data[j]
            if s==0xFF:
                typ=data[j+1]; j+=2; l=vlq()
                if typ==0x51: tempos.append((t,(data[j]<<16)|(data[j+1]<<8)|data[j+2]))
                j+=l; continue
            if s in (0xF0,0xF7):
                j+=1; l=vlq(); j+=l; continue
            if s&0x80: run=s; j+=1
            k=run&0xF0; ch=run&0x0F
            if k in (0xC0,0xD0): j+=1; continue
            a,b=data[j],data[j+1]; j+=2
            if k==0x90 and b>0: on.setdefault((ch,a),[]).append(t)
            elif k==0x80 or (k==0x90 and b==0):
                q=on.get((ch,a))
                if q: notes.append((q.pop(0),t,ch,a))
        i=end
    tempos.sort()
    return div,tempos or [(0,500000)],notes

def secs(div,tempos):
    def f(tick):
        s=0.0; last_t=0; us=500000
        for tt,u in tempos:
            if tt>tick: break
            s+=(tt-last_t)*us/div/1e6; last_t=tt; us=u
        return s+(tick-last_t)*us/div/1e6
    return f

def mid_bytes(abc):
    with tempfile.TemporaryDirectory() as td:
        open(td+"/a.abc","w").write(abc); sp.run([ABC2MIDI,td+"/a.abc","-o",td+"/a.mid"],capture_output=True)
        return open(td+"/a.mid","rb").read()

def audio(abc):
    div,tm,notes=tempo_map(mid_bytes(abc)); f=secs(div,tm)
    return sorted((round(f(a),4),round(f(b),4),c,p) for a,b,c,p in notes), len(tm)

def scale_frac(s, k):  # "1/16" * k
    x=Fr(s)*k; return f"{x.numerator}/{x.denominator}"

def renote(abc, k):
    """k=2: every notated value doubled; k=1/2 halved. Rescale L:, M: denominator, Q: unit."""
    k=Fr(k)
    has_L=re.search(r"^L:",abc,re.M)
    def L(m): return m.group(1)+scale_frac(m.group(2).strip(),k)
    def M(m):
        v=m.group(2).strip()
        if v=="C": v="4/4"
        if v=="C|": v="2/2"
        if v=="none" or "/" not in v: return m.group(0)
        num,den=v.split("/"); den=Fr(int(den))/k
        if den.denominator!=1: raise ValueError("meter")
        return m.group(1)+f"{num}/{den.numerator}"
    def Q(m):
        v=m.group(2).strip()
        mm=re.match(r'(?:"[^"]*"\s*)?((?:\d+/\d+\s*)+)=\s*(\d+)(.*)$', v)
        if not mm: raise ValueError("Q:"+v)
        units=" ".join(scale_frac(u,k) for u in mm.group(1).split())
        return m.group(1)+units+"="+mm.group(2)+mm.group(3)
    if not has_L: raise ValueError("no L")
    abc=re.sub(r"^(L:)(.*)$",L,abc,flags=re.M); abc=re.sub(r"(\[L:)([^\]]*)(?=\])",L,abc)
    abc=re.sub(r"^(M:)(.*)$",M,abc,flags=re.M); abc=re.sub(r"(\[M:)([^\]]*)(?=\])",M,abc)
    abc=re.sub(r"^(Q:)(.*)$",Q,abc,flags=re.M); abc=re.sub(r"(\[Q:)([^\]]*)(?=\])",Q,abc)
    return abc

def same_audio(a,b,tol=0.005):
    if len(a)!=len(b): return False, f"n {len(a)} vs {len(b)}", None
    on=[abs(x[0]-y[0]) for x,y in zip(a,b)]; off=[abs(x[1]-y[1]) for x,y in zip(a,b)]
    pitch=all(x[3]==y[3] for x,y in zip(a,b))
    return pitch, max(on), max(off)

rows=[]
for pid,t,abc,r in pieces():
    try:
        v={k:renote(abc,k) for k in (Fr(1,2),Fr(2))}
    except ValueError as e:
        print(pid,"skip",e); continue
    a0,ntemp=audio(abc); sc0=S(abc); out={"id":pid,"title":t,"s1":sc0,"ntempo":ntemp}
    for k,x in v.items():
        ak,_=audio(x); ok,mon,moff=same_audio(a0,ak)
        out[f"s{k}"]=S(x); out[f"audio{k}"]=(ok,mon,moff)
        out[f"exact{k}"]= ok and mon is not None and mon<0.005 and moff<0.005
        out[f"near{k}"]= ok and mon is not None and sum(1 for p,q in zip(a0,ak) if abs(p[0]-q[0])<0.025)/len(a0)>=0.95
    out["swing"]=max(out["s1"],out["s1/2"],out["s2"])-min(out["s1"],out["s1/2"],out["s2"])
    rows.append(out)
    print(f"{pid} {t[:34]:34s} x0.5 {out['s1/2']:.3f}  x1 {sc0:.3f}  x2 {out['s2']:.3f}  swing {out['swing']:.3f}  audio(x0.5) {out['audio1/2']}  audio(x2) {out['audio2']}  tempos {ntemp}",flush=True)
json.dump(rows,open("c4_renotate.json","w"),default=str,indent=0)
ex=[r for r in rows if r["exact1/2"] and r["exact2"]]
nr=[r for r in rows if r["near1/2"] and r["near2"]]
for lab,R in (("all",rows),("exact audio (all onsets/offsets <5ms)",ex),("near (>=95% onsets <25ms)",nr)):
    if R: print(f"{lab}: n={len(R)} median swing {st.median(r['swing'] for r in R):.3f} max {max(r['swing'] for r in R):.3f}")
