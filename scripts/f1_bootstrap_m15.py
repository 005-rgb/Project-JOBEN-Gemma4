#!/usr/bin/env python3
"""F1.8: Bootstrap >=10.000 resampel M15 untuk memilih L bulat terbesar in [4..10]."""
import argparse, json, math, pathlib, random

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m12", required=True)
    ap.add_argument("--overhead-s", type=float, default=600.0)
    ap.add_argument("--horizon-s", type=float, default=39600.0)
    ap.add_argument("--resamples", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    data = json.loads(pathlib.Path(args.m12).read_text(encoding="utf-8"))
    times = [float(t["elapsed_s"]) for t in data["tasks"]]
    rng = random.Random(args.seed)

    report = {}
    chosen_L = 4
    for L in range(4, 11):
        cap = L * 60.0
        capped = [min(x, cap) for x in times]
        ok_both = True
        scen_stats = {}
        for name, n_tasks, mult in (("scen_a_120x1.0", 120, 1.0), ("scen_b_150x1.2", 150, 1.2)):
            totals = sorted(
                args.overhead_s + mult * sum(rng.choice(capped) for _ in range(n_tasks))
                for _ in range(args.resamples)
            )
            p99 = totals[int(0.99 * len(totals)) - 1]
            scen_stats[name] = {"p99_s": round(p99, 1), "pass": p99 <= args.horizon_s}
            if p99 > args.horizon_s:
                ok_both = False
        report[f"L={L}m"] = {"pass_both": ok_both, **scen_stats}
        if ok_both:
            chosen_L = L

    out = {"chosen_L_minutes": chosen_L, "horizon_s": args.horizon_s, "details": report}
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
