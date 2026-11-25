---
name: seo
description: PropFuel's SEO agency in a skill. Use for SEO, keyword research, site audit, technical SEO, meta titles and descriptions, H1s, schema, page outline or brief, "optimize this page", a new landing page or blog for SEO, backlinks, GEO / AEO / AI search / LLM visibility, the monthly SEO report, the weekly SEO check-in, or "what would Mamba do". Claude runs the program end to end (audit, keywords, fixes, outlines, articles, reports) and a person approves every change that ships.
---

# SEO (PropFuel agency in a skill)

## 1. What this replaces and how it runs
Replaces the Mamba SEO agency engagement (Feb to Nov 2026: weekly call, Google Sheet workbook, per-page "Outline & Article" docs, paid guest posts, monthly report). Claude does that work. Alex (or a teammate he names) approves.

Start every run:
1. `get_briefing` (OS). 2. `get_knowledge seo-program.md` (program state: workbook and doc links, keyword-to-page map, open items, baselines). 3. Pick the mode below and open its reference file.

End every run:
1. `log_update` with initiative `mamba-seo` (one line per outcome). 2. Update `seo-program.md` (`update_knowledge`, mode "replace", only what changed: done, live, open items, numbers). 3. Say what needs Alex's approval, with the exact diff or link.

Links to the SEO Program workbook, the SEO and GEO report, the Schema audit, the Content Fix List and every page doc live in `seo-program.md`, not in this repo.

## 2. Modes
| Mode | Say | Open |
|---|---|---|
| Audit | "SEO audit", "what is broken on the site" | references/audit.md (+ scripts/crawl_check.py) |
| Keyword research | "keyword research", "what should we rank for" | references/keyword-research.md |
| Technical fixes | "fix schema / canonicals / redirects / sitemap / llms.txt" | references/technical.md |
| Optimize existing page | "optimize this page", "outline and article", "metadata and H1" | references/page-optimization.md |
| New page | "new landing page for SEO", "integration page" | references/new-pages.md |
| Blog / template content | "blog for SEO", "which template posts first" | references/blog-and-templates.md |
| Backlinks | "backlinks", "guest posts", "Associations Now" | references/backlinks.md |
| GEO | "AI search", "LLM visibility", "AEO prompts" | references/geo.md |
| Monthly report | "monthly SEO report", "how did SEO do" | references/reporting.md |
| Weekly check-in | "SEO status", "weekly SEO update" | references/program.md |
| Program cycle | "what runs this month", "SEO roadmap" | references/program.md |

## 3. Hard rules
- ICP filter: the word "association" is the ICP qualifier. Formula: use case + "for associations". Why: "member ___" alone also pulls YMCAs, yacht clubs, Boys and Girls Clubs. AMS, LMS, advocacy and generic marketing terms are out (PropFuel is not a CRM or LMS and cannot win that fight). Integration queries ("member engagement platform that integrates with <AMS>") are in.
- One page, one primary intent. Landing pages own commercial terms; blogs never target a term a landing page owns. Why: cannibalization.
- Everything a crawler needs is native HTML in Webflow, never JS-injected: titles, metas, canonicals, schema, FAQPage JSON-LD (matched word for word to the visible FAQ), OG tags, headings, copy, alt text, internal link hrefs. JS is for behavior only. Why: GPTBot, ClaudeBot, PerplexityBot and link unfurlers do not run JS.
- Facts allow-list. Only: 370+ associations; tagline "Know and Grow Your Membership" (front-facing; "Make Membership Meaningful" is the umbrella job only); "12% average annual revenue growth after implementing PropFuel", always next to "vs 0.98% for the average association". Client results only from the Help Center or the Case Studies master, labeled as one client, never an average. Banned: AAMFT 12%, AAP 80%. Unknown number: write `{{number}}` and flag it. Why: Mamba's drafts carried unsourced stats (see Corrections).
- US spelling ("organization", not "organisation"). No em dashes. Start sentences with a subject so AI engines can quote them.
- Recommendations must be AI-executable: exact old text to exact new text, per element. Never "name the product" or "improve the hero". Why: Oct 1 lesson, the homepage H1 did not change because the brief was written for a human writer.
- Label CRO suggestions (CTA wording, button tests) separately from SEO. Why: Alex asked why a free-demo CTA sat inside an SEO outline.
- No gray-hat links. Paid placements must carry rel="sponsored". Why: undisclosed paid links are link spam; Mamba's batches did not disclose.
- Nothing ships to Webflow or GitHub main until Alex approves that exact diff. Drafts (outlines, articles, metadata sheets, reports) go out end to end without asking.
- After every Webflow publish, re-check the native title, meta and canonical of the pages touched. Why: a full-site publish once reverted the homepage meta title.

