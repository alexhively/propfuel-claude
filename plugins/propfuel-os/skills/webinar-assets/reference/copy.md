# Webinar copy system

Source: Alejandra's Webinar Assets project (master doc section 7 and 8). Draft only. Nothing is sent, posted or uploaded; Alex and Alejandra review first.

## Brand rules (every piece of copy)
- Tagline: "Know and Grow Your Membership" (front-facing). "Make Membership Meaningful" is the umbrella line only.
- Growth stat: "12% average annual revenue growth after implementing PropFuel", always next to "vs 0.98% for the average association". Never 8.68%.
- Reach: "370+ associations" (end cards add "and counting").
- A client is named in public copy only if their case study is live (check get_case_studies). Otherwise anonymize ("a veterinary association"). FelineVMA is always anonymous outward.
- No em dashes. Use a colon, comma, period or parentheses. (Only exception: a series name that carries its own dash.)
- Conversational, professional, human. First person from the actual sender. Bold only the full series name and the full session title.
- No session counts ("Session 1 of 4"). No "free" near a CTA. No question marks in subject lines.
- Never mention a repeat, a session that will run shorter than its blocked hour, or anything leadership asked to keep private. Never say "again" or "back by popular demand".
- Never invent links, dates or registration pages (use the card's Tracking Links). Unknowns are [square-bracket placeholders]. Speaker name stays out of the pop-up description.
- Keep proof points and case studies out of the Zoom description.

## 1. Zoom description (no links)
Bold title line, italic tagline line if a series, hook paragraph, framing paragraph naming the speaker and title, bold "You'll learn:" with 4 "•" bullets, one-line close that fits the series.

Example (Oct 28 2026):
> **How to Win Back Lapsed Members**
> Every association has them: members who didn't renew, didn't say why, and quietly dropped off the list. Most organizations write them off. But a lot of lapsed members never actually decided to leave. Many don't even realize their membership expired.
> Join us for a practical session on turning your lapsed list into one of your best sources of returning members, led by Ryan Graham, Chief Revenue Officer at PropFuel.
> **You'll learn:** • Which lapsed members are most likely to come back, and where to focus first • Why asking a simple question often works better than another renewal pitch • How to build a win-back sequence that feels personal, not pushy • Easy changes your team can start making the week after the webinar
> If your lapsed members are sitting in a spreadsheet with no plan attached, or past win-back efforts haven't moved the needle, this one's for you.

## 2. PropFuel email (sent through PropFuel's conversation format)
Three blocks, always.
- **Part 1** (short): "First Name," then one or two short paragraphs naming the session (bold title), day, date and ET time, with a warm first-person invite from the sender. A second paragraph starts "Next,".
- **Question**: "Would you like to join us on Wednesday, October 28th at 2 PM ET?" (yes/no). Follow-ups may use a poll with 3 to 4 options.
- **Part 2** (short): one or two sentences on why it matters, "I'll walk through:" plus exactly 3 "•" bullets, one-line close ("Hope to see you on the 28th!").
Sender voice: Ryan sends, "I'll walk through". Brittany with a client co-presenter: "Join me and [client speaker]". Sender unknown: use "we" and say you will switch once confirmed.
Also offer 3 to 5 subject lines (no question marks) plus preview text.

Example (Ryan sending):
> **Part 1:** First Name, / Most associations have a list of lapsed members with no real plan behind it. On Wednesday, October 28th at 2 PM ET, we're hosting **How to Win Back Lapsed Members**, and I'd love for you to join us.
> **Question:** Would you like to join us on Wednesday, October 28th at 2 PM ET?
> **Part 2:** A lot of lapsed members never actually decided to leave. Many don't even know their membership expired. I'll walk through: • Which lapsed members to focus on first • Why a simple question beats another renewal pitch • How to build a win-back sequence that feels personal, not pushy / Hope to see you on the 28th!

## 3. Recording page (Webflow, propfuel.com/videos/<slug>)
Four fields, approved one at a time if asked.
- Slug: lowercase, hyphenated, exactly the locked title.
- Meta description: one sentence, 150 to 160 characters, names the speaker, one hook or number. Offer 2 or 3.
- Short description: one sentence, 180 to 220 characters, names the speaker, frames the core problem, covers the whole session.
- Full description: paragraph 1 the common assumption; paragraph 2 speaker name and title and how the session breaks from the assumption; italic "*During the session, he covers:*" with 4 bullets.
Lock the title with the user before writing these.

## 4. LinkedIn post
Scroll-stopping first line, short, content is the point. No hashtags wall. Link placeholder [registration link] unless given. Draft only, goes to the Q4 Posts calendar via the OS after approval.

## 5. Slack hand-off
Super quick and scannable: one-line header, then bullets (what is ready, where the files are, what needs a decision). No long prose.

## Final check
Run `python3 scripts/lint_copy.py <file>` on every piece of copy before delivering.
