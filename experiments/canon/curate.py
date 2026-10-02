"""Hand-curated 'acclaimed but low' shortlist (passing the gates) + key zeroed exemplars, with scorer breakdown,
grid-phase counterfactual and fidelity spot-check joined in. Selection was made by reading the lowest-passing list
(tables_auto.md) and keeping recognised, complete concert/teaching-canon works; generic hymn tunes, single-line
excerpts, vocal/instrumental parts, textbook examples and 'arrangements' were skipped."""
import pandas as pd, json, os
D = os.path.dirname(os.path.abspath(__file__))
LOW = ["C1184", "C0960", "C0599", "C1049", "C1052", "C0371", "C0893", "C1179", "C1061", "C0894", "C1089", "C0544",
       "C0095", "C0534", "C2222", "C1142", "C0501", "C0515", "C0577", "C0254", "C0406", "C2223", "C0329"]
pp = pd.read_csv(D + "/per_piece_full.csv", low_memory=False)
cf = pd.read_csv(D + "/cf_grid_phase.csv")
fid = pd.DataFrame([json.loads(l) for l in open(D + "/fidelity_spotcheck.jsonl")])
m = pp.merge(cf[["key", "shift_total", "orig_polyphony_rate", "shift_polyphony_rate"]], left_on="cid", right_on="key", how="left") \
      .merge(fid[["cid", "n_src", "n_abc_midi", "onset_pitch_F1", "pitch_multiset_overlap"]], on="cid", how="left")
cols = ["cid", "reward", "shift_total", "composer", "composer_death", "title", "license", "license_conflict", "article_clean",
        "needs_pubdate_check", "pdmx_rel", "f_n_note", "n_chan", "orig_polyphony_rate", "shift_polyphony_rate",
        "grp_rhythm", "grp_texture", "grp_acoustic", "grp_tonal", "grp_register", "grp_structure", "dist_score",
        "top_losses", "n_src", "n_abc_midi", "onset_pitch_F1", "pitch_multiset_overlap"]
c = m[m.cid.isin(LOW)][cols].sort_values("reward")
c.to_csv(D + "/curated_low.csv", index=False)
pd.set_option("display.width", 300); pd.set_option("display.max_colwidth", 200)
print(c.to_string())
