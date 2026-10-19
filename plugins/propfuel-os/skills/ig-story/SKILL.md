---
name: ig-story
description: >-
  Write the day's Instagram Stories - the frame-by-frame sequence, which
  stickers to use where, and the one that moves people into the DMs. Use when
  the user says "stories", "what do I post on my story", "story sequence",
  "poll idea", "I have nothing to story about", or wants to sell something
  without making a post about it.
metadata:
  origin: instagram-agent-skill
---

> **PropFuel adaptation.** From the Instagram Agent Skill (github.com/Jakeschincariol/instagram-agent-skill, MIT, by Jake Schincariol; license in `ig-human/LICENSE-instagram-agent-skill`). PropFuel rules win over anything below.
>
> 1. **Load the brain first.** If the PropFuel Marketing OS connector is available, call `get_knowledge` "Instagram - Master.md" before anything else, and "Skill - instagram.md" for the workflow detail on Stories. The Master doc wins over the generic advice in this skill where they differ. If the name doesn't match, check the knowledge list.
> 2. **Voice.** Use `~/.claude/instagram/voice.md` if the person has one (their personal voice for their own account). Otherwise, and always for the PropFuel company account, use `${CLAUDE_PLUGIN_ROOT}/skills/ig-caption/propfuel-voice.md`, which comes from the Brand Persona and Core Message masters.
> 3. **Hard rules.** Say "370+ associations", never another count. The tagline is "Know and Grow Your Membership". Numbers only from the ROI - Master and Case Studies - Master docs, never invented. Clients may be named without a live case study. No client quote, testimonial or client footage without written consent. Never log into Instagram, never post, comment, reply, DM or schedule anything, and never set up automation on anyone's behalf: every skill ends with copy the person reads, approves and posts themselves. It writes, you post.
> 4. **Scripts** in this pack are stdlib-only and run locally: `python3 -I "${CLAUDE_PLUGIN_ROOT}/skills/<skill>/<script>.py" …`. Nothing is uploaded.
> 5. **Log it.** When a reel, plan or audit is done, record one line in the OS with `log_update`.

# ig-story

Stories are not a smaller feed. The feed is how strangers find you. Stories are
how the people who already follow you decide whether you are a person worth
buying from, and they are the only surface on Instagram where a tap turns into
a conversation in one move.

Nobody outside your followers sees these, so the job is completely different:
depth, not reach.

## The daily shape

Three to seven frames a day. Beyond about seven, the tap-forward rate climbs
and the last frames play to nobody, which is exactly where people put the ask.

```
1       THE OPEN     something happening today, with a face or a hand in it.
2-3     THE MIDDLE   the actual content: the process, the result, the mistake.
4       THE ASK      one sticker. Poll, question box, quiz or link.
5       THE CLOSE    the answer, the outcome, or tomorrow's setup.
```

Put the ask at frame 4, not frame 7. Completion drops with every tap and the
ask should be seen by the people who are still there.

## The stickers, and what each is actually for

| sticker | job | use when |
| --- | --- | --- |
| **Poll** | the cheapest tap there is | you want volume of response, not information |
| **Question box** | harvesting the exact words people use | you need content ideas or objections, verbatim |
| **Quiz** | teaching by letting them be wrong | there is a common misconception in the niche |
| **Slider** | vibe check | nothing important. Fun, low value |
| **Link** | the only clickable surface besides the bio | there is somewhere real to go |
| **Countdown** | a deadline people can subscribe to | a launch, a live, a close date |
| **Add yours** | reach beyond your followers, occasionally | the prompt is one anyone in the niche can answer |

The question box is the most undervalued one in the list. Every answer is a
caption, a Reel hook or a DM opener written in the audience's own words. Feed
them to `/ig-reel` as formula #16.

## Rules

**PropFuel brand (company account and anything about PropFuel):** DM Sans throughout; cream backgrounds #F6F2E8 / #EAE4D8, charcoal text #2F2F2F, one gold accent #FBC02D. No other palette, no stock-photo clichés. Personal accounts may use their own look, but keep PropFuel slides on-brand.

- **A face or a hand in the first frame.** Text on a coloured background gets
  tapped through, and the first frame decides whether the rest get watched.
- **One idea per frame.** Reading a paragraph on a story is not a thing anyone
  does.
- **Keep text inside the middle.** On 1080x1920, nothing above y=250 or below
  y=1600. The profile row sits on top and the reply bar sits underneath.
- **Talk to one person.** "You" singular. Stories are the closest thing to a
  DM that is not one.
- **Do not repost your own feed post to stories with no comment.** It is the
  single most ignored frame on the platform. If you are pointing at a post, say
  what happened in the comments and why it is worth going back for.
- **Sell on stories, not in posts.** Three frames of context, one frame of
  offer, one frame of proof. That sequence sells more than a feed post about
  the same thing and costs you no reach.

## The DM funnel, done honestly

The sequence that works: a story that names a problem, a question box or a poll
that lets people say "that's me", and then a reply to each person who answered.
The conversation starts because they spoke first.

Automated keyword DM replies are a real, supported feature for professional
accounts, through Instagram's own tools and approved partners. Bulk DMing
people who did not interact is not, and it is what gets accounts restricted.
The rule is simple: **they act first, then you reply.**

## Output

The frames in order, each with what is on screen, what is said, and which
sticker, plus what to do with the answers:

```
STORIES  ·  Tuesday  ·  5 frames

1  [selfie, walking]      "Third refund request this year. Same reason."
2  [screen recording]     the clause, highlighted
3  [talking]              "Approval is a feeling. Delivery is a date."
4  [poll]                 "Have you been burned by a late approval?"  Yes / Not yet
5  [text on photo]        "Reply and I will send you the clause."

After: everyone who votes Yes gets a reply. That is the whole funnel.
```

Nothing is posted. The user posts it.
