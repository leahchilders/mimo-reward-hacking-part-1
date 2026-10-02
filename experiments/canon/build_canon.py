"""Build the 'canon' list: acclaimed keyboard works from PDMX (+ a few music21-corpus items).

Selection (PDMX):
  * piece is in a private corpus manifest as solo_grand_staff or multi_keyboard_split_grand
    (i.e. PDMX deduplicated subset, keyboard-only; any encoder outcome except skipped_duplicate)
  * composer matches a canon-composer regex (composer_name first; title/artist as fallback)
  * flags (not exclusions): arrangement/excerpt/easy/transcription keywords, multi-composer match
  * work-level dedup: key = composer + catalog tokens (BWV/K/Op/No/D/Hob/WoO/L/S/Sz/Mvt) or
    normalized title; keep best (unflagged first, then rating*n_ratings, favorites, views)
music21 corpus: all Bach chorales (4-voice, separate group) + keyboard items bwv846,
Schoenberg Op.19/2,/6, Chopin mazurka Op.6/2 (kern), Joplin Maple Leaf, Clara Schumann polonaises.
Writes canon_list.csv.
"""
import re, json, csv, sys, os
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "common"))
import config  # sets ABC2MIDI_BIN, aliases the upstream scorer as `music_scorer`

OUT = os.path.dirname(os.path.abspath(__file__))
# A private corpus manifest (keyboard category per PDMX file). Not public; without it every candidate
# goes through the MusicXML peek below, so the list will differ from the shipped canon_list.csv.
MANIFEST = os.environ.get("CANON_MANIFEST", "")

# (label, era, death_year, regex)  -- regex applied case-insensitively
COMPOSERS = [
    ("Bach, J.S.", "Baroque", 1750, r"(johann\s+sebastian\s+bach|\bj\.?\s*s\.?\s*bach|^\s*bach\b|\bbach\s*$|\bbwv\b)"),
    ("Handel", "Baroque", 1759, r"\bh(a|ä|ae)ndel\b"),
    ("Couperin", "Baroque", 1733, r"\bcouperin\b"),
    ("Rameau", "Baroque", 1764, r"\brameau\b"),
    ("Scarlatti, D.", "Baroque", 1757, r"scarlatti"),
    ("Haydn", "Classical", 1809, r"\bhaydn\b"),
    ("Mozart", "Classical", 1791, r"(?<!leopold )mozart"),
    ("Clementi", "Classical", 1832, r"\bclementi\b"),
    ("Beethoven", "Classical", 1827, r"beethoven"),
    ("Schubert", "Romantic", 1828, r"schubert"),
    ("Mendelssohn", "Romantic", 1847, r"mendelssohn"),
    ("Chopin", "Romantic", 1849, r"chopin"),
    ("Schumann, R.", "Romantic", 1856, r"(robert\s+schumann|^\s*r\.?\s*schumann|^\s*schumann\b(?!.*clara))"),
    ("Schumann, C.", "Romantic", 1896, r"clara\s+(wieck[- ]?)?schumann"),
    ("Liszt", "Romantic", 1886, r"\bliszt\b"),
    ("Alkan", "Romantic", 1888, r"\balkan\b"),
    ("Brahms", "Romantic", 1897, r"\bbrahms\b"),
    ("Tchaikovsky", "Romantic", 1893, r"tchaikovsk|tschaikowsk|chaikovsk"),
    ("Mussorgsky", "Romantic", 1881, r"mussorgsk|moussorgsk|musorgsk"),
    ("Grieg", "Romantic", 1907, r"\bgrieg\b"),
    ("Dvorak", "Romantic", 1904, r"dvo(r|ř)(a|á)k"),
    ("Franck", "Romantic", 1890, r"c(e|é)sar\s+franck"),
    ("Faure", "Late Romantic/Impressionist", 1924, r"\bfaur(e|é)\b"),
    ("Albeniz", "Late Romantic/Impressionist", 1909, r"alb(e|é)niz"),
    ("Granados", "Late Romantic/Impressionist", 1916, r"granados"),
    ("Debussy", "Late Romantic/Impressionist", 1918, r"debussy"),
    ("Ravel", "Late Romantic/Impressionist", 1937, r"(maurice\s+ravel|^\s*m\.?\s*ravel|^\s*ravel\b|\bravel\s*$)"),
    ("Satie", "Late Romantic/Impressionist", 1925, r"\bsatie\b"),
    ("Scriabin", "Late Romantic/Impressionist", 1915, r"scriabin|skriabin|skrjabin"),
    ("Rachmaninoff", "Late Romantic/Impressionist", 1943, r"rachmanino|rakhmanino"),
    ("Janacek", "20th c.", 1928, r"jan(a|á)(c|č)ek"),
    ("Schoenberg", "20th c. (atonal/serial)", 1951, r"scho(e|ö|o)nberg"),
    ("Berg, A.", "20th c. (atonal/serial)", 1935, r"alban\s+berg"),
    ("Webern", "20th c. (atonal/serial)", 1945, r"webern"),
    ("Bartok", "20th c.", 1945, r"bart(o|ó)k"),
    ("Ives", "20th c.", 1954, r"charles\s+ives|^\s*ives\s*$"),
    ("Stravinsky", "20th c.", 1971, r"stravinsk|strawinsk"),
    ("Prokofiev", "20th c.", 1953, r"prokofie|prokofje"),
    ("Joplin", "Ragtime/American", 1917, r"\bjoplin\b"),
    ("Gershwin", "Ragtime/American", 1937, r"gershwin"),
    ("Busoni", "20th c.", 1924, r"busoni"),
    ("Cowell", "20th c.", 1965, r"henry\s+cowell"),
    ("Cage", "20th c.", 1992, r"john\s+cage"),
    ("Poulenc", "20th c.", 1963, r"poulenc"),
    ("Hindemith", "20th c.", 1963, r"hindemith"),
    ("Messiaen", "20th c.", 1992, r"messiaen"),
    ("Shostakovich", "20th c.", 1975, r"shostakovich|schostakowitsch"),
    ("Villa-Lobos", "20th c.", 1959, r"villa[- ]lobos"),
    ("Mompou", "20th c.", 1987, r"mompou"),
]
CRX = [(a, e, d, re.compile(r, re.I)) for a, e, d, r in COMPOSERS]

