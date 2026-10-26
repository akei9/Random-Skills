# Random Skills

Skills for [Claude Code](https://claude.com/claude-code) that turn a **MEGA Assessment** into a shareable "player card" — a FUT-style overall rating with a 24-spoke skill radar and a scouting report.

## Skills

| Skill | What it does |
|---|---|
| [mega-card](mega-card/SKILL.md) | FIFA/FUT-style card and a 24-spoke skill radar from a MEGA Assessment report. HTML and PNG (headless Chrome). |
| [mega-card-graphite](mega-card-graphite/SKILL.md) | Graphite/brass restyle of mega-card: the same FUT card and 24-trait radar in a dark, monochrome-luxe style, with a scouting-report panel and MEGA's 5-pillar grouping. Also takes a MEGA record JSON directly. |

## Prerequisites

- **Claude Code** (or any agent that can run shell commands) — to run the MEGA assessment that produces your data.
- **Python 3** — standard library only, nothing to `pip install`.
- **Google Chrome or Chromium** — rendered headlessly for the PNG. Optional: pass `--no-png` for HTML only.

The skill **only draws the card.** It never runs the assessment and never contacts MEGA — you bring the assessment output to it.

## Install

Clone this repo, then copy the skill into `~/.claude/skills/` so Claude Code can run it by name:

```bash
git clone https://github.com/akei9/Random-Skills
cp -R Random-Skills/mega-card-graphite ~/.claude/skills/
```

(Do the same with `mega-card` for the lighter original style.)

## Generate your own card

### 1. Run the MEGA assessment

In a Claude Code session, hand your agent the MEGA assessment prompt and let it run:

> Fetch https://mega.dev/challenge.md and follow it. Ask me before uploading anything.

The agent scans **your own** session history, counts the 24 collaboration traits, and writes the result to a **record JSON** (the file it would upload). After you approve the upload, MEGA's claim page shows your official card and your **archetype** (e.g. "The Architect").

Two things from this step feed the card:

- the **record JSON** the agent built — ask it for the path (it is written to a temp file before upload), and
- your **archetype**, read from the MEGA claim page.

### 2. Make the card

Point the skill at that record JSON:

```bash
python3 ~/.claude/skills/mega-card-graphite/render.py mega-assessment-<id>.json \
  --name "Your Name" \
  --archetype "The Architect"
```

It writes `mega-skill-web-<date>.html` and `.png` next to the JSON. In Claude Code the headless-Chrome step must run outside the sandbox (`dangerouslyDisableSandbox: true`); or pass `--no-png` for HTML only. Simplest of all: once the skill is installed, just ask your agent — *"make my MEGA card from that assessment"* — and it runs this for you.

<details>
<summary>Prefer a hand-written report instead of the JSON?</summary>

`render.py` also accepts a `mega-assessment-*.md` with a trait table:

```markdown
**Scan date:** 2026-10-26

| Metric | Value |
|---|---|
| Task episodes | 120 |
| Sessions | 14 |
| Window | 2026-08-01 → 2026-10-20 (80 days) |

| ID | Trait | eligible | applied | declined | missed | verified |
|---|---|---|---|---|---|---|
| T01 | Intent Clarity | 90 | 70 | 0 | 20 | 5 |
| ... one row for every trait T01 through T24 ... |
```

All 24 rows (T01–T24) must be present; the footer fields are optional.
</details>

### Options

| Option | Effect |
|---|---|
| `--name NAME` | Name on the card. Without `--archetype`, it is the headline. |
| `--archetype TEXT` | Headline (e.g. your MEGA archetype); `--name` then shows as the cardholder line beneath it. |
| `--tagline TEXT` | Replaces the default tier tagline. |
| `--date YYYY-MM-DD` | Scan date on the card (JSON input only; default: today). |
| `--out-dir DIR` | Where to write the files (default: next to the input). |
| `--no-png` | Write the HTML only; skip the screenshot. |

## How the score works

- Trait score = `(applied + declined) / eligible × 100`, rounded — a deliberate skip (`declined`) counts as a plus.
- A trait with fewer than 3 eligible episodes is "low-data": drawn hollow and left out of the overall and the colour bands (MEGA's own "measured" threshold).
- Overall = mean of the measured traits. Tier: 75+ gold, 65–74 silver, below 65 bronze.
- **These scores and the archetype are not MEGA's.** The scores are a local heuristic for the visual, and `--archetype` is whatever text you pass. Your MEGA claim page is the authoritative result; this card is a stylized, shareable snapshot of the same counts.

## Card Example (mega-card-graphite)

<img width="1475" height="1404" alt="Screenshot 2026-09-13 at 23 59 40" src="https://github.com/user-attachments/assets/a08bd72f-9efc-4ec6-8828-007c8338295e" />

## Credit

A restyle of **mega-card** by [piotrkrych2](https://github.com/piotrkrych2/Random-Skills).
