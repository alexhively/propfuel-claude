---
name: sweep
description: One-time (or occasional) sweep that finds everything this Claude knows about the user's PropFuel work — memories, CLAUDE.md files, project folders, notes, recent sessions — and syncs it into the PropFuel Marketing OS after the user approves. Run with /propfuel-os:sweep.
---

# Sweep my Claude into the PropFuel Marketing OS

Goal: the Marketing OS should reflect everything the user's Claude knows about their PropFuel work, so the whole team (and every future session) works from the same picture. Nothing is written until the user approves the plan.

## 1. Load the current OS state
Call `get_briefing` with `include_all_initiatives: true`, then `get_case_studies`, `get_q4_plan` (section "all"), and `get_knowledge` (list, then read any doc relevant to the user's work). Note who you're signed in as; that person "owns" the records whose owner field names them.

## 2. Gather what this Claude knows about PropFuel
Search, read, and take notes — do not change anything yet:
- Claude Code memory: `~/.claude/CLAUDE.md`, `~/.claude/projects/*/memory/` (MEMORY.md and the files it lists), and any project `CLAUDE.md` / `AGENTS.md`.
- Project folders that look like PropFuel work (search the home directory, Desktop, Documents and ~/Projects for "propfuel", "PropFuel", client/association names, "webinar", "case study", "event", "campaign"), their READMEs, CONTEXT/handoff docs and recent git history (`git log --since=60.days --oneline`).
- Recent session transcripts in `~/.claude/projects/` from the last 60 days that mention PropFuel: skim for decisions, shipped work, open loops, blockers, numbers and learnings.
Skip anything personal, credentials/API keys, and member or customer personal data.

## 3. Compare and draft a sync plan
Organize what you found against the OS into a table for the user:
- **Progress to log** (`log_update`): dated outcomes from the last 60 days that the OS doesn't show (shipped, decided, learned). Give each its initiative_id when one fits.
- **Initiative updates** (`update_initiative`): where the OS is stale for initiatives the user works on — status, health, progress, next step, blocker, due. Mark which ones the user doesn't own (those need their OK, and the owner should hear about it).
- **New initiatives** (`create_initiative`): real ongoing work the OS doesn't track.
- **Case studies / plan / milestones**: any stage, date or status the OS has wrong.
- **Knowledge** (`update_knowledge`, mode "append"/"create"): durable learnings worth sharing — messaging that worked, call insights, how-tos, vendor/event details, decisions and their reasons. Name the target doc.
- **Conflicts**: where the user's Claude and the OS disagree; say which source looks newer and ask.
Keep each line short. Don't invent; if unsure, list it as a question.

## 4. Get approval, then write
Ask the user to approve, edit or drop items (they can approve all, approve by section, or strike lines). Then make the approved writes. For records they don't own, the tool returns `needs_confirmation`: only proceed with `confirm_not_owner: true` for items the user explicitly approved knowing the owner. Collect every `change_id`.

## 5. Wrap up
- Report what was written (counts by type) and list the change_ids so anything can be undone with `undo_change`.
- List what you left out and why, and any questions for the owners of records you touched.
- Remind the user: from now on, PropFuel sessions start with the OS briefing and end by logging outcomes (the propfuel-os plugin does this automatically).