FLAG_RX = re.compile(
    r"\barr\b|arr\.|arrang|easy|simplif|excerpt|beginner|theme from|\btheme\b|transcri|short version|abridged|"
    r"duet|4 hands|four hands|for guitar|remix|cover|medley|\bpart\s*\d|incomplete|unfinished|\bwip\b|lesson|"
    r"\bpage\s*\d|intro only|first page|practice|exercise|\bsnippet|reduction|in the style|inspired|tribute|"
    r"\bpiano\s+tutorial|synthesia|sheet ?music boss|jazz|\bcut\b|shortened|abbreviated|opening|beginning",
    re.I)
CAT_RX = re.compile(
    r"(bwv\s*\.?\s*\d+[a-z]?|\bk\.?\s*\d+[a-z]?\b|\bkv\.?\s*\d+[a-z]?|\bop(us)?\.?\s*\d+[a-z]?|\bno\.?\s*\d+|\bnr\.?\s*\d+|"
    r"\bd\.?\s*\d{2,3}\b|hob\.?\s*[xvi]+[:/.]?\s*\d+|\bwoo\s*\d+|\bl\.?\s*\d+\b|\bs\.?\s*\d{2,3}\b|\bsz\.?\s*\d+|"
    r"\bb\.?\s*\d{2,3}\b|mov(ement|t)?\.?\s*(\d+|[ivx]+)\b|\b(1st|2nd|3rd|4th)\s+mov|"
    r"\b(variation|var\.|prelud\w*|praeludium|fug\w*|invention|sinfonia|[eé]tude|nocturne|mazurka|waltz|valse|ballade|"
    r"scherzo|polonaise|impromptu|sonata|sonate|partita|suite|book|livre|part|teil)\s*(no\.?\s*)?([ivxlc]+\b|\d+))", re.I)
ORCH_RX = re.compile(r"symphon|concerto|serenade|\btrio\b|quartet|overture|\bost\b|anthem|hymn|opera|ballet|nutcracker|"
                     r"sugar.?plum|swan lake|wedding march|lullaby|wiegenlied|ave maria|\bsongs?\b(?! without)|\blied\b(?! ohne)|\baria\b|cantata|"
                     r"jesu,? joy|jesus alegria|air on the g|\bmetal\b|virus|piano solo\)|\(piano solo|for piano\b|piano version", re.I)
KB_NAME = re.compile(r"piano|klavier|clavier|harpsichord|cembalo|clavecin|keyboard|pianoforte|fortepiano|klavecimbel|clavicembalo|virginal", re.I)


