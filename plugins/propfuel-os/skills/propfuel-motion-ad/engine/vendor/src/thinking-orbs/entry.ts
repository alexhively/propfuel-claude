// PropFuel port of thinking-orbs (MIT, Jakub Antalik, github.com/RareFormLabs/thinking-orbs @ main 2026-07-21):
// the canvas engine only (no Vue component, no rAF loop, no clocks). draw(ctx, state, size, t) is a pure
// function of t, so HyperFrames can seek it. Changes from upstream: paint() inks on a charcoal->cream ramp
// (INK) instead of greyscale, and draw() takes density/dot multipliers for video-size orbs (upstream tunes 20/64 px).
import { MODE_DRAWS } from './src/engine/registry';
import { resolvePreset } from './src/presets';
import { scaleCounts, scaleRadii } from './src/engine/profiles';
import { INK } from './src/engine/core';
export { INK };
export function draw(ctx: CanvasRenderingContext2D, state: any, size: number, t: number, density = 1, dot = 1) {
  const { mode, speed, opts } = resolvePreset(state, 64);
  let o = opts;
  if (density !== 1) o = scaleCounts(o, density);
  if (dot !== 1) o = scaleRadii(o, dot);
  MODE_DRAWS[mode](ctx, size, t * speed, false, o);
}
