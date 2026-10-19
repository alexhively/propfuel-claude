---
name: li-carousel
description: >-
  Build a LinkedIn document post (carousel) - slide-by-slide copy, the cover
  that earns the swipe, and the PDF to upload. Use when the user says
  "carousel", "document post", "slides for LinkedIn", "turn this into a
  carousel", or has a list-shaped idea that would die as a text post.
metadata:
  origin: linkedin-agent-skill
---

> **PropFuel adaptation.** From the LinkedIn Agent Skill (github.com/avi691/linkedin-agent-skill, MIT, by Avi Grondin and Jake Schincariol; license in `li-human/LICENSE-linkedin-agent-skill`). PropFuel rules win over anything below.
>
> 1. **Load the brain first.** If the PropFuel Marketing OS connector is available, call `get_knowledge` "LinkedIn - Master.md" before anything else, then the matching LinkedIn KB doc(s) for this job: formats-playbook (named "LinkedIn KB - <topic>.md"; if a name doesn't match, check the knowledge list). The Master doc wins over the generic advice in this skill where they differ.
> 2. **Voice.** Use `~/.claude/linkedin/voice.md` if the person has one (their personal voice for their own profile). Otherwise, and always for the PropFuel company page, use `${CLAUDE_PLUGIN_ROOT}/skills/li-post/propfuel-voice.md`, which comes from the Brand Persona and Core Message masters.
> 3. **Hard rules.** Say "370+ associations", never another count. The tagline is "Know and Grow Your Membership". Numbers only from the ROI - Master and Case Studies - Master docs, never invented. Clients may be named without a live case study. No client quote or testimonial without written consent. Never post, comment, connect or send a DM: every skill ends with copy the person reads, approves and pastes themselves.
> 4. **Log it.** When a post, plan or audit is done, record one line in the OS with `log_update`.

# li-carousel

Document posts are the highest-dwell format on LinkedIn, because a swipe is
counted and a scroll is not. The format rewards one idea broken into steps.
It punishes a text post cut into pieces.

## When to use it instead of a text post

Use a carousel when the idea has **sequence** - steps, a countdown, a
before/after progression, a framework with parts. Use a text post when the
idea is one claim. Splitting one claim across eight slides is the most common
way carousels fail, and if that is what the user has, say so and hand them to
`/li-post`.

## Structure

8-12 slides. Under 8 is a text post. Over 12 and the completion rate falls off
a cliff.

```
1        COVER      the hook, 6 words or fewer, plus one line of promise
2        THE STAKE  why this matters, in one sentence
3-N      ONE IDEA PER SLIDE. A headline of 3-7 words, and at most 25 words
                    under it. If a slide needs a paragraph, it is two slides.
N+1      RECAP      the whole thing as a list, so the screenshot is useful
LAST     CTA        one action. Follow, comment a keyword, or the link. One.
```

## Slide copy rules

- **Slide 1 is 80% of the result.** Six words. Big. The rest of the deck
  cannot save a cover nobody swipes.
- **Number every slide** (3/10). Completion goes up when people can see the
  end.
- **No slide is a paragraph.** If you cannot say it in 25 words, split it.
- **The recap slide is the one people screenshot.** Make it standalone.
- **The user's handle on every slide**, small, bottom corner. Screenshots
  travel without you.

## Making the PDF

LinkedIn wants a PDF, 1080x1350 (4:5) for maximum feed real estate, under
100MB, under 300 pages. Build it as HTML and print to PDF:

```bash
# one page per slide, 1080x1350, no margins
# then: Chrome headless --print-to-pdf, or any HTML-to-PDF you already use
```

Write the HTML with one `<section>` per slide, `width:1080px; height:1350px;
page-break-after:always`, a single accent colour, and type no smaller than
28px - people read these on a phone at thumbnail size. If the user has a brand
skill or design system in this project, use it and do not invent a palette.

**PropFuel brand (wins over the generic advice above):** DM Sans only, nothing else, loaded from Google Fonts with system fallbacks.
Background Card Cream `#F6F2E8` (Deep Cream `#EAE4D8` for alternating slides), all text Charcoal `#2F2F2F`, and Golden Yellow `#FBC02D` as the single accent for the cover band, slide numbers and one highlighted word per slide.
The last slide carries "Know and Grow Your Membership" and propfuel.com. The full system is in the meta-ads repo's `knowledge/brand-style-guide-v5.2.md`, or ask the OS for the brand style guide.

## Output

The slide-by-slide copy first, as a numbered list the user can read in ten
seconds. Then the accompanying **post text** - a carousel still needs 2-3
lines above it, which is the actual hook in the feed. Run both through
`/li-human`. Then build the PDF only if the user approves the copy.

Nothing is uploaded to LinkedIn. The user posts the PDF themselves.
