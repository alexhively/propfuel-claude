# Audit

Run order: crawl raw HTML (scripts/crawl_check.py) -> work the 40-item checklist -> add the org profile's platform-specific checks -> grade -> Technical Task Tracker -> fix list with owner.

## Crawl (no JS)
```
python3 -I scripts/crawl_check.py https://example.com/sitemap.xml --out crawl.csv
python3 -I scripts/crawl_check.py https://example.com/sitemap.xml --limit 20   # quick pass
python3 -I scripts/crawl_check.py --self-test
```
CSV columns: url, status, title, title_len, meta_description, meta_len, canonical, robots_meta, h1_count, h1_text, jsonld_types (includes nested types), word_count, internal_links_out.
Flag rows: status not 200; title empty, duplicated, a CMS default string (e.g. "Home" or the site's draft name) or over 65 chars; meta empty or over 160; canonical empty, not self, or on a staging host; h1_count not 1; no FAQPage where a FAQ is visible; word_count under 300 on a page that has a lot of copy in the browser (JS-built content); internal_links_out under 3.
Then compare against the rendered DOM (browser or Playwright) for the few key pages. Anything in the DOM but not the raw HTML is a bug.
Also check any agent-readiness tooling the profile names.

## Crawlability
- robots.txt allows important pages and blocks low-value surfaces (internal search, carts, staging).
- No important page is unintentionally `noindex`; pages that should not rank are.
- Important pages reachable within a shallow click depth (money pages within 3 clicks).
- Redirect chains max 2 hops (aim for 1); no loops.
- Canonical tags self-consistent and non-looping.

## Indexability
- One preferred URL format (https, www or not, trailing slash, lowercase), enforced by redirects.
- Multilingual pages have correct hreflang (reciprocal, self-referencing, valid codes); mark N/A if single-language.
- Sitemap = the intended public surface: only 200, indexable, canonical URLs; submitted in Search Console.
- No duplicate URLs competing without canonical control (parameters, UTMs, print views, trailing slash).

## Performance (Core Web Vitals)
- LCP under 2.5s, INP under 200ms, CLS under 0.1 (field data from CrUX or Search Console first, lab data second).
- Common fixes: preload the hero asset and set `fetchpriority="high"`; reduce render-blocking CSS/JS; defer third-party tags; reserve layout space (width/height or aspect-ratio on images, embeds and ads) for CLS; serve modern image formats at the right size; lazy-load below-the-fold images only; trim heavy JS and long tasks for INP; use font-display: swap with preloaded fonts.

## The 40-item checklist (what / why / how)
Grade each A+ to F with estimated fix time (by number of affected URLs). Per item: status, last checked, notes. Tick items only with evidence in notes.

### Technical (18)
1. Search Console errors. Why: Google's own list of what it cannot index. How: Indexing and Experience reports, "Not indexed" first.
2. JavaScript content in initial HTML. Why: crawlers that do not run JS see nothing. How: curl vs rendered DOM.
3. Google cache / rendered snapshot. How: URL Inspection live test.
4. Pagination (crawlable page links). How: blog index.
5. SSL. How: all URLs https, cert valid.
6. 404 pages and images. How: crawl status column; broken image src.
7. Redirects: chains, loops, 302s, JS redirects, to broken URLs, query strings kept. How: curl -I -L each.
8. Noindex / nofollow on pages that should rank (and missing on pages that should not).
9. Canonicals: self-referencing, absolute, https, one per page, never to 3xx/4xx or staging.
10. robots.txt: allows pages and AI bots, has the Sitemap line.
11. sitemap.xml: only 200, indexable, canonical URLs; submitted in Search Console.
12. Site structure: logical folders, nav reaches every money page.
13. Crawl depth: money pages within 3 clicks.
14. Orphan pages: no internal links in. How: sitemap URLs minus linked URLs.
15. Speed and Core Web Vitals (Lighthouse, CrUX): thresholds above.
16. hreflang (only if multilingual).
17. http to https resource links (mixed content).
18. Mobile friendly at 390px (mobile-first indexing).

### On-page (10)
19. Missing titles and metas.
20. Too long: title 50-60 (up to about 65 ok), meta 120-160, focus keyword in title.
21. SEO-unfriendly URLs: short, lowercase, hyphenated, descriptive, evergreen.
22. Thin content and intent mismatch (under about 500 words on money pages; page does not match what the SERP rewards).
23. Internal links: 2 to 3 valuable links per page, descriptive anchors.
24. Broken internal and external links.
25. Missing or multiple H1; one H1 with the focus keyword.
26. Heading hierarchy: no skipped levels.
27. Schema present, valid, correct type (references/technical.md matrix).
28. Image alt text and filenames: plain language, keyword only if natural, decorative blank.
(Local business listing data: N/A unless the org has locations.)

### Off-page (1)
29. Backlink profile audit: referring domains, anchors, toxic or high-spam links into a disavow file.

### UX / CRO (11, label every finding "CRO, optional")
30. HTML tags for structure. 31. Body text 16px min, ideally 18px. 32. Contrast 4.5:1 (3:1 bold and links). 33. Clear anchor text. 34. Video and audio captions or transcripts. 35. Can pause or mute autoplay. 36. Consistent menu order. 37. Copy states benefits and USPs. 38. Calls to action clear. 39. Descriptive copy. 40. Orphan words and layout at 390px.

## Platform-specific checks
Add the org profile's "known live-site issues" and platform checks (staging indexed, template defaults, widget-injected schema, placeholder text in raw HTML, UTM canonicalization, query strings dropped by redirects). Re-check every item after template edits.

## Technical Task Tracker (columns)
ID | Priority (P1/P2/P3) | Checklist item # | Issue | Affected URLs (count + list or template) | Why it matters | Exact fix | Owner | Status (Open / PR open / Approved / Live / Verified) | Date found | Date verified live | Notes
Sort by priority then URL count. Fix by template (blog post, video, case study, author) before one-off pages.

## Output of an audit
1. Summary: grades by category, top 5 fixes by impact.
2. Tracker rows.
3. A diff-ready fix per row (references/technical.md).
Findings use this shape, tied to a page or asset:
```text
[HIGH] Duplicate title tags on product pages
Location: src/routes/products/[slug].tsx
Issue: Dynamic titles collapse to the same default string, which weakens relevance and creates duplicate signals.
Fix: Generate a unique title per product using the product name and primary category.
```
Severity: HIGH blocks indexing or ranking; MEDIUM weakens relevance; LOW hygiene.

## Anti-patterns
| Anti-pattern | Fix |
|---|---|
| keyword stuffing | write for users first |
| thin near-duplicate pages | consolidate or differentiate them |
| schema for content that is not actually on the page | match schema to reality |
| content advice without checking the actual page | read the real page first |
| generic "improve SEO" outputs | tie every recommendation to a page or asset |
| hand-typed grades or placeholders | tick only with evidence |
