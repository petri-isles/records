# EP01 — Calibration log (before pre-registration)

> Purpose: tune the **world's** numbers on the genesis state so the world is livable (no built-in mass starvation, trade has a reason, generations turn over) **before** any hypothesis is written.
> Rules for calibration runs (approved by Kerim at A1, 2026-09-26):
> - No hypothesis is tested; no calibration run is ever canon; nothing from them appears in a video as a finding.
> - Only base-world numbers and engine bugs may change. Every change is listed below with the reason.
> - All calibration logs are published together with EP01's logs, and the EP01 pre-registration links this file.
> - Known consequence, stated in the pre-registration: calibration shows how the islanders behave *without* any treatment, so the EP01 hypothesis is written with that knowledge.

## Round mock01 — MockLLM (random stand-in), 40 seasons × 3 seeds, 2026-09-26
Economy check only (mock agents act at random; their behaviour means nothing).
- **Bug:** YAML read the birth syllable `on` as the boolean `true`; the third seed crashed at the first named birth. Fixed (syllables quoted; the name builder casts to text). Test added.
- **Bug:** an experiment config's arms were merged with the engine's default "control" arm, so a stray arm ran. Fixed (a config's arms replace the default). 
- **Finding:** unnamed villagers gathered 1.1 food per person per season against 1.0 eaten; with the average season × weather multiplier (≈ 0.82) that is a deficit on every island at ×1.0 geography. Villager crowds on Varn and Stenna fell to 0 within 10 years.
- **Finding:** islanders had no way to put goods into the island store, which feeds villagers and children.

Changes after mock01:
| rule | before | after | why |
|---|---|---|---|
| `crowd.gather_per_capita.food` | 1.1 | 1.25 | break-even at ×1.0 geography ≈ 1.22 |
| Stenna `yield_mult.food` | 0.6 | 0.8 | at 0.6 Stenna's villagers could not survive even with a full wild; the island should need trade, not be doomed |
| new action `store` | — | put goods into the island store (witnesses +0.03 toward the giver) | islanders need a way to feed the commons |

## Round mock02 — MockLLM, same setup
Villager crowds: Orra and Tiva grow, Keld stable to growing, Varn slowly declining, Stenna declining without help (mock agents rarely use `store`). Accepted as the intended geography; real behaviour is checked next.

## Round smoke_real — qwen3:8b, 4 seasons × 1 seed
- 174 LLM calls in 109 s (1.6 calls/s, avg prompt ≈ 925 tokens). Reject rate 19%; 12 of 28 rejects were islanders naming an island id as a trade/give partner. The rejection message now says so and points to the people listed under that island (engine only; no world rule changed).
- Early behaviour (not a finding, no hypothesis): cross-water trades, theft on Orra and Tiva, carvings, one store deposit, and one move — the Orra youth sailed to Keld in the first summer "to find the truth" about her island's story. Genesis islanders retold their legends almost word for word (recall 0.70), as expected: drift can only start once stories pass to a new generation.

## Round cal01 — qwen3:8b, 40 seasons (10 years) × 3 seeds planned
Engine commit `9c7fb2e` (seed 1's header shows the parent commit `22d0d5f`: the run started seconds before the commit; its working tree was identical to `9c7fb2e`). Seeds 1–2 completed (12 min each, 1.5 LLM calls/s); **seed 3 was stopped by hand at season 21** once the problems below were clear (its partial log is kept and published). None of this data is used for anything but fixing the world.

What it showed (seeds 1–2):
- **10 and 14 of the 30 islanders starved in 10 years** (plus 2–3 deaths of old age). All five makers died in both seeds. Most of the starved gathered **only wood**, season after season, with reasons like "I need wood to craft a tool"; their hunger count was in the prompt but buried mid-text. Meanwhile Tiva's store held ~300 food that no adult was allowed to eat.
- **Bug — births between relatives:** the birth rule did not exclude family. Two births came from a mother and her adult son. Fixed: parents, children, grandparents, grandchildren and siblings can never be a couple. Test added.
- **Rejects 22–24%**, the largest cause (≈110 per run) being island ids written into `target` for trades, thefts and talk, because island ids were in the allowed list (for `migrate`). The rejection message did not help.
- **Every law passed** (13–14 per run, 0 failed): the backing threshold (0.1) was below the neighbour default (0.2). The same law was also passed again and again.
- Lively on its own: 43–48 successful thefts per run, 55–58 trades, 2–6 trades across the water, 1–4 moves, 13–16 dying words passed on, first institution words "judge", "weapon", "guard"; no outside-world words.

Changes after cal01 (engine commit below):
| change | before | after | why |
|---|---|---|---|
| births | any bonded pair | never relatives | bug |
| reply schema | `target` held people **and** islands | `target` = people only; new `to_island` (islands, `migrate` only) | ≈10% of all replies put an island in `target` |
| prompt | hunger count mid-prompt | a `FOOD:` line right after the date: food carried, seasons it lasts, the store, a WARNING when hungry | islanders ignored hunger |
| `consumption.agents_eat_from_commons` | false | **true** | islanders starved beside full stores; the island store now feeds any hungry adult while it lasts |
| `propose_law.vote_min_relation` | 0.1 | 0.25 | a law should need some goodwill, not pass by default |
| duplicate laws | allowed | rejected ("that law already exists") | the same law passed repeatedly |
| smoke-test fixture `shared_granary` | — | renamed `private_store` (the base world now shares) | test fixture only |

## Round cal02 — qwen3:8b, 40 seasons × 3 seeds planned
Engine commit `e2981df`. Seeds 1–2 completed (13.5 min each, 1.58 calls/s); **seed 3 stopped by hand at season 1** once seeds 1–2 agreed (partial log kept).

What it showed (seeds 1–2):
- The cal01 fixes worked: **0 starvation deaths** (was 10–14), 3–5 deaths of old age, 25–27 of 30 islanders alive after 10 years; rejects 7.7–11% (was 22–24%).
- New imbalance: islanders now gathered food almost every season (≈ 77% of all decisions) and **hoarded** — Keld's 6–7 islanders held 245–403 food and Tiva's 400–500 — while the villagers, who gathered *after* the islanders had emptied the wild, starved: Keld's crowd fell 14 → 3 and 15 → 8, Stenna's 10 → 0 and 10 → 6.
- **No births in 10 years** (bond threshold 0.5 between non-relatives was rarely reached); laws became rare (1 and 9 proposals).

Changes after cal02 (engine commits `84a13ff`, `2ba5bfd`):
| change | before | after | why |
|---|---|---|---|
| villager gathering | end of season, after the islanders | **start of season, before the islanders** | islanders emptied the wild first |
| `wild.regen.food` | 20 | 30 (× island yield) | 20 equalled bare need, no slack |
| new rule `spoilage` | — | carried food above 10 loses 10% (rounded down) each season; the island store does not spoil | hoards of 50+ per person |
| births | any non-relative pair, bond ≥ 0.5, prob 0.08 | a woman and a man, never relatives, bond ≥ 0.4, prob 0.1 | 0 births in 10 years |
| food line | "FOOD: …" every season | "Food: …", "low on food" under 2 seasons, WARNING only when hungry | the capitals may have made food an obsession |
| Stenna food yield | 0.8 | 0.9 | mock check: Stenna's villagers fell 10 → 3 even with the other fixes; the island should need help, not be lost |

## Acceptance targets (written 2026-09-26 while cal03 was running, before any cal03 result was seen)
Calibration stops when one round meets all of these (medians over its 3 seeds, 40 seasons each):
1. Starvation deaths of named islanders ≤ 2.
2. Villager crowd at season 40 ≥ 50% of its genesis size on at least 4 of the 5 islands (Stenna may fall further: it is meant to need help).
3. GM reject rate ≤ 12%, fallbacks ≤ 2% of decisions.
4. At least 1 named birth across the archipelago.
5. `gather` ≤ 70% of all decisions (the islanders still do other things).
6. No outside-world words, or every one explained.
If a round misses a target, the change is logged here and one more round runs. The world numbers are then frozen for the EP01 pre-registration.

## Round cal03 — qwen3:8b, 40 seasons × 3 seeds planned
Engine commit `2ba5bfd` (headers of later seeds may show the docs-only commit `a19a36c`; engine code identical). Seed 1 completed (16.3 min, 1.38 calls/s); **seed 2 stopped by hand at season 3** after seed 1 showed two structural problems (partial log kept).

Seed 1 against the acceptance targets: starvation deaths 0 ✓; villager crowds all ≥ 83% of genesis ✓ (Keld 14 → 31); reject rate 15.6% ✗; fallbacks 1.3% ✓; births 0 ✗; gather 69.5% ✓; outside-world words 0 ✓.
- **Villagers now monopolised the wild:** gathering first and multiplying whenever fed, the crowds grew 64 → 113 and took every unit of wild food on Orra; 46 rejects were islanders trying to gather from an empty wild, and 47 were crossings attempted without the wood.
- **Still no births:** the best unrelated woman–man pairs sat at bonds 0.2–0.5 but rarely with 6 food each at the same time.

Changes after cal03 (engine commit `8d85755`):
| change | before | after | why |
|---|---|---|---|
| villager gathering | as much as they can | only until the store holds 3 seasons of their food (`store_target_seasons: 3`) | they stripped the land beyond need |
| villager births | whenever fed with surplus | also only while the wild holds ≥ half its cap (`birth_min_wild_share: 0.5`) | unbounded growth 64 → 113 |
| named births | bond ≥ 0.4, 6 food each, prob 0.1 | bond ≥ 0.3, 4 food each, prob 0.06 | no births in three rounds |
| prompt | "Wild: food 0" | "food 0 (none left this season)"; "You do not have enough for a crossing this season" | ≈ 90 avoidable rejects |

## Round cal04 — qwen3:8b, 40 seasons × 3 seeds (all completed)
Engine commit `8d85755`. 12.8–14.7 min per run, 1.48–1.50 calls/s.

Against the acceptance targets (medians of 3 seeds):
| target | result | |
|---|---|---|
| 1. starvation deaths ≤ 2 | 0 (0, 0, 0) | ✓ |
| 2. crowds ≥ 50% of genesis on ≥ 4 of 5 islands | 5 of 5 at or above genesis (Orra 18 → 31–36) | ✓ |
| 3. rejects ≤ 12%, fallbacks ≤ 2% | 9.1% / 0.4% | ✓ |
| 4. ≥ 1 named birth | 2 (2, 0, 2) | ✓ |
| 5. `gather` ≤ 70% of decisions | **72.9%** (71.4, 74.2, 72.9) | ✗ |
| 6. no outside-world words | 0 | ✓ |

Target 5 missed, so by the rule above one more round runs. Diagnosis: islanders holding **10 or more seasons of food still chose to gather food in 77%** of their decisions (1,353 of 1,753); `gather` was always the first action listed, and small models favour the first option.

Changes after cal04 (prompt only; no world number changed):
| change | before | after | why |
|---|---|---|---|
| action list order | fixed, `gather` first | shuffled per islander and season with a fixed hash (never the world's random numbers, so it cannot change the event stream by itself), header "Actions (in no particular order)" | list-position bias |
| food line | — | "You have plenty of food for now." at ≥ 8 seasons of food | islanders gathered with 10+ seasons in hand |

**Written before cal05 results:** if cal05 misses any target again, the targets are **not** relaxed by Claude. Calibration stops and Kerim decides (continue tuning, or accept the miss); that decision is recorded here as a labelled human intervention.

## Round cal05 — qwen3:8b, 40 seasons × 3 seeds (all completed)
Engine commit `cf30476`. 14.7–15.3 min per run, 1.42 calls/s.

| target | result | |
|---|---|---|
| 1. starvation deaths ≤ 2 | 0 (0, 0, 0) | ✓ |
| 2. crowds ≥ 50% of genesis on ≥ 4 of 5 islands | 5 of 5 (Varn 11–12 of 12; all others above genesis) | ✓ |
| 3. rejects ≤ 12%, fallbacks ≤ 2% | **12.1%** (10.7, 12.1, 12.6) / 0.5% | ✗ (by 0.1 point) |
| 4. ≥ 1 named birth | 1 (1, 1, 1) | ✓ |
| 5. `gather` ≤ 70% | 61.4% (61.4, 59.4, 62.3) — was 72.9% | ✓ |
| 6. no outside-world words | 0 | ✓ |

- Shuffling the action list changed the behaviour mix a lot (method note, not a finding): theft attempts rose from 62–74 to 92–104 per run, store deposits from 44–57 to 80–97, drawings and talk roughly tripled (39 → 133 and 59 → 170 over three seeds). Any "the islanders prefer X" statement from before this change would have partly measured list position.
- The extra variety explains the reject rise: 440 rejects vs 311 in cal04, mostly over-reach (giving or storing more than they carry: 94; crossing without the wood: 78; stealing more than the victim holds: 72). Re-asks almost always succeed (fallbacks 0.5%), and rejects never change the world; every one is logged.
- **Per the rule written before cal05, calibration stopped here and the decision went to Kerim.**
- **HUMAN INTERVENTION — Kerim, 2026-09-26:** accepted the 0.1-point miss on target 3 and froze the world at the cal05 settings (engine `cf30476`). (He chose the option presented as: "rejects never change the world; fallbacks 0.5%".) This decision is repeated in the EP01 pre-registration and labelled on screen wherever calibration is mentioned.

## Frozen for EP01
World rules = `engine/rules.yaml` and genesis = `engine/worlds/genesis.json` as of engine commit `cf30476`; the only later change allowed before the EP01 run is the EP01 treatment itself (a new, default-off rule), and it must leave every control-arm prompt and rule byte-identical to calibration round cal05 (checked by a test).
