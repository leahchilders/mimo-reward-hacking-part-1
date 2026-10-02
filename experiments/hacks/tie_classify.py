"""Own minimal ABC tie analyser. For every tie in the gated real pieces' ABC, find the next
musical event in the same voice and classify the tie against ABC 2.1 section 4.11. Then ablate: delete
only the ties in a given class and see whether abc2midi's tie Errors disappear (attribution check)."""
import re, csv, os, json, collections
import hc

NOTE = re.compile(r"(\^\^|__|\^|_|=)?([A-Ga-g])([,']*)([0-9]*(?:/[0-9]*)*)(\.?-)?")
REST = re.compile(r"([zxZX])([0-9]*(?:/[0-9]*)*)(-)?")

def tokenize(abc):
    """yield (voice, kind, data, pos) over the body; pos = absolute char offset of the tie '-' if any."""
    lines = abc.split("\n"); off = 0; voice = "1"; in_body = False; out = []
    for line in lines:
        L = line
        if not in_body:
            if L.startswith("K:"): in_body = True
            off += len(line) + 1; continue
        if re.match(r"^[A-Za-z]:", L):
            m = re.match(r"^V:\s*(\S+)", L)
            if m: voice = m.group(1)
            off += len(line) + 1; continue
        if L.startswith("%"): off += len(line) + 1; continue
        i = 0
        while i < len(L):
            c = L[i]
            if c == "%": break
            if c == '"':
                j = L.find('"', i + 1); i = (j + 1) if j >= 0 else len(L); continue
            if c == "!":
                j = L.find("!", i + 1); i = (j + 1) if j >= 0 else len(L); continue
            if c == "[" and i + 2 < len(L) and L[i+1].isalpha() and L[i+2] == ":":
                j = L.find("]", i); fld = L[i+1:j]
                if fld.startswith("V:"): voice = fld[2:].strip().split()[0]
                i = j + 1; continue
            if c == "[" and i + 1 < len(L) and L[i+1].isdigit():
                out.append((voice, "bar", None, off + i)); i += 2; continue
            if c == "{":
                j = L.find("}", i); out.append((voice, "grace", L[i:j+1], off + i)); i = j + 1; continue
            if c == "[":
                j = L.find("]", i); inner = L[i+1:j]; k = j + 1
                m = re.match(r"[0-9]*(?:/[0-9]*)*", L[k:]); k += m.end()
                ctie = L[k:k+1] == "-"
                notes = []
                for mm in NOTE.finditer(re.sub(r"![^!]*!", "", inner)):
                    notes.append((mm.group(1) or "", mm.group(2), mm.group(3), bool(mm.group(5))))
                out.append((voice, "chord", dict(notes=notes, ctie=ctie), off + i)); i = k + (1 if ctie else 0); continue
            if c in "|:":
                out.append((voice, "bar", None, off + i)); i += 1; continue
            if c == "&":
                out.append((voice, "overlay", None, off + i)); i += 1; continue
            m = REST.match(L, i)
            if m and c in "zxZX":
                out.append((voice, "rest", c, off + i)); i = m.end(); continue
            m = NOTE.match(L, i)
            if m:
                out.append((voice, "note", (m.group(1) or "", m.group(2), m.group(3), bool(m.group(5))), off + i)); i = m.end(); continue
            i += 1
        off += len(line) + 1
    return out

def classify(abc):
    toks = tokenize(abc)
    byv = collections.defaultdict(list)
    for t in toks: byv[t[0]].append(t)
    res = []
    for v, ts in byv.items():
        acc = {}
        def eff(n):  # effective accidental in bar ('' = key default)
            a, l, o = n[0], n[1], n[2]
            if a: acc[(l, o)] = a
            return acc.get((l, o), "")
        resolved = []
        for idx, (vv, kind, data, pos) in enumerate(ts):
            if kind == "bar": acc.clear(); continue
            if kind == "note":
                cur = [(data[1], data[2], eff(data), data[3])]; chordtie = data[3]; is_chord = False
            elif kind == "chord":
                cur = [(n[1], n[2], eff(n), n[3] or data["ctie"]) for n in data["notes"]]; chordtie = data["ctie"]; is_chord = True
            else: continue
            tied = [c for c in cur if c[3]]
            if not tied: continue
            # look ahead for next sounding event in this voice (accidental state continues until a bar)
            nxt = None; crossed_bar = False; saw_overlay = False
            for (_, k2, d2, p2) in ts[idx+1:]:
                if k2 == "bar": crossed_bar = True; continue
                if k2 == "overlay": saw_overlay = True; continue
                nxt = (k2, d2); break
            if saw_overlay: cls = "tie_before_overlay(&)"
            elif nxt is None: cls = "tie_at_end_of_voice"
            elif nxt[0] == "rest": cls = "tie_to_rest_or_spacer" if nxt[1] in "zZ" else "tie_to_invisible_spacer_x"
            elif nxt[0] == "grace": cls = "tie_then_grace_note"
            else:
                tgt = [nxt[1]] if nxt[0] == "note" else nxt[1]["notes"]
                tgt_lo = {(n[1], n[2]) for n in tgt}
                missing = [c for c in tied if (c[0], c[1]) not in tgt_lo]
                if not missing: cls = "ok_same_pitch"
                elif is_chord and chordtie and len(missing) < len(tied): cls = "partial_chord_tie"
                elif any(n[1].lower() == c[0].lower() for c in missing for n in tgt): cls = "tie_to_other_octave"
                else: cls = "tie_to_different_pitch"
            res.append(dict(voice=v, pos=pos, cls=cls, chordtie=chordtie and is_chord))
    return res

