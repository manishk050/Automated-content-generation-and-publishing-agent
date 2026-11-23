// Demo Remotion composition skeleton.
// Production renders this shape with Remotion: 1080x1920, 30 fps,
// about 95 seconds, landscape pillarboxed into vertical.
// This file has no Remotion dependency, so the demo runs without
// installing Remotion. The Node demo script uses this spec to print
// the render plan. Do not claim a video was rendered from this file.

export const VIDEO = {
  width: 1080,
  height: 1920,
  fps: 30,
  durationInSeconds: 95,
};

export const COMPOSITION_ID = "ItHappenedToMeDemo";

export const SHOTS = [
  { shot: 1, location: "hallway", startSeconds: 0, endSeconds: 14 },
  { shot: 2, location: "hallway", startSeconds: 14, endSeconds: 30 },
  { shot: 3, location: "hallway", startSeconds: 30, endSeconds: 48 },
  { shot: 4, location: "kitchen", startSeconds: 48, endSeconds: 66 },
  { shot: 5, location: "kitchen", startSeconds: 66, endSeconds: 80 },
  { shot: 6, location: "hallway", startSeconds: 80, endSeconds: 95 },
];

export const AUDIO = {
  lufs: -14.3,
  truePeakDb: -1.2,
  sampleRateHz: 48000,
};
