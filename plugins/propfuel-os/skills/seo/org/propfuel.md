# Org profile: PropFuel

Loaded by SKILL.md step 0. Everything PropFuel-specific lives here. Program state (workbook and doc links, open items, live numbers) lives in OS knowledge `seo-program.md`, not in this repo.

## Identity
- Org: PropFuel. Site: https://www.propfuel.com (US English). Staging: *.webflow.io (must never be indexed or canonical).
- Approver: Alex, or a teammate he names. Nothing ships until the named approver approves the exact diff. Drafts (outlines, articles, metadata sheets, reports) go out end to end without asking.
- The Mamba SEO agency engagement CONTINUES (weekly call, workbook, per-page docs, backlink batches, monthly report). This skill captures their method so Claude can run and check the same program. It is not a plan to end the engagement. Claude's job: do the work, audit the agency's output against these rules, and flag drift.

## Marketing OS hooks
Start of every run: `get_briefing`, then `get_knowledge seo-program.md`.
End of every run: `log_update` with initiative `mamba-seo` (one line per outcome); `update_knowledge` on `seo-program.md`, mode "replace", only what changed (done, live, open items, numbers); say what needs Alex's approval with the exact diff or link.
Known live-site gaps (open fixes, tracker status) are listed in `seo-program.md`; read it before auditing so you do not re-report fixed items.

## Audience and keyword qualifier
- ICP: associations (professional about 75% of clients, trade, individual). The word "association" is the qualifier. Formula: use case + "for associations".
- Why: "member ___" alone also pulls YMCAs, yacht clubs, Boys and Girls Clubs.
- In: member acquisition, retention, onboarding, engagement, experience, renewals, events; integration queries ("member engagement platform that integrates with <AMS>").
- Excluded classes: AMS terms (association management software and its brands: the AMS is the CRM, PropFuel is not one, wrong intent, hardest fight); LMS; advocacy software; "membership benefits"; generic marketing tools (SMS marketing software, personalized email marketing). Exceptions: one "best AMS" post with integration messaging (50+ AMS integrations, about 90% of the market); AMS integration queries.
- Rule: keep the association variant as focus keyword wherever one exists, even at 10 searches a month. Staff often drop the word, so keep the broad "member ..." variant as secondary or on the homepage.
- Member vs association classification (Feb list, 128 keywords, 10,050 volume): MEMBER variants (contains member/membership, not association) 80 keywords, 6,230; ASSOCIATION variants 47, 3,760; OTHER (e.g. "best ams software"). Association variants have higher KD and CPC and need page clusters.
- Easy-win examples (vol/KD): member engagement 400/4, member experience 300/0, member retention 300/2, member engagement strategy 200/2, membership marketing 200/2, member engagement platform 200/2, membership retention ideas 150/0, member survey 150/1, how to attract new members to an association 100/0, new member onboarding 100/0. Funnel averages (Feb list): TOF 73 keywords avg vol 79; MOF 29 avg 78; BOF 21 avg 75.
- Tiny-volume association terms stay for topical and GEO relevance (e.g. "student membership benefits", about 10/mo). Strategy: many low-KD association terms, not a few head terms (most targets are under 100/mo, KD under 10).

### Triage examples (Aug 27 and Sep 3 reviews)
| Color | Examples |
|---|---|
| Green keep | how to increase member engagement; new member onboarding; member retention strategies |
| Yellow | membership marketing; member survey (generic but PropFuel can serve it) |
| Red remove | membership marketing agency; membership marketing ideas; marketing strategy; what is association management software; associate member management software; advocacy software; LMS for member engagement |
| Exception | member engagement platform that integrates with <AMS> |

## Facts allow-list and banned claims
Allowed only:
- 370+ associations (always "370+"; end cards may add "and counting").
- Tagline "Know and Grow Your Membership" (front-facing). "Make Membership Meaningful" is the big-picture umbrella job only.
- "12% average annual revenue growth after implementing PropFuel", always next to "vs 0.98% for the average association".
- Client results only from the Help Center or the Case Studies master, labeled as one client's result, never an average ("individual client results, not averages").
- Unknown number: write `{{number}}` and flag it.
Banned: AAMFT 12%, AAP 80%, 8.68%. Also banned: hourly sync, guaranteed real-time write-back, "5-30 minutes" AMS setup, "plug-and-play", "connected in minutes", "No IT project", any PropFuel API claim, unsourced stats, "See One Question in 87 Seconds". Write-back only "where your AMS supports it". Do not quote prices (sales and leadership call; explain structure only). Skipped-claim precedents: "No credit card required" (B2B demo), "15-minute demo" (discovery call is 45 minutes), "See it working with your AMS data" (cannot confirm), official G2 badge (must be earned; use a "Verified reviews on G2" link).
Sources: Marketing OS Master docs (`get_knowledge`), Help Center, Case Studies master. Live numbers come from OS tools; say live or snapshot with as-of time.

