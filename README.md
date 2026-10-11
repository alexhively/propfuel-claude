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

#### Changelog

- **1.3.0 (Oct 11 2026):** added the 11 `li-*` skills, the PropFuel voice default, and PropFuel brand tokens for carousels. The humanizer scripts now run from the plugin folder with `python3 -I`.
