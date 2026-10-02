Base: real n=52 median 0.837; hack n=8 median 0.947

| knob | real: median Δ | real: up/down/zeroed (n) | hack: median Δ | hack: up/down/zeroed (n) | features moved (real, median Δ ≠ 0) |
|---|---|---|---|---|---|
| tempo_x0.5 (Q:) | +0.000 | 2/1/0 (52) | +0.000 | 0/0/0 (8) |  |
| tempo_x2 (Q:) | +0.000 | 1/1/0 (52) | +0.000 | 0/0/0 (8) |  |
| L:_halved (2x faster) | -0.837 | 0/52/52 (52) | -0.947 | 0/8/8 (8) | ioi_mean -0.04, rhythm_surprisal -0.08, qualified_note_rate -0.08, polyphony_rate -0.07, polyphony_mean -0.14, roughness_p90 -0.19, harmonicity_mean -0.09, local_key_certainty +0.07, tension_peaks -0.21 |
| trim 1/32 (%%MIDI trim) | +0.000 | 23/14/0 (52) | -0.000 | 0/4/0 (8) | note_len_entropy +0.06 |
| trim 1/16 (%%MIDI trim) | +0.007 | 35/17/0 (52) | +0.014 | 4/4/0 (8) | note_len_entropy -0.03, qualified_note_rate -0.02, JS dist_score/100 +0.02 |
| nobeataccents | +0.000 | 7/6/0 (52) | +0.000 | 0/1/0 (8) |  |
| dyn pp (beat 45 35 20) | +0.000 | 4/15/0 (52) | +0.000 | 0/1/0 (8) |  |
| dyn ff (beat 120 110 95) | +0.000 | 6/5/0 (52) | +0.000 | 0/1/0 (8) |  |
| vel extreme (beat 127 64 1) | +0.000 | 4/12/0 (52) | -0.013 | 0/4/0 (8) |  |
| droneon (V:1) | +0.000 | 0/0/0 (52) | +0.000 | 0/0/0 (8) |  |
| drum pattern (V:1) | +0.000 | 13/6/4 (52) | +0.000 | 0/0/0 (8) | ioi_mean +0.03, rhythm_surprisal +0.03 |
| extra voice: 1 note C,,, (new chan) | -0.045 | 3/49/0 (52) | -0.046 | 0/8/0 (8) | pitch_min -0.77, pitch_range -0.31 |
| extra voice: 1 note C,,, (chan 1) | -0.045 | 3/49/0 (52) | -0.046 | 0/8/0 (8) | pitch_min -0.77, pitch_range -0.31 |
| extra voice: 1 note c (new chan) | +0.000 | 24/3/0 (52) | +0.000 | 0/1/0 (8) |  |
| extra voice: 3 one-note voices | +0.001 | 32/2/0 (52) | +0.000 | 0/1/0 (8) | qualified_note_rate +0.05 |
| extra voice: 1 note at vol 0 (CC7=0) | -0.045 | 3/49/0 (52) | -0.046 | 0/8/0 (8) | pitch_min -0.77, pitch_range -0.31 |
| grace %%MIDI grace 1/2 | +0.000 | 3/5/0 (52) | +0.000 | 0/0/0 (8) |  |
| chordattack 20 | +0.000 | 14/4/0 (52) | +0.000 | 0/0/0 (8) |  |
| randomchordattack 30 | +0.001 | 27/12/0 (52) | -0.001 | 0/6/0 (8) | note_len_entropy +0.02, ioi_mean +0.02 |
| ratio 3 1 (broken rhythm) | +0.000 | 0/0/0 (52) | +0.000 | 0/0/0 (8) |  |
| expand 1/8 | -0.103 | 2/49/25 (52) | -0.947 | 0/8/8 (8) | ioi_mean +0.03, rhythm_surprisal -0.22, qualified_note_rate -0.15, polyphony_rate -0.34, polyphony_mean +0.12, roughness_p90 +0.11, harmonicity_mean -0.07, local_key_certainty -0.02, self_similarity -0.03, JS dist_score/100 -0.03 |
| temperament 1200 698 | +0.000 | 0/0/0 (52) | +0.000 | 0/0/0 (8) |  |
| transpose -6 | -0.018 | 16/36/0 (52) | -0.029 | 0/8/0 (8) | roughness_p90 -0.18, pitch_min -0.08, JS dist_score/100 -0.05 |
| transpose -5 | -0.004 | 20/31/0 (52) | -0.003 | 0/8/0 (8) | roughness_p90 -0.13, pitch_min -0.06 |
| transpose -4 | -0.010 | 18/34/0 (52) | -0.020 | 0/8/0 (8) | roughness_p90 -0.09, pitch_min -0.05, JS dist_score/100 -0.04 |
| transpose -3 | -0.008 | 19/32/0 (52) | -0.011 | 0/8/0 (8) | roughness_p90 -0.05, pitch_min -0.02, tension_peaks -0.03 |
| transpose -2 | -0.003 | 19/33/0 (52) | -0.008 | 0/8/0 (8) | roughness_p90 -0.04, JS dist_score/100 -0.02 |
| transpose -1 | -0.010 | 14/37/0 (52) | -0.021 | 0/8/0 (8) | tension_peaks -0.03, JS dist_score/100 -0.04 |
| transpose +1 | -0.010 | 13/38/0 (52) | -0.036 | 0/8/0 (8) | pitch_min -0.03, JS dist_score/100 -0.05 |
| transpose +2 | -0.004 | 20/30/0 (52) | -0.005 | 0/8/0 (8) | pitch_min -0.06, tension_peaks +0.03 |
| transpose +3 | -0.012 | 15/37/0 (52) | -0.014 | 0/8/0 (8) | pitch_min -0.09, tension_peaks +0.02, JS dist_score/100 -0.03 |
| transpose +4 | -0.014 | 14/38/0 (52) | -0.016 | 0/8/0 (8) | pitch_min -0.13, JS dist_score/100 -0.03 |
| transpose +5 | -0.012 | 13/38/0 (52) | -0.013 | 0/8/0 (8) | roughness_p90 -0.02, pitch_min -0.19, tension_peaks +0.04 |
| transpose -12 | -0.046 | 12/38/0 (52) | -0.060 | 0/8/0 (8) | roughness_p90 -0.49, pitch_min -0.22 |
| transpose +12 | -0.045 | 6/45/0 (52) | -0.048 | 0/8/0 (8) | roughness_p90 -0.32, pitch_min -0.43 |
