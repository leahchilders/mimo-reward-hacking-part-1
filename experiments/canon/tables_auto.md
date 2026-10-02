# auto tables

status counts: {('m21_bach_chorales', 'ok'): 409, ('m21_keyboard', 'ok'): 9, ('pdmx_canon', 'ok'): 1443, ('pdmx_canon', 'xml2abc_fail'): 5, ('pdmx_flagged', 'ok'): 361, ('pdmx_flagged', 'xml2abc_fail'): 1}

wall per piece (s): median 0.73 p90 4.14 max 219.53 sum 6391 


## group pdmx_canon

| n | scored | zeroed | zeroed_pct | med_reward_all | med_pass | iqr_pass | min_pass | med_ungated |
|---|---|---|---|---|---|---|---|---|
| 1448 | 1443 | 485 | 34.0 | 0.729 | 0.799 | 0.73-0.867 | 0.172 | 0.817 |

## group pdmx_flagged

| n | scored | zeroed | zeroed_pct | med_reward_all | med_pass | iqr_pass | min_pass | med_ungated |
|---|---|---|---|---|---|---|---|---|
| 362 | 361 | 139 | 39.0 | 0.698 | 0.799 | 0.717-0.857 | 0.12 | 0.807 |

## group m21_keyboard

| n | scored | zeroed | zeroed_pct | med_reward_all | med_pass | iqr_pass | min_pass | med_ungated |
|---|---|---|---|---|---|---|---|---|
| 9 | 9 | 0 | 0.0 | 0.868 | 0.868 | 0.767-0.893 | 0.473 | 0.868 |

## group m21_bach_chorales

| n | scored | zeroed | zeroed_pct | med_reward_all | med_pass | iqr_pass | min_pass | med_ungated |
|---|---|---|---|---|---|---|---|---|
| 409 | 409 | 346 | 85.0 | 0.0 | 0.76 | 0.72-0.814 | 0.594 | 0.752 |

## pdmx_canon by era

| era | n | scored | zeroed | zeroed_pct | med_reward_all | med_pass | iqr_pass | min_pass | med_ungated |
|---|---|---|---|---|---|---|---|---|---|
| 20th c. (atonal/serial) | 6 | 6 | 2 | 33.0 | 0.203 | 0.395 | 0.218-0.586 | 0.172 | 0.556 |
| Classical | 254 | 254 | 64 | 25.0 | 0.738 | 0.782 | 0.716-0.871 | 0.227 | 0.807 |
| Baroque | 601 | 601 | 136 | 23.0 | 0.765 | 0.792 | 0.735-0.85 | 0.295 | 0.794 |
| Romantic | 334 | 332 | 154 | 46.0 | 0.528 | 0.808 | 0.715-0.869 | 0.182 | 0.829 |
| Late Romantic/Impressionist | 158 | 156 | 92 | 59.0 | 0.0 | 0.832 | 0.796-0.885 | 0.505 | 0.849 |
| 20th c. | 26 | 25 | 5 | 20.0 | 0.852 | 0.852 | 0.65-0.852 | 0.439 | 0.852 |
| Ragtime/American | 69 | 69 | 32 | 46.0 | 0.834 | 0.909 | 0.881-0.935 | 0.823 | 0.909 |

## pdmx_canon by composer (n>=3)

