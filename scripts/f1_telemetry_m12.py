#!/usr/bin/env python3
"""F1.5: Ekstraktor telemetri M12 dari direktori hasil swegemma eval."""
import argparse, json, pathlib, re

PROTECTED_RE = re.compile(r"(^|/)(tests?|testing)/|(^|/)test_[^/]+\.py$|_test\.py$|(^|/)(conftest\.py|pytest\.ini|pyproject\.toml|tox\.ini|setup\.cfg)$")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--out", default="experiments/m12_report.json")
    args = ap.parse_args()

    rdir = pathlib.Path(args.results_dir)
    tr_file = rdir / "task_results.jsonl"
    rows = [json.loads(l) for l in tr_file.read_text(encoding="utf-8").splitlines() if l.strip()]

    per_task = []
    for r in rows:
        iid = r["instance_id"]
        patch_p = rdir / "patches" / f"{iid}.patch"
        patch_txt = patch_p.read_text(encoding="utf-8") if patch_p.exists() else ""
        touched = re.findall(r"^diff --git a/(\S+) b/(\S+)", patch_txt, flags=re.M)
        junk = [b for _, b in touched if PROTECTED_RE.search(b)]

        trace_p = rdir / "traces" / f"trace_{iid}.json"
        edit_not_found = 0
        thinking_tokens = 0
        if trace_p.exists():
            raw = trace_p.read_text(encoding="utf-8")
            edit_not_found = raw.count("FileEditError")
            try:
                tdata = json.loads(raw)
                thinking_tokens = int(tdata.get("thinking_tokens", 0) or 0)
            except Exception:
                pass

        per_task.append({
            "instance_id": iid,
            "resolved": bool(r.get("resolved", False)),
            "elapsed_s": float(r.get("elapsed_seconds", r.get("duration_seconds", 0.0))),
            "tool_calls": int(r.get("tool_calls", 0)),
            "empty_patch": len(patch_txt.strip()) == 0,
            "diff_lines": len(patch_txt.splitlines()),
            "junk_files": junk,
            "edit_not_found": edit_not_found,
            "thinking_tokens": thinking_tokens,
            "over_budget": str(r.get("error", "")).lower().find("budget") >= 0 or str(r.get("error", "")).lower().find("timeout") >= 0,
        })

    n = max(1, len(per_task))
    summary = {
        "n_tasks": len(per_task),
        "resolution_rate": round(sum(t["resolved"] for t in per_task) / n, 4),
        "empty_patch_rate": round(sum(t["empty_patch"] for t in per_task) / n, 4),
        "junk_file_rate": round(sum(len(t["junk_files"]) > 0 for t in per_task) / n, 4),
        "edit_not_found_rate": round(sum(t["edit_not_found"] > 0 for t in per_task) / n, 4),
        "over_budget_rate": round(sum(t["over_budget"] for t in per_task) / n, 4),
        "mean_elapsed_s": round(sum(t["elapsed_s"] for t in per_task) / n, 2),
        "tasks": per_task,
    }
    pathlib.Path(args.out).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "tasks"}, indent=2))

if __name__ == "__main__":
    main()
