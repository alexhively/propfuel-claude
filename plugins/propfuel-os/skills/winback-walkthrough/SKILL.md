---
name: winback-walkthrough
description: Build a prospect-branded "win-back walkthrough" for a PropFuel demo that didn't happen (no-show, cancelled, or a demo request that never booked), plus the emails that carry it. Input is the account name, a Salesforce opportunity/account link, a Gong call, or a PropFuel campaign link. Output is the 3-page walkthrough (the note, the campaign map, the comparison) in the house template, a cover email, a follow-up bump, an optional lateral email, and the web-page draft, using only that account's real Salesforce data and published proof. Use when someone says "win-back walkthrough", "the call we missed", "send them the walkthrough", "demo no-show asset", "they cancelled, send something", or names a Demo Unperformed opp.
---

# Win-back walkthrough

From the Sales OTM, Oct 9 2026 (demo-unperformed playbook; owners Alex + Ryan, rebooks Lisa). When a demo goes unperformed, the rep sends a 3-page PDF "prepared for our call" that shows a lapsed-member win-back *for their association* in PropFuel, next to the flat sequence they send today. It gives value either way and earns the rebook.

**Not this skill:** closed-lost deals and former clients go to Lisa's Amplemarket win-back sequences (System map: "Win-back sequences"). The "win-back" here is the campaign *shown* in the walkthrough, not the sales motion.

Draft only. The rep reviews and sends. Never email, post or upload anything yourself.

## 1. Get the facts (read-only)

Resolve the input to one Salesforce Opportunity and read:

```sql
SELECT Id, Name, StageName, Demo_Status__c, First_Demo_Date__c, Demo_Brief_Notes__c,
       Account.Name, Account.Website, Owner.Name, Owner.Title, Owner.Email,
       (SELECT Contact.FirstName, Contact.LastName, Contact.Title, IsPrimary FROM OpportunityContactRoles)
FROM Opportunity WHERE Id = '<id>'
```

- From a name, match on `Account.Name` and prefer `StageName = 'Demo Unperformed'`. From a Gong link, use the call's account. From a PropFuel campaign link, use that client's account.
- **Scenario** from `Demo_Status__c`: `No Show` → `no_show`. `Cancelled`, `Rescheduling` or `Rescheduled` with no new date → `cancelled`. `Requested - Scheduling`, or no demo date at all → `request`. If the status is `Performed` or `Upcoming`, stop and say the asset doesn't fit.
- **Contact:** first name of the primary contact role. **Rep:** the opp owner's name, title and email. **Meeting date:** `First_Demo_Date__c` written as "Oct 14". Leave the booking link empty unless the rep gives one.
- **Brand colour and logo:** only from their own logo or website. Never guess; the PropFuel orange default is fine.
- If a Gong call or `Demo_Brief_Notes__c` names their AMS, renewal cycle or a pain point, you may add **one** clause to the note on page 1, quoting it as they said it. Never add numbers about their membership. We don't have them, and the page 3 CTA promises to use "their own numbers" on the call.

Ask the user only for what you can't find: who it's for (if the opp has no contact role) and the booking link (optional).

## 2. The walkthrough (3 pages, landscape Letter)

The structure is fixed and every claim on it is pre-verified. Change only the merge fields and the scenario copy.

