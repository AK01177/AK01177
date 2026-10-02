"""Renderers for the hand-authored SVG assets (minimal / futuristic / Japanese typography)."""
import math
import random

from aes import *  # noqa: F401,F403
from aes import _n

SPLINE = 'calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"'


def T(fk, text, size, x, y, anchor="start", ls=0.0, op=1.0, fill=CREAM):
    """Cream lettering with an opacity."""
    extra = f'fill-opacity="{op}"' if op != 1 else ""
    return txt(fk, text, size, x, y, fill, anchor, ls, extra)


# ----------------------------------------------------- rotating role banner
def titles():
    W, H = 900, 78
    items = [("FULL STACK DEVELOPER", "フルスタック開発者"), ("SYSTEM DESIGN", "システム設計"),
             ("MACHINE LEARNING", "機械学習"), ("COMPETITIVE PROGRAMMING · C++", "競技プログラミング")]
    b = [frame(W, H), ticks(0, 0, W, H, 9, .7),
         T("mono", "ROLE", 10, 28, 34, ls=4, op=.5), T("jp", "役割", 12, 28, 54, ls=4, op=.5),
         blink_dot(W - 34, 39, 2.6), hline(W - 96, W - 52, 39, .3),
         hline(84, 96, 39, .35)]
    for i, (en, jp) in enumerate(items):
        s = fit("j3", en, 25, 560, 9)
        b.append(f'<g opacity="{1 if i == 0 else 0}"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.05;.22;.27;1" dur="12s" begin="{3 * i}s" repeatCount="indefinite"/>'
                 f'<animateTransform attributeName="transform" type="translate" values="0 7;0 0;0 0;0 -7;0 -7" keyTimes="0;.05;.22;.27;1" dur="12s" begin="{3 * i}s" repeatCount="indefinite"/>'
                 + T("j3", en, s, 450, 40, "middle", 9) + T("jp", jp, 14, 450, 62, "middle", 5, .6) + "</g>")
    b.append(traveler(0, W, H - 1, 200, 6))
    return svg(W, H, "".join(b), "", "Full stack developer, system design, machine learning, competitive programming in C++")


# --------------------------------------------------- section header/divider
def section_header(idx, en, jp):
    W, H = 900, 78
    size, ls = 27, 12
    e = en.upper()
    ew = width("j3", e, size, ls)
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>', T("jp", jp, 92, W - 8, 70, "end", 10, .06),
         T("mono", idx, 12, 12, 38, ls=2, op=.5),
         f'<rect x="45.5" y="28.5" width="8" height="8" fill="none" stroke="{CREAM}" stroke-opacity=".8"/><rect x="48" y="31" width="3" height="3" fill="{TEAL}"><animate attributeName="opacity" values="1;.2;1" dur="2.4s" repeatCount="indefinite"/></rect>',
         T("j3", e, size, 76, 40, ls=ls),
         T("jp", jp, 17, 76 + ew + 28, 39, ls=6, op=.7),
         hline(0, W, 60, .14), traveler(0, W, 60, 200, 6.5), ticks(0, 0, W, H, 9, .6)]
    return svg(W, H, "".join(b), "", f"{en}")


def divider():
    W, H = 900, 34
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>', hline(0, 330, 17, .12), hline(570, W, 17, .12), plus(450, 17, 5, .7),
         f'<rect x="417" y="16" width="12" height="2" fill="{CREAM}" fill-opacity=".25"/><rect x="471" y="16" width="12" height="2" fill="{CREAM}" fill-opacity=".25"/>',
         f'<circle r="2" cy="17" fill="{TEAL}"><animate attributeName="cx" values="0;{W}" dur="9s" repeatCount="indefinite"/>'
         '<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="9s" repeatCount="indefinite"/></circle>']
    return svg(W, H, "".join(b), "", "divider")


