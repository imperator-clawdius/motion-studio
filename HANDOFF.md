# HANDOFF — motion-studio

**One-liner:** Deterministic motion-graphics video rendered from a `seek(t)` code function — broadcast-style reels for the cost of electricity, no video-gen API.
**Status:** prototype — ~35% to shippable
**Monetization:** Indirect. Not a SaaS as-is; earns as (a) a done-for-you reel/animation service (undercut $0.13/sec video-gen APIs) or (b) a productized template pack / render engine. No billing in-repo.

## What it is
A self-contained technique demo: you write a pure function of time `seek(t)` that paints the exact frame for any timestamp, a headless browser screenshots N frames, ffmpeg stitches them, and Python synthesizes beat-locked audio. Output is byte-identical every run and a change is a one-line edit plus re-render. The "product" is the pattern and the harness, not a packaged app.

## Who pays & why
Indie creators, agencies, and marketers who need polished 15–30s motion graphics (logo lockups, kinetic type, product reels) and balk at per-second AI-video pricing or Adobe/After Effects licensing. Pain: recurring per-render cost and non-determinism. Willingness to pay: per-reel service fee, or a one-time template-pack / tool purchase.

## Stack
Node.js (ESM), `puppeteer-core` + system Chrome (headless screenshotting), HTML5 Canvas 2D (no libs), Python 3 + NumPy (WAV synth), ffmpeg (stitch + mux). No `package.json`/lockfile. Apache-2.0.

## Architecture
`seek(t)` canvas program → headless Chrome screenshots 450 frames → ffmpeg → mp4; NumPy synth → WAV → ffmpeg mux → final.mp4.
- `index.html` — the showreel: `window.seek(t)` dispatches to 5 hardcoded shots (kinetic type, morph, camera push, dot grid, logo lockup), seeded PRNG, custom easings.
- `render.mjs` — frame-capture harness (FPS/DUR/W/H constants; `executablePath` hardcoded to `/usr/bin/google-chrome`).
- `synth_audio.py` — 15s beat-locked drum/bass/pad/riser synth, writes `tornado_audio.wav`.

## What works today
- Full deterministic render pipeline end-to-end (frames → mp4 → audio → muxed final).
- Five polished canvas shots with overshoot easing, kinetic type, motion-blur ghosting, vortex montage.
- Beat-synced procedural audio locked to the reel's 15s timeline.

## Gaps to ship (ranked)
1. Not reusable/parameterized — one hardcoded reel; no way to feed text/logo/colors/timing without editing source. Needs a scene config/template layer.
2. No `package.json`, lockfile, CLI, or one-command build — manual `npm install` + 3 separate ffmpeg/python invocations; not cross-platform (Linux Chrome path hardcoded).
3. Audio is hand-timed to this exact reel; no sync to arbitrary scene durations. No asset ingestion (logos/images) pipeline.

## Run it
```bash
# Edit render.mjs: set executablePath to your Chrome (Win/macOS) before running
npm install puppeteer-core
node render.mjs
ffmpeg -framerate 30 -i frames/f%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 out.mp4
python3 synth_audio.py
ffmpeg -i out.mp4 -i tornado_audio.wav -c:v copy -c:a aac -shortest final.mp4
```

## Risks / unknowns
- Google Fonts fail silently in headless/offline → falls back to system sans (visual drift).
- Canvas 2D ceiling: 3D/complex particle work would need WebGL/Three.js rewrite.
- Value prop assumes the buyer wants a code workflow; non-technical buyers need a UI that does not exist.
- No tests, no CI, no error handling in the harness.

## Fastest path to revenue
1. Wrap `seek(t)` scenes behind a JSON/CLI config (text, logo, colors, duration) so one reel becomes a template.
2. Package 5–10 templates + a one-command `make-reel` script; add cross-platform Chrome detection.
3. Sell as a done-for-you reel service (fixed price/reel) or a template pack; use rendered samples as the funnel.
