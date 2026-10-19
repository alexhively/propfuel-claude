---
name: propfuel-motion-ad
description: Make a PropFuel video ad where every frame is drawn by code (HTML/CSS/GSAP rendered by HyperFrames), with no video model, no stock footage and no AI imagery or AI people. Real PropFuel logo, real product UI recreated in code, type and shapes only. Storyboard first, then 9:16 / 4:5 / 1:1 / 16:9 and a 6s bumper, safe zones, burned-in captions, H.264 export, frame QA contact sheets. Use when someone asks for a video ad, motion ad, reel, animated stat, case-study video, bumper, "coded video" or "an animation drawn in code", or wants to replace an AI-generated video. Replaces the cinematic AI-footage case-study videos (Alex, 2026-10-12).
---

# PropFuel motion ad (drawn entirely in code)

A motion ad is a small program: `brief.xml` + storyboard → `spec.json` (beats, copy, proof) → `engine/build.mjs`
→ one HyperFrames project per cut × format → `scripts/test-1s.sh` (the hardest second) → `scripts/keyframes.sh`
(pre-render sheet, wait for feedback) → `scripts/render.sh` (mp4) → `scripts/qa.sh` (contact sheets). Change a
word, rebuild, re-render in about 15 seconds. Pattern 3 of the Opus 5.5 build guide ("An animation drawn
entirely in code").

## Hard rules

1. **No AI-generated footage, no AI people, no AI imagery, no stock.** (PLAYBOOK §8, Alex 2026-10-12.) The
   rejected Seedance videos had a woman typing on a laptop that wasn't there. If a beat seems to need a
   person, it needs a different beat: show the product UI, the number or the words instead.
2. **Real logos only.** `engine/assets/propfuel-logo.png` is the current mark (yellow speech bubble, charcoal).
   A client's logo only if we hold the official file. Otherwise set the client's name in DM Sans.
3. **Every claim is sourced.** Numbers come from ROI - Master, Case Studies - Master or the live case-study
   page (OS knowledge, `get_knowledge`). List each on-screen claim and its source in `spec.proof.claims`.
4. **A client is named only if its case study is live** (OS `get_case_studies`: stage Live, shown_as Named,
   and the URL returns 200 today). Anonymous studies stay anonymous ("a state CPA society").
5. **Count and tagline:** "370+ associations" and "Know and Grow Your Membership." Nothing else.
6. **Nothing ships to an ad account, or anywhere public, until Alex approves the exact file** (path +
   render date). This skill never uploads. It saves locally and asks.

## When to use it

- A paid social or YouTube video ad, an organic reel, a website loop, or a sales-email GIF built from a
  stat, a case study, a product moment or a message.
- Replacing any AI-generated video.
- **Not** for real recorded footage (Gong clips, Dave on camera): that's `testimonial-video` in
  propfuel-meta-ads. Captions and lower-thirds on real footage can still borrow this look.
- **Speaker tiles on real call footage** (Alex, Oct 14 2026): show only the person who is speaking, in one
  Zoom-style tile with their name label and a sound-wave ring (crisp gold edge plus a soft gold glow) driven by
  their real audio. The listener isn't shown: no second tile, no avatar, no still. No footage of the speaker at that
  moment (camera off, sharing screen) means a camera-off tile (their initial and name, no photo) with the same ring.
  Never a frozen frame or footage borrowed from another moment. Crossfade at speaker changes and hold each tile at
  least ~0.6s. Keep the LIVE CLIENT CALL chip and the client attribution. Full rule in `testimonial-video`.

## Workflow

### 1. Lock the proof (5 min)

- `get_case_studies` → pick a **Live + Named** study. `curl -sL -A "Mozilla/5.0" -o /dev/null -w '%{http_code}'`
  the case-study URL and the CTA URL (`https://www.propfuel.com/book-a-demo`). Both must be 200.
- Copy the numbers **from the live page**, not from a draft. If the page and the OS disagree, stop and flag it.
- Real product UI: the campaign question and answers are in the content repurposer at `exemplars/campaign-visual/specs/<org>.json`.
  Recreate them in code; never invent a question the client didn't send.

### 2. Brief + storyboard first (show them before building)

Fill in `templates/brief.xml` and save it as `<adDir>/brief.xml`. Its tags keep the instructions apart:
`<art_direction>` (look, the one gradient element, which effect beats and why), `<references>` (real product
screens, inspiration links), `<timing>` (every beat to the hundredth of a second, plus the hardest second),
`<deliverable>` (cuts, formats, codec, paths) and `<proof>` (every claim and its source). Then write the beats as
a table and show both to the requester before writing any spec:

| # | Time | Caption (burned in, ≤7 words) | Visual (drawn in code) | Motion | Proof |
|---|---|---|---|---|---|

Rules for a 15s ad (Shiver, `propfuel-meta-ads/knowledge/matt-shiver-method.md`):
- **0–2s hook.** Avatar call-out first ("Membership directors"), one line that reframes their assumption.
  Frame 0 is the thumbnail: it must already read with nothing animated in (the engine skips entrances at t=0).
- **2–5s the turn.** The product moment (the question inside the email, the answer being tapped).
- **5–9s the stat reveal.** One hero number, gradient text fill, counting up. Support line 3–5× smaller.
- **CTA by 10s** ("See it with your members" → Book a demo, propfuel.com/book-a-demo), then hold it to the end.
- One idea per beat. One gradient element per frame. Hero 3–5× the support text.

**6s bumper (YouTube):** hook caption over the stat 0–3.4s, CTA 3.4–6s. No product UI: there isn't time.

If running autonomously (no one to show), write the brief and storyboard into the ad folder and proceed.

### 3. Write the spec

Copy `examples/txcpa-autorenewal.json`. Fields: `slug`, `proof` (client, status, URL, claims → sources),
`cta`, and `cuts` (`15s`, `6s`, …), each with `duration`, `captions[]` and `scenes[]`.

Scene types the engine draws today:

| type | What it draws | Key fields |
|---|---|---|
| `inbox` | An email card; optional hand-off to a PropFuel question with answer buttons and a tap | `email{from,subject,body,rows,receipt}`, `question{at,text,answers,pick,pickAt}` |
| `stat` | Hero number counting up (gradient), label, 100-dot grid, support line, source line | `value,decimals,suffix,label,sub,dots,source` |
| `quote` | Verbatim client quote + name and title (only Gong-verified quotes: grep the transcript for the exact string) | `text,name,role` |
| `cta` | Full-safe-zone end card: logo, headline, gradient button, URL, tagline, button pulses | uses `spec.cta` (+ optional `sub`) |
| `popup` | A website (skeleton page, real domain in the URL bar) with the PropFuel Website Engagement pop-up | `site`, `question{at,text,answers or skeleton,pick,pickAt}` |
| product beats | `builder`, `checklist`, `drafts`, `guard`, `signals`, `segment`, `profile`, `home`, `initiative`, `headline`, `site`: real PropFuel screens recreated in code | see the header of `engine/scenes-product.mjs` |
| **effect beats** | `stack`, `sketch`, `brush`, `filter` (glow / glitch), `orb`, `words`: see **Effects library** below | `references/effects.md` |

`stat` also takes `prefix`, `comma: true`, `size: md|sm`, and `dots: null` to hide the grid; a stat at
`start: 0` shows its final value on frame 0.

New beat type? Add a renderer function to `engine/build.mjs` and its CSS to `engine/template.html`,
following the existing ones (static end-state HTML, then `tl.fromTo` from-states; `immediateRender: false`
on any tween that starts later than its element is first visible).

### 4. Build, then test the hardest second

```bash
SK="<this skill's folder>"   # e.g. ~/Projects/propfuel-content-repurposer/.claude/skills/propfuel-motion-ad
AD="$HOME/Desktop/PropFuel/03 Video/PropFuel Motion Ads/<slug>"
node $SK/engine/build.mjs <spec.json> "$AD" --cuts 15s --formats 9x16,4x5      # add 1x1,16x9 / --cuts 6s as needed
cp <spec.json> "$AD/spec.json"
```

**4b. 1-second test (required when a beat uses an effect or anything new).** Before building every format,
render only the hardest second, at 1080×1080, 30 fps:

```bash
$SK/scripts/test-1s.sh <spec.json> 15s:1@0.3      # cut 15s, scene index 1, starting 0.3 s into the beat
```

It writes `test_<cut>_s<i>.mp4` plus a timestamped keyframe sheet and an all-30-frames sheet to
`~/Desktop/PropFuel/03 Video/PropFuel Motion Ads/_fx-tests/<slug>/`. Look at them, show the requester, and wait for a yes on the
texture and motion before expanding the effect into the full ad.

Before writing composition HTML by hand, read the `hyperframes-core` skill (the engine already obeys it:
one paused timeline on `window.__timelines["main"]`, local `@font-face`, vendored GSAP, no clocks/random/network).

### 5. Formats and safe zones

`engine/formats.json` holds canvas + safe box per format. Every word, number and logo sits inside the box;
only the cream ground and grain may run to the edge.

| Format | Canvas | Safe box (px from edge: top / bottom / sides) | Why |
|---|---|---|---|
| 9:16 | 1080×1920 | 270 / 672 / 72 | Meta Reels: top 14%, bottom 35% (caption, CTA, profile), sides 6%. Covers Stories (bottom 20%), IG Reels, YouTube Shorts (bottom ~25%, right-rail buttons sit inside the bottom zone) and LinkedIn vertical |
| 4:5 | 1080×1350 | 60 / 60 / 60 | Meta + IG feed, LinkedIn mobile feed: no overlays, just keep a margin |
| 1:1 | 1080×1080 | 60 / 60 / 60 | Feed fallback, LinkedIn, Meta right column |
| 16:9 | 1920×1080 | 72 / 150 / 110 | YouTube in-stream + bumpers: progress bar, "Skip" and the advertiser card sit bottom; LinkedIn desktop |

The 9:16 bottom 35% stays empty on purpose. Do not "fill" it with copy.

### 6. Captions are burned in

Most feed video plays muted, so the captions carry the story and are part of the picture (not an .srt).
DM Sans 750, charcoal, ≤7 words, one per beat, top of the safe box (left column on 16:9). If the ad has a
voiceover, the captions are the VO words, timed to it; if not, they are the narrative line. Never more than
two text sizes competing in one zone.

### 7. Keyframe sheet, wait, then render (HyperFrames → H.264)

**7a. Pre-render keyframe sheet (required).** Fast: snapshots only, no video encoded.

```bash
$SK/scripts/keyframes.sh "$AD"
```

For every project it captures the start, just before and after every beat and caption change, the middle of
each beat and the final hold, all labelled with their timestamps, into `qa/keyframes/<cut>-<fmt>_keyframes_<n>.jpg`.
Check for cropped text, accidental overlaps and elements that vanish mid-transition. Then **stop: show the
sheets and wait for the requester's feedback before the final render.** (Autonomous runs: note the check in the
README and continue.)

