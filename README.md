# Petri Isles — records

Thirty AI islanders live on five small islands. One rule changes at a time. Every experiment is written down and made public **before** it runs, and every run log is published after. The videos are on the YouTube channel *Petri Isles*, narrated by The Archivist, an AI chronicler.

This repository holds only what is needed to trust the results. The simulation engine is private; its exact version is committed by hash (see `METHOD.md`).

| file | what |
|---|---|
| `EP01/prereg.md` | the EP01 pre-registration: question, hypothesis, arms, seeds, metric, thresholds, canon rule, stopping rule, known limitations |
| `EP01/calibration.md` | how the world's numbers were tuned **before** any hypothesis (no-hypothesis runs, never canon) |
| `EP01/rules.yaml`, `EP01/lexicon_watch.yaml` | the world's rules and the outside-world word list exactly as used in EP01 |
| `EP01/ep01_verdict.py` | computes the primary metric and the pre-registered verdict straight from the logs (Python standard library only) |
| `ledger.md` | The Archivist's predictions, written before each run, scored after |
| `METHOD.md` | what the islanders read each season, and how the engine version is committed |
| Releases | every run's gzipped JSONL event log (calibration runs included) + `SHA256SUMS.txt` |
| Issues | the public pre-registration post of each episode (timestamped by GitHub) |

## Check a verdict yourself
```bash
# download the EP01 release assets into ./logs, then:
python EP01/ep01_verdict.py logs --rules EP01/rules.yaml --engine-tree <hash from EP01/prereg.md>
```

## Licences
Records and documents: **CC BY 4.0** (`LICENSE`). Analysis scripts (files marked `SPDX-License-Identifier: MIT`): **MIT** (`LICENSE-MIT`). Attribution: "Petri Isles".

*All findings are about language-model islanders in this simulation — not about people.*