# --------------------------------------------------------------- about card
def about():
    W, H = 900, 372
    rows = [("NAME", "名前", "Aryan Ranavat"),
            ("AFFILIATION", "所属", "B.Tech ICT · DA-IICT, Gandhinagar"),
            ("FOCUS", "専門", "Full Stack · System Design · Machine Learning"),
            ("CP LANGUAGE", "競技", "C++, for competitive programming"),
            ("BUILD STACK", "開発", "TypeScript & Python, for projects"),
            ("NOW", "現在", "Argus, an AI-powered codebase companion"),
            ("GOAL", "目標", "Software engineering internships & placements")]
    b = [frame(W, H), ticks(0, 0, W, H, 12, .75),
         T("mono", "PROFILE  /  プロフィール", 11, 40, 44, ls=4, op=.55), hline(40, 590, 58, .16), traveler(40, 590, 58, 130, 6)]
    y = 98
    for en, jp, val in rows:
        b.append(T("mono", en, 10, 40, y - 6, ls=3, op=.55))
        b.append(T("jp", jp, 12, 40, y + 11, ls=3, op=.5))
        b.append(T("j4", val, fit("j4", val, 20, 385), 214, y + 3))
        b.append(hline(40, 600, y + 21, .07))
        y += 42
    # right: floating cube, barcode, vertical JP
    b.append(f'<circle cx="748" cy="150" r="86" fill="url(#halo)"/>')
    b.append(cube(738, 156, 112, .95))
    b.append(plus(650, 84, 4, .5) + plus(846, 222, 4, .5))
    b.append(vtxt("jp", "開発者", 22, 852, 84, CREAM, 1.5, 'fill-opacity=".6"'))
    b.append(barcode(7, 640, 272, 200, 30, .55))
    b.append(T("mono", "AK01177 · DA-IICT · 2024", 10, 640, 322, ls=3, op=.5))
    b.append(vline(624, 84, 330, .12))
    return svg(W, H, "".join(b), "", "Profile: Aryan Ranavat, B.Tech ICT at DA-IICT Gandhinagar. Focus on full stack, system design and machine learning. C++ for competitive programming, TypeScript and Python for projects. Current project Argus. Seeking software engineering internships and placements.")


# ------------------------------------------------------------------- stack
TIERS = [
    ("01", "LANGUAGES", "言語", [("C++", "cplusplus"), ("Python", "python"), ("TypeScript", "typescript"), ("JavaScript", "javascript"), ("SQL", "mysql")]),
    ("02", "TOOLS", "ツール", [("React", "react"), ("FastAPI", "fastapi"), ("Node.js", "nodedotjs"), ("Tailwind", "tailwindcss"), ("Vite", "vite")]),
    ("03", "PLATFORM", "基盤", [("Git", "git"), ("Vercel", "vercel"), ("Render", "render"), ("Linux", "linux")]),
]


def stack():
    RH = 142
    W, H = 900, 62 + RH * 3
    b = [frame(W, H), ticks(0, 0, W, H, 12, .75), T("mono", "TECH STACK  /  技術スタック", 11, 40, 44, ls=4, op=.55),
         hline(40, W - 40, 58, .14), traveler(40, W - 40, 58, 160, 7)]
    for r, (idx, en, jp, items) in enumerate(TIERS):
        top = 78 + r * RH
        b.append(T("mono", idx, 11, 40, top + 22, ls=3, op=.5))
        b.append(T("j3", en, 19, 40, top + 56, ls=8))
        b.append(T("jp", jp, 14, 40, top + 78, ls=5, op=.6))
        b.append(T("mono", f"{len(items):02d} ITEMS", 10, 40, top + 100, ls=3, op=.35))
        if r:
            b.append(hline(40, W - 40, top - 8, .08))
        for i, (label, ic) in enumerate(items):
            tx, ty = 250 + i * 124, top
            idx2 = r * 5 + i
            b.append(ticks(tx, ty, 112, 112, 8, .55))
            b.append(f'<circle cx="{tx + 56}" cy="{ty + 46}" r="34" fill="none" stroke="{CREAM}" stroke-opacity=".22" stroke-dasharray="2 5"><animateTransform attributeName="transform" type="rotate" from="0 {tx + 56} {ty + 46}" to="{360 if idx2 % 2 else -360} {tx + 56} {ty + 46}" dur="{40 + idx2 * 3}s" repeatCount="indefinite"/></circle>'
                     f'<path d="{arc(tx + 56, ty + 46, 34, -20, 40)}" fill="none" stroke="url(#holo)" stroke-width="1.4" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" from="0 {tx + 56} {ty + 46}" to="360 {tx + 56} {ty + 46}" dur="{9 + idx2 % 4 * 2}s" repeatCount="indefinite"/></path>')
            b.append(f'<g>{icon(ic, tx + 56, ty + 46, 38, CREAM, 1)}'
                     f'<animate attributeName="opacity" values=".55;1;.55" dur="{4 + (idx2 % 3)}s" begin="-{idx2 * .8:.1f}s" repeatCount="indefinite"/></g>')
            b.append(T("mono", label.upper(), 10, tx + 56, ty + 96, "middle", 2, .75))
    return svg(W, H, "".join(b), "", "Tech stack. Languages: C++, Python, TypeScript, JavaScript, SQL. Tools: React, FastAPI, Node.js, Tailwind CSS, Vite. Platform: Git, Vercel, Render, Linux.")