| composer | n | scored | zeroed | zeroed_pct | med_reward_all | med_pass | iqr_pass | min_pass | med_ungated |
|---|---|---|---|---|---|---|---|---|---|
| Schoenberg | 6 | 6 | 2 | 33.0 | 0.203 | 0.395 | 0.218-0.586 | 0.172 | 0.556 |
| Dvorak | 4 | 4 | 2 | 50.0 | 0.2 | 0.647 | 0.523-0.772 | 0.399 | 0.893 |
| Alkan | 4 | 4 | 1 | 25.0 | 0.691 | 0.697 | 0.691-0.793 | 0.685 | 0.794 |
| Brahms | 23 | 23 | 10 | 43.0 | 0.344 | 0.702 | 0.408-0.845 | 0.245 | 0.834 |
| Tchaikovsky | 9 | 9 | 1 | 11.0 | 0.713 | 0.722 | 0.58-0.815 | 0.182 | 0.732 |
| Rachmaninoff | 20 | 19 | 16 | 84.0 | 0.0 | 0.739 | 0.707-0.812 | 0.675 | 0.872 |
| Beethoven | 84 | 84 | 27 | 32.0 | 0.641 | 0.752 | 0.636-0.808 | 0.251 | 0.794 |
| Haydn | 65 | 65 | 14 | 22.0 | 0.75 | 0.765 | 0.732-0.8 | 0.227 | 0.784 |
| Handel | 68 | 68 | 12 | 18.0 | 0.742 | 0.771 | 0.712-0.835 | 0.383 | 0.773 |
| Mussorgsky | 15 | 15 | 7 | 47.0 | 0.536 | 0.774 | 0.703-0.825 | 0.536 | 0.813 |
| Bach, J.S. | 475 | 475 | 98 | 21.0 | 0.767 | 0.792 | 0.735-0.847 | 0.295 | 0.793 |
| Liszt | 40 | 38 | 28 | 74.0 | 0.0 | 0.792 | 0.603-0.859 | 0.3 | 0.791 |
| Grieg | 18 | 18 | 5 | 28.0 | 0.728 | 0.795 | 0.718-0.887 | 0.562 | 0.806 |
| Ravel | 14 | 13 | 9 | 69.0 | 0.0 | 0.796 | 0.751-0.82 | 0.624 | 0.786 |
| Mendelssohn | 34 | 34 | 7 | 21.0 | 0.758 | 0.797 | 0.734-0.862 | 0.584 | 0.815 |
| Satie | 30 | 30 | 1 | 3.0 | 0.8 | 0.8 | 0.798-0.878 | 0.505 | 0.8 |
| Faure | 5 | 5 | 3 | 60.0 | 0.0 | 0.811 | 0.761-0.861 | 0.712 | 0.815 |
| Schubert | 43 | 43 | 10 | 23.0 | 0.794 | 0.82 | 0.77-0.877 | 0.301 | 0.833 |
| Schumann, R. | 43 | 43 | 20 | 47.0 | 0.582 | 0.821 | 0.72-0.857 | 0.514 | 0.826 |
| Chopin | 100 | 100 | 62 | 62.0 | 0.0 | 0.833 | 0.783-0.878 | 0.615 | 0.847 |
| Mozart | 99 | 99 | 23 | 23.0 | 0.771 | 0.845 | 0.716-0.896 | 0.246 | 0.869 |
| Rameau | 16 | 16 | 11 | 69.0 | 0.0 | 0.848 | 0.814-0.864 | 0.783 | 0.861 |
| Debussy | 54 | 54 | 46 | 85.0 | 0.0 | 0.851 | 0.804-0.891 | 0.695 | 0.871 |
| Bartok | 17 | 16 | 2 | 12.0 | 0.852 | 0.852 | 0.708-0.852 | 0.439 | 0.852 |
| Clementi | 6 | 6 | 0 | 0.0 | 0.856 | 0.856 | 0.778-0.933 | 0.668 | 0.856 |
| Scriabin | 14 | 14 | 9 | 64.0 | 0.0 | 0.86 | 0.799-0.887 | 0.797 | 0.823 |
| Scarlatti, D. | 40 | 40 | 14 | 35.0 | 0.776 | 0.863 | 0.788-0.892 | 0.597 | 0.867 |
| Albeniz | 6 | 6 | 5 | 83.0 | 0.0 | 0.874 | 0.874-0.874 | 0.874 | 0.846 |
| Granados | 15 | 15 | 3 | 20.0 | 0.886 | 0.895 | 0.864-0.92 | 0.606 | 0.891 |
| Gershwin | 3 | 3 | 2 | 67.0 | 0.0 | 0.9 | 0.9-0.9 | 0.9 | 0.885 |
| Joplin | 66 | 66 | 30 | 45.0 | 0.844 | 0.91 | 0.881-0.935 | 0.823 | 0.913 |
| Shostakovich | 4 | 4 | 1 | 25.0 | 0.853 | 0.911 | 0.853-0.923 | 0.795 | 0.873 |

## lowest 40 passing (pdmx_canon + m21_keyboard)

