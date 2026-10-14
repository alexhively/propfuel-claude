# Vendored libraries

Every library the engine loads at render time lives in this folder. Nothing is fetched from a CDN. `build.mjs`
copies a file into a project's `assets/` only when a beat in that cut uses it (`VENDOR` in `../scenes-fx.mjs`).

Fetched 2026-10-14 with `npm install --ignore-scripts --save-exact` into an empty temp folder (no install
scripts run). Only the minified browser builds are kept, with their `sourceMappingURL` comments stripped. The
full license texts are in `licenses/`.

| File | Library | Version | License | Source | sha256 |
|---|---|---|---|---|---|
| `gsap.min.js` | GSAP | 3.14.2 | GSAP Standard "No Charge" License (free for commercial use; not OSI) | https://gsap.com/standard-license | c174bfce53a72941 |
| `matter.min.js` | Matter.js | 0.20.0 | MIT | https://github.com/liabru/matter-js | 72d30be0f579eb02 |
| `rough.min.js` | Rough.js (`bundled/rough.js`) | 4.6.6 | MIT | https://github.com/rough-stuff/rough | 6853af8619532f39 |
| `pixi.min.js` | PixiJS | 8.21.0 | MIT | https://github.com/pixijs/pixijs | 47c542b4038968be |
| `pixi-filters.min.js` | pixi-filters | 6.1.5 | MIT | https://github.com/pixijs/filters | 6f8aafba08b7edce |
| `anime.umd.min.js` | Anime.js | 4.5.0 | MIT | https://github.com/juliangarnier/anime | 8d5b3a58a1f64023 |
| `p5.brush.standalone.min.js` | p5.brush, standalone build (`dist/brush.js`) | 2.2.3 | MIT | https://github.com/acamposuribe/p5.brush | 5f6f40904a974650 |
| `thinking-orbs.min.js` | thinking-orbs, canvas engine only (our port) | main @ 2026-07-21 (npm 0.1.1) | MIT | https://github.com/RareFormLabs/thinking-orbs | 1fe801535ace4487 |

The sha256 column is the first 16 hex digits; run `shasum -a 256 *.js` here for the full hashes.

## Notes and decisions

- **pixi.js 8.21.0, not 8.22.0.** 8.22.0 was published 2026-10-01, under two weeks before vendoring; we take
  releases at least two weeks old.
- **p5.brush uses the standalone build, so p5.js is not vendored.** p5.js itself is LGPL-2.1, which is outside
  our permissive-only rule (MIT, ISC, BSD, Apache). p5.brush 2.x ships a standalone WebGL2 build that needs no
  p5, so we use that. It seeds its PRNG with `Math.random()` once at load; every beat calls `brush.seed()` and
  `brush.noiseSeed()` before drawing, so the output is fixed. (The task brief suggested p5 instance mode; the
  standalone build makes p5 unnecessary.)
- **thinking-orbs is a port, not the package.** The GitHub repo ships a Vue component (Vue peer dependency,
  `requestAnimationFrame` loop, `performance.now()` clock), and the npm name `thinking-orbs` now points at a
  later React rewrite by the same author. We read the whole engine (`src/engine/*.ts`, `src/presets.ts`,
  about 25 KB): plain 2D canvas, `Math.sin`-hash pseudo-randomness, no network, no DOM access, no
  `Math.random`. We kept only that engine, bundled with esbuild into an IIFE (`window.ThinkingOrbs`), and
  changed two things: dots are inked on a charcoal-to-cream ramp instead of greyscale, and `draw()` takes
  density and dot-size multipliers for video-size orbs. Source and the build entry are in
  `src/thinking-orbs/` (MIT notice kept). Rebuild with:
  `esbuild entry.ts --bundle --format=iife --global-name=ThinkingOrbs --minify --target=es2019`.
- **pixi-filters GlitchFilter** calls `Math.random()` in `refresh()`. The `filter` beat swaps in a seeded PRNG
  for the length of each call, keyed to the frame number, so every frame is fixed.
