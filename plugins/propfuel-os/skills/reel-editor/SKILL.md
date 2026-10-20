---
name: reel-editor
description: >-
  Edit raw talking-head clips into a finished PropFuel reel (best takes, dead air
  cut, captions, animation, effects) in the team's house styles: Show and Tell
  (default), Color Block, Viral Guy. Runs on Creator Studio (Tenfold), which this
  skill installs and sets up for PropFuel. Use when someone says "edit this
  video", "edit these clips", "make a reel from this", "cut this down",
  "add captions", "edit it in Color Block", or wants Creator Studio set up.
---

# Reel editor (PropFuel)

Raw 9:16 clips in, finished reel out, in PropFuel's house styles. The editing engine is
**Creator Studio** by Tenfold Marketing (Marc Cleroux). PropFuel's team is licensed to use it
(Alex cleared it with Marc, 2026-10-20). This skill installs it, sets it up the PropFuel way and
adds PropFuel's rules on top. It contains none of Creator Studio's code.

## 1. Is Creator Studio installed?
Check for the `video-studio:video-studio` skill (or `~/.claude/plugins/cache/creator-studio/`).
Missing: the person runs these two lines themselves in Terminal (not inside Claude), then starts
a new Claude Code chat:
```
claude plugin marketplace add tenfoldmarc/studio-plugin
claude plugin install video-studio@creator-studio
```
Desktop app instead: Code tab > + > Plugins > Browse plugins > Add > Add marketplace > Add from a
repository > `https://github.com/tenfoldmarc/studio-plugin` > Sync > install **Creator Studio**.

## 2. First-time setup, the PropFuel way
Run `/video-studio setup` (the `video-studio:video-studio` skill) and follow its Step 0 (the
quiet check + background download, about 3 GB one time). Then, instead of its welcome questions
and style building:
1. **Folders.** Write the Studio `config.json` (path in its `.platform.json` as `config`; keep
   any keys already there): `"clipsDir": "~/Downloads"`, `"projectsDir": "~/Desktop/PropFuel/03 Video/Reel Edits"`.
   Create that folder if missing. Ask only if they want different folders.
2. **House styles.** Copy each folder in `${CLAUDE_PLUGIN_ROOT}/skills/reel-editor/house-styles/`
   into `<state_dir>/styles/` (`state_dir` from `.platform.json`). Never overwrite a style folder
   that already exists there; say it was kept. Then run
   `PY "<SK>/scripts/my_styles.py" default "Show and Tell"` and `my_styles.py list` to confirm.
3. **Clean cutout.** Show and Tell needs it: `PY "<SK>/scripts/setup.py" --matting` if Step 0
   said `clean cutout NOT SET UP` (the prefetch usually covers it).
4. Tell them in two lines: their styles (Show and Tell default, Color Block, Viral Guy) and
   "drop clips in and say edit it, or edit these in Color Block".

## 3. Every edit
Follow the Creator Studio skill's workflow ("edit it"). PropFuel rules win over it where they differ:
- **Never post.** Do not use its posting (`post.py`, Zernio) for PropFuel accounts. Deliver the
  files; the person posts.
- **Alex approves before anything ships** publicly (ads, social, website). Give him the phone copy.
- **Client footage needs written consent** (Testimonial Library rule) before it is used anywhere public.
- **Numbers on screen** only from the ROI - Master and Case Studies - Master docs (`get_knowledge`).
  "370+ associations", never another count. Growth stat: "12% avg annual revenue growth after
  implementing PropFuel" next to "vs 0.98% for the average association". Tagline: "Know and Grow
  Your Membership". Never invent numbers, comments or results.
- **Captions say what was said.** Fix mishearings: PropFuel (not "prop fuel"/"proper fuel"),
  Claude (not "cloud"). Pass `"PropFuel, Claude, <client names>"` to `transcribe_cut.py`.
- **No AI-generated footage, people or voices** (Oct 12 rule). Editing real footage is fine; the
  Studio's GIFs and effects are fine as long as nothing claims to be a real person or client.
- No em dashes in on-screen text. No single word alone on a caption's last line.

## 4. Team style changes
A note meant for every PropFuel reel ("always", "from now on") goes into the house style here, not
only the person's local copy: update `house-styles/<style>/style.json` / `style.md`, bump the
plugin version, and follow the save-skill recipe so everyone gets it. Personal one-offs stay local.

## 5. Log it
When a reel is delivered: `log_update` with one line (what, which style, where the file is).

## Changelog
- 2026-10-20: created from Alex's setup session. House styles = his Studio Picker picks
  (Show and Tell with The Stack + Pointer Callout; Color Block; Viral Guy).
