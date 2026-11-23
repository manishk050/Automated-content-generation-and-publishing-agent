"""Script builder with word timings.

Builds a script from beats, then assigns every word a start and end
time so the shot list can be built from the narration. Demo only,
fake sample outline, no real story text.
"""

from __future__ import annotations

import argparse
import json

# About 2.5 words per second, 0.4 seconds per word. Simple, explicit,
# and easy to check by hand against the shot list.
SECONDS_PER_WORD = 0.4

SAMPLE_OUTLINE = [
    {"beat": "normal life", "text": "I moved into the flat in March, and the hallway light was the first thing I fixed. The flat was small, one bedroom, one kitchen, and a hallway that was always cold. I worked late most nights, so I came home after dark, and the light was the first thing I saw."},
    {"beat": "small detail", "text": "On the third night the light went out at 3:03, and it came back on by itself. I checked the switch, I checked the bulb, and I checked the fuse box in the cupboard by the door. Nothing was loose, nothing was warm, and nothing smelled of burning. I told myself it was an old building, and old buildings do strange things at night."},
    {"beat": "rule with a cost", "text": "The next morning I found a note on the kitchen counter, in my own handwriting, and I had not written it. The note said to leave the light on, so I did, and the flat stayed quiet for a week. I left the door open that night so I could hear it, and I heard the handle turn. I did not get up, I did not call out, and I did not open the door. I waited until morning, and the light was still on."},
    {"beat": "proof", "text": "This morning the light was off again, and the note was gone."},
]


def build_script(outline, start_seconds=0.0):
    """Return a timed script: a list of words with start and end times."""
    words = []
    cursor = start_seconds
    for line in outline:
        for word in line["text"].split():
            words.append(
                {
                    "word": word,
                    "start": round(cursor, 2),
                    "end": round(cursor + SECONDS_PER_WORD, 2),
                    "beat": line["beat"],
                }
            )
            cursor += SECONDS_PER_WORD
    return words


def main():
    parser = argparse.ArgumentParser(description="Demo script builder with word timings.")
    parser.add_argument("--demo", action="store_true", help="Run with the fake sample outline only.")
    args = parser.parse_args()
    if not args.demo:
        print("Refusing to run without --demo. This pack ships sample data only.")
        raise SystemExit(2)
    words = build_script(SAMPLE_OUTLINE)
    duration = words[-1]["end"] if words else 0.0
    print("DEMO ONLY: fake sample script, no real story text.")
    print(json.dumps({"word_count": len(words), "duration_seconds": duration, "words_per_second": 1 / SECONDS_PER_WORD, "first_words": words[:5]}, indent=2))


if __name__ == "__main__":
    main()
