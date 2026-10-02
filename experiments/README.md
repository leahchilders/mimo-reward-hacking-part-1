# Experiments

Each folder holds its scripts next to the files they produce. Run a script from its own folder (see the main README for setup). Every score comes from the scorer's own `compute_score`, the same function that grades a model's answer.

## `abc_route/`: a random sample of real piano pieces

- `score_abc_route.py` converts 80 random PDMX piano pieces (listed in `sources.json`) to ABC with xml2abc and scores them. It writes `per_piece.csv` and `hacks.json`.
  - It tries three spellings of the same ABC: `raw` (xml2abc defaults), `stripped` (blank lines removed) and `norm` (`-d 16 --nbr`, fingerings dropped, `U:` lines moved above `K:`). None of them changes the notes.
  - It also scores the hill-climbed pieces in `hack_pieces/` and `examples/`.
- `summarize.py` prints summary statistics from those two files.
- The `norm` ABC this writes to `abc_norm/` is the real-piece input for `hacks/`.

## `hacks/`: ways to raise or zero the score

- `hc.py`: shared grading helpers.
- `climb.py`, `climb_cell.py`: hill-climbers (whole pieces, and short looped cells). Pieces are in `pieces/`.
  - `python climb.py 2 1 1500 16` regrows the 16-bar headline piece: it writes `pieces/climb_s2_st1_b16.abc`, which is `examples/hack_hillclimb_16bar.abc` byte for byte.
- `search64/`: regrows the 64-bar pieces in `examples/`.
  - `search.py` runs a random search over 200 generator configs (seed 0) and writes `search_results.json` and the best piece, `abc_best_random.abc` (0.889).
  - `climb.py` reruns that search, then hill-climbs 600 steps from the best config (rng seed 7). It writes `abc_hillclimb.abc`, which is `examples/hack_hillclimb.abc` byte for byte.
  - `gen.py` builds the ABC; `harness.py` holds the scoring helpers.
  - `examples/hack_hillclimb_staccato.abc` is `hack_hillclimb.abc` with staccato dots added afterwards. Removing every `.` gives the identical file.
- `degen.py`: unoptimized random and degenerate generators (`degen_summary.txt`).
- `knobs.py`, `knobs2.py`, `hack_knobs.py`, `analyze_knobs.py`: one change at a time (tempo, key, note values, instruments, volume, staccato and more) applied to real pieces and hacks (`*_summary.md`, `analyze_knobs.txt`).
- `verify_renotate.py`: checks that the doubled and halved note-value versions really produce the same audio.
- `onevoice.py`: single melodies plus silent or tiny extra voices.
- `mnone.py`: the `M:none` bar-check bypass.
- `breakers.py`: small constructs, valid and invalid ABC, that zero a high-scoring piece (`breakers_out.txt`).
- `tie_errors.py`, `tie_classify.py`: what the tie errors in real pieces actually are (`tie_classify.txt`).
- `length_meter.py`: how length and meter affect the score.
- `grid_alias.py`: how many notes the scorer's eighth-note grid never sees.
- `briefs.py`: the same answers scored against all 1,000 task briefs.

## `canon/`: 1,443 canonical keyboard works and the Bach chorales

- `build_canon.py` builds the piece list (`canon_list.csv`). Use the shipped list; see PROVENANCE.md.
- `run_all.py` scores every piece with `score_one.py` (`results.jsonl`).
- `analyze.py` merges the list and the results (`per_piece.csv`, `per_piece_full.csv`, `tables_auto.md`). Each `loss_*` column is the points that feature cost the piece.
- `cf_grid_phase.py`: re-scores with the eighth-note grid shifted 30 ticks, to separate the timing blind spot from the music (`cf_grid_phase.csv`).
- `fermata_check.py`: re-scores bar-warning failures with fermatas removed (`fermata_check.csv`).
- `fidelity_check.py`: checks that the converted MIDI matches the source score (`fidelity_spotcheck.jsonl`).
- `curate.py`: the hand-picked low-scoring and zeroed examples (`curated_low.csv`).

## `blog_part1/`: the article's examples

These scripts build and check the files in `examples/`:
- re-scoring;
- preparing the MusicXML for Sibelius (`regroup_voices.py`, `explicit_accidentals.py`);
- checking that the MusicXML and the scored MIDI carry the same notes (`check_equiv.py`);
- the unison-chord check (`unison_check.py`).

## `verify/`: independent re-derivations

A second, separately written implementation of the main claims. It reuses only the scorer itself.

- `verify/hacks/`:
  - `c3`: random notes and voices;
  - `c4`: same sound, different note values (`c4b_strict.py` is the exact-audio version used in the article);
  - `c5`: invisible notes and the staccato mechanism;
  - `c6`: silent voices;
  - `c7`: `M:none`;
  - `c8`: briefs;
  - `c9`: breakers;
  - `c10`: tie errors;
  - `c11`: meter;
  - `climb.py`: an independent hill-climber. `python climb.py 11 4 1200` regrows `examples/best_loop_4bar.abc`.
  - `climb_fixed.py`: the same hill-climber against the scorer with the timing blind spot fixed (the 30-tick grid shift from `verify/canon/son_phase_patch.py`). `python climb_fixed.py 11 4 1200`; results for seeds 11–15 are in `climb_fixed_n4_s*.json`.
- `verify/canon/`:
  - `t1`: low-scoring passers;
  - `t2`: the timing blind spot and the grid shift (`son_phase_patch.py`);
  - `t3`: ties and zeroed pieces;
  - `t4`: chorales and fermatas;
  - `t5`: spot checks and summary statistics.

  Saved outputs are in `recorded/`.
