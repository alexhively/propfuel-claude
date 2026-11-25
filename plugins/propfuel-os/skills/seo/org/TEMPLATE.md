# Org profile: <Organization name>

Copy to `org/<slug>.md`, or keep the filled version in the user's own state doc. SKILL.md step 0 loads it before any mode.

## Intake (run when no profile exists)
Interview the user, one short group at a time. Do not guess answers; mark unknowns "unknown" and say what is missing.
1. Who: organization name, site URL(s), who approves what ships.
2. Stack: CMS or framework, where titles, metas, schema and redirects are edited, how a change reaches production (repo and PR, CMS API, ticket), staging URL and whether it is indexable.
3. Audience: who buys, who the ICP is, what words qualify a keyword (the qualifier rule), which keyword classes are out of scope.
4. Competitors: 3 to 6 direct, plus big generic vendors that own head terms.
5. Facts: the numbers, names and claims copy may use. Anything banned or legally sensitive. Brand tagline rules.
6. Voice: spelling locale, banned punctuation or phrases, reading level.
7. Data: Search Console property and access, keyword-volume route, AI-visibility tool and prompt list, analytics and conversion tracking, rank tracker if any.
8. State: where program state lives, which tool to log outcomes to, any start-of-run and end-of-run hooks.
9. Today: the current keyword-to-page map (if any), tracked AI prompts (if any), known live-site problems, past mistakes to never repeat.

## Identity
- Organization:
- Site URL(s):
- Staging URL(s) and indexing policy:
- Approver(s) (who signs off the exact diff):

## Stack and how changes ship
- CMS / framework:
- Where native fields live (title, meta, canonical, schema, redirects, robots, sitemap):
- Ship flow (branch, PR, CMS publish, who publishes):
- Undo path:
- QA gates before showing the approver:

## Audience and keyword rules
- ICP:
- Qualifier rule (e.g. "keyword must contain X"):
- Why the rule exists:
- Excluded keyword classes (with reasons):
- Allowed exceptions:
- Competitors (benchmark set):
- Competitors that are poor comparisons:

## Facts allow-list and banned claims
Allowed (only these):
-
Banned (never write):
-
Unknown number rule: write `{{number}}` and flag it.
Source of truth for facts:

## Brand and style
- Tagline and its usage tiers:
- Spelling locale:
- Style rules (punctuation, banned words, sentence shape):
- CTA wording rules:

## Data sources
| Source | Connected as | Notes (lag, limits) |
|---|---|---|
| Search Console | property: | |
| Keyword volumes | route: | |
| AI-visibility tracker | tool and prompt slots: | |
| Analytics / conversions | | |
| Rank tracker | | |

## State and logging hooks
- State doc location:
- Start-of-run hook:
- End-of-run hook (log, update state, request approval):

## Tracked AI prompts
Number | Prompt | Cluster | Key prompt? | Keywords behind it | In tracker? (Y/N)

## Keyword-to-page map
Page | Primary keyword (vol/KD) | Secondary | Baseline position and date
Rule: one head term per page.

## Known live-site issues
Issue | URLs | Status | Date found

## Corrections log (dated, newest first)
- YYYY-MM-DD: what the approver corrected and why.

## Changelog
- YYYY-MM-DD: what changed in this profile.
