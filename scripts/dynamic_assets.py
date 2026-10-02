"""Renderers for the SVGs that change with your GitHub activity."""
import math
import random

from aes import *  # noqa: F401,F403
from aes import _n

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
DASH = "—"


def T(fk, text, size, x, y, anchor="start", ls=0.0, op=1.0, fill=CREAM):
    extra = f'fill-opacity="{op}"' if op != 1 else ""
    return txt(fk, text, size, x, y, fill, anchor, ls, extra)


def fmt(v):
    return DASH if v is None else f"{v:,}"


def stats(d):
    W, H = 900, 476
    b = [frame(W, H), ticks(0, 0, W, H, 12, .75), T("mono", "STATS  /  統計", 11, 40, 44, ls=4, op=.55),
         hline(40, W - 40, 58, .14), traveler(40, W - 40, 58, 160, 7)]

    def col(x, value, en, jp, sub, anchor="start"):
        s = fit("j2", value, 84, 240, 2)
        return (T("j2", value, s, x, 168, anchor, 2) + T("mono", en, 10, x, 200, anchor, 3, .6)
                + T("jp", jp, 13, x, 221, anchor, 4, .6) + T("mono", sub, 9.5, x, 242, anchor, 2.5, .35))

    b.append(col(40, fmt(d.get("total")), "TOTAL CONTRIBUTIONS", "総貢献数", d.get("since_label", "SINCE THE FIRST COMMIT")))
    b.append(col(860, fmt(d.get("longest")), "LONGEST STREAK", "最長連続日数", d.get("longest_range", ""), "end"))
    # centre: current streak ring
    cx, cy, r = 450, 148, 76
    C = 2 * math.pi * r
    v = fmt(d.get("cur"))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 30}" fill="url(#halo)"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CREAM}" stroke-opacity=".16"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r + 9}" fill="none" stroke="{CREAM}" stroke-opacity=".3" stroke-width="4" stroke-dasharray="1 {C / 90 * 1.1 - 1:.2f}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#holo)" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="{C * .42:.0f} {C * .58:.0f}">'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="9s" repeatCount="indefinite"/></circle>'
             f'<circle cx="{cx}" cy="{cy - r}" r="3" fill="{TEAL}"><animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" dur="14s" repeatCount="indefinite"/></circle>')
    b.append(T("j2", v, fit("j2", v, 64, 100, 1), cx, cy + 22, "middle", 1))
    b.append(T("mono", "CURRENT STREAK", 10, cx, 262, "middle", 3, .6) + T("jp", "現在の連続日数", 13, cx, 283, "middle", 4, .6)
             + T("mono", d.get("cur_range", ""), 9.5, cx, 303, "middle", 2.5, .35))
    b.append(hline(40, W - 40, 322, .12))

    cols = [(fmt(d.get("commits")), "COMMITS · 12 MO", "コミット"), (fmt(d.get("prs")), "PULL REQUESTS", "プルリクエスト"),
            (fmt(d.get("stars")), "STARS EARNED", "スター"), (fmt(d.get("repos")), "REPOSITORIES", "リポジトリ")]
    for i, (val, en, jp) in enumerate(cols):
        x = 40 + i * 215
        if i:
            b.append(vline(x - 22, 344, 416, .1))
        b.append(T("j2", val, fit("j2", val, 44, 170, 2), x, 378, ls=2))
        b.append(T("mono", en, 9.5, x, 400, ls=3, op=.6) + T("jp", jp, 12, x, 418, ls=3, op=.55))
    b.append(T("mono", d.get("updated_label", "AWAITING FIRST SYNC"), 9, W - 40, H - 22, "end", 3, .35))
    return svg(W, H, "".join(b), "", "Statistics: contributions, streaks, commits, pull requests, stars and repositories")


def langs(d):
    rows = (d.get("langs") or [])[:6]
    placeholder = not rows
    W = 900
    H = 150 if placeholder else 104 + len(rows) * 44
    b = [frame(W, H), ticks(0, 0, W, H, 12, .75), T("mono", "LANGUAGES  /  使用言語", 11, 40, 44, ls=4, op=.55),
         T("mono", "BY BYTES · PUBLIC REPOS", 9.5, W - 40, 44, "end", 3, .35), hline(40, W - 40, 58, .14), traveler(40, W - 40, 58, 160, 7)]
    bx, bw = 250, 500
    for i, (name, pct) in enumerate(rows):
        y = 96 + i * 44
        fw = max(6, bw * pct / 100)
        b.append(T("mono", f"{i + 1:02d}", 10, 40, y + 5, ls=2, op=.4))
        b.append(T("j4", name.upper(), fit("j4", name.upper(), 15, 170, 3), 78, y + 5.5, ls=3))
        b.append(hline(bx, bx + bw, y, .12, h=2))
        b.append(f'<rect x="{bx}" y="{y - 1}" width="{fw:.0f}" height="2" fill="url(#holo)"/>'
                 f'<circle cx="{bx + fw:.0f}" cy="{y}" r="3" fill="{CREAM}"><animate attributeName="r" values="3;5;3" dur="{2.6 + i * .3:.1f}s" repeatCount="indefinite"/></circle>')
        b.append(T("mono", f"{pct:.1f}%", 13, W - 40, y + 5, "end", 1, .9))
    if placeholder:
        b.append(T("jp", "集計中…", 20, 450, 100, "middle", 8, .8) + T("mono", "COMPILING LANGUAGE DATA", 10, 450, 124, "middle", 4, .4))
    return svg(W, H, "".join(b), "", "Languages by share of code: " + (", ".join(f"{a} {p:.0f}%" for a, p in rows) or "not yet counted"))