| cid | reward | composer | title | license | license_conflict | article_clean | f_n_note | top_losses |
|---|---|---|---|---|---|---|---|---|
| C1384 | 0.172 | Schoenberg | Fundamentos da Composicao Musical - Schoenberg Arnold - Ex. 2 - i - Wagner - Motivo de Wotan | cc-zero | False | False | 16.0 | dist_hist(JS) -13.4; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1043 | 0.182 | Tchaikovsky | Danza Rusa Trepak Score - Piano-Violín-Guitarra PI | cc-zero | True | False | 160.0 | dist_hist(JS) -13.8; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1399 | 0.227 | Haydn | Tema de La Creació - Haydn | cc-zero | False | True | 52.0 | dist_hist(JS) -11.1; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1371 | 0.233 | Schoenberg | Fundamentos da Composicao Musical - Schoenberg Arnold - Ex. 1 - b - Op. 28-II | cc-zero | False | False | 12.0 | dist_hist(JS) -10.1; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1369 | 0.245 | Brahms | Fundamentos da Composicao Musical - Schoenberg Arnold - Ex. 2 - f - Brahms - Sinfomia com Piano | cc-zero | False | True | 16.0 | dist_hist(JS) -10.4; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1241 | 0.246 | Mozart | Dona_Nobis_Pacem | cc-zero | False | True | 60.0 | dist_hist(JS) -8.4; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C0689 | 0.251 | Beethoven | Himne a l'alegria - Beethoven | cc-zero | False | True | 88.0 | dist_hist(JS) -12.1; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1328 | 0.28 | Beethoven | Sonatina - Beethoven | cc-zero | False | True | 44.0 | dist_hist(JS) -8.2; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1312 | 0.288 | Beethoven | Marxa turca - Beethoven | cc-zero | False | True | 111.0 | dist_hist(JS) -8.5; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1337 | 0.295 | Beethoven | Tema de la Simfonia Pastoral - Beethoven | cc-zero | False | True | 24.0 | dist_hist(JS) -11.1; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1019 | 0.295 | Bach, J.S. | Minuet en Sol major - Bach | cc-zero | False | True | 64.0 | dist_hist(JS) -8.5; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1221 | 0.3 | Liszt | Prélude Omnitonique | cc-zero | False | True | 64.0 | dist_hist(JS) -10.5; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 0.0) -5.7 |
| C1255 | 0.301 | Tchaikovsky | Danza Rusa Trepak Score - Piano II PS | cc-zero | True | False | 334.0 | dist_hist(JS) -8.5; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 0.0) -5.7 |
| C1299 | 0.301 | Schubert | Zum Sanctus | cc-zero | False | True | 45.0 | dist_hist(JS) -14.1; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1403 | 0.316 | Beethoven | Rondó en Do major - Beethoven | cc-zero | False | True | 81.0 | dist_hist(JS) -8.5; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C0828 | 0.344 | Brahms | Brahms - 51 Übungen für Klavier No. 2a | cc-zero | False | True | 1000.0 | dist_hist(JS) -8.2; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 0.0) -5.7 |
| C1290 | 0.366 | Beethoven | Fundamentos da Composicao Musical - Schoenberg Arnold - Ex. 2 - g - Beethoven - Sinfonia nº 9-I | cc-zero | False | True | 36.0 | dist_hist(JS) -6.2; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C0638 | 0.367 | Brahms | Berceuse de Brahms | cc-zero | False | True | 60.0 | dist_hist(JS) -6.3; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1260 | 0.376 | Beethoven | Sonatina en Sol major - Beethoven | cc-zero | False | True | 142.0 | dist_hist(JS) -8.2; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1130 | 0.383 | Handel | Dixit Dominus Tenor | cc-zero | False | False | 549.0 | roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7; dist_hist(JS) -4.8 |
| C1095 | 0.389 | Bach, J.S. | Bach's enharmonic modulation | cc-zero | False | True | 44.0 | dist_hist(JS) -10.0; polyphony_rate(high 1.0) -5.7; self_similarity(low 0.0) -5.1; key_certainty(low 0.61) -4.5; pitch_min(high 49) -4.5 |
| C1115 | 0.399 | Dvorak | IVCSO Violin II Dvorak Slavonic Dances Nos 1-4 | cc-zero | False | True | 226.0 | dist_hist(JS) -6.7; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1278 | 0.402 | Handel | Zadok the pries | cc-zero | False | True | 572.0 | dist_hist(JS) -6.1; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C0857 | 0.408 | Brahms | Brahms - 51 Übungen für Klavier No. 8a | cc-zero | False | True | 176.0 | dist_hist(JS) -9.7; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 0.0) -5.7 |
| C0442 | 0.435 | Bach, J.S. | Minuet No.2 (J.S. Bach) | publicdomain | False | True | 165.0 | dist_hist(JS) -6.5; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C0329 | 0.439 | Bartok | Six Unison Melodies | cc-zero | False | True | 336.0 | dist_hist(JS) -13.9; roughness_p90(low 0.0012) -6.0; polyphony_rate(high 1.0) -5.7; local_key_certainty(low 0.623) -4.5; voice_leading_cost(low 1.784) -4.5 |
| C1184 | 0.443 | Bach, J.S. | BWV 988 Goldberg Variations: Variation XXIII | cc-zero | False | True | 1474.0 | dist_hist(JS) -7.6; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1415 | 0.453 | Handel | Messiah | cc-zero | False | False | 696.0 | roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7; pitch_min(high 63) -4.5 |
| C0960 | 0.463 | Bach, J.S. | BWV 856 The Well-Tempered Clavier Part I Praeludium XI | cc-zero | False | True | 915.0 | roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7; dist_hist(JS) -4.7 |
| C1293 | 0.47 | Bartok | Bartok_Bela_-_Primera_lección_de_piano | cc-zero | False | True | 301.0 | dist_hist(JS) -11.2; local_key_certainty(low 0.635) -4.5; pitch_min(high 48) -4.5; voice_leading_cost(low 1.726) -4.5; self_similarity(low 0.432) -4.3 |
| C2223 | 0.473 | Schoenberg | Sechs kleine Klavierstücke Op.19 No.6 | music21 corpus (not redistributed) | False | False | 52.0 | dist_hist(JS) -6.5; harmonicity_mean(low 0.4009) -6.0; self_similarity(low 0.067) -5.1; polyphony_rate(high 0.948) -4.9; key_certainty(low 0.448) -4.5 |
| C1262 | 0.473 | Liszt | Andantino | cc-zero | False | False | 132.0 | dist_hist(JS) -12.5; polyphony_rate(high 0.973) -5.3; pitch_min(high 55) -4.5; pitch_range(low 19) -4.5; note_len_entropy(low 0.226) -3.7 |
| C1440 | 0.491 | Mozart | Eternal source of every joy - Philip Doddridge | publicdomain | False | True | 146.0 | dist_hist(JS) -11.1; polyphony_rate(high 0.994) -5.7; self_similarity(low 0.338) -5.1; pitch_min(high 48) -4.5; pitch_range(low 26) -4.5 |
| C1155 | 0.501 | Handel | 89 Joy to the World - Chord | cc-zero | False | True | 133.0 | dist_hist(JS) -6.9; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1231 | 0.504 | Bartok | Bartok Apuntes analíticos MK148 | cc-zero | False | False | 65.0 | dist_hist(JS) -7.7; self_similarity(low 0.167) -5.1; key_certainty(low 0.61) -4.5; local_key_certainty(low 0.634) -4.5; pitch_min(high 47) -4.5 |
| C0406 | 0.505 | Satie | Erik Satie - Enfantillages Pittoresques - Berceuse | cc-zero | False | True | 255.0 | dist_hist(JS) -10.4; polyphony_rate(high 0.995) -5.7; pitch_min(high 65) -4.5; pitch_range(low 16) -4.5; ioi_mean(high 0.704) -3.7 |
| C1437 | 0.508 | Handel | êµì¼ ììë D | cc-zero | True | False | 135.0 | dist_hist(JS) -6.7; roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7 |
| C1129 | 0.514 | Schumann, R. | Primera Romanza de Schumann | cc-zero | False | True | 292.0 | roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7; pitch_min(high 59) -4.5 |
| C1258 | 0.514 | Bach, J.S. | Bach Choral 19 m.5 | cc-zero | False | False | 19.0 | dist_hist(JS) -11.4; self_similarity(low 0.0) -5.1; tension_peaks(low 0) -5.1; pitch_min(high 50) -4.5; pitch_range(low 22) -4.5 |
| C0599 | 0.517 | Bach, J.S. | BWV 855 The Well-Tempered Clavier Part I Fuga X | cc-zero | False | True | 810.0 | roughness_p90(low 0.0) -6.0; harmonicity_mean(low 0.0) -6.0; polyphony_rate(very-low 0.0) -5.7; polyphony_mean(low 1) -5.7; dist_hist(JS) -5.0 |