**Page 1 · The note.** Eyebrow, headline and the opening line come from the scenario (table below). Then this fixed body: "It's what a lapsed-member win-back would look like for {ASSOC} in PropFuel: four short emails, each asking one question…". Signed by the rep. On the right: one standard reminder email (what it does and doesn't do) vs one PropFuel check-in, and **22** automated actions from four one-question emails. 22 is counted from the map: 19 answer actions plus 3 that run the whole time. Recount if you change the map.

**Page 2 · The campaign map.** It's the recently-lapsed win-back from `campaign-walkthroughs.md`:
1. **When they lapse:** "Did you know your membership has expired?" No → renewal link, tagged, saved to AMS. Yes → tagged, saved. No answer → email 2.
2. **One week later:** "Would you like to rejoin {ASSOC}?" Yes → rejoin page, saved. Not sure → staff alerted, tagged warm. No → asks why, reason saved, stops emailing ("Cost" also alerts staff).
3. **Two weeks later:** "Which goal matters most to your career this year?" (Credential · Network · Learning · Job) → matching resource, tagged by interest, saved.
4. **Two weeks later:** "What's holding you back from rejoining?" (Cost · Time · Value · I'm interested in rejoining!) Interested → staff alerted now, rejoin page. Any reason → reason saved, tagged by reason.

Running the whole time: enrolled automatically when the AMS marks a member lapsed; removed the moment they rejoin; rejoins and dues counted.

**Page 3 · The comparison.**
- The same four sends as a standard Mailchimp/HubSpot sequence: what you learn and what doesn't happen.
- The 8 things you'd have to build to replicate it.
- The proof: the published, anonymous case study at https://www.propfuel.com/case-studies/medical-society-lapsed-member-win-back. **42** lapsed members rejoined, **$18,438** recovered in dues in seven weeks, and **72%** of first answers said they didn't know they'd lapsed (72% of 54 respondents). It recovered more than it pays for PropFuel in a year.
- The scenario CTA.

Don't swap in another proof point unless it's a live case study (`get_case_studies`, stage Live) for the same use case. Never name an anonymous client.

| scenario | eyebrow | headline | opening line | CTA head / sub / button |
|---|---|---|---|---|
| `no_show` | For the call we missed | I built this for **our call**. It's yours either way. | We had {MEETING DATE} on the calendar, so I put this together ahead of time. No worries that it didn't happen. I'd rather you have it than leave it in a folder. | Worth 20 minutes to walk through it together? / Pick any time that works and I'll show you this campaign built on {ASSOC}'s own data. / Pick a new time |
| `cancelled` | Prepared for our call | The walkthrough I had ready for **{MEETING DATE}** | I know {MEETING DATE} didn't work out. I'd already built this for our conversation, so I wanted you to have it. | When the timing is better, I'll walk you through it / Twenty minutes, on {ASSOC}'s own renewal numbers. / Pick a new time |
| `request` | Before we talk | What a win-back looks like for **{ASSOC}** | Thanks for asking about PropFuel. Before we find a time, here's the kind of thing we'd walk through together, already set up for {ASSOC}. | Want to see it on your own data? / Twenty minutes, and you leave with a plan whether or not you buy. / Book the walkthrough |

### How to render it

- **In the content repurposer repo** (`~/Projects/propfuel-content-repurposer`): write `output/winback/content/<slug>.json` (fields in `templates/winback/README.md`, plus a `_source` line naming the Salesforce opp). Then run `node scripts/make-winback-asset.mjs output/winback/content/<slug>.json`. You get `output/winback/pdf/<slug>.pdf` and `.html`. The script fails on unfilled fields and reports overflow; fix any overflow before handing it over. Exemplars: `exemplars/winback-walkthrough/`.
- **Anywhere else** (the plugin, claude.ai): fill `walkthrough-template.html` in this skill's folder. Replace every bracketed merge field: `[ASSOCIATION]`, `[FIRST NAME]`, `[DATE]` (today, e.g. "October 12, 2026"), `[MEETING DATE]`, `[REP NAME]`, `[TITLE]`, `[REP EMAIL]` and `[BOOKING LINK]`. If there's no booking link, drop " · [BOOKING LINK]". Swap the page 1 eyebrow, headline and opening line and the page 3 CTA for the scenario (the template ships as `no_show`). Add `class="filled"` to `<body>` to remove the yellow merge highlights. For a long association name (over 34 characters), drop the page 2 title to 16pt. Then print to PDF (landscape Letter, background graphics on), or give the HTML as a file. Check that no `[` merge field is left.

## 3. Companion assets

Write these to `output/winback/<slug>-companions.md` in the repo, or as one file elsewhere. All are drafts from the rep, plain text, no links except the booking link.

1. **Cover email** (sent with the PDF, same or next business day). Subject: "{First name}, the walkthrough I had ready" (`cancelled`) / "For the call we missed" (`no_show`) / "Before we talk: a win-back for {ASSOC}" (`request`). Body under 80 words: one line acknowledging the missed or unbooked call with no guilt, one line on what's attached, one proof sentence (42 rejoined, $18,438 in seven weeks, anonymous medical society), and a tiny ask ("Worth 20 minutes when the timing's better?"). Signed by the rep.
2. **Bump** (day 3–4, same thread). Two sentences. Point at one specific thing on page 2, e.g. "the 'Did you know it expired?' question is the one that brought back 42", and repeat the ask.
3. **Lateral email** (only if Salesforce has a second contact, or the rep names one). For the playbook's "lateral or up the account" step: three sentences in the house cold-email shape (`exemplars/email/PATTERNS.md`, family 1). Name that you'd built this for {first contact}, offer to send it, and keep the ask tiny. Don't attach the PDF unsolicited.
4. **Web page draft.** The rendered HTML is the one-URL-per-prospect page. Don't deploy it; the Vercel version is still a planned build.
5. **CRM note** (one line for the rep to paste on the opp): "Win-back walkthrough sent {date}: scenario {scenario}, cover + bump drafted."

## 4. Check before handing over

- Every fact traces to the Salesforce opp, their website or the live case study. No invented membership numbers, no other client names.
- "370+ associations" if a count comes up; tagline "Know and Grow Your Membership".
- No unfilled merge fields, no overflow, the scenario copy matches `Demo_Status__c`, and the meeting date's weekday is right.
- Run the `brand-qa` skill where it exists (in the repo).
- Log it to the Marketing OS with `log_update` (account, scenario, files). Don't change the opp.
