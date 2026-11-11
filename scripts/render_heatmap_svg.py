"""Render data/contributions.json as an animated, GitHub-dark heatmap SVG.

Usage: python scripts/render_heatmap_svg.py data/contributions.json contrib-heatmap.svg
"""
import datetime as dt
import json
import sys

CELL, GAP = 13, 3
STEP = CELL + GAP
LEFT, TOP = 46, 34
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def level(n: int, peak: int) -> int:
    if n <= 0:
        return 0
    q = n / max(peak, 1)
    return 1 if q <= 0.25 else 2 if q <= 0.5 else 3 if q <= 0.75 else 4


def current_streak(days):
    counts = [n for _, n in days]
    i = len(counts) - 1
    if counts and counts[i] == 0:  # today not counted yet
        i -= 1
    s = 0
    while i >= 0 and counts[i] > 0:
        s, i = s + 1, i - 1
    return s


def render(data: dict) -> str:
    days = [(dt.date.fromisoformat(d), n) for d, n in data["days"]]
    peak = sorted(n for _, n in days)[int(len(days) * 0.95)] or max(n for _, n in days) or 1
    start = days[0][0] - dt.timedelta(days=(days[0][0].weekday() + 1) % 7)  # back to Sunday
    weeks = (days[-1][0] - start).days // 7 + 1
    width = LEFT + weeks * STEP + 20
    height = TOP + 7 * STEP + 52

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
         f'viewBox="0 0 {width} {height}" font-family="{FONT}">',
         f'<rect width="{width}" height="{height}" rx="8" fill="#0d1117" stroke="#30363d"/>']

    # month labels
    last_month = None
    for w in range(weeks):
        d = start + dt.timedelta(weeks=w)
        if d.month != last_month and w < weeks - 2:
            o.append(f'<text x="{LEFT + w * STEP}" y="{TOP - 10}" font-size="11" fill="#8b949e">{d.strftime("%b")}</text>')
            last_month = d.month
    for row, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        o.append(f'<text x="12" y="{TOP + row * STEP + 10}" font-size="11" fill="#8b949e">{lab}</text>')

    # cells, revealed column by column
    for d, n in days:
        w = (d - start).days // 7
        r = (d - start).days % 7
        delay = w * 0.025
        o.append(
            f'<rect x="{LEFT + w * STEP}" y="{TOP + r * STEP}" width="{CELL}" height="{CELL}" rx="2.5" '
            f'fill="{COLORS[level(n, peak)]}" opacity="0"><title>{n} on {d.isoformat()}</title>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.35s" fill="freeze"/></rect>'
        )

    fy = TOP + 7 * STEP + 28
    streak = current_streak(data["days"])
    o.append(f'<text x="{LEFT}" y="{fy}" font-size="12" fill="#c9d1d9">{data["total"]} contributions in the last year'
             f' · {streak}-day streak</text>')
    lx = width - 20 - 5 * STEP - 74
    o.append(f'<text x="{lx}" y="{fy}" font-size="11" fill="#8b949e">Less</text>')
    for i, c in enumerate(COLORS):
        o.append(f'<rect x="{lx + 34 + i * STEP}" y="{fy - 11}" width="{CELL}" height="{CELL}" rx="2.5" fill="{c}"/>')
    o.append(f'<text x="{lx + 38 + 5 * STEP}" y="{fy}" font-size="11" fill="#8b949e">More</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
    with open(src) as f:
        svg = render(json.load(f))
    with open(out, "w") as f:
        f.write(svg)
    print(f"wrote {out}")
