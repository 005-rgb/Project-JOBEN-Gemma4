#!/usr/bin/env python3
"""F1.1: Gold-check §10.1 dan pembagian seimbang Dev (M>=30) + Hold-out (10)."""
import argparse, json, pathlib, random, re, shutil, subprocess, tarfile, tempfile
import xml.etree.ElementTree as ET

def norm_patch(txt: str) -> str:
    txt = (txt or "").replace("\r\n", "\n")
    return txt if txt.endswith("\n") else txt + "\n"

def apply_patch_file(patch_path: pathlib.Path, cwd: pathlib.Path) -> bool:
    for cmd in (
        ["git", "apply", str(patch_path)],
        ["git", "apply", "--recount", str(patch_path)],
        ["patch", "-p1", "--batch", "--forward", "-i", str(patch_path)],
    ):
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        if r.returncode == 0:
            return True
    return False

def extract_test_targets(test_patch: str):
    files = re.findall(r"^\+\+\+ b/(\S+)", test_patch, flags=re.M)
    target_files = sorted({b for b in files if b.endswith(".py")})
    test_funcs = sorted(set(re.findall(r"^\+\s*(?:async\s+)?def\s+(test_\w+)\s*\(", test_patch, flags=re.M)))
    return target_files, test_funcs

def parse_junit(xml_path: pathlib.Path):
    if not xml_path.exists():
        return None
    root = ET.parse(xml_path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    tests = sum(int(s.attrib.get("tests", 0)) for s in suites)
    failures = sum(int(s.attrib.get("failures", 0)) for s in suites)
    errors = sum(int(s.attrib.get("errors", 0)) for s in suites)
    skipped = sum(int(s.attrib.get("skipped", 0)) for s in suites)
    passed = tests - failures - errors - skipped
    return {"passed": passed, "failures": failures, "errors": errors, "skipped": skipped}

def find_snapshot(snapshots_dir: pathlib.Path, instance_id: str):
    for ext in (".tgz", ".tar.gz", ".tar"):
        cand = snapshots_dir / f"{instance_id}{ext}"
        if cand.exists():
            return cand
    matches = list(snapshots_dir.rglob(f"*{instance_id}*.t*gz"))
    return matches[0] if matches else None

def verify_single_task(task: dict, snap_path: pathlib.Path, timeout_s: int = 180):
    iid = task["instance_id"]
    target_files, test_funcs = extract_test_targets(task["test_patch"])
    if not target_files:
        return False, "no_target_test_files"

    with tempfile.TemporaryDirectory(prefix=f"gold_{iid[:18]}_") as tmp:
        tmp_p = pathlib.Path(tmp)
        ws_orig = tmp_p / "orig"
        ws_gold = tmp_p / "gold"
        ws_orig.mkdir()
        ws_gold.mkdir()

        with tarfile.open(snap_path, "r:*") as tf:
            tf.extractall(ws_orig, filter="data")
            tf.extractall(ws_gold, filter="data")

        # 1) Kode asli + test_patch WAJIB gagal (FAIL_TO_PASS)
        (tmp_p / "test.patch").write_text(norm_patch(task["test_patch"]), encoding="utf-8")
        if not apply_patch_file(tmp_p / "test.patch", ws_orig):
            return False, "test_patch_apply_failed_orig"

        cmd_base = [
            "python3", "-s", "-m", "pytest", *target_files,
            "-p", "no:anyio", "-o", "timeout=0", "-o", "python_classes=Test* *Test", "-q"
        ]
        env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "PYTHONSAFEPATH": "1", "PYTHONNOUSERSITE": "1"}
        r_orig = subprocess.run(cmd_base, cwd=ws_orig, env=env, capture_output=True, text=True, timeout=timeout_s)
        if r_orig.returncode == 0:
            return False, "orig_passed_unexpectedly"

        # 2) Kode + reference patch + test_patch WAJIB lulus 2/2 tanpa skipped
        (tmp_p / "gold.patch").write_text(norm_patch(task["patch"]), encoding="utf-8")
        for p_file in (tmp_p / "gold.patch", tmp_p / "test.patch"):
            if not apply_patch_file(p_file, ws_gold):
                return False, f"apply_failed_{p_file.name}"

        for run_idx in (1, 2):
            junit_xml = tmp_p / f"junit_{run_idx}.xml"
            cmd_gold = cmd_base + [f"--junitxml={junit_xml}"]
            r_gold = subprocess.run(cmd_gold, cwd=ws_gold, env=env, capture_output=True, text=True, timeout=timeout_s)
            stats = parse_junit(junit_xml)
            if r_gold.returncode != 0 or not stats:
                return False, f"gold_run{run_idx}_rc_{r_gold.returncode}"
            if stats["passed"] <= 0 or stats["failures"] > 0 or stats["errors"] > 0 or stats["skipped"] > 0:
                return False, f"gold_run{run_idx}_bad_junit_{stats}"

    return True, "ok_2of2"

def balanced_split(valid_tasks: list, dev_size: int = 32, holdout_size: int = 10, seed: int = 42):
    rng = random.Random(seed)
    by_repo = {}
    for t in valid_tasks:
        by_repo.setdefault(t["repo"], []).append(t)
    for r in by_repo:
        rng.shuffle(by_repo[r])

    total_needed = dev_size + holdout_size
    selected = []
    repos = sorted(by_repo.keys())
    while len(selected) < total_needed and any(by_repo.values()):
        for r in repos:
            if by_repo[r] and len(selected) < total_needed:
                selected.append(by_repo[r].pop())

    rng.shuffle(selected)
    holdout = selected[:holdout_size]
    dev = selected[holdout_size:holdout_size + dev_size]
    return dev, holdout

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="data/tasks.jsonl")
    ap.add_argument("--snapshots-dir", default="")
    ap.add_argument("--out", default="experiments/dev_split.json")
    ap.add_argument("--dev-size", type=int, default=32)
    ap.add_argument("--holdout-size", type=int, default=10)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    tasks = [json.loads(line) for line in pathlib.Path(args.tasks).read_text(encoding="utf-8").splitlines() if line.strip()]
    snap_dir = pathlib.Path(args.snapshots_dir) if args.snapshots_dir else None

    verified = []
    rejected = {}
    for t in tasks:
        if snap_dir and snap_dir.exists():
            sp = find_snapshot(snap_dir, t["instance_id"])
            if not sp:
                rejected[t["instance_id"]] = "snapshot_missing"
                continue
            ok, reason = verify_single_task(t, sp)
            if ok:
                verified.append({"instance_id": t["instance_id"], "repo": t["repo"]})
            else:
                rejected[t["instance_id"]] = reason
        else:
            t_files, _ = extract_test_targets(t["test_patch"])
            if t_files:
                verified.append({"instance_id": t["instance_id"], "repo": t["repo"]})

    dev, holdout = balanced_split(verified, args.dev_size, args.holdout_size, args.seed)
    out_obj = {
        "mode": "gold_verified_2of2" if (snap_dir and snap_dir.exists()) else "provisional_pre_snapshot",
        "seed": args.seed,
        "total_verified": len(verified),
        "dev_count": len(dev),
        "holdout_count": len(holdout),
        "dev": dev,
        "holdout": holdout,
        "rejected_summary": {v: list(rejected.values()).count(v) for v in set(rejected.values())},
    }
    pathlib.Path(args.out).write_text(json.dumps(out_obj, indent=2), encoding="utf-8")
    print(json.dumps({k: out_obj[k] for k in ("mode", "total_verified", "dev_count", "holdout_count", "rejected_summary")}, indent=2))

if __name__ == "__main__":
    main()
