---
name: mega-card-graphite
description: Graphite/brass FUT-style card plus a 24-spoke skill radar from a MEGA record JSON (the challenge POST body). HTML and PNG (headless Chrome). A dark, monochrome-luxe restyle of mega-card. Use when the user wants a player card, skill web, radar, or skills chart of their MEGA / assessment result in a dark style.
---

# MEGA card — graphite variant

A dark graphite + brushed-brass restyle of `mega-card`: the same FUT-style overall rating and 24-spoke skill web, in a monochrome-luxe look, with a scouting-report panel beside the card. The data contract and CLI are identical to `mega-card`, so it is a drop-in template swap.

## Differences from mega-card

- **Style:** graphite/brass, English labels, plus a scouting report — top form, weak foot, low-data, and a full 24-trait legend.
- **Grouping:** the canonical MEGA 5-pillar grouping (Direction · Context · Ground · Orchestration · Proof) instead of 6 custom stats. `MEGA` defines these five; the six-stat split in `mega-card` is its author's own.
- **Honesty flag:** a trait with fewer than 3 eligible episodes is shown as low-data (hollow spoke, `~n LOW`) and left out of the score and the colour bands — matching MEGA's own "measured" threshold. `mega-card` plots every trait raw.

## Steps

1. **Find the record.** The MEGA **record JSON** — the exact body posted when the agent runs the `mega.dev/challenge.md` assessment. Path from the argument; otherwise the newest `mega-assessment-*.json` in cwd (the challenge writes it to the OS temp dir, so you usually pass that path). Nothing found: ask for the path.
2. **Generate.** Headless Chrome hangs in the sandbox, so run with `dangerouslyDisableSandbox: true`:
   ```bash
   python3 ~/.claude/skills/mega-card-graphite/render.py <record.json> [--name NAME] [--archetype TEXT] [--tagline TEXT] [--date YYYY-MM-DD] [--out-dir DIR] [--no-png]
   ```
   Files land next to the record as `mega-skill-web-<date>.html/.png`. The record supplies the 24 trait counts (`traits[].counts`) and the episode/day totals (`coverage`); scan date defaults to today (`--date` to override). The script errors if any of T01–T24 is missing. The archetype is **not** in the record, so pass MEGA's archetype (from the claim page) via `--archetype`: the headline then shows it (e.g. "The Architect") with `--name` as the cardholder line beneath; without `--archetype`, `--name` is the headline.
3. **Look at the PNG once** (Read). Fix clipped text or overlaps in `template.html`, never in the generated file.
4. **Publish** the HTML via Artifact (favicon `⚓`) unless the user only wants the PNG. Give the link and the PNG path.

## How it is scored

- Trait score = `(applied + declined) / eligible × 100`, rounded. A deliberate skip (`declined`) counts as a plus.
- Overall = mean of the **measured** traits (eligible ≥ 3). Tier: 75+ gold, 65–74 silver, below 65 bronze.
- Dot colours: 70+ green, 50–69 amber, below 50 red.

Change the grouping or trait names: `PILLARS` and `NAMES` in `template.html`.

## Credit

A restyle of **mega-card** by piotrkrych2 — https://github.com/piotrkrych2/Random-Skills. `render.py` is adapted from his original (reads the MEGA record JSON instead of a markdown report, adds `--archetype`/`--tagline`); `template.html` and this `SKILL.md` are new.
