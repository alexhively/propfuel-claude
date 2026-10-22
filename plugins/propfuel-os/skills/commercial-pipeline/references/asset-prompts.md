# Stage 1 — asset image prompts

Reference images carry identity. The video prompt carries behaviour. Everything a reference gets wrong has to be fought in every segment afterwards, so the cheapest place to fix a film is here.

## House format

Plain text in one code block. Section labels in CAPS on their own line, prose underneath. No markdown, no bullets, no bold inside the prompt.

```
[one declarative opening line — what this image is]
BACKGROUND LOCK
SUBJECT
[MATERIAL or PACKAGING LOCK — if the asset has a paired state]
[SCALE LOCK — if relative size is the point]
LIGHTING
COMPOSITION
STYLE
NEGATIVE
ASPECT RATIO
```

Not every asset needs every section. Order does not vary.

## The four rules that matter

**1. Flat light on anything that travels.** Products and characters appear under every lighting state in the film. Bake a dramatic key into the reference and the model fights it in every segment, or worse, carries the reference's lighting into a scene lit the opposite way. Use the anti-studio block:

```
LIGHTING
This is not a studio photoshoot. No studio lights, no softboxes, no flash, no hard
directional key, no dramatic highlights. Plain ordinary soft ambient light wrapping
the subject evenly from all sides, gentle and uniform, no visible light direction,
no hotspots, no deep shadows. The only shadow in the image is a faint soft natural
contact shadow directly beneath the subject.
```

The location is the exception. It does not move through the film, so it is where the lighting design gets established, and it should be lit dramatically and deliberately.

**2. Redundancy beats precision on backgrounds.** Models leak environment into product shots. State the background four ways in one paragraph — behind, beneath, to the edges, and what it is not:

```
BACKGROUND LOCK
The entire background is seamless pure white: white behind the subject, white
surface beneath it, white to every edge of the frame. No room, no table, no walls,
no props, no textures, no gradients, no color anywhere in the background — only the
subject on infinite clean white, like a catalog product cutout photo.
```

**3. Paired assets share paragraphs verbatim.** If a before and after must read as the same object transformed, the paragraph describing the shared material is copied word for word into both prompts. Same sentences, same order, same adjectives. Two separately-written descriptions of "plain kraft cardboard" will produce two different cardboards, and the reveal will look like a swap instead of a change.

Identify the shared paragraph explicitly when delivering, so the user knows which block to carry across.

**4. Scale is a video-prompt problem.** Generate a machine, vehicle or prop at its real size. Trying to make an image look enormous produces distortion and breaks the object's own geometry. The size override goes in the reference line in Stage 2:

```
In this film the machine is COLOSSAL — the size of a two-story building, each drum
over 4 meters tall, utterly dwarfing every person in the scene, yet built from real
steel with real weight, rivets, hydraulics and wear.
```

## By asset class

### Product

Pure white, catalogue cutout, flat light, no branding unless the brand asset is the point. If the product sits in or on something — packaging, a vessel, a stand — that container gets its own LOCK paragraph, because it is the thing most likely to drift between the before and the after.

If the relationship between two objects is the idea (oversized item in undersized container, tiny item in huge space), write a SCALE LOCK that states the contrast in physical terms — what reaches where, what overflows, what cannot close — rather than adjectives like "huge" and "tiny".

Aspect: 1:1 for pairs that will cut together.

### Character

A three-view sheet: full-body front, full-body back, head-and-shoulders close-up. Plain light grey background, flat ambient light, identical clothing and proportions across all three views.

Keep the identity anchor list short — four or five items. These same anchors get repeated verbatim in the Stage 2 reference line, so they need to be things the image can actually carry: glasses shape, hair, one distinctive garment, gloves, a held prop.

Add a **performance lock** alongside the look, because it costs the video model nothing and is where character comedy or tone lives: *deadpan, never smiling, no exaggerated reactions*.

Character sheets frequently generate with a missing or malformed front-view head. The close-up carries the face, so this is usually survivable, but check it and flag it.

### Location

The one asset that should be lit dramatically. It establishes the palette and direction everything else inherits.

Generate it **empty of the action**. The central playing area must be clear end to end — every crate, cable and pallet left in the path is one more object the video model has to simulate when something moves through it, and one more chance for the segment to break.

Do not worry about generating background people. Add them in the Stage 2 LOCATION MAP instead, where they can be described as behaviour rather than fixed positions.

Aspect: match the film. 16:9 or 2.39:1.

### Machine, vehicle or hero prop

Three-quarter view, entire object in frame, nothing cropped or occluded. Flat light. Real material wear — chipped paint, dust in the seams, oxidised metal — because clean CAD-looking machinery reads as CGI immediately.

This is the asset class with the widest spread between image models. If the budget allows, run the same prompt through three or four different models and compare before locking one.

No branding, no decals, no numbers. Text is what image models mangle.

### Logo

Never generate it. Use the client file. A regenerated logo is wrong in a way everyone at the client will notice instantly.

## Delivering a Stage 1 artifact

Name the model, say batch 4, then give three specific things to judge on — not "which looks best". Good judging criteria are binary and check the thing the prompt was fighting for: *is the box unmistakably undersized without the product looking crushed, is the board clean and unbranded, is the white truly white to every edge.*

Close with a one-line statement of assumptions, and name which paragraph is the shared one if the asset is half of a pair.
