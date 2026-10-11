---
name: ig-carousel
description: >-
  Build an Instagram carousel - the cover that earns the swipe, slide-by-slide
  copy, and the 1080x1350 files to upload. Use when the user says "carousel",
  "slides", "swipe post", "turn this into a carousel", or has a list-shaped or
  step-shaped idea that would die as a single image.
metadata:
  origin: instagram-agent-skill
---

> **PropFuel adaptation.** From the Instagram Agent Skill (github.com/Jakeschincariol/instagram-agent-skill, MIT, by Jake Schincariol; license in `ig-human/LICENSE-instagram-agent-skill`). PropFuel rules win over anything below.
>
> 1. **Load the brain first.** If the PropFuel Marketing OS connector is available, call `get_knowledge` "Instagram - Master.md" before anything else, and "Skill - instagram.md" for the workflow detail on carousels. The Master doc wins over the generic advice in this skill where they differ. If the name doesn't match, check the knowledge list.
> 2. **Voice.** Use `~/.claude/instagram/voice.md` if the person has one (their personal voice for their own account). Otherwise, and always for the PropFuel company account, use `${CLAUDE_PLUGIN_ROOT}/skills/ig-caption/propfuel-voice.md`, which comes from the Brand Persona and Core Message masters.
> 3. **Hard rules.** Say "370+ associations", never another count. The tagline is "Know and Grow Your Membership". Numbers only from the ROI - Master and Case Studies - Master docs, never invented. Name a client only if its case study is live on propfuel.com; otherwise "one association". No client quote, testimonial or client footage without written consent. Never log into Instagram, never post, comment, reply, DM or schedule anything, and never set up automation on anyone's behalf: every skill ends with copy the person reads, approves and posts themselves. It writes, you post.
> 4. **Scripts** in this pack are stdlib-only and run locally: `python3 -I "${CLAUDE_PLUGIN_ROOT}/skills/<skill>/<script>.py" …`. Nothing is uploaded.
> 5. **Log it.** When a reel, plan or audit is done, record one line in the OS with `log_update`.

# ig-carousel

Carousels are the highest-dwell format on the grid, because a swipe is an
interaction and a scroll is not. They also get a second chance: Instagram can
show a carousel again starting from a later slide to someone who did not engage
the first time, so slide two has to stand on its own as well.

The format rewards one idea broken into steps. It punishes a caption cut into
pieces.

## When to use it instead of a Reel

Use a carousel when the idea has **sequence and needs to be re-read**: steps, a
framework with parts, a before and after, a list worth screenshotting. Use a
Reel when the idea has motion, a face, or a payoff that has to be seen
happening.

If the idea is one claim, it is neither. Hand it to `/ig-reel` and say so.

## Structure

6 to 10 slides. The cap is 20 and 20 is almost always a book nobody finishes.
Under 5 and the swipe never starts.

```
1         COVER     the hook. 6 words or fewer, at a size that is legible in
                    the grid at thumbnail. One line of promise under it.
2         THE STAKE why this matters, in one sentence. This slide is also a
                    second cover, so it cannot be setup.
3 to N    ONE IDEA PER SLIDE. A headline of 3 to 7 words, at most 25 words
                    under it. If a slide needs a paragraph, it is two slides.
N+1       RECAP     the whole thing as a list. This is the screenshot slide.
LAST      CTA       one action. Save, comment a keyword, or follow. One.
```

## Slide copy rules

- **The cover is 80% of the result.** Six words. Big. Nothing on the deck saves
  a cover nobody swipes.
- **Design for the grid crop.** The profile grid crops to a portrait rectangle
  that is taller than it is wide, and the exact ratio has moved more than once.
  Build at 1080x1350 and keep the cover text well inside the middle, clear of
  the outer 120 pixels on every side, and the crop stops mattering.
- **Number the slides** (3/8). Completion goes up when people can see the end.
- **No slide is a paragraph.** If it cannot be said in 25 words, split it.
- **The recap slide is the one people screenshot and send.** Sends are the
  strongest signal you can earn. Make it standalone and readable with no
  context.
- **The handle on every slide**, small, bottom corner. Screenshots travel
  without you.
- **Alt text on the cover at minimum.** It is read by screen readers and by
  Instagram.

## Building the files

Instagram wants 1080x1350 (4:5), JPEG or PNG, up to 20 items. Build it as HTML
and print each slide:

```bash
# one <section> per slide, 1080x1350, page-break-after: always
# then Chrome headless --print-to-pdf, or any HTML-to-image you already use
```

**PropFuel brand (company account and anything about PropFuel):** DM Sans throughout; cream backgrounds #F6F2E8 / #EAE4D8, charcoal text #2F2F2F, one gold accent #FBC02D. No other palette, no stock-photo clichés. Personal accounts may use their own look, but keep PropFuel slides on-brand.

Write the HTML with `width:1080px; height:1350px`, a single accent colour, and
type no smaller than 32px, because this is read on a phone at a third of its
real size. If the project has a brand skill or a design system, use it and do
not invent a palette.

## Output

The slide-by-slide copy first, as a numbered list the user can read in ten
seconds and edit before anything is rendered. Then the **caption**, which for a
carousel is Job B in `/ig-caption`: the caption is doing work here, because the
cover has already used its six words.

Run both through `/ig-human`. Build the files only after the user approves the
copy.

```
CAROUSEL  ·  8 slides

1  COVER   THE $18,000 CLAUSE
           One line I now put in every contract.
2  STAKE   I approved the work. They asked for the money back nine days later.
3          WHAT IT SAYS
           Payment on delivery, not on approval.
...
7  RECAP   All four lines, in order.
8  CTA     Comment CONTRACT and I will send the full clause.

Caption: Job B, hook in line 1, one ask, 3 tags.
```

Nothing is uploaded. The user posts it.
