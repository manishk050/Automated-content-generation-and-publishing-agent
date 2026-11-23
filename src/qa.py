"""QA checks: loudness, sync, and consistency.

Demo mode checks the sample shot list and prints a PASS report.
It never claims to have measured a real audio or video file unless
a real file path is given and that file exists. A failed QA blocks
publish in production.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

TARGET_LUFS = -14.3
LUFS_TOLERANCE = 0.5
MAX_TRUE_PEAK_DB = -1.0
REQUIRED_SAMPLE_RATE_HZ = 48000
SYNC_CHECK_COUNT = 4


def check_audio(audio):
    problems = []
    lufs = audio.get("lufs")
    if lufs is None or abs(lufs - TARGET_LUFS) > LUFS_TOLERANCE:
        problems.append(f"LUFS {lufs}, expected {TARGET_LUFS} plus or minus {LUFS_TOLERANCE}")
    peak = audio.get("true_peak_db")
    if peak is None or peak >= MAX_TRUE_PEAK_DB:
        problems.append(f"True peak {peak} dB, must be under {MAX_TRUE_PEAK_DB} dB")
    rate = audio.get("sample_rate_hz")
    if rate != REQUIRED_SAMPLE_RATE_HZ:
        problems.append(f"Sample rate {rate} Hz, expected {REQUIRED_SAMPLE_RATE_HZ} Hz before AAC encode")
    return problems


def check_sync(data):
    """4-timestamp sync check on the sample shot list.

    At each timestamp, the expected word must appear in that shot's
    word timings, so the picture on screen matches the narration.
    """
    problems = []
    checks = data.get("sync_check_timestamps", [])
    if len(checks) != SYNC_CHECK_COUNT:
        problems.append(f"Expected {SYNC_CHECK_COUNT} sync timestamps, found {len(checks)}")
    shots = {shot["shot"]: shot for shot in data.get("shots", [])}
    for check in checks:
        shot = shots.get(check["shot"])
        if shot is None:
            problems.append(f"Sync check at {check['t_seconds']}s: shot {check['shot']} not found")
            continue
        words = {w["word"].strip(",.") for w in shot.get("words", [])}
        if check["expected_word"] not in words:
            problems.append(f"Sync check at {check['t_seconds']}s: expected word '{check['expected_word']}' not in shot {check['shot']} word timings")
    return problems


def check_consistency(data):
    problems = []
    by_location = {}
    for shot in data.get("shots", []):
        by_location.setdefault(shot["location"], set()).add((shot["rig"], shot["set"]))
    for location, combos in by_location.items():
        if len(combos) != 1:
            problems.append(f"{location}: more than one rig and set combination: {sorted(combos)}")
    for shot in data.get("shots", []):
        if not shot.get("cut_on_beat"):
            problems.append(f"Shot {shot['shot']}: cut is not on a narration beat boundary")
    return problems


def main():
    parser = argparse.ArgumentParser(description="Demo QA checks on the sample shot list.")
    parser.add_argument("--demo", action="store_true", help="Run QA on the sample shot list only.")
    parser.add_argument("--shot-list", default="examples/sample-shot-list.json", help="Shot list JSON to check.")
    parser.add_argument("--audio", default=None, help="Optional real audio file. If given, it must exist, otherwise QA refuses.")
    args = parser.parse_args()
    if not args.demo:
        print("Refusing to run without --demo. This pack ships sample data only.")
        raise SystemExit(2)
    if args.audio is not None:
        audio_path = Path(args.audio)
        if not audio_path.exists():
            print(f"Refusing: audio file not found: {args.audio}. QA never claims a measurement it did not make.")
            raise SystemExit(2)
        print(f"Note: real audio file given ({args.audio}). This demo still checks the sample shot list values, it does not measure the file.")
    data = json.loads(Path(args.shot_list).read_text(encoding="utf-8"))
    problems = []
    problems += check_audio(data.get("audio", {}))
    problems += check_sync(data)
    problems += check_consistency(data)
    passed = not problems
    print("DEMO ONLY: sample data QA, no real audio or video file was measured.")
    print(json.dumps({"title": data.get("title"), "lufs": data.get("audio", {}).get("lufs"), "true_peak_db": data.get("audio", {}).get("true_peak_db"), "sync_checks_passed": f"{SYNC_CHECK_COUNT - len(check_sync(data))} of {SYNC_CHECK_COUNT}", "passed": passed, "problems": problems}, indent=2))
    print("PASS" if passed else "FAIL: publish blocked")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
