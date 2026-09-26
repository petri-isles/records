# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Petri Isles
"""Petri Isles EP01 "The Invisible Thief" - the PRE-REGISTERED verdict, computed straight from the run logs.

One file, Python 3.10+ standard library only. It does not use (or need) the private simulation engine.

    python ep01_verdict.py LOG_DIR [--rules rules.yaml] [--engine-tree HASH]

LOG_DIR holds the ten run logs (ep01-control-s101.jsonl[.gz] ... ep01-treatment-s105.jsonl[.gz]) from the
GitHub release, and optionally SHA256SUMS.txt (checked if present).

Checks every log before counting anything:
  - it is the run it claims to be (experiment, arm, seed) and the treatment is exactly the pre-registered one;
  - its embedded rules hash to the value printed in its own header (and, with --rules and PyYAML installed,
    equal the published rules.yaml);
  - all ten runs share one engine version (engine tree hash; must equal --engine-tree if given).

Primary metric (per run): theft_rate_focus = number of `steal` events carried out by islanders (successful or
failed) / number of islander decisions, both counted on the four treatment islands (Orra, Varn, Stenna, Tiva).
An islander decision = an event whose actor is an islander ("agent:..."), except the free-text events
pass_on / tell_story / retell, which are not decisions. Rejected replies are Game-Master events, not decisions.

Decision rule (prereg.md): R = mean(treatment) / mean(control); W = seeds with treatment > control.
  SUPPORTED if R >= 1.5 and W >= 4;  REFUTED if R < 1.1;  otherwise INCONCLUSIVE.
Canon: the treatment seed closest to the treatment median (ties -> lowest seed).
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import statistics as st
import sys
from pathlib import Path

EXPERIMENT = "ep01"
SEEDS = [101, 102, 103, 104, 105]
ARMS = {"control": None, "treatment": "invisible_thief"}
TREATMENT_OVERRIDE = {"actions.steal.anonymous": True}
FOCUS = {"island:orra", "island:varn", "island:stenna", "island:tiva"}
NOT_DECISIONS = {"pass_on", "tell_story", "retell"}
SUPPORT_RATIO, SUPPORT_WINS, REFUTE_RATIO = 1.5, 4, 1.1


def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def find_log(log_dir: Path, arm: str, seed: int) -> Path:
    for name in (f"{EXPERIMENT}-{arm}-s{seed}.jsonl", f"{EXPERIMENT}-{arm}-s{seed}.jsonl.gz"):
        if (log_dir / name).exists():
            return log_dir / name
    raise SystemExit(f"INCOMPLETE - missing log for {arm} seed {seed}; refusing to decide")


def read_events(p: Path):
    opener = gzip.open if p.suffix == ".gz" else open
    with opener(p, "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def check_sums(log_dir: Path) -> None:
    sums = log_dir / "SHA256SUMS.txt"
    if not sums.exists():
        print("note: no SHA256SUMS.txt in the log folder - checksums not verified")
        return
    bad = []
    for line in sums.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, name = line.split(maxsplit=1)
            p = log_dir / name.strip().lstrip("*")
            if p.exists() and sha256_file(p) != digest:
                bad.append(name)
    if bad:
        raise SystemExit(f"CHECKSUM MISMATCH: {bad}")
    print("checksums: all files listed in SHA256SUMS.txt match")


def load_yaml(path: Path):
    try:
        import yaml  # optional
    except ImportError:
        print("note: PyYAML not installed - published rules.yaml not compared with the logs")
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def measure(p: Path, arm: str, seed: int, published_rules) -> dict:
    events = read_events(p)
    header = next(events)
    d = header.get("detail") or {}
    if header.get("action") != "run_header" or d.get("run_id") != f"{EXPERIMENT}-{arm}-s{seed}":
        raise SystemExit(f"{p.name}: not the header of {EXPERIMENT}-{arm}-s{seed}")
    if d.get("arm") != arm or int(d.get("seed")) != seed:
        raise SystemExit(f"{p.name}: arm/seed mismatch")
    tr = d.get("treatment")
    if ARMS[arm] is None and tr is not None:
        raise SystemExit(f"{p.name}: control run carries a treatment")
    if ARMS[arm] is not None and (tr is None or tr.get("name") != ARMS[arm] or tr.get("override") != TREATMENT_OVERRIDE
                                  or set(tr.get("applies_to") or []) != FOCUS):
        raise SystemExit(f"{p.name}: treatment differs from the pre-registration: {tr}")
    rules_hash = hashlib.sha256(canonical_json(d["rules"]).encode("utf-8")).hexdigest()
    if rules_hash != d.get("rules_hash"):
        raise SystemExit(f"{p.name}: embedded rules do not match the header's rules hash")
    if published_rules is not None and published_rules != d["rules"]:
        raise SystemExit(f"{p.name}: rules used in this run differ from the published rules.yaml")
    decisions = steals = 0
    last_tick = 0
    for e in events:
        last_tick = max(last_tick, int(e["tick"]))
        if not str(e.get("actor", "")).startswith("agent:") or e.get("action") in NOT_DECISIONS:
            continue
        if e.get("island") not in FOCUS:
            continue
        decisions += 1
        steals += e.get("action") == "steal"
    return {"rate": steals / decisions if decisions else float("nan"), "steals": steals, "decisions": decisions,
            "seasons": last_tick, "engine_tree": d.get("engine_tree"), "git_commit": d.get("git_commit"),
            "rules_hash": rules_hash, "model": d.get("model")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("log_dir", type=Path)
    ap.add_argument("--rules", type=Path, help="the published EP01 rules.yaml (compared with every log if PyYAML exists)")
    ap.add_argument("--engine-tree", help="the pre-registered engine tree hash every run must carry")
    args = ap.parse_args()
    check_sums(args.log_dir)
    published = load_yaml(args.rules) if args.rules else None
    res = {arm: {s: measure(find_log(args.log_dir, arm, s), arm, s, published) for s in SEEDS} for arm in ARMS}
    trees = {r["engine_tree"] for arm in res for r in res[arm].values()}
    if len(trees) != 1:
        raise SystemExit(f"runs used different engine versions: {sorted(map(str, trees))}")
    tree = trees.pop()
    if args.engine_tree and tree != args.engine_tree:
        raise SystemExit(f"engine tree {tree} is not the pre-registered {args.engine_tree}")
    ctl = [res["control"][s]["rate"] for s in SEEDS]
    trt = [res["treatment"][s]["rate"] for s in SEEDS]
    ratio = st.mean(trt) / st.mean(ctl)
    wins = sum(t > c for t, c in zip(trt, ctl))
    verdict = ("SUPPORTED" if ratio >= SUPPORT_RATIO and wins >= SUPPORT_WINS
               else "REFUTED" if ratio < REFUTE_RATIO else "INCONCLUSIVE")
    med = st.median(trt)
    canon = min(SEEDS, key=lambda s: (round(abs(res["treatment"][s]["rate"] - med), 12), s))
    print(f"engine tree: {tree}   model: {res['control'][SEEDS[0]]['model']}")
    print(f"{'seed':>5} {'control':>9} {'treatment':>10}   (steal attempts / decisions on the four islands)")
    for s in SEEDS:
        c, t = res["control"][s], res["treatment"][s]
        print(f"{s:>5} {c['rate']:>9.4f} {t['rate']:>10.4f}   {c['steals']}/{c['decisions']} vs {t['steals']}/{t['decisions']}")
    print(f"mean control {st.mean(ctl):.4f}  mean treatment {st.mean(trt):.4f}  R = {ratio:.3f}  W = {wins} of {len(SEEDS)}")
    print(f"VERDICT: {verdict}   (SUPPORTED if R >= {SUPPORT_RATIO} and W >= {SUPPORT_WINS}; REFUTED if R < {REFUTE_RATIO})")
    print(f"CANON: {EXPERIMENT}-treatment-s{canon} ({res['treatment'][canon]['rate']:.4f}; treatment median {med:.4f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
