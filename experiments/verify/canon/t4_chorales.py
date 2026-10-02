import os, sys, re, random, json, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vc
import music21
cdir = os.path.join(os.path.dirname(music21.__file__), "corpus", "bach")
files = sorted(f for f in os.listdir(cdir) if f.startswith("bwv") and f.endswith(".mxl"))
print("chorale mxl files in corpus:", len(files))
random.seed(930)
pick = random.sample(files, 30)
rows = []
for f in pick:
    abc = vc.norm(vc.xml2abc(os.path.join(cdir, f))[0])
    nf = abc.count("!fermata!") + len(re.findall(r"(?<![A-Za-z!\"])H(?=[\[A-Ga-gz^_=])", abc))
    rw, r = vc.score_abc(abc)
    nofer = re.sub(r"!fermata!", "", abc)
    rw2, r2 = vc.score_abc(nofer)
    # also: same ABC, abc2midi told to keep fermata notes at written length via -NFER-equivalent? (scorer allows no flags) -> skip
    rows.append(dict(f=f, n_fermata=nf, reward=rw, err=r.get("err"), bar=r.get("bar"), total=r.get("total"),
                     reward_nofer=rw2, err_nofer=r2.get("err"), bar_nofer=r2.get("bar"), total_nofer=r2.get("total")))
    print(json.dumps(rows[-1]), flush=True)
z = [x for x in rows if x["reward"] == 0]
print("zeroed", len(z), "/", len(rows))
print("zeroed by bar-warn only:", sum(1 for x in z if x["err"] == 0 and x["bar"] >= 10))
print("median bar warnings before/after:", st.median(x["bar"] for x in rows), st.median(x["bar_nofer"] for x in rows))
print("of zeroed, pass after fermata removal:", sum(1 for x in z if x["reward_nofer"] > 0))
json.dump(rows, open(os.path.join(vc.HERE, "work", "t4.json"), "w"), indent=1)