**7b. Render.** Check usage first: `npx hyperframes usage --json`. Then:

```bash
$SK/scripts/render.sh "$AD" 600
```

- **Budget gate:** the script totals frames (duration × 30 × projects) and stops over **3,000 frames**
  (≈ 7 × 15s formats) unless `MOTION_AD_BUDGET_OK=1` after the requester agrees. Each render is killed at the
  **cap** (default 600 s). A 15s ad renders in ~15 s on this Mac; a render near the cap means a bug, not a
  slow machine.
- Each project runs `hyperframes check` first (lint + runtime + layout + contrast) and won't render on a failure.
- Export: HyperFrames `--quality delivery --fps 30`, then ffmpeg normalizes to **H.264 High 4.1, yuv420p,
  30 fps CFR, CRF 17 (max 12 Mbps), GOP 60, +faststart, AAC 128k stereo 48 kHz** (a silent track when there's
  no audio: some placements reject video with no audio stream). Output: `<slug>_<cut>_<format>.mp4`.
- Platform limits this clears: Meta (≤4 GB, 1–241 min, H.264/AAC mp4), LinkedIn (75 KB–200 MB, 3s–30 min,
  ≤30 fps), YouTube (bumper ≤6s exactly; in-stream any length). Keep ads ≤15s unless asked.

