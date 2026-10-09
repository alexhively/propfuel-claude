# PropFuel Claude Code plugins

## propfuel-os

Connects Claude Code to the **PropFuel Marketing OS** (https://propfuel-marketing-os.vercel.app). In any PropFuel session Claude:

- starts by pulling a briefing from the OS (your initiatives, what's blocked, deadlines, Q4 pacing, what teammates changed), and
- writes back what happened: progress logs, initiative / case study / plan updates and knowledge, credited to you, versioned and undoable.

Edits to things someone else owns ask you first.

### Install (once)

In Claude Code:

```
/plugin marketplace add alexhively/propfuel-claude
/plugin install propfuel-os@propfuel
```

Restart Claude Code, then run `/mcp`, pick **propfuel-os**, and sign in with your name and passcode (ask Alex). That's it.

### Commands

- `/propfuel-os:sweep` — one-time sync of everything your Claude already knows about your PropFuel work into the OS (you approve before anything is written).

The plugin contains no credentials: each person signs in to the OS with their own passcode.
