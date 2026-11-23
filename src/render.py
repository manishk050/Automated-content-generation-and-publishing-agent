"""Detached render driver outline.

Production renders with Remotion, landscape pillarboxed into vertical
1080x1920. The driver is detached and logs straight to a file, never
through tee or a process substitution pipe, because a broken pipe can
kill a long render at session teardown.

Demo mode prints the render plan and writes out/render-plan.json.
It does not render a video.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

VIDEO = {"width": 1080, "height": 1920, "fps": 30, "duration_seconds": 95}
AUDIO = {"sample_rate_hz": 48000, "note": "Downsample mastered audio to 48 kHz before AAC encode, never feed 192 kHz to the encoder."}


def build_render_plan(title="DEMO ONLY: The Hallway Light"):
    return {
        "title": title,
        "video": VIDEO,
        "audio": AUDIO,
        "frames": VIDEO["fps"] * VIDEO["duration_seconds"],
        "mode": "demo",
        "note": "Demo plan only. No video was rendered.",
    }


def run_detached(command, log_path):
    """Run a long job detached, logging straight to a file.

    This is the pattern production uses: stdout and stderr go
    directly to the log file handle, with no pipe in between.
    Returns the Popen object. Callers must not pipe its output.
    """
    log_file = open(log_path, "a", encoding="utf-8")
    process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True, close_fds=True)
    return process


def main():
    parser = argparse.ArgumentParser(description="Demo render driver, plan only.")
    parser.add_argument("--demo", action="store_true", help="Print the render plan, render nothing.")
    parser.add_argument("--out", default="out/render-plan.json", help="Where to write the render plan JSON.")
    args = parser.parse_args()
    if not args.demo:
        print("Refusing to run without --demo. Real rendering needs the full Remotion studio, not this demo pack.")
        raise SystemExit(2)
    plan = build_render_plan()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print("DEMO ONLY: render plan, no video was rendered.")
    print(json.dumps(plan, indent=2))
    print(f"Plan written to {out_path}. Log straight to a file in production, never through tee. Detached helper: run_detached(command, log_path).")


if __name__ == "__main__":
    main()
