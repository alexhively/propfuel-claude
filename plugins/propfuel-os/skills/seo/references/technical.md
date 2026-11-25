# Technical fixes: how to implement

Principle: the server sends static HTML and everything crawler-relevant is native to it. Scripts add behavior only. Two sources of truth drift: if the CMS has a field natively, no script may inject it. The org profile says where each item lives on this site and how changes ship.

## Where each thing lives (generic)
| Item | Native home |
|---|---|
| Title, meta description, OG title/description, canonical | CMS page settings, or template bindings for collections (Title Tag to Name, Meta Description to a description field, OG image to featured image) |
| OG image | CMS settings or the design tool; check the API can set it |
| Organization JSON-LD | Site-wide head code |
| WebPage, BreadcrumbList, FAQPage, SoftwareApplication, CollectionPage, AboutPage | Page-level head code |
| BlogPosting, VideoObject, Article, Person/ProfilePage | Collection template head code using field tokens |
| H1, headings, body copy, FAQ answers, stats, logos with alt text | Native elements or HTML embeds |
| Redirects | CMS or host redirect rules. Remove the page occupying the old slug first |
| robots.txt, sitemap, llms.txt | Site settings or static files |
Stays in JS: carousels, tab switching, accordions, scroll animations, nav behavior, tracking.

## Redirect rules
- One hop (max 2). No chains, no loops.
- Keep query strings (UTMs); test with `curl -sI "https://example.com/old?utm_source=x"`. Update old links and ads to the final URL.
- JS redirects (window.location.replace) are not redirects to Google. Never use them.
- Removed or renamed URL: add the 301 in the same change, to the closest equivalent (not a lossy catch-all).
- Native CTAs pointing at a redirected URL cost an extra hop: repoint them.

## Schema by page type
| Page type | Required | Never |
|---|---|---|
| Homepage | Organization (or LocalBusiness where appropriate), WebSite, WebPage | Product unless it is a product |
| Product / software page | Product or SoftwareApplication with Offer where true, BreadcrumbList | aggregateRating not backed by real, visible reviews |
| Use-case, solution, integration pages | WebPage, BreadcrumbList, Organization (site head); FAQPage only where a visible FAQ exists | Product, aggregateRating |
| Blog posts | BlogPosting or Article (headline, author Person, publisher Organization, datePublished), BreadcrumbList | Product |
| Blog index, case study index | CollectionPage, BreadcrumbList | |
| Video pages | VideoObject, BreadcrumbList, WebPage | |
| Authors / team pages | ProfilePage + Person, BreadcrumbList | |
| About / Contact | AboutPage / ContactPage | |
| Q&A sections | FAQPage only when the content truly is Q&A and visible | FAQPage for content not on the page |
Rules: schema matches visible content. FAQPage JSON-LD matches the visible FAQ word for word and appears once per page (Q and A in a `<details>` or accordion in HTML). Parse every block (`json.loads`); validate with the Rich Results Test. Third-party review widgets can inject fake aggregateRating: turn it off.
Minimal example:
```json
{"@context":"https://schema.org","@type":"Article","headline":"Page Title Here",
 "author":{"@type":"Person","name":"Author Name"},
 "publisher":{"@type":"Organization","name":"Brand Name"}}
```

## Robots, sitemap, llms.txt, markdown
- robots.txt: `User-agent: *`, `Allow: /`, one `Sitemap:` line (dedupe repeats), block only low-value surfaces. AI bots stay allowed unless the org decides otherwise.
- Sitemap: only 200, indexable, canonical URLs; review landing-page variants and parameter pages.
- llms.txt (llmstxt.org format): H1, summary, "When to use" (with an explicit not-the-right-fit list), "How an agent should engage", Product, Use cases, Proof, Company, Optional. Keep facts in sync with the allow-list.
- Markdown alternates: a mirror host that is noindex, with a canonical Link header to the main site. The `<link rel="alternate" type="text/markdown">` belongs in native head code, not a script.

