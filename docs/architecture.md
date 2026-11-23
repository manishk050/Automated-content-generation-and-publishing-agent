# Architecture

Pipeline: Story queue -> Script -> Voice -> Storyboard -> Render -> QA -> Publish

Two videos a day, 10:00 AM and 8:00 PM ET on YouTube, with same-day
Instagram Reels. Each video is about 2 minutes, 1080x1920 vertical.
Real production numbers referenced in the README: 16 Shorts published,
2 videos a day, 1080x1920, -14.3 LUFS, peak under -1 dB, 4-timestamp
sync check. No other metrics are claimed here.

## 1. Story queue - src/story_queue.py

- Stories are queued with a type, a location, and a variety tag.
- Variety rule: never run the same story type twice in a row.
  Countdown stories and door stories are limited to one a week each.
- A story is picked only if its type was not used in the last run.
- The real queue holds adapted stories from real people's accounts.
  This demo repo holds one fake sample story only.

## 2. Script - src/script.py

- The script is built from beats: normal life, small detail, rule
  with a cost, concrete proof at the end.
- Every word gets a start and end time. At about 2.5 words per
  second, a 95 second video holds about 230 words.
- The shot list is built from those word timings, not after the
  render. Every cut lands on a narration beat boundary.

## 3. Voice

- One consistent voice across the channel.
- Audio is mastered to -14.3 LUFS with true peak under -1 dB.
- Audio is downsampled to 48 kHz before AAC encode, never fed
  at 192 kHz to the encoder.

## 4. Storyboard - src/storyboard.py

- One character rig and one set per location for the whole episode.
- All stills are checked side by side before anything animates.
- `check_stills_consistency()` fails the episode if a rig, set,
  face, or prop changes inside one location.
- A failed consistency check stops the run before rendering.

## 5. Render - src/render.py and src/remotion/

- Production render uses Remotion, landscape pillarboxed into
  vertical 1080x1920.
- The render driver is detached and logs straight to a file.
  It never logs through `tee` or a process substitution pipe,
  because a broken pipe can kill a long render.
- This demo repo uses a Node demo script (`npm run render -- --demo`)
  that prints the render plan and writes `out/render-plan.json`.
  It does not render a video. The real Remotion composition
  skeleton lives in `src/remotion/Composition.js` and is wired
  in the same shape as production, so the plan matches the
  real composition: 1080x1920, 30 fps, about 95 seconds.

## 6. QA - src/qa.py

- Runs on every video, before publish. A failed QA blocks publish.
- Audio: loudness -14.3 LUFS, true peak under -1 dB, 48 kHz.
- Video: 1080x1920, 30 fps, no stretch, pillarbox only.
- Sync: 4-timestamp spot check. At each timestamp, the picture
  on screen must be what the voice is saying at that second.
- Consistency: one rig and one set per location, all cuts on beats.
- Demo mode checks the sample shot list and labels the result
  as demo data. It never claims to have measured a real file
  unless a real file path is given and exists.

## 7. Publish - src/publish.py

- YouTube: scheduled for 10:00 AM and 8:00 PM ET.
- Instagram: posts live the night the video is built, since
  the Instagram API has no scheduled publish.
- Hashtags are plain clickable tags, never URL-encoded.
- Demo mode prints the schedule and posts nothing.
- Real publish requires `--confirm` plus credentials from
  the environment, and refuses without both. This demo pack
  ships no credentials.

## Nightly run, in order

1. Pick the next story from the queue.
2. Build the script with word timings.
3. Build the storyboard and pass the stills check.
4. Render detached, log straight to a file.
5. Run QA. If QA fails, stop, do not publish.
6. Publish the morning slot, then the evening slot.
7. Log the result and queue the next story.

## Files

- `src/story_queue.py`, `src/script.py`, `src/storyboard.py`
- `src/render.py`, `src/qa.py`, `src/publish.py`
- `src/remotion/Composition.js`, `src/remotion/render-demo.js`
- `examples/sample-shot-list.json`, `examples/sample-qa-report.md`
- `docs/story-rules.md`
