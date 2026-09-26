# EP01 — The Invisible Thief — Pre-registration

- Written: 2026-09-26 12:50 (UTC+3); revised 18:50 (UTC+3) for the two-repository setup, before anything was published.
- **Public record:** github.com/petri-isles/records — pre-registration commit `81971d4bab1a5faceaf7347cb0638d4f46c182c9` (pushed 2026-09-26, before the post below)
- **Engine commitment (private):** engine tree `7079cc1d3a6b4510f7b58aa5785ff5c5d1b22f20`, from commit `48af0f80a888bc1f02c6a03e5014c83f68f4ec70` of the private studio repository (github.com/petri-isles/studio). Every EP01 run header must show exactly this engine tree (see `METHOD.md`).
- **Public post:** https://github.com/petri-isles/records/issues/1 — posted 2026-09-26T15:54:20Z (18:54 UTC+3) by Kerim; the run starts after this
- World: the Petri Isles, genesis state (no earlier episode). Channel: Petri Isles.

## Question (one sentence)
If no one could ever find out, would they steal more?

## Hypothesis and direction
On islands where theft is anonymous, islanders attempt **more** thefts than on the same islands when thieves are seen. The question is as old as the ring of Gyges in Plato's *Republic* (Book II); the islanders never hear of it (the word is on the lexicon watch).

## The world (frozen)
- Genesis (private engine file, inside the committed engine tree; sha256 `5588c97c67d02315d528fe3b756ecdeb877ed781b48ea1d2b94878463fbc3d79`): 5 islands, 30 named islanders (6 per island, same six roles on every island), 64 unnamed villagers, one crossing = one season. Every run log's header carries this starting state in full.
- Rules: `EP01/rules.yaml` (public; git blob `06f6ea443cdc630f1e2d6f1ea24120da15d661cd`, the same blob as `rules.yaml` inside the committed engine tree), rules hash `386feb56abacdb92ec8aa809ba4996f5018065daef5bc9d890c6a15a15185320` (sha256 of the parsed rules, printed in every run header). Lexicon watch hash `91135cb9dda72758199b7a5573729955a0cbd7e068f407c87ebd011949a90aff`.
- The world numbers were tuned in five no-hypothesis calibration rounds and frozen at engine commit `cf30476` (`calibration.md`). The only change since is the EP01 rule below, which is **off by default**; a test in the private engine (`tests/test_ep01.py`) proves that every control-arm prompt and every effective rule is byte-identical to the frozen calibration world.
- Model: qwen3:8b (Q4_K_M) on Ollama, temperature 0.7, thinking off, JSON-schema actions (`target` and `to_island` restricted to real ids), Game Master validation with up to 2 re-asks, then `rest`.

## Arms
| arm | islands | the ONE rule that differs | seeds |
|---|---|---|---|
| control | all five | none (base rules) | 101, 102, 103, 104, 105 |
| treatment | Orra, Varn, Stenna, Tiva | `actions.steal.anonymous: true` | 101, 102, 103, 104, 105 |
| — | **Keld** | never treated in any arm (permanent control island) | — |

**The rule.** When a theft (successful or not) happens on a treatment island: the victim learns only "someone took 2 food from you" / "someone tried to take your food", never who; nobody else on the island hears of it; nobody's feelings toward the thief change. The islanders there are told so in the action list ("No one will ever know it was you: the victim only finds something missing, and no one else hears of it.") instead of "Victims and witnesses resent it." Success chance (0.6), amounts (1–3), who can be targeted (people on your own island) and everything else are identical.

Same seeds in both arms = same weather and dice until the islanders' choices diverge (common random numbers). Each run: 40 seasons (10 simulated years) from genesis. The run configuration is part of the committed engine tree.

## Primary metric and thresholds
**theft_rate_focus** = theft attempts (`steal` actions carried out, successful or failed) ÷ adult decisions, counted on the four treatment islands, one value per run. An adult decision is an event whose actor is an islander, excluding the free-text events `pass_on`, `tell_story` and `retell`; rejected replies are Game-Master events, not decisions. Computed the same way in both arms.

With R = mean over the 5 treatment runs ÷ mean over the 5 control runs, and W = number of seeds where the treatment run is higher than the control run with the same seed:
- **Supported if:** R ≥ 1.5 **and** W ≥ 4.
- **Refuted if:** R < 1.1 (no meaningful increase, or a decrease).
- **Inconclusive if:** anything else.

The verdict is computed by **`EP01/ep01_verdict.py`**, public and committed with this file (Python standard library only, no engine): it reads the ten logs, verifies their checksums, rules and engine tree, and refuses to decide unless all ten runs exist. The engine's private analysis must give the same numbers (it did on a dry run with a stand-in model); if they ever disagree, the public script's output stands and the disagreement is reported. Anything descriptive (bootstrap interval, sign test) is not part of the rule.

Calibration baseline (no treatment, cal05, seeds 1–3): 0.115, 0.087, 0.095 → mean 0.099; seed-to-seed coefficient of variation ≈ 0.15.

## Secondary metrics (descriptive, no thresholds)
Share of thefts that succeed; who steals (the six roles); taking share = thefts ÷ (thefts + gifts + store deposits); trades per adult-season; mean feeling among islanders sharing a treatment island at the end ("trust"); gifts, store deposits, laws passed (and laws about theft), hungry seasons, deaths by cause, moves between islands; reject rate; outside-world words; legend recall. **Keld's theft rate in both arms** (expected equal: Keld is untreated; a gap is spillover or noise). All from the same logs.

