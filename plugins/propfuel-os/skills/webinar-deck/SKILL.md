---
name: webinar-deck
description: Build a PropFuel webinar's slide deck AND talk track from the webinar brain (21 past 2026 sessions: every slide, what was said over it, what landed). New webinar → a full deck + talk track in the house structure and Brittany's voice. Repeat webinar → start from the last run's deck and talk track, propose a change list for approval, then write the updated version. Outputs an editable PPTX (talk track in the speaker notes; opens in Google Slides) and a PDF. Use when someone says "deck", "slides", "talk track", "build the webinar deck", "refresh the deck for the repeat", or the webinar build's deck step runs.
---

# Webinar deck + talk track

The brain is in the PropFuel Marketing OS (load with `get_knowledge`; in a content-repurposer checkout the same files are in `knowledge/webinars/`):
- `Webinar Deck - DECK-BRAIN.md`: how PropFuel webinar decks are built (arc, timing, layout library, Brittany's talk-track voice, polls, proof, what hurts depth) and the procedure for a new webinar.
- `Webinar Deck - REPEAT-PLAYBOOK.md`: how a repeat gets refreshed, learned from real repeats (UST Apr 22 → Jun 3, win-back Mar 27 → Jul 9).
- `Webinar Deck - INDEX.md`: every 2026 session, its performance, and which Q4 webinar it seeds.
- `Webinar Session - <date-slug>.md` (repo: `sessions/<date-slug>.md`): one record per past webinar, slide by slide with the talk track as it was actually said. The comparisons: `Webinar Session - diff-ust-original-vs-repeat.md`, `Webinar Session - diff-winback-mar27-vs-jul09.md`, `Webinar Session - series-year-in-between.md`.

## 1. New or repeat?
Look the title and topic up in the INDEX. A repeat (same title, or the OS webinar's `type: Repeat` / `prior_run`) or a close sibling (same campaign topic) starts from that session's record. Otherwise it's new.

## 2a. New webinar
Follow DECK-BRAIN "Generation procedure". Inputs: title, date, length, presenter(s) and guest(s), the description, the proof you're allowed to use (`Case Studies - Master.md`, `ROI - Master.md`), and the 2–3 closest past sessions from the INDEX (read their records: reuse what landed, avoid what lost the room).

## 2b. Repeat
Follow the REPEAT-PLAYBOOK:
1. Load the prior session record: its slides, talk track, Q&A, audience signals, lessons and any "Refresh notes for <date>".
2. Write the **change list** first (slide · keep / edit / cut / add · why · evidence) and stop for approval. On the webinar build this goes on the webinar's Notion card and to the presenter; nothing else is written until a person says yes.
3. After the yes, write the new deck JSON: unchanged slides copy their on-screen text and talk track from the record; edited slides change only what the change list says.

## 3. Output
- A deck JSON for the renderer (layouts and fields are the `LAYOUTS` dict at the top of it; every slide carries `notes` = the talk track for that slide, first person, in the presenter's voice, timed to the session length).
- Render. The renderer is one self-contained Python file: in a content-repurposer checkout `templates/deck/render.py`; bundled next to this skill as `render.py` (claude.ai org skill); anywhere else `get_knowledge "Skill - webinar-deck - renderer.md"` and save its code block as `render.py`. Then `pip install python-pptx` and `python3 render.py deck.json --out <dir>` → `.pptx` (editable, talk track in the speaker notes, opens in Google Slides) + `.pdf` (house look; needs Chrome or Playwright Chromium, otherwise you get the PPTX and the HTML).
- A one-page talk-track doc (slide number, headline, the notes, the timing) for the presenter to rehearse from.
- On a webinar build: attach the PPTX, PDF and talk-track doc to the webinar's Notion card ("Slide deck" toggle) and set the OS asset slots `deck` and `talk_track` (update_event action asset, slot, link, status draft). The presenter reviews; never mark them done yourself.

## Rules
- Proof comes from the OS `Webinar Proof Map.md` first (each Q4 webinar's premier case study plus banks like the Oct 28 win-back proof bank, with exact wording and source checks), then `Case Studies - Master.md`. Only sourced proof; current house numbers (12% avg annual revenue growth vs 0.98% for the average association; 370+ associations; tagline Know and Grow Your Membership). If a past slide disagrees with what was said aloud, use the sourced number and flag it.
- Client names only as the records and Case Studies - Master allow.
- No attendee names anywhere.
- Run `brand-qa` on the deck text and the talk track before handing it over.

## Visual QA before handoff (self-improve, Oct 20 2026)
Alex has rejected visuals shipped without a render check. Before showing anything:
- Render at desktop and 390px mobile; open the screenshots and look at them (do not assume).
- Check: text overflow or smashed text, ugly negative space, orphan words (balance/pretty wrap), H2s on mobile, overlapping controls, button styling, GIF/video playback.
- Re-check every feature Alex asked to keep (regression list), not just what you changed.
- Fix issues first; only then send.
