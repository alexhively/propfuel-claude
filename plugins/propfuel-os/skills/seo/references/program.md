# Program: cadence, roadmap, tracker, weekly check-in

## Cadence
- Weekly (Thursday, async or on a call): status in Alex's format (below).
- Monthly cycle, in order:
  1. Monthly report (references/reporting.md) for the month that just closed.
  2. Keyword snapshot: current positions for the tracked list (GSC when connected; WebSearch spot checks otherwise). Bucket: Top 10 / Page 2 / Page 3+ / Not ranking.
  3. Pick the month's pages: existing pages first, new pages and blogs from the calendar.
  4. Outline, then article, per page (references/page-optimization.md).
  5. Approve: send Alex one link per page and the exact diff.
  6. Publish (references/technical.md ship flow). Alex publishes or approves.
  7. Re-audit live: fetch the raw HTML of every page touched, compare to the approved text, check native fields, schema, one H1.
  8. Backlinks: aim the month's new links at keywords that are stagnating (position flat or falling), 2 anchors per placement (references/backlinks.md).
- Pace Mamba reached: one page every 3 to 4 days when approvals were fast. Approval speed is the bottleneck, not drafting.

## 90-day roadmap shape (reuse for any new quarter)
| Stage | Weeks | Work |
|---|---|---|
| 1 Strategy building | 1-4 | Access (GSC, GA4, GTM, Webflow, GitHub). ICP and baseline. Full audit and Technical Task Tracker. List of simulated LLM outputs ("AI target opportunities"). Competitor analysis. Priority keywords, raw list, clusters, sitemap and metadata plan, 90-day content calendar. Report dashboards. |
| 2 Site optimization | 3-8 | All audit fixes. All on-page items (metadata, H1, headings, FAQs). Interlink pages. |
| 3 Site expansion | 6-15 | Publish new content steadily. Backlink strategy and execution. Blogs from templates. |
| 4 Reporting | 1-15 | Deliverable tracker, monthly report, keyword and page performance reports. |

## Deliverable tracker (columns: SEO Component | Goal Target | Timeline | Progress % | Status)
Month 1: competitor analysis, full site audit, raw keyword list, keyword cluster, content calendar, technical and on-page optimizations.
Month 2: 4 on-page pages, 4 weekly status updates, monthly website and keyword report.
Month 3: 6 on-page pages, backlinks, 4 weekly updates, monthly report.
Rule: progress is computed from the calendar and live checks, never typed by hand (the Mamba dashboard went stale: placeholder grades, "Not Yet Assigned" on shipped pages, #REF! cells).

## Content calendar
Columns: Target Month | Category | Cluster | Page Title | Search Intent | Page Type (Existing Landing Page / New Landing Page / New Blog Content) | Content Draft (doc name) | Timeline | Content Status | Keyword Type (Primary/Secondary) | Keywords | Search Volume | Live Link | Date of Publish | Rechecked Status.
Status ladder (numbered):
1. Not started
2. Outline In Progress
3. Outline Complete
4. Article In Progress
5. Content In Progress
6. Ready For Final Review
7. Approved
8. Ready To Publish
9. Published
(Mamba's sheet showed 2, 3, 5, 6 and 9; 1, 4, 7, 8 are the in-between steps added here so every handoff has a number.)
Notes rule: anchor text in old pages must be noticeable; the bottom CTA is duplicated on old pages (one or two CTAs).

## Weekly check-in format (post in Slack or the OS; short lines)
```
SEO status, week of <date>
Technical: <done / in progress / blocked>, one line each
Content: <pages published, in review, next up>, with links
Backlinks: <live, pending>, anchors and target pages
Rankings: <top-10 count, biggest movers up and down>; say monthly or 3-month average
GEO: <prompts tracked, visibility, new citations>
Asks for Alex:
1. <approve this diff / review this doc / decide X>, link, suggested answer
Next steps:
- <task>, owner, date (business day, weekday checked)
```
Rules: status first, asks second, dates last. Every ask carries a link and a recommended answer. Never invent due dates; propose one and flag weekends.

## What Alex asked of Mamba (keep doing all of it)
- Explain why for every change ("tell me why you made these changes because I want to learn").
- Give exact prompts and steps so he can repeat the process himself.
- Benchmarks and progress data: ranking, traffic, where it comes from, direct and organic bumps, competitor visibility.
- A status per workstream, out loud, every week.
- Growth ideas: what are we missing, where is the upside, what to test. Mamba's list: GEO, tangential keywords (CRM-adjacent), internal linking, author pages, faster content.
