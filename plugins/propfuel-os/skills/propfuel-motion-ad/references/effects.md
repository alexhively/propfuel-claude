# Effects library

Six effect beats on top of the core beats (inbox, popup, stat, quote, cta and the product-UI beats). Each sits
in `engine/scenes-fx.mjs`, loads only its own vendored library (`engine/vendor/LICENSES.md`) and renders the same
pixels every time. Proven on 2026-10-14 by 1-second test renders, two-run snapshot hashes, and a 13s demo
(`examples/fx-demo.json`); outputs in `~/Desktop/PropFuel Motion Ads/_fx-tests/`.

**Use one effect beat per ad, two at most.** Effects support the message; they are never the message. Each one
needs a 1-second test (`scripts/test-1s.sh`) before you build the full ad, and every effect animates in, so
none of them can be frame 0 (the thumbnail) except `stack` with `preDrop`.

| type | Library | What it is for | Don't use it when |
|---|---|---|---|
| `stack` | Matter.js 0.20 | Word cards fall, collide and pile up: lots of topics, signals or reasons landing at once ("what's on members' minds") | The words are a sequence (use captions), or there are more than 8 cards (the pile turns to noise) |
| `sketch` | Rough.js 4.6 | A hand-drawn circle, underline, box or hatch around one number or word: "look here" | The number needs a count-up (use `stat`), or the frame already has a gradient element |
| `brush` | p5.brush 2.2 (standalone, WebGL2) | A textured gradient swipe behind one word of a headline, like a highlighter: the tagline, a key verb | More than one word needs it, or the word wraps onto two lines (keep the marked phrase short) |
| `filter` `glow` | PixiJS 8.21 + pixi-filters 6.1 (WebGL) | A gold halo blooms on one line and settles: a quiet reveal | Body copy or anything below ~60px; it's a moment, not a style |
| `filter` `glitch` | PixiJS 8.21 + pixi-filters 6.1 (WebGL) | A short seeded slice-glitch burst that resolves to clean type: "the old way is broken" | Anything about PropFuel itself, client names or numbers (unreadable for ~1s). Use at most once per ad |
| `orb` | thinking-orbs engine (our MIT port) | A dotted 3D orb for an AI moment: Poppy thinking, "PropFuel is listening", the Campaign Builder working | It would read as an AI person or a face. It's an indicator, not a character |
| `words` | Anime.js 4.5 | Word-by-word kinetic headline with an optional gradient word | Almost always: GSAP already does this (captions, `cta`). It is here as the documented, seekable Anime.js pattern for when you need Anime.js-only tools |

## Spec fields

All beats take `type`, `start`, `end` (seconds on the cut) and `hold: true` to skip the exit fade.

```jsonc
{ "type": "stack", "words": ["Renewal", "Events", "Dues"], "hero": 0, "title": "optional line above",
  "seed": 7, "dropAt": 0.15, "gap": 0.16, "preDrop": 3, "inertia": 6 }
// hero = index of the one gradient card. preDrop = n cards already resting at the beat's first frame (use it when the
// stack opens the ad). inertia = rotational-inertia multiplier (higher = less tumbling; 6 keeps words upright).

{ "type": "sketch", "value": "370+", "label": "associations", "sub": "", "source": "",
  "mark": "circle", "seed": 3, "drawAt": 0.45, "drawDur": 0.7 }
// mark: circle | underline | box | hatch. Same seed = same strokes. The mark is the gradient element.

{ "type": "brush", "text": "Know and Grow Your Membership.", "mark": "Grow", "sub": "",
  "brush": "charcoal", "weight": null, "seed": 11, "swipeAt": 0.35, "swipeDur": 0.55 }
// brush: charcoal (default) | crayon | marker | pastel | spray. weight defaults to the word height / 8.5.

{ "type": "filter", "effect": "glow", "text": "Your members are talking.", "sub": "", "peakAt": 0.45, "seed": 5 }
// effect: glow | glitch. If WebGL is unavailable the same line renders as DOM text (glow gets a CSS gold shadow).

{ "type": "orb", "state": "listening", "label": "PropFuel is listening", "sub": "", "density": 2.2, "dot": 2.6 }
// state: listening (wave) | searching (globe) | working (orbits) | solving (rubik) | composing (ribbon) | shaping (morph).

{ "type": "words", "text": "One question. Every member.", "hero": 3, "stagger": 70 }
```

## How each one stays deterministic in HyperFrames

The rule (hyperframes-core): one paused GSAP timeline on `window.__timelines["main"]`, seekable, no clocks,
no unseeded `Math.random`, no network.

- **Every effect is a pure function of time.** A proxy tween on the main timeline (`ease: "none"`) calls the
  beat's `draw(t)` on every seek. Nothing uses `requestAnimationFrame`, `Date` or `performance.now()`.
- **Async setup waits.** Beats that measure text after fonts load, or start Pixi (async `app.init`), push a
  promise onto `__fx`; the template registers the timeline only after all of them settle. Cuts without fx
  beats register synchronously, exactly as before (txcpa example: pixel-identical to the previous engine).
- **stack**: Matter.js runs once on load at a fixed 60 Hz step from fixed spawn points (sin-hash, not
  `Math.random`) and bakes x, y and angle for every frame; a seek reads the bake.
- **sketch**: Rough.js `seed` fixes the strokes; the draw-on is a GSAP `strokeDashoffset` tween.
- **brush**: p5.brush paints once on load into an OffscreenCanvas after `brush.seed()` and `noiseSeed()`, is
  copied to a 2D canvas and tinted with the gradient; the reveal is a GSAP `clip-path` wipe, so the texture can't
  swim. Never call `brush.scaleBrushes()` in a beat: it multiplies on every call (we size with the weight).
- **filter**: Pixi runs with its ticker stopped and `app.render()` called from `draw(t)`. GlitchFilter's
  `refresh()` uses `Math.random`, so it runs under a seeded PRNG keyed to the frame; outside the burst the
  filter is switched off.
- **orb**: the thinking-orbs engine draws from `t` alone.
- **words**: an Anime.js timeline with `autoplay: false`, registered on `window.__hfAnime` (HyperFrames' animejs
  adapter seeks it in ms). `__fxAnime()` adds the 1-second-test offset.

**Verified 2026-10-14:** snapshot PNG hashes identical across two runs for stack, sketch, brush, glow, glitch,
orb, words and the whole demo. Re-encoded mp4s can differ by a few levels in a few blocks (x264 noise,
seen on plain GSAP beats too), so check determinism on snapshot PNGs, not mp4 bytes.

**WebGL:** `brush` and `filter` need WebGL2/WebGL. HyperFrames uses the host GPU (ANGLE Metal on Alex's Mac) and
falls back to SwiftShader; both were tested (`snapshot --no-browser-gpu`) and render correctly. WebGL frames
switch HyperFrames from fast capture to screenshot capture: still about 4 s per 1-second test here.

## Gallery (inspiration only)

Browse for moves to adapt (text reveals, transitions, timing), then build them in our look. Never copy another
brand's work, layout or copy.

- https://skillry.dev/ai-videos/opus-5-5 (400+ Claude-made videos)
- https://github.com/yihui-dev/awesome-opus5-5-videos
- Library demos: brm.io/matter-js/demo, roughjs.com, pixijs.io/filters/examples, animejs.com,
  rareformlabs.github.io/thinking-orbs

Source: "Claude Motion Tips" (withian.notion.site), read 2026-10-14. It lists these six libraries plus three workflow
upgrades, which are now steps 2, 4b and 7a of SKILL.md: the XML brief, the 1-second test and the pre-render keyframe sheet.
