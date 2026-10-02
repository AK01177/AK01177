"""Renderers for the SVGs that change with your GitHub activity (calm, high-legibility)."""
import math

from aes import *  # noqa: F401,F403
from aes import _n

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
DASH = "—"


def T(fk, text, size, x, y, anchor="start", ls=0.0, op=1.0, fill=CREAM):
    extra = f'fill-opacity="{op}"' if op != 1 else ""
    return txt(fk, text, size, x, y, fill, anchor, ls, extra)


def card(W, H):
    return (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" fill="url(#bgpanel)" stroke="{CREAM}" stroke-opacity=".16"/>'
            f'<rect width="44" height="2" fill="{CREAM}" fill-opacity=".85"/>')


def ptitle(en, jp, W, right=None):
    out = T("mono", f"{en}  /  {jp}", 13, 40, 46, ls=4, op=.85) + hline(40, W - 40, 62, .14)
    if right:
        out += T("mono", right, 11.5, W - 40, 46, "end", 3, .6)
    return out


def fmt(v):
    return DASH if v is None else f"{v:,}"


def stats(d):
    W, H = 900, 480
    b = [card(W, H), ptitle("STATS", "統計", W)]

    def col(x, value, en, jp, sub, anchor="start"):
        return (T("j2", value, fit("j2", value, 76, 240, 2), x, 170, anchor, 2) + T("mono", en, 12, x, 202, anchor, 3, .85)
                + T("jp", jp, 14, x, 224, anchor, 4, .78) + T("mono", sub, 11, x, 246, anchor, 2.5, .6))

    b.append(col(40, fmt(d.get("total")), "TOTAL CONTRIBUTIONS", "総貢献数", d.get("since_label", "SINCE THE FIRST COMMIT")))
    b.append(col(860, fmt(d.get("longest")), "LONGEST STREAK", "最長連続日数", d.get("longest_range", ""), "end"))
    cx, cy, r = 450, 148, 68
    C = 2 * math.pi * r
    v = fmt(d.get("cur"))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 26}" fill="url(#halo)"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CREAM}" stroke-opacity=".2"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r + 8}" fill="none" stroke="{CREAM}" stroke-opacity=".3" stroke-width="3" stroke-dasharray="1 {C / 80 * 1.12 - 1:.2f}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#holo)" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="{C * .5:.0f} {C * .5:.0f}" transform="rotate(-90 {cx} {cy})"/>')
    b.append(T("j2", v, fit("j2", v, 56, 92, 1), cx, cy + 20, "middle", 1))
    b.append(T("mono", "CURRENT STREAK", 12, cx, 262, "middle", 3, .85) + T("jp", "現在の連続日数", 14, cx, 284, "middle", 4, .78)
             + T("mono", d.get("cur_range", ""), 11, cx, 306, "middle", 2.5, .6))
    b.append(hline(40, W - 40, 328, .12))
    cols = [(fmt(d.get("commits")), "COMMITS · 12 MO", "コミット"), (fmt(d.get("prs")), "PULL REQUESTS", "プルリクエスト"),
            (fmt(d.get("stars")), "STARS EARNED", "スター"), (fmt(d.get("repos")), "REPOSITORIES", "リポジトリ")]
    for i, (val, en, jp) in enumerate(cols):
        x = 40 + i * 215
        if i:
            b.append(vline(x - 22, 352, 426, .1))
        b.append(T("j2", val, fit("j2", val, 42, 170, 2), x, 384, ls=2))
        b.append(T("mono", en, 11.5, x, 406, ls=3, op=.85) + T("jp", jp, 13, x, 426, ls=3, op=.75))
    b.append(T("mono", d.get("updated_label", "AWAITING FIRST SYNC"), 10.5, W - 40, H - 16, "end", 3, .5))
    return svg(W, H, "".join(b), "", "Statistics: contributions, streaks, commits, pull requests, stars and repositories")


def langs(d):
    rows = (d.get("langs") or [])[:6]
    placeholder = not rows
    W = 900
    H = 170 if placeholder else 100 + len(rows) * 46
    b = [card(W, H), ptitle("LANGUAGES", "使用言語", W, "BY BYTES · PUBLIC REPOS")]
    bx, bw = 260, 490
    for i, (name, pct) in enumerate(rows):
        y = 104 + i * 46
        fw = max(6, bw * pct / 100)
        b.append(T("mono", f"{i + 1:02d}", 12, 40, y + 5, ls=2, op=.6))
        b.append(T("j4", name.upper(), fit("j4", name.upper(), 16, 170, 3), 80, y + 6, ls=3))
        b.append(hline(bx, bx + bw, y, .16, h=2))
        b.append(f'<rect x="{bx}" y="{y - 1}" width="{fw:.0f}" height="2" fill="url(#holo)"/><circle cx="{bx + fw:.0f}" cy="{y}" r="3.4" fill="{CREAM}"/>')
        b.append(T("mono", f"{pct:.1f}%", 14, W - 40, y + 5, "end", 1, .95))
    if placeholder:
        b.append(T("jp", "更新中…", 22, 450, 116, "middle", 8, .9) + T("mono", "WAITING FOR FIRST SYNC", 11.5, 450, 142, "middle", 4, .6))
    return svg(W, H, "".join(b), "", "Languages by share of code: " + (", ".join(f"{a} {p:.0f}%" for a, p in rows) or "not yet counted"))


LEVELS = [.08, .26, .46, .72, 1.0]


def heatmap(d):
    weeks = d.get("weeks")
    W, H = 900, 250
    c, g, x0, y0 = 12, 3, 84, 100
    placeholder = not weeks
    if placeholder:
        weeks = [[(None, 0)] * 7 for _ in range(53)]
    mx = max((cnt for wk in weeks for _, cnt in wk), default=0)
    total = d.get("year_total")
    b = [card(W, H), ptitle("ACTIVITY", "活動記録", W, f"{total:,} CONTRIBUTIONS · PAST YEAR" if total is not None else "PAST YEAR · DAY BY DAY")]
    prev, last_x, cells = None, -99, []
    for ci, wk in enumerate(weeks):
        x = x0 + ci * (c + g)
        first = wk[0][0]
        if first:
            m = int(first[5:7]) - 1
            if m != prev:
                if ci < len(weeks) - 2 and x - last_x >= 42:
                    b.append(T("mono", MONTHS[m], 11, x, 90, ls=2, op=.7))
                    last_x = x
                prev = m
        for ri, (dt, cnt) in enumerate(wk):
            lvl = 0 if cnt <= 0 or mx == 0 else max(1, min(4, math.ceil(4 * cnt / mx)))
            cells.append(f'<rect x="{x}" y="{y0 + ri * (c + g)}" width="{c}" height="{c}" fill="{CREAM}" fill-opacity="{LEVELS[lvl]}"/>')
    b.append("".join(cells))
    for ri, lab in ((1, "MON"), (3, "WED"), (5, "FRI")):
        b.append(T("mono", lab, 10.5, x0 - 10, y0 + ri * (c + g) + 10, "end", 1.5, .65))
    ly, lx = H - 36, W - 40 - 5 * 16 - 70
    b.append(T("mono", "LESS", 10.5, lx, ly + 10, "end", 2, .65))
    for i in range(5):
        b.append(f'<rect x="{lx + 10 + i * 16}" y="{ly}" width="{c}" height="{c}" fill="{CREAM}" fill-opacity="{LEVELS[i]}"/>')
    b.append(T("mono", "MORE", 10.5, lx + 18 + 5 * 16, ly + 10, ls=2, op=.65))
    if placeholder:
        b.append(f'<rect x="250" y="122" width="400" height="56" fill="{INK}" fill-opacity=".94" stroke="{CREAM}" stroke-opacity=".3"/>'
                 + T("jp", "更新中…", 20, 450, 148, "middle", 8, .92) + T("mono", "WAITING FOR FIRST SYNC", 11, 450, 168, "middle", 4, .6))
    return svg(W, H, "".join(b), "", "Contribution heatmap for the past year")


def _star(cx, cy, r=6):
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * .45
        a = -math.pi / 2 + k * math.pi / 5
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{CREAM}" fill-opacity=".85"/>'


def recent(d):
    rows = (d.get("recent") or [])[:5]
    placeholder = not rows
    W = 900
    H = 170 if placeholder else 96 + len(rows) * 48
    b = [card(W, H), ptitle("RECENT WORK", "最近の作業", W, "LATEST PUBLIC REPOSITORIES")]
    for i, r in enumerate(rows):
        y = 108 + i * 48
        if i:
            b.append(hline(40, W - 40, y - 26, .08))
        b.append(T("mono", f"{i + 1:02d}", 12, 40, y + 5, ls=2, op=.6))
        b.append(T("j4", r["name"], fit("j4", r["name"], 19, 300, 1), 80, y + 6, ls=1))
        if r.get("lang"):
            b.append(f'<circle cx="442" cy="{y}" r="3.4" fill="{TEAL}"/>' + T("mono", r["lang"].upper(), 12, 456, y + 4.5, ls=2, op=.9))
        b.append(T("mono", r.get("pushed", ""), 12, 620, y + 4.5, "start", 2, .8))
        if r.get("stars"):
            b.append(_star(806, y - .5) + T("mono", str(r["stars"]), 13, 820, y + 4.5, ls=1, op=.9))
    if placeholder:
        b.append(T("jp", "更新中…", 22, 450, 116, "middle", 8, .9) + T("mono", "WAITING FOR FIRST SYNC", 11.5, 450, 142, "middle", 4, .6))
    return svg(W, H, "".join(b), "", "Recent work: " + (", ".join(r["name"] for r in rows) or "not yet loaded"))
