---
name: vertical-safe-zones
description: Safe zones for 9:16 vertical content (1080x1920) on Instagram Reels, Stories and Feed, TikTok For You, and Facebook Feed and Reels, plus the combined safe box that is clear on all of them. Rule - make key elements as big as possible while staying fully inside the safe box. Includes CSS variables, a debug overlay for HyperFrames/HTML compositions and a frame QA step. Use whenever you make or review reels, stories, shorts, TikToks, 9:16 or vertical video, vertical statics, story ads or any 1080x1920 creative.
---

# Vertical safe zones (9:16, 1080x1920)

Platform UI (username, caption, buttons, the right-side action rail, progress bars) sits on top of vertical
video. Anything under it is hidden or unreadable. This skill holds the exact clear areas and the rule for using them.

**Source:** the Runneth post-preview app (Alysha's tool, zones dated Oct 18 2026). The numbers below are copied from
the app's own overlay SVG (`reference/safe-zones-overlay.svg`, verbatim); nothing here is estimated.

## The rule

**Make key elements as big as possible while staying fully inside the safe box.**

- Headlines, hero numbers, faces and product UI fill the safe box **width** (780px for the combined box). Size type
  up until the longest line touches both sides of the box, then stop. Small and centred in a big empty frame is the
  failure mode, not the safe choice.
- Burned-in captions go in the **lower-middle of the safe box** (roughly y 1100-1340), above the bottom UI. Never below y 1340.
- Nothing important goes under the **right-side action rail** (the right 194px from y 871 down on IG Reels, see the table).
- Only background (colour, texture, b-roll, gradients) runs to the frame edge.
- When a piece runs on one placement only, you may use that placement's own zone. When in doubt, use the combined box.

## Combined safe box (clear on every placement)

The app's lime "Clear everywhere" box. Use this for anything that runs on more than one placement.

| | px at 1080x1920 | % of frame |
|---|---|---|
| Box | x 100 → 880, y 290 → 1340 (780 × 1050) | 72.2% wide × 54.7% tall |
| Top inset | 290 | 15.1% |
| Bottom inset | 580 | 30.2% |
| Left inset | 100 | 9.3% |
| Right inset | 200 | 18.5% |

Derived from the polygons below (not drawn in the app): the strict intersection is x 97-886, y 285-1347; the app's
box sits a few px inside it as a margin. Above y 871 the only right-hand limit is IG Reels' x 983, so a wide
element in the **top band (y 290-871) can extend right to x 983** if it has to.

## Per placement (from the app)

Insets are px from each edge of the 1080x1920 frame (% in brackets). "Rail" = the right-side action buttons: below
the given y the right inset grows to the rail value.

| Placement | Top | Bottom | Left | Right | Right-side rail |
|---|---|---|---|---|---|
| Instagram Reels | 206 (10.7%) | 573 (29.8%) | 97 (9.0%) | 97 (9.0%) | from y 871 (45.4%): right 194 (18.0%) |
| Instagram Stories | 224 (11.7%) | 377 (19.6%) | 0 | 0 | none |
| Instagram Feed | 91 (4.7%) | 91 (4.7%) | 0 | 0 | none (feed crops 9:16 to about y 84-1836) |
| TikTok For You | 228 (11.9%) | 323 (16.8%) | 54 (5.0%) | 54 (5.0%) | from y 1020 (53.1%): right 173 (16.0%) |
| Facebook Feed | 285 (14.8%) | 285 (14.8%) | 0 | 0 | none |
| Facebook Reels | 217 (11.3%) | 422 (22.0%) | 57 (5.3%) | 57 (5.3%) | from y 1196 (62.3%): right 150 (13.9%) |

What sits in the bottom zones (from the app's mock UI): avatar, username + Follow, "Original audio" line and a
one-line caption on Reels-style placements (caption starts y 1598 at x 131); on ads, the CTA button / bar.

**Not in the app:** YouTube Shorts, LinkedIn vertical and Facebook Stories. No numbers are given for them here. Use
the combined box and check a real-device screenshot before shipping to those.

Reference images (rendered from the app's SVG): `reference/all.png` (every line + lime box), `reference/safe.png`,
and one per placement: `ig-reels.png`, `ig-story.png`, `ig-feed.png`, `tt.png`, `fb-feed.png`, `fb-reels.png`.

## CSS + debug overlay for HyperFrames / HTML compositions

Put the variables on the 1080x1920 stage and lay key content out inside `.safe`:

```css
:root {
  --safe-top: 290px; --safe-right: 200px; --safe-bottom: 580px; --safe-left: 100px;
  --safe-w: 780px; --safe-h: 1050px;            /* combined box, Runneth post-preview, Oct 18 2026 */
  --safe-top-band-right: 97px;                  /* y 290-871 only: may widen to x 983 */
}
.safe { position: absolute; top: var(--safe-top); left: var(--safe-left); width: var(--safe-w); height: var(--safe-h); }
.safe .caption { position: absolute; left: 0; right: 0; bottom: 0; }   /* lower-middle, above the bottom UI */
```

Debug overlay: add the app's lines on top of the stage when the URL has `?safe=1` (or press `S` in preview).
Off by default, so the render is unchanged; no network, so HyperFrames determinism holds. Paste the contents of
`reference/safe-zones-overlay.svg` into `SAFE_SVG`.

```html
<script>
  const SAFE_SVG = `<!-- paste reference/safe-zones-overlay.svg here -->`;
  function safeOverlay(on) {
    let el = document.getElementById("safe-debug");
    if (!el) {
      el = document.createElement("div");
      el.id = "safe-debug";
      el.style.cssText = "position:absolute;inset:0;pointer-events:none;z-index:99999";
      el.innerHTML = SAFE_SVG.replace("<svg ", '<svg style="width:100%;height:100%" preserveAspectRatio="none" ');
      document.querySelector("#stage, [data-composition], body").appendChild(el);
    }
    el.hidden = !on;
  }
  safeOverlay(new URLSearchParams(location.search).has("safe"));
  addEventListener("keydown", (e) => { if (e.key === "s" || e.key === "S") safeOverlay(document.getElementById("safe-debug").hidden); });
</script>
```

Fill-the-width helper (deterministic: measures once, no timers). Call after fonts load:

```js
// grow font-size until the element's widest line meets maxW (default: the safe box width)
function fitWidth(el, maxW = 780, max = 400) {
  let lo = 8, hi = max;
  while (hi - lo > 0.5) { const mid = (lo + hi) / 2; el.style.fontSize = mid + "px"; (el.scrollWidth <= maxW ? (lo = mid) : (hi = mid)); }
  el.style.fontSize = lo + "px";
}
```

For `propfuel-motion-ad`, the same numbers in its `engine/formats.json` shape:
`"safe": { "top": 290, "bottom": 580, "left": 100, "right": 200 }`.

## QA (before anything is shown or shipped)

1. Render key frames (every beat, plus the first and last frame) with `?safe=1` so the lines are burned in.
   For HyperFrames, `propfuel-motion-ad/scripts/qa.sh` already makes a `_safezone.jpg` contact sheet; check it uses these numbers.
2. Open each frame and check: no word, number, logo, face or product UI crosses the lime box (or the target placement's
   line). Pay attention to the bottom-right corner, where the rail and the caption block meet.
3. Check the size works: also check every frame at **390px wide** (phone width, scale 0.361). Body text should be at least
   48px on the 1080 canvas (about 17px on the phone); headlines and hero numbers should nearly fill the safe box width. If
   something fits but reads small at 390px, make it bigger, not the box.
4. Static (1080x1920 PNG/JPG): same check, overlay on, at full size and at 390px.
5. Turn the overlay off for the final export and confirm no debug lines are left in the delivered file.