## zeroed canon, highest ungated (30)

| cid | quality_ungated | composer | title | gates | first_errors | article_clean |
|---|---|---|---|---|---|---|
| C0126 | 97.7 | Joplin | Paragon Rag - Scott Joplin - 1909 | abc2midi_Error x22 | Error in line-char 20-30 : Could not find note to be tied / Error in line-char 20-30 : Could not find note to be tied / Error in line-char 22-30 : Could not find note to be tied | False |
| C0006 | 97.3 | Joplin | The Entertainer - Scott Joplin - 1902 | abc2midi_Error x1 | Error in line-char 40-29 : Could not find note to be tied | False |
| C0287 | 97.2 | Beethoven | Beethoven: Rondo alla ingharese quasi un capriccio (Rage Over a Lost Penny) (c. 1795-98) | bar_warnings x28 |  | False |
| C0088 | 97.0 | Faure | Fauré - Dolly Suite No. 1: Berceuse | bar_warnings x12 |  | True |
| C0127 | 97.0 | Joplin | Heliotrope Bouquet - Joplin and Chauvin - 1907 | abc2midi_Error x11 | Error in line-char 17-13 : Could not find note to be tied / Error in line-char 17-13 : Could not find note to be tied / Error in line-char 18-13 : Could not find note to be tied | False |
| C0651 | 96.8 | Rachmaninoff | Prelude (S.Rachmaninoff Op.23.No.6) | abc2midi_Error x6 | Error in line-char 18-68 : Could not find note to be tied / Error in line-char 25-68 : Could not find note to be tied / Error in line-char 68-68 : Could not find note to be tied | True |
| C0916 | 96.4 | Scarlatti, D. | D. Scarlatti Sonata in C (K159) | abc2midi_Error x1 | Error in line-char 26-32 : Could not find note to be tied | True |
| C0189 | 96.4 | Haydn | Haydn: Sonata in C Major HOB.XVI:7 | abc2midi_Error x6 | Error in line-char 19-83 : Rolls and trills not supported in chords / Error in line-char 19-85 : Rolls and trills not supported in chords / Error in line-char 39-43 : '!' or '+' in middle of line ignored | False |
| C0445 | 96.3 | Scarlatti, D. | Scarlatti: Sonata K. 63 | abc2midi_Error x4 | Error in line-char 20-36 : Could not find note to be tied / Error in line-char 21-36 : Could not find note to be tied / Error in line-char 21-36 : Could not find note to be tied | False |
| C0561 | 96.3 | Mozart | Mozart's Favorite Waltz | abc2midi_Error x4 | Error in line-char 18-60 : Malformed note : expecting a-g or A-G / Error in line-char 22-56 : Malformed note : expecting a-g or A-G / Error in line-char 23-41 : Malformed note : expecting a-g or A-G | False |
| C0072 | 96.1 | Haydn | Haydn - Sonata in E minor Hob XVI/34 Movement I | abc2midi_Error x3;bar_warnings x28 | Error in line-char 19-10 : Rolls and trills not supported in chords / Error in line-char 19-12 : Rolls and trills not supported in chords / Error in line-char 84-63 : Cannot find note before tie | True |
| C0327 | 96.0 | Beethoven | Rondo a Capriccio Rage over a lost Penny Beethoven op 129 | abc2midi_Error x15;bar_warnings x14 | Error in line-char 257-1 : 3 b is not a power of 2 / Error in line-char 257-18 : 3 b is not a power of 2 / Error in line-char 260-1 : 3 b is not a power of 2 | True |
| C0205 | 96.0 | Joplin | Eugenia - Scott Joplin - 1905-6 | abc2midi_Error x8 | Error in line-char 19-24 : Could not find note to be tied / Error in line-char 22-24 : Could not find note to be tied / Error in line-char 24-24 : Could not find note to be tied | False |
| C0860 | 96.0 | Joplin | Something Doing. | abc2midi_Error x3 | Error in line-char 25-6 : Cannot find note before tie / Error in line-char 25-6 : Cannot find note before tie / Error in line-char 25-6 : Cannot find note before tie | False |
| C1251 | 95.9 | Joplin | Entertainer | abc2midi_Error x8;bar_warnings x212 | Error in line-char 69-73 : 60 b is not a power of 2 / Error in line-char 71-18 : 60 b is not a power of 2 / Error in line-char 97-77 : 20 b is not a power of 2 | True |
| C0812 | 95.9 | Brahms | Hungarian Dance No 5 in F Minor | abc2midi_Error x6 | Error in line-char 23-0 : Unrecognized chord name "In" / Error in line-char 23-27 : Unrecognized chord name "Tempo" / Error in line-char 29-0 : Unrecognized chord name "rit." | True |
| C0036 | 95.8 | Brahms | Brahms Intermezzo Op. 118 No. 2 (A Major) [unedited] | abc2midi_Error x2 | Error in line-char 73-47 : Could not find note to be tied / Error in line-char 73-47 : Could not find note to be tied | True |
| C0444 | 95.8 | Mozart | Viennese Sonatina No 5 in F Major I Adagio K 439b - Mozart | abc2midi_Error x1 | Error in line-char 25-63 : Cannot find note before tie | False |
| C0790 | 95.7 | Schumann, R. | Concert Étude after Paganini's 2nd Caprice - R. Schumann Op. 10 No. 5 | abc2midi_Error x1 | Error in line-char 95-45 : Could not find note to be tied | True |
| C0619 | 95.7 | Mozart | Donne mie la fate a tanti (piano-vocal score) | abc2midi_Error x1;bar_warnings x10 | Error in line-char 191-16 : Could not find note to be tied | False |
| C0173 | 95.7 | Joplin | Kismet Rag - Joplin and Hayden - 1913 | abc2midi_Error x2 | Error in line-char 33-68 : Could not find note to be tied / Error in line-char 33-68 : Could not find note to be tied | False |
| C0046 | 95.6 | Joplin | Fig Leaf Rag Scott Joplin 1908 | abc2midi_Error x14 | Error in line-char 20-45 : Could not find note to be tied / Error in line-char 20-45 : Could not find note to be tied / Error in line-char 26-45 : Could not find note to be tied | False |
| C0090 | 95.5 | Mozart | Mozart Fantasy in D minor K397 | bar_warnings x42 |  | False |
| C0101 | 95.3 | Chopin | Mazurka in D major Op. 33 No. 2 - Frédéric Chopin - 1838 | abc2midi_Error x9 | Error in line-char 32-41 : Could not find note to be tied / Error in line-char 32-41 : Could not find note to be tied / Error in line-char 32-41 : Could not find note to be tied | False |
| C0239 | 95.3 | Schumann, R. | Schumann- Schlummerlied | abc2midi_Error x4 | Error in line-char 55-97 : Could not find note to be tied / Error in line-char 76-97 : Could not find note to be tied / Error in line-char 94-97 : Could not find note to be tied | True |
| C0094 | 94.9 | Mozart | Mozart Sonata No.8 KV.310 1st | abc2midi_Error x11 | Error in line-char 76-19 : Could not find note to be tied / Error in line-char 117-19 : Could not find note to be tied / Error in line-char 169-19 : Could not find note to be tied | True |
| C0461 | 94.8 | Brahms | Intermezzo Op. 116 No. 2 (Johannes Brahms) | abc2midi_Error x16 | Error in line-char 26-89 : Could not find note to be tied / Error in line-char 27-89 : Could not find note to be tied / Error in line-char 55-89 : Could not find note to be tied | True |
| C0430 | 94.8 | Mozart | Wolfgang Amadeus Mozart - Morgen kommt der Weihnachtsmann | abc2midi_Error x1;bar_warnings x24 | Error in line-char 148-54 : Could not find note to be tied | True |
| C0039 | 94.5 | Joplin | Pine Apple Rag - Scott Joplin - 1908 | abc2midi_Error x7 | Error in line-char 43-38 : Could not find note to be tied / Error in line-char 43-38 : Could not find note to be tied / Error in line-char 44-38 : Could not find note to be tied | False |
| C0393 | 94.4 | Bach, J.S. | Bach js capriccio bwv 992 | bar_warnings x24 |  | True |

