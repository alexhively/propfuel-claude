---
name: commercial-pipeline
description: End-to-end workflow for producing a short AI commercial or branded film — planning the reference assets, writing the image prompts that generate them, writing the multi-segment video prompt that assembles them, and diagnosing what broke between generations. Use this whenever the user is working toward an ad, commercial, brand film, product video, promo, spot, or teaser with an AI video model (Seedance, Veo, Kling, Sora, Runway and similar), including when they only ask for one small piece of it — a product shot on white, a character sheet, a location plate, a machine reference, a video prompt, or a fix for a generation that came out wrong. Trigger even when the user never says "commercial" and just asks for something like "a burger in a box on white" or "make the box stop moving between shots", because those are stages of this pipeline and the house rules still apply.
---

# Commercial pipeline

A three-stage workflow for making short branded films with reference-driven video models. Every stage produces one artifact and names the next.

```
STAGE 1  ASSETS       image prompts → reference images, one per element
STAGE 2  VIDEO PROMPT one long structured prompt that assembles them
STAGE 3  FIXES        diagnose a bad generation, rewrite only what broke
```

The pipeline exists because video models cannot hold identity, geography and continuity from prose alone. Identity is moved out of the video prompt and into images. What remains in the video prompt is behaviour, timing and rules.

This skill writes **prompts**. It never generates anything and never calls a generation tool. The user pastes every prompt into their own image generator, and the video prompt into Seedance 2.5.

## Reading order

Read the reference file for the stage you are in. Do not read all of them.

| File | Read when |
|---|---|
| `references/asset-prompts.md` | Writing any image prompt — product, character, location, prop, machine |
| `references/video-prompt.md` | Writing or rewriting the video prompt |
| `references/fix-playbook.md` | The user reports a problem with a generation |
| `references/example-commercial.md` | Before writing a video prompt from scratch, for density and tone |

## On load, show the map first

**When the user invokes the skill by name with no concrete request** (`/commercial-pipeline`, "how does this work", "let's make a commercial"), the FIRST message opens with a one-line summary of what this skill is (a prompt-writing pipeline for short AI commercials: it plans the references, writes every image prompt, writes the one video prompt that assembles them, and fixes what breaks), then the AT A GLANCE table below, then what the user brings, THEN the opening question. Never jump straight into the question without showing the map. Write the map in the user's language.

**When the user arrives with a concrete request instead** ("a burger in a box on white", "the box keeps moving between shots"), skip the map. Produce first, exactly as described under *How to behave*, and close the turn with the progress line so they can see where that piece sits in the pipeline.

### AT A GLANCE

| Stage | What you get | What you do with it |
|---|---|---|
| 1 · Assets | An asset plan, then one image prompt per reference image (product, characters, location, machine) | Paste each into your image generator, batch of 4, keep the best |
| 2 · Video prompt | One long structured Seedance 2.5 prompt that assembles every reference into the full 30-second multi-cut film | Attach the references in the order shown, paste, batch of 4, keep the best |
| 3 · Fixes | A diagnosis of what broke and a rewrite of only the affected sections | Re-batch the rewritten prompt. Stop when a version is clean |

**What you bring:**

- The film in plain language: the product, what happens, how it ends. A few sentences is enough.
- The client's logo file. It is never generated.
- The name of the image generator you run. Video is Seedance 2.5.

**The opening question**, asked as one short message after the map:

> "Tell me the film in a few plain sentences: what the product is, what happens, how it ends. And which image generator do you run? Video goes to Seedance 2.5."

If the user names no image generator, suggest Nano Banana Pro once and keep it for the whole session. Then Stage 1 begins with the asset plan.

## How to behave

**Produce first, ask second.** The user asking for "a product on white" wants the prompt, not a discovery call. Write it, state assumptions in one line at the end, and let them correct. Ask a question only when the answer changes the whole artifact and cannot be assumed.

**One artifact per turn.** Deliver the current stage, then name the next stage in one line. Do not run ahead into stages the user has not reached. The one line is the progress line described under *Guiding the flow*.

**Every prompt goes in a single code block**, plain text, no markdown formatting inside it. The user is pasting this into a generation tool. Commentary lives outside the block.

**Always name the model and always say batch 4.** Identical prompts diverge hard. One generation tells you nothing about whether the prompt is good. The model and the batch size live in the settings table under every prompt; the video model is Seedance 2.5 unless the user names another.

**Always say what to judge the batch on** — three or four specific checks, in priority order. Never "pick the one you like best". A batch judged on prettiness selects for the wrong thing and the next iteration inherits it.

**Talk to the user in their language.** The prompts themselves stay in English regardless — that is what the models are trained on.

## Delivery format

Every prompt is delivered in this order:

1. **Bolded title line** naming the artifact: `**Asset 3 of 7, location plate, 16:9**` or `**Video prompt v2, 30s**`.
2. **One fenced code block**, the full prompt, plain text, nothing else inside it.
3. **The settings table, immediately BELOW the code block.** Below it, not above: the prompt is long, so the table stays visible at the bottom with the prompt right above it. Render it as a markdown table, never as prose.
4. **Judge on**, a short numbered list of the three or four checks for this batch, in priority order.
5. **The progress line.**

The settings table:

```
| Setting | Value |
|---|---|
| Model | <image generator for Stage 1 · Seedance 2.5 for Stage 2 and 3> |
| Aspect | <ratio> |
| Duration | <30s, Stage 2 and 3 only; drop the row for images> |
| Batch | 4 |
| Attachments | <none for most images · for the video prompt: 1) … = <<<image_1>>> · 2) … = <<<image_2>>>, in this order> |
```

Per-stage defaults:

| Stage | Model | Aspect | Duration | Attachments |
|---|---|---|---|---|
| 1 · Product, prop, machine | the user's image generator | 1:1 for pairs that cut together, else as the asset rules say | — | none |
| 1 · Character sheet | the user's image generator | per the asset rules | — | none |
| 1 · Location plate | the user's image generator | match the film, 16:9 or 2.39:1 | — | none |
| 2 · Video prompt | Seedance 2.5 | match the film, 16:9 default | 30s | every reference, numbered in handle order |
| 3 · Fix | Seedance 2.5 | unchanged | 30s | unchanged unless an asset was regenerated |

The attachments row for the video prompt is the one place the user learns which image is `<<<image_1>>>`, which is `<<<image_2>>>`, and so on. List them in handle order with a short descriptor each, so attaching is a matter of following the numbers.

On a Stage 3 rewrite, the code block contains the rewritten sections only when the fix is a targeted patch, or the full prompt when more than a couple of sections changed. Say which it is in the title line.

## Guiding the flow

After every artifact, close the turn with one progress line, so the user always knows where they are and what comes next. Keep it to one or two sentences, in the user's language, and make the next action a thing they can say or do.

- After the **asset plan**: `**Stage 1 · asset plan. Next → asset 1 of 7, the hero product on white. Say "go", or change the list first.**`
- After each **asset prompt**: `**Stage 1 · asset 3 of 7 delivered (location plate). Next → asset 4, the road roller. Say "next", or tell me what the batch did wrong.**`
- After the **last asset**: `**Stage 1 complete. Next → Stage 2, the video prompt. Tell me what actually generated for each asset (anything that differs from the plan), then I write the prompt.**`
- After the **video prompt**: `**Stage 2 · video prompt v1 delivered. Next → generate 4, judge on the checks above, and tell me what broke. That is Stage 3.**`
- After a **fix**: `**Stage 3 · v2, geometry lock rewritten. Next → re-batch 4. If the box holds, ship it. If not, tell me what you see.**`
- When a version is **clean**: `**Stage 3 · v3 is clean. Ship it. Anything you add now spends the complexity budget.**`

**Present the asset plan as a table** before the first prompt: number, asset, what it carries, aspect. The user corrects the list there, not seven prompts later.

| # | Asset | Carries | Aspect |
|---|---|---|---|
| 1 | Hero product on white | the thing being sold | 1:1 |
| 2 | Second product state | the after of the transformation, same packaging paragraph as 1 | 1:1 |
| 3 | Character sheet, scientist | identity anchors, three views, flat light | 16:9 |
| … | … | … | … |
| 7 | Logo | client file, never generated | — |

## Stage 1 — assets

Plan the full asset list before generating anything. A typical short commercial needs five to eight references:

- **Hero product** — the thing being sold, on pure white
- **Second product state** — if the film has a before/after, transformation or reveal
- **Characters** — one three-view sheet each, flat lighting
- **Location** — the set, empty of the action, lit the way the film will be lit
- **Machine or hero prop** — anything large or mechanical that the story turns on
- **Logo** — never generate this, use the client file

Each asset is a separate prompt and a separate batch. Full craft rules in `references/asset-prompts.md`. The rules that matter most:

- **References carry identity, prompts carry behaviour.** Do not bake camera drama into a reference. Product and character references get flat ambient light so they survive every lighting state in the film. The location is the exception — it does not move, so it establishes the lighting design.
- **Paired assets share paragraphs verbatim.** If a before and after must read as the same object, the packaging or material paragraph is copied word for word between the two image prompts. Designing them separately guarantees they will not match.
- **Scale lives in the video prompt, not the image.** Generate the machine at normal size and override it in its reference line later.

## Stage 2 — the video prompt

One long structured prompt in a fixed section order. Full architecture in `references/video-prompt.md`, worked example in `references/example-commercial.md`.

```
SCENE CONTEXT · ACTIVE REFERENCES · LOCATION MAP · GEOMETRY LOCK
FIRST FRAME AND SPATIAL BLOCKING · FORMAT MODE · EDIT ACCELERATION LOCK
OPTICS · LIGHTING PROGRESSION · CAMERA · ACTION TIMING
PHYSICS · AUDIO · POSITIVE LOCKS · global style tail
```

Spatial rules before camera style. Optics before aesthetic language. Lighting is a lock, not decoration. Everything critical appears twice — once where it applies, once in POSITIVE LOCKS.

**Assign the reference handles yourself.** The user should never have to work out which reference belongs in which segment.

**Write the assets you actually have, not the ones you planned.** Generated characters rarely match the brief exactly. Rewrite every reference line to describe what is in the image. A reference line describing a moustache that did not generate is worse than no reference line.

## Stage 3 — fixes

When the user reports a problem: name the failure, apply the fix, rewrite **only** the affected sections, say what to re-batch. Never re-roll an unchanged prompt.

The master rule, and the highest-value lesson in the whole workflow:

> **If something keeps breaking between cuts, stop describing it better inside every shot. Give it its own lock.**

Position, orientation, facing, speed, where a character stands, how fast the edit moves — anything that must survive multiple cuts gets promoted out of the segment descriptions into a named rule of its own, stated in absolutes. Adding more careful description inside each of sixteen segments does not work.

Full failure catalogue in `references/fix-playbook.md`.

## The complexity budget

Every prompt has one. Once a prompt is generating clean results, one more brilliant idea often just gives the model one more thing to get wrong. Individually good changes can add up to a worse film — more emotion means more character consistency to hold, more elaborate food shots mean more physics to get right, more camera variety means more instructions to follow.

Expect roughly ten generations for a thirty-second film, of which only three or four are actual prompt changes. The rest are re-rolls of a version already liked. When a version is clean, stop and ship it. If a change made things worse, revert to the last clean version rather than trying to fix forward.