### 8. Frame QA (contact sheet) — required

```bash
$SK/scripts/qa.sh "$AD"
```

Writes `qa/specs.txt` (size, duration, fps, codec, pix_fmt, audio), and per file `_contact.jpg` (1 frame
per second, left to right), `_safezone.jpg` (same frames with the safe box in red) and `_poster.jpg` (frame 0).
**Open every sheet and look.** Pass only when all are true:

- [ ] Specs match: right canvas, duration = cut, 30 fps, h264, yuv420p, aac.
- [ ] Frame 0 reads on its own (it is the thumbnail): hook caption + visual present.
- [ ] Hook is readable by 2s; CTA is on screen by 10s and holds to the end.
- [ ] No word, number or logo crosses the red box on any frame.
- [ ] No overlapping text mid-transition (sample the hand-offs at 0.1s steps with `ffmpeg -ss`).
- [ ] Every number on screen equals the source exactly (count-ups land on the final value).
- [ ] One gradient element per frame; no pure white or black; DM Sans only; no banned words
      (unlock, leverage, empower, transform, seamless, robust, game-changing, best, agent, "!").
- [ ] Nothing animates in before it should (a stray dot or ripple at rest means a missing `immediateRender: false`).
- [ ] No AI imagery, no people, no stock: every pixel traces to the spec.

Record the result (pass, or each fix made) in the ad folder README.

