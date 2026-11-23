"""Publish scheduler.

Demo mode prints the schedule and posts NOTHING to YouTube or
Instagram. Real publish requires --confirm plus credentials from
the environment, and refuses without both.
"""

from __future__ import annotations

import argparse
import json
import os

SCHEDULE = [
    {"platform": "YouTube", "slot": "10:00 AM ET", "kind": "scheduled Short"},
    {"platform": "YouTube", "slot": "8:00 PM ET", "kind": "scheduled Short"},
    {"platform": "Instagram", "slot": "same night the video is built", "kind": "immediate Reel, no scheduled publish in the API"},
]
HASHTAGS = ["#horrorstories", "#scarystories", "#reels"]
REQUIRED_ENV = ["YOUTUBE_API_KEY", "INSTAGRAM_ACCESS_TOKEN"]


def main():
    parser = argparse.ArgumentParser(description="Demo publish scheduler. Demo posts nothing.")
    parser.add_argument("--demo", action="store_true", help="Print the schedule, post nothing.")
    parser.add_argument("--confirm", action="store_true", help="Required for a real publish, plus credentials. Not used in demo.")
    args = parser.parse_args()
    if args.demo:
        print("DEMO ONLY: schedule preview, nothing was posted to YouTube or Instagram.")
        print(json.dumps({"schedule": SCHEDULE, "hashtags": HASHTAGS, "posted": False}, indent=2))
        return
    if not args.confirm:
        print("Refusing to publish without --confirm. Demo mode is --demo, and it posts nothing.")
        raise SystemExit(2)
    missing = [name for name in REQUIRED_ENV if not os.environ.get(name)]
    if missing:
        print(f"Refusing to publish: missing credentials in environment: {', '.join(missing)}. This pack ships no keys or tokens.")
        raise SystemExit(2)
    print("Credentials present and --confirm given. Real publish logic lives outside this demo pack and must pass QA first.")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
