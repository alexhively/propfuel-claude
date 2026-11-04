---
name: gong-promo
description: Turn a Gong call link into a finished vertical promo clip of a client talking, posted as a DRAFT to Slack #testimonial-drafts. Use when someone pastes a Gong call link and says "make this a promo video for PropFuel", "cut a clip from this call", "testimonial clip from this Gong". Picks the strongest 15-30 s client moment, lets you choose, renders 9:16 with verbatim captions, a name tile and the approved PropFuel logo sting, QA's it, and submits it as a draft. Claude Code only; needs ffmpeg.
---

# Gong link to promo clip (draft)

You paste a Gong call link; you get a 1080x1920 clip of a **client** talking in the approved cream "Client stories" style (headline quote with the yellow highlight, gold-ringed call window with the "Recorded client call" tag, dark caption pill, name card, PropFuel logo sting end card), sitting as a draft in #testimonial-drafts for Alex and Brittany. Nothing goes public from this skill.

## Hard rules
- Draft only. This skill never posts anywhere but #testimonial-drafts (via `submit_proof`), never uploads to YouTube or Meta, never emails a client. Consent is left "not asked": nothing with a client's face or words goes public until the client says yes and Alex or Brittany approve.
- The speaker is a **client** (Gong side `client`), never PropFuel staff. Use the OS tool's speaker data, not your guess from the transcript.
- Captions are the words spoken, verbatim. Never paraphrase, tighten or fix grammar inside quote marks. Allowed: capitalise PropFuel, drop Gong's "..." marks.
- Never clip a word's tail: the script cuts on the measured end of the last word plus real room tone, then fades. Never hand-set an end time that skips this.
- **Required QA step, every render: "Are you cutting off at the end before they're done speaking?"** Transcript end-times run early or late and hide the decay of a last word (Alex, Nov 3: clip after clip still cut people off). The render refuses to write a clip that fails the end check (tail is room tone, the last word has decayed, the last transcribed word is the quote's last word) and prints `End check: last word '<word>' completes at <t>s, fade at <t>s, tail room tone <dB> -> PASS/FAIL`. Never bypass it; a FAIL means move the out point to the measured energy decay, then re-render.
- No mid-phrase pauses (the script cuts gaps over 0.7 s between sentences; watch for pauses inside a sentence, see QA).
- Numbers: "370+ associations"; the growth stat is "12% avg annual revenue growth vs 0.98% for the average association". Never the line "See One Question in 87 Seconds". Don't add stats the client didn't say; a stat in the clip must be what they said.
- Gong credentials never leave the OS. You never ask for or handle a Gong key.

## Step 0: setup check
1. `ffmpeg -version` and `ffprobe -version`. Missing: tell the person to run `brew install ffmpeg` (no Homebrew: https://brew.sh), then continue.
2. `python3 -c "import PIL, numpy"`. Missing: `python3 -m pip install --user pillow numpy`.
3. `SK="${CLAUDE_PLUGIN_ROOT}/skills/gong-promo"`; `python3 "$SK/scripts/promo.py" check` should print "python deps ok".
4. The OS connector must be connected (`get_briefing` works). Work in a scratch folder, e.g. `mkdir -p ~/gong-promo/<org-slug>`.

## Step 1: pull the call
`gong_call_media {call: <link>, side: "client"}`. Returns `speakers`, the client's `transcript` as `[start_s, end_s, text]` sentences, and `media.url` (Gong's link, about 8 hours).
- `error: not_found` → the link is wrong or the call isn't visible to PropFuel's Gong key; ask for the link again. `internal_call` → no client on it; stop. `no_transcript` → Gong is still processing; try later. `media: null` → no recording; stop and say so.
- "Gong is not connected to the OS yet" → Alex has to add the Gong key to the OS; tell the person to ask him. Do not look for a key anywhere else.
- Download now: `curl -L --fail -o ~/gong-promo/<org>/call.mp4 "<media.url>"` (if `kind` is audio, name it call.m4a: the clip then uses the name tile instead of the face).

## Step 2: choose the moment
Read the client transcript (and the angle the person gave, e.g. "renewals"). Look for 15-30 s of one client speaking: a result, number, before/after, or a plain "why we use it", that stands alone with no context. Prefer a specific result over praise. Skip anything confidential, negative about a named person, or about pricing or contracts.
Show the person: the best pick as the exact quote, its start-end in mm:ss, who said it and their org, plus 1-2 alternates in the same form. Ask which one (or "none"). Wait for the answer. Choose whole consecutive sentences by the same client; they are `sentences` in the spec.
Also write the **headline** (`head`): a short run of words the client actually said, in order and untouched, ideally the punchiest line; wrap the 2-4 words that carry the point in [brackets] for the yellow highlight, e.g. `Our numbers have [pretty much doubled.]`. The script refuses a headline that isn't contiguous spoken words. The look is fixed: don't restyle it.

## Step 3: render
1. If the recording is video: find the speaker's tile. Gong records a gallery, or a screen share with a small active-speaker tile (often top right: the Elevate screen share was `[1600, 0, 320, 180]` on a 1920x1080 recording). Grab a frame in the quote: `ffmpeg -ss <t> -i call.mp4 -frames:v 1 frame.jpg`, open it, and give `face` as `[x, y, w, h]` of the speaker's tile in source pixels. No clear tile, or audio only: omit `face`.
2. Write `spec.json`: `src` (the downloaded file), `out` (clip.mp4), `person`, `org` (shown as "<org> · PropFuel client"), `head`, optional `face`, `sentences` (copied from the tool output, text untouched).
3. `python3 "$SK/scripts/promo.py" render spec.json`. It prints the cut points, the room tone kept after the last word, and how much of the clip shows the speaker's face (staff faces that Gong flashes up under the client's words are replaced by the name tile automatically).
   - "the speaker runs on": the sentence has no pause after it. End the quote one sentence earlier or later and re-run.
   - "caption too wide" or "headline must be words said": fix the spec and re-run.
   - A clip over ~30 s: pick a shorter moment.
