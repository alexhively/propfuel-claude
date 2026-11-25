---
name: seo
description: An SEO agency in a skill, for any organization. Use for SEO, keyword research, site audit, technical SEO, crawlability and indexability, Core Web Vitals, meta titles and descriptions, H1s, schema and structured data, page outline or brief, "optimize this page", new landing pages or blogs for SEO, backlinks, GEO / AEO / AI search / LLM visibility, the monthly SEO report, or the weekly SEO check-in. Claude runs the program end to end (audit, keywords, fixes, outlines, articles, reports) and a named person approves every change that ships. Org specifics live in org/<slug>.md.
---

# SEO (agency in a skill)

Method lives here and in references/. Everything specific to one organization (ICP, facts, stack, keyword map, corrections) lives in `org/<slug>.md`. Attribution: the generic checklist was merged from the ECC SEO skill (MIT, github.com/affaan-m/ECC).

## 0. Load the org profile (before any mode)
1. Find the organization being worked on. This plugin is PropFuel's, so default to `org/propfuel.md`.
2. Read `org/<slug>.md` in full. It names the approver, stack, ship flow, facts allow-list, qualifier rule, data sources, state doc and hooks. Run its start-of-run hooks.
3. No profile for this organization? Run the intake in `org/TEMPLATE.md` first: interview the user, then write `org/<slug>.md` (or keep it in the user's own state doc). Do not start any mode without one.
4. End of every run: run the profile's end-of-run hooks (log outcomes, update the state doc), then list what needs approval with the exact diff or link.

## 1. Principles
1. Fix technical blockers before content optimization.
2. One page, one primary search intent.
3. Long-term quality signals over manipulation.
4. Mobile-first: Google indexes the mobile version. Check at 390px.
5. Recommendations are page-specific and implementable: exact old text to exact new text.
6. Read the real page before advising. Never give generic "improve SEO" output.

## 2. Modes
| Mode | Say | Open |
|---|---|---|
| Audit | "SEO audit", "what is broken", crawlability, Core Web Vitals | references/audit.md (+ scripts/crawl_check.py) |
| Keyword research | "keyword research", "what should we rank for" | references/keyword-research.md |
| Technical fixes | "fix schema / canonicals / redirects / sitemap / llms.txt" | references/technical.md |
| Optimize existing page | "optimize this page", "outline and article", "metadata and H1" | references/page-optimization.md |
| New page | "new landing page for SEO", "integration page" | references/new-pages.md |
| Blog / template content | "blog for SEO", "which posts first" | references/blog-and-templates.md |
| Backlinks | "backlinks", "guest posts" | references/backlinks.md |
| GEO | "AI search", "LLM visibility", "AEO prompts" | references/geo.md |
| Monthly report | "monthly SEO report", "how did SEO do" | references/reporting.md |
| Weekly check-in | "SEO status", "weekly SEO update" | references/program.md |
| Program cycle | "what runs this month", "SEO roadmap" | references/program.md |

## 3. Hard rules
- Native, crawlable HTML. Titles, metas, canonicals, schema, FAQ JSON-LD (word for word the visible FAQ), OG tags, headings, copy, alt text and internal link hrefs are in the served HTML, never injected by JS. JS is for behavior only. Why: GPTBot, ClaudeBot, PerplexityBot and link unfurlers do not run JS.
- One intent per page. Landing pages own commercial terms; blogs never target a term a landing page owns. Why: cannibalization.
- Facts allow-list. Copy uses only the facts, numbers, names and quotes the org profile lists. Anything else: write `{{number}}` and flag it. Client results only from a named source, labeled as one client, never an average.
- Recommendations are AI-executable: exact old text to exact new text, per element. Never "name the product" or "improve the hero".
- Label CRO suggestions (CTA wording, button tests) separately from SEO.
- No gray-hat links (PBNs, link trades at scale, comment spam, "link drip" tricks). Paid placements carry rel="sponsored".
- Nothing ships until the approver named in the profile approves that exact diff. Drafts (outlines, articles, sheets, reports) go out end to end without asking.
- After every publish, re-check the native title, meta and canonical of the pages touched. Why: a full-site publish can revert them.
- Never fake numbers. If a data source is missing, say so, label the number "unknown" or its as-of date, and raise the ask.
- Follow the profile's spelling and style rules.

## 4. Data sources and how each mode degrades
Read the profile's "Data sources" for what is actually connected. Pull data into a CSV or the state doc; always state the as-of date and whether a figure is monthly or an average.
| Source | Used by | Without it |
|---|---|---|
| Search Console (`scripts/gsc.py`) | keyword positions, reports, indexation, AI Overview impressions | Report from the last snapshot, label every number with its as-of date, put "Search Console access needed" at the top; use WebSearch spot checks for positions |
| Keyword volumes (Keyword Planner API via `scripts/kp.py`, Keyword Planner web UI, or a paid tool) | keyword research, content triage, easy-win rule | Mark volume and KD "unknown"; judge by SERP fit (who ranks, how big, does the page type match) and cluster judgment; say so in the sheet |
| AI-visibility tracker (HubSpot AEO, Profound, Peec, etc.) | GEO | Run the tracked prompts by hand in WebSearch or an LLM monthly; record whether the brand is named and which domains are cited |
| Analytics and conversions (GA4, PostHog) | reports, AI referral traffic, organic conversions | Report stops at clicks and impressions; raise the conversion-tracking ask |
| Live HTML crawl (`scripts/crawl_check.py`, curl) | audit, post-publish checks | Never optional; it only needs a sitemap URL |
| SERP and competitor checks (WebSearch) | difficulty, SERP fit, competitor gaps | Say what could not be checked |
Difficulty is always a SERP judgment when no KD tool exists.

### Scripts (stdlib only, run with `python3 -I`)
- `scripts/crawl_check.py <sitemap URL> [--limit N] [--out file.csv]` raw-HTML crawl (no JS). `--self-test`.
- `scripts/gsc.py auth | sites | query --site <property> --start --end --dims query,page`. `self-test`.
- `scripts/kp.py "kw" ... | --file f.txt | --ideas "seed"` Keyword Planner API volumes. Requires Google Ads API Basic access. `--self-test`.
- Config dir: env `SEO_CONFIG_DIR`, default `~/.config/seo`, falling back to `~/.config/propfuel` if that exists. Files: `gsc.json` (token), `google-ads.env`, `google-ads-adc.json` (OAuth client).

## 5. Changelog
- 2026-11-25: org-agnostic: method in SKILL.md and references, org specifics in org/<slug>.md; merged the ECC generic SEO checklist.
- 2026-11-25: Basic API denied twice (Internal app); volumes come from Keyword Planner in Chrome.
- 2026-11-25: Keyword Planner script (scripts/kp.py); Google Ads Basic access only, no paid SEO tool.
- 2026-11-25: Search Console connected (scripts/gsc.py); unbranded numbers exclude person-name queries.
- 2026-11-25: rebuilt from the full agency engagement (14 weekly calls, shared Slack channel, workbook and docs, custom-code repo history, live-site fetch). Replaces the ECC generic SEO skill. Program state moved to OS knowledge `seo-program.md`.
