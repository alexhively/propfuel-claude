---
name: storytelling
description: "Four-beat story loop (stakes, big question, head fake, rehook) for any PropFuel asset that tells a story: case studies, webinar openers and talk tracks, LinkedIn posts and carousels, reels, testimonial and motion-ad hooks, sales-call stories, emails, lead-magnet intros. Use alongside the asset's own skill: that skill sets the format, this one sets the narrative shape. Use when someone says 'make this a story', 'storytelling', 'hook them', 'make it addictive', 'head fake', 'rehook', or a draft reads flat."
metadata:
  version: 1.0.0
  origin: Adapted from Kallaway's "addictive storytelling" video (https://youtu.be/KyC8r-zitVE), Oct 21 2026
---

# Skill - storytelling

## What it's for
A four-beat story loop that keeps an audience leaning in. Use it on any PropFuel asset that tells a story: case studies, webinar openers and talk tracks, LinkedIn posts and carousels, testimonial and motion-ad hooks, sales-call stories, emails, lead-magnet intros. Load it alongside the asset's own skill (case-study, linkedin-post, webinar-deck, etc.). That skill sets the format; this one sets the narrative shape.

Source: adapted from Kallaway's YouTube video on "addictive storytelling" (https://youtu.be/KyC8r-zitVE), saved Oct 21 2026 at Alex's request. The core claim is that attention runs on anticipation, not payoff. People stay when they're predicting what happens next and get pulled along when the outcome surprises them. A predictable story works like a vending machine and loses the room. An uncertain one holds it.

## Inputs
- The asset type and its channel (post, case study, webinar, ad, call)
- The raw material: transcript, case study draft, campaign results, call notes
- The proof you're allowed to use: the Case Studies, Testimonials and ROI masters, CLEARED tags for AMC work, and verbatim quotes only
- The audience and what they personally care about (Target Audience and JTBD masters)

If the PropFuel Marketing OS connector is available, pull the masters with `get_knowledge` before drafting.

## Steps
1. **Stakes: make them care.** Before anything happens, the reader needs three things:
   - **A person they can root for.** This is usually a membership director, an ED, or a team at a named or described association.
   - **Something at risk.** Examples: renewal revenue, a lapse rate the board is watching, a conference that needs registrations, a new-member cohort that never logs in.
   - **A clock.** Examples: renewal season, a board meeting, a budget deadline, the next dues cycle. A specific time window beats "eventually."
   Stakes don't need drama. They need to feel real to an association professional.
2. **Big question: give them something to predict.** Load in enough specific detail that the reader forms a guess, then hold the answer back. Vague teasers ("something surprising happened") don't work, because there's nothing to guess at. Put the biggest question as early as possible.
3. **Head fake: break the prediction, but fairly.** Work out what a typical reader would expect, then reveal something different that clicks once they hear it. For associations, the expected answer is usually "they sent more emails," "they discounted dues" or "they bought a new AMS." The real answer is often simpler and more human: they asked members one question and listened. Plant the clues earlier so the reveal feels earned. A random twist only confuses people.
4. **Rehook: open the next question before closing the last one.** At every point where a section ends and attention could drop, start a new question in the same sentence. Useful connectors:
   - "which would have been great, except…"
   - "but the answers showed something else…"
   - "that's when they realized…"
   - "which is exactly why…"
   Don't let a section end on "anyway, that went well."
5. Repeat steps 2 to 4 for longer pieces (webinars, case studies, carousels). Short pieces like a post, a reel or an ad can run the loop once and end the final rehook on the CTA.

## Standards
- **Facts first, shape second.** The loop structures true material. It never adds invented stakes, numbers, deadlines, customers or outcomes. Every stat and quote follows the Hard rules (12% always next to 0.98%, 370+, NAIFA ROI wording, verbatim quotes only, ALA disambiguation).
- **Keep the brain science out of customer-facing copy.** Dopamine, casino and addiction language is the source's teaching frame, not PropFuel voice. Our voice is plain, specific, confident and warm.
- **Plant the head fake.** If you can't point to the earlier line that sets up the reveal, rewrite it.
- **Specific beats dramatic.** "Three weeks before the renewal deadline" beats "the clock was ticking."
- **Check the stakes test before drafting.** Who is it happening to, what's at risk, and why now. If any of these is unclear in the opening, fix the opening first.

## Corrections
- 2026-10-21 (Dave Will, via Alex, on the running-reel hooks): **The hook must name something association pros really do and really feel.** Don't tell them to stop a standard practice (three renewal reminders are universal) or a habit they don't have (discounting lapsed members is rare), and never tell them to stop a growth channel we'd also recommend (ads for new members). Hook on the pain behind the practice instead, e.g. "Stop sending so many emails just to get your members to renew." Check every hook against: do associations actually do this, would PropFuel agree they should stop, and does it hurt?

## Examples
Illustrative shapes only. Pull real numbers from the masters before using any of these.

- **Flat (vending machine):** "An association used PropFuel for win-back and got members back."
- **Loop version (win-back webinar or post):**
  - *Stakes:* A medical society's lapsed list kept growing, and every lapsed member was dues walking out the door.
  - *Big question:* So they asked the lapsed members why they'd left. What do you think most of them said?
  - *Head fake:* Most of them didn't know their membership had expired.
  - *Rehook:* Which meant the problem wasn't value at all. It was something much easier to fix…
  - The stat behind this example is the international medical society proof in the Webinar Proof Map, never named publicly. Verify the figures there before use.
- **Sales-call story:** Stakes (the renewal team's quarter), big question (what the first answers showed), head fake (the members they assumed were safe weren't), rehook into the demo.

## Before it ships
- [ ] Can you name the stakes, the big question, the head fake and each rehook in the draft?
- [ ] Is the head fake set up by an earlier clue?
- [ ] Is there any dead air between sections? If so, add a rehook.
- [ ] Is every number and quote sourced to a master or a verbatim transcript?
- [ ] Is the copy free of dopamine, casino and addiction framing?
- [ ] Has it passed the asset's own skill and `Skill - brand-qa.md`?

## Changelog
- 2026-10-21 (Wed): Created from Kallaway's "addictive storytelling" video transcript, at Alex's request. Moved into the propfuel-os plugin (git is the source of truth; the OS doc syncs from here).