def peek_keyboard(path):
    """Cheap MusicXML peek: 1 part with 2 staves, or <=2 parts all keyboard-named -> keyboard."""
    import zipfile
    try:
        z = zipfile.ZipFile(path)
        names = [n for n in z.namelist() if n.endswith((".xml", ".musicxml")) and not n.startswith("META-INF")]
        x = z.read(names[0]).decode("utf-8", "replace")
    except Exception:
        return None
    parts = re.findall(r"<score-part\b.*?</score-part>", x, re.S)
    staves = [int(v) for v in re.findall(r"<staves>(\d+)</staves>", x)]
    kbn = [bool(KB_NAME.search(pp)) for pp in parts]
    if len(parts) == 1 and (max(staves, default=1) >= 2 or kbn[0]):
        return "1part_%sstaff%s" % (max(staves, default=1), "_kbname" if kbn[0] else "")
    if 1 < len(parts) <= 2 and all(kbn):
        return "%dparts_kbname" % len(parts)
    return None


def norm_cat(s):
    toks = [re.sub(r"[\s.:/]", "", m.group(0).lower()).replace("opus", "op").replace("nr", "no").replace("kv", "k")
            for m in CAT_RX.finditer(s)]
    toks = [t.replace("movement", "mvt").replace("mov", "mvt").replace("mvtt", "mvt") for t in toks]
    toks = list(dict.fromkeys(toks))
    prim = [t for t in toks if re.match(r"(bwv|op|k|d|hob|woo|l|s|sz|b)\d", t)]
    if prim:
        keep = prim + [t for t in toks if re.match(r"(no|mvt|variation|var)", t)]
        if any(re.match(r"pr(a|ae|e)lud", t) for t in toks): keep.append("prelude")
        if any(t.startswith("fug") for t in toks): keep.append("fugue")
        toks = keep
    return tuple(sorted(set(toks)))


def match_composer(row):
    cn = str(row.composer_name) if pd.notna(row.composer_name) else ""
    hits = [c for c in CRX if c[3].search(cn)]
    src = "composer_name"
    if not hits:
        blob = " | ".join(str(x) for x in (row.title, row.song_name, row.subtitle, row.artist_name) if pd.notna(x))
        hits = [c for c in CRX if c[3].search(blob)]
        src = "title/artist"
    return hits, src


