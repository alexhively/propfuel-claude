---
name: customize-my-os-page
description: Change how one of your PropFuel Marketing OS pages looks or works. Use when an owner of an OS page (webinars, events, calendar, organic and LinkedIn, case studies, Client Success, SDR desk) says "hide this panel", "move X above Y", "rename this heading", "show fewer columns", "default to Live case studies", "add a saved view", or asks for a new function on their page. Starts with the customize_page tool (no code); only goes to code for something it cannot do.
---

# Customize my OS page

Pages belong to people. The Share panel on each page shows who owns it (Brittany + Alejandra: webinars, events, calendar, organic, LinkedIn, case studies; Ashley: Client Success; Lisa: SDR desk; Alex: everything). You can only reshape a page you own. Anyone else gets a 403 that says so: tell them who to ask, don't work around it.

## 1. Try `customize_page` first (no code, instant, undoable)
- `customize_page {action: "get", section}` shows the current setup plus the panel ids, column ids and sorts you may use.
- `customize_page {action: "set", section, patch}` merges a patch. Keys: `hidden` (panel ids), `order` (panel ids, first = top), `columns` (table columns to show), `labels` ({id: new heading, 60 characters, plain text}), `filters` ({stage, q}), `sort` ({by, dir}), `views` ([{name, filters, sort}] up to 8). A key set to `null` clears it.
- `customize_page {action: "reset", section}` puts the page back to standard.
- Sections: webinars, events, plan, calendar, organic, linkedin, case_studies, cs_center, sdr_desk. Panel and column ids are the visible heading in lowercase with dashes ("every-case-study"). Filters, sort and saved views apply on Case studies today; panels, order, labels and columns apply on every page that has cards or tables.
- Every change returns a `change_id`. If they don't like it: `undo_change`. Tell the person what changed in one line and offer the undo.
- Unknown ids, markup or long labels are refused with the reason. Fix the patch; don't try to sneak it in.

## 2. New function? Branch, edit, ship (code)
Only when `customize_page` can't do it (a new field, a new button, new logic). No one has to approve it: it ships by itself when the automated gates pass.
1. In the OS repo (`~/Projects/propfuel-marketing-os`), make a worktree and branch: `git worktree add ~/Projects/pfos-<topic> -b <your-name>/<topic> origin/main`. Never work on `main`.
2. Edit what the feature needs. Your own section's files are listed in `.github/section-owners.json`; shared core files (store, auth, acl, mcp, index.html) are allowed too, because the gates, not a person, decide. Don't edit the gate files (the `gate` list in that same file: the acl/ownership tests and the ship/scan/smoke/path scripts): a change that touches them is stopped.
3. No secrets, no real names or emails in the repo, no `alert`/`confirm`/`prompt`. Add a test for new logic and add it to the `check` list in `package.json` (checks can be added, never removed).
4. `node scripts/ship.mjs --dry-run --author <your GitHub login>` first. It runs the gates and shows what would happen.
5. `npm run ship -- --author <your GitHub login>`. It runs every test, scans for secrets and personal data, merges to `main`, waits for the deploy, smoke-checks the live site, and rolls back by itself if that fails.
6. Finish with the `LOG_UPDATE` line it prints: call `log_update` with that `summary` and `shipped` object. That puts "who shipped what" in the OS activity feed and in Slack.

## 3. When it stops
Each stop comes with a plain reason; tell the person in one or two sentences and fix it.
- A test failed (it names which, and what it said): fix the code, never the test.
- Secrets or personal data found: remove them (env var or the private Blob store), commit, ship again.
- You edited a gate file: split that file out of the change. Those files need Alex.
- Main moved on: `git rebase origin/main`, ship again.
- The deploy or smoke check failed after merging: it already rolled back. Report that to the person, and look at why before trying again.
