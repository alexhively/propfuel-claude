---
name: li-repurpose
description: >-
  Turn one long asset - a YouTube video, podcast, newsletter, blog post,
  transcript or client call - into a week of LinkedIn posts. Use when the user
  says "repurpose this", "turn this into posts", "I have a video/newsletter/
  transcript", or pastes a long piece of content and wants it on LinkedIn.
metadata:
  origin: linkedin-agent-skill
---

> **PropFuel adaptation.** From the LinkedIn Agent Skill (github.com/avi691/linkedin-agent-skill, MIT, by Avi Grondin and Jake Schincariol; license in `li-human/LICENSE-linkedin-agent-skill`). PropFuel rules win over anything below.
>
> 1. **Load the brain first.** If the PropFuel Marketing OS connector is available, call `get_knowledge` "LinkedIn - Master.md" before anything else, then the matching LinkedIn KB doc(s) for this job: formats-playbook, topic-authority-and-pillars (named "LinkedIn KB - <topic>.md"; if a name doesn't match, check the knowledge list). The Master doc wins over the generic advice in this skill where they differ.
> 2. **Voice.** Use `~/.claude/linkedin/voice.md` if the person has one (their personal voice for their own profile). Otherwise, and always for the PropFuel company page, use `${CLAUDE_PLUGIN_ROOT}/skills/li-post/propfuel-voice.md`, which comes from the Brand Persona and Core Message masters.
> 3. **Hard rules.** Say "370+ associations", never another count. The tagline is "Know and Grow Your Membership". Numbers only from the ROI - Master and Case Studies - Master docs, never invented. Clients may be named without a live case study. No client quote or testimonial without written consent. Never post, comment, connect or send a DM: every skill ends with copy the person reads, approves and pastes themselves.
> 4. **Log it.** When a post, plan or audit is done, record one line in the OS with `log_update`.

# li-repurpose

One good long asset contains four to six posts. Most people extract one and
throw the rest away.

## Input

A transcript, an article, a newsletter, a script, a call summary. If the user
gives a YouTube URL and there is a transcript tool available in the session,
use it; otherwise ask them to paste the text. Read the whole thing before
extracting anything.

## Extract, do not summarise

A summary of a video is not a post. Nobody wants the summary. Go through the
asset and pull out the things that stand alone:

| pull | what it is |
| --- | --- |
| **Claims** | every sentence that would start an argument |
| **Numbers** | every figure, cost, duration, percentage |
| **Stories** | every moment with a person, a scene and a cost |
| **Mechanisms** | every "the way this works is..." explanation |
| **Mistakes** | every admission of something that went wrong |
| **Lines** | every sentence that is already quotable as-is |

List what you found, with counts, before writing anything. If the asset yields
fewer than four items, it is thin, and four posts squeezed out of it will be
thin too. Say that.

## Then build the week

Each extract becomes one post, and each post has to stand completely on its
own - the reader has not seen the video and never will. Never write "as I
mentioned in my latest video". The post is the thing.

Assign a hook formula from `li-post/hooks.json` to each, and vary them: five
posts from one source with the same hook shape reads as a content mill.

Order them across the week so the strongest claim goes first, the story goes
midweek, and the mechanism post goes last, when people who liked the earlier
ones are watching for it.

## Output

```
SOURCE: "Why we killed discovery calls" (18 min, 3,400 words)

FOUND  4 claims, 6 numbers, 2 stories, 3 mechanisms, 1 mistake, 5 quotable lines

WEEK
TUE  #1  Contrarian    Discovery calls are a tax you pay for a bad website
WED  #17 Time Anchor   We got 6 hours a week back by deleting one calendar link
THU  #9  Cold Open     "Can we just hop on a quick call?"
FRI  #21 Direct Value  The 4-question form that replaced the call. Steal it.

Say "write Tuesday" and I will draft it.
```

Then draft on request, one at a time, each through `/li-post` and `/li-human`.
Do not dump four finished posts at once - they will all sound the same, and
the user will edit none of them.
