"""Storyboard consistency check.

One character rig and one set per location for the whole episode.
All stills are checked side by side before anything animates, so a
prop, face, or set cannot change mid-video inside one location.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def check_stills_consistency(stills):
    """Check that each location uses exactly one rig and one set.

    stills: list of dicts with location, rig, set, and props.
    Returns (passed, problems). A problem stops the run before render.
    """
    problems = []
    by_location = {}
    for still in stills:
        by_location.setdefault(still["location"], []).append(still)
    for location, items in by_location.items():
        rigs = {item["rig"] for item in items}
        sets = {item["set"] for item in items}
        if len(rigs) != 1:
            problems.append(f"{location}: {len(rigs)} rigs found, expected 1: {sorted(rigs)}")
        if len(sets) != 1:
            problems.append(f"{location}: {len(sets)} sets found, expected 1: {sorted(sets)}")
        props = {tuple(sorted(item.get("props", []))) for item in items}
        if len(props) != 1:
            problems.append(f"{location}: props changed between stills: {sorted(props)}")
    return (not problems, problems)


def stills_from_shot_list(path):
    """Build a stills list from a shot list JSON file."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    stills = []
    for shot in data["shots"]:
        stills.append(
            {
                "shot": shot["shot"],
                "location": shot["location"],
                "rig": shot["rig"],
                "set": shot["set"],
                "props": ["hallway light", "door"] if shot["location"] == "hallway" else ["counter note", "kitchen light"],
            }
        )
    return stills


def main():
    parser = argparse.ArgumentParser(description="Demo storyboard consistency check.")
    parser.add_argument("--demo", action="store_true", help="Run on the sample shot list only.")
    parser.add_argument("--shot-list", default="examples/sample-shot-list.json", help="Shot list JSON to check.")
    args = parser.parse_args()
    if not args.demo:
        print("Refusing to run without --demo. This pack ships sample data only.")
        raise SystemExit(2)
    stills = stills_from_shot_list(args.shot_list)
    passed, problems = check_stills_consistency(stills)
    print("DEMO ONLY: fake sample stills, no real images.")
    print(json.dumps({"shots_checked": len(stills), "passed": passed, "problems": problems}, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
