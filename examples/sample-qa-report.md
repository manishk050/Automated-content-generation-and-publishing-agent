# Sample QA Report - DEMO ONLY

Title: DEMO ONLY: The Hallway Light
Source file: examples/sample-shot-list.json
Date: demo run, no real video or audio file was measured
Result: PASS (demo data)

This report shows what a passing QA report looks like. The numbers below
are the demo values in the sample shot list, not measurements from a real
render. A real run must measure the real rendered file before it can pass.

## Audio

- Integrated loudness: -14.3 LUFS (target -14.3 LUFS, pass range -14.8 to -13.8 LUFS)
- True peak: -1.2 dBTP (must be under -1 dB, PASS)
- Sample rate before AAC encode: 48000 Hz (must be 48000 Hz, PASS)
- Voice: single consistent voice, no voice change mid-video (PASS)

## Video

- Resolution: 1080x1920 vertical (PASS)
- Frame rate: 30 fps (PASS)
- Duration: 95 seconds, about 2 minutes (PASS)
- Pillarbox: landscape source pillarboxed into vertical frame, no stretch (PASS)

## Sync check - 4 timestamps

Each check asks: does the picture on screen at this second match what
the voice is saying at this second?

- 12 seconds, expected word "light", shot 2: PASS, hallway light is on screen
- 34 seconds, expected word "door", shot 3: PASS, hallway door is on screen
- 58 seconds, expected word "note", shot 4: PASS, kitchen note is on screen
- 81 seconds, expected word "morning", shot 6: PASS, morning hallway is on screen

Result: 4 of 4 sync checks passed.

## Consistency check

- One rig and one set per location: PASS
- Hallway: rig-narrator-hallway-v1, set-hallway-night-v1 in shots 1, 2, 3, 6
- Kitchen: rig-narrator-kitchen-v1, set-kitchen-night-v1 in shots 4, 5
- No prop, face, or set change inside a location: PASS
- All cuts on narration beat boundaries: PASS

## Publish gate

- QA result: PASS
- Publish allowed: yes, only after a real render passes the same checks
- Demo note: this demo run posted nothing to YouTube or Instagram.