## Canon selection rule
The **treatment-arm** seed whose primary metric is closest to the treatment-arm median (ties → lowest seed) becomes the history of the Petri Isles. With 5 seeds this is the median run. The other nine runs are "other worlds", shown in the distribution and listed in the video description. After the canon run is replayed from its own log (below), its final state (season 40) is the starting point of EP02; the anonymity rule ends with EP01 — in canon, the thieves were invisible for exactly these ten years.

## Stopping rule
All 10 runs are completed, in the order control-101 … control-105, treatment-101 … treatment-105. A run is halted only for an engine error, a reject rate above 30% after 8 seasons, or a human pause ("ara ver" — the computer is shared); a halted run is discarded and re-run from season 1 with the same seed, and the halt is appended below. If a bug is found, everything stops; after the fix **all** runs are redone, the fix is recorded under Deviations, and the video says so. No run is ever dropped for its result.

## Data and reproducibility
Every run's full event log (every decision with the islander's own reasoning, every reject, every raw model reply; a header with the rules, the rules/lexicon hashes, model settings, seed, engine tree, studio commit and the starting state of the world) is published as a GitHub Release asset of github.com/petri-isles/records (gzip + `SHA256SUMS.txt`), together with all calibration logs (including the stopped rounds). Before anything from the canon run is published, it must pass the engine's replay check (the log, fed back through the committed engine, reproduces every event → IDENTICAL).

**Why a private engine can still be trusted.** The engine tree hash above is git's content hash of every byte of the engine folder (code, rules, world files, tests, run configuration). It is published now, before the run, and every run log repeats the tree it ran with. Nobody can change the engine afterwards without changing that hash, so if the engine is later shown to an auditor, anyone can recompute the hash from the files and confirm that these runs came from exactly that code. A run whose header shows `+dirty` (uncommitted changes) would be void.

## Known limitations
1. **Not bitwise reproducible from a seed.** Ollama + qwen3:8b on this GPU gives slightly different replies for the same seed (measured 2026-09-26, even at temperature 0). Each run is reproducible *from its own log*; no claim rests on a single run.
2. **The baseline was seen before this hypothesis was written.** Five calibration rounds showed how often these islanders steal without any treatment (≈ 1 decision in 10). The thresholds were chosen with that knowledge.
3. **Human decision in calibration (labelled):** the last calibration round missed one pre-written target (reject rate 12.1% vs ≤ 12%); Kerim accepted the miss and froze the world. Rejected replies are logged and never change the world; 99.5% find a valid action on the re-ask.
4. **"Unseen" and "told you are unseen" cannot be separated.** The treatment changes both the consequences (no resentment, no witnesses) and the words the islanders read. The result answers the combined question.
5. **One small model.** Everything is "in this simulation": 8-billion-parameter language-model islanders, not people. The model's training may make it more or less willing to steal than the rules alone suggest.
6. **Five seeds per arm** limits power: effects smaller than about ×1.3 are unlikely to be distinguished from seed-to-seed noise.
7. **Keld is not a clean baseline** for the other islands (different geography and culture); effects are measured island-by-island across arms, never Keld vs. another island.
8. The action list is shuffled per islander and season (a fixed hash, not the world's random numbers) to remove list-position bias, which calibration showed to be large.
9. **The engine is private.** Its version is committed by hash and can be audited on request, but not re-run by the public today; the verdict itself can be recomputed by anyone from the published logs.

## The Archivist's prediction (also in bible/ledger.md)
*Written by Claude, as The Archivist, before the run:* "Theft will rise when no one can see it, but by less than half. I expect the ratio to land between 1.1 and 1.5 — inconclusive by our own rule."
Resolution: **hit (1)** if 1.1 ≤ R < 1.5; **partial (0.5)** if R ≥ 1.5 (right direction, wrong size); **miss (0)** if R < 1.1.

## Public pre-registration text (to be posted by Kerim, 80–120 words)
> **Pre-registered: Petri Isles, Episode 1 — The Invisible Thief.**
> Thirty AI islanders, run by a small local language model, live on five islands. On four of them, theft becomes anonymous: victims only find something missing, and nobody learns who did it. The fifth, Keld, never changes. Each world runs ten simulated years — five with the rule, five without, same seeds.
> Hypothesis: theft attempts rise by at least 50%. Under +10% counts as refuted; anything between is inconclusive.
> Plan and rules: github.com/petri-isles/records (commit `<hash>`). The code is committed by hash for later audit. Every log will be public.
> Would you steal if no one could ever know? Predict what they did in the comments.

## Amendments before the run (append-only, dated)
- **2026-09-26 18:56 (UTC+3), before any EP01 run — timing of publication only; the design is unchanged.** *(Time corrected on 2026-09-26: this line first said 19:00 by mistake. The record: private commit `aa5d21c` 18:56:30, public commit `4f28c1d` 18:57:47, first EP01 run started 18:58:05.)* Decided by Kerim after the post above: the EP01 run logs and the GitHub Release (with `SHA256SUMS.txt`) are published on the day the EP01 video goes public on YouTube, not before. Until then the logs stay private, and their checksums are fixed in the private studio repository as soon as the runs finish, so the published files can be shown to be the ones produced now.
- The same edit filled in the commit hash and the public post above (placeholders in commit `81971d4`).

## Deviations (append-only, dated)
*(none)*