## Brand, spelling, style
- US spelling ("organization"). No em dashes. Start sentences with a subject so AI engines can quote them.
- H1 rule: keyword phrase in the H1 (Oct 8). Homepage H1 "Member Engagement Platform for Associations" with the tagline as eyebrow. /platform/overview keeps "Know and Grow Your Membership" as H1 (keyword carried by title, meta, hero sub).
- Hero CTA "Get a Free Demo"; secondary CTA scrolls to the page's centerpiece by id. Bottom CTA duplicated on old pages. All demo links go to /book-a-demo.
- Blog CTA: "See how 370+ associations use PropFuel to Know and Grow Your Membership. Book a demo."
- Orphan-word gate: no single word alone on the last line (text-wrap balance on headings and buttons, pretty on body, nbsp ties).
- Brand guide first for visuals (brand-style-guide-v5.2 + brand-qa-prompt).

## Stack and how changes ship
- Webflow site + custom-code repo `alexhively/propfuel-webflow-custom` (GitHub Pages scripts, QA hooks). Local build source for generated pages: `~/Projects/propfuel-page-previews/src/mamba-system`.
- Enhancement script `js/webflow-enhancements.js` adds behavior only. Mamba's Sep 11 and Oct 7 commits removed all SEO injection from it; do not reintroduce. Every script injector checks for the static node first (two sources of truth drift). Stays in JS: carousels, tabs, accordions, scroll animations, nav, tracking, text-wrap CSS, the claims safety net (`js/copy-fixes.js`).
- Tooling: Webflow MCP `data_pages_tool` (page SEO), `data_cms_tool`, `data_scripts_tool`, `data_element_tool`, `data_whtml_builder`. OG image: Designer only. `llms.txt` source: `agent/llms.txt` in the custom-code repo, re-upload to Site settings when it changes. Agent readiness: `node qa/agent-readiness.mjs https://www.propfuel.com` (16 checks).
- Markdown alternates: `propfuel-edge.vercel.app/<page>.md` mirrors (noindex host, canonical Link header to www). The `<link rel="alternate" type="text/markdown">` is currently JS-injected: move into native head code.
- Redirects: /demo and /request-demo are Webflow 301s to /book-a-demo (single hop). Webflow 301s drop query strings (UTMs lost): repoint live ads and emails to /book-a-demo directly; test `curl -sI "https://www.propfuel.com/demo?utm_source=x"`. /solutions/associations 301s to /client-success/customers (lossy). Native CTAs still pointing at /demo cost an extra hop.
- robots.txt: `User-agent: *`, `Allow: /`, one `Sitemap: https://www.propfuel.com/sitemap.xml` line (live file repeats it twice: dedupe). AI bots stay allowed. Sitemap had 212 URLs on Nov 25; review /book-a-demo-15min and landing-page variants.
- llms.txt (llmstxt.org format): H1, summary, "When to use PropFuel" (with not-the-right-fit list), "How an agent should engage" (send to /book-a-demo, no public API, do not quote prices, 2-3 week typical timeline), Product, Use cases, Proof, Company, Optional. Current file is stale ("330+ associations", "5-30 minutes"): fix both.
- Nav placement: new audience pages sit under the Use Cases dropdown, above the direct product use cases, as 2 mini cards (like Membership AI above Solutions and Tools); the Solutions row is a featured full-width item. Ship nav items hidden until HEAD requests to all new paths return 200 (`?pfsol=1` forces preview).
- Homepage blog cards: set links natively to "Current Blog Post" in the Designer (the API cannot) so hrefs are real.

### Ship flow
1. Branch per page group in `alexhively/propfuel-webflow-custom`. JS first (backward compatible), then Webflow edits, then publish.
2. PR body: what changed, QA checks, what is staged separately in Webflow.
3. Show Alex the exact diff and before/after table. Alex approves that exact diff. Send one link per page in Slack to approve and publish.
4. Merge to main, `git push origin` (GitHub = what is live; about 1-2 min deploy, about 10 min browser cache; bump `?v=` on copy-fixes.js when its table changes). Pushing to main is live on prod and staging. Before the push: PII and secrets scan, `node --check` on edited JS, QA hook `qa/hooks/pre-push` (runs `qa/run-qa.mjs`). Never `--no-verify`.
5. Webflow publish (Alex, or Claude after approval). Re-check native title, meta, canonical on pages touched (a full-site publish once reverted the homepage meta title).
6. Verify live; write the change log.