# ------------------------------------------------------------------ quests
def _eye():
    return (f'<circle r="58" fill="none" stroke="{CREAM}" stroke-opacity=".3" stroke-dasharray="1.5 7"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="80s" repeatCount="indefinite"/></circle>'
            f'<circle r="46" fill="none" stroke="{CREAM}" stroke-opacity=".18"/>'
            f'<g><animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 .08;1 1" keyTimes="0;.9;.95;1" dur="6s" repeatCount="indefinite"/>'
            f'<path d="M-42 0Q0 -30 42 0Q0 30 -42 0Z" fill="none" stroke="{CREAM}" stroke-opacity=".85" stroke-width="1.2"/>'
            f'<g><animateTransform attributeName="transform" type="translate" values="0 0;8 0;-7 1;0 0" keyTimes="0;.35;.7;1" dur="9s" repeatCount="indefinite"/>'
            f'<circle r="15" fill="none" stroke="url(#holo)" stroke-width="1.6"/><circle r="5.5" fill="{CREAM}"/></g></g>'
            f'<path d="M0 -70V-60M0 60V70M-70 0H-60M60 0H70" stroke="{CREAM}" stroke-opacity=".5"/>')


def _calc():
    dots = []
    for r in range(4):
        for c in range(3):
            n = r * 3 + c
            dots.append(f'<circle cx="{-16 + c * 16}" cy="{-2 + r * 15}" r="2.6" fill="{CREAM}"><animate attributeName="opacity" values=".25;1;.25" dur="3.6s" begin="-{n * .3:.1f}s" repeatCount="indefinite"/></circle>')
    return (f'<circle r="58" fill="none" stroke="{CREAM}" stroke-opacity=".3" stroke-dasharray="1.5 7"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="80s" repeatCount="indefinite"/></circle>'
            f'<rect x="-30" y="-42" width="60" height="84" rx="5" fill="none" stroke="{CREAM}" stroke-opacity=".85" stroke-width="1.2"/>'
            f'<rect x="-22" y="-34" width="44" height="18" rx="2" fill="none" stroke="url(#holo)" stroke-width="1.2"/>'
            f'<path d="M-15 -25H-3M9 -25H16" stroke="{CREAM}" stroke-opacity=".8"/>' + "".join(dots))


def quest_card(idx, title, subtitle_jp, status_en, status_jp, scol, desc, bullets, tags, emblem):
    W, x0 = 900, 236
    maxw = W - x0 - 48
    b_txt = []
    b_txt.append(T("mono", f"PROJECT {idx}  /  作品", 11, x0, 52, ls=4, op=.5))
    ts = fit("j3", title.upper(), 40, 330, 13)
    b_txt.append(T("j3", title.upper(), ts, x0 - 2, 102, ls=13))
    b_txt.append(T("jp", subtitle_jp, 17, x0, 132, ls=4, op=.8))
    stw = width("mono", status_en, 10, 3) + width("jp", status_jp, 12, 3) + 64
    px = W - 40 - stw
    b_txt.append(f'<rect x="{px:.0f}" y="36" width="{stw:.0f}" height="26" fill="none" stroke="{scol}" stroke-opacity=".6"/>' + blink_dot(px + 15, 49, 2.6, scol, 2.2)
                 + T("jp", status_jp, 12, px + 30, 53, ls=3, fill=scol) + T("mono", status_en, 10, px + 40 + width("jp", status_jp, 12, 3), 53, ls=3, op=.85, fill=scol))
    b_txt.append(hline(x0, W - 40, 152, .14))
    d, n = para("j4", desc, 18.5, x0, 184, maxw, 28, CREAM)
    b_txt.append(f'<g fill-opacity=".85">{d}</g>')
    y = 184 + n * 28 + 4
    for bl in bullets:
        d, k = para("j4", bl, 16.5, x0 + 22, y, maxw - 22, 24, CREAM)
        b_txt.append(f'<rect x="{x0 + 2}" y="{y - 10}" width="6" height="6" fill="none" stroke="{TEAL}"/><g fill-opacity=".7">{d}</g>')
        y += k * 24 + 6
    y += 14
    cx = x0
    for t in tags:
        cw = width("mono", t.upper(), 10, 2) + 26
        b_txt.append(f'<rect x="{cx:.0f}" y="{y:.0f}" width="{cw:.0f}" height="24" fill="none" stroke="{CREAM}" stroke-opacity=".3"/>' + T("mono", t.upper(), 10, cx + cw / 2, y + 16, "middle", 2, .75))
        cx += cw + 10
    H = int(y + 24 + 36)
    body = (frame(W, H) + ticks(0, 0, W, H, 12, .75)
            + T("j2", idx, 150, 22, H - 22, ls=0, op=.05)
            + f'<circle cx="112" cy="{H / 2:.0f}" r="90" fill="url(#halo)"/>'
            + f'<g transform="translate(112 {H / 2:.0f})">{emblem}</g>'
            + f'<g transform="translate({W - 130} {H / 2:.0f})" opacity=".11"><path d="{tunnel(300, 220, 46, 34, 6, 5)}" fill="none" stroke="{CREAM}" stroke-width=".8"/></g>'
            + vline(200, 40, H - 40, .12) + "".join(b_txt) + traveler(0, W, H - 1, 200, 7))
    return svg(W, H, body, "", f"{title}: {desc}")


