"""Build the two static `whoami` panels: the ASCII portrait and the info card.

Usage: python scripts/make_profile_art.py
Edit INFO below to change the card, then re-run.
"""
import base64

from PIL import Image

FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

# Both panels share this height so they line up side by side.
PANEL_H = 560

INFO = [
    ("Name", ["Aryan Choudhary"]),
    ("Location", ["Kolkata, India"]),
    ("Role", ["B.Tech CSE (AI & ML) @ Narula"]),
    ("Built", ["AgentShield · MediQueue", "Milestone Pot · RainGuard"]),
    ("Stack", ["TypeScript · Next.js · React", "Python"]),
    ("Contact", ["choudharyaryan3691@gmail.com"]),
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def portrait(src="assets/portrait.png", out="awr1n-ascii.svg", W=370, rows=40):
    im = Image.open(src)
    iw, ih = im.size
    h = round(W * ih / iw)
    pad = (PANEL_H - h) // 2
    b64 = base64.b64encode(open(src, "rb").read()).decode()
    band = h / rows
    clips, o = [], []
    # reveal the art band by band, like a terminal printing line after line
    for i in range(rows):
        y = pad + i * band
        clips.append(
            f'<clipPath id="r{i}"><rect x="0" y="{y:.2f}" width="0" height="{band + 0.6:.2f}">'
            f'<animate attributeName="width" from="0" to="{W}" begin="{i * 0.06:.2f}s" dur="0.4s" fill="freeze"/>'
            f"</rect></clipPath>"
        )
        o.append(f'<use href="#art" clip-path="url(#r{i})"/>')
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}" height="{PANEL_H}" viewBox="0 0 {W} {PANEL_H}">'
        f'<rect width="{W}" height="{PANEL_H}" rx="8" fill="#000"/>'
        f'<defs><image id="art" x="0" y="{pad}" width="{W}" height="{h}" '
        f'href="data:image/png;base64,{b64}"/>{"".join(clips)}</defs>'
        + "".join(o)
        + "</svg>"
    )
    open(out, "w").write(svg)
    print(f"wrote {out}")


def info_card(out="info-card.svg", W=490):
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{PANEL_H}" viewBox="0 0 {W} {PANEL_H}" '
        f'font-family="{FONT}">',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{PANEL_H - 1}" rx="8" fill="#0d1117" stroke="#30363d"/>',
        f'<path d="M.5 34V8.5a8 8 0 0 1 8-8h{W - 17}a8 8 0 0 1 8 8V34z" fill="#161b22"/>',
        '<line x1="0" y1="34" x2="%d" y2="34" stroke="#30363d"/>' % W,
        '<circle cx="20" cy="17" r="6" fill="#ff5f56"/><circle cx="40" cy="17" r="6" fill="#ffbd2e"/>'
        '<circle cx="60" cy="17" r="6" fill="#27c93f"/>',
        f'<text x="{W / 2}" y="22" text-anchor="middle" font-size="12" fill="#8b949e">awr1n@github</text>',
    ]
    lines = [('<tspan fill="#58a6ff" font-weight="700">awr1n@github</tspan>', 15),
             ('<tspan fill="#8b949e">' + "-" * 12 + "</tspan>", 15)]
    for key, vals in INFO:
        for j, v in enumerate(vals):
            k = f'<tspan fill="#3fb950" font-weight="700">{esc(key)}</tspan>' if j == 0 else ""
            lines.append((f'{k}<tspan x="150" fill="#c9d1d9">{esc(v)}</tspan>', 13))
    y, t = 74, 0.3
    for text, size in lines:
        o.append(
            f'<text x="28" y="{y}" font-size="{size}" opacity="0">{text}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="0.3s" fill="freeze"/></text>'
        )
        y += 30 if size == 15 else 28
        t += 0.18
    # colour blocks, neofetch-style
    y += 14
    for i, c in enumerate(["#0d1117", "#ff7b72", "#3fb950", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#c9d1d9"]):
        o.append(f'<rect x="{28 + i * 30}" y="{y}" width="26" height="16" rx="2" fill="{c}" stroke="#30363d"/>')
    # blinking cursor
    o.append(
        f'<text x="28" y="{PANEL_H - 28}" font-size="14" fill="#c9d1d9"><tspan fill="#3fb950">awr1n@github</tspan>'
        f' ~ $ <tspan fill="#c9d1d9">█<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.51;1" '
        f'dur="1.1s" repeatCount="indefinite"/></tspan></text>'
    )
    o.append("</svg>")
    open(out, "w").write("\n".join(o))
    print(f"wrote {out}")


if __name__ == "__main__":
    portrait()
    info_card()
