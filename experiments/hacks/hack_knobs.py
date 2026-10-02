"""Note-level knobs that need bar-level edits, applied to the 8 own climbed hacks and to
20 unclimbed random 3-voice pieces (degen 'random16', seeds 0-19). V:1 = melody voice."""
import re, random, json, glob, statistics as st
from multiprocessing import Pool
import hc, degen

NOTE = r"(?<![\w'!,\[])(\.?)(\^|_|=)?([A-Ga-g][,']*)(\d*)"
def edit_v1(abc, fn):
    ls = abc.split("\n"); i = next(i for i, l in enumerate(ls) if l.startswith("V:1")) + 1
    ls[i] = fn(ls[i]); return "\n".join(ls)
def edit_all(abc, fn):
    ls = abc.split("\n")
    for i, l in enumerate(ls):
        if l.endswith("|]") and not l.startswith("V:"): ls[i] = fn(l)
    return "\n".join(ls)
def per_note(line, f, p, seed=0):
    rng = random.Random(seed)
    def r(m):
        return f(m) if rng.random() < p else m.group(0)
    # do not touch notes inside chords
    parts = re.split(r"(\[[^\]]*\])", line)
    return "".join(x if x.startswith("[") else re.sub(NOTE, r, x) for x in parts)
def up8(n):
    return n.lower() if n[0].isupper() and "," not in n else (n + "'" if n[0].islower() else n.replace(",", "", 1))

def tie_split(m):
    st_, acc, n, d = m.groups(); d = int(d) if d else 1
    if d < 2 or st_: return m.group(0)   # staccato+tie ('.c-c') is a separate breaker, see breakers.py
    a = d // 2; b = d - a
    return f"{st_}{acc or ''}{n}{a if a > 1 else ''}-{n}{b if b > 1 else ''}"
def rep_split(m):
    st_, acc, n, d = m.groups(); d = int(d) if d else 1
    if d < 2 or st_: return m.group(0)
    a = d // 2; b = d - a
    return f"{st_}{acc or ''}{n}{a if a > 1 else ''} {n}{b if b > 1 else ''}"

KN = {
    "grace note before 25% of melody notes": lambda a: edit_v1(a, lambda l: per_note(l, lambda m: "{g}" + m.group(0), 0.25)),
    "!trill! on 25% of melody notes":        lambda a: edit_v1(a, lambda l: per_note(l, lambda m: "!trill!" + m.group(0), 0.25)),
    "!>! accent on every melody note":       lambda a: edit_v1(a, lambda l: per_note(l, lambda m: "!>!" + m.group(0), 1.0)),
    "staccato on every note (all voices)":   lambda a: edit_all(a, lambda l: per_note(l.replace(".[", "["), lambda m: "." + m.group(0).lstrip("."), 1.0)),
    "remove all staccato":                   lambda a: a.replace(" .", " ").replace("|.", "|"),
    "melody octave-doubled":                 lambda a: edit_v1(a, lambda l: per_note(l, lambda m: f"{m.group(1)}[{(m.group(2) or '')}{m.group(3)}{(m.group(2) or '')}{up8(m.group(3))}]{m.group(4)}", 1.0)),
    "non-staccato long notes -> tied halves (same audio)":lambda a: edit_all(a, lambda l: per_note(l, tie_split, 1.0)),
    "non-staccato long notes -> repeated halves":         lambda a: edit_all(a, lambda l: per_note(l, rep_split, 1.0)),
    "one chromatic note (first melody note sharpened)": lambda a: edit_v1(a, lambda l: re.sub(NOTE, lambda m: f"{m.group(1)}^{m.group(3)}{m.group(4)}", l, count=1)),
    "whole piece inside |: :| (played twice)": lambda a: edit_all(a, lambda l: "|: " + l[:-2].rstrip().rstrip("|") + " :|"),
    "guitar chords C-F-G7-C on melody bars": lambda a: edit_v1(a, lambda l: " | ".join(f'"{["C","F","G7","C"][i%4]}"' + b.strip() for i, b in enumerate(l[:-2].split(" | "))) + " |]"),
    "dynamics !p!/!f! alternating per bar (all voices)": lambda a: edit_all(a, lambda l: " | ".join(("!p!" if i % 2 else "!f!") + b.strip() for i, b in enumerate(l[:-2].split(" | "))) + " |]"),
    "lyrics w: under melody":                lambda a: a.replace("\nV:2", "\nw: la la la la la la la la la la la la\nV:2", 1),
}

def job(args):
    kind, pid, abc = args
    b = hc.reward(abc); out = []
    for k, f in KN.items():
        a2 = f(abc); d = hc.diag(a2)
        out.append(dict(kind=kind, pid=pid, knob=k, base=b, reward=d["reward"], err=d["err"], bar=d["bar"],
                        msg=hc.errlines(d["log"], 1) if d["reward"] == 0 else []))
    return out

if __name__ == "__main__":
    P = [("hack", p.split("/")[-1][:-4], open(p).read().rstrip()) for p in sorted(glob.glob("pieces/climb_s*_b16.abc"))]
    P += [("random", f"r{s}", degen.gen(s, "random16")) for s in range(20)]
    with Pool(18) as pool: rows = [r for rs in pool.map(job, P) for r in rs]
    json.dump(rows, open("hack_knobs.json", "w"), indent=1)
    L = ["| knob | climbed hacks (n=8): median Δ, up/down/zeroed | unclimbed random (n=20): median Δ, up/down/zeroed |", "|---|---|---|"]
    for k in KN:
        c = []
        for kind in ("hack", "random"):
            rs = [r for r in rows if r["knob"] == k and r["kind"] == kind]; ds = [r["reward"] - r["base"] for r in rs]
            c.append(f"{st.median(ds):+.3f}, {sum(x>5e-4 for x in ds)}/{sum(x<-5e-4 for x in ds)}/{sum(r['reward']==0 for r in rs)}")
        L.append(f"| {k} | " + " | ".join(c) + " |")
    open("hack_knobs_summary.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
    for r in rows:
        if r["reward"] == 0: print("ZERO", r["pid"], r["knob"], r["msg"]); break