## gate reasons among zeroed pdmx_canon

| gates | count |
|---|---|
| abc2midi_Error | 274 |
| abc2midi_Error;bar_warnings | 126 |
| bar_warnings | 81 |
| abc2midi_Error;no_total:no_notes | 3 |
| abc2midi_Error;blank_line | 1 |

## feature blame, passing pdmx_canon (n=958); total mean loss 22.03

| index | mean_pts_lost | pct_pieces_losing>=1pt | direction_counts |
|---|---|---|---|
| loss_dist_hist(JS) | 5.34 | 100.0 | {} |
| loss_polyphony_rate | 2.47 | 61.0 | {'high': 447, 'very-low': 223} |
| loss_polyphony_mean | 1.39 | 36.0 | {'low': 394} |
| loss_local_key_certainty | 1.32 | 50.0 | {'low': 672} |
| loss_tension_peaks | 1.16 | 37.0 | {'low': 380, 'high': 44} |
| loss_note_len_entropy | 1.09 | 37.0 | {'low': 467} |
| loss_rhythm_surprisal | 1.08 | 33.0 | {'low': 323, 'high': 42} |
| loss_key_certainty | 1.05 | 44.0 | {'low': 689} |
| loss_pitch_min | 0.94 | 29.0 | {'high': 311, 'low': 7} |
| loss_roughness_p90 | 0.94 | 24.0 | {'low': 224, 'high': 50} |
| loss_qualified_note_rate | 0.86 | 39.0 | {'high': 329, 'low': 126} |
| loss_self_similarity | 0.83 | 22.0 | {'low': 234, 'high': 26} |
| loss_voice_leading_cost | 0.77 | 27.0 | {'low': 300, 'high': 21} |
| loss_ioi_mean | 0.76 | 25.0 | {'high': 327, 'low': 7} |
| loss_harmonicity_mean | 0.64 | 15.0 | {'low': 149, 'high': 25} |
| loss_pitch_range | 0.61 | 22.0 | {'low': 233, 'high': 23} |
| loss_note_density | 0.49 | 18.0 | {'low': 243, 'high': 6} |
| loss_pitch_in_scale | 0.26 | 10.0 | {'high': 63, 'low': 46} |
| loss_n_chan | 0.04 | 2.0 | {'low': 15} |

