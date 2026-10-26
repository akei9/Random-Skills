#!/usr/bin/env python3
"""Render a FUT-style skill card and a 24-spoke radar from a MEGA record JSON."""
import argparse
import datetime
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "template.html"
PROFILE_DIR = Path.home() / ".cache" / "mega-card" / "chrome-profile"
WINDOW = "1600,1240"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]


def from_record(obj, date_override=None):
    """Build (traits, date, foot) from a MEGA record JSON (the challenge POST body)."""
    traits = {}
    for t in obj.get("traits", []):
        tid = t.get("trait_id")
        c = t.get("counts", {})
        if tid:
            traits[tid] = [int(c.get("eligible", 0)), int(c.get("applied", 0)), int(c.get("declined", 0))]
    missing = [f"T{i:02d}" for i in range(1, 25) if f"T{i:02d}" not in traits]
    if missing:
        sys.exit(f"Record JSON has no trait counts for: {', '.join(missing)}")
    cov = obj.get("coverage", {})
    parts = []
    episodes = cov.get("task_episodes")
    if episodes is not None:
        parts.append(f"{episodes} {'episode' if episodes == 1 else 'episodes'}")
    days = cov.get("window_days")
    if days is not None:
        parts.append(f"{days} {'day' if days == 1 else 'days'}")
    date = date_override or datetime.date.today().isoformat()
    return traits, date, " · ".join(parts)


def find_chrome():
    for candidate in CHROME_CANDIDATES:
        path = candidate if candidate.startswith("/") and Path(candidate).exists() else shutil.which(candidate)
        if path:
            return path
    return None


def render_png(html_path, png_path, chrome):
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    png_path.unlink(missing_ok=True)
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={PROFILE_DIR}",
        "--force-device-scale-factor=2",
        f"--window-size={WINDOW}",
        "--virtual-time-budget=5000",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ]
    # Headless Chrome can keep running after it writes the screenshot, so wait for a stable file, not for exit.
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.time() + 60
    last_size = -1
    while time.time() < deadline:
        if proc.poll() is not None:
            break
        if png_path.exists():
            size = png_path.stat().st_size
            if size > 0 and size == last_size:
                break
            last_size = size
        time.sleep(0.5)
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(5)
        except subprocess.TimeoutExpired:
            proc.kill()
    if not png_path.exists():
        sys.exit("Chrome produced no screenshot. In Claude Code run this script outside the sandbox.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="a MEGA record JSON (the challenge POST body)")
    parser.add_argument("--name", default="KRYCH", help="name printed on the card")
    parser.add_argument("--date", help="scan date YYYY-MM-DD for the card (default: today)")
    parser.add_argument("--out-dir", type=Path, help="default: the record's directory")
    parser.add_argument("--no-png", action="store_true", help="write HTML only")
    args = parser.parse_args()

    obj = json.loads(args.record.read_text(encoding="utf-8"))
    traits, date, foot = from_record(obj, args.date)

    out_dir = (args.out_dir or args.record.parent).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"mega-skill-web-{date}"
    html_path = out_dir / f"{stem}.html"
    png_path = out_dir / f"{stem}.png"

    data = {"name": args.name.upper(), "date": date, "foot": foot, "traits": traits}
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/", f"const DATA = {payload};")
    html_path.write_text(html, encoding="utf-8")
    print(f"HTML: {html_path}")

    if args.no_png:
        return
    chrome = find_chrome()
    if not chrome:
        sys.exit("Chrome/Chromium not found, PNG skipped. HTML is ready.")
    render_png(html_path, png_path, chrome)
    print(f"PNG:  {png_path}")


if __name__ == "__main__":
    main()
