"""ABC building blocks for search.py and climb.py: diatonic pitch pools, random-walk bars, header, voice assembly."""
import random
NOTES_C = "C D E F G A B".split()
def pname(midi):
    # diatonic-only name for C major (midi assumed in C major scale), ABC octave rules
    pc = {0:"C",2:"D",4:"E",5:"F",7:"G",9:"A",11:"B",1:"^C",3:"^D",6:"^F",8:"^G",10:"^A"}[midi%12]
    octv = midi//12 - 1  # C4=60 -> 4
    acc = pc[:-1]; L = pc[-1]
    if octv >= 5:
        s = acc + L.lower() + "'"*(octv-5)
    else:
        s = acc + L + ","*(4-octv)
    return s
def dur(n):  # n eighths with L:1/8
    return "" if n==1 else str(n)
CMAJ=[0,2,4,5,7,9,11]
def diatonic(lo,hi,scale=CMAJ,root=0):
    return [p for p in range(lo,hi+1) if (p-root)%12 in scale]

def header(meter="4/4",key="C",bpm=100,title="t",nvoice=2,programs=None):
    h=[f"X:1",f"T:{title}",f"M:{meter}","L:1/8",f"Q:1/4={bpm}"]
    for v in range(1,nvoice+1):
        clef="treble" if v==1 else "bass"
        h.append(f"V:{v} clef={clef}")
        if programs: h.append(f"%%MIDI program {programs[v-1]}")
    h.append(f"K:{key}")
    return h

def assemble(h, voices_bars, bars_per_line=4):
    out=list(h)
    nb=len(voices_bars[0])
    for b0 in range(0,nb,bars_per_line):
        for v,bars in enumerate(voices_bars):
            out.append(f"[V:{v+1}] "+" | ".join(bars[b0:b0+bars_per_line])+" |")
    return "\n".join(out)

def rand_bar(rng, pool, beat8=8, durs=(1,1,2,2,3,4), walk=None, step=2, chord_p=0.0, rest_p=0.0):
    left=beat8; toks=[]; cur=walk[0] if walk else rng.choice(pool)
    while left>0:
        d=min(rng.choice(durs),left)
        if rng.random()<rest_p: toks.append("z"+dur(d)); left-=d; continue
        i=pool.index(cur) if cur in pool else rng.randrange(len(pool))
        i=max(0,min(len(pool)-1,i+rng.randint(-step,step))); cur=pool[i]
        if rng.random()<chord_p:
            j=min(len(pool)-1,i+2); k=min(len(pool)-1,i+4)
            toks.append("["+pname(pool[i])+pname(pool[j])+pname(pool[k])+"]"+dur(d))
        else:
            toks.append(pname(cur)+dur(d))
        left-=d
    if walk: walk[0]=cur
    return " ".join(toks)

def random_walk_piece(seed, nbars=64, p=None):
    p=p or {}
    rng=random.Random(seed)
    rh_pool=diatonic(p.get("rh_lo",60),p.get("rh_hi",84))
    lh_pool=diatonic(p.get("lh_lo",36),p.get("lh_hi",59))
    wr=[rh_pool[len(rh_pool)//2]]; wl=[lh_pool[len(lh_pool)//2]]
    rh=[rand_bar(rng,rh_pool,durs=p.get("rh_durs",(1,1,2,2,3,4)),walk=wr,step=p.get("step",2)) for _ in range(nbars)]
    lh=[rand_bar(rng,lh_pool,durs=p.get("lh_durs",(2,4,8)),walk=wl,step=p.get("lstep",3),chord_p=p.get("chord_p",0.3)) for _ in range(nbars)]
    return assemble(header(bpm=p.get("bpm",100),title="random walk"),[rh,lh])
