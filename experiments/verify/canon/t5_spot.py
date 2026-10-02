import os, sys, json, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vc
d = pd.read_csv(os.path.join(vc.HERE, "..", "canon", "per_piece.csv"))
d = d[(d.status == "ok") & d.pdmx_rel.notna() & ~d.pdmx_rel.str.startswith("m21:")]
s = d.sample(20, random_state=20260930)
def run(row):
    abc = vc.norm(vc.xml2abc(os.path.join(vc.PDMX, row["pdmx_rel"]))[0])
    rw, r = vc.score_abc(abc)
    return dict(cid=row["cid"], title=str(row["title"])[:40], theirs=row["reward"], mine=round(rw, 4),
                their_ung=row["quality_ungated"], my_ung=r.get("total"), err=(row["err"], r.get("err")), bar=(row["bar_warn"], r.get("bar")))
with Pool(10) as p:
    res = p.map(run, [r for _, r in s.iterrows()])
for x in res: print(json.dumps(x, ensure_ascii=False))
print("exact reward matches:", sum(abs(x["theirs"] - x["mine"]) < 1e-3 for x in res), "/", len(res))
c = pd.read_csv(os.path.join(vc.HERE, "..", "canon", "per_piece.csv"))
c = c[(c.group == "pdmx_canon") & (c.status == "ok")]
print("polyphony_rate==0: all canon", (c.f_polyphony_rate == 0).mean(), " passing", (c[c.reward > 0].f_polyphony_rate == 0).sum(), "of", (c.reward > 0).sum())
pas = c[c.reward > 0]
print("passing with loss_polyphony_rate>=1 and f_poly<0.666:", ((pas.loss_polyphony_rate >= 1) & (pas.f_polyphony_rate < 0.666)).sum(), " and >0.666:", ((pas.loss_polyphony_rate >= 1) & (pas.f_polyphony_rate > 0.666)).sum())
