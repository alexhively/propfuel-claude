# Stage 2 — video prompt architecture

One long structured prompt. Read `example-commercial.md` before writing from scratch — it is the strongest available reference for density and section behaviour.

## Section order

```
SCENE CONTEXT
ACTIVE REFERENCES
LOCATION MAP
GEOMETRY LOCK
FIRST FRAME AND SPATIAL BLOCKING
FORMAT MODE
EDIT ACCELERATION LOCK
OPTICS
LIGHTING PROGRESSION
CAMERA
ACTION TIMING
PHYSICS
AUDIO
POSITIVE LOCKS
[global style tail]
```

Spatial rules before camera style. Optics before aesthetic language. Locks before the segments they govern, so the segments can reference them by name.

Sections in brackets below are conditional — include them when the film has the problem they solve.

## Reference handles

Handles are `<<<image_1>>>` … `<<<image_N>>>`, numbered in the order images are attached. Not `@tags`.

Every reference gets one line: identity anchors only, then the fidelity phrase.

```
<<<image_1>>>: older male scientist, thin build, oversized round thick clear-frame
safety glasses, greying dark hair swept back, white lab coat over a white shirt and
dark tie, blue nitrile gloves. Deadpan-serious, never smiling. 100% matches the
reference.
```

`100% matches the reference.` closes every line. Anchors only — the image already carries the face, and prose piled on top competes with it rather than reinforcing it.

**Describe what generated, not what was planned.** If the character sheet came back without the moustache you asked for, the reference line has no moustache. A reference line that contradicts its own image is worse than no reference line.

Two things ride on reference lines that people usually put elsewhere:

- **The scale override** goes inside the object's own reference line
- **The logo's permitted placements** are declared on its reference line, then repeated in POSITIVE LOCKS

## What each section does

**SCENE CONTEXT** — one paragraph, the whole film start to finish, in plain language. Concept, not craft.

**LOCATION MAP** — the location reference converted into geography: walls, doors, what is along which wall, where the empty playing area is, what the floor is. Name the important zones in caps (`THE ANALYSIS BENCH`, `THE TEST AREA`) so segments can reference them.

Include the living background here — *four to six people work at the benches, two or three walk across the depth*. A dead background reads as a render.

**GEOMETRY LOCK** — see below. Include whenever an object must hold position across cuts.

**FIRST FRAME AND SPATIAL BLOCKING** — what is on screen at frame one, stated as an image, plus `No empty establishing frame.` Then the geometry that must survive the whole film.

If the film has a threat, a machine or a payoff object, put it in frame one. *The first visible frame is a ground-level close-up: shoes entering from the left, and filling the entire background behind them, the vast curved steel wall of the roller's leading drum. The threat is legible in frame one.*

**FORMAT MODE** — segment count, runtime, cut types, and a ban on everything else: *sixteen scripted segments across 30.0 seconds, HARD CUTS and one INSERT CUT, every cut hidden in motion or motivated by a look. No fades, no dissolves, no unscripted cuts.*

**OPTICS** — one `LENS LOCK` line per segment, in **degrees of diagonal field of view**, never millimetres. Millimetres work on image models; video models want the observable optical outcome. Close with `No lens drift mid-segment.`

Rough map: 8° super-telephoto observation · 18° classic telephoto or macro insert · 29° short telephoto and product macro · 47° standard normal · 84° classic wide · 107° wide rectilinear.

For macro blocks, give each shot its own camera distance and downward angle in the lens lock. This is what stops six product shots collapsing into the same shot six times.

**CAMERA** — operator behaviour plus any global movement law. Worth stealing:

- *Every shot moves from its first frame* — with named exceptions. If some segments are true handheld, say so and say it overrides the smooth-camera rule *for those segments only*.
- Weight cues belong here, not in PHYSICS: *the frame carries a low continuous vibration caused by the machine's mass transmitting through the floor — machine weight, not handheld shake.*

**ACTION TIMING** — the body of the prompt. Every segment gets a range, an ID, a lighting tag, and an explicit cut marker between segments. Timings run to one decimal and every gap is filled, so the model is never left to invent a transition.

Write body mechanics the way a director would give a note — *one knee bending forward into a shallow lunge, the other leg braced behind, torso leaning over — never a deep squat* — because "he puts it down" produces a model-default crouch every time.

**PHYSICS** — mass, inertia, contact, materials. Viscosity, parabolic arcs, exhaust shimmer, and a restatement of anything about the environment that must not change.

**AUDIO** — write it as a sound-design pass in film order, not a list of nouns. SFX only unless asked.

**POSITIVE LOCKS** — every non-negotiable restated as a hard rule in plain declarative sentences. Everything here is also written inside the segment where it applies. Saying it twice is the point.

**Global style tail** — an unlabelled closing paragraph: format, grain, bokeh behaviour, framing law, cut law, absolutes. End on the hard ones — `NO CGI. NON-IP.`

## The lock catalogue

Locks are how a rule survives a cut. Each one is a named section or a named line, stated in absolutes, and restated in POSITIVE LOCKS.

### GEOMETRY LOCK

For any object that must hold position across cuts. The single most valuable section in the architecture.

