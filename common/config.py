"""One place for every external path. Each comes from an env var, with a default relative to the repo root.

  MIMO_SCORER_DIR  dir that contains the upstream `scorer` package
                   (default: third_party/mimo_verl/recipes/design/music)
  ABC2MIDI_BIN     abc2midi binary                (default: third_party/abcmidi/abc2midi)
  XML2ABC          xml2abc.py, version 177        (default: third_party/xml2abc/xml2abc.py)
  MIMO_BRIEFS      the 1,000 MiMo music briefs    (default: third_party/mimo-music-grpo/data/music.parquet)
  PDMX_ROOT        PDMX dataset root; only the canon/ and abc_route/ studies need it
  PDMX_MXL_DIR     optional; the dir holding PDMX's <a>/<b>/<hash>.mxl tree (default: auto-detected under PDMX_ROOT)

Importing this module also sets ABC2MIDI_BIN in the environment (the scorer reads it at import time),
puts the upstream scorer on sys.path, and aliases it as `music_scorer` and `mscorer`, the names the
scripts were written against. The upstream code is used unmodified.
"""
import importlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _path(var, default):
    v = os.environ.get(var)
    return os.path.abspath(v) if v else os.path.join(ROOT, default)


MIMO_SCORER_DIR = _path("MIMO_SCORER_DIR", "third_party/mimo_verl/recipes/design/music")
ABC2MIDI_BIN = _path("ABC2MIDI_BIN", "third_party/abcmidi/abc2midi")
XML2ABC = _path("XML2ABC", "third_party/xml2abc/xml2abc.py")
MIMO_BRIEFS = _path("MIMO_BRIEFS", "third_party/mimo-music-grpo/data/music.parquet")
PDMX_ROOT = os.path.abspath(os.environ["PDMX_ROOT"]) if os.environ.get("PDMX_ROOT") else None
EXAMPLES = os.path.join(ROOT, "examples")
EXPERIMENTS = os.path.join(ROOT, "experiments")
REF_PATH = os.path.join(MIMO_SCORER_DIR, "scorer", "baselines", "ref_full4k.json")


def _need_pdmx():
    if not PDMX_ROOT:
        sys.exit("PDMX_ROOT is not set; this study needs the PDMX dataset (see README).")
    return PDMX_ROOT


def pdmx_mxl_dir():
    if os.environ.get("PDMX_MXL_DIR"):
        return os.path.abspath(os.environ["PDMX_MXL_DIR"])
    root = _need_pdmx()
    nested = os.path.join(root, "mxl", "mxl")   # the mxl archive sometimes unpacks one level deeper
    return nested if os.path.isdir(nested) else os.path.join(root, "mxl")


def pdmx_mxl(rel):
    """PDMX-relative path ('./mxl/5/27/Qm....mxl' or '5/27/Qm....mxl') -> absolute .mxl path."""
    rel = rel[2:] if rel.startswith("./") else rel
    rel = rel[4:] if rel.startswith("mxl/") else rel
    return os.path.join(pdmx_mxl_dir(), rel)


def pdmx_csv():
    root = _need_pdmx()
    for p in (os.path.join(root, "PDMX.csv"), os.path.join(root, "metadata", "PDMX.csv")):
        if os.path.exists(p):
            return p
    sys.exit(f"PDMX.csv not found under {root}")


def canon_path(row):
    """Source file for a canon_list.csv row: a PDMX .mxl, or a music21-corpus file ('m21:<rel>')."""
    rel = row["pdmx_rel"]
    if rel.startswith("m21:"):
        import music21
        return os.path.join(os.path.dirname(music21.__file__), "corpus", rel[4:])
    return pdmx_mxl(rel)


# ---- scorer import + module aliases ----
os.environ["ABC2MIDI_BIN"] = ABC2MIDI_BIN
if not os.path.isdir(os.path.join(MIMO_SCORER_DIR, "scorer")):
    sys.exit(f"MiMo scorer not found at {MIMO_SCORER_DIR}/scorer; run ./setup.sh or set MIMO_SCORER_DIR.")
sys.path.insert(0, MIMO_SCORER_DIR)
_SUBS = ("core", "feats", "score", "pipeline")
scorer = importlib.import_module("scorer")
for _s in _SUBS:
    importlib.import_module("scorer." + _s)
for _alias in ("music_scorer", "mscorer"):
    sys.modules[_alias] = scorer
    for _s in _SUBS:
        sys.modules[f"{_alias}.{_s}"] = sys.modules["scorer." + _s]