LEVELS = [.07, .24, .44, .70, .98]


def heatmap(d):
    weeks = d.get("weeks")
    W, H = 900, 246
    c, g, x0, y0 = 11, 4, 84, 96
    placeholder = not weeks
    if placeholder:
        weeks = [[(None, 0)] * 7 for _ in range(53)]
    mx = max((cnt for wk in weeks for _, cnt in wk), default=0)
    total = d.get("year_total")
    defs = ('<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    b = [frame(W, H), ticks(0, 0, W, H, 12, .75), T("mono", "ACTIVITY  /  活動記録", 11, 40, 44, ls=4, op=.55),
         T("mono", (f"{total:,} CONTRIBUTIONS · PAST YEAR" if total is not None else "PAST YEAR · DAY BY DAY"), 9.5, W - 40, 44, "end", 3, .4),
         hline(40, W - 40, 58, .14), traveler(40, W - 40, 58, 160, 7)]
    rng = random.Random(5)
    prev, last_x, cells = None, -99, []
    for ci, wk in enumerate(weeks):
        x = x0 + ci * (c + g)
        first = wk[0][0]
        if first:
            m = int(first[5:7]) - 1
            if m != prev:
                if ci < len(weeks) - 2 and x - last_x >= 40:
                    b.append(T("mono", MONTHS[m], 9, x, 86, ls=2, op=.5))
                    last_x = x
                prev = m
        for ri, (dt, cnt) in enumerate(wk):
            lvl = 0 if cnt <= 0 or mx == 0 else max(1, min(4, math.ceil(4 * cnt / mx)))
            y = y0 + ri * (c + g)
            if lvl == 4 and rng.random() < .4:
                cells.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{CREAM}" fill-opacity="{LEVELS[4]}"><animate attributeName="fill" values="{CREAM};{TEAL};{CREAM}" dur="{rng.uniform(3, 7):.1f}s" begin="-{rng.uniform(0, 5):.1f}s" repeatCount="indefinite"/></rect>')
            else:
                cells.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{CREAM}" fill-opacity="{LEVELS[lvl]}"/>')
    b.append("".join(cells))
    for ri, lab in ((1, "MON"), (3, "WED"), (5, "FRI")):
        b.append(T("mono", lab, 8.5, x0 - 10, y0 + ri * (c + g) + 9, "end", 1.5, .4))
    gw = 53 * (c + g)
    b.append(f'<clipPath id="gridclip"><rect x="{x0}" y="{y0}" width="{gw}" height="{7 * (c + g)}"/></clipPath>'
             f'<g clip-path="url(#gridclip)"><rect y="{y0}" width="120" height="{7 * (c + g)}" fill="url(#beam)"><animate attributeName="x" values="{x0 - 120};{x0 + gw}" dur="7s" repeatCount="indefinite"/></rect></g>')
    ly, lx = H - 36, W - 40 - 5 * 15 - 78
    b.append(T("mono", "LESS", 9, lx, ly + 9, "end", 2, .4))
    for i in range(5):
        b.append(f'<rect x="{lx + 10 + i * 15}" y="{ly}" width="{c}" height="{c}" fill="{CREAM}" fill-opacity="{LEVELS[i]}"/>')
    b.append(T("mono", "MORE", 9, lx + 18 + 5 * 15, ly + 9, ls=2, op=.4))
    if placeholder:
        b.append(f'<rect x="270" y="118" width="360" height="52" fill="{INK}" fill-opacity=".92" stroke="{CREAM}" stroke-opacity=".3"/>'
                 + T("jp", "集計中…", 18, 450, 142, "middle", 8, .85) + T("mono", "COMPILING ACTIVITY DATA", 9.5, 450, 160, "middle", 4, .45))
    return svg(W, H, "".join(b), defs, "Contribution heatmap for the past year")
