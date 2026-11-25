# Backlinks

Purpose: backlinks are a mechanical signal that points Google at the keywords and pages to prioritize. Relevance and established domains help. Content and links go live together. Once content is live, aim new links at keywords that are stagnating.

## Tracker (Backlink Tracker tab; columns)
Sr No | Month | Anchor 1 | URL 1 | Anchor 2 | URL 2 | Blog Link (placement URL) | Domain | DR | Avg Monthly Traffic | No. of backlinks (2 per placement) | Status (Live / In Progress / Replace) | Live Link | Checked | rel attribute (sponsored / dofollow) | Notes
No pricing column values in this repo or in shared docs. Cost tracking lives in the finance system, not the tracker.

## Vendor criteria
US based and US-publishing; SaaS or tech relevance; high DR/DA; low spam score; real, existing traffic (check it, do not trust the vendor's number); topical fit with associations or B2B software.
Reject: link farms, no traffic, unrelated verticals, sites that publish anything for a fee without editing.

## Placement rules
- 2 anchors per placement, to 2 different money pages.
- Anchor = the target keyword of that page. Article topic = that page's use case.
- Targets: bottom-of-funnel and stagnating keywords. Prospect list and target pages go to Alex for sign-off before outreach.
- Past mapping examples: "member engagement software" to the homepage; "two-way AMS integration" to /integrations; "member retention software" to /use-cases/renewals; "member communication platform" to /platform/overview; "measure member engagement metrics" to /use-cases/data-intelligence; "AI agent for membership automation" to /membership-ai.
- Vary anchors; do not repeat exact-match anchors to the same URL from many sites. Include some branded and URL anchors.

## rel="sponsored"
Paid placements must carry rel="sponsored" (Google policy). Mamba's September and October batches did not disclose whether links were tagged. Before any new paid placement: require the vendor to tag the link or choose a placement that is editorial. Check the live link's HTML (`curl` the page, grep the anchor).
Why: undisclosed paid links are link spam and risk a manual penalty, which would cost more than the links earn.

## Better sources than paid batches
- Associations Now (ASAE's media outlet): most credible source in the space. Not in vendor catalogs; cold outreach gets poor replies. Route through the ASAE partnership conversation (likely paid or reciprocal; the content can be written by us). Owner: Alex raises with ASAE.
- Client and partner pages (AMS partners, integration partners): links from "works with" pages.
- Case-study co-publishing with named clients.
- Review sites for GEO (G2; Gartner-type directories) only where citation data shows LLMs pull from them. Reddit needs a careful subreddit-level approach. Wikipedia needs third-party non-promotional coverage.
- Memberful's trick (client subdomains pushing authority to the root) is not applicable.

## Never
Gray-hat tactics (link trades at scale, PBNs, comment spam, "link drip" tricks from social reels). Nov 13 advice: works short term, risks penalization, do not game the system. Disavow only genuinely toxic links, via a disavow file after the off-page audit.

## Monthly routine
1. Check last month's placements are live and the anchor and URL are right. 2. Pick this month's targets from the Keyword Tracker (Page 2 and stagnating terms). 3. Send the list to Alex. 4. Write the guest article (US spelling, facts allow-list, no unsourced stats). 5. Record in the tracker.
