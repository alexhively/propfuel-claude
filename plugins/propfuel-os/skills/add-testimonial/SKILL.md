---
name: add-testimonial
description: Add a client testimonial to the PropFuel testimonial database. Use when someone says "add this to the testimonial database", "add this testimonial", "log this testimonial", "save this client quote", or pastes/attaches a client quote (text, email, screenshot, G2 or LinkedIn post, call clip or video link) and wants it captured. Creates the Notion Testimonial Library row with "Testifies to" tags, posts to #testimonial-drafts and queues a hidden Famewall add. Never publishes anything.
---

# Add a testimonial to the database

One call to the Marketing OS `submit_testimonial` tool does all of it: Notion row (searchable "Testifies to" tags), a quote card in Slack #testimonial-drafts saying who added what, and a to-do for the Famewall owner to add it **hidden**. Nothing goes live: only a testimonial the client approved, and Alex or Brittany marked approved, is usable.

## Steps
1. Get the content from what the teammate gave you. Screenshot or file: read it. Video or call link: put the link in `links` (Gong with mm:ss) and quote only words you can read or hear.
2. Pull out `org` (full name), `person`, `role`, `date` (YYYY-MM-DD, default today), `source` (email, call, G2, LinkedIn, screenshot...). If the org is missing, ask once. Don't guess names.
3. `quote` must be the client's words copied exactly. A paraphrase goes in as given with the source noted, never in quotation marks you made up.
4. Pick 1 to 4 `tags` from this list, only for what the client actually says (a vague "you guys are the best" is General praise / advocacy, not Customer support):
   Win-back / lapsed members, Renewals / retention, New member onboarding, Engagement / response rates, Member insights / data, Revenue / ROI, Time savings / efficiency, Ease of use / setup, Customer support / CSM, AMS integration, Membership AI, Events / conferences, Certifications, Acquisition / recruitment, Personalization / member experience, vs. previous tools, General praise / advocacy.
5. Call `submit_testimonial` (org, quote, person, role, tags, date, source, links). Leave `consent` as `not-asked` unless the teammate says the client already agreed; the database still records consent as "not requested" until the client's own reply is logged.
6. Tell the teammate in two lines: the Notion row link, and that the Famewall add is queued as hidden for the owner.

## Rules
- Never use a MemberCentral comparison quote, and never mark anything approved or public yourself.
- Never put client contact emails or phone numbers in the quote, notes or anywhere in the call.
- Adding the same quote again updates the row instead of duplicating it.
- If the response has `library.error`, the Slack card still posted; tell the teammate and ask Alex's Head of Ops session to retry the Notion row.

## Changelog
- 2026-10-28: created. Famewall has no write API, so the add is a to-do for now.