### 9. List what you cut

Every ad folder README ends with **"What I cut"**: beats, lines, numbers or formats left out and why
(time, a claim that couldn't be sourced, a second gradient, a quote that wasn't verified). It lets Alex
put something back in one sentence instead of re-briefing.

### 10. Where outputs go

```
~/Desktop/PropFuel/03 Video/PropFuel Motion Ads/<slug>/
  README.md                       storyboard, proof table, QA result, What I cut, approval status
  brief.xml                       the XML brief (art_direction, references, timing, deliverable, proof)
  spec.json                       the program's input (re-render from this)
  <slug>_<cut>_<format>.mp4       deliverables
  qa/                             specs.txt, *_contact.jpg, *_safezone.jpg, *_poster.jpg
  qa/keyframes/                   the pre-render keyframe sheets (step 7a)
  src/<cut>-<format>/             the generated HyperFrames projects (npx hyperframes preview to scrub)
~/Desktop/PropFuel/03 Video/PropFuel Motion Ads/_fx-tests/<slug>/   1-second tests (step 4b)
```

Log the outcome to the OS (`log_update`) with the folder path. Don't commit mp4s to any repo.

**Drive library:** after rendering, make sure `~/Projects/propfuel-drive-sync/manifest.yaml` covers the new ad's
folder (status `pending` until Alex approves; flip it to `ready` on his yes), then run
`~/Projects/propfuel-drive-sync/.venv/bin/python ~/Projects/propfuel-drive-sync/sync.py`.

### 11. Approval (standing rule)

Hand Alex the exact file paths and the contact sheets and ask: approve as-is, change, or kill. **Nothing goes
to Meta, LinkedIn, YouTube, Webflow, HubSpot or anyone outside PropFuel until Alex approves that exact file.**
A re-render is a new file and needs a new yes. After approval, ad setup follows propfuel-meta-ads
`campaign-setup` (always PAUSED).

## Effects library

Six effect beats on vendored open-source libraries, each made deterministic for HyperFrames (one paused
timeline, seekable, seeded, no clocks or network). Full guide, spec fields and "don't use it when" in
`references/effects.md`; licenses in `engine/vendor/LICENSES.md`.

| type | Library | Use it for |
|---|---|---|
| `stack` | Matter.js | Word cards fall and pile up (topics, signals, reasons). `preDrop` lets it open the ad |
| `sketch` | Rough.js | Hand-drawn circle / underline / box / hatch around one number or word |
| `brush` | p5.brush (standalone, WebGL2) | Textured gradient swipe behind one word of a headline |
| `filter` | PixiJS + pixi-filters (WebGL) | `glow`: a gold halo blooms on one line. `glitch`: a short seeded burst that resolves to clean type |
| `orb` | thinking-orbs engine (MIT port) | An AI-thinking / listening moment: Poppy, "PropFuel is listening", the builder working |
| `words` | Anime.js | Optional: GSAP covers this. The documented, seekable Anime.js pattern (`window.__hfAnime`) |

Rules: one effect beat per ad, two at most; each counts toward the one-gradient-per-frame rule; every effect
animates in, so frame 0 belongs to a caption + static beat (or `stack` with `preDrop`); a 1-second test (4b)
before the full build. Demo spec: `examples/fx-demo.json` (no client named, only "370+ associations").
Inspiration only, never copied: https://skillry.dev/ai-videos/opus-5-5 and
https://github.com/yihui-dev/awesome-opus5-5-videos.

## Files

- `engine/build.mjs` spec → projects (`--test <cut>:<i>[@s]` builds a 1-second test) · `engine/scenes-product.mjs`
  product-UI beats · `engine/scenes-fx.mjs` effect beats · `engine/template.html` look (brand v5.2: cream #F4F1EA + grain, charcoal
  #2F2F2F, DM Sans, one #F47C2C→#FBC02D gradient) · `engine/formats.json` canvases + safe zones ·
  `engine/assets/` DM Sans variable font + PropFuel logo · `engine/vendor/` GSAP 3.14.2 + the effect libraries (no CDN at render; `LICENSES.md`, `licenses/`, and the
  thinking-orbs port source in `src/`)
- `scripts/test-1s.sh` 1-second test of one beat · `scripts/keyframes.sh` pre-render keyframe sheet ·
  `scripts/render.sh` budget gate + check + render + H.264 export · `scripts/qa.sh` post-render contact sheets
- `templates/brief.xml` the XML brief · `references/effects.md` the effects guide
- `examples/txcpa-autorenewal.json` the reference ad (15s + 6s cuts) · `examples/fx-demo.json` every effect beat
