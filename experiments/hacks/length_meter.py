"""Length dependence and meter dependence, on the ABC path."""
import re, csv, os, json, random, statistics as st
from multiprocessing import Pool
import hc, degen, knobs

# ---------- length ----------
def rand_n(args):
    seed, nb = args
    rng = random.Random(seed)
    vb = [[degen.render_bar(degen.rbar(rng, degen.LAD[degen.VO[v][0]], degen.VO[v][2], 0.5), degen.LAD[degen.VO[v][0]]) for _ in range(nb)] for v in range(3)]
    d = hc.diag(degen.piece(vb, 3))
    return nb, seed, d["reward"], d["feat"]["tension_peaks"], d["per"]["tension_peaks"], d["per"]["self_similarity"]

def loop_hack(args):
    reps, = args
    a = open("pieces/climb_s2_st1_b16.abc").read()
    ls = a.split("\n"); out = []
    for l in ls:
        if l.endswith("|]") and not l.startswith("V:"):
            body = l[:-2].rstrip().rstrip("|").strip()
            l = " | ".join([body] * reps) + " |]"
        out.append(l)
    d = hc.diag("\n".join(out))
    return reps, d["reward"], d["feat"]["tension_peaks"], d["per"]["tension_peaks"], d["per"]["self_similarity"], d["total"]

# ---------- meter ----------
def relabel(abc, to="4/4"):
    a = re.sub(r"^M:\s*\S+", f"M:{to}", abc, flags=re.M)
    return re.sub(r"\[M:[^\]]*\]", f"[M:{to}]", a)

def strip_vel(notes):
    return sorted((o, d, ch, p) for o, d, ch, p, v in notes)

def real_meter(pid):
    a = hc.load_norm(pid); m = re.search(r"^M:\s*(\S+)", a, re.M).group(1)
    b = relabel(a)
    da, db = hc.diag(a), hc.diag(b)
    na = knobs.pervoice(a, ["%%MIDI nobeataccents"]); nb = knobs.pervoice(b, ["%%MIDI nobeataccents"])
    dna, dnb = hc.diag(na), hc.diag(nb)
    return dict(id=pid, meter=m, reward=da["reward"], relabeled_reward=db["reward"], relabeled_bar_warnings=db["bar"],
                total=da["total"], relabeled_total=db["total"], same_notes=strip_vel(da["notes"]) == strip_vel(db["notes"]),
                same_velocities=da["notes"] == db["notes"],
                total_noaccent=dna["total"], relabeled_total_noaccent=dnb["total"])

def rebar_stream(seed, unit_per_bar, total_units=240, nv=3):
    """identical event stream per voice, cut into bars of unit_per_bar eighths; notes crossing a barline are split with ties."""
    rng = random.Random(seed); voices = []
    for v in range(nv):
        lad = degen.LAD[degen.VO[v][0]]; ev = []; left = total_units
        while left:
            d = rng.choice([x for x in (1, 2, 3, 4) if x <= left]); left -= d
            n = rng.randrange(len(lad))
            ch = (n, min(len(lad) - 1, n + 2)) if rng.random() < degen.VO[v][2] else (n,)
            ev.append((ch, d))
        voices.append((lad, ev))
    out = []
    for lad, ev in voices:
        toks, pos = [], 0
        for ch, d in ev:
            ps = [lad[i] for i in ch]; nm = ps[0] if len(ps) == 1 else "[" + "".join(ps) + "]"
            while d:
                room = unit_per_bar - pos % unit_per_bar; take = min(d, room); d -= take
                toks.append(nm + (str(take) if take != 1 else "") + ("-" if d else "")); pos += take
                if pos % unit_per_bar == 0: toks.append("|")
        out.append(" ".join(toks)[:-1] + "|]")
    return out

METERS = {"4/4": 8, "3/4": 6, "6/8": 6, "2/4": 4, "5/4": 10, "12/8": 12}
def syn_meter(seed):
    r = {}
    base_notes = None
    for M, u in METERS.items():
        bodies = rebar_stream(seed, u)
        h = ["X:1", "T:t", f"M:{M}", "L:1/8", "Q:1/4=100", "K:C"]
        for v, b in enumerate(bodies): h += [f"V:{v+1} clef={degen.VO[v][1]}", b]
        a = "\n".join(h); d = hc.diag(a)
        an = knobs.pervoice(a, ["%%MIDI nobeataccents"]); dn = hc.diag(an)
        nn = strip_vel(d["notes"])
        if base_notes is None: base_notes = nn
        r[M] = dict(reward=d["reward"], err=d["err"], bar=d["bar"], reward_noaccent=dn["reward"], same_notes_as_4_4=(nn == base_notes))
    return seed, r

