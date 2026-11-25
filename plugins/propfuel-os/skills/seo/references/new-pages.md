# New pages

## New page vs optimize
Optimize when a live page already owns the intent (or can). Build new when: the keyword cluster has no page (e.g. "member survey" cluster, about 320 combined volume, no page); an audience (trade or professional) searches differently; a high-value query pattern needs its own page (an AMS integration). Never create a second page for a term an existing landing page owns.
Run the brief first (references/page-optimization.md, Page Type = New Page), then build.

## Patterns already built (copy the structure)
Generated pages come from `~/Projects/propfuel-page-previews/src/mamba-system` (`build.mjs`, `solutions.mjs`, `usecases.mjs`, `system.css`, `usecase-data.json`): one shared `.mm` UI system, CSS-only motion, no new runtime JS. Output: `embed-static.html` (self-contained, pastes into a native Webflow Code Embed so the copy is in served HTML), `og.jpg`, per-page meta JSON with the JSON-LD @graph.

### Solutions hub (/solutions)
Hero (eyebrow, H1 "Built for associations. Every kind, every size.", sub, "Get a Free Demo", link to case studies, trust line) > problem (0.98% stat) > core idea (Attract / Engage / Retain, each linking a use case) > strategy (link to data-intelligence) > "What PropFuel does, and what your AMS does" (link /integrations) > your audience (two cards to the audience pages) > proof (named client results) > FAQ (5 Qs, links to both audience pages) > CTA ("Know and Grow Your Membership.").
JSON-LD @graph: WebPage, FAQPage (add BreadcrumbList: missing today).

### Trade and Professional association pages
Hero with breadcrumb ("Solutions / Trade Associations"), H1, sub, CTA plus anchor CTA > problem reframed ("The person who pays the dues isn't the person using the benefits." / "Career value changes. Most member communication doesn't.") > segmentation (trade: roles at a member company; professional: career stages) > two topic sections tied to the audience's jobs (trade: advocacy and policy input, trade shows and events; professional: credentials and continuing education, chapters and volunteers) > results, dark (NACUBO, TXCPA, ARN, from the Help Center) > FAQ (4 Qs, link /integrations) > CTA to /solutions, /book-a-demo and a related use case.
Rule: every body section links to the use case or case study it summarizes, keyword anchor text. Each audience page links up to /solutions and sideways to the other. Breadcrumb Home > Solutions > page.

### Use-case revamp section pattern (7 pages)
1 Hero: eyebrow, H1, sub, "Get a Free Demo", secondary anchor naming the centerpiece ("See the Two Tracks"), optional note under buttons.
2 Problem: H2 phrased as a customer pain sentence; 3 to 5 paragraphs, one bolded line.
3 Centerpiece (anchor target): the process as steps, tracks, phases or stages.
4 "Four Engines Working Together to ..." (H3 per engine, each linking its engine page).
5 "Built to Work With Your AMS" (win-back, acquisition).
6 Proof: "Proof That Conversations ..." with 3 to 4 stat cards, each linking a named case study.
7 FAQ: H2 "Questions About ...", 5 to 7 questions as H3, mirrored as FAQPage JSON-LD.
8 CTA: short imperative H2 ("Bring them back."), primary demo, secondary adjacent use case.
Add FAQs for keyword coverage (e.g. "Which member engagement metrics should we track?").

## Placement rule
New audience pages sit under the Use Cases nav dropdown, above the direct product use cases, as 2 mini cards (like Membership AI above Solutions and Tools in the Platform dropdown); the Solutions row is a featured full-width item. Ship the nav items hidden until HEAD requests to all new paths return 200 (`?pfsol=1` forces preview), so there are never dead links.

## Proposed but unbuilt (backlog)
1. Integration page per AMS (Salesforce, Novi, iMIS, Nimble AMS, Fonteva, etc.), target "member engagement platform that integrates with <AMS>". Alex: "so freaking important" for prospects. Model: Memberful's per-integration pages. Include walkthrough, case study, what writes back, what does not (only claims that are true: write-back "where your AMS supports it"). Cluster: ams integration (pos 5), association management software integration, imis / salesforce AMS terms.
2. /use-cases/feedback (member survey cluster, about 320 combined). Outline exists: H1 + hero; the problem (annual long surveys fail); satisfaction surveys; interest surveys; exit surveys; feedback-tool checklist; "From answers to action" (ask, capture, act; "you said, we did"); proof; 6 FAQs; CTA. Min 500 words. Currently a 404 that other pages linked to (links repointed to the satisfaction-data blog post).
3. Best-AMS listicle with the integration angle (50+ AMS integrations, about 90% of the market). The one allowed AMS-adjacent post.
4. Mamba's later docs still pending as of Nov 25: Website, SMS, Integrations optimizations; Membership AI, Insight, Automation Engine, Engagement Engine, Email pages ready for review.

## Templated section library (for fast builds)
Hero (centered with CTAs; split with form); social proof (static logo bar, stats bar, single large testimonial, case-study card); features (50/50 image-text left and right, 4-column icon grid, product screenshot, comparison table, how-it-works 3 steps, unique feature); conversion (full-width banner, split banner, contact form, demo form, newsletter bar, pricing tiers); content (FAQ accordion, blog card grid); integrations (scrolling logo bar, grouped "works with your stack"); team and company (bio page, values grid, mission and vision, timeline). 15 to 17 sections are enough; new pages are copy-paste builds. Every section is native HTML.