def main():
    df = pd.read_csv(config.pdmx_csv(), low_memory=False)
    man = {}
    for l in (open(MANIFEST) if os.path.exists(MANIFEST) else []):
        r = json.loads(l)
        man[r["md5_path_key"]] = (r["final_category"], r["outcome"], r.get("reason", ""))
    df["stem"] = df.mxl.str.split("/").str[-1].str.replace(".mxl", "", regex=False)
    df["cat"] = df.stem.map(lambda s: man.get(s, (None,))[0])
    df["enc_outcome"] = df.stem.map(lambda s: man.get(s, (None, None))[1])
    # candidate pool: ALL of PDMX; keyboard-ness from our manifest category, else a MusicXML peek
    g = df
    rows = []
    for r in g.itertuples():
        if not isinstance(r.mxl, str):
            continue
        hits, src = match_composer(r)
        if not hits:
            continue
        if r.cat in ("solo_grand_staff", "multi_keyboard_split_grand"):
            kbsrc = "manifest:" + r.cat
        elif r.cat in ("solo_single_staff", "ensemble_extracted"):
            continue
        else:
            pk = peek_keyboard(config.pdmx_mxl(r.mxl))
            if not pk:
                continue
            kbsrc = "peek:" + pk
        # prefer the more specific hit if several (e.g. 'Schumann, C.' over 'Schumann, R.')
        lab, era, dy, _ = hits[0]
        if len(hits) > 1 and {h[0] for h in hits} == {"Schumann, R.", "Schumann, C."}:
            lab, era, dy, _ = [h for h in hits if h[0] == "Schumann, C."][0]
        text = " | ".join(str(x) for x in (r.title, r.song_name, r.subtitle) if pd.notna(x))
        flags = []
        if FLAG_RX.search(text + " | " + (str(r.composer_name) if pd.notna(r.composer_name) else "")):
            flags.append("arr/excerpt_kw")
        if ORCH_RX.search(text):
            flags.append("orch/vocal_transcription_kw")
        if len({h[0] for h in hits}) > 1 and lab != "Schumann, C.":
            flags.append("multi_composer:" + "+".join(sorted({h[0] for h in hits})))
        if src != "composer_name":
            flags.append("composer_from_title")
        cat = norm_cat(text)
        key = (lab, cat) if cat else (lab, re.sub(r"[^a-z0-9]", "", str(r.title).lower())[:40])
        rows.append(dict(
            source="PDMX", composer=lab, era=era, composer_death=dy, title=str(r.title)[:120],
            composer_name_raw=str(r.composer_name)[:80], keyboard_src=kbsrc, pdmx_dedup=getattr(r, "_58", None),
            pdmx_rel=r.mxl.replace("./mxl/", "", 1), license=r.license, license_conflict=r.license_conflict,
            rating=r.rating, n_ratings=r.n_ratings, n_favorites=r.n_favorites, n_views=r.n_views,
            corpus_cat=r.cat, enc_outcome=r.enc_outcome,
            flags=";".join(flags), work_key=json.dumps(key, ensure_ascii=False)))
    c = pd.DataFrame(rows)
    c["pdmx_bars"] = c.pdmx_rel.map(dict(zip(g.mxl.str.replace("./mxl/", "", n=1, regex=False), g["song_length.bars"])))
    c["flagged"] = c["flags"].str.contains("arr/excerpt|multi_composer|orch/vocal")
    c["pop"] = c.rating.fillna(0) * c.n_ratings.fillna(0)
    c = c.sort_values(["flagged", "pop", "n_favorites", "n_views"], ascending=[True, False, False, False])
    c["dup_rank"] = c.groupby("work_key").cumcount()
    print("matched", len(c), "unique work keys", c.work_key.nunique(), file=sys.stderr)
    c = c[c.dup_rank == 0].drop(columns=["dup_rank", "pop"])

    # music21 corpus items
    from music21 import corpus
    m21 = []
    for p in corpus.getPaths():
        s = str(p); rel = s.split("corpus/")[-1]
        if re.match(r"bach/bwv\d", rel) and rel != "bach/bwv846.mxl" and s.endswith((".mxl", ".xml")):
            m21.append(dict(source="music21", composer="Bach, J.S.", era="Baroque (chorale, 4-voice)", composer_death=1750,
                            title="Chorale " + rel.split("/")[-1].rsplit(".", 1)[0], pdmx_rel="m21:" + rel,
                            license="music21 corpus (not redistributed)", license_conflict=False, flags="chorale_4voice"))
    kb = {"bach/bwv846.mxl": ("Bach, J.S.", "Baroque", 1750, "WTC I Prelude & Fugue in C, BWV 846"),
          "schoenberg/opus19/movement2.mxl": ("Schoenberg", "20th c. (atonal/serial)", 1951, "Sechs kleine Klavierstücke Op.19 No.2"),
          "schoenberg/opus19/movement6.mxl": ("Schoenberg", "20th c. (atonal/serial)", 1951, "Sechs kleine Klavierstücke Op.19 No.6"),
          "chopin/mazurka06-2.krn": ("Chopin", "Romantic", 1849, "Mazurka Op.6 No.2 (kern)"),
          "joplin/maple_leaf_rag.mxl": ("Joplin", "Ragtime/American", 1917, "Maple Leaf Rag"),
          "schumann_clara/polonaise_op1n1.mxl": ("Schumann, C.", "Romantic", 1896, "Polonaise Op.1 No.1"),
          "schumann_clara/polonaise_op1n2.mxl": ("Schumann, C.", "Romantic", 1896, "Polonaise Op.1 No.2"),
          "schumann_clara/polonaise_op1n3.mxl": ("Schumann, C.", "Romantic", 1896, "Polonaise Op.1 No.3"),
          "schumann_clara/polonaise_op1n4.mxl": ("Schumann, C.", "Romantic", 1896, "Polonaise Op.1 No.4")}
    for p in corpus.getPaths():
        s = str(p); rel = s.split("corpus/")[-1]
        if rel in kb:
            a, e, d, t = kb[rel]
            m21.append(dict(source="music21", composer=a, era=e, composer_death=d, title=t, pdmx_rel="m21:" + rel,
                            license="music21 corpus (not redistributed)", license_conflict=False,
                            flags="needs_m21_to_xml" if rel.endswith(".krn") else ""))
    out = pd.concat([c, pd.DataFrame(m21)], ignore_index=True)
    out.insert(0, "cid", [f"C{i:04d}" for i in range(len(out))])
    out.to_csv(OUT + "/canon_list.csv", index=False)
    print(out.groupby(["source", "composer"]).size().to_string(), file=sys.stderr)
    print("total", len(out), "flagged", out.flagged.fillna(False).sum(), file=sys.stderr)


if __name__ == "__main__":
    main()
