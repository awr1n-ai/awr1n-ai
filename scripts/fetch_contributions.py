"""Fetch the public GitHub contribution calendar for a user and save it as JSON.

Reads the same calendar shown on the profile page, so the totals match
what visitors see. Standard library only.

Usage: python scripts/fetch_contributions.py awr1n-ai data/contributions.json
"""
import json
import re
import sys
import urllib.request


def fetch(user: str) -> dict:
    req = urllib.request.Request(
        f"https://github.com/users/{user}/contributions",
        headers={"User-Agent": "profile-art-bot", "Accept": "text/html"},
    )
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")

    # <td ... data-date="2026-01-01" id="contribution-day-component-x-y" data-level="2" ...>
    cells = {}
    for td in re.finditer(r"<td[^>]*data-date=\"([\d-]+)\"[^>]*>", html):
        tag = td.group(0)
        cid = re.search(r'id="([^"]+)"', tag)
        cells[cid.group(1) if cid else td.group(1)] = td.group(1)

    # <tool-tip for="contribution-day-component-x-y">3 contributions on ...</tool-tip>
    counts = {}
    for tip in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html):
        date = cells.get(tip.group(1))
        if not date:
            continue
        m = re.match(r"\s*(\d+|No)\s+contribution", tip.group(2))
        counts[date] = 0 if (not m or m.group(1) == "No") else int(m.group(1))

    if len(counts) < 300:
        raise SystemExit(f"Parsed only {len(counts)} days - GitHub markup may have changed.")

    days = sorted(counts.items())
    return {"user": user, "total": sum(n for _, n in days), "days": [list(d) for d in days]}


if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "awr1n-ai"
    out = sys.argv[2] if len(sys.argv) > 2 else "data/contributions.json"
    data = fetch(user)
    with open(out, "w") as f:
        json.dump(data, f)
    print(f"{len(data['days'])} days, {data['total']} contributions -> {out}")
