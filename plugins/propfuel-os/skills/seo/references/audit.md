# Audit

Run order: crawl raw HTML (scripts/crawl_check.py) -> work the 40-item checklist -> add the PropFuel-specific checks -> grade -> Technical Task Tracker -> fix list with owner.

## Crawl (no JS)
```
python3 -I scripts/crawl_check.py https://www.propfuel.com/sitemap.xml --out crawl.csv
python3 -I scripts/crawl_check.py https://www.propfuel.com/sitemap.xml --limit 20   # quick pass
python3 -I scripts/crawl_check.py --self-test
```
CSV columns: url, status, title, title_len, meta_description, meta_len, canonical, robots_meta, h1_count, h1_text, jsonld_types (includes nested types), word_count, internal_links_out.
Flag rows: status not 200; title empty, duplicated, "PropFuel V2" or over 65 chars; meta empty or over 160; canonical empty, not self, or on a .webflow.io host; h1_count not 1; no FAQPage where a FAQ is visible; word_count under 300 on a page that has a lot of copy in the browser (JS-built content, the Mamba "not in JS" rule); internal_links_out under 3.
Then compare against the rendered DOM (browser or Playwright) for the few key pages. Anything in the DOM but not the raw HTML is a bug.
Agent readiness: `node qa/agent-readiness.mjs https://www.propfuel.com` in the custom-code repo (16 checks).

## The 40-item checklist (what / why / how)
Grade each A+ to F with estimated fix time (by number of affected URLs). Per item: status, last checked, notes.

### Technical (18)
1. GSC errors. Why: Google's own list of what it cannot index. How: Indexing and Experience reports, "Not indexed" first.
2. JavaScript content in initial HTML. Why: crawlers that do not run JS see nothing. How: curl vs rendered DOM.
3. Google cache / rendered snapshot. How: URL Inspection live test.
4. Pagination (rel next/prev, crawlable page links). How: blog index.
5. SSL. How: all URLs https, cert valid.
6. 404 pages and images. How: crawl status column; broken image src.
7. Redirects: chains, loops, 302s, JS redirects, to broken URLs, query strings kept. How: curl -I -L each.
8. Noindex / nofollow on pages that should rank (and missing on pages that should not).
9. Canonicals: self-referencing, absolute, https, www, one per page, never to 3xx/4xx or staging.
10. robots.txt: allows pages and AI bots, has the Sitemap line.
11. sitemap.xml: only 200, indexable, canonical URLs; submitted in GSC.
12. Site structure: logical folders, nav reaches every money page.
13. Crawl depth: money pages within 3 clicks.
14. Orphan pages: no internal links in. How: sitemap URLs minus linked URLs.
15. Speed and Core Web Vitals (Lighthouse, GTmetrix, CrUX): LCP under 2.5s, INP under 200ms, CLS under 0.1.
16. hreflang (only if multilingual; PropFuel is US English, mark N/A).
17. http to https resource links (mixed content).
18. Mobile friendly at 390px.

### On-page (10)
19. Missing titles and metas.
20. Too long: title 55-60 (up to ~65 ok), meta 155-160, focus keyword in title.
21. SEO-unfriendly URLs: short, lowercase, hyphenated, descriptive, evergreen.
22. Thin content and intent mismatch (under ~500 words on money pages; page does not match what the SERP rewards).
23. Internal links: 2 to 3 valuable links per page, descriptive anchors.
24. Broken internal and external links.
25. Missing or multiple H1; one H1 with the focus keyword.
26. Heading hierarchy: no skipped levels.
27. Schema present, valid, correct type (see references/technical.md matrix).
28. Image alt text and filenames: plain language, keyword only if natural, decorative blank.
(Mamba's list also had local GMB data; N/A for PropFuel.)

### Off-page (1)
29. Backlink profile audit: referring domains, anchors, toxic or high-spam links into a disavow file.

### UX / CRO (11, label every finding "CRO, optional")
30. HTML tags for structure. 31. Body text 16px min, ideally 18px. 32. Contrast 4.5:1 (3:1 bold and links). 33. Clear anchor text. 34. Video and audio captions or transcripts. 35. Can pause or mute autoplay. 36. Consistent menu order. 37. Copy states benefits and USPs. 38. Calls to action clear. 39. Descriptive copy. 40. Orphan words and layout at 390px (house rule).

Lesson: Mamba's sheet had 1 of 40 ticked and placeholder grades (B+, A+, C+, F) that contradicted its own proposal audit. Tick items only with evidence in notes.

## PropFuel and Webflow specific checks (all found on this site)
- Canonical pointing at staging (.webflow.io): fixed May 13. Re-check after template edits.
- Staging indexed despite the Webflow setting (the ROI page showed in a site: search). Staging must stay live for testing, so fix with noindex signals and canonical to prod.
- Customer-built landing pages hosted by PropFuel (e.g. survey pages) indexed as PropFuel content: add noindex, request removal in GSC.
- 328 auto-generated customer logo pages and 14 internal/event pages: noindex.
- app.propfuel.com and app.propfuel.com/to/... tracking links appear as ranking pages: noindex question stays open.
- Paid and conference landing pages (/cats-ask, /ig, Google Search LPs, /downloads/*): explicit index or noindex decision.
- UTM canonicalization: ?utm_source=... URLs must canonicalize to the clean page.
- Famewall review widget injected a fake 5.0 Product/aggregateRating on every page (Google policy violation). Turn off review-rating schema. Confirm status.
- Placeholder CEO quote ("Sarah Chen, co-founder and CEO") hidden on all 17 team pages. Remove.
- Duplicate "PropFuel V2" titles on 126 CMS pages (fixed Sep 11 with CMS bindings). Re-check new CMS collections.
- JS-only schema (Organization, WebPage, FAQPage written by script): fixed Sep 11 and Oct 7. Re-check any new page.
- Placeholder text and fake testimonial quotes in raw HTML that JS overwrote ("This is some text inside of a div block", "Sarah Mitchell, VP of Membership, AAP"): grep raw HTML for these.
- Orphan pages: 43 open as of the October report.
- 301s dropping query strings: Webflow 301s for /demo and /request-demo drop UTMs. Check live ad and email URLs.
- Homepage blog cards render href="#" in raw HTML (no crawlable links to posts).
- Product schema on about 149 pages where it does not belong.
- Duplicate H2s across /platform/engagement and /platform/insights (leftover skeleton).
- /book-a-demo has no H1 in raw HTML.
- Markdown alternate link is JS-injected, so non-JS agents never see it.

## Technical Task Tracker (create in the SEO Program workbook; columns)
ID | Priority (P1/P2/P3) | Checklist item # | Issue | Affected URLs (count + list or template) | Why it matters | Exact fix | Owner (Claude / Alex / Webflow dev) | Status (Open / PR open / Approved / Live / Verified) | Date found | Date verified live | Notes
Sort by priority then URL count. Fix by template (blog post, video, case study, author) before one-off pages.

## Output of an audit
1. Summary: grades by category, top 5 fixes by impact.
2. Tracker rows.
3. A diff-ready fix per row (references/technical.md).
Findings use: `[SEVERITY] title / Location (URL) / Issue / Fix (exact old to new)`.
