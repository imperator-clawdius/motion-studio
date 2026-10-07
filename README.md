# Motion Studio — deterministic motion-graphics video from code

Make motion-graphics videos for **$0**. No AI video API, no per-second billing. No GPU, no license, no cloud.

The trick: instead of paying a video model to hallucinate frames, you write a **pure function of time** — `seek(t)` — that paints the exact frame for any timestamp. A headless browser screenshots N frames. ffmpeg stitches them. Audio is synthesized in Python. The render is deterministic: identical output every run, and a change is a one-line edit + re-render.

> The same reel on a video-gen API (e.g. MiniMax H3) runs roughly **$0.13/second** at 2K. This engine runs it for the cost of electricity.

## The seek(t) pattern

A "program, not a video." `seek(t)` is deterministic — no `Date.now()`, no timers, no `Math.random()` (use a seeded PRNG for anything that looks random).

- **Easing with overshoot** (the "expensive" motion feel):
  `easeOutBack = t => 1 + 2.70158*(t-1)**3 + 1.70158*(t-1)**2`
- **Kinetic type** — stagger each letter (`t0 + i*0.07`) and spring it in.
- **Motion blur** — draw echo ghosts: render the element at N earlier time samples at low alpha.
- **Tornado / vortex montages** — arrange images on an Archimedean spiral, rotate + shrink radius to 0, resolve a logo lockup.

## Files

- `index.html` — a `seek(t)` showreel (5 shots: kinetic type, shape morph, camera push, dot grid, logo lockup).
- `render.mjs` — frame capture harness (puppeteer-core + system Chrome).
- `synth_audio.py` — beat-locked WAV synth (kick/hat/snare/bass/pad + riser → hit), mux with ffmpeg.

## Quick start

```bash
npm install puppeteer-core        # needs no browser download

node render.mjs                   # screenshots 450 frames (15s @ 30fps)

ffmpeg -framerate 30 -i frames/f%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 out.mp4

python3 synth_audio.py            # writes a 15s WAV, then:

ffmpeg -i out.mp4 -i tornado_audio.wav -c:v copy -c:a aac -shortest final.mp4
```

## Notes

- `render.mjs` points at `/usr/bin/google-chrome` (Linux). On Windows/macOS, change `executablePath` to your Chrome/Chromium path.
- `--no-sandbox` is required when running Chrome as root.
- Google Fonts may not load in headless — it silently falls back to system sans.

## License

Apache-2.0
