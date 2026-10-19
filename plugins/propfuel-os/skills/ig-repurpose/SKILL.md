---
name: ig-repurpose
description: >-
  Turn one long asset - a YouTube video, podcast, livestream, newsletter, blog
  post or client call - into a week of reels and carousels. Use when the user
  says "repurpose this", "turn this into reels", "I have a video/podcast/
  transcript", "cut this up", or pastes something long and wants it on
  Instagram.
metadata:
  origin: instagram-agent-skill
---

> **PropFuel adaptation.** From the Instagram Agent Skill (github.com/Jakeschincariol/instagram-agent-skill, MIT, by Jake Schincariol; license in `ig-human/LICENSE-instagram-agent-skill`). PropFuel rules win over anything below.
>
> 1. **Load the brain first.** If the PropFuel Marketing OS connector is available, call `get_knowledge` "Instagram - Master.md" before anything else, and "Skill - instagram.md" for the workflow detail on repurposing. The Master doc wins over the generic advice in this skill where they differ. If the name doesn't match, check the knowledge list.
> 2. **Voice.** Use `~/.claude/instagram/voice.md` if the person has one (their personal voice for their own account). Otherwise, and always for the PropFuel company account, use `${CLAUDE_PLUGIN_ROOT}/skills/ig-caption/propfuel-voice.md`, which comes from the Brand Persona and Core Message masters.
> 3. **Hard rules.** Say "370+ associations", never another count. The tagline is "Know and Grow Your Membership". Numbers only from the ROI - Master and Case Studies - Master docs, never invented. Clients may be named without a live case study. No client quote, testimonial or client footage without written consent. Never log into Instagram, never post, comment, reply, DM or schedule anything, and never set up automation on anyone's behalf: every skill ends with copy the person reads, approves and posts themselves. It writes, you post.
> 4. **Scripts** in this pack are stdlib-only and run locally: `python3 -I "${CLAUDE_PLUGIN_ROOT}/skills/<skill>/<script>.py" …`. Nothing is uploaded.
> 5. **Log it.** When a reel, plan or audit is done, record one line in the OS with `log_update`.

# ig-repurpose

One good long asset contains four to six posts. Most people extract one and
throw the rest away.

## Input

A transcript, an article, a newsletter, a script, a call summary, a livestream.
If the user gives a URL and this session has a transcript tool, use it;
otherwise ask them to paste. Read the whole thing before extracting anything.

If the source is a video the user owns, ask for the file too. A Reel built on
their own footage beats one built on their own words read again.

## Extract, do not summarise

A summary of a video is not a Reel. Nobody wants the summary. Go through the
asset and pull out the things that stand alone:

| pull | what it is |
| --- | --- |
| **Claims** | every sentence that would start an argument |
| **Numbers** | every figure, cost, duration, percentage |
| **Stories** | every moment with a person, a scene and a cost |
| **Mechanisms** | every "the way this actually works is..." |
| **Mistakes** | every admission of something that went wrong |
| **Lines** | every sentence already quotable as-is |

List what you found, with counts, before writing anything. If the asset yields
fewer than four items, it is thin, and four posts squeezed out of it will be
thin too. Say that.

## Then pick the format per extract

Not everything is a Reel.

- **Claim, mistake, story** to a Reel. They need a voice and a face.
- **Mechanism, numbered list** to a carousel. They need to be re-read.
- **A quotable line** to a story frame, not a post.

## Then build the week

Each extract becomes one post and each post stands completely on its own. The
viewer has not seen the source and never will. Never write "as I said in my
latest video". The post is the thing.

Assign a hook formula from `ig-reel/hooks.json` to each and vary them. Five
posts from one source with the same hook shape reads as a content mill, because
it is one.

If the source is the user's own video, **use the actual footage**. The clip
where they said the thing, with the real reaction in it, beats a re-record
every time. Cut on the sentence, not on the breath.

Order across the week so the strongest claim goes first, the story lands
midweek, and the mechanism goes last, when the people who liked the earlier
ones are watching for it.

## Output

```
SOURCE: "Why we killed discovery calls" (42 min podcast, 8,900 words)

FOUND  5 claims, 9 numbers, 3 stories, 4 mechanisms, 2 mistakes, 7 quotable lines

WEEK
TUE  REEL      #2  Negative Command  Stop running discovery calls
                                     use the 14:20 clip, he laughs at the end
WED  CAROUSEL  Job B caption         The 4-question form that replaced the call
FRI  REEL      #21 Mid-Sentence      "...and he asked for a refund nine days later"
SUN  REEL      #5  Time Collapse     Six hours a week back, one deleted link

Say "write Tuesday" and I will draft it.
```

Then draft on request, one at a time, each through `/ig-reel` and `/ig-human`.
Do not dump four finished scripts at once. They will all sound the same and the
user will shoot none of them.
