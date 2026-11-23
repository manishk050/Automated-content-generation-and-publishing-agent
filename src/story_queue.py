"""Story queue for the video engine.

Demo only. The queue here holds fake sample entries, not real stories.
The real queue holds adapted stories from real people's accounts, and
its source links stay private. See docs/story-rules.md.
"""

from __future__ import annotations

import argparse
import json


# Fake sample queue. Types drive the variety rule, not real content.
SAMPLE_QUEUE = [
    {"id": "demo-001", "title": "DEMO ONLY: The Hallway Light", "type": "house", "location": "hallway", "status": "queued"},
    {"id": "demo-002", "title": "DEMO ONLY: The Night Bus", "type": "travel", "location": "bus", "status": "queued"},
    {"id": "demo-003", "title": "DEMO ONLY: The Countdown Clock", "type": "countdown", "location": "flat", "status": "queued"},
    {"id": "demo-004", "title": "DEMO ONLY: The Door That Locks Itself", "type": "door", "location": "flat", "status": "queued"},
]

# Types limited to one a week each in production.
WEEKLY_LIMIT_TYPES = {"countdown", "door"}


def pick_next(queue, last_type=None, weekly_used=None):
    """Pick the next story, enforcing the variety rules.

    Never run the same type twice in a row. Weekly limited types
    are skipped if already used that week.
    """
    weekly_used = set(weekly_used or [])
    for entry in queue:
        if entry["status"] != "queued":
            continue
        if entry["type"] == last_type:
            continue
        if entry["type"] in WEEKLY_LIMIT_TYPES and entry["type"] in weekly_used:
            continue
        return entry
    return None


def main():
    parser = argparse.ArgumentParser(description="Demo story queue picker.")
    parser.add_argument("--demo", action="store_true", help="Run with fake sample data only.")
    parser.add_argument("--last-type", default=None, help="Type used in the last run, to avoid repeats.")
    args = parser.parse_args()
    if not args.demo:
        print("Refusing to run without --demo. This pack ships sample data only.")
        raise SystemExit(2)
    picked = pick_next(SAMPLE_QUEUE, last_type=args.last_type)
    print("DEMO ONLY: fake sample queue, no real stories.")
    print(json.dumps({"queue_size": len(SAMPLE_QUEUE), "picked": picked}, indent=2))


if __name__ == "__main__":
    main()
