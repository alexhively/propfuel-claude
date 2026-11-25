# Monthly SEO + GEO report

Build it as the "SEO and GEO report" workbook, one tab per section. Compute everything from GSC, GA4, PostHog and HubSpot AEO data; never leave placeholders. Without GSC access, build from the last snapshot, label every number with its as-of date and put "GSC access needed" at the top.

## Tabs
1. Summary: 5 bullets (what moved, what to double down on, what is stuck, GEO headline, the one ask).
2. Technical SEO (before/after): metric | before | now. From the audit crawl (titles, metas, canonicals, duplicates, 4xx, schema coverage, orphans, indexable pages, thin pages, slow pages).
3. KPI Scorecard: the 12 metrics below, previous month, current month, MoM %, growth to date, starting metric.
4. Keyword Tracker: Keyword | Target page | Vol | KD | Position now | Position last month | Change | Bucket (Top 10 / Page 2 / Page 3+ / Not ranking yet). Highlight position changes (Alex's ask).
5. Priority Pages: per optimized or new page: impressions by month, non-brand impressions, clicks, average position, publish date.
6. AI Search: Google AI Overview / AI Mode impressions; HubSpot AEO visibility and citations per prompt cluster; AI referrals (PostHog); branded prompt fact-check notes.
7. Work and Next Month: shipped (with links), in review, next month's pages, backlink placements, asks for Alex.
Plus raw tabs: GSC monthly, keyword YoY.
Report on: clicks and performance per page; keyword positions and clicks per keyword; pages that improved or worsened most; trends; October vs September style comparison; GEO section.

## The 12 metrics (stage | metric | source)
Awareness: Total Impressions (GSC); Unbranded Impressions (GSC); Branded Impressions (GSC); Avg Keyword Position (GSC); # Keywords Ranked (volume tool or GSC query count); # Keywords in Top 10.
Consideration: Total Clicks (GSC); Unbranded Clicks (GSC); Branded Clicks (GSC); Avg CTR (GSC; Mamba used GA4).
SEO hygiene: Domain Rating (volume/DR tool); Total Backlinks (same); # Indexed Pages (GSC).
Add when GA4 conversions exist: organic sessions and organic demo bookings (not tracked today).
Branded query regex: `propfuel|prop fuel`. Unbranded = everything else.

## Reading average position
- New pages enter at low positions (50 to 100) and temporarily raise the average. Filter by page or keyword; do not read the site-wide average.
- Always say whether a number is a monthly value or a 3-month average. The "8 vs 5" lesson: the report said 8 keywords in the top 10 (an Aug-Oct average) while the filtered monthly sheet showed 5.
- Report non-brand average position separately from total.
- Use top-10 count and per-keyword movement as the headline, with the filter shown.
- Semantic variants (member engagement solutions) can lag the head term; judge after a month of added content and internal links.

## October 2026 baseline (last data on file; GSC)
- Total clicks: May 755, Jun 809, Jul 854, Aug 603, Sep 563, Oct 611.
- Branded clicks: 558, 601, 634, 349, 284, 380. Unbranded clicks: 197, 208, 220, 254, 279, 231.
- Non-brand impressions: 1,668; 2,855; 2,771; 2,949; 2,228; 2,698. Non-brand average position: 18.6, 22.4, 24.0, 23.9, 20.4, 20.7.
- Tracked keywords in top 10: Aug 3, Sep 7, Oct 5. Year over year (Aug to Oct): tracked keywords showing in Google 13 to 25; top 10 from 0 to 8 (an average); 6 keywords up 10+ positions.
- Keyword tracker Oct: member engagement software 4.8, member engagement platform 6.0 (Top 10); member onboarding 13.8, association member onboarding 14.5, lapsed members 10.8 (Page 2); automate membership renewals 46.5, membership acquisition 20.8 (Page 3+); others not ranking yet. Membership renewal AI agent had the biggest jump.
- AI Overviews / AI Mode impressions: Jul 1,065; Aug 1,183; Sep 1,382; Oct 4,991 (US 868, 903, 1,134, 1,672).
- Technical (before to now): Google-ready titles 22 to 212; missing meta descriptions 126 to 0; pages with schema 0 to 213; duplicate titles 126 to 8; 4xx 25 to 0; missing canonicals 148 to 0; indexable 148 to 209; too-short titles 339 to 1; duplicate H1s 367 to 8; thin pages 334 to 11; orphan pages 43 open; slow pages (>2s) 10 to 7.
- Earlier baseline (pre-engagement): 498 organic visits a month, 92 ranking keywords, 14 in the top 10, branded share about 96%.
Scope of progress to report: branded traffic fell, unbranded rose; total organic did not grow in the first quarter. Targets set at the start: +350 organic visits a month, +125 ranking keywords, DR 33 in 6 months.
Organic demo bookings: not tracked (needs GA4 conversion tracking).
