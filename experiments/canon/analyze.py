"""Merge canon_list.csv + results.jsonl -> per_piece.csv and tables_auto.md.

Point-loss attribution (exact decomposition of 100 - total):
  total = 100*(0.85*base + 0.15*dist_s), base = sum_g W_g * mean_{f in g} s_f  (sum W = 1.0)
  loss_f = 85 * W_g * (1 - s_f) / n_g ;  loss_dist = 15 * (1 - dist_s)
  sum(loss_f) + loss_dist == 100 - total  (up to rounding)
Direction for a penalized feature: 'low' if value < p10 (band) / < p75 (high-kind), 'high' if > p90 (band) / > p25 (low-kind).
"""
import json, os, sys, statistics as st, re
import pandas as pd
import numpy as np

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "common"))
import config  # sets ABC2MIDI_BIN, aliases the upstream scorer as `music_scorer`
from music_scorer.score import SPEC, W
REF = json.load(open(config.REF_PATH))
GN = {g: sum(1 for _, _, gg in SPEC if gg == g) for g in W}
KIND = {f: k for f, k, _ in SPEC}
GRP = {f: g for f, _, g in SPEC}

c = pd.read_csv(D + "/canon_list.csv")
res = [json.loads(l) for l in open(D + "/results.jsonl")]
r = pd.DataFrame(res).drop(columns=["path"], errors="ignore")
df = c.merge(r, on="cid", how="left")


def md(d, index=True):
    d = d.reset_index() if index else d
    cols = [str(c) for c in d.columns]
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for row in d.itertuples(index=False):
        out.append("| " + " | ".join(str(v).replace("|", "/") for v in row) + " |")
    return "\n".join(out)


def direction(f, x):
    if x is None or (isinstance(x, float) and np.isnan(x)): return ""
    rf = REF[f]; k = KIND[f]
    if k == "band": return "low" if x < rf["p10"] else ("high" if x > rf["p90"] else "")
    if k == "high": return "low" if x < rf["p75"] else ""
    return "high" if x > rf["p25"] else ("very-low" if x < rf["p05"] else "")


rows = []
for _, x in df.iterrows():
    o = {}
    pf = x.get("per_feature"); ft = x.get("feat")
    if isinstance(pf, dict):
        losses = {f: 85 * W[GRP[f]] * (1 - s) / GN[GRP[f]] for f, s in pf.items()}
        losses["dist_hist(JS)"] = 15 * (1 - x["dist_score"] / 100)
        for f, l in losses.items(): o["loss_" + f] = round(l, 2)
        top = sorted(losses.items(), key=lambda kv: -kv[1])
        o["top_losses"] = "; ".join(
            f"{f}{'(' + direction(f, ft.get(f)) + ' ' + str(ft.get(f)) + ')' if f in KIND else ''} -{l:.1f}"
            for f, l in top[:5] if l >= 0.5)
        for g, v in x["groups"].items(): o["grp_" + g] = v
        o["dist_score"] = x["dist_score"]
    if isinstance(ft, dict):
        for k, v in ft.items(): o["f_" + k] = v
    rows.append(o)
df = pd.concat([df.drop(columns=["per_feature", "feat", "groups", "dist_score"], errors="ignore"), pd.DataFrame(rows)], axis=1)

flags = df["flags"].fillna("")
df["group"] = np.where(df.source == "music21", np.where(flags.str.contains("chorale"), "m21_bach_chorales", "m21_keyboard"),
                       np.where(flags.str.contains("arr/excerpt|multi_composer|orch/vocal"), "pdmx_flagged", "pdmx_canon"))
df["scored"] = df.status == "ok"
df["passed"] = df.scored & (df.gates.fillna("") == "")
df["zeroed"] = df.scored & ~df.passed
# article cleanliness: PD composer by life+70 (died <1956); US: 20th-c works need pub<1931 (manual check flagged)
df["pd_composer_life70"] = df.composer_death < 1956
df["needs_pubdate_check"] = df.composer_death > 1930
lc = df.license_conflict.astype(str).str.lower().isin(["false", "0"])
df["article_clean"] = (df.group == "pdmx_canon") & df.pd_composer_life70 & lc & ~flags.str.contains("composer_from_title")
df.to_csv(D + "/per_piece_full.csv", index=False)

keep = ["cid", "group", "source", "composer", "era", "composer_death", "title", "composer_name_raw", "pdmx_rel", "license",
        "license_conflict", "rating", "n_ratings", "keyboard_src", "flags", "status", "reward", "quality_ungated", "gates",
        "err", "bar_warn", "first_errors", "n_chan", "abc_bars", "abc_voices", "pdmx_bars", "f_n_note", "f_dur_sec", "top_losses",
        "grp_rhythm", "grp_texture", "grp_acoustic", "grp_tonal", "grp_register", "grp_structure", "dist_score",
        "article_clean", "needs_pubdate_check", "t_total", "wall"] + [k for k in df.columns if k.startswith("f_") and k not in ("f_n_note", "f_dur_sec")] \
       + [k for k in df.columns if k.startswith("loss_")]