if __name__ == "__main__":
    out = {}
    with Pool(18) as p:
        L = p.map(rand_n, [(s, nb) for nb in (1, 2, 4, 8, 16, 32, 64, 128, 200) for s in range(30)])
        out["random_by_length"] = {nb: dict(n=30, median_reward=st.median(x[2] for x in L if x[0] == nb),
                                            median_tension_peaks=st.median(x[3] for x in L if x[0] == nb),
                                            median_tp_score=st.median(x[4] for x in L if x[0] == nb),
                                            median_selfsim_score=st.median(x[5] for x in L if x[0] == nb)) for nb in (1, 2, 4, 8, 16, 32, 64, 128, 200)}
        LH = p.map(loop_hack, [(r,) for r in (1, 2, 4, 8, 13)])
        out["hack_looped"] = [dict(bars=16 * r, reward=rw, tension_peaks=tp, tp_score=tps, selfsim_score=ss) for r, rw, tp, tps, ss, _ in LH]
        real = [r["id"] for r in csv.DictReader(open(os.path.join(os.path.dirname(hc.HERE), "abc_route", "per_piece.csv"))) if float(r["abc_norm"]) > 0]
        RM = p.map(real_meter, real)
        SM = p.map(syn_meter, range(30))
    # real-piece tension_peaks vs length
    tp = []
    for pid in real:
        d = hc.diag(hc.load_norm(pid)); tp.append((pid, d["feat"]["n_note"], d["feat"]["tension_peaks"], d["per"]["tension_peaks"], d["reward"]))
    n_note = [x[1] for x in tp]; peaks = [x[2] for x in tp]
    out["real_tension_peaks"] = dict(n=len(tp), pearson_nnote_peaks=round(st.correlation(n_note, peaks), 3),
                                    too_few_lt12=sum(x[2] < 12 for x in tp), too_many_gt96=sum(x[2] > 96 for x in tp),
                                    lose_points=sum(x[3] < 1 for x in tp), rows=tp)
    nf = [r for r in RM if r["meter"] != "4/4"]
    out["real_meter_relabel"] = dict(n_non44=len(nf), rows=RM,
        same_notes=sum(r["same_notes"] for r in nf), same_velocities=sum(r["same_velocities"] for r in nf),
        delta_total=[round((r["relabeled_total"] - r["total"]) / 100, 3) for r in nf],
        delta_total_noaccent=[round((r["relabeled_total_noaccent"] - r["total_noaccent"]) / 100, 3) for r in nf],
        zeroed_by_relabel=sum(r["relabeled_reward"] == 0 for r in nf))
    out["synthetic_rebar"] = dict(n=len(SM), rows={s: r for s, r in SM})
    summ = {}
    for M in METERS:
        dl = [r[M]["reward"] - r["4/4"]["reward"] for s, r in SM]
        dn = [r[M]["reward_noaccent"] - r["4/4"]["reward_noaccent"] for s, r in SM]
        summ[M] = dict(median_reward=st.median(r[M]["reward"] for s, r in SM), median_delta_vs_44=round(st.median(dl), 4),
                       max_abs_delta=round(max(abs(x) for x in dl), 4), max_abs_delta_noaccent=round(max(abs(x) for x in dn), 4),
                       same_notes=sum(r[M]["same_notes_as_4_4"] for s, r in SM), gated=sum(r[M]["reward"] == 0 for s, r in SM))
    out["synthetic_rebar_summary"] = summ
    json.dump(out, open("length_meter.json", "w"), indent=1)
    for k in ("random_by_length", "hack_looped", "synthetic_rebar_summary"): print(k, json.dumps(out[k], indent=0))
    rt = dict(out["real_tension_peaks"]); rt.pop("rows"); print(rt)
    rm = dict(out["real_meter_relabel"]); rm.pop("rows"); print(rm)