### Undo
JS: revert the merge commit (GitHub Pages updates in about a minute). Webflow: Designer, Backups, take a backup before publish and note its timestamp, restore if needed. HTML Embed: delete it and the script re-injects its fallback (only where the fallback still exists). Redirect: remove the 301 rule.

### QA gates (all pages)
Served HTML: new title, meta, canonical, OG, exactly one H1, expected H2 order, JSON-LD parses with one FAQPage, no placeholder text. Internal links 200. Claims check against the allow-list above. Orphan-word gate. Screenshots at 1440 and 390 px: no horizontal scroll, no JS errors, accordions and carousels work; read them before showing Alex.

### Commit history (precedent)
Mamba authored PR #1, #2 and the Oct 7 commit; the rest is Alex + Claude implementing Mamba outlines.
- 2026-09-11 PR #1: removed client-side title, meta, canonical, OG and Organization/WebPage JSON-LD; rebuilt natively; CMS templates bound; 301s for /request-demo. Why: crawlers saw `<title>PropFuel V2</title>` and no description or canonical on every CMS page.
- 2026-09-11 PR #2: removed the JS /demo redirect.
- 2026-10-07 (direct to main): removed client-side FAQ schema; FAQPage now native.
- 2026-10-08 PR #21: native homepage engine rows and static testimonial grid; PR #26/#40 agent readiness (llms.txt, markdown alternates, 16 checks).
- 2026-10-19/20 PRs #46-#49, #54: claims and orphan-word safety net, one H1 per page, MGI 2026 citation in the renewals FAQ.
- 2026-09-24 PRs #4-#7: homepage, platform, onboarding, renewals static-first.
- 2026-10-26 PRs #64/#65: Solutions hub and use-case revamps.

