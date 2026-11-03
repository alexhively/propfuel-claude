---
name: web-popups
description: Put a pop-up on propfuel.com, change one, schedule it or take it down, straight from Claude. Use when someone says "add a pop-up", "website pop-up", "put the webinar pop-up live", "change/turn off the pop-up", "what pop-ups are running", or hands over a 1080x1080 pop-up image. Uploads the image to the Marketing OS, saves the pop-up as a draft, checks the preview on desktop and phone, then sets it live. The website shows it within about 2 minutes.
---

# Website pop-ups

Pop-ups on propfuel.com live in the Marketing OS, not in the website code. The site reads the live ones from the OS on every page and shows at most one per visit. You make them with three OS tools: `popup_upload_url`, `update_popup`, `get_popups`.

## Before anything
Load the rules: `get_knowledge` "Web Pop-ups - Master.md". Follow it. Then `get_popups` to see what's running now.

## Steps
1. **Image.** 1080x1080, under 2 MB, jpg/png/webp. Check: `sips -g pixelWidth -g pixelHeight <file>`. Look at it: every word readable at phone size (~350px wide), title + date and time in ET + call to action, brand colors. Never "See One Question in 87 Seconds". Wrong size → stop and say so.
2. **Upload.** `popup_upload_url {popup_id, filename}` → run the returned curl from the image's folder. Keep the `pathname`.
3. **Save as draft.** `update_popup` with id, name, image (pathname), link (for a webinar: its Zoom "Web pop-up" tracking link; see the webinar's Notion card or `get_events {id}`), alt (everything the image says), `ends_at` (webinar start, ISO with offset, e.g. `2026-11-18T14:00:00-05:00`), `pages` (`["*"]` for a webinar, `["/"]` homepage only), `webinar_id`.
4. **Preview.** Open the returned `preview` link on desktop and at 390px wide (Claude in Chrome, or ask the teammate to open it on their phone). Check the image, the × button and that the click goes to the right place. Fix → re-upload (a changed image = a new upload) → save again.
5. **Go live.** `update_popup {id, status: "live"}` (add `starts_at` to schedule it). Read `overlaps` in the reply; if two overlap, set `priority` on purpose or ask.
6. **Webinar?** Tick its asset: `update_event {action: "asset", id: <webinar id>, slot: "popup", link: <preview link>, status: "live"}`.
7. Tell the teammate in two lines: what's live, where, until when, and the preview link.

## Changing or stopping
- Change text/image/link/dates: `update_popup` with the id and only what changes.
- Take it down: `update_popup {id, status: "off"}`. Undo any change: `undo_change` with the `change_id`.
- Someone else's pop-up returns `needs_confirmation`: ask the teammate before repeating with `confirm_not_owner: true`.

## Never
- Pop-ups on demo or form pages (the OS refuses them anyway).
- A pop-up with no end date, or "live" without checking the preview.
- Editing the website code (js/pages/popups.js) to add a pop-up: that's only the renderer.
