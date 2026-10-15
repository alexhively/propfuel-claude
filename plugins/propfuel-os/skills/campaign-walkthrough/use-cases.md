# Campaign maps by use case

Source: Campaign Walkthroughs - Master (Notion; snapshot in the content repurposer at `knowledge/messaging/campaign-walkthroughs.md`). Each map is four one-question emails. Rewrite every question and answer option for the prospect's members (see "Write for the member type" in SKILL.md). Keep the actions: every pill is a standard PropFuel feature.

Pill classes in the template: `route` (sends them to a page or resource), `tag`, `ams` (saved to AMS; write "Saved to Salesforce" etc. when you know their AMS), `alert` (staff alerted), `ask` (asks a follow-up), `stop` (stops emailing), `next` (no answer: gets the next email; **not counted** as an action).

**Action count** (page 1 `[ACTION COUNT]`) = every pill on page 2 except `next`, plus the 3 "Running the whole time" items. Recount after you edit the map.

**Proof** (page 3 dark box): only a case study that `get_case_studies` lists as **Live**, for the same use case. Use the metric exactly as the OS lists it. Name the client only if `shown_as` is Named; otherwise describe it ("an international medical society"). If none fits, drop the three numbers and keep only the `.src` line. Never invent numbers, never the 8.68% stat.

---

