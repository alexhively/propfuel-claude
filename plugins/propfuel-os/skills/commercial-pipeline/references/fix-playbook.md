# Stage 3 — fix playbook

When the user reports a problem: name the failure, apply the fix, rewrite **only** the affected sections, and say what to re-batch. Never re-roll an unchanged prompt.

## The master rule

**If something keeps breaking between cuts, stop describing it better inside every shot. Give it its own lock.**

Position, orientation, facing, speed, where a character stands, how fast the edit moves — anything that must survive multiple cuts gets promoted out of the segment descriptions into a hard rule of its own, stated in absolutes:

```
THE OBJECT NEVER MOVES OR TURNS.
```

Same position, same orientation, same facing, in every segment. Adding more careful description inside each of sixteen segments does not work. This is the single highest-value lesson in the workflow.

## Failure catalogue

| Symptom | Cause | Fix |
|---|---|---|
| Object drifts or rotates between cuts | No dedicated rule; it is being re-described per shot | Its own GEOMETRY LOCK in caps, with explicit negation of every drift mode |
| Object still drifts after a geometry lock | Lock anchored to screen coordinates, which move with the camera | Re-anchor to a world landmark — a floor joint, a distance from another object, an alignment with a door. Add *the anchor is a place on the floor, not a place in the frame* |
| Object re-centres itself shot to shot | Model is correcting composition and thinks it is helping | Explicit line: *do not re-centre it, do not re-frame around it, do not correct its position to match a previous shot's composition* |
| A duplicate of the hero object appears | Never stated that only one exists | A definition clause at the top of the geometry lock: *there is only ever ONE of this object in the film* |
| Object teleports to a new position | It legitimately moves, but the move was never shown | Second anchor plus a visible on-screen transit. An unshown move is worse than drift |
| Object changes between before and after | Two assets designed separately | Identical material paragraph in both image prompts, plus a lock that both are the same material |
| Transformation looks fake | Model asked to morph | Hide it: A before the cover, B after, never both in frame. Tell the change with light, then `No glow effects, no magic` |
| Product shot looks cheap | Product on the floor, camera below it | Onto a table or bench, camera slightly **above** looking down. State *never shot from below* |
| Product shots all look the same | No variety rule | PRODUCT VARIETY LOCK plus a distinct camera distance and downward angle in each shot's lens lock |
| A product action shot breaks | Tool entering frame is high-difficulty | Downgrade to a passive macro from a new angle. The shot count stays the same |
| Nothing feels like it changes | One lighting state across the whole film | Named light states, defined by dominant sources, tagged per segment |
| Lighting states written but ignored | Lighting written as prose decoration | Tag every segment with its state like a lens lock, and bind transitions to a frame: *cuts to STATE B on the press, not after it* |
| Middle drags | Time spent on setup and travel | Start segments on the action. Delete the run-up entirely rather than shortening it |
| No tension | Edit and subject move at the same rate | EDIT ACCELERATION LOCK, with named exceptions for the beats that must breathe |
| Acceleration rule eats the big beats | Rule applied without exceptions | Name the two or three long segments explicitly inside the rule |
| Machine feels light | No weight cues | Camera vibration caused by mass, not handheld shake; deep floor rumble; visible inertia |
| Machine keeps speeding up | No global speed rule | SPEED LOCK plus a restatement in POSITIVE LOCKS |
| Threat reads late | Hero object far from the threat at the start | Move it close. State that the threat is legible in frame one |
| Characters drift | Cinematic light baked into the character sheet | Regenerate the sheet with flat ambient light; keep anchors short and repeat verbatim |
| Character has a prop that was never in the sheet | Prop introduced by the video prompt | Acceptable, but flag it as the thing to watch. Props drift more than faces |
| Reference line contradicts its own image | Written from the plan, not the generated asset | Rewrite every reference line to describe what actually generated |
| A prop returns in the wrong colour | Never stated | A one-line lock naming the correct state and the wrong one |
| Body mechanics look wrong | Action written as intent, not mechanics | Direct it: *one knee bending forward into a shallow lunge — never a deep squat* |
| Scene looks like a render | Empty background | *The background stays alive in every wide and medium shot* — people working plus people crossing the depth |
| Logo comes out mangled | Redrawn too often | Two placements maximum, both named, plus *the logo appears nowhere else* |
| Version got worse after improvements | Complexity budget spent | Revert to the last clean version and ship it |

## How the iteration actually goes

**v1 — baseline.** Describe the whole film in plain English, nothing clever. The concept usually works immediately; three or four specific things break. Diagnose them as named problems rather than a general sense that it is not good enough.

**v2 — targeted fixes.** Apply the catalogue fixes for each named problem. This version is reliably much better and reliably still has the continuity problem, because v2 fixes are usually applied inside the segments.

**v3 — promote to locks.** The thing that kept breaking gets its own rule instead of better descriptions. Setup deleted rather than compressed. Edit acceleration made explicit. Product block expanded. This is normally the winner.

**v4 and v5 — the trap.** More emotion, more elaborate shots, more camera variety. Individually every change is an improvement. Together they make the output worse: more emotion means more character consistency to hold, more complex shots mean more physics to get right, more variety means more instructions to follow.

> **Every prompt has a complexity budget.** Once a prompt is generating clean results, one more brilliant idea often just gives the model one more thing to get wrong. Know when to stop and ship.

## Batching

Several generations per version, never one. Identical prompts diverge hard — one nails the camera and breaks the product, another nails the transformation and breaks the characters. Generate four, compare side by side, keep what works.

Budget expectation for a thirty-second film: around ten generations, of which only three or four are actual prompt changes.

If only one generation in four is clean, that is normal. Keep it and stop.

## When renumbering segments

Deleting or adding a segment shifts every ID after it. Lens locks, light state ranges, lock restatements and cross-references all name segments by ID, so they all have to be rewritten together. Say so when delivering — if the user has a voiceover or edit notes referencing shot numbers, they need to re-sync.
