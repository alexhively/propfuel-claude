---
name: propfuel-os
description: Use for ANY PropFuel work (marketing, website, campaigns, content, case studies, events, ads, sales enablement, analytics, AMC, partners). Pulls the current state from the PropFuel Marketing OS before starting and writes progress, initiative updates and learnings back when done.
---

# PropFuel Marketing OS

The PropFuel Marketing OS (https://propfuel-marketing-os.vercel.app) is the team's shared source of truth: initiatives (owner, status, health, next step, blocker), the Q4 plan and goals, deadlines, case studies, living knowledge docs, and the live Salesforce demand model. You reach it through the `propfuel-os` MCP tools. You are signed in as the user, so everything you write is credited to them.

## Before starting PropFuel work
1. Call `get_briefing`. Work from it: the user's initiatives, what's blocked or at risk, deadlines, Q4 pacing, and what teammates changed recently.
2. If the task touches a specific initiative, case study, plan item or knowledge doc, read it (`get_initiatives`, `get_case_studies`, `get_q4_plan`, `get_knowledge`) so you don't redo or contradict work that's already recorded.
3. If what the user says conflicts with the OS (e.g. a different number, owner or status), point it out and ask which is right.

## While working and before finishing
- For each meaningful outcome (shipped, decided, learned, blocked), call `log_update` with one plain sentence, the `initiative_id`, and a link if there is one. One entry per outcome, not per step.
- When an initiative's status, health, progress, next step, blocker or due date changes, call `update_initiative` with only the changed fields.
- Case studies: `update_case_study`. Gifting milestones: `update_milestone`. Other plan sections: `update_plan_section`. Goals: `update_q4_goal`.
- New durable knowledge (call learnings, messaging decisions, research): `update_knowledge` with mode "append" to the right doc, or "create" for a new topic.
- New work that isn't tracked yet: `create_initiative` (ask the user first).
- At the end of the session, tell the user in one line what you wrote to the OS.

## Permissions
- If a write returns `needs_confirmation`, the record belongs to someone else. Tell the user who owns it, ask whether to go ahead, and only then repeat the call with `confirm_not_owner: true`.
- Never change goals, numbers, owners or due dates the user didn't ask to change. Demand-model numbers come from Salesforce and are read-only.
- Every write returns a `change_id`; `undo_change` restores the previous version if something was wrong.

## If the tools are missing
Tell the user to run `/mcp`, choose `propfuel-os`, and sign in with their name and passcode (Alex has it).