def quest_argus():
    return quest_card("01", "Argus", "コードを読み解くAIの相棒", "IN DEVELOPMENT", "開発中", "#f5d68a",
                      "An AI-powered codebase companion that helps developers understand and navigate code. My flagship build, currently taking shape.",
                      [], ["AI COMPANION", "DEVELOPER TOOLING", "IN DEVELOPMENT"], _eye())


def quest_aicalc():
    return quest_card("02", "AICalc", "手書きで解く、AI電卓", "LIVE", "公開中", TEAL,
                      "Draw math, physics and chemistry problems on a canvas and receive AI-solved answers rendered in LaTeX. Powered by Gemini 2.5 Flash.",
                      ["Freehand drawing, movable text boxes and step-by-step explanations",
                       "Rotates across N API keys on rate limits, retrying on network errors",
                       "Skips blank-canvas requests and compresses images to 768px to cut API costs",
                       "Token usage tracked locally in the browser"],
                      ["REACT", "TYPESCRIPT", "FASTAPI", "GEMINI 2.5 FLASH", "LATEX"], _calc())


# ------------------------------------------------------------------- feats
def feats():
    W, H = 900, 268
    data = [("2026", "Goldman Sachs India Hackathon", "Advanced to the Interview Round", "面接選考へ進出"),
            ("2025", "Google Agentic AI Day Hackathon", "Invited On-site · BIEC Bengaluru", "現地招待"),
            ("2025 · 26", "Tic Tech Toe Hackathon", "On Campus · DAU", "学内大会")]
    b = [frame(W, H), ticks(0, 0, W, H, 12, .75), T("mono", "ACHIEVEMENTS  /  実績", 11, 40, 44, ls=4, op=.55), hline(40, W - 40, 58, .14), traveler(40, W - 40, 58, 160, 7)]
    for i, (yr, ev, res, jp) in enumerate(data):
        x = 40 + i * 286
        if i:
            b.append(vline(x - 22, 84, H - 34, .1))
        b.append(f'<rect x="{x}" y="86" width="18" height="2" fill="url(#holo)"/>')
        b.append(T("j2", yr, fit("j2", yr, 66, 236, 2), x - 2, 158, ls=2))
        y = 194
        for ln in wrap("j4", ev.upper(), 14.5, 236, 2.4):
            b.append(T("j4", ln, 14.5, x, y, ls=2.4))
            y += 22
        d, k = para("j3", res, 16.5, x, y + 4, 236, 23, CREAM)
        b.append(f'<g fill-opacity=".72">{d}</g>')
        y += 4 + k * 23 + 10
        b.append(f'<rect x="{x}" y="{y - 12}" width="6" height="6" fill="none" stroke="{TEAL}"/>' + T("jp", jp, 13, x + 16, y - 5, ls=3, op=.7))
    return svg(W, H, "".join(b), "", "Achievements: Goldman Sachs India Hackathon 2026 (interview round), Google Agentic AI Day Hackathon 2025 (invited on-site, BIEC Bengaluru), Tic Tech Toe Hackathon 2025 and 2026 (on campus, DAU)")


# ----------------------------------------------------------------- buttons
def _bicon(kind, cx, cy):
    if kind == "github":
        return icon("github", cx, cy, 20, CREAM, .9)
    if kind == "mail":
        return (f'<g transform="translate({cx} {cy})" fill="none" stroke="{CREAM}" stroke-opacity=".9" stroke-width="1.5" stroke-linejoin="round"><rect x="-10" y="-7" width="20" height="14" rx="1.5"/><path d="M-10 -6L0 2L10 -6"/></g>')
    if kind == "in":
        return T("j3", "in", 19, cx, cy + 6, "middle", 0, .9)
    return (f'<g transform="translate({cx} {cy})" fill="none" stroke="{CREAM}" stroke-opacity=".9" stroke-width="1.5" stroke-linejoin="round"><circle r="10"/><path d="M-3 -5L5 0L-3 5Z"/></g>')


def button(label, jp, kind, w=240):
    H = 60
    b = [f'<rect x=".5" y=".5" width="{w - 1}" height="{H - 1}" fill="{PANEL}" stroke="{CREAM}" stroke-opacity=".28"/>', ticks(0, 0, w, H, 7, .9),
         f'<rect x="6.5" y="{H / 2 - 16}" width="1.5" height="32" fill="{TEAL}"><animate attributeName="opacity" values="1;.25;1" dur="2.6s" repeatCount="indefinite"/></rect>',
         _bicon(kind, 36, H / 2), vline(62, 12, H - 12, .16),
         T("j4", label, fit("j4", label, 14, w - 130, 4), 78, 27, ls=4), T("jp", jp, 11.5, 78, 46, ls=3, op=.55),
         f'<path d="M{w - 36} {H / 2}H{w - 18}M{w - 25} {H / 2 - 6}L{w - 18} {H / 2}L{w - 25} {H / 2 + 6}" fill="none" stroke="{CREAM}" stroke-opacity=".8"/>',
         traveler(0, w, H - 1, 100, 3.6)]
    return svg(w, H, "".join(b), "", f"{label}")




