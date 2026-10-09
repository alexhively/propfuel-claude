---
name: save-skill
description: Save or update a PropFuel content skill from the work in this session, so the next person (or Claude) makes that kind of content the way it was just refined. Use when the user says "save this as a skill", "update the skill", "remember how we made this", "train the brain on this", or at the end of a session where the user refined how a piece of PropFuel content gets made (testimonial videos, ads, case studies, emails, decks, landing pages, LinkedIn posts, webinar kits, anything repeatable). Also use when the user hand-edits Claude's output and asks Claude to learn from the edits.
---

# Save a content skill

A content skill is the recipe for one kind of PropFuel content: what it's for, the steps, the standards that make it good, and the specific corrections the team has made along the way. It turns this session's back-and-forth into something every future session starts from.

## 1. Work out what was learned
Go back through the session (and any files the user edited by hand) and pull out:
- **The content type**, named the way the team would say it, e.g. "testimonial video", "AMC cold email", "case study one-pager".
- **The process that worked:** inputs and where they come from (Gong, Hook signals, Salesforce, Drive, Desktop folders), the steps in order, tools and scripts with exact paths and commands, and output formats and sizes.
- **Standards:** what makes a good one. Length, structure, hook, tone, brand rules, things to always or never do.
- **Corrections:** every time the user said "no, do it like this", one line each, written as the rule plus why. These are the most valuable part, so don't summarize them away.
- **Examples:** paths or links to the best finished pieces, so the next run can copy what good looks like.
- **Gates:** approvals or consents needed before anything ships (e.g. written client consent for testimonials).

If a correction contradicts the existing skill, the newer correction wins. Note what changed.

## 2. Find or create the skill
1. Look for an existing skill that covers this content type, in this order: the current repo's `.claude/skills/`, then `~/Projects/propfuel-content-repurposer/.claude/skills/`, `~/Projects/propfuel-meta-ads/.claude/skills/`, and this plugin's `skills/`.
2. If one exists, update it in place. Merge; don't append a second copy of the process. Keep its frontmatter `name` and sharpen its `description`.
3. If none exists, create `.claude/skills/<kebab-name>/SKILL.md` in the repo where this content is normally made. Use the plugin (`~/Projects/propfuel-claude/plugins/propfuel-os/skills/`) only for skills every teammate's Claude Code should have.
4. Tell the user which file you're writing before writing it, in one line.

## 3. Write it in this shape
```
---
name: <kebab-name>
description: <when to use it, in the words people use to ask for it; mention the content type and key trigger phrases>
---
# <Content type>
What it's for and who sees it (one or two sentences).

## Inputs
## Steps
## Standards
## Corrections (newest first)
- YYYY-MM-DD: <rule>. Why: <reason the user gave>.
## Examples
## Before it ships
## Changelog
- YYYY-MM-DD: <what changed in this update>, from <person>'s session.
```
Keep it skimmable: short lines, exact paths and commands, no narrative. Put long reference material (prompt templates, shot lists) in files next to SKILL.md and link them.

## 4. Share it with the team's Claude
- Mirror the skill into the Marketing OS so claude.ai users get it too: call `update_knowledge` with name `skill-<kebab-name>.md`. Use mode "create" the first time and "replace" after that (replace asks for confirmation; say yes when the user asked for this update). The content is the SKILL.md body.
- Call `log_update`: "Updated the <content type> skill: <the main changes>", with the matching `initiative_id` if there is one.
- If the skill lives in a git repo, commit it with a message naming the skill and the main change. Push only if the user says to.

## 5. Report back
In two or three lines: which skill (file path), what was added or changed (especially new corrections), and where the team can find it.
