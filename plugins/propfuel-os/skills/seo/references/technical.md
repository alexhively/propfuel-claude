# Technical fixes: how to implement on this stack

Principle: Webflow serves static HTML. Everything crawler-relevant is native. The enhancement script (js/webflow-enhancements.js on GitHub Pages) adds behavior only. Mamba's Sep 11 and Oct 7 commits removed all SEO injection from the script; do not reintroduce it.

## Where each thing lives
| Item | Where | Tool |
|---|---|---|
| Title, meta description, OG title/description, canonical | Webflow page settings (static pages); CMS template bindings (Title Tag to Name, Meta Description to description field, OG image to featured image) | Webflow MCP `data_pages_tool` (page SEO), `data_cms_tool` |
| OG image | Designer only (cannot be set through the Data API) | Designer |
| Organization JSON-LD | Site-wide head custom code | `data_scripts_tool` / Site settings |
| WebPage, BreadcrumbList, FAQPage, SoftwareApplication, CollectionPage, AboutPage | Page-level custom code ("schema" field in page settings) | `data_pages_tool` |
| BlogPosting, VideoObject, Article, Person/ProfilePage, DigitalDocument | CMS template head code using field tokens | Designer / CMS template |
| H1, headings, body copy, FAQ answers, stats, logos with alt text | Native elements or HTML Embeds (same markup and classes the script used) | `data_element_tool`, `data_whtml_builder` |
| Redirects | Webflow 301s (Site settings, Publishing). Delete the page that occupies the old slug first | Designer / site settings |
| robots.txt, sitemap, llms.txt | Webflow Site settings (SEO). llms.txt source: `agent/llms.txt` in the custom-code repo; re-upload when it changes | Site settings |
| Markdown alternate link | Site head code (currently JS-injected: fix) | Site settings |
Stays in JS: carousel loops, tab switching, accordion open and close, scroll animations, nav behavior, tracking, text-wrap CSS, the claims safety net (js/copy-fixes.js).
Rule from the code: two sources of truth drift. If Webflow has it natively, the script must skip it. Every script injector checks for the static node first.

## Redirect rules
- Every demo link goes to /book-a-demo. /demo and /request-demo are Webflow 301s to /book-a-demo (single hop, no chains).
- Keep query strings. Today's Webflow 301s drop them (UTMs lost on /demo?utm_source=x). Fix by updating old links and ads to /book-a-demo directly; test with `curl -sI "https://www.propfuel.com/demo?utm_source=x"`.
- JS redirects (window.location.replace) are not redirects to Google. Never use them.
- Removed or renamed URL: add the 301 in the same change. /solutions/associations 301s to /client-success/customers (lossy); /use-cases/feedback is a 404 that other pages linked to.
- Native CTAs still pointing at /demo cost one extra hop: repoint.

## Schema by page type (Schema Check tab matrix)
| Page type | Required | Never |
|---|---|---|
| Homepage | Organization, WebSite, WebPage, SoftwareApplication with offers and brand | Product |
| Product, use-case, solutions, integrations pages | WebPage, BreadcrumbList, Organization (site head); FAQPage only where a visible FAQ exists; SoftwareApplication on /platform/overview | Product, aggregateRating |
| Blog posts | BlogPosting (or Article), BreadcrumbList, WebPage | Product |
| Blog index, case study index | CollectionPage, BreadcrumbList | |
| Video pages | VideoObject, BreadcrumbList, WebPage | |
| Authors / team pages | ProfilePage + Person, BreadcrumbList | |
| About | AboutPage | |
| Contact | ContactPage | |
Rules: FAQPage JSON-LD matches the visible FAQ word for word and appears once per page (Q and A in a `<details>` or accordion in HTML). Parse every block (`json.loads`); validate with the Rich Results Test. Known gaps: /solutions lacks BreadcrumbList; /membership-ai lacks FAQPage; Famewall markup must stay off.

