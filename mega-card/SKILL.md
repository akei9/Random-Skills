---
name: mega-card
description: FIFA/FUT-style card plus a 24-spoke skill radar from a MEGA record JSON (the challenge POST body). Generates HTML and PNG, and can publish as an artifact. Use when the user asks for a player card, skill web, radar, or skills chart from a MEGA / assessment result.
---

# MEGA card

From a MEGA Assessment report it builds a graphic: a bronze / silver / gold FUT card with an overall rating and 6 stats on a hexagon, next to the full 24-trait skill web (0-100).

## Steps

1. **Find the record.** The MEGA **record JSON** — the body posted when the agent runs the `mega.dev/challenge.md` assessment. Path from the argument; otherwise the newest `mega-assessment-*.json` in cwd, then in `~/projects/tmp/` (the challenge writes it to the OS temp dir, so you usually pass that path). Nothing found: ask for the path.
2. **Generate.** Bash with `dangerouslyDisableSandbox: true` — headless Chrome hangs inside the sandbox and writes no screenshot:
   ```bash
   python3 ~/.claude/skills/mega-card/render.py <record.json> [--name NAME] [--date YYYY-MM-DD] [--out-dir DIR] [--no-png]
   ```
   Default name `KRYCH`; files land next to the record as `mega-skill-web-<date>.html/.png`. The record supplies the 24 trait counts (`traits[].counts`) and the episode/day totals (`coverage`); scan date defaults to today (`--date` to override). The script errors if any of T01-T24 is missing.
3. **Look at the PNG once** (Read). Watch for clipped text and overlapping labels. Make fixes in `template.html`, not in the generated file.
4. **Publish** the generated HTML via Artifact (favicon `🕸️`), unless the user only wants the PNG. Give the link and the PNG path.

## How it is scored

- Trait score = `(applied + declined) / eligible * 100`, rounded. `declined` is a deliberate skip and counts as a plus.
- Overall = mean of the 24 traits. Card tier: 75+ gold, 65-74 silver, below that bronze (FIFA-like thresholds).
- Dot colours: 70+ green, 50-69 yellow, below 50 red.
- Groups (a custom split; MEGA does not define them):

| Code | Group | Traits |
|---|---|---|
| INT | Intent | T01, T02, T05, T06 |
| CTX | Context | T03, T04, T09, T10, T11, T12 |
| DIA | Diagnosis | T07, T08, T13 |
| DEL | Delegation | T14, T15, T16, T17, T19, T20 |
| STR | Steering | T18, T21, T22 |
| VER | Verification | T23, T24 |

Change the groups or trait names: `GROUPS` and `NAMES` in `template.html`.

## Record parsing

- Traits: 24 counts from `traits[].counts` — `eligible`, `applied`, `declined` per `trait_id`. The script errors if any of T01–T24 is missing.
- Card footer: `coverage.task_episodes` and `coverage.window_days` become the episode/day line; the scan date defaults to today unless `--date` is passed.
