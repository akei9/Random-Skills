---
name: mega-card-graphite
description: Graphite/brass FUT-style card plus a 24-spoke skill radar from a MEGA Assessment report (mega-assessment-*.md). HTML and PNG (headless Chrome). A dark, monochrome-luxe restyle of mega-card. Use when the user wants a player card, skill web, radar, or skills chart of their MEGA / assessment result in a dark style.
---

# MEGA card — graphite variant

A dark graphite + brushed-brass restyle of `mega-card`: the same FUT-style overall rating and 24-spoke skill web, in a monochrome-luxe look, with a scouting-report panel beside the card. The data contract and CLI are identical to `mega-card`, so it is a drop-in template swap.

## Differences from mega-card

- **Style:** graphite/brass, English labels, plus a scouting report — top form, weak foot, low-data, and a full 24-trait legend.
- **Grouping:** the canonical MEGA 5-pillar grouping (Direction · Context · Ground · Orchestration · Proof) instead of 6 custom stats. `MEGA` defines these five; the six-stat split in `mega-card` is its author's own.
- **Honesty flag:** a trait with fewer than 3 eligible episodes is shown as low-data (hollow spoke, `~n LOW`) and left out of the score and the colour bands — matching MEGA's own "measured" threshold. `mega-card` plots every trait raw.

## Steps

1. **Find the report.** Path from the argument; otherwise the newest `mega-assessment-*.md` in cwd. Nothing found: ask for the path.
2. **Generate.** Headless Chrome hangs in the sandbox, so run with `dangerouslyDisableSandbox: true`:
   ```bash
   python3 ~/.claude/skills/mega-card-graphite/render.py <report.md> [--name NAME] [--out-dir DIR] [--no-png]
   ```
   Files land next to the report as `mega-pajeczyna-<date>.html/.png`. The script errors if any of T01–T24 is missing.
3. **Look at the PNG once** (Read). Fix clipped text or overlaps in `template.html`, never in the generated file.
4. **Publish** the HTML via Artifact (favicon `⚓`) unless the user only wants the PNG. Give the link and the PNG path.

## How it is scored

- Trait score = `(applied + declined) / eligible × 100`, rounded. A deliberate skip (`declined`) counts as a plus.
- Overall = mean of the **measured** traits (eligible ≥ 3). Tier: 75+ gold, 65–74 silver, below 65 bronze.
- Dot colours: 70+ green, 50–69 amber, below 50 red.

Change the grouping or trait names: `PILLARS` and `NAMES` in `template.html`.

## Credit

A restyle of **mega-card** by piotrkrych2 — https://github.com/piotrkrych2/Random-Skills. `render.py` is his work, unchanged; only `template.html` and this `SKILL.md` are new.