## Internal linking and authors
- 2 to 3 links per page with descriptive keyword anchors; link from strong pages to pages you want to rank; backfill links from new pages to relevant existing ones.
- Every new page linked from nav, a body section and the sitemap.
- Blogs link to the landing page they support (never compete with it); landing pages link down to supporting posts.
- Every blog post links to its author page (a trust signal). Team pages stay free of placeholder quotes.
- Make links real hrefs in served HTML (not `href="#"` filled by script).
- Run a link check on every change (all internal links return 200).

## Ship flow (generic)
1. Branch or draft per page group. Code first if it is backward compatible, then CMS edits, then publish.
2. PR or change note: what changed, QA checks, what is staged separately in the CMS.
3. Show the approver the exact diff and a before/after table. Approver approves that exact diff.
4. Merge or publish. Before pushing code: PII and secrets scan, syntax check, the repo's QA hook; never bypass hooks.
5. Re-check native title, meta and canonical on pages touched.
6. Verify live (below). Write the change log (references/page-optimization.md).

## QA gates (all pages)
- Fetch served HTML: new title, meta, canonical, OG, exactly one H1, expected H2 order, JSON-LD parses with one FAQPage, no placeholder text.
- Internal links return 200.
- Claims check against the facts allow-list; spelling and style per the profile.
- Orphan-word gate: no single word alone on the last line (text-wrap balance on headings and buttons, pretty on body, nbsp ties).
- Screenshots at 1440 and 390 px: no horizontal scroll, no JS errors, accordions and carousels work. Read them before showing the approver.

## Undo
- Code: revert the merge commit.
- CMS: restore the backup taken just before publish (note its timestamp in the change log), then publish.
- Embed or snippet: delete it (check no script re-injects a fallback).
- Redirect: remove the rule.

## Platform notes: Webflow
Useful to any Webflow org. Webflow serves static HTML, so native fields are crawler-safe.
- Title, meta, OG, canonical: page settings (static pages) and CMS template bindings. Data API: pages tool for page SEO, CMS tool for collections. OG image: Designer only (not settable through the Data API).
- Site-wide schema and custom code: Site settings, head code. Page-level schema: the page settings custom code field. Collection schema: CMS template head code with field tokens.
- Redirects: Site settings, Publishing, 301 rules. Delete or unpublish the page occupying the old slug first. Webflow 301s can drop query strings: test with curl.
- robots.txt, sitemap, llms.txt: Site settings, SEO. Re-upload llms.txt when its source changes.
- Staging (*.webflow.io) can be indexed despite the setting: disable indexing and make sure canonicals point to production, never to staging.
- Collection pages default to a CMS title string if bindings are missing (duplicate titles site-wide): bind Title Tag and Meta Description in every template.
- Custom code and embeds: put crawler-relevant markup in native elements or HTML Embeds (served HTML), not injected by site scripts. Third-party widgets (reviews) can inject schema: audit raw HTML.
- Publishing the whole site can overwrite settings edited elsewhere: re-check title, meta, canonical after every publish. Take a backup first (Designer, Backups).
- Dynamic list links: set them natively to the collection item; the API cannot set some of them.

## Other platforms
- WordPress: titles and metas, canonicals, robots meta and schema in the SEO plugin (Yoast, Rank Math) per post/template; redirects in the plugin or server config; robots.txt and sitemap generated by the plugin or core; theme and builder output can inject duplicate H1s.
- Next.js / Vercel: titles, metas, canonicals, OG in the Metadata API (`generateMetadata`) or `<Head>`; JSON-LD as a `<script type="application/ld+json">` in the server component; redirects in `next.config.js` (`redirects()`) or `vercel.json`; `app/robots.ts` and `app/sitemap.ts`. Server-render these; client-only rendering hides them from non-JS crawlers.
- HubSpot CMS: title and meta in page or post settings; canonical and schema in head HTML (page, template or domain); redirects in Settings > Website > URL Redirects; robots.txt and sitemap in Settings > Website > Pages > SEO & Crawlers; check the blog's tag and author archive pages for thin or duplicate content.
