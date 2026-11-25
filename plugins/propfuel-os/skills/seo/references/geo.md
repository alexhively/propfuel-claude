# GEO / AEO (AI search visibility)

GEO is SEO with prompt selection. Same execution, different choice of what to track. AI engines run Google searches in real time and cite what ranks, so ranking on Google stays the mechanism.

## 5-step workflow
1. Choose concise prompts (target about 40 to 50; 33 are approved) and tag each with a cluster.
2. Run them in the visibility tool: visibility and sentiment per prompt across ChatGPT, Gemini, Claude, Perplexity.
3. Pull the top-cited domains across all prompts.
4. Split them: on-page (listicle and guide content PropFuel owns: "best X", "top 10 X") vs off-page (third-party review and forum sites where PropFuel needs presence).
5. Monitor. Lock the prompt list early: there is no history, so the first run is the clean baseline.
Limits: no search-volume data for prompts; approximate by mapping each prompt to its closest SEO keywords and summing their volume.

## Prompt-writing rule
Take a high-volume keyword cluster and reword it as the natural-language question a buyer asks an LLM, with "associations" in it. Each prompt gets a "why we track it" tied to a page or product. One Key Prompt per cluster.

## The 33 approved prompts (approved Nov 23; location US; volume = summed keyword volume)
Cluster 1 Member Engagement Platform
1 (KEY, 1,020) What is the best member engagement software for associations?
2 (300) Which member engagement solutions work best for a small association with a small staff?
3 (610) What tools can help an association increase member engagement?
4 (490) What software do associations use to run their member engagement strategy?
5 (110) What are the best member engagement platforms for trade associations?
6 (430) What platforms help associations improve the member experience?
7 (60) What are the best member engagement apps for membership organizations?
Cluster 2 Member Retention + Renewals
8 (KEY, 580) What is the best member retention software for associations?
9 (800) What tools help associations improve membership retention?
10 (85) What is the best software to automate membership renewals for an association?
11 (90) Which AI tools can automate membership renewal outreach for associations?
12 (140) What are the best tools for associations to win back lapsed members?
13 (70) Which platforms help associations with both member engagement and retention?
Cluster 3 Member Acquisition + Onboarding
14 (KEY, 200) What is the best new member onboarding software for associations?
15 (110) What tools help associations automate the new member onboarding process?
16 (150) What are the best membership acquisition tools for associations?
17 (880) What software helps associations recruit and attract new members?
Cluster 4 Member Communication
18 (120) What is the best member communication software for associations?
19 (60) Which platforms let associations send personalized email and SMS messages to members?
Cluster 5 Member Feedback + Data
20 (330) What are the best member survey and feedback tools for associations?
21 (60) What tools help associations measure and report on member engagement?
22 (180) What tools help associations keep member profile data up to date?
Cluster 6 AMS Integration
23 (KEY, 180) What are the best member engagement tools for associations that already use an AMS?
24 (170) What tools do associations use alongside their AMS for member communication and engagement?
25 (460) AMS vs member engagement platform: what is the difference and which does my association need?
26 (90) Which member engagement platforms integrate with iMIS or a Salesforce-based AMS?
Cluster 7 Events + Programs
27 (90) What are the best tools to increase association event registration and attendance?
28 (20) What platforms help associations promote certifications and continuing education to members?
Branded (check facts and sentiment)
B1 What is PropFuel and how does it help associations?
B2 Is PropFuel a good member engagement platform for a small association?
B3 How much does PropFuel cost? (AI answers on price are often wrong; flags what to fix)
B4 PropFuel vs Higher Logic: which is better for association member engagement?
B5 Which association management systems does PropFuel integrate with?
Sheet columns: # | Prompt | Cluster 1 | Cluster 2 (Key Prompt flag) | Location | Keywords behind it | Searches / month | Why we track it | Approval | PropFuel notes.

## HubSpot AEO setup (25 free prompt slots; unconfigured as of 2026-11-25)
Load in this order, then record the date as the baseline:
1. Key Prompts #1, #8, #14, #23 plus B1 (is the brand described correctly).
2. Remaining branded: B2, B3, B4, B5.
3. Highest-volume non-branded, then the rest by value.
The 25: 1, 8, 14, 23, B1, B2, B3, B4, B5, 9, 17, 3, 4, 6, 20, 25, 2, 5, 12, 10, 11, 22, 24, 27, 15.
Left out (8): 7, 13, 16, 18, 19, 21, 26, 28. Track those by manual WebSearch runs monthly.
Use: `manage_aeo_prompts` to add, `get_aeo_metrics` to read visibility, citations and sentiment per prompt, `manage_aeo_recommendations` for suggestions. Webflow AEO (`data_aeo_tool`) is not entitled on this plan: do not rely on it. Without HubSpot data, run prompts by hand in WebSearch and record whether PropFuel is named and which domains are cited.

## KPI funnel
- Top: retrievals (the LLM fetched a page) and citations (the page was used in the answer). They can diverge. Use them to reverse-engineer what the LLMs favor.
- Middle: visibility (% of runs where the answer references PropFuel), per prompt, per LLM, plus sentiment.
- Bottom: referral traffic from LLMs (PostHog AI-assistant referrals, GA4) and AI-referral conversions.
Also track Google AI Overviews / AI Mode impressions from GSC (Jul 1,065; Aug 1,183; Sep 1,382; Oct 4,991, mostly a brand spike after Oct 12).

## Technical GEO
Static HTML for every heading, FAQ and stat; native JSON-LD matched to visible content; llms.txt current; markdown alternates reachable; no animation-only sections (hover menus are invisible to AI crawlers); clean H1 and heading order; descriptive alt text. Sentences start with a subject so they can be quoted. Include copy-and-paste lists (question sets, checklists): AI answers favor them.

## On-page vs off-page split
- On-page (we own): use-case and solutions pages, blogs, "best X" listicles with the association angle, Blueprint and template pages.
- Off-page (third party): G2 and review sites where data shows citations, Associations Now / ASAE, partner and integration pages. Only pursue where cited.

## Blueprints and templates as GEO substance
The Use-Case Blog Kit and Blueprints (member acquisition campaign template, member renewal campaign template) answer "build me a campaign" prompts. Publish them as template pages and posts with copyable questions and email wording, linked to the matching use-case page (references/blog-and-templates.md). Priority prompt themes from Alex (Oct 29): member engagement strategy (professional-association persona) and email campaign templates and outlines.

## Competitor visibility
Run the same prompts with competitor domains (MemberNova, Higher Logic Thrive, Feathr, Tradewing) to see who gets cited. Alex finds "which competitors get shown today" valuable.