VALIDITY = {"ok_same_pitch": "valid (4.11)", "tie_then_grace_note": "valid (4.11+4.20: grace precedes the note)",
            "partial_chord_tie": "spec-undefined (4.11: tie joins notes of the same pitch)",
            "tie_to_rest_or_spacer": "invalid (4.11)", "tie_to_invisible_spacer_x": "invalid (4.11)",
            "tie_to_different_pitch": "invalid (4.11)", "tie_to_other_octave": "invalid (4.11)",
            "tie_before_overlay(&)": "spec-undefined (7.4)", "tie_at_end_of_voice": "invalid (dangling)"}

def drop_ties(abc, positions):
    s = list(abc)
    for p in positions:
        # find the '-' belonging to the event starting at p
        j = p
        while j < len(s) and s[j] != "-" and s[j] != "\n": j += 1
        if j < len(s) and s[j] == "-": s[j] = ""
    return "".join(s)

def tie_errs(log):
    return len(re.findall(r"^Error.*(tied|before tie|Bad tie)", log, re.M))

if __name__ == "__main__":
    rows = list(csv.DictReader(open(os.path.join(os.path.dirname(hc.HERE), "abc_route", "per_piece.csv"))))
    report = []; agg = collections.Counter(); summary = []
    for r in rows:
        a = hc.load_norm(r["id"]); d = hc.diag(a)
        te = tie_errs(d["log"])
        cl = classify(a)
        cnt = collections.Counter(c["cls"] for c in cl)
        if te == 0:
            for k, v in cnt.items(): agg[("clean", k)] += v
            continue
        for k, v in cnt.items(): agg[("tie_err", k)] += v
        bad = [c["pos"] for c in cl if c["cls"] not in ("ok_same_pitch", "tie_then_grace_note")]
        d2 = hc.diag(drop_ties(a, bad)); te2 = tie_errs(d2["log"])
        grace = [c["pos"] for c in cl if c["cls"] == "tie_then_grace_note"]
        d3 = hc.diag(drop_ties(a, bad + grace)); te3 = tie_errs(d3["log"])
        summary.append(dict(id=r["id"], title=r["title"][:40], tie_errors=te, classes=dict(cnt),
                            tie_errors_after_dropping_invalid_or_undefined=te2,
                            tie_errors_after_also_dropping_grace=te3,
                            reward_after_drop=d2["reward"], other_errors_after=d2["err"] - te2, bar_after=d2["bar"]))
    out = ["Tie classes (all ties, by whether the piece has abc2midi tie Errors):"]
    for (g, k), v in sorted(agg.items()): out.append(f"  {g:8s} {k:28s} {v:6d}   [{VALIDITY[k]}]")
    out.append("\nPieces with tie Errors (n=%d):" % len(summary))
    for s in summary:
        cls = {k: v for k, v in s["classes"].items() if k != "ok_same_pitch"}
        out.append(f"  {s['id']} {s['title']:40s} tieErr={s['tie_errors']:3d} -> after dropping invalid/undefined ties: {s['tie_errors_after_dropping_invalid_or_undefined']:3d} (+grace: {s['tie_errors_after_also_dropping_grace']}); reward after={s['reward_after_drop']:.3f} other_err={s['other_errors_after']} bar={s['bar_after']}  non-ok ties: {cls}")
    open("tie_classify.txt", "w").write("\n".join(out) + "\n"); json.dump(summary, open("tie_classify.json", "w"), indent=1)
    print("\n".join(out))
