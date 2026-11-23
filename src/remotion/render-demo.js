// Demo render script. Prints the render plan and writes
// out/render-plan.json. It does NOT render a video.
// Run: npm run render -- --demo
// Real production rendering uses Remotion with the composition
// in Composition.js. This demo keeps npm install instant and
// offline safe, with no Remotion dependency.

const fs = require("fs");
const path = require("path");

function main() {
  const args = process.argv.slice(2);
  if (!args.includes("--demo")) {
    console.log("Refusing to run without --demo. Real rendering needs the full Remotion studio, not this demo pack.");
    process.exit(2);
  }
  const plan = {
    title: "DEMO ONLY: The Hallway Light",
    composition: "ItHappenedToMeDemo",
    video: { width: 1080, height: 1920, fps: 30, durationSeconds: 95, frames: 2850 },
    audio: { lufs: -14.3, truePeakDb: -1.2, sampleRateHz: 48000 },
    shots: 6,
    mode: "demo",
    note: "Demo plan only. No video was rendered.",
  };
  const outPath = path.join(__dirname, "..", "..", "out", "render-plan.json");
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(plan, null, 2));
  console.log("DEMO ONLY: render plan, no video was rendered.");
  console.log(JSON.stringify(plan, null, 2));
  console.log(`Plan written to ${outPath}.`);
}

main();
