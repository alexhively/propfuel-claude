---
name: customize-my-os-page
description: Change how one of your PropFuel Marketing OS pages looks or works. Use when an owner of an OS page (webinars, events, calendar, organic and LinkedIn, case studies, Client Success, SDR desk) says "hide this panel", "move X above Y", "rename this heading", "show fewer columns", "default to Live case studies", "add a saved view", "fix this wording on my page", or asks for a new function on their page. Starts with the customize_page tool (no code); only goes to code for something it cannot do, and then does the whole job (clone, change, ship) for them.
---

# Customize my OS page

The person says what they want in plain words. You do everything else. Never hand them a command to run, a file to edit or a git step: they should only ever see "Done, here's what changed" (or one plain question).

Pages belong to people. The Share panel on each page shows who owns it (Brittany + Alejandra: webinars, events, calendar, organic, LinkedIn, case studies; Ashley: Client Success; Lisa: SDR desk; Alex: everything). Only an owner can reshape a page. Anyone else gets a 403 that says so: tell them who to ask, don't work around it.

## 1. Try `customize_page` first (no code, instant, undoable)
- `customize_page {action: "get", section}` shows the current setup plus the panel ids, column ids and sorts you may use.
- `customize_page {action: "set", section, patch}` merges a patch. Keys: `hidden` (panel ids), `order` (panel ids, first = top), `columns` (table columns to show), `labels` ({id: new heading, 60 characters, plain text}), `filters` ({stage, q}), `sort` ({by, dir}), `views` ([{name, filters, sort}] up to 8). A key set to `null` clears it.
- `customize_page {action: "reset", section}` puts the page back to standard.
- Sections: webinars, events, plan, calendar, organic, linkedin, case_studies, cs_center, sdr_desk. Panel and column ids are the visible heading in lowercase with dashes ("every-case-study"). Filters, sort and saved views apply on Case studies today; panels, order, labels and columns apply on every page that has cards or tables.
- Every change returns a `change_id`. Tell the person what changed in one line and offer the undo (`undo_change`).
- Unknown ids, markup or long labels are refused with the reason. Fix the patch; don't try to sneak it in.

## 2. Anything else (new wording, a new field, a button, new logic): you change the code and ship it
No one has to approve it: it ships by itself when the automated gates pass, and rolls back by itself if the live site breaks.

### First time on this computer (do it silently, once)
1. `gh auth status`. If gh is missing or signed out, stop and walk them through it in plain steps: install from https://cli.github.com, then type `! gh auth login` in this chat and pick GitHub.com → HTTPS → "Login with a web browser". They need a GitHub account that Alex has invited to `alexhively/propfuel-marketing-os`; if `gh repo view alexhively/propfuel-marketing-os` fails, ask them to accept the invite email (or ask Alex for one).
2. `node --version` must be 20 or newer. If not, ask them to install Node from https://nodejs.org (the LTS button), then continue.
3. If `~/Projects/propfuel-marketing-os` doesn't exist: `gh repo clone alexhively/propfuel-marketing-os ~/Projects/propfuel-marketing-os`, then `npm ci` in it.
4. Their GitHub login is `gh api user --jq .login`. It must be listed under `logins` in `.github/section-owners.json` on main. If it isn't, tell the hub/Alex (that file is a gate file: you can't add it yourself).

### Each change
1. `cd ~/Projects/propfuel-marketing-os && git fetch origin && git worktree add ~/Projects/pfos-<topic> -b <login>/<topic> origin/main`, and work in that folder. Never on `main`.
2. Make the change. Your own section's files are listed in `.github/section-owners.json`; shared core files (store, auth, acl, mcp, index.html) are fine too. Don't touch the gate files (the `gate` list in that file): a change that touches them is stopped.
3. No secrets, no real names or emails in the repo, no `alert`/`confirm`/`prompt`. New logic gets a small test, added to the `check` list in `package.json` (checks can be added, never removed). `npm run check` must pass.
4. Commit with a plain one-line message ("Case studies: Alejandra edits directly too").
5. `node scripts/ship.mjs --dry-run --author <login>`, then for real: `npm run ship -- --author <login>`. It runs every test, scans for secrets and personal data, merges to `main`, waits for the deploy, smoke-checks the live site and rolls back by itself on failure.
6. Pass the `LOG_UPDATE {…}` line it prints to `log_update` (its `summary` and `shipped`). That writes the OS activity entry and posts one line in #os-changes.
7. Tell them in one or two sentences what changed and that it's live (or what stopped it). Remove the worktree: `git worktree remove ~/Projects/pfos-<topic>`.

## 3. When it stops
Each stop comes with a plain reason; fix it yourself and ship again, then tell the person in one sentence.
- A test failed (it names which, and what it said): fix the code, never the test.
- Secrets or personal data found: remove them (env var or the private Blob store), commit, ship again.
- You edited a gate file: split that file out of the change. Those files need Alex.
- Main moved on: `git rebase origin/main`, ship again.
- The deploy or smoke check failed after merging: it already rolled back. Say so, look at why, and only try again once you know.
