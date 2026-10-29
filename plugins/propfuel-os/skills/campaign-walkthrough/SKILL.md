---
name: campaign-walkthrough
description: Campaign Walkthrough (any use case). Build a prospect-branded 3-page PDF walkthrough of a PropFuel campaign for one association (win-back, renewal, new-member onboarding, member acquisition, events, or other), tailored to the relationship (cold prospecting, no-show / re-engagement, or open-pipeline follow-up), to their industry and member type, their AMS and email system, and what they said on Gong calls. The "Pick a time" button links to the sending rep's Chili Piper. Plus the cover and bump emails. Replaces winback-walkthrough. Use when someone says "campaign walkthrough", "win-back walkthrough", "build me a [win-back / renewal / onboarding] campaign example for [association]", "send them the walkthrough", "the call we missed", "demo no-show asset", or names a Demo Unperformed opp.
---

# Campaign Walkthrough (any use case)

Was **winback-walkthrough** (Sales OTM, Oct 9 2026). Widened at the Sales Team OTM, Oct 15 2026 (Alex, Ryan, Mike, Lisa): "not just the no-show win-back walkthrough, but the any-use-case campaign walkthrough, tailored to prospecting, no-shows and re-engagement, or moving people down the funnel in the pipeline… customize to their industry and value proposition… and if we have context from Gong calls, tailor to their specific needs and pain points."

Output: a 3-page landscape-Letter PDF (the note · the campaign map · the comparison), plus a cover email and a bump. Draft only: the rep reviews and sends. Never email, post or upload anything yourself.

**Offer model (Oct 14 2026):** we build the plan *with* them on a short call and they leave with it. We don't run the campaign for free. Never write "we'll run / send / launch your campaign".

## 1. Read the prompt: use case, context mode, sender

**Use case** (from the prompt; default **win-back** when unclear): `win-back` (lapsed, former members) · `renewal` · `onboarding` (new members, first 4 months) · `acquisition` (recruitment, prospects) · `event` (registration, engagement) · `other`. Maps for each are in `use-cases.md` next to this file.

**Context mode** sets the opening line. Get it right; it is the first thing they read.

| mode | when | the note may say | the note must never say |
|---|---|---|---|
| `cold` (prospecting / outbound) | no opp and no Gong call with us, or the rep says it's cold | a fresh, one-line intro: who the rep is, why we built this for them | "following up", "following back up", "when we last talked", "our call", anything implying we've met |
| `no_show` / `re-engage` | a demo was booked and missed or cancelled (`Demo_Status__c` No Show, Cancelled, Rescheduling), or the opp went quiet | the missed date, no guilt; the scenario lines below | blame |
| `pipeline` (open opp, moving them down the funnel) | an open opp with a performed demo or a recent call | "Following back up on…", a Gong line | invented commitments |

"Following back up" and "when we last talked" appear **only** if Salesforce or Gong shows a real meeting.

**Sender / rep** decides the signature and the Chili Piper link:

| rep | Chili Piper (the button links here) |
|---|---|
| Mike Arisco, Account Executive, mike@propfuel.com — **default** | https://propfuel.chilipiper.com/me/mike-arisco/meeting-with-mike |
| Ryan Graham, Chief Revenue Officer, ryan@propfuel.com — when Ryan is the sender, or Ryan owns the opp | https://propfuel.chilipiper.com/me/ryan-graham/meeting-with-ryan |

Pick from the prompt ("from Ryan"), else the opp owner, else Mike. Any other rep: ask for their Chili Piper link; until you have it, use Mike's and say so. Both links were checked live on Oct 15 2026 (each opens that rep's calendar). Never leave the button without a working `href`.

## 2. Get the facts (read-only)

1. **Salesforce** (Salesforce connector, or `salesforce-account-tool` in PropFuel Super Admin): the account and its latest opp.
   ```sql
   SELECT Id, Name, StageName, Demo_Status__c, First_Demo_Date__c, Demo_Brief_Notes__c, Owner.Name,
          Account.Id, Account.Name, Account.Website,
          (SELECT Contact.FirstName, Contact.Title, IsPrimary FROM OpportunityContactRoles)
   FROM Opportunity WHERE Account.Name LIKE '%<name>%' ORDER BY CreatedDate DESC LIMIT 5
   ```
   Contact = primary contact role's first name (or who the rep names). Meeting date = `First_Demo_Date__c`, written "Tuesday, Oct 13" (check the weekday).
