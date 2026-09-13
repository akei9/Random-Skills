---
name: mega-card
description: FIFA/FUT-style card plus a 24-spoke skill radar from a MEGA Assessment report (mega-assessment-*.md). Generates HTML and PNG, and can publish as an artifact. Use when the user asks for a player card, skill web, radar, or skills chart from a MEGA / assessment result.
---

# MEGA card

From a MEGA Assessment report it builds a graphic: a bronze / silver / gold FUT card with an overall rating and 6 stats on a hexagon, next to the full 24-trait skill web (0-100).

## Steps

1. **Find the report.** Path from the argument. No argument: the newest `mega-assessment-*.md` in cwd, then in `~/projects/tmp/`. Nothing found: ask for the path.
2. **Generate.** Bash with `dangerouslyDisableSandbox: true` — headless Chrome hangs inside the sandbox and writes no screenshot:
   ```bash
   python3 ~/.claude/skills/mega-card/render.py <report.md> [--name NAME] [--out-dir DIR] [--no-png]
   ```
   Default name `KRYCH`; files land next to the report as `mega-skill-web-<date>.html/.png`. The script errors if any of T01-T24 is missing from the report.
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
| KTX | Context | T03, T04, T09, T10, T11, T12 |
| DIA | Diagnosis | T07, T08, T13 |
| DEL | Delegation | T14, T15, T16, T17, T19, T20 |
| STR | Steering | T18, T21, T22 |
| WER | Verification | T23, T24 |

Change the groups or trait names: `GROUPS` and `NAMES` in `template.html`.

## Report parsing

- Traits: the first `| Txx | Name | eligible | applied | declined | missed | verified |` table row for each ID. Indicator table rows (a kebab-case slug in the second column) are skipped.
- Card footer: the report labels `**Scan date:**`, `Task episodes`, `Sessions` / `Scanned`, `(N days)` — `render.py` also accepts the Polish equivalents (`Data skanu`, `Epizody zadaniowe`, `Przeskanowane`, `dni`). A missing field is skipped.
