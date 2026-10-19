---
name: email-voice
description: Learn how a person really writes email from 5-20 of their own sent emails, save a private voice profile (tone, greetings, sign-offs, rhythm, words they use and never use), then write every email draft in that voice. Use when someone says "learn my email voice", "build my email voice", "update my email voice", "write this like me", or asks Claude to draft, reply to or follow up on any email. Drafts only; never sends.
---

# Email Voice

Claude drafts email that sounds like the person who will send it, not like Claude. It learns from their real sent mail once, keeps a private profile, and reads that profile before every draft.

## Where the profile lives (private, never shared)
- **Claude Code:** `~/.claude/email-voice/<firstname>.md` (lowercase first name, e.g. `alex.md`). Create the folder with `mkdir -p ~/.claude/email-voice && chmod 700 ~/.claude/email-voice`.
- **claude.ai:** paste the profile into your own personal Claude Project's instructions (not a shared team project), or ask Claude to remember it in your memory.
- **Never** put a profile in a git repo, the Marketing OS (`update_knowledge`), a shared Claude Project, Slack or Drive. It quotes real emails.

## A. Build the profile ("learn my email voice", or no profile exists yet)
1. **Check the mail tool.** Gmail tools must be connected (claude.ai: Settings > Connectors > Gmail; in Claude Code they show as `mcp__claude_ai_Gmail__*`). If they are missing, say so and stop. Read only the signed-in person's own mailbox.
2. **Find samples cheaply.** `search_threads` with `in:sent newer_than:90d -subject:(Accepted OR Declined OR Invitation OR "Out of office" OR "Automatic reply" OR Fwd OR TEST) -from:noreply`, `pageSize` 30-40, default (minimal) view. Pick 5-20 threads where the person wrote real prose. Skip:
   - auto-replies, calendar invites and booking confirmations
   - forwards with no note of their own, newsletters, test sends, marketing emails sent from a tool
   - one-word replies (keep a couple, they show the "quick reply" style)
   - Aim for a mix of audiences: teammates, clients or prospects, vendors, strangers, personal.
3. **Read only what they wrote.** `get_thread` with `messageFormat: PLAIN_TEXT`. Keep only messages where the sender is the user, and cut each one at the first quoted line (`On <date> ... wrote:`, `From:`, lines starting with `>`). Threads can be huge (100K+ characters); if a result is saved to a file, pull just the user's messages with `jq` instead of reading the whole file.
4. **Analyse** across all samples. Count, don't guess: how many open with "Hi", how many sign off "Best", how many use `!`, any emoji, any em dashes. Note how style shifts by audience (team vs external vs personal) and by length (quick reply vs full email).
5. **Write the profile** in exactly this shape:

```markdown
# Email voice: <First name>
Built <YYYY-MM-DD> from <N> sent emails (<date range>). Private: never share or commit.

## TONE
<warm vs direct; how it shifts by audience; energy level>

## GREETINGS
- Default: ...
- Groups: ...
- Strangers / first contact: ...
- Quick replies: ...

## SIGN-OFFS
- Default: ... (count)
- When asking for something: ...
- Quick replies: ...
- Never: ...

## SENTENCE STYLE & RHYTHM
- Paragraph length: ...
- Punctuation: ... (exclamation marks, question style, lists)
- Emoji: ...
- Em dashes: ...
- Other habits: ...

## WORDS THEY USE
- ...

## WORDS THEY NEVER USE
- ...

## EXAMPLE LINES (anonymized)
- "..."  (3-5 lines, each under ~25 words)

## DRAFTING CHECKLIST
- <5-7 one-line rules Claude checks every draft against>
```

6. **Anonymize the example lines** before saving: replace people, clients, associations, companies, deal terms, amounts, dates, emails, phone numbers, addresses and links with `[Name]`, `[Org]`, `[date]`, `[amount]`, `[link]`. Keep the person's own phrasing and punctuation. No full emails in the profile, only short lines.
7. **Save** to the location above. Tell the user the path, show the TONE / GREETINGS / SIGN-OFFS lines, and ask if anything feels off. Fix what they correct; their corrections beat the analysis.
8. **Make it stick.** So every later session uses it, add one pointer line (ask first if the file is shared):
   - Claude Code: in the user's auto-memory, or `~/.claude/CLAUDE.md`: `Before drafting any email, read ~/.claude/email-voice/<name>.md and follow it.`
   - claude.ai: the profile in personal project instructions or memory already does this.

## B. Draft in their voice (every email, every time)
1. Read the profile first. If none exists, offer to build one (section A); if they decline, draft plainly and say it's not in their voice yet.
2. PropFuel content rules still apply on top of the voice: for anything about PropFuel, start from the Marketing OS (`get_briefing`, the Master docs), "370+ associations", numbers only from the ROI and Case Studies masters, clients may be named without a live case study, no invented stats or quotes.
3. Write the draft, then check it against the DRAFTING CHECKLIST: greeting, sign-off, paragraph length, exclamation and emoji habits, em dashes, banned words. Fix before showing it.
4. Deliver as a Gmail draft (`create_draft`, or `replyToMessageId` for a reply) or a copy-ready block. Say which.

## C. Update ("update my email voice")
Re-run section A on sent mail newer than the profile's "Built" date (plus enough older mail to reach 5-20 samples), keep any rules the user set by hand, bump the Built line, and list what changed.

## Hard rules
- **Never send.** No `send_message`, no `forward`, no `reply` that sends. Drafts only; the person sends.
- Read only the user's own sent mail. Never someone else's mailbox, never their inbox for "voice".
- Profiles stay private (see above). Never paste one into OS knowledge, a repo, Slack or a shared doc.
- Strip client names, emails, phone numbers and deal details from anything saved.
- Voice changes how it sounds, not what's true: no new facts, promises, prices or dates the user didn't give.

## Changelog
- 2026-10-15: created (Alex). Tested on Alex's sent mail; profile at `~/.claude/email-voice/alex.md` (private).
