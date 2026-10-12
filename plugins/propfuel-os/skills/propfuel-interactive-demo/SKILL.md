---
name: propfuel-interactive-demo
description: Build an interactive PropFuel demo, a "lab" a prospect plays with instead of reading a brochure. It's one self-contained page with a real model, controls that change the result live, a side panel that explains every change in plain language, and one named rule the math must obey: only published PropFuel numbers (ROI - Master, Case Studies - Master), never invented. It ships as a noindex preview on propfuel-page-previews, and only after Alex approves as a GitHub-built page on propfuel.com. Use when someone says "interactive demo", "lab", "calculator", "let them play with it", "ROI simulator", "renewal lab", "make it interactive", or wants a prospect to see PropFuel's effect on their own numbers.
---

# PropFuel interactive demo

This adapts pattern 2 of the Opus 5.5 build guide ("An interactive explainer or lab") for PropFuel. The prospect moves sliders for their own situation, flips a PropFuel switch, and watches the outcome change. Each change is explained in plain words next to it. The worked example is the **Renewal lab**: `src/renewal-lab/` in `~/Projects/propfuel-page-previews`, also shipped next to this file as `renewal-lab.embed.html`.

It's a draft until Alex approves it. Don't post the URL anywhere public, email it or put it on propfuel.com yourself.

## When to use it

- A PropFuel effect is easier to feel than to read: renewal rates, lapsed win-back, new-member onboarding, response rates, staff time.
- A rep or a page needs "what would this mean for us?" answered on the prospect's own numbers.
- A Q4 campaign, ad or email needs a destination people play with instead of a PDF.

**Not this skill:**
- A one-prospect asset from Salesforce data. Use `winback-walkthrough`.
- A static page. Use the `web-page` flow in the content repurposer.
- A forecast or quote. A lab shows a published result applied to their numbers, never a promise.

## 0. Before you build: two rules from the guide

1. **Set a budget first.** Before a long unattended build, write down the limit in time and credit. The default is 90 minutes of agent time for one lab, and ask before going over it. The guide's optics lab took 86 minutes and $25.66 of API credit. Use flat-plan apps for exploring, and keep API runs for the real build.
2. **End every build with "what I cut", plus a human play-test.** List every feature you dropped or simplified, and every modelling choice someone could argue with. Then a person plays it on a phone and on a laptop, tries to break it, and reads the numbers before anyone external sees it. A build that looks finished in a screenshot doesn't count as tested.

## 1. Pick the one number and its proof

Load the proof with the OS `get_knowledge`: `ROI - Master.md` and `Case Studies - Master.md`. Pick **one** published result that the lab's switch stands for, and write down the exact line you're using.

**The named rule.** Every number in the math comes from those two documents, and nothing else. Label each one:
- **One client's result** (a case study): name the client only if its case study is live on propfuel.com (`get_case_studies`, stage Live). Otherwise say "one association". The Renewal lab uses AAMFT's 80.5% → 95% on-time renewals, unnamed.
- **Platform-wide** (ROI - Master, as of Feb 2026). For example: 8.68% average year-one revenue growth, $650K average first-year revenue growth, 72% of declining organisations reversed course. Write "platform-wide" or "across PropFuel clients" next to it.

Never invent a benchmark, a lift, a conversion rate or a "typical association" number. If the model needs a number the documents don't have, the prospect sets it with a slider, or you cut that part and list it under "what I cut".

**Apply the proof honestly.**
- Turn the result into the smallest rule that reproduces it exactly at the published starting point. The Renewal lab closes the same *share of the gap*: (95 − 80.5) / (100 − 80.5) = 74%. That gives exactly +14.5 points at 80.5% and can never pass 100%.
- Show that rule on the page, in one sentence.
- Say what the output is *not*. Late renewers would have paid eventually, so the Renewal lab says "dues renewed on time instead of late or at risk", not "new revenue".
- Put this line under the model: "one association's published result applied to your numbers, not a forecast or a guarantee".

## 2. The build prompt (paste, fill the brackets)

```
Build an interactive PropFuel lab that teaches [WHAT PROPFUEL CHANGES] by letting an association
staff member play with it, not by describing it.

Rules:
- One self-contained embed: a <style> block, the markup in one root <div class="[px]" id="[px]">,
  and one <script>. No external assets, no libraries, no build step. DM Sans is already on the page.
- The main object is a real model of [THEIR SITUATION]. Controls: [2-4 sliders for their own
  numbers, with sensible ranges and sample defaults] and one switch: "[THE PROPFUEL ACTION]".
  Moving any control changes the outcome live (on input), not on a submit button.
- A side panel, "What changed, and why", explains each change in plain language with the new
  numbers: what moved, why, and how it follows from the rule. Newest first, last 4 kept, aria-live.
- It has to be correct. THE NAMED RULE: the only numbers in the math are [PASTE THE EXACT LINES
  FROM ROI - Master / Case Studies - Master], labelled [one association / platform-wide]. State
  the rule in one sentence on the page, and add a fine-print line saying it's one published result
  applied to their numbers, not a forecast.
- Show the result three ways: one big number (the single gradient focal element), a few plain
  supporting numbers, and a visual of the model (e.g. 100 dots = every 100 members) that
  changes state when the switch flips.
- PropFuel brand v5.2 (below), apple-design motion, prefers-reduced-motion, works at 375px.

Plan the whole thing first, then build it in one pass. Then list what you cut, and every
modelling choice someone could argue with.
```

## 3. Brand, motion, mobile

The brand guide is `knowledge/brand/brand-style-guide-v5.2.md` in the content repurposer. The guide's prompt says "dark background, one accent colour". For PropFuel, that becomes:

- **Colour:** warm surfaces only (`#F4F1EA` page, `#F6F2E8` cards, `#EAE4D8` deep) with T1 grain, and charcoal `#2F2F2F` for text and for the dark side panel. Never pure white or black, and no cool greys. Heritage Steel `#4A7FA5` is for links only.
- **Gradient:** one focal element per page. Use the text fill (`to top, #F47C2C → #FBC02D`) on the big result number and nowhere else. Buttons use the horizontal gradient. Small marks under 32px use solid `#F9A825`.
- **Controls:**
  - Range thumbs are 28px with a 44px hit area.
  - The toggle follows §6G: a 44×24 track that is `#E7E2D8` off and `#F47C2C` on.
  - Labels sit above the control (13px, weight 600), with the live value on the right in tabular numbers.
- **Motion (apple-design):**
  - Respond on input.
  - Number tweens retarget every frame, so a new drag interrupts the old one cleanly.
  - The switch thumb moves on a light spring. Dots change state with a small stagger.
  - Entrance only, moving up 24px with a fade, staggered 100ms.
  - Nothing animates out, and nothing slides in from the side.
- **Reduced motion:** numbers jump to the new value, with no stagger, no springs and no entrance.
- **Mobile:**
  - At 375px the layout stacks into controls → model → panel, and the page never scrolls sideways.
  - Set `touch-action: pan-y` on sliders so scrolling still works.
- **Accessibility:**
  - Use real `<input type=range>` controls with `<label>` and `<output>`.
  - The switch is a `<button role="switch" aria-checked>`.
  - The visual gets `role="img"` with a live `aria-label` that states the numbers.
- **No modal dialogs.** No `alert`, `confirm` or `prompt`, ever.
- **Copy rules:**
  - "370+ associations" if a count appears.
  - "Know and Grow Your Membership" for the tagline.
  - Left-align the copy, and run `ig-human`/`li-human`-style checks: no em dashes, no slop words.
- **CTA:** one Book a demo button to `https://www.propfuel.com/book-a-demo?utm_source=<slug>&utm_medium=interactive&utm_campaign=<slug>`.
- **Webflow-proof CSS:** prefix every class, put the resets at (0,1,0) as `:where()` under the root class, and add `html[data-wf-page] .<px>-wrap{padding-top:124px}` so the page clears the fixed propfuel.com nav.

## 4. Ship it: preview first, then the site the way our pages ship

**Preview (always first).** Repo: `~/Projects/propfuel-page-previews`, served at https://propfuel-page-previews.vercel.app. Every response is noindex and robots.txt disallows everything.

1. Create `src/<slug>/`, containing:
   - `embed.html`: the lab.
   - `page.json`: `slug`, a *proposed* `liveUrl`, `title`, `description`, `ogTitle`, `ogDescription`, `ogImageAlt`, `"schema": "webpage"` and `"ctaCampaign": "<slug>"`.
   - `og.html`: a 1200×630 card.
2. Run `node build.mjs`. This writes `public/<slug>/` with the page, the OG image and the Webflow handoff files.
3. Play-test locally, then deploy with `npx vercel deploy --prod --yes --scope alex-7579s-projects`. This deploys the previews site, not propfuel.com.
4. Check `https://propfuel-page-previews.vercel.app/<slug>`: it should return 200, and the headers should include `X-Robots-Tag: noindex`. Then commit to the repo.

**Live on propfuel.com (only after Alex approves the preview).** Ship it the way `/membership-ai-overview` shipped (handoff: `~/Desktop/Membership AI Page Update/membership-ai-page-handoff.md`).

1. **Webflow shell:**
   - Create a page with only the Navigation and Footer components.
   - In the page settings, add the SEO title and description, the OG title, description and image, and the head code from `public/<slug>/webflow-page-head.html`.
   - Crawlers and iMessage read these from the server HTML, so they stay in Webflow.
2. **Build the page module:** run `node tools/gh-page.mjs <slug> <propfuel-webflow-custom clone>`. It writes `js/pages/<slug>.js` and guards on your root id.
3. **Add the loader:** in `js/webflow-enhancements.js`, add a path-gated loader for `/<slug>` that loads `js/pages/<slug>.js?v=1`. Copy `renderMembershipAIOverviewPage()`.
4. **Publish:**
   - Copy the OG image to `og-images/<slug>.png`.
   - Scan for secrets and PII, then commit and push to `main`. GitHub Pages serves `main`, so the merge makes it live.
   - Bump `?v=` on every later change.

## 5. Check before anyone external sees it

- Every number in the script traces to a line in ROI - Master or Case Studies - Master, and the rule is stated on the page. Recompute the published starting point by hand: the Renewal lab at 80.5% must give exactly 95%.
- Labels are honest: "one association" or "platform-wide", "not a forecast". No client name unless the case study is live.
- Play-test at 1280 and 375, and with reduced motion on.
  - Check the extremes of every slider: min, max, and any spot where rounding shows.
  - No console errors, no sideways scroll.
  - The side panel text reads right at every setting.
- Write the **"what I cut"** list and give it to Alex with the preview URL.
- Log it to the OS with `log_update`. Include the slug, the preview URL, the proof line used and the cut list.

### Renewal lab: what was cut and what can be argued (template for your own list)

- **Share-of-gap vs flat +14.5 points.** The lab uses share of gap (74%). A flat lift would be simpler, but it breaks above 85.5%.
- **On-time is not new revenue.** Some late renewers would have paid anyway, and the page says so.
- **The 7% membership growth is shown as a stat only.** It isn't applied to their numbers.
- **8.68% (platform-wide) is context only.** It isn't in the math.
- **No multi-year view, no staff-time saving, no per-segment controls.** There is no published number for these.
