# Tuned Noise Beats Bach: Reward-Hacking the MiMo-V2.6 Music Scorer

Code, data and media for the article: https://leahchilders-portfolio.vercel.app/music-ml/mimo-reward-hacking-part-1

Xiaomi's MiMo-V2.6 release (September 22) included about a thousand "music composition" RL tasks and the reward function used to score them. In their tech report, Xiaomi used these tasks for training experiments on a small 9B model. That reward is now being ported into two widely used open RL frameworks, NVIDIA NeMo-Gym and Prime Intellect's environment library (both [pull](https://github.com/NVIDIA-NeMo/Gym/pull/3704) [requests](https://github.com/PrimeIntellect-ai/prime-envs/pull/843) still open as of October 1, 2026). If they merge, it may be one of the ready-made music environments people train against.

I ran real classical music through it, **1,443 keyboard pieces by canonical composers** from the public-domain PDMX corpus, from Bach and Scarlatti through Chopin, Debussy and Joplin.

- **A third of them scored exactly zero.** In most cases this wasn't the music's fault: the file failed the ABC-to-MIDI step, often because of how it had been converted to ABC in the first place.
- **The rest scored a median of 0.80** out of 1.

Then I let a simple search algorithm write music against the scorer.

- Random C-major notes, tuned by the search and sprinkled with staccato dots, reached **0.978**. That beats **every one of the 958 real pieces that got a score**, including all 377 scored Bach pieces (Bach's best: 0.94).
- Short loops do almost as well: one 4-bar pattern played twice, 335 characters of text, reached **0.97**.
- Bach's Goldberg Variation XXIII scores **0.44** (one of his lowest).

## What's here

- `media/`: the audio, score PDFs, Sibelius files and figure used in the article.
- `examples/`: our generated pieces (ABC + MusicXML) with their scores; `best_loop_4bar.abc` is the 0.973 loop.
- `experiments/`: one folder per study, each with its scripts and results (see `experiments/README.md`).
  - `abc_route/`: 80 random PDMX piano pieces scored the way a model's answer is scored.
  - `hacks/`: hill-climbers, the exploit map, gate breakers, tie analysis, and length/meter checks.
  - `canon/`: 1,443 canonical keyboard works plus the Bach chorales, feature blame and the grid-shift counterfactual.
  - `blog_part1/`: scripts that built and checked `examples/`.
  - `verify/`: independent re-derivations of the `hacks/` and `canon/` claims.
- `common/`: `config.py` (all paths, from env vars) and shared helpers.
- `setup.sh`: fetches the upstream scorer, abc2midi, xml2abc and the MiMo briefs into `third_party/` (gitignored).

## Reproduce

Run `./setup.sh` and `pip install -r requirements.txt`. Or point `MIMO_SCORER_DIR`, `ABC2MIDI_BIN` and `XML2ABC` at existing copies (see `common/config.py`). Run each script from its own folder, since many read and write files next to it. Example: `cd experiments/verify/hacks && python climb.py 11 4 1200` reproduces the 0.973 loop.

`abc_route/`, `canon/` and `verify/canon/` need the PDMX dataset (paper: arXiv:2409.10831; data on Zenodo). Set `PDMX_ROOT` to it. The real-piece parts of `hacks/` and `verify/hacks/` read the ABC that `abc_route/score_abc_route.py` generates. The synthetic hacks and `examples/` need only the scorer and abc2midi.

## Licenses

Code: MIT (see `LICENSE`). Media in `media/` (audio renders, PDFs, Sibelius files, image): CC BY 4.0 (see `media/LICENSE`). The underlying compositions are in the public domain.

The plain abc2midi audio (`*-abc2midi.mp3`, what the scorer "heard") is abc2midi MIDI rendered with fluidsynth 2.3.4 and the Salamander Grand V3 piano (gain 0.5, reverb and chorus on, 44.1 kHz, LAME VBR q2). The other renders were made in Sibelius with NotePerformer.