## feature blame, bottom decile of passing pdmx_canon (n=95, reward < 0.64)

| index | mean_pts_lost |
|---|---|
| loss_dist_hist(JS) | 7.92 |
| loss_polyphony_rate | 4.58 |
| loss_roughness_p90 | 3.78 |
| loss_polyphony_mean | 3.44 |
| loss_harmonicity_mean | 3.04 |
| loss_pitch_min | 2.72 |
| loss_note_len_entropy | 2.5 |
| loss_self_similarity | 2.5 |
| loss_pitch_range | 2.39 |
| loss_local_key_certainty | 2.24 |
| loss_tension_peaks | 2.16 |
| loss_ioi_mean | 2.07 |
| loss_rhythm_surprisal | 2.06 |
| loss_voice_leading_cost | 1.94 |
| loss_qualified_note_rate | 1.84 |
| loss_note_density | 1.78 |
| loss_key_certainty | 1.62 |
| loss_pitch_in_scale | 0.85 |
| loss_n_chan | 0.45 |

## length effects (pdmx_canon scored)

spearman(n_note, ungated) 0.403
spearman(n_note, f_tension_peaks) 0.674
pct with tension_peaks > p90 (96): 10.4
zeroed% by n_note quartile: {Interval(1.999, 314.75, closed='right'): 0.14, Interval(314.75, 806.5, closed='right'): 0.21, Interval(806.5, 1816.75, closed='right'): 0.39, Interval(1816.75, 36850.0, closed='right'): 0.6}
median ungated by n_note quartile: {Interval(1.999, 314.75, closed='right'): 76.05, Interval(314.75, 806.5, closed='right'): 80.75, Interval(806.5, 1816.75, closed='right'): 85.65, Interval(1816.75, 36850.0, closed='right'): 85.65}
n_chan distribution: {4.0: 554, 2.0: 259, 3.0: 251, 5.0: 149, 6.0: 117, 7.0: 47, 8.0: 29, 1.0: 20, 9.0: 6, 10.0: 5, 12.0: 3}