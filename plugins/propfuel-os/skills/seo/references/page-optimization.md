# Optimize an existing page: Outline & Article

Two steps. Outline = research (keywords, competitors, headings, structure). Article = the written content filled into the outline. Deliver both. The brief must be AI-executable: every recommendation is exact old text to exact new text per element (a brief written for a human writer leaves the H1 unchanged). Claude drafts both, the approver reviews the diff.

## Brief template (one doc per page, named "<Page> - Outline & Article - <Org>")
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
| Schema Mark Up | type list (fill it from the matrix in references/technical.md) |

### 2. Keyword Research table
Type (Focus / Secondary) | Keyword | SV | Instances (count in the live body) | Actual (count after the rewrite) | Status ("No Instances" until used). Every focus and secondary keyword appears at least once in the body, naturally, not stuffed.
Focus SV and Secondary SV come from the keyword map (references/keyword-research.md).

### Targeting details
- Target Product/Solution.
- Target Persona: one sentence naming who searches and what they want to do.
- Target Word Count: min 500 words for existing pages.

### Internal Link Recommendations
Anchor Text | Page URL | Status. 2 to 3 links per page, descriptive anchors.

### LLM Reverse Engineering Insights (how to do it)
1. Ask the page's core question in an LLM or WebSearch ("what should a renewal campaign include?").
2. Note what the answers emphasize (themes, named tools, structure) and which sources they cite.
3. Write one paragraph: "LLMs emphasize X, Y, Z and cite A, B." Then make the page cover those themes with quotable, subject-first sentences.

### Competitor references
1 to 3 URLs of pages that rank for the focus keyword. Note what they cover that this page does not.

### Style guide
"N/A" unless the page needs one. Content writing standard: fonts and headings, spacing, bullets, TLDR, answer-first formatting, personalization, tone Do and Don't, ethical AI use, review and approval, keywords, internal linking with noticeable anchor text, external references, CTAs. Writer verifies every claim.

### Writing scope for existing pages
Light (meta and H1 only) / Moderate (retag headings, add sections, FAQs) / Heavy (rewrite). Default Moderate.

### Content Outline: two-column table "Existing | Recommended"
Walk the live page section by section. First row always: "Overall: ensure important text and images are not in JS (static HTML, native CMS elements)". Typical recommended actions:
- Retag: a label `<p>` to `<h2>`; a big display line `<h2>` to `<p>` (same classes, same look); card names `<h4>` to `<h3>`.
- Rename a section to name the mechanism (replace "Welcome to X" with what the thing does).
- Replace abstract copy with the mechanism: one step, one result, what happens next.
- Name the audience; add a differentiator line under the buttons.
- Make CTAs specific. Label any button-wording change as CRO.
- Add proof (named client stat from an approved source) and third-party proof only if real.
- FAQs: add 3 to 5 buyer questions (cost structure, data handling, support during setup), cut or merge duplicates.
- Add a keyword-bearing H2 section linking sibling pages.
- Add time to value only if an owner page states it.
- End with a direct-ask CTA.
For each row also write the exact new text (the Article tab holds it).

### 4. Written Article tab
H1 / Meta Title / Meta Description, then the full body with HTML tag labels per element (eyebrow `<p>`, section H2, H3 cards), buttons, design notes for the developer, FAQ (answer in HTML `<details>` plus native FAQPage JSON-LD), proof placeholders as `{{number}}`.
Color legend: yellow = new or edited text; red strikethrough = removed; green = primary keyword; blue = secondary keyword.

## Metadata + H1 sheet (the batch version for all pages)
Columns: Page | URL | Assigned Status | Focus Keyword(s) | Title Old | Title New | Title chars | Description Old | Description New | Description chars | H1 Old | H1 New | Internal Linking (checkbox) | CTA (checkbox). Two rows per page (labels, values); sections "Core Pages" and "Blog Pages"; new pages marked "*new page"; "Remained" = keep. Update Assigned Status when shipped (it goes stale). The approver marks "approved" to push live.

## Title, meta, heading rules
- Title: 50 to 60 characters (up to about 65 accepted). Primary keyword or concept near the front, in Title Case. Legible to humans, not stuffed. Brand suffix only if it fits. Formula: `Primary Topic - Specific Modifier | Brand`.
- Meta description: 120 to 160 characters. Lead with a benefit sentence, then the keyword. Describe the page honestly. Formula: action + topic + value proposition + one supporting detail. Over 160 gets trimmed in results.
- No stat in a meta that is not on the page and sourced.
- One H1 with the focus keyword (unless the profile's brand rule says otherwise). H1 pattern: keyword phrase + brand line.
- H2 and H3 reflect the real content hierarchy; do not skip levels for visual styling. H2s descriptive, keyword-bearing; FAQ H2 "Questions About ..." or "<Topic> FAQs".
- FAQs: 4 to 6 (5 to 7 on use-case pages), each `<h3>`, answers in HTML, mirrored as native FAQPage JSON-LD, word for word. FAQPage only when the content truly is Q&A.
- 2 to 3 internal links with descriptive anchors (avoid "click here").
- Every claim has a named source from the profile's allow-list; else drop it.

## Change-log format (write one per page batch)
Header: Page | CMS page id | Source brief | Date | Status | Code PRs.
Sections:
1. "How it was implemented": native vs script, in two lines.
2. Per section: table Before | After | Why. Quote exact text.
3. Keyword coverage table: Keyword | Instances | Where. Word count vs minimum.
4. Flags: items skipped with reasons, decisions needed from the approver.
5. Process notes (anything surprising, e.g. someone else published mid-edit).
6. Verification (served HTML, JSON-LD, links, 1440 and 390 screenshots).
7. Rollback (code revert; CMS backup timestamp).
Skipped items always carry the reason (claim not in the allow-list, cannot be confirmed, belongs to sales or legal).

## Worked examples
PropFuel examples (titles, H1s, metas, a heading retag, a meta claim removed for failing the allow-list) are in org/propfuel.md. Pattern: say the before text, the after text, and why in one line.