df[[k for k in keep if k in df.columns]].to_csv(D + "/per_piece.csv", index=False)

# ---------------- tables ----------------
L = []
P = lambda *a: L.append(" ".join(str(x) for x in a))
P("# auto tables\n")
P("status counts:", df.groupby(["group", "status"]).size().to_dict())
P("\nwall per piece (s): median", round(df.wall.median(), 2), "p90", round(df.wall.quantile(.9), 2), "max", df.wall.max(),
  "sum", round(df.wall.sum()), "\n")


def q(s, p): return round(float(s.quantile(p)), 3) if len(s) else float("nan")


def summ(g):
    sc = g[g.scored]; ps = sc[sc.passed]
    return pd.Series(dict(n=len(g), scored=len(sc), zeroed=int(sc.zeroed.sum()),
                          zeroed_pct=round(100 * sc.zeroed.mean(), 0) if len(sc) else np.nan,
                          med_reward_all=q(sc.reward, .5),
                          med_pass=q(ps.reward, .5), iqr_pass=f"{q(ps.reward, .25)}-{q(ps.reward, .75)}", min_pass=q(ps.reward, 0),
                          med_ungated=q(sc.quality_ungated.dropna() / 100, .5)))


for gname in ["pdmx_canon", "pdmx_flagged", "m21_keyboard", "m21_bach_chorales"]:
    P(f"\n## group {gname}\n"); P(md(summ(df[df.group == gname]).to_frame().T, index=False))
canon = df[df.group == "pdmx_canon"]
P("\n## pdmx_canon by era\n"); P(md(canon.groupby("era").apply(summ).sort_values("med_pass")))
P("\n## pdmx_canon by composer (n>=3)\n")
bc = canon.groupby("composer").apply(summ); P(md(bc[bc.n >= 3].sort_values("med_pass")))

# lowest passing
ps = df[df.passed & df.group.isin(["pdmx_canon", "m21_keyboard"])].sort_values("reward")
P("\n## lowest 40 passing (pdmx_canon + m21_keyboard)\n")
P(md(ps.head(40)[["cid", "reward", "composer", "title", "license", "license_conflict", "article_clean", "f_n_note", "top_losses"]], index=False))
P("\n## zeroed canon, highest ungated (30)\n")
z = df[df.zeroed & (df.group == "pdmx_canon")].sort_values("quality_ungated", ascending=False)
P(md(z.head(30)[["cid", "quality_ungated", "composer", "title", "gates", "first_errors", "article_clean"]], index=False))
P("\n## gate reasons among zeroed pdmx_canon\n")
gr = z.gates.str.replace(r" x\d+", "", regex=True)
P(md(gr.value_counts()))
# feature blame over passing canon
lc_cols = [k for k in df.columns if k.startswith("loss_")]
pc = df[df.passed & (df.group == "pdmx_canon")]
fb = pd.DataFrame({"mean_pts_lost": pc[lc_cols].mean().round(2), "pct_pieces_losing>=1pt": (100 * (pc[lc_cols] >= 1).mean()).round(0)})
dirs = {}
for f in KIND:
    d = pc.apply(lambda x: direction(f, x.get("f_" + f)), axis=1)
    dirs["loss_" + f] = d.value_counts().to_dict()
fb["direction_counts"] = [str({k: v for k, v in dirs.get(i, {}).items() if k}) for i in fb.index]
P(f"\n## feature blame, passing pdmx_canon (n={len(pc)}); total mean loss {round(100 - pc.quality_ungated.mean(), 2)}\n")
P(md(fb.sort_values("mean_pts_lost", ascending=False)))
low = pc[pc.reward < pc.reward.quantile(.1)]
fb2 = low[lc_cols].mean().round(2).sort_values(ascending=False)
P(f"\n## feature blame, bottom decile of passing pdmx_canon (n={len(low)}, reward < {round(pc.reward.quantile(.1), 3)})\n")
P(md(fb2.to_frame("mean_pts_lost")))
# length effect
sc = df[df.scored & (df.group == "pdmx_canon")]
P("\n## length effects (pdmx_canon scored)\n")
P("spearman(n_note, ungated)", round(sc[["f_n_note", "quality_ungated"]].corr("spearman").iloc[0, 1], 3))
P("spearman(n_note, f_tension_peaks)", round(sc[["f_n_note", "f_tension_peaks"]].corr("spearman").iloc[0, 1], 3))
P("pct with tension_peaks > p90 (96):", round(100 * (sc.f_tension_peaks > REF['tension_peaks']['p90']).mean(), 1))
P("zeroed% by n_note quartile:", sc.groupby(pd.qcut(sc.f_n_note, 4)).zeroed.mean().round(2).to_dict())
P("median ungated by n_note quartile:", sc.groupby(pd.qcut(sc.f_n_note, 4)).quality_ungated.median().to_dict())
P("n_chan distribution:", sc.n_chan.value_counts().to_dict())
open(D + "/tables_auto.md", "w").write("\n".join(L))
print("\n".join(L))
