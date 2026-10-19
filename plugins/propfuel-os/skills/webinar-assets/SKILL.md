---
name: webinar-assets
description: Webinar Assets. From a title, date/time, speaker(s), registration link and description, build the PRE set (Zoom banner 1280x400, email banner 2400x600, pop-up 1080x1080, long-title variants chosen automatically), the POST set (YouTube thumbnail 1280x720, website banner 1200x400, platform banner 2400x600), and the copy (Zoom description, PropFuel email Part 1 / Question / Part 2, recording page fields, LinkedIn post, Slack hand-off). Also the registration-list CRM cross-check. Use when someone says "webinar assets", "pre-webinar set", "post-webinar assets", "webinar banners", "Zoom banner", "pop-up", "replay thumbnail", "webinar email", "recording page copy", or "cross-check this registration list". Draft only: never posts, sends or uploads.
---

# Webinar Assets

Alejandra's Webinar Assets project turned into an OS skill (Oct 19 2026). Repo: alexhively/propfuel-webinar-assets (private). Everything here is a draft: Alex and Alejandra review before anything goes anywhere. Never post, send or upload an asset.

Bundled next to this file: `scripts/` (builders, font installer, copy lint), `templates/` (HTML + PIL templates, logo, brand guide), `reference/` (copy rules, CRM runbook, approved Sep 9 reference JPGs).

## 0. Set up (every session)
```bash
bash scripts/install_dmsans.sh   # DM Sans variable font; verify before rendering
```
Needs Python 3 with `playwright` (run `python3 -m playwright install chromium` once) and `Pillow`. Output defaults to `./out` unless `/mnt/user-data/outputs` exists. Without DM Sans the HTML banners silently fall back to Liberation Sans: stop and fix.

## 1. Inputs
Title (lock it explicitly before POST assets and recording copy), date, time ET, duration (ASK if missing; 30 min default, 1 hr is common), speaker(s) (default Brittany Lancor), registration link, 2 to 3 sentence description (no speaker name inside it), series subtitle if any, sender of the email. Pull details first with the OS `get_events` tool when an event id is known. Name every assumption in the delivery note.

## 2. PRE set
```bash
python3 scripts/build_prewebinar_assets.py --title "..." --date "Oct 28, 2026" --time "2:00 PM ET" \
  --duration "1 hr" --speaker "Ryan Graham" --description "..." --slug <slug> --out <dir>
```
`--preset auto` tries the one-line look and falls back to the two-line long-title look, measuring each render. Flags: `--subtitle`, `--eyebrow "Live Deminar"`, `--no-speaker`, `--no-duration`, `--cta`, `--only zoom|email|popup`. Short date ("Oct 28, 2026"). Outputs `zoom_banner_<slug>_1280x400.jpg`, `email_banner_<slug>_2400x600.jpg`, `popup_<slug>_1080x1080.jpg` plus the HTML.

Expected for a short title: Zoom headline 68px (text ends near x 1100), eyebrow 21px, meta row y 317; email headline 127px. Long title: Zoom 45px, email 80px, pop-up 66 to 68px, two lines, nothing touching the divider.

## 3. POST set
```bash
python3 scripts/build_postwebinar_assets.py --title "..." --date "July 9, 2026" --speaker "..." --slug <slug> --out <dir>
# long title: --font-scale 0.85 ; Membership AI webinar: --membership-ai
```
Long month in the date. YT 1280x720 ("WEBINAR REPLAY", 84px, "Watch Now"), website 1200x400 (52px), platform 2400x600 (110px, "WATCH THE RECORDING", "Webinar Replay" button).

## 4. Always look at the images
Open every JPG and check: DM Sans (round "a", geometric "o"), no overflow, nothing touching the divider, logo top-right. Check the size with PIL. Re-run with a smaller size if needed.

## 5. Copy
Write from `reference/copy.md` (brand rules, formats, approved examples), then lint:
```bash
python3 scripts/lint_copy.py zoom.md email.md recording.md linkedin.md slack.md
```
Brand rules: "Know and Grow Your Membership"; "12% average annual revenue growth after implementing PropFuel" only beside "vs 0.98% for the average association", never 8.68%; "370+ associations"; name a client in public copy only if their case study is live (check `get_case_studies`), otherwise anonymize; no em dashes.

## 6. Save and record
Save to `~/Desktop/PropFuel/04 Content/Webinars/<date-slug>/` (PRE/, POST/, copy/). Add links to the webinar's assets with the OS `update_event` tool (action "asset"; use `slot` if available). Log the outcome with `log_update`.

## 7. CRM cross-check
For "cross-check this registration list", follow `reference/crm-crosscheck.md`. Read-only; report cleanup notes and wait for a yes before any change.
