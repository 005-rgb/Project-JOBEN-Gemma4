#!/usr/bin/env python3
"""F1.2: Benchmark infrastruktur §2.3 (31B, 12B, E4B QAT pada 4xL4 vLLM OpenAI endpoint)."""
import argparse, concurrent.futures, json, math, pathlib, statistics, time, urllib.request

def make_tokens_text(approx_tokens: int, salt: str = "") -> str:
    base = "def solve_issue(items, config=None):\n    if items is None:\n        return []\n    return [x for x in items if x]\n"
    repeats = max(1, (approx_tokens * 4) // len(base))
    return f"# SALT:{salt}\n" + (base * repeats)

def call_chat(base_url: str, model: str, prompt: str, max_tokens: int = 1024, thinking_budget: int = 0):
    t0 = time.perf_counter()
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": max_tokens,
        "stream": True,
    }
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    ttft = None
    chunks = 0
    with urllib.request.urlopen(req, timeout=300) as resp:
        for raw in resp:
            line = raw.decode("utf-8", errors="ignore").strip()
            if not line.startswith("data:") or line == "data: [DONE]":
                continue
            if ttft is None:
                ttft = time.perf_counter() - t0
            chunks += 1
    elapsed = time.perf_counter() - t0
    return {"ttft_s": ttft or elapsed, "elapsed_s": elapsed, "out_tokens_est": chunks}

def run_concurrent_batch(base_url: str, model: str, prompts: list, max_tokens: int):
    t_start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(prompts)) as ex:
        futs = [ex.submit(call_chat, base_url, model, p, max_tokens) for p in prompts]
        res = [f.result() for f in futs]
    wall_s = time.perf_counter() - t_start
    total_tok = sum(r["out_tokens_est"] for r in res)
    latencies = sorted(r["elapsed_s"] for r in res)
    ttfts = [r["ttft_s"] for r in res]
    p50 = statistics.median(latencies)
    p90 = latencies[min(len(latencies) - 1, math.ceil(0.9 * len(latencies)) - 1)]
    return {
        "concurrency": len(prompts),
        "wall_s": round(wall_s, 3),
        "agg_tok_per_s": round(total_tok / max(wall_s, 1e-6), 2),
        "per_stream_tok_per_s": round((total_tok / len(prompts)) / max(p50, 1e-6), 2),
        "ttft_mean_s": round(statistics.mean(ttfts), 3),
        "lat_p50_s": round(p50, 3),
        "lat_p90_s": round(p90, 3),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://127.0.0.1:8000/v1")
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", default="experiments/hw_bench.json")
    args = ap.parse_args()

    results = {"model": args.model, "unshared": {}, "shared_prefix_10": {}}
    for c in (1, 3, 4, 10):
        prompts = [make_tokens_text(8000, salt=f"u_{c}_{i}") for i in range(c)]
        results["unshared"][str(c)] = run_concurrent_batch(args.base_url, args.model, prompts, max_tokens=1024)

    # Uji V-25: 10 permintaan dengan prefiks identik 8k token + 2 baris penutup unik
    shared_prefix = make_tokens_text(8000, salt="SHARED_FUNNEL_PREFIX")
    shared_prompts = [
        f"{shared_prefix}\nMODUS: TULIS PATCH (branch_{i}).\nSimpan hasil hanya dengan write_file ke /tmp/cand/prop_{i}.txt."
        for i in range(10)
    ]
    results["shared_prefix_10"] = run_concurrent_batch(args.base_url, args.model, shared_prompts, max_tokens=1024)

    tps1 = results["unshared"]["1"]["agg_tok_per_s"]
    tps3 = results["unshared"]["3"]["agg_tok_per_s"]
    ttft_cold10 = results["unshared"]["10"]["ttft_mean_s"]
    ttft_shared10 = results["shared_prefix_10"]["ttft_mean_s"]
    results["gates"] = {
        "v18_conc3_vs_conc1_ratio": round(tps3 / max(tps1, 1e-6), 2),
        "v18_pass_ge_2_0": (tps3 / max(tps1, 1e-6)) >= 2.0,
        "v25_ttft_speedup_ratio": round(ttft_cold10 / max(ttft_shared10, 1e-6), 2),
    }
    pathlib.Path(args.out).write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