## win-back (default)
- **Phrase:** a lapsed-member win-back · **Standard sequence name:** win-back sequence
- **Starts:** when a member lapses in [AMS], and stops the moment they rejoin.
- **Map:**
  1. *When they lapse* · "Did you know your membership has expired?" "No, I didn't know" → route Renewal link, tag, ams · "Yes" → tag, ams · No answer → next
  2. *One week later* · "Would you like to rejoin [ASSOC]?" "Yes" → route Rejoin page, ams · "Not sure" → alert, tag Tagged warm · "No" → ask Asks why, ams Reason saved, stop (why: cost, value, changed jobs or other; "Cost" also alerts staff)
  3. *Two weeks later* · a goal question for their members (e.g. "Which goal matters most to your career this year?") → route Matching resource, tag Tagged by interest, ams
  4. *Two weeks later* · "What's holding you back from rejoining?" (Cost · Time · Value · I'm interested in rejoining!) Interested → alert Staff alerted now, route Rejoin page · Any reason → ams Reason saved, tag Tagged by reason
- **Running the whole time:** enrolled automatically when the AMS marks a member lapsed · removed the moment they rejoin · rejoins and dues counted. **Count: 22.**
- **Page 1 left box first line:** Sends the same "Your membership has expired" message to everyone · **PF box last line:** Stops emailing people as soon as they renew
- **Page 3 standard sequence:** "Your membership has expired" → "Don't miss out" → "We miss you" → "Last chance". Doesn't happen: no reason for leaving; renewers keep getting "last chance"; warm replies sit in an inbox; the AMS looks the same.
- **Removal rule:** A rule that removes members when [AMS] shows they renewed
- **Proof:** International medical society (anonymous), Live: 42 lapsed members rejoined · $18,438 recovered in dues · 72% of first answers said they didn't know they'd lapsed (of 54). Eyebrow "One question, seven weeks". It recovered more than it pays for PropFuel in a year.

## renewal
- **Phrase:** a renewal conversation · **Standard sequence name:** renewal reminder series
- **Starts:** 90 days before a member's renewal date in [AMS], and stops the moment they renew.
- **Map:**
  1. *90 days out* · "Are you planning to renew your membership this year?" "Yes" → route Renewal page, tag, ams · "Maybe, I need more time" → tag, route Value recap · "No" → ask Asks why, alert, ams Reason saved
  2. *60 days out* · a benefit-reflection question for their members (e.g. physicians: "Which benefit mattered most to your practice this year?" Advocacy · CME · Practice resources · Peer network) → route Matching renewal message, tag Tagged by benefit, ams
  3. *30 days out* · "Would you like to renew now?" (no "maybe") "Yes" → route Renewal page, ams · No answer or "Not yet" → next
  4. *At expiration* · "Is something holding you back from renewing?" (Cost · My employer pays · Retiring or leaving the field · "I'd like to renew after all!") After all → alert, route Renewal page · Employer pays → route Employer letter, tag · Any other reason → ams Reason saved, tag Tagged by reason
- **Running the whole time:** enrolled automatically 90 days before the renewal date · removed the moment they renew · anyone still unrenewed at expiration moves into the win-back campaign. **Count: 22.**
- **Page 1 left box first line:** Sends the same "Time to renew" message to everyone · **PF box last line:** Stops emailing people as soon as they renew
- **Page 3 standard sequence:** "Time to renew" → "Renew today" → "Don't lose your benefits" → "Final notice"
- **Removal rule:** A rule that removes members when [AMS] shows they renewed
- **Proof:** Geological Society of America (Named, Live): 1,078 renewals · 14.4% average response. Texas Society of CPAs (Named, Live, autorenewal): 38.3% response rate, 575 of 1,502 members.

## onboarding (new members, first 4 months)
- **Phrase:** a new-member onboarding · **Standard sequence name:** welcome series
- **Starts:** when a new member joins in [AMS], and runs through their first four months.
- **Map:**
  1. *Week 1 · Welcome* · "What are you most hoping to get out of your membership this year?" (options for their members) → route Matching resource, tag Tagged by interest, ams
  2. *Week 3* · a get-involved question native to the org (bar: "Have you joined a section yet?"; medical: "Have you found your specialty section?"; trade: "Have you joined a committee?") "Yes" → tag, ams · "Not yet" → route Section finder, tag · "What's a section?" → route Explainer page, tag
  3. *Month 2* · a preference question (bar: "How do you like to earn your CLE?"; medical: CME) → route Matching list, tag, ams
  4. *Month 4* · "How well is [ASSOC] meeting your needs so far?" 4–5 → tag Tagged happy, ams · 1–3 → alert, ask Asks what's missing, ams
- **Running the whole time:** enrolled automatically when a member joins · every answer feeds the renewal campaign · removed if they cancel. **Count: 20.**
- **Page 1 left box first line:** Sends every new member the same "Welcome! Here are your benefits" email · **PF box last line:** Hands each new member's answers to your renewal campaign
- **Page 3 standard sequence:** "Welcome to [ASSOC]" → "Your member benefits" → "Don't miss [flagship benefit]" → "Upcoming events". Doesn't happen: no idea why they joined; everyone gets the same benefits list; quiet new members aren't spotted until they don't renew; the AMS looks the same.
- **Removal rule:** A rule that removes members when [AMS] shows they cancelled
- **Proof:** AMA onboarding (Named, Live): 45% engagement · new-member engagement doubled.

## acquisition / recruitment
- **Phrase:** a member-recruitment campaign · **Standard sequence name:** prospect drip
- **Starts:** when a non-member creates an account, registers for an event or downloads a resource.
- **Map:** 1 *Day 1* needs question ("What's most important to you this year?") → route Matching resource, tag, ams · 2 *One week later* "Are you interested in joining as a member?" Yes → route Join page, alert · Not sure → tag, route Member stories · No → ask Asks why, stop · 3 *Two weeks later* value-alignment question → route Matching benefit, tag · 4 *Two weeks later* "Is something holding you back from joining?" (Cost · Time · Not sure it's for me · "I'd like to join!") Join → alert, route Join page · Any reason → ams Reason saved, tag
- **Running:** enrolled automatically from the trigger · removed the moment they join · joins and dues counted.
- **Standard sequence:** "Join today" → "Member benefits" → "Limited-time offer" → "Last chance to save"
- **Proof:** AMA website (Named, Live): 3,803 conversions · $304,240 revenue. Emergency Nurses Association (Named, Live): 9,739 responses · 395 leads.

## event / engagement
- **Phrase:** an event registration campaign · **Standard sequence name:** event promo series
- **Starts:** when early-bird registration opens, and stops for each person the moment they register.
- **Map:** 1 *Early bird* "Are you planning to attend this year?" Yes → route Registration page, tag · Maybe → tag · No → ask Asks why, ams · 2 *Three weeks later* "Which topic interests you most?" → route Matching sessions, tag, ams · 3 *Two weeks out* "Can we save you a seat?" Yes → route Registration page · Not this year → ams Reason saved, stop · 4 *One week out* "Is something holding you back?" (Cost · Travel · Timing · "I'd like to register after all!") After all → alert, route Registration page · Any reason → ams, tag
- **Running:** enrolled automatically when registration opens · removed the moment they register · registrations and revenue counted.
- **Standard sequence:** "Registration is open" → "Early bird ends soon" → "Agenda announced" → "Last chance"
- **Proof:** VECCS (Named, Live): 449 registrations · $315,300 revenue.

## other
Ask the user for the goal in one line, then build four one-question emails on the Ask → Capture → Act pattern from Campaign Walkthroughs - Master (data/profile updates, certification, NPS). No proof numbers unless a Live case study matches.