## Robots, sitemap, llms.txt, markdown
- robots.txt: `User-agent: *`, `Allow: /`, one `Sitemap: https://www.propfuel.com/sitemap.xml` line (live file repeats it twice: dedupe). AI bots stay allowed.
- Sitemap: only 200, indexable, canonical URLs (212 on Nov 25). Review /book-a-demo-15min and landing-page variants.
- llms.txt (llmstxt.org format): H1, summary, "When to use PropFuel" (with an explicit not-the-right-fit list), "How an agent should engage" (send to /book-a-demo, no public API, do not quote prices, 2-3 week typical timeline), Product, Use cases, Proof, Company, Optional. Current file is stale: says "330+ associations" and "5-30 minutes" AMS setup. Fix both.
- Markdown alternates: `propfuel-edge.vercel.app/<page>.md` mirrors, noindex host, canonical Link header to www. Move the `<link rel="alternate" type="text/markdown">` into native head code.

## Internal linking and authors
- 2 to 3 links per page with descriptive keyword anchors; every new page linked from nav, a body section and the sitemap.
- Every blog post links to its author page (blog to author bio is a trust signal). Team pages must stay free of placeholder quotes.
- Blogs link to the landing page they support (never compete with it); landing pages link down to the supporting posts.
- Set homepage blog card links natively to "Current Blog Post" in the Designer (the API cannot), so hrefs are real.
- Run a link check on every change (PR #48: 37 of 37 returned 200).

## Ship flow
1. Branch per page group in `alexhively/propfuel-webflow-custom`. JS first (backward compatible, so pages never break), then Webflow edits, then publish.
2. PR body: what changed, QA checks, what is staged separately in Webflow (git cannot show the Webflow half).
3. Show Alex the exact diff and before/after table. Alex approves that exact diff.
4. Merge to main, `git push origin` (GitHub = what is live; ~1-2 min deploy, ~10 min browser cache; bump `?v=` on copy-fixes.js when its table changes).
5. Webflow publish (Alex, or Claude after approval). Re-check native title, meta, canonical on the pages touched.
6. Verify live (below). Write the change log (references/page-optimization.md).
Pushing to main is live on prod and staging. Before the push: PII and secrets scan, `node --check` on edited JS, QA hook (`qa/hooks/pre-push`, runs `qa/run-qa.mjs`). Do not bypass with --no-verify.

## QA gates (all pages)
- Fetch served HTML: new title, meta, canonical, OG, exactly one H1, expected H2 order, JSON-LD parses with one FAQPage, no placeholder text.
- Internal links return 200.
- Claims check: 370+ associations; 12% always with "vs 0.98% for the average association"; no hourly sync, guaranteed real-time write-back, "5-30 minutes", "plug-and-play", "connected in minutes", "No IT project"; no PropFuel API claim; no unsourced stats; US spelling; no em dashes.
- Orphan-word gate: no single word alone on the last line (text-wrap balance on headings and buttons, pretty on body, nbsp ties).
- Screenshots at 1440 and 390 px: no horizontal scroll, no JS errors, accordions and carousels work. Read them before showing Alex.

## Undo
- JS: revert the merge commit (script is backward compatible); GitHub Pages updates in about a minute.
- Webflow: Designer, Backups, restore the backup taken just before publish, then publish. Take that backup first and note its timestamp in the change log.
- HTML Embed: delete the embed and the script re-injects its fallback (only on pages that still have the fallback).
- Redirect: remove the 301 rule.

## Commit history (precedent). Mamba authored PR #1, #2 and the Oct 7 commit; the rest is Alex + Claude implementing Mamba outlines
- 2026-09-11 PR #1: removed client-side title, meta, canonical, OG and Organization/WebPage JSON-LD; rebuilt natively; CMS templates bound; 301s for /request-demo. Why: crawlers saw `<title>PropFuel V2</title>` and no description or canonical on every CMS page.
- 2026-09-11 PR #2: removed the JS /demo redirect.
- 2026-10-07 (direct to main): removed client-side FAQ schema; FAQPage now native.
- 2026-10-08 PR #21: native homepage engine rows and static testimonial grid; PR #26/#40 agent readiness (llms.txt, markdown alternates, 16 checks).
- 2026-10-19/20 PRs #46-#49, #54: claims and orphan-word safety net, one H1 per page, MGI 2026 citation in the renewals FAQ.
- 2026-09-24 PRs #4-#7: homepage, platform, onboarding, renewals made static-first.
- 2026-10-26 PRs #64/#65: Solutions hub and use-case revamps.
