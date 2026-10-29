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

## 2. New function? Use a branch (code)
Only when `customize_page` can't do it (a new field, a new button, new logic):
1. In the OS repo (`~/Projects/propfuel-marketing-os`), make a worktree and branch: `git worktree add ~/Projects/pfos-<topic> -b <your-name>/<topic> origin/main`. Never work on `main`.
2. Edit **only your section's files**. The list is `.github/section-owners.json` (`sections`); `node scripts/check-section-paths.mjs --base origin/main --author <your GitHub login>` tells you before you push. `index.html`, `lib/store.js`, `lib/auth.js`, `lib/acl.js`, `api/mcp.js`, `package.json` and the other shared files are Alex's: if your idea needs them, say so in the PR instead of editing them.
3. No secrets, no real names or emails in the repo. No `alert`, `confirm` or `prompt`.
4. `npm run check` must be green.
5. `vercel deploy` (no `--prod`) for a preview URL. Careful: previews read and write the **real** data, so look but don't click Save on anything you don't mean to change.
6. Open a pull request with the preview URL and one plain sentence on what changed. Never merge to `main` and never `vercel --prod` yourself.

## 3. What happens next
The `section-paths` check on the PR runs the same path guard. All green and inside your section: it can merge with a quick look. Anything shared or outside your section: it says **NEEDS ALEX**, and Alex reviews and merges. That is the system working, not a failure.
