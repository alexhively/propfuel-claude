# Optimize an existing page: Outline & Article

Two steps. Outline = research (keywords, competitors, headings, structure). Article = the written content filled into the outline. Deliver both. The brief must be AI-executable: every recommendation is exact old text to exact new text per element (Oct 1 lesson). Claude drafts both, Alex reviews the diff.

## Brief template (one doc per page, named "<Page> - Outline & Article - PropFuel")
Title: "Content Outline | Page Title: <H1>". Sections: 1 Meta Data and SEO Elements; 2 Guidelines; 3 Content Outline; 4 Written Article [For Client Review]; 5 Content Guidelines.

### 1. Title & Meta Data table
| Field | Value |
|---|---|
| Page Type | Existing Page / New Page |
| Page Title (H1) | |
| Meta Title | |
| Meta Description | |
| SERP Intent | e.g. Transactional |
| Keyword Intent | e.g. Commercial |
| Schema Mark Up | type list (blank in Mamba's briefs; fill it) |

### 2. Keyword Research table
Type (Focus / Secondary) | Keyword | SV | Instances (count in the live body) | Actual (count after the rewrite) | Status ("No Instances" until used). Every focus and secondary keyword appears at least once in the body, naturally, not stuffed.
Focus SV and Secondary SV come from the keyword map (references/keyword-research.md).

### Targeting details
- Target Product/Solution.
- Target Persona: one sentence, e.g. "People looking for membership renewal solutions who want to identify at-risk members, understand renewal concerns, automate personalized campaigns, and improve renewal rates."
- Target Word Count: min 500 words for existing pages (shipped pages ran about 1,100 to 1,550).

### Internal Link Recommendations
Anchor Text | Page URL | Status. Examples that shipped: "Reads from your AMS" -> /integrations; "success stories" -> /client-success/case-studies; "prepare for renewal" -> /use-cases/renewals; "win back lapsed members" -> /use-cases/win-back; "Retention starts at onboarding" -> /use-cases/onboarding. 2 to 3 links per page.

### LLM Reverse Engineering Insights (how to do it)
1. Ask the page's core question in an LLM or WebSearch ("what should a membership renewal campaign include?").
2. Note what the answers emphasize (themes, named tools, structure) and which sources they cite.
3. Write one paragraph: "LLMs emphasize X, Y, Z and cite A, B." Then make the page cover those themes with quotable, subject-first sentences.
Example (Renewals): personalized communication, engagement tracking, automation, churn prevention, member analytics, targeted campaigns, feedback, renewal management.

### Competitor references
1 to 3 URLs of pages that rank for the focus keyword (competitor set in keyword-research.md). Note what they cover that PropFuel's page does not.

### Style guide
"N/A" unless the page needs one. Content writing standard (Mamba's live guideline, now ours): fonts and headings, spacing, bullets, TLDR, answer-first formatting, personalization, tone Do and Don't, ethical AI use, review and approval, keywords, internal linking with noticeable anchor text, external references, CTAs. Writer verifies every claim.

### Writing scope for existing pages
Light (meta and H1 only) / Moderate (retag headings, add sections, FAQs) / Heavy (rewrite). Default Moderate.

### Content Outline: two-column table "Existing | Recommended"
Walk the live page section by section. First row always: "Overall: ensure important text and images are not in JS (static HTML, native Webflow)". Typical recommended actions (copy the style):
- Retag: "The Problem" label `<p>` to `<h2>`; the big display line `<h2>` to `<p>` (same classes, same look); engine names `<h4>` to `<h3>`.
- Rename a section to name the mechanism: "Welcome to PropFuel" to "The Membership Engagement Loop".
- Replace abstract copy with the mechanism: one question, one click, lands on the profile, triggers the next action.
- Name the audience; add a differentiator line under the buttons ("Works alongside your existing renewal emails").
- Make CTAs specific ("Explore Insights Engine"). Label any button-wording change as CRO.
- Add proof (named client stat from the Help Center) and third-party proof only if real.
- FAQs: add 3 to 5 buyer questions (cost structure, data handling, support during setup), cut or merge duplicates.
- Add a keyword-bearing H2 section (e.g. "Member Retention Strategies Before the Renewal Notice") linking sibling use cases.
- Add time to value ("first campaign live in 2 to 3 weeks") only if the Implementation page says so.
- End with a direct-ask CTA ("Bring your AMS. We'll show you what your members are already telling you.").
For each row also write the exact new text (the Article tab holds it).

### 4. Written Article tab
H1 / Meta Title / Meta Description, then the full body with HTML tag labels per element (eyebrow `<p>`, section H2, H3 cards), buttons, design notes for the developer, FAQ (answer in HTML `<details>` plus native FAQPage JSON-LD), proof placeholders as `{{number}}`.
Color legend: yellow = new or edited text; red strikethrough = removed; green = primary keyword; blue = secondary keyword.

## Metadata + H1 sheet (the batch version for all pages)
Columns: Page | URL | Assigned Status | Focus Keyword(s) | Title Old | Title New | Title chars | Description Old | Description New | Description chars | H1 Old | H1 New | Internal Linking (checkbox) | CTA (checkbox). Two rows per page (labels, values); sections "Core Pages" and "Blog Pages"; new pages marked "*new page"; "Remained" = keep. Assigned Status must be updated when shipped (it went stale). Alex marks "approved" to push live.

## Rules derived from what shipped
- Title: 50 to 60 characters (up to ~65 accepted), keyword phrase first in Title Case. Brand suffix only if it fits.
- Meta description: 140 to 160 characters. Lead with a benefit sentence, then the keyword. Shipped ones that ran 169 to 187 are too long: trim.
- One H1 with the exact focus keyword, unless the brand tagline rule applies: /platform/overview keeps "Know and Grow Your Membership" as H1 (keyword carried by title, meta and hero sub). Homepage H1 is "Member Engagement Platform for Associations" with the tagline as eyebrow.
- Pattern for H1: keyword phrase + brand line ("Member Engagement Engine. More Engagement. Less Silence.").
- H2s descriptive, keyword-bearing, Title Case where they are section names; FAQ H2 "Questions About ..." or "<Topic> FAQs".
- FAQs: 4 to 6 (5 to 7 on use-case pages), each `<h3>`, answers in HTML, mirrored as native FAQPage JSON-LD, word for word.
- 2 to 3 internal links with descriptive anchors. Bottom CTA duplicated on old pages. Hero CTA "Get a Free Demo"; secondary CTA scrolls to the page's centerpiece section by id.
- No stat in a meta that is not on the page and sourced.
- Every claim has a named source in the OS master docs or Help Center; else drop it.

## Change-log format (what PropFuel used; write one per page batch)
Header: Page | Webflow page id | Source brief | Date | Status | Code PRs.
Sections:
1. "How it was implemented": native Webflow vs script, in two lines.
2. Per section: table Before | After | Why. Quote exact text.
3. Keyword coverage table: Keyword | Instances | Where. Word count vs minimum.
4. Flags: items skipped with reasons, decisions needed from Alex.
5. Process notes (anything surprising, e.g. someone else published mid-edit).
6. Verification (served HTML, JSON-LD, links, 1440 and 390 screenshots).
7. Rollback (JS revert; Webflow backup timestamp).
Skipped-item examples with reasons: "No credit card required" (B2B demo, irrelevant); "15-minute demo" (discovery call is 45 minutes); "See it working with your AMS data" (cannot confirm); official G2 badge (must be earned and exported from G2; added a "Verified reviews on G2" link instead); pricing dollar figures (sales and leadership call; explained the structure only).

## Worked examples
1. Homepage meta and hero. Title before: "AI-Powered Member Engagement Platform | PropFuel". After: "Powerful AI-Powered Member Engagement Software & Platform" (57; suffix dropped to stay under 60; both focus keywords in). Description after: "PropFuel is a member engagement platform that helps associations understand what members truly want, turning insights into stronger retention and lasting revenue." H1 after: "Member Engagement Platform for Associations". Why: the focus keywords were absent from title and H1.
2. Onboarding H1 and title. H1 before "The retention conversation starts the day a member joins." After "Member Onboarding Starts the Retention Conversation." Title before "Automate New Member Onboarding Journeys | PropFuel", after "New Member Onboarding & Engagement Software for Associations". Meta claim "drive 3x engagement in the first 60 days" removed (unsourced); now "personalized check-ins across the first year, enrolled from your AMS". Why: keyword in H1, claim had no source.
3. Heading retag (homepage Problem section). "The Problem" `<p>` to `<h2>`; "Your data isn't up to date." `<h2>` to `<p>`. Why: one clear H2 per section instead of three H2 fragments; styling identical.
4. Renewals meta. Before: "recovering $320K+ in at-risk revenue" (unsourced). After: "adaptive campaigns that start 60 days before expiration". Why: stat failed the facts allow-list.
