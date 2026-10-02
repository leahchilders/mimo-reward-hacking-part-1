# Provenance

## Tools

| Tool | Source | Version | License |
|---|---|---|---|
| MiMo-V2.6 music scorer | https://github.com/XiaomiMiMo/verl, branch `mimo-oss`, `recipes/design/music/scorer` | commit `a2ad9f6` | Apache-2.0 |
| abc2midi | https://github.com/sshlien/abcmidi, built from source (`./configure && make abc2midi`) | commit `11f66bb` | GPL |
| xml2abc.py (Wim Vree) | https://wim.vree.org/svgParse/xml2abc.html (`xml2abc.py-177.zip`, sha256 `158ae6ac87c34b7f170a7a57712206fac756e0434806e38a280f6fd968c8816d`) | 177 | LGPL |
| MiMo music briefs (`data/music.parquet`) | https://github.com/PromptEngineer48/mimo-music-grpo | commit `6153898` | see that repo |
| music21 | PyPI | 9.9.2 | BSD-3-Clause |

The scorer is used unmodified. `common/config.py` imports it under the names the scripts use (`music_scorer`, `mscorer`). For the grid-phase counterfactual, the original run used a patched copy of `feats.py` that started the sonority sampling grid at `SON_PHASE` ticks. `experiments/verify/canon/son_phase_patch.py` applies the same change to the upstream function at runtime. `experiments/canon/cf_grid_phase.py` swaps in its own version of the same 30-tick shift.

The MiMo Harbor tasks pin Debian `abcmidi=20250216+ds-1`. Our abc2midi is a source build of `11f66bb` (version 5.04). Results were checked under two abc2midi versions, our 5.04 build and upstream 5.02 (2025-02-16, the version Debian packages; its packaged binary was tested too), and gave identical scores.

## Data

- **PDMX**: public-domain MusicXML from MuseScore ("PDMX: A Large-Scale Public Domain MusicXML Dataset for Symbolic Music Processing", arXiv:2409.10831; data on Zenodo). Result files keep only metadata: titles, PDMX-relative paths, licenses, scores and feature values.
- **music21 corpus**: the Bach chorales and a few keyboard items in `canon/` are read from the corpus installed with music21. They are not redistributed here.
- **Not included**: `canon/build_canon.py` used a private corpus manifest (`CANON_MANIFEST`) to find keyboard pieces, so without it a rebuilt list will differ. Use the shipped `canon_list.csv`.

## Rendered pieces (media/)

| Piece | Source | Source license |
|---|---|---|
| Bach, Goldberg Variation XXIII | PDMX `7/11/QmPb7NggGCNXqTZ6GdqkyerQc2YfkeFUrx6ujuqMiW5XTr.mxl` | cc-zero |
| Joplin, The Entertainer | PDMX `5/27/QmfJ9kKExnxAoh69DMVttznStQaR5HRBAtqSocxW6u9ncx.mxl` | publicdomain |
| Hill-climbed + staccato hack | `examples/hack_hillclimb_staccato.abc` (ours) | n/a |

The Sibelius + NotePerformer renders, PDFs and Sibelius files were made by the author. The `*-abc2midi.mp3` files are the abc2midi MIDI rendered with fluidsynth 2.3.4 and the Salamander Grand V3 piano (gain 0.5, reverb and chorus on, 44.1 kHz, LAME VBR q2).