# ------------------------------------------------------------------ header
def header():
    W, H = 1200, 460
    rng = random.Random(11)
    AX, AY, AR = 236, 232, 118
    x0 = 470
    defs = (f'<clipPath id="av"><circle cx="{AX}" cy="{AY}" r="{AR}"/></clipPath>'
            f'<linearGradient id="hbg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0b0e15" stop-opacity="0"/><stop offset=".6" stop-color="#0f121a"/><stop offset="1" stop-color="#090b11"/></linearGradient>')
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>', f'<rect width="{W}" height="{H}" fill="url(#hbg)"/>',
         aurora([(250, 250, 300, 210, TEAL, .13, 26, 22), (950, 130, 330, 170, PINK, .10, 34, 28), (760, 440, 400, 130, LILAC, .12, 40, 32)]),
         kana_rain(rng, [28, 58, 414, 442, 972, 1004, 1038, 1072], H, 15, 13, .15),
         '<g transform="translate(790 232)" opacity=".16"><g><animateTransform attributeName="transform" type="scale" values="1;1.07;1" dur="18s" repeatCount="indefinite" '
         'calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
         f'<path d="{tunnel(1300, 760, 210, 120, 10, 8)}" fill="none" stroke="{CREAM}" stroke-width=".8" vector-effect="non-scaling-stroke"/></g></g>',
         dust(rng, 14, W, H)]
    # ---- portrait + HUD
    b.append(f'<circle cx="{AX}" cy="{AY}" r="240" fill="url(#halo)"/>')
    b.append(f'<circle cx="{AX}" cy="{AY}" r="152" fill="none" stroke="{CREAM}" stroke-opacity=".38" stroke-width="7" stroke-dasharray="1.2 6.758">'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {AX} {AY}" to="360 {AX} {AY}" dur="240s" repeatCount="indefinite"/></circle>')
    b.append(f'<circle cx="{AX}" cy="{AY}" r="140" fill="none" stroke="{CREAM}" stroke-opacity=".28" stroke-dasharray="3 6">'
             f'<animateTransform attributeName="transform" type="rotate" from="360 {AX} {AY}" to="0 {AX} {AY}" dur="90s" repeatCount="indefinite"/></circle>')
    b.append(f'<circle cx="{AX}" cy="{AY}" r="129" fill="none" stroke="url(#holo)" stroke-width="2" stroke-linecap="round" stroke-dasharray="150 660">'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {AX} {AY}" to="360 {AX} {AY}" dur="12s" repeatCount="indefinite"/></circle>')
    b.append(f'<path d="{arc(AX, AY, 172, -35, 35)}{arc(AX, AY, 172, 85, 155)}{arc(AX, AY, 172, 205, 275)}" fill="none" stroke="{CREAM}" stroke-opacity=".5" stroke-width="1.4">'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {AX} {AY}" to="-360 {AX} {AY}" dur="60s" repeatCount="indefinite"/></path>')
    b.append(f'<circle cx="{AX}" cy="{AY - 152}" r="3" fill="{PINK}"><animateTransform attributeName="transform" type="rotate" from="0 {AX} {AY}" to="360 {AX} {AY}" dur="20s" repeatCount="indefinite"/></circle>')
    b.append(f'<image href="{data_uri(os.path.join(HERE, "avatar.png"))}" x="{AX - AR}" y="{AY - AR}" width="{AR * 2}" height="{AR * 2}" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/>')
    b.append(f'<circle cx="{AX}" cy="{AY}" r="{AR}" fill="none" stroke="{CREAM}" stroke-opacity=".7"/>')
    for ang, lab in ((-90, "000"), (0, "090"), (90, "180"), (180, "270")):
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        b.append(f'<path d="M{AX + ca * 180:.1f} {AY + sa * 180:.1f}L{AX + ca * 192:.1f} {AY + sa * 192:.1f}" stroke="{CREAM}" stroke-opacity=".6"/>')
    b.append(T("mono", "AK01177", 11, AX, 38, "middle", 6, .6))
    b.append(T("mono", "ID · 001  /  オンライン", 10, AX, H - 24, "middle", 4, .4))
    b.append(T("mono", "000", 8, AX, AY - 198, "middle", 2, .35))

    # ---- title block
    b.append(T("mono", "PORTFOLIO  /  ポートフォリオ", 11, x0, 92, ls=4, op=.55))
    b.append(hline(x0, x0 + 34, 108, .5))
    b.append(glitch("g1", "j2", "ARYAN", 78, x0 - 4, 198, ls=22, period=7.0, begin=0))
    b.append(glitch("g2", "j2", "RANAVAT", 78, x0 - 4, 280, ls=22, period=7.0, begin=.25))
    b.append(T("jp", "アーリヤン・ラナヴァト", 19, x0, 318, ls=9, op=.78))
    b.append(f'<rect x="{x0}" y="336" width="380" height="1.4" fill="url(#holo)"/>' + traveler(x0, x0 + 380, 336.7, 110, 4.5))
    b.append(T("mono", "SOFTWARE  /  SYSTEMS  /  MACHINE LEARNING", 12, x0, 366, ls=3, op=.85))
    b.append(T("jp", "ソフトウェア開発 ・ システム設計 ・ 機械学習", 14, x0, 390, ls=4, op=.55))
    b.append(blink_dot(x0 + 4, 420, 3))
    sw = width("mono", "OPEN TO INTERNSHIPS", 11, 3)
    b.append(T("mono", "OPEN TO INTERNSHIPS", 11, x0 + 18, 424, ls=3, op=.8))
    b.append(T("jp", "インターンシップを探しています", 12, x0 + 30 + sw, 424, ls=3, op=.5))

    # ---- right edge
    b.append(vline(1112, 90, 346, .16))
    b.append(vtxt("jp", "未来を創る", 26, 1148, 128, CREAM, 1.5, 'fill-opacity=".8"'))
    b.append(rtxt("mono", "BUILDING THE FUTURE", 10, 1182, 110, CREAM, 90, "start", 5, 'fill-opacity=".4"'))
    b.append(T("mono", "2026  ·  23.22°N  72.64°E", 11, W - 60, 48, "end", 3, .5))
    b.append(equalizer(1096, 424, 12, 30))
    b.append(T("mono", "SIGNAL", 8.5, 1180, 440, "end", 3, .35))
    b.append(scan(W, H, 10, 110))
    b.append(ticks(14, 14, W - 28, H - 28, 16, .55))
    for px, py in ((470, 48), (1080, 410), (430, 358)):
        b.append(plus(px, py, 4, .5))
    return svg(W, H, "".join(b), defs, "Aryan Ranavat. Software, systems and machine learning. B.Tech ICT student at DA-IICT, Gandhinagar.")


# --------------------------------------------------------------- marquee
def marquee():
    W, H = 900, 108
    u1 = "FUTURE  ·  未来  ·  DESIGN  ·  設計  ·  CODE  ·  開発  ·  LEARN  ·  学習  ·  "
    u2 = "// BUILD QUIETLY  ·  静かに作る  ·  SHIP BOLDLY  ·  大胆に届ける  ·  "
    w1, w2 = width("j2", u1, 50, 12), width("mono", u2, 11, 4)
    defs = f'<path id="m1" d="{pathd("j2", u1, 50, 0, 62, "start", 12)}"/>'
    row2 = txt("mono", u2, 11, 0, 94, CREAM, "start", 4, 'fill-opacity=".45"')
    b = [frame(W, H), ticks(0, 0, W, H, 10, .7),
         f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{-w1:.0f} 0" dur="46s" repeatCount="indefinite"/>'
         f'<use href="#m1" fill="none" stroke="url(#holo)" stroke-width="1" /><use href="#m1" x="{w1:.0f}" fill="none" stroke="url(#holo)" stroke-width="1"/></g>',
         f'<g><animateTransform attributeName="transform" type="translate" values="{-w2:.0f} 0;0 0" dur="38s" repeatCount="indefinite"/>'
         f'{row2}<g transform="translate({w2:.0f} 0)">{row2}</g><g transform="translate({2 * w2:.0f} 0)">{row2}</g></g>',
         f'<rect width="70" height="{H}" fill="{INK}" opacity=".0"/>']
    # soft edge fades
    b.append(f'<linearGradient id="ef" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PANEL}"/><stop offset="1" stop-color="{PANEL}" stop-opacity="0"/></linearGradient>'
             f'<rect x="1" y="1" width="90" height="{H - 2}" fill="url(#ef)"/><rect x="{W - 91}" y="1" width="90" height="{H - 2}" fill="url(#ef)" transform="translate({W * 2 - 2} 0) scale(-1 1)"/>')
    return svg(W, H, "".join(b), defs, "Future, design, code, learn. Build quietly, ship boldly.")


# ------------------------------------------------------------- manifesto
def manifesto():
    W, H = 900, 340
    defs = f'<clipPath id="mclip"><rect x="1" y="1" width="{W - 2}" height="{H - 2}"/></clipPath>'
    fs = fit("j2", "BUILD QUIETLY.", 46, 400, 9)
    b = [frame(W, H), ticks(0, 0, W, H, 12, .75),
         f'<g clip-path="url(#mclip)">',
         aurora([(170, 190, 200, 160, PINK, .10, 20, 24), (560, 300, 260, 110, TEAL, .09, 28, 30)]),
         f'<g transform="translate(168 176)" opacity=".13"><path d="{tunnel(560, 360, 90, 60, 8, 6)}" fill="none" stroke="{CREAM}" stroke-width=".8"/></g>',
         otxt("jp", "創", 300, 20, 296, "url(#holo)", "start", 0, 1.3, .95),
         T("jp", "創", 300, 20, 296, "start", 0, .04),
         "</g>",
         T("mono", "// CREED  /  信条", 11, 360, 70, ls=4, op=.55), hline(360, 392, 84, .5),
         glitch("g3", "j2", "BUILD QUIETLY.", fs, 360, 164, ls=9, period=9, begin=2),
         glitch("g4", "j2", "SHIP BOLDLY.", fs, 360, 164 + fs * 1.5, ls=9, period=9, begin=2.3),
         f'<rect x="360" y="{164 + fs * 1.5 + 26:.0f}" width="300" height="1.4" fill="url(#holo)"/>',
         T("mono", "QUIET CRAFT  ·  BOLD DELIVERY", 10.5, 360, 164 + fs * 1.5 + 54, ls=4, op=.55),
         vline(756, 60, H - 40, .14),
         vtxt("jp", "静かに作る", 28, 850, 84, CREAM, 1.46, 'fill-opacity=".9"'),
         vtxt("jp", "大胆に届ける", 28, 800, 84, CREAM, 1.46, 'fill-opacity=".6"'),
         plus(342, 40, 4, .5), plus(W - 34, H - 34, 4, .5), scan(W, H, 11, 100, .8), traveler(0, W, H - 1, 200, 7)]
    return svg(W, H, "".join(b), defs, "Creed: build quietly, ship boldly.")


# ------------------------------------------------------- footer & skyline
def _pagoda(cx, base, s=1.0):
    g = [f'<g transform="translate({cx} {base}) scale({s})" fill="{INK}" stroke="{CREAM}" stroke-opacity=".62" stroke-width=".9" stroke-linejoin="round">',
         '<rect x="-48" y="-7" width="96" height="7"/><rect x="-40" y="-14" width="80" height="7"/>']
    y = -14
    for i in range(5):
        hw, bw = 36 - 4.5 * i, (36 - 4.5 * i) * .6
        g.append(f'<rect x="{-bw:.1f}" y="{y - 15}" width="{2 * bw:.1f}" height="15"/><path d="M{-bw * .3:.1f} {y - 4}V{y - 11}M{bw * .3:.1f} {y - 4}V{y - 11}" fill="none"/>')
        y -= 15
        g.append(f'<path d="M{-hw - 9:.1f} {y - 5}Q{-hw + 2:.1f} {y} {-hw + 10:.1f} {y}H{hw - 10:.1f}Q{hw - 2:.1f} {y} {hw + 9:.1f} {y - 5}Q{hw - 6:.1f} {y - 7} {hw - 14:.1f} {y - 14}H{-hw + 14:.1f}Q{-hw + 6:.1f} {y - 7} {-hw - 9:.1f} {y - 5}Z"/>')
        y -= 14
    g.append(f'<path d="M0 {y}V{y - 34}" fill="none"/><path d="M-5 {y - 10}H5M-4 {y - 18}H4M-3 {y - 26}H3" fill="none"/>')
    g.append(f'<circle cx="0" cy="{y - 38}" r="2.4" fill="{PINK}" stroke="none"><animate attributeName="opacity" values="1;.2;1" dur="2.2s" repeatCount="indefinite"/></circle></g>')
    return "".join(g)


def _tower(cx, base, s=1.0):
    half = lambda y: 36 - 30 * (-y) / 132
    g = [f'<g transform="translate({cx} {base}) scale({s})" fill="none" stroke="{CREAM}" stroke-opacity=".6" stroke-width=".9" stroke-linejoin="round">',
         f'<path d="M-36 0L-6 -132M36 0L6 -132"/>']
    lv = [0, -26, -52, -80, -108, -132]
    for a, c in zip(lv, lv[1:]):
        g.append(f'<path d="M{-half(a):.1f} {a}L{half(c):.1f} {c}M{half(a):.1f} {a}L{-half(c):.1f} {c}M{-half(c):.1f} {c}H{half(c):.1f}" stroke-opacity=".35"/>')
    g.append(f'<rect x="{-half(-56) - 6:.1f}" y="-60" width="{2 * half(-56) + 12:.1f}" height="7" fill="{INK}"/><rect x="{-half(-104) - 4:.1f}" y="-107" width="{2 * half(-104) + 8:.1f}" height="5" fill="{INK}"/>')
    g.append(f'<path d="M0 -132V-196"/><path d="M-3 -150H3M-2 -166H2" />')
    g.append(f'<circle cx="0" cy="-199" r="2.6" fill="{PINK}" stroke="none"><animate attributeName="opacity" values="1;.15;1" dur="1.6s" repeatCount="indefinite"/></circle></g>')
    return "".join(g)


def footer():
    W, H = 1200, 400
    HZ = 232
    rng = random.Random(2)
    N = 9
    yf = lambda i: HZ + (H - HZ + 40) * (i / N) ** 2.0
    of = lambda i: .10 + .5 * min(1, i / N)
    defs = (f'<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CREAM}"/><stop offset=".5" stop-color="{PINK}"/><stop offset="1" stop-color="{LILAC}"/></linearGradient>'
            f'<mask id="stripes"><rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>'
            + "".join(f'<rect x="0" y="{HZ - 70 + k * 12 + k * k * .6:.1f}" width="{W}" height="{1 + k * .6:.1f}" fill="#000"/>' for k in range(1, 8))
            + f'</mask><clipPath id="above"><rect x="0" y="0" width="{W}" height="{HZ}"/></clipPath>'
            f'<linearGradient id="floorfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient>'
            f'<radialGradient id="scrim"><stop offset="0" stop-color="{INK}" stop-opacity=".88"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient>')
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>',
         aurora([(300, 150, 340, 120, TEAL, .10, 30, 26), (900, 130, 340, 110, PINK, .10, 34, 30), (600, 230, 360, 100, LILAC, .12, 24, 24)]),
         stars(rng, 70, W, HZ - 70), dust(rng, 10, W, HZ),
         f'<circle cx="600" cy="{HZ - 20}" r="260" fill="url(#halo)"/>',
         f'<g clip-path="url(#above)" mask="url(#stripes)"><circle cx="600" cy="{HZ - 14}" r="84" fill="url(#sun)" fill-opacity=".95"><animate attributeName="fill-opacity" values=".82;1;.82" dur="8s" repeatCount="indefinite"/></circle></g>']
    # skyline
    x, flick, wins = -10, [], []
    while x < W + 10:
        w = rng.uniform(26, 58)
        h = rng.uniform(24, 100) * (.35 + .95 * abs(x + w / 2 - 600) / 600) + 12
        b.append(f'<rect x="{x:.0f}" y="{HZ - h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{INK}" fill-opacity=".96" stroke="{CREAM}" stroke-opacity=".34" stroke-width=".8"/>')
        for wy in range(int(HZ - h + 8), HZ - 4, 8):
            for wx in range(int(x + 5), int(x + w - 4), 7):
                r = rng.random()
                if r < .30:
                    wins.append(f"M{wx} {wy}h2v2h-2Z")
                elif r < .33 and len(flick) < 26:
                    flick.append(f'<rect x="{wx}" y="{wy}" width="2" height="2" fill="{TEAL}" opacity="0"><animate attributeName="opacity" values="0;.9;0" dur="{rng.uniform(2, 6):.1f}s" begin="-{rng.uniform(0, 5):.1f}s" repeatCount="indefinite"/></rect>')
        if rng.random() < .3:
            flick.append(f'<circle cx="{x + w / 2:.0f}" cy="{HZ - h - 3:.0f}" r="1.6" fill="{PINK}"><animate attributeName="opacity" values="1;.1;1" dur="{rng.uniform(1.4, 3):.1f}s" repeatCount="indefinite"/></circle>')
        x += w + rng.uniform(0, 5)
    b.append(f'<path d="{"".join(wins)}" fill="{CREAM}" fill-opacity=".38"/>' + "".join(flick))
    b += [_pagoda(236, HZ, 1.0), _tower(980, HZ, 1.05)]
    rays = "".join(f"M600 {HZ}L{600 + j * 150} {H + 40}" for j in range(-14, 15))
    b.append(f'<path d="{rays}" stroke="{CREAM}" stroke-opacity=".3" stroke-width=".8" fill="none"/>')
    for i in range(N + 1):
        b.append(f'<rect x="0" y="{yf(i):.1f}" width="{W}" height="1" fill="{CREAM}" fill-opacity="{of(i):.2f}">'
                 f'<animate attributeName="y" values="{yf(i):.1f};{yf(i + 1):.1f}" dur="3.2s" repeatCount="indefinite"/>'
                 f'<animate attributeName="fill-opacity" values="{of(i):.2f};{of(i + 1):.2f}" dur="3.2s" repeatCount="indefinite"/></rect>')
    b.append(f'<rect x="0" y="{HZ}" width="{W}" height="70" fill="url(#floorfade)"/>')
    b.append(hline(0, W, HZ, .55))
    b.append(traveler(0, W, HZ, 260, 8))
    b += [f'<ellipse cx="600" cy="334" rx="440" ry="76" fill="url(#scrim)"/>',
          T("jp", "ご訪問ありがとうございます", 28, 600, 322, "middle", 12, .95),
          T("j3", "THANK YOU FOR VISITING", 13, 600, 352, "middle", 13, .65),
          T("mono", "© 2026 ARYAN RANAVAT  ·  DA-IICT", 10, 600, 376, "middle", 4, .42),
          ticks(14, 14, W - 28, H - 28, 16, .5), plus(60, 60, 4, .5), plus(1140, 96, 4, .5)]
    return svg(W, H, "".join(b), defs, "Thank you for visiting.")