## Webflow and PropFuel specific audit checks (all found on this site)
- Canonical pointing at staging (.webflow.io): fixed May 13. Re-check after template edits.
- Staging indexed despite the Webflow setting (the ROI page showed in a site: search). Staging must stay live for testing: noindex signals and canonical to prod.
- Customer-built landing pages hosted by PropFuel (e.g. survey pages) indexed as PropFuel content: noindex, request removal in GSC.
- 328 auto-generated customer logo pages and 14 internal/event pages: noindex.
- app.propfuel.com and app.propfuel.com/to/... tracking links appear as ranking pages: noindex question open.
- Paid and conference landing pages (/cats-ask, /ig, Google Search LPs, /downloads/*): explicit index or noindex decision.
- UTM canonicalization: ?utm_source=... URLs canonicalize to the clean page.
- Famewall review widget injected a fake 5.0 Product/aggregateRating on every page (policy violation). Turn off review-rating schema; confirm status.
- Placeholder CEO quote ("Sarah Chen, co-founder and CEO") hidden on all 17 team pages: remove.
- Duplicate "PropFuel V2" titles on 126 CMS pages (fixed Sep 11 with CMS bindings): re-check new CMS collections.
- JS-only schema (Organization, WebPage, FAQPage by script): fixed Sep 11 and Oct 7. Re-check any new page.
- Placeholder text and fake testimonial quotes in raw HTML that JS overwrote ("This is some text inside of a div block", "Sarah Mitchell, VP of Membership, AAP"): grep raw HTML.
- Orphan pages: 43 open as of the October report.
- Homepage blog cards render href="#" in raw HTML.
- Product schema on about 149 pages where it does not belong.
- Duplicate H2s across /platform/engagement and /platform/insights (leftover skeleton).
- /book-a-demo has no H1 in raw HTML.
- Title flag string for crawl_check output: "PropFuel V2". Known schema gaps: /solutions lacks BreadcrumbList; /membership-ai lacks FAQPage; Famewall markup must stay off.
- hreflang: N/A (US English). Local GMB items: N/A.

## Competitors
Benchmark set: MemberNova, Higher Logic Thrive, Feathr, Tradewing. Memberful was benchmarked by the agency but is a creator-paywall tool: poor comparison (useful only for the per-integration page and subdomain-authority ideas). Ugenie has negligible SEO. Generic terms owned by big vendors (NPS survey questions: Qualtrics, SurveyMonkey) are won on the association angle ("member NPS").

## Keyword-to-page map (baseline positions from Aug 2026; vol / KD)
Rule: one head term per page. "member engagement" belongs to /platform/engagement; "member engagement platform" to the homepage. The full 128-keyword list lives in the SEO Program workbook (link in `seo-program.md`).
| Page | Primary | Secondary |
|---|---|---|
| Homepage | member engagement software 200/48; member engagement platform 200/2; member engagement solution(s) 150 each; member engagement platforms 40 (pos 12) | tools 20; app 20 |
| /platform/overview | member communication solutions 60; member communication 50; online member engagement platform 30 | multichannel member communication 30; member communication software 10 |
| /use-cases/onboarding | new member onboarding 100/0; member onboarding 70/0; association member onboarding 20; association new member onboarding 10 | member onboarding process 70; new member onboarding checklist 40 |
| /use-cases/renewals | member retention 300/2; membership retention 150; member retention software 10; automate membership renewals 30 (pos 56); member renewals 5 | member and membership retention strategies 150 each; membership retention strategy 70 |
| /use-cases/win-back | reengagement emails 100; reengagement campaign 40 | lapsed members (blog angle) |
| /use-cases/acquisition | membership acquisition 90; association member acquisition 60 (pos 20) | |
| /use-cases/events | member events 30 | association event strategy 30 |
| /use-cases/certifications | none usable | membership certification terms |
| /use-cases/data-intelligence | member engagement metrics 20; member engagement reporting 20 | how to measure member engagement 20 |
| /use-cases/feedback (not built) | member survey 150; member satisfaction survey 70; member feedback tools 50 | member interest survey 30; member exit survey 20 |
| /membership-ai | membership automation 30; membership renewal ai agent 60 (pos 15) | |
| /platform/insights | membership database 150; association membership database 30 | |
| /platform/automation | membership renewal automation 50 (pos 28) | |
| /platform/engagement | member engagement 400 (pos 57); membership engagement 100; association engagement platform 80 | |
| /platform/email | personalized member communication 20 | |
| /platform/website | association membership portal 30; custom association member portal 30; member engagement website solutions 20 | best membership association websites 50; portal development 40; website design 30 |
| /platform/sms | member benefits communication 10 | |
| /integrations | ams software 400/37; ams integration 80 (pos 5); ams crm software 100; association membership system 40 | best ams software 60 |
| /solutions | association membership 200/10; association member management 40; association membership management tools 30 | association strategy 100; association growth 40 |
| /solutions/trade-associations | trade association member engagement 30 | |
| /solutions/professional-associations | professional association membership 50 | |
Blogs (retarget existing posts): member-engagement-ideas (member engagement ideas 150; improving member engagement 150; how to increase member engagement 100); member-retention-ideas (membership retention ideas 150; member retention ideas 80; best practices 80); member-engagement-strategies (member engagement strategy 200; strategies 150); membership-marketing-guide (membership marketing 200; association membership marketing 100); member-experience-vs-member-engagement (member experience 300; improve member experience 100); member-retention-how-to-calculate (what is member retention 70; how to calculate membership retention rate 70); strategies-for-optimizing-new-member-acquisition (how to attract new members to an association 100; association membership recruitment 50; how to grow association membership 40).

## Data sources as connected
- Webflow MCP (pages, SEO fields, CMS, sitemap, publish) and the custom-code repo (above).
- Google Search Console: property `sc-domain:propfuel.com`, connected 2026-11-25. `python3 -I scripts/gsc.py query --site sc-domain:propfuel.com --start YYYY-MM-DD --end YYYY-MM-DD --dims query,page > out.csv`. Token in the config dir (`~/.config/propfuel/gsc.json` on Alex's Mac; re-run `gsc.py auth` if it expires). Data lags about 2 days. Branded regex `propfuel|prop fuel`. Also exclude team-member and celebrity-name queries (, , , ) from unbranded and report them as a "people" bucket: in Oct 27 to Nov 23 they were most of the unbranded clicks.
- HubSpot AEO: `get_aeo_metrics`, `manage_aeo_prompts`, `manage_aeo_recommendations`. 25 free prompt slots; loaded with the 25 prompts below (baseline date recorded in `seo-program.md`). Webflow AEO (`data_aeo_tool`) is not entitled on this plan: do not rely on it.
- Keyword volumes: Keyword Planner in the Google Ads web UI via Claude in Chrome (new tab, never Alex's open tabs): Tools > Keyword Planner > "Get search volume and forecasts", paste up to about 50 keywords, US, English, download "Historical metrics" CSV, read avg monthly searches, competition, top-of-page bid. Why: Google Ads API Basic access was denied twice (2026-11-25) because the OAuth app is Internal and cannot be brand-verified. Do not switch it to External (breaks OS sign-in). No paid SEO tool by Alex's choice. `scripts/kp.py` stays for if API access is ever granted. Difficulty is always a SERP judgment.
- PostHog "SEO & AEO" dashboard and AI-assistant referrals (project in the PostHog reference note).
- Live HTML fetch (`scripts/crawl_check.py`, curl) and WebSearch for SERP, competitor and LLM checks.
- Not connected: GA4 conversions (no organic demo bookings; report stops at clicks and AI referrals; ask: finish GA4 and GTM plus demo-booking conversion tracking, open since Sep).
- Credentials: `~/.config/propfuel/` (gsc.json, google-ads.env, google-ads-adc.json). `scripts/*.py` fall back to this dir when `~/.config/seo` is absent.

## Tracked AI prompts (33 approved Nov 23; location US; volume = summed keyword volume)
Prompts are written as buyer questions with "associations" in them.
Cluster 1 Member Engagement Platform
1 (KEY, 1,020) What is the best member engagement software for associations?
2 (300) Which member engagement solutions work best for a small association with a small staff?
3 (610) What tools can help an association increase member engagement?
4 (490) What software do associations use to run their member engagement strategy?
5 (110) What are the best member engagement platforms for trade associations?
6 (430) What platforms help associations improve the member experience?
7 (60) What are the best member engagement apps for membership organizations?
Cluster 2 Member Retention + Renewals
8 (KEY, 580) What is the best member retention software for associations?
9 (800) What tools help associations improve membership retention?
10 (85) What is the best software to automate membership renewals for an association?
11 (90) Which AI tools can automate membership renewal outreach for associations?
12 (140) What are the best tools for associations to win back lapsed members?
13 (70) Which platforms help associations with both member engagement and retention?
Cluster 3 Member Acquisition + Onboarding
14 (KEY, 200) What is the best new member onboarding software for associations?
15 (110) What tools help associations automate the new member onboarding process?
16 (150) What are the best membership acquisition tools for associations?
17 (880) What software helps associations recruit and attract new members?
Cluster 4 Member Communication
18 (120) What is the best member communication software for associations?
19 (60) Which platforms let associations send personalized email and SMS messages to members?
Cluster 5 Member Feedback + Data
20 (330) What are the best member survey and feedback tools for associations?
21 (60) What tools help associations measure and report on member engagement?
22 (180) What tools help associations keep member profile data up to date?
Cluster 6 AMS Integration
23 (KEY, 180) What are the best member engagement tools for associations that already use an AMS?
24 (170) What tools do associations use alongside their AMS for member communication and engagement?
25 (460) AMS vs member engagement platform: what is the difference and which does my association need?
26 (90) Which member engagement platforms integrate with iMIS or a Salesforce-based AMS?
Cluster 7 Events + Programs
27 (90) What are the best tools to increase association event registration and attendance?
28 (20) What platforms help associations promote certifications and continuing education to members?
Branded (check facts and sentiment)
B1 What is PropFuel and how does it help associations?
B2 Is PropFuel a good member engagement platform for a small association?
B3 How much does PropFuel cost? (AI answers on price are often wrong; flags what to fix)
B4 PropFuel vs Higher Logic: which is better for association member engagement?
B5 Which association management systems does PropFuel integrate with?
Sheet columns: # | Prompt | Cluster 1 | Cluster 2 (Key Prompt flag) | Location | Keywords behind it | Searches / month | Why we track it | Approval | PropFuel notes.

### Which 25 are in HubSpot AEO
Load order: Key Prompts #1, #8, #14, #23 plus B1; remaining branded B2 to B5; then highest-volume non-branded by value.
The 25: 1, 8, 14, 23, B1, B2, B3, B4, B5, 9, 17, 3, 4, 6, 20, 25, 2, 5, 12, 10, 11, 22, 24, 27, 15.
Left out (8): 7, 13, 16, 18, 19, 21, 26, 28. Track those by manual WebSearch runs monthly.
Priority prompt themes from Alex (Oct 29): member engagement strategy (professional-association persona) and email campaign templates and outlines.
Competitor visibility: run the same prompts and check which of MemberNova, Higher Logic Thrive, Feathr, Tradewing get cited; Alex finds "which competitors get shown today" valuable.
AI Overviews / AI Mode impressions from GSC: Jul 1,065; Aug 1,183; Sep 1,382; Oct 4,991 (mostly a brand spike after Oct 12). US: 868, 903, 1,134, 1,672.
Off-page GEO targets: G2 and review sites where data shows citations, Associations Now / ASAE, partner and integration pages.

## Backlinks (PropFuel)
- Mapping examples: "member engagement software" to the homepage; "two-way AMS integration" to /integrations; "member retention software" to /use-cases/renewals; "member communication platform" to /platform/overview; "measure member engagement metrics" to /use-cases/data-intelligence; "AI agent for membership automation" to /membership-ai.
- The agency's September and October paid batches did not disclose whether links were tagged rel="sponsored". Check live link HTML before any new placement.
- Associations Now (ASAE's media outlet): most credible source in the space, not in vendor catalogs; cold outreach gets poor replies. Route through the ASAE partnership conversation (likely paid or reciprocal; we can write the content). Owner: Alex raises with ASAE.
- Other sources: client and partner (AMS and integration partner) "works with" pages; case-study co-publishing with named clients; G2 and Gartner-type directories only where citation data shows LLMs pull from them; Reddit via careful subreddit-level approach; Wikipedia needs third-party non-promotional coverage. Memberful's trick (client subdomains pushing authority to the root) does not apply.
- No pricing values in this repo or shared docs; costs live in finance.

## Program, cadence, reporting (PropFuel)
- Weekly status Thursday (async or call), in Alex's format (references/program.md).
- Pace reached: one page every 3 to 4 days when approvals were fast. Approval speed is the bottleneck.
- What Alex asked of the agency (keep doing all of it): explain why for every change ("tell me why you made these changes because I want to learn"); exact prompts and steps so he can repeat it; benchmarks and progress data (ranking, traffic, sources, competitor visibility); a status per workstream weekly; growth ideas (GEO, tangential CRM-adjacent keywords, internal linking, author pages, faster content). Wants links in chat, not a doc to hunt for.
- Source docs per page, the workbook, report, Schema audit and Content Fix List: links in `seo-program.md`.
- Page doc naming: "<Page> - Outline & Article - PropFuel".

### Oct 2026 baseline (last data on file; GSC)
- Total clicks: May 755, Jun 809, Jul 854, Aug 603, Sep 563, Oct 611.
- Branded clicks: 558, 601, 634, 349, 284, 380. Unbranded clicks: 197, 208, 220, 254, 279, 231.
- Non-brand impressions: 1,668; 2,855; 2,771; 2,949; 2,228; 2,698. Non-brand average position: 18.6, 22.4, 24.0, 23.9, 20.4, 20.7.
- Tracked keywords in top 10: Aug 3, Sep 7, Oct 5. YoY (Aug to Oct): tracked keywords showing in Google 13 to 25; top 10 from 0 to 8 (an average); 6 keywords up 10+ positions.
- Keyword tracker Oct: member engagement software 4.8, member engagement platform 6.0 (Top 10); member onboarding 13.8, association member onboarding 14.5, lapsed members 10.8 (Page 2); automate membership renewals 46.5, membership acquisition 20.8 (Page 3+); others not ranking yet. Membership renewal AI agent had the biggest jump.
- Technical (before to now): Google-ready titles 22 to 212; missing meta descriptions 126 to 0; pages with schema 0 to 213; duplicate titles 126 to 8; 4xx 25 to 0; missing canonicals 148 to 0; indexable 148 to 209; too-short titles 339 to 1; duplicate H1s 367 to 8; thin pages 334 to 11; orphan pages 43 open; slow pages (>2s) 10 to 7.
- Pre-engagement baseline: 498 organic visits a month, 92 ranking keywords, 14 in top 10, branded share about 96%. Targets: +350 organic visits a month, +125 ranking keywords, DR 33 in 6 months.
- Progress read: branded traffic fell, unbranded rose; total organic did not grow in the first quarter. Organic demo bookings not tracked.

## Content: triage, kit, calendar (PropFuel)
- Blogs because landing pages alone did not move keywords (Nov 12). Alex approved all current briefs ("move forward and write them"). Low-volume relevant posts stay for topical relevance and AI coverage.
- Triage sheet header: "Content/SEO Strategy for PropFuel Templates: which posts to write, in order". Source: the Use-Case Blog Kit (22 briefs).
- Current triage (Nov 5). Write now (all approved): 1 sponsor and corporate partner outreach ("how to get sponsors for an event" 590, KD 6; links /use-cases/events; angle: four-question qualifier sequence plus email templates); 2 event and conference registration ("event reminder email" 140); 3 event attendee engagement and post-event feedback ("post event survey questions" 260, KD 11); 4 member acquisition and recruitment ("membership drive" 260, SERP strong; links /use-cases/acquisition); 5 membership renewal campaign ("membership renewal letter template" 70; links renewals); 6 lapsed and dormant win-back, merged ("lapsed members"); 7 new member onboarding ("new member orientation" 210). Write next: volunteer recruitment ("how to recruit volunteers" 110); advocacy campaign (210, KD 6); call for abstracts and speakers ("call for speakers" 880; 2,868 AI searches = strong GEO value); NPS and member feedback ("nps survey questions" 260). Merge: year 2+ engagement into the engagement-ideas blog. GEO or support only: SMS opt-in (weak SERP), website pop-up survey, member profile updates, certification campaigns (mismatch), student engagement (mismatch), CPA society series, 4 docs (mismatch).
- Dec calendar: sponsors, event reminder email, post-event survey questions, membership drive (outline stage), plus two GEO slots. Next slots: renewal letter template, lapsed members, new member orientation.
- Do not target terms a landing page owns ("membership acquisition", "association membership"). Consumer-intent head terms (gym, fitness membership) only at section level.
- Use-Case Blog Kit brief shape: one doc per campaign use case: one line; who it is for, when to run, when not to; how it works (short series of one-question check-ins, the answer decides what they see next); the questions, answers and why each works; follow-up flow per answer; results (Help Center only, labeled "individual client results, not averages"); SEO and GEO brief (questions this answers including "Build me a <campaign> and write the emails", suggested title and H2s, FAQ ideas, copy-and-paste question list, internal links to Help Center guide, use-case page, SMS, /book-a-demo, CTA, sources). Facts line: "Facts to use (and only these)". Example H2 pattern (renewals): Why most renewal emails get ignored; Start 90 days out; The five check-ins; What to do with each answer; Renewing organizational memberships; Add a text or on-site reminder; What to measure; Example results from real associations.
- Goal: be the answer when staff ask ChatGPT or Google to "build me a new member onboarding campaign and write the emails". Blueprints (in-platform campaign templates) are the substance for template and GEO posts; source: Help Center campaign guides category.

## New-page patterns and backlog (PropFuel)
- Generated pages come from `~/Projects/propfuel-page-previews/src/mamba-system` (`build.mjs`, `solutions.mjs`, `usecases.mjs`, `system.css`, `usecase-data.json`): shared `.mm` UI system, CSS-only motion, no new runtime JS. Output: `embed-static.html` (pastes into a native Webflow Code Embed), `og.jpg`, per-page meta JSON with the JSON-LD @graph.
- Solutions hub (/solutions): hero (H1 "Built for associations. Every kind, every size.") > problem (0.98% stat) > core idea (Attract / Engage / Retain, each linking a use case) > strategy (link data-intelligence) > "What PropFuel does, and what your AMS does" (link /integrations) > your audience (two cards) > proof > FAQ (5 Qs) > CTA ("Know and Grow Your Membership."). JSON-LD: WebPage, FAQPage (add BreadcrumbList: missing).
- Trade and Professional pages: breadcrumb hero > problem reframed ("The person who pays the dues isn't the person using the benefits." / "Career value changes. Most member communication doesn't.") > segmentation (trade: roles at a member company; professional: career stages) > two topic sections (trade: advocacy and policy input, trade shows and events; professional: credentials and continuing education, chapters and volunteers) > dark results (NACUBO, TXCPA, ARN from the Help Center) > FAQ (4 Qs) > CTA. Breadcrumb Home > Solutions > page.
- Use-case revamp pattern (7 pages): hero with secondary anchor naming the centerpiece ("See the Two Tracks"); problem H2 as a customer pain sentence; centerpiece process; "Four Engines Working Together to ..." (H3 per engine, linking engine pages); "Built to Work With Your AMS" (win-back, acquisition); proof "Proof That Conversations ..." with 3 to 4 stat cards linking named case studies; FAQ "Questions About ..." 5 to 7 H3s; short imperative CTA H2 ("Bring them back.").
- Page-type FAQ counts: 4 to 6 (5 to 7 on use-case pages).
- Backlog: (1) integration page per AMS (Salesforce, Novi, iMIS, Nimble AMS, Fonteva), target "member engagement platform that integrates with <AMS>"; Alex: "so freaking important" for prospects; model Memberful per-integration pages; cluster ams integration (pos 5). (2) /use-cases/feedback (member survey cluster, about 320 combined; currently a 404 other pages linked to; links repointed to the satisfaction-data blog post). Outline: H1 + hero; problem (annual long surveys fail); satisfaction surveys; interest surveys; exit surveys; feedback-tool checklist; "From answers to action" ("you said, we did"); proof; 6 FAQs; CTA; min 500 words. (3) Best-AMS listicle with the integration angle. (4) Pending agency docs as of Nov 25: Website, SMS, Integrations optimizations; Membership AI, Insight, Automation Engine, Engagement Engine, Email pages ready for review.

## Page optimization: PropFuel examples and rules
- Title 50 to 60 characters (up to about 65 accepted), keyword phrase first in Title Case; meta 140 to 160 (shipped ones at 169 to 187 were too long).
- H1 pattern: keyword phrase + brand line ("Member Engagement Engine. More Engagement. Less Silence.").
- Internal link examples shipped: "Reads from your AMS" to /integrations; "success stories" to /client-success/case-studies; "prepare for renewal" to /use-cases/renewals; "win back lapsed members" to /use-cases/win-back; "Retention starts at onboarding" to /use-cases/onboarding.
- Target persona example (renewals): "People looking for membership renewal solutions who want to identify at-risk members, understand renewal concerns, automate personalized campaigns, and improve renewal rates." Shipped pages ran about 1,100 to 1,550 words.
- LLM insight example (Renewals): personalized communication, engagement tracking, automation, churn prevention, member analytics, targeted campaigns, feedback, renewal management.
- Add time to value ("first campaign live in 2 to 3 weeks") only if the Implementation page says so. End with a direct-ask CTA ("Bring your AMS. We'll show you what your members are already telling you."). Make CTAs specific ("Explore Insights Engine"); label wording changes as CRO.
- Worked examples:
  1. Homepage. Title before "AI-Powered Member Engagement Platform | PropFuel"; after "Powerful AI-Powered Member Engagement Software & Platform" (57; suffix dropped, both focus keywords in). Description after: "PropFuel is a member engagement platform that helps associations understand what members truly want, turning insights into stronger retention and lasting revenue." H1 after "Member Engagement Platform for Associations". Why: focus keywords absent from title and H1.
  2. Onboarding. H1 before "The retention conversation starts the day a member joins." After "Member Onboarding Starts the Retention Conversation." Title before "Automate New Member Onboarding Journeys | PropFuel", after "New Member Onboarding & Engagement Software for Associations". Meta claim "drive 3x engagement in the first 60 days" removed (unsourced); now "personalized check-ins across the first year, enrolled from your AMS".
  3. Heading retag (homepage Problem). "The Problem" `<p>` to `<h2>`; "Your data isn't up to date." `<h2>` to `<p>`. Same classes, same look.
  4. Renewals meta. Before: "recovering $320K+ in at-risk revenue" (unsourced). After: "adaptive campaigns that start 60 days before expiration". Why: failed the allow-list.
- Change-log header: Page | Webflow page id | Source brief | Date | Status | Code PRs.

## Corrections from Alex (dated, newest first)
- 2026-11-13: No gray-hat link tactics (an Instagram reel pushed a link trick). The agency also advised against. Why: short-term gains, penalty risk.
- 2026-11-12: Explain "outline" and "article": outline = research (keywords, competitors, headings, structure); article = the written content filled in. Filter to the top-10 keywords and say whether a count is monthly or a 3-month average (the "8 vs 5" question).
- 2026-11-12: Approved all current blog briefs. Low-volume but relevant posts stay for topical relevance and AI coverage.
- 2026-10-30: Brand facts allowed are only 370+ associations, the tagline, and 12% vs 0.98%. Client results from the Help Center only, labeled as one client. Banned: AAMFT 12%, AAP 80%. "If you build a few, AI should be able to build the rest" (templates).
- 2026-10-22: New ICP pages sit under the Use Cases dropdown as 2 mini cards above the product use cases. Show keyword position changes in reports. Send links per page in Slack to approve and publish.
- 2026-10-19: Treat the outlines as exactly what we want, subject to security and QA checks.
- 2026-10-08: Tagline is "Know and Grow Your Membership"; the keyword goes in the H1. Model that works: the agency drafts the page and writes the content, Alex reviews diffs and signs off, Alex publishes. Always explain why each change was made. Split test CTAs.
- 2026-10-01: Briefs must be specific enough for direct AI execution. Do one page first, then repeat. (The homepage H1 did not change because the brief was written for a human writer.)
- 2026-09-24: Wants links in chat, not a doc to hunt for. Wants benchmark and metric data.
- 2026-09-03: Association qualifier is the strongest signal; keep tiny-volume association keywords. Cut LMS and AMS brand keywords. Integration pages and ICP pages are wanted. PropFuel writes copy with its own Claude; the agency does not.
- 2026-08-27: Prioritize association keywords but keep a balance with member TOFU. "Membership marketing" is yellow, not red. ICP: professional associations about 75% of clients, trade associations, individual.
- 2026-06-18: AMS keywords are out (CRM territory, wrong intent, hardest fight). Use cases and webinar-style topics are rich. Research renewal and onboarding campaign terms.
- 2026-02-04: Only association- or member-qualified keywords ("SMS marketing software for associations", never generic). Wants a playbook up front to avoid rework, and an outline per page before design.
- Why rule exists: the agency's drafts carried unsourced stats; undisclosed paid links; a stale dashboard (placeholder grades, "Not Yet Assigned" on shipped pages, #REF! cells); an audit sheet with 1 of 40 ticked and placeholder grades.
- Pending: the audit's grades must come from evidence in notes, not placeholders.

## Changelog (org)
- 2026-11-25: profile split out of SKILL.md (org-agnostic refactor).
