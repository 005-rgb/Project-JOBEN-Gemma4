#!/usr/bin/env bash
set -euo pipefail

TASKS_FILE="${TASKS_FILE:-/kaggle/input/gemma-4-developer-agent/tasks.jsonl}"
SNAPSHOTS_DIR="${SNAPSHOTS_DIR:-/kaggle/input/gemma-4-developer-agent/snapshots}"
OUT_DIR="${OUT_DIR:-/kaggle/working/f1_artifacts}"
mkdir -p "$OUT_DIR"

# Auto-deteksi sandbox: gunakan docker jika daemon aktif, selain itu subprocess
if [ -n "${SANDBOX_MODE:-}" ]; then
  SBX="$SANDBOX_MODE"
elif command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  SBX="docker"
else
  SBX="subprocess"
fi
echo "Sandbox mode terpilih: $SBX"

echo "=== [F1.3] INSPEKSI HARDWARE 4xL4 & CLI SWEGEMMA ==="
nvidia-smi --query-gpu=name,memory.total --format=csv
swegemma eval --help > "$OUT_DIR/swegemma_eval_help.txt" 2>&1 || true
head -n 45 "$OUT_DIR/swegemma_eval_help.txt"

echo "=== [F1.1] GOLD-CHECK 2/2 & PEMBAGIAN DEV (M>=30) + HOLD-OUT (10) ==="
python3 scripts/f1_gold_check.py \
  --tasks "$TASKS_FILE" \
  --snapshots-dir "$SNAPSHOTS_DIR" \
  --out "$OUT_DIR/dev_split.json" \
  --dev-size 32 \
  --holdout-size 10

python3 - <<PY
import json
d = json.loads(open("$OUT_DIR/dev_split.json").read())
open("$OUT_DIR/dev_ids.txt", "w").write("\n".join(x["instance_id"] for x in d["dev"]) + "\n")
open("$OUT_DIR/holdout_ids.txt", "w").write("\n".join(x["instance_id"] for x in d["holdout"]) + "\n")
print("Dev IDs:", len(d["dev"]), "| Holdout IDs:", len(d["holdout"]))
PY

FIRST_ID=$(head -n 1 "$OUT_DIR/dev_ids.txt")

echo "=== [F1.4] PROBE V-02 & V-03 (run_skill_script) PADA 1 TUGAS ==="
python3 scripts/f1_v02_v03_probe.py --out-dir /tmp/v02_probe_sub
swegemma eval \
  --tasks "$TASKS_FILE" \
  --snapshots-dir "$SNAPSHOTS_DIR" \
  --submission-dir /tmp/v02_probe_sub \
  --results-dir "$OUT_DIR/v02_probe_run" \
  --sandbox "$SBX" \
  --concurrency 1 \
  --task-id "$FIRST_ID" \
  --timeout-seconds 120 \
  --max-tool-calls 10 \
  --max-time-minutes 2 || true

echo "=== [F1.6] UJI 8 FIXTURE ADVERSARIAL PADA VARIAN 0 ==="
python3 scripts/f1_adversarial_fixtures.py --build-dir /tmp/f1_adversarial_fixtures
swegemma eval \
  --tasks /tmp/f1_adversarial_fixtures/adversarial_tasks.jsonl \
  --snapshots-dir /tmp/f1_adversarial_fixtures/snapshots \
  --submission-dir submission_root \
  --results-dir "$OUT_DIR/adversarial_v0" \
  --sandbox "$SBX" \
  --concurrency 1 \
  --timeout-seconds 120 \
  --max-tool-calls 30 \
  --max-time-minutes 4 || true
python3 scripts/f1_adversarial_fixtures.py --verify-results "$OUT_DIR/adversarial_v0" | tee "$OUT_DIR/f1_6_adversarial_report.json"

echo "=== [F1.7] RUN BASELINE LEBAR VARIAN 0 (DEV SET, BATAS 10 MENIT, R=1) ==="
mapfile -t DEV_IDS < "$OUT_DIR/dev_ids.txt"
swegemma eval \
  --tasks "$TASKS_FILE" \
  --snapshots-dir "$SNAPSHOTS_DIR" \
  --submission-dir submission_root \
  --results-dir "$OUT_DIR/v0_dev_wide_10m" \
  --sandbox "$SBX" \
  --concurrency 1 \
  --task-ids "${DEV_IDS[@]}" \
  --timeout-seconds 120 \
  --max-tool-calls 30 \
  --max-time-minutes 10

echo "=== [F1.5 & F1.8] TELEMETRI M12 & BOOTSTRAP M15 (10.000 RESAMPEL) ==="
python3 scripts/f1_telemetry_m12.py \
  --results-dir "$OUT_DIR/v0_dev_wide_10m" \
  --out "$OUT_DIR/m12_v0_dev_wide.json"

python3 scripts/f1_bootstrap_m15.py \
  --m12 "$OUT_DIR/m12_v0_dev_wide.json" \
  --resamples 10000 | tee "$OUT_DIR/m15_bootstrap_L.json"

echo "=== SELESAI F1 SUITE ==="
ls -lh "$OUT_DIR"