## 4. Corrections from Alex (newest first)
- 2026-11-13: Do not use gray-hat link tactics (an Instagram reel pushed a link trick). Mamba also advised against. Why: short-term gains, penalty risk.
- 2026-11-12: Explain "outline" and "article": outline = research (keywords, competitors, headings, structure); article = the written content filled in. Also: filter to the top-10 keywords and say whether a count is monthly or a 3-month average (the "8 vs 5" question).
- 2026-11-12: Approved all current blog briefs ("move forward and write them"). Low-volume but relevant posts stay for topical relevance and AI coverage.
- 2026-10-30: Brand facts allowed are only 370+ associations, the tagline, and 12% vs 0.98%. Client results from the Help Center only, labeled as one client. Banned: AAMFT 12%, AAP 80%. "If you build a few, AI should be able to build the rest" (templates).
- 2026-10-22: New ICP pages sit under the Use Cases dropdown as 2 mini cards above the product use cases (mirrors Membership AI above Solutions and Tools). Show keyword position changes in reports. Send links per page in Slack to approve and publish.
- 2026-10-19: Treat the outlines as exactly what we want, subject to security and QA checks.
- 2026-10-08: Tagline is "Know and Grow Your Membership"; the keyword goes in the H1 ("Member Engagement Software for Associations"). Model that works: the agency drafts the page and writes the content, Alex reviews diffs and signs off, Alex publishes. Always explain why each change was made. Split test CTAs.
- 2026-10-01: Briefs must be specific enough for direct AI execution. Do one page first, then repeat the process.
- 2026-09-24: Wants links in chat, not a doc to hunt for. Wants benchmark and metric data.
- 2026-09-03: Association qualifier is the strongest signal; keep tiny-volume association keywords. Cut LMS and AMS brand keywords. Integration pages and ICP pages are wanted. PropFuel writes copy with its own Claude; the agency does not.
- 2026-08-27: Prioritize association keywords but keep a balance with member TOFU. "Membership marketing" is yellow, not red (PropFuel can serve it). ICP: professional associations about 75% of clients, trade associations, individual.
- 2026-06-18: AMS keywords are out (CRM territory, wrong intent, hardest fight). Use cases and webinar-style topics are rich. Research renewal and onboarding campaign terms.
- 2026-02-04: Only association- or member-qualified keywords ("SMS marketing software for associations", never generic). Wants a playbook up front to avoid rework, and an outline per page before design.

## 5. Data sources and gaps
Connected:
- Webflow MCP (pages, SEO fields, CMS, sitemap, publish) and the custom-code repo `alexhively/propfuel-webflow-custom` (GitHub Pages scripts, QA hooks). Local build source: `~/Projects/propfuel-page-previews/src/mamba-system`.
- HubSpot AEO: `get_aeo_metrics`, `manage_aeo_prompts` (25 free prompt slots). Unconfigured as of 2026-11-25.
- PostHog "SEO & AEO" dashboard and AI-assistant referrals.
- Google Search Console (connected 2026-11-25, property `sc-domain:propfuel.com`): `python3 -I scripts/gsc.py query --site sc-domain:propfuel.com --start YYYY-MM-DD --end YYYY-MM-DD --dims query,page > out.csv`. Token in ~/.config/propfuel/gsc.json on Alex's Mac (re-run `gsc.py auth` if it expires). Data lags about 2 days. Branded = regex `propfuel|prop fuel`; also exclude team-member and person-name queries (e.g. Michael Arisco, Love is Blind traffic) from unbranded before reporting.
- Live HTML fetch (`scripts/crawl_check.py`, curl) and WebSearch for SERP, competitor and LLM checks.

Not connected (raise the ask, do not fake the number):
| Missing | Without it | Ask to raise |
|---|---|---|
| GA4 conversions | No organic demo bookings. Report stops at clicks and AI referrals (PostHog). | Finish GA4 and GTM plus demo-booking conversion tracking (open since Sep). |
| Volume / KD tool (Ahrefs, Semrush, DataForSEO, or Google Ads Keyword Planner with a developer token) | Keyword research reuses the 128-keyword list and its volumes; new terms get SERP-based difficulty judgment, labeled "no volume". No DR or backlink counts. | Pick one tool and connect it. Keyword Planner with the existing Google Ads MCP is the cheapest. |
| HubSpot AEO prompts | GEO tracks by manual prompt runs in WebSearch only. | Load the key prompts (references/geo.md). |

## 6. Changelog
- 2026-11-25: Search Console connected (scripts/gsc.py); unbranded numbers now exclude person-name queries.
- 2026-11-25: rebuilt from the full Mamba engagement (14 weekly calls, shared Slack channel, workbook and docs, the Webflow custom-code repo history, live-site fetch). Replaces the ECC generic SEO skill. Program state moved to OS knowledge `seo-program.md`.