2. **Gong** (`gong-call-search-tool` with `salesforce_account_id`, then `gong-call-detail-tool`; or the Gong connector's `ask_account`). From the most recent sales call's insights take: their **AMS and email/marketing system** (`tech_stack`), and **one or two real stated needs or pain points** (`problems_to_solve`, `pain_points`, `goals_and_jtbd`).
3. **Their website** (or what you know of the org): the member type, the profession, the flagship benefits, and their value proposition in their own words.

### The Gong line (page 1, optional)

One or two sentences, in the note after the opening line, in the rep's voice:
- Use their words. Quote only a phrase that is in the Gong insight or transcript ("dumping information"); paraphrase the rest plainly. Never invent a need, a number or a quote.
- Attribute carefully: "you said" only when the insight or transcript puts the words in that contact's mouth; otherwise "your team said" (and only if someone from their side was on the call).
- Date it: call within the last 9 months → "When we talked on Sep 3, you said…". Older than 9 months → "When we talked a while back, you mentioned…".
- No Gong call → leave the line out (delete the `[GONG LINE]` paragraph). Never fill it from guesswork. `cold` mode never has a Gong line.
- Put the call's title and date in the companion file's source line so the rep can check it.

## 3. Tailor

- **Write for the member type.** Every question on page 2 is written the way their members talk. Bar association: "Have you joined a section yet?", CLE. Medical society: specialty sections, CME, advocacy, practice resources. Trade association: committees, the company membership, the primary contact. AMC (association management company): frame it as "for your client associations", build once and copy it to the next client with their branding (AMC-BRAIN: "do this for your client association").
- **Their value proposition:** one clause in the note ties the campaign to what they say they do for members (from their site or Gong). No claims about their numbers: we don't have them.
- **Their systems, named on page 3:** `[EMAIL SYSTEM]` = their email/marketing tool when known ("Salesforce Marketing Cloud"), else "HubSpot or Mailchimp". `[EMAIL SYSTEM LINE]` = "Salesforce Marketing Cloud, the way most teams set it up" or the default "Mailchimp, HubSpot, Constant Contact or your AMS's email tool". `[AMS]` = their AMS when known ("Salesforce"), else "your AMS"; pills on page 2 can read "Saved to Salesforce". Only name a system that Salesforce or Gong actually shows.
- **Brand colour / logo:** only from their own site. Otherwise keep PropFuel orange.

## 4. Fill the template

`walkthrough-template.html` (next to this file) ships filled with the win-back map and the `no_show` copy. Replace every bracketed field and swap the use-case blocks from `use-cases.md`:

- **Page 1:** eyebrow, headline, `[OPENING LINE]` paragraph, `[GONG LINE]`, `[USE CASE PHRASE]`, `[STANDARD SEQUENCE NAME]`, `[SHORT VERSION]` (one plain sentence: what a standard email tells you vs what this tells you), the left box's first line and the PF box's last line, and `[ACTION COUNT]` (count it from your page 2: every pill except "→ next", plus the 3 running items).
- **Page 2:** `.when` labels, the four `.colm` blocks (question, choices, answer rows and pills), the `.starts` line and the `.always` bar.
- **Page 3:** `[USE CASE]`, the standard-sequence chips and lists, the PropFuel chips, `[EMAIL SYSTEM]`, `[AMS]`, `[REMOVAL RULE]`, the proof box (`[PROOF EYEBROW]`, numbers, one sentence) and the CTA.
- Header/footer: `[FIRST NAME]`, `[DATE]` (today), `[REP NAME]`, `[TITLE]`, `[REP EMAIL]`. Add `class="filled"` to `<body>`.

| mode | eyebrow | headline | opening line | CTA head / sub / button |
|---|---|---|---|---|
| `cold` | Built for {ASSOC} | What {use-case phrase} could look like for **{ASSOC}** | We haven't met yet, so a quick hello: I'm {rep first name}, and I work with associations like {ASSOC} at PropFuel. I built this because {one clause on their value prop / member type}. | Worth 20 minutes to build the real one together? / We'll build the plan with you, live, on {ASSOC}'s own data. You keep it either way. / Pick a time |
| `no_show` | For the call we missed | I built this for **our call**. It's yours either way. | We had {MEETING DATE} on the calendar, so I put this together ahead of time. No worries that it didn't happen. I'd rather you have it than leave it in a folder. | Worth 20 minutes to walk through it together? / Pick any time that works and we'll build this campaign with you on {ASSOC}'s own data. / Pick a new time |
| `cancelled` | Prepared for our call | The walkthrough I had ready for **{MEETING DATE}** | I know {MEETING DATE} didn't work out. I'd already built this for our conversation, so I wanted you to have it. | When the timing is better, I'll walk you through it / Twenty minutes, on {ASSOC}'s own numbers. / Pick a new time |
| `pipeline` | Following back up | Your {use case} plan, built for **{ASSOC}** | Following back up on our conversation{ on DATE}. I mapped out what {use-case phrase} would look like for {ASSOC}, so your team has something concrete to react to. | Ready to build the real one together? / Twenty minutes: we build the plan with you on {ASSOC}'s own data. / Pick a time |

The CTA is `<a class="btn" href="{rep's Chili Piper URL}">`. It stays a real link in the PDF.

### Render

- **Claude Code:** `node ~/Projects/propfuel-content-repurposer/scripts/render-pdf.mjs <file>.html <file>.pdf` (Puppeteer; keeps links and backgrounds). Or Chrome: print, landscape Letter, background graphics on.
- **claude.ai:** render the HTML to PDF with a Chromium-based tool if you have one (it keeps the link); otherwise give the HTML file and tell the rep to print it from Chrome (landscape, background graphics on).

## 5. Check before handing over (look at every page)

- Open the PDF and look at all 3 pages: no overflow, nothing cut off, **no single word stranded on a last line** (the template sets `text-wrap: pretty`; if one still strands, trim a word).
- The opening matches the context mode (no "following up" or "when we last talked" without a real meeting; cold gets a fresh intro). The meeting date's weekday is right.
- The Gong line quotes a real call, is attributed and dated correctly, and says "a while back" if older than 9 months.
- The CTA link works: the PDF has a link annotation to the rep's Chili Piper URL (`python3 -c "import fitz;d=fitz.open('x.pdf');print([l['uri'] for p in d for l in p.get_links()])"`).
- Stats: only "370+ associations" and "12% average annual revenue growth after implementing PropFuel". **Never 8.68%.** No invented membership numbers.
- Proof: only a Live case study for the same use case, labelled as published and illustrative, never as a forecast for them. Clients may be named without a live case study.
- The last page's footer says "370+ associations and counting". Tagline: "Know and Grow Your Membership".
- No `[` merge field left. Offer copy says we build it *with* them.
- `log_update` to the Marketing OS (account, use case, mode, file). Don't change the opp.

## 6. Companion emails (one file, plain text, drafts from the rep)

1. **Cover email** (under 80 words). Subject by mode: cold "{ASSOC}: a {use case} campaign, already mapped" · no_show "For the call we missed" · cancelled "{First name}, the walkthrough I had ready" · pipeline "Your {use case} plan, mapped out". One line that matches the mode, one line on what's attached, one proof sentence (only from the Live case study you used), and a tiny ask with the Chili Piper link.
2. **Bump** (day 3–4, same thread): two sentences that point at one question on page 2 and repeat the ask.
3. **Source line** for the rep: Salesforce opp, Gong call title and date used, systems named.
4. **CRM note:** "Campaign walkthrough sent {date}: {use case}, {mode}, cover + bump drafted."

The per-prospect web page (propfuel-winback.vercel.app, `~/Projects/propfuel-winback`) still exists for the win-back `no_show` case; see that repo's README.

## Correction: source = unperformed demo (automated no-show / cancelled / rescheduling) (2026-10-22, Ryan Graham)

**Why (Ryan, Oct 22 2026):** unperformed-demo walkthroughs are now generated automatically for every unperformed demo and sent by Lisa inside the three Amplemarket unperformed-demo sequences. Ryan and Mike both run demos, so the booking link has to be the shared round-robin, not one rep's calendar.

**Rule.** When the source is an unperformed demo (`Demo_Status__c` = No Show, Cancelled or Rescheduling, or the prompt says "unperformed demo" / names a Demo Unperformed opp), this overrides section 1's sender table:

| field | value |
|---|---|
| Chili Piper (the button and every booking link) | **https://propfuel.chilipiper.com/round-robin/unknown-account** (round-robins Mike and Ryan) |
| Sender / signature | Lisa McNeil, Sales Development Representative, lisa@propfuel.com |
| Context mode | No Show → `no_show` · Cancelled → `cancelled` · Rescheduling → `no_show` copy, with the opening line acknowledging their note ("Thanks for letting us know {MEETING DATE} wouldn't work.") |
| Use case | win-back by default, unless Gong or the opp notes name another one |
| Draft-only rule | The automated run publishes the page and passes the link into the sequence. The section 5 checks become a pass/fail gate: on any FAIL, don't send the link. Flag it to Lisa instead. |

Never use Mike's or Ryan's personal Chili Piper link on an unperformed-demo walkthrough. In the section 5 check, confirm the PDF/page link annotation equals the round-robin URL.

## Changelog
- 2026-10-22: unperformed-demo rule (Ryan Graham): shared round-robin Chili Piper link, Lisa as sender, automated pass/fail gate. Written in the OS, merged to git Oct 29.
- 2026-10-15: renamed from winback-walkthrough; any use case, three context modes, industry/value-prop/system tailoring, Gong line rules, clickable Chili Piper CTA (Mike default, Ryan when sender/owner), illustrative-proof label, 370+ end card, no stranded words (Sales Team OTM, Oct 15).
- 2026-10-12: created as winback-walkthrough (Sales OTM, Oct 9).
