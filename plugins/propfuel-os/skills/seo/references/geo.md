# GEO / AEO (AI search visibility)

GEO is SEO with prompt selection. Same execution, different choice of what to track. AI engines run Google searches in real time and cite what ranks, so ranking on Google stays the mechanism.

## 5-step workflow
1. Choose concise prompts (target about 40 to 50) and tag each with a cluster.
2. Run them in the visibility tool: visibility and sentiment per prompt across ChatGPT, Gemini, Claude, Perplexity.
3. Pull the top-cited domains across all prompts.
4. Split them: on-page (listicle and guide content the org owns: "best X", "top 10 X") vs off-page (third-party review and forum sites where the org needs presence).
5. Monitor. Lock the prompt list early: there is no history, so the first run is the clean baseline.
Limits: no search-volume data for prompts; approximate by mapping each prompt to its closest SEO keywords and summing their volume.

## Prompt-writing rule
Take a high-volume keyword cluster and reword it as the natural-language question a buyer asks an LLM, including the qualifier from the profile. Each prompt gets a "why we track it" tied to a page or product. One Key Prompt per cluster. Add a few branded prompts (is the brand described correctly, price, comparisons, integrations) to fact-check AI answers.
Sheet columns: # | Prompt | Cluster | Key Prompt flag | Location | Keywords behind it | Searches / month | Why we track it | Approval | Notes.
Example (PropFuel): "What is the best member engagement software for associations?" The tracked list lives in the profile.

## Tool setup
Load prompts in this order, then record the date as the baseline: Key Prompts plus the brand-description prompt; remaining branded prompts; highest-volume non-branded, then the rest by value. If the tool has a slot cap, track the rest by manual monthly runs. Without a tool, run prompts by hand in WebSearch and record whether the brand is named and which domains are cited. Check the plan is entitled to any platform-native AEO feature before relying on it.

## KPI funnel
- Top: retrievals (the LLM fetched a page) and citations (the page was used in the answer). They can diverge. Use them to reverse-engineer what the LLMs favor.
- Middle: visibility (% of runs where the answer references the brand), per prompt, per LLM, plus sentiment.
- Bottom: referral traffic from LLMs (analytics AI-assistant referrals) and AI-referral conversions.
Also track Google AI Overviews / AI Mode impressions from Search Console, and separate brand spikes from organic growth.

## Technical GEO
Static HTML for every heading, FAQ and stat; native JSON-LD matched to visible content; llms.txt current; markdown alternates reachable; no animation-only sections (hover menus are invisible to AI crawlers); clean H1 and heading order; descriptive alt text. Sentences start with a subject so they can be quoted. Include copy-and-paste lists (question sets, checklists): AI answers favor them. Keep AI bots allowed in robots.txt unless the org decides otherwise.

## On-page vs off-page split
- On-page (we own): use-case and solution pages, blogs, "best X" listicles with the niche angle, template pages.
- Off-page (third party): review sites where data shows citations, trade media, partner and integration pages. Only pursue where cited.

## Templates as GEO substance
Template kits answer "build me a <campaign>" prompts. Publish them as template pages and posts with copyable questions and wording, linked to the matching use-case page (references/blog-and-templates.md).

## Competitor visibility
Run the same prompts and note which competitor domains (from the profile) get cited. Report "who gets shown today".
