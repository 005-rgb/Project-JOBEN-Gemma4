#!/usr/bin/env python3
"""F1.4: Bangun submission uji mini di /tmp/v02_probe_sub untuk menguji V-02 & V-03."""
import argparse, pathlib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="/tmp/v02_probe_sub")
    ap.add_argument("--model", default="gemma-4-e4b-it-qat-w4a16-ct")
    args = ap.parse_args()

    out = pathlib.Path(args.out_dir)
    (out / "configs").mkdir(parents=True, exist_ok=True)
    (out / "prompts").mkdir(parents=True, exist_ok=True)
    (out / "skills" / "probe" / "scripts").mkdir(parents=True, exist_ok=True)

    (out / "agent.yaml").write_text(
        f"name: v02_v03_probe_agent\n"
        f"model: {args.model}\n"
        f"instruction: !include prompts/system.md\n"
        f"tools:\n"
        f"  - get_status\n"
        f"  - run_skill_script\n"
        f"  - submit_patch\n"
        f"skills:\n"
        f"  - skills/probe\n"
        f"generate_content_config: !include configs/sampling.yaml\n",
        encoding="utf-8",
    )
    (out / "eval_config.yaml").write_text(
        "evaluation:\n"
        "  timeout_seconds: 120\n"
        "  max_tool_calls: 10\n"
        "  max_time_minutes: 2\n"
        "  max_turns: 10\n",
        encoding="utf-8",
    )
    (out / "configs" / "sampling.yaml").write_text(
        "temperature: 0.0\n"
        "max_output_tokens: 2048\n"
        "thinking_config:\n"
        "  thinking_budget: 512\n"
        "  include_thoughts: false\n",
        encoding="utf-8",
    )
    (out / "skills" / "probe" / "SKILL.md").write_text(
        "---\n"
        "name: probe\n"
        "description: Diagnostic skill to verify Python execution and /workspace access.\n"
        "---\n"
        "Run `scripts/check_env.py` via `run_skill_script`.\n",
        encoding="utf-8",
    )
    (out / "skills" / "probe" / "scripts" / "check_env.py").write_text(
        "#!/usr/bin/env python3\n"
        "import os, pathlib, sys\n"
        "ws = pathlib.Path('/workspace')\n"
        "can_read_ws = ws.exists() and any(ws.iterdir())\n"
        "probe_file = pathlib.Path('/tmp/v02_probe_ok.txt')\n"
        "probe_file.write_text('OK_FROM_SKILL_SCRIPT', encoding='utf-8')\n"
        "ws_probe = ws / '_v02_ws_probe.tmp'\n"
        "ws_probe.write_text('OK_WS_WRITE', encoding='utf-8')\n"
        "ws_probe.unlink()\n"
        "print(f'PROBE_RESULT: py={sys.version.split()[0]} can_read_ws={can_read_ws} ws_write=True argv={sys.argv[1:]}')\n",
        encoding="utf-8",
    )
    (out / "prompts" / "system.md").write_text(
        "Execute these exact steps in order and do nothing else:\n"
        "1. Call `get_status` and note `tool_calls_used`.\n"
        "2. Load skill `probe` if required, then run `scripts/check_env.py` using `run_skill_script`.\n"
        "3. Call `get_status` again to check whether `tool_calls_used` increased by 1 or 0.\n"
        "4. Call `submit_patch` and finish with a 1-sentence summary.\n",
        encoding="utf-8",
    )
    print(f"Built V-02/V-03 probe submission at {out}")

if __name__ == "__main__":
    main()
