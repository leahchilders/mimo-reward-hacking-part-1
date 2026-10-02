import os, pandas as pd, numpy as np
d = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "canon", "per_piece.csv"))
print(d.status.value_counts().to_dict())
for g, x in d.groupby("group"):
    s = x[x.status == "ok"]
    z = (s.reward == 0)
    p = s[~z]
    print(f"{g:20s} n_ok={len(s)} zeroed={z.sum()} ({z.mean():.1%}) med_all={s.reward.median():.3f} "
          f"med_pass={p.reward.median():.3f} IQR=({p.reward.quantile(.25):.3f},{p.reward.quantile(.75):.3f}) "
          f"med_ungated={(s.quality_ungated/100).median():.3f}")
c = d[(d.group == "pdmx_canon") & (d.status == "ok")]
z = c[c.reward == 0]
print("zeroed pdmx_canon gate composition: err>0", (z.err > 0).sum(), " bar>=10 & err==0", ((z.err == 0) & (z.bar_warn >= 10)).sum(),
      " other", ((z.err == 0) & (z.bar_warn < 10)).sum())
print("median ungated zeroed vs pass:", (z.quality_ungated/100).median(), (c[c.reward > 0].quality_ungated/100).median())
print("polyphony_rate==0 among passing canon:", (c[c.reward > 0].f_polyphony_rate == 0).mean())