Anchor to a **world landmark**, never to screen coordinates. Screen coordinates move when the camera moves, so a box locked to `x 68%, y 75%` will be dragged around the floor by the model trying to satisfy the coordinate. Anchor instead to a floor joint, a distance from another object, an alignment with a door.

```
FLOOR ANCHOR — governs S1 to S9
Position: on the concrete, eighty centimetres in front of the machine's leading
edge, directly in line with the centre of the doorway.
Orientation: open side faces SCREEN-LEFT. Lid stands upright at the BACK.
THE OBJECT NEVER MOVES OR TURNS.
The anchor is a place ON THE FLOOR, not a place in the frame. When the camera
moves, the object does not. Do not re-centre it, do not re-frame around it, do not
correct its position to match a previous shot's composition.
```

Four clauses earn their place:

- **A definition clause** — state that only ONE of the object exists in the film. Without it a duplicate appears on a bench in a wide shot.
- **Explicit negation of drift** — *it does not slide, rotate, shift, tilt, settle or get nudged.* Listing the ways it can fail is more effective than asserting it stays put.
- **"Do not re-centre it"** — models correct composition between cuts and think they are being helpful.
- **A restatement requirement** — every segment where the object appears names its anchor by name. Not assumed from the previous shot.

If the object legitimately moves once, give it a second anchor and **show the transit on screen**. An object that changes place between cuts without a visible move reads as a teleport, which is a worse failure than drift.

If the film has a hidden swap — object A becomes object B under cover — the swap inherits the anchor and says so: *the object changes, the position does not.*

### SPEED LOCK

For anything whose pace keeps drifting.

```
SPEED LOCK: the machine NEVER moves fast. In every shot it creeps at a slow, heavy,
inevitable pace — slower than a person strolls. No speed-up, no lurch, no fast pass.
```

### EDIT ACCELERATION LOCK

Tension comes from the edit and the subject moving at different rates. State the shape of the cutting as a rule, and **name the exceptions**, or the rule will eat the beats that need to breathe.

```
EDIT ACCELERATION LOCK
The edit gets faster while the subject stays slow.
Before the trigger the film breathes: S1 is 3.0s, S2 is 2.4s, S3 is 1.6s. From the
trigger onward segment lengths shorten and keep shortening. No segment after S3 is
longer than the segment before it EXCEPT the two scripted exceptions below.
THE TWO EXCEPTIONS: S5 at 3.2s and S8 at 3.6s. These are long on purpose.
```

### LIGHTING PROGRESSION

Lighting written as prose is decoration and gets ignored. Written as named states and tagged per segment like a lens lock, it becomes a rule.

Declare three or four states, in order, each defined by its **dominant sources** rather than a mood word. Then tag every segment: `LIGHT STATE B.`

```
LIGHT STATE A — CLINICAL, S1 to S3. Cold white daylight from the doorway and the
skylight bands. Flat, even, unremarkable, top-down. No warmth touches the subject.
This is the boring baseline the rest of the film departs from.

LIGHT STATE B — ALARM, S4 to S7. Triggered on the button press, instantly, not
gradually. Overheads drop to half. The amber beacon becomes the dominant moving
source: hard turning bars sweeping across the floor and faces at a slow rhythm.
```

Bind the transitions to a frame, not to a section boundary: *LIGHT STATE A cuts to LIGHT STATE B on the press, not after it.*

Name one state as the light event of the film — usually the reveal — and tell the change with light rather than with an effect: *the shadow slides off the object, the beam sweeps across it, steam rises through the light.* Then: `No glow effects, no magic.`

### PRODUCT VARIETY LOCK

For any block of consecutive product shots. Without it, six product shots become the same macro six times.

```
PRODUCT VARIETY LOCK: S10, S11, S12, S13, S14 and S16 are SIX different shots. Each
differs from the one before it in angle, in distance and in camera move. No two share
a framing. In order: overhead pour, low skimming lateral, top-down gravity drop,
pull, extreme macro, hero pull-back. No repeats.
```

## Patterns for commercials

- **Hidden transformation.** Never ask the model to morph. Object A before the cover, object B after, never both in frame, stated as a lock. The cover can be a machine, a hand, a door, a whip pan. This is why paired assets must share packaging.
- **Start every segment on the action.** If the beat is a button press, cut to the finger on the button already in contact. Two seconds of someone getting ready is 6% of a thirty-second ad spent on nothing.
- **Delete setup entirely rather than shortening it.** A driver getting into a cab compressed to one second is still a driver getting into a cab. Cut to the press.
- **Put the payoff object near the threat from segment one** so the stakes are legible immediately.
- **The edit accelerates while the subject stays slow.**
- **Give the product reveal room** — five or six varied beats beat two good ones.
- **Prefer angle shots to action shots in product blocks.** A macro from a new angle is cheap and reliable. A shot where a tool enters frame and pours, lifts or cuts is expensive and often breaks. Have the downgrade ready: replace the action shot with a passive macro and the count stays the same.
- **Keep the background alive** in every wide and medium shot.
- **Two logo placements maximum** — one diegetic, one endcard — plus *the logo appears nowhere else, no other logos or text in frame.* If no diegetic surface exists in the assets, use the endcard only rather than inventing a prop.
