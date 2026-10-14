# PropFuel Claude Code plugins

## propfuel-os

Connects Claude Code to the **PropFuel Marketing OS** (https://propfuel-marketing-os.vercel.app). In any PropFuel session Claude:

- starts by pulling a briefing from the OS (your initiatives, what's blocked, deadlines, Q4 pacing, what teammates changed), and
- writes back what happened: progress logs, initiative / case study / plan updates and knowledge, credited to you, versioned and undoable.

Edits to things someone else owns ask you first.

### Install (once)

In Claude Code:

```
/plugin marketplace add alexhively/propfuel-claude
/plugin install propfuel-os@propfuel
```

Restart Claude Code, then run `/mcp`, pick **propfuel-os**, and sign in with your name and passcode (ask Alex). That's it.

### Commands

- `/propfuel-os:sweep` — one-time sync of everything your Claude already knows about your PropFuel work into the OS (you approve before anything is written).

The plugin contains no credentials: each person signs in to the OS with their own passcode.

### Team marketing skills (1.2.0)

The plugin also ships 12 skills from ECC (MIT), adapted to PropFuel: `marketing-campaign`, `seo`, `content-engine`, `article-writing`, `brand-voice`, `market-research`, `deep-research`, `competitive-platform-analysis`, `competitive-report-structure`, `lead-intelligence`, `frontend-slides`, `crosspost`. The same playbooks live in the Marketing OS knowledge (`Skill - <name>.md`) so claude.ai and Poppy use them too. Update with `/plugin marketplace update propfuel`.

### LinkedIn skills (1.3.0)

Eleven LinkedIn skills from the LinkedIn Agent Skill (github.com/avi691/linkedin-agent-skill, MIT, by Avi Grondin and Jake Schincariol), adapted to PropFuel:

- `li-post`: a post from an idea, with 21 hook formulas
- `li-comment`: comments on other people's posts
- `li-reply`: replies under your own posts
- `li-dm`: connection notes and DMs
- `li-inbox`: sorts your inbox
- `li-carousel`: a PDF carousel in PropFuel brand
- `li-repurpose`: one long piece into a week of posts
- `li-plan`: the weekly plan and engagement list
- `li-profile`: scores a profile out of 100
- `li-audit`: audits what you've posted
- `li-human`: humanizer scripts that clean and score every draft

Every skill loads **LinkedIn - Master.md** from the Marketing OS first, and the matching "LinkedIn KB" doc. It writes in your own voice if you have `~/.claude/linkedin/voice.md`; otherwise it uses PropFuel's (`skills/li-post/propfuel-voice.md`).

None of them post, comment or send anything. You read, approve and paste.

### Video ad skill (1.10.0)

- `/propfuel-motion-ad`: a PropFuel video ad where every frame is drawn by code (HyperFrames: HTML, CSS and GSAP rendered to mp4). No video model, stock footage, AI imagery or AI people. It uses the real logo, real product UI recreated in code, and type. Storyboard first, then a `spec.json` builds 9:16, 4:5, 1:1 and 16:9 projects plus a 6s bumper, with platform safe zones and burned-in captions. A budget-gated render exports H.264 mp4s, and `qa.sh` writes contact sheets for the frame check. Outputs go to `~/Desktop/PropFuel Motion Ads/<slug>/`. Nothing is uploaded until Alex approves the exact file. Needs Node 22+ and ffmpeg. The reference ad is TXCPA autorenewal (15s). Also in OS knowledge as `Skill - propfuel-motion-ad.md`.

### Sales skill (1.7.0)

- `/winback-walkthrough`: when a demo goes unperformed (no-show, cancelled, or requested but never booked), builds the 3-page win-back walkthrough "prepared for our call" for that association (the note, the campaign map, the comparison with the published medical-society proof), plus a cover email, a day-3 bump, an optional lateral email and a CRM note. Facts come from the Salesforce opp; no invented membership numbers. Draft only: the rep sends. In the content repurposer it renders through `scripts/make-winback-asset.mjs`; anywhere else it fills the bundled `walkthrough-template.html`. Also in OS knowledge as `Skill - winback-walkthrough.md`.

### Design skill (1.6.0)

- `/apple-design`: Apple's approach to interface design and fluid motion (springs, interruptible gestures, momentum, materials and depth, typography, reduced motion, the eight design principles), from Emil Kowalski's skills (github.com/emilkowalski/skills, MIT), translated for the web. Use it when building or reviewing any PropFuel UI: the Marketing OS, Webflow pages, landing pages, artifacts. PropFuel's brand tokens and rules come first (no `alert`/`confirm`/`prompt` dialogs; inline confirm or undo instead). The same playbook is in the OS knowledge as `Skill - apple-design.md`.

### Instagram skills (1.5.0)

Thirteen Instagram skills from the Instagram Agent Skill (github.com/Jakeschincariol/instagram-agent-skill, MIT, by Jake Schincariol), adapted to PropFuel:

- `/ig-reel`: Reel script from an idea: hook options off 26 formulas, spoken script, on-screen text, timed beat sheet
- `/ig-caption`: caption, one ask, search terms and three hashtags, linted
- `/ig-carousel`: carousel cover and slides, 1080x1350, PropFuel brand
- `/ig-story`: the day's Stories sequence and stickers
- `/ig-comment`, `/ig-reply`, `/ig-dm`: comments, replies and DMs that read as a person
- `/ig-plan`: the week: what, which format, when, who to engage with
- `/ig-profile`: 100-point profile score and rewrites
- `/ig-repurpose`: one long asset (webinar, case study, call) into a week of reels and carousels
- `/ig-audit`: what's working in your insights and why
- `/ig-viral`: study what works in the niche through your own browser, never logged in by Claude (the yt-dlp step only if Alex OKs installing it)
- `/ig-human`: humanizer and five-check AI detector

Every skill loads **Instagram - Master.md** from the Marketing OS first. It writes in your own voice if you have `~/.claude/instagram/voice.md`; otherwise it uses PropFuel's (`skills/ig-caption/propfuel-voice.md`). None of them post, comment, reply, DM or automate anything. It writes, you post.

### More ECC skills and two agents (1.4.0)

Eight more ECC skills (MIT), adapted to PropFuel: `email-ops` (draft-first; sends only on your explicit OK), `growth-log`, `product-lens`, `brand-discovery`, `click-path-audit`, `browser-qa`, `dashboard-builder`, `research-ops`. Plus two ECC agents Claude can hand work to: `marketing-agent` (campaign strategy and copy, drafts only) and `seo-specialist` (site audits as recommendations; never publishes Webflow). Each starts from the Marketing OS (`get_briefing`, Master docs) and carries PropFuel's hard rules. The same playbooks are in the OS knowledge as `Skill - <name>.md` and `Agent - <name>.md`.

Not included on purpose: ECC's hooks, its coding and build agents, investor skills, `security-review` (would shadow the built-in `/security-review`) and `social-publisher` (posts through a third-party API).

#### Changelog

- **1.10.3 (Oct 14 2026):** speaker tiles without footage show the speaker's initial and name (no photo crop).

- **1.10.2 (Oct 14 2026):** the speaker-tile rule is now Alex's pick: show only the person speaking, one tile with a sound-wave ring driven by their real audio; the listener isn't shown.

- **1.10.1 (Oct 14 2026):** `propfuel-motion-ad` carries the speaker-tile rule for real call footage: real moving footage from that exact moment, or an avatar card that reads as not on camera. Never a frozen frame or reused footage (Alex, ANA ad).

- **1.10.0 (Oct 12 2026):** added `propfuel-motion-ad`: coded video ads (HyperFrames), the replacement for the AI-generated case-study videos. It ships with its engine, the DM Sans font (OFL), the PropFuel logo, vendored GSAP, and render and QA scripts.

- **1.8.0 (Oct 12 2026):** `winback-walkthrough` publishes a per-prospect web page through the propfuel-winback generator (`npm run new -- "<account>" --preview`, then `publish-page` when the rep says so), and the cover email links to it; opens show in `npm run views`.

- **1.7.0 (Oct 12 2026):** added `winback-walkthrough` (Sales OTM Oct 9 demo-unperformed playbook), with a self-contained template so it works outside the repurposer.

- **1.6.0 (Oct 11 2026):** added `apple-design` (Emil Kowalski, MIT), PropFuel-adapted: brand tokens first, no modal dialogs, iOS share instead of download links.

- **1.5.0 (Oct 11 2026):** added the 13 `ig-*` Instagram skills (MIT, Jake Schincariol), the PropFuel Instagram voice default and brand tokens for carousels and Stories. Scripts run from the plugin folder with `python3 -I`; ig-viral never logs in and does not install yt-dlp.

- **1.4.0 (Oct 11 2026):** 8 more ECC skills and the `marketing-agent` and `seo-specialist` agents, PropFuel-adapted. Browser and click-path QA never submit real propfuel.com forms (they create real leads and ad conversions); email-ops is draft-first.

- **1.3.0 (Oct 11 2026):** added the 11 `li-*` skills, the PropFuel voice default, and PropFuel brand tokens for carousels. The humanizer scripts now run from the plugin folder with `python3 -I`.