4. The end card is the approved v4 logo sting (icon animation with its sound, then the tagline and Book a demo button). Don't swap it.

## Step 4: QA before posting
0. **Are you cutting off at the end before they're done speaking?** Read the `End check:` line from step 3: it must say PASS. If the line is missing or no local whisper was found, the transcript half of the check did not run: say so, and also read the last 3 seconds aloud against the quote (`ffplay -ss <end-3> -t 4 -nodisp clip.mp4`) before submitting.
1. `python3 "$SK/scripts/promo.py" qa clip.mp4 sheet.jpg`. It checks size, codec, length and that the voice has fully stopped in the room tone before the end card (a clipped last word fails). Fix and re-render on any FAIL.
2. **Open `sheet.jpg`** and look: every caption readable and inside the frame, the name and org right, the face (or name tile) is the client, the last frame is the logo end card. If you have a recent approved clip nearby (e.g. in the Testimonial Review folder), compare: it should look like the same family.
3. Caption timing inside a sentence is estimated (Gong gives sentence times, not word times). Scrub 2-3 spots: `ffmpeg -ss <t> -i clip.mp4 -frames:v 1 f.png` and compare the caption to what is said at that second (listen with `ffplay -ss <t> -t 4 -nodisp clip.mp4` if available). If captions drift or there is a long pause inside a sentence, pick different sentences.
4. Layout is the house 9x16 layout (content inside x 40-1040, y 200-1560); the script refuses anything that runs outside it.

## Step 5: post the draft
Key: `testimonial:gong-<callid>:<org-slug>-<mmss>`.
1. `proof_upload_url {key, filename: "clip-9x16.mp4"}`, then run the returned `curl` from the clip's folder. Keep the `pathname`.
2. `submit_proof` with: `key`, `kind: "testimonial"`, `org`, `person`, `role`, `quote` (the exact words, same as the captions), `title` (e.g. "<Org>: <highlight>"), `call_date` (YYYY-MM-DD from the call), `evidence: [{label: "Gong call at mm:ss", url: <call link>}]`, `video: {path9x16: <pathname>}`. Leave `consent_given` and `consent_asked` out unless the client really said yes or was asked on that call (then follow the tool's description).
3. Tell the person, in plain words: it's a draft in #testimonial-drafts for Alex/Brittany to approve; nothing with the client's face or words goes public until the client agrees and one of them approves; the clip file is at <path> if they want to look again.
Optionally `log_update` one line ("Cut a promo clip from <org> call, draft posted").

## Changing a draft
Re-render, upload again (same key), `submit_proof` with the same key: it updates the card (a reposted clip lands in the card's thread if changes were requested).
