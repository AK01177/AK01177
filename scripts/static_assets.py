"""Static SVG assets: calm, premium, Japanese-typographic. Everything is designed at 900px (GitHub's README width)."""
import math
import random

from aes import *  # noqa: F401,F403
from aes import _n


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


# ------------------------------------------------------------------ header
def header():
    W, H = 900, 410
    AX, AY, AR = 148, 200, 100
    x0 = 304
    defs = (f'<clipPath id="av"><circle cx="{AX}" cy="{AY}" r="{AR}"/></clipPath>'
            f'<linearGradient id="hbg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0b0e15" stop-opacity="0"/><stop offset=".6" stop-color="#0f121a"/><stop offset="1" stop-color="#090b11"/></linearGradient>')
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>', f'<rect width="{W}" height="{H}" fill="url(#hbg)"/>',
         aurora([(150, 210, 230, 180, TEAL, .10, 16, 26), (730, 110, 270, 150, PINK, .07, 22, 30)]),
         '<g transform="translate(640 205)" opacity=".12"><g><animateTransform attributeName="transform" type="scale" values="1;1.05;1" dur="28s" repeatCount="indefinite" '
         'calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
         f'<path d="{tunnel(1100, 640, 190, 110, 9, 8)}" fill="none" stroke="{CREAM}" stroke-width=".8" vector-effect="non-scaling-stroke"/></g></g>',
         f'<circle cx="{AX}" cy="{AY}" r="190" fill="url(#halo)"/>',
         f'<circle cx="{AX}" cy="{AY}" r="128" fill="none" stroke="{CREAM}" stroke-opacity=".34" stroke-width="6" stroke-dasharray="1.1 5.6"/>',
         f'<circle cx="{AX}" cy="{AY}" r="118" fill="none" stroke="{CREAM}" stroke-opacity=".22" stroke-dasharray="3 6"/>',
         f'<circle cx="{AX}" cy="{AY}" r="110" fill="none" stroke="url(#holo)" stroke-width="2" stroke-linecap="round" stroke-dasharray="120 571">'
         f'<animateTransform attributeName="transform" type="rotate" from="0 {AX} {AY}" to="360 {AX} {AY}" dur="26s" repeatCount="indefinite"/></circle>',
         f'<image href="{data_uri(os.path.join(HERE, "avatar.png"))}" x="{AX - AR}" y="{AY - AR}" width="{AR * 2}" height="{AR * 2}" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/>',
         f'<circle cx="{AX}" cy="{AY}" r="{AR}" fill="none" stroke="{CREAM}" stroke-opacity=".7"/>',
         T("mono", "AK01177", 12, AX, 366, "middle", 6, .8)]
    b.append(T("mono", "PORTFOLIO  /  ポートフォリオ", 12.5, x0, 92, ls=4, op=.8))
    b.append(T("j2", "ARYAN", 62, x0 - 3, 172, ls=16))
    b.append(T("j2", "RANAVAT", 62, x0 - 3, 240, ls=16))
    b.append(T("jp", "アーリヤン・ラナヴァト", 18, x0, 278, ls=8, op=.88))
    b.append(f'<rect x="{x0}" y="298" width="340" height="1.4" fill="url(#holo)"/>')
    b.append(T("mono", "SOFTWARE  /  SYSTEMS  /  MACHINE LEARNING", 13, x0, 330, ls=3, op=.95))
    b.append(T("jp", "ソフトウェア開発 ・ システム設計 ・ 機械学習", 15, x0, 354, ls=3, op=.78))
    b.append(f'<circle cx="{x0 + 4}" cy="384" r="3.2" fill="{TEAL}"/>')
    sw = width("mono", "OPEN TO INTERNSHIPS", 12, 3)
    b.append(T("mono", "OPEN TO INTERNSHIPS", 12, x0 + 18, 388, ls=3, op=.9))
    b.append(T("jp", "インターンシップを探しています", 14, x0 + 34 + sw, 388, ls=2, op=.7))
    b.append(vline(828, 92, 330, .16))
    b.append(vtxt("jp", "未来を創る", 22, 862, 122, CREAM, 1.55, 'fill-opacity=".85"'))
    b.append(ticks(12, 12, W - 24, H - 24, 14, .5))
    return svg(W, H, "".join(b), defs, "Aryan Ranavat. Software, systems and machine learning. B.Tech ICT student at DA-IICT, Gandhinagar.")


# --------------------------------------------------- section header/divider
def section_header(idx, en, jp):
    W, H = 900, 84
    e = en.upper()
    ew = width("j3", e, 28, 12)
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>', T("jp", jp, 86, W - 10, 74, "end", 8, .06),
         T("mono", idx, 14, 14, 44, ls=2, op=.7),
         T("j3", e, 28, 62, 46, ls=12), T("jp", jp, 18, 62 + ew + 26, 45, ls=6, op=.85),
         hline(0, W, 66, .16), f'<rect x="0" y="65" width="44" height="2" fill="{CREAM}" fill-opacity=".85"/>']
    return svg(W, H, "".join(b), "", en)


def divider():
    W, H = 900, 30
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>', hline(0, 410, 15, .12), hline(490, W, 15, .12), plus(450, 15, 5, .7)]
    return svg(W, H, "".join(b), "", "divider")


# --------------------------------------------------------------- about card
def about():
    W, H = 900, 428
    rows = [("NAME", "名前", "Aryan Ranavat"),
            ("AFFILIATION", "所属", "B.Tech ICT · DA-IICT, Gandhinagar"),
            ("FOCUS", "専門", "Full Stack · System Design · Machine Learning"),
            ("CP LANGUAGE", "競技", "C++, for competitive programming"),
            ("BUILD STACK", "開発", "TypeScript & Python, for projects"),
            ("NOW", "現在", "Argus, an AI-powered codebase companion"),
            ("GOAL", "目標", "Software engineering internships & placements")]
    b = [card(W, H), ptitle("PROFILE", "プロフィール", 640)]
    y = 104
    for en, jp, val in rows:
        b.append(T("mono", en, 11.5, 40, y - 5, ls=3, op=.75))
        b.append(T("jp", jp, 13.5, 40, y + 13, ls=3, op=.7))
        b.append(T("j4", val, fit("j4", val, 20, 392), 232, y + 5))
        b.append(hline(40, 640, y + 24, .08))
        y += 46
    b.append(vline(664, 84, H - 36, .12))
    b.append(f'<circle cx="748" cy="222" r="96" fill="url(#halo)"/>')
    b.append(cube(738, 222, 112, .95, 12))
    b.append(vtxt("jp", "開発者", 22, 862, 104, CREAM, 1.55, 'fill-opacity=".8"'))
    b.append(T("mono", "DA-IICT  ·  2024", 12, 764, H - 34, "middle", 3, .65))
    return svg(W, H, "".join(b), "", "Profile: Aryan Ranavat, B.Tech ICT at DA-IICT Gandhinagar. Focus on full stack, system design and machine learning. C++ for competitive programming, TypeScript and Python for projects. Current project Argus. Seeking software engineering internships and placements.")


# ------------------------------------------------------------------- stack
TIERS = [
    ("01", "LANGUAGES", "言語", [("C++", "cplusplus"), ("Python", "python"), ("TypeScript", "typescript"), ("JavaScript", "javascript"), ("SQL", "mysql")]),
    ("02", "TOOLS", "ツール", [("React", "react"), ("FastAPI", "fastapi"), ("Node.js", "nodedotjs"), ("Tailwind", "tailwindcss"), ("Vite", "vite")]),
    ("03", "PLATFORM", "基盤", [("Git", "git"), ("Vercel", "vercel"), ("Render", "render"), ("Linux", "linux")]),
]


def stack():
    RH = 140
    W, H = 900, 84 + RH * 3
    b = [card(W, H), ptitle("TECH STACK", "技術スタック", W)]
    for r, (idx, en, jp, items) in enumerate(TIERS):
        top = 90 + r * RH
        b.append(T("mono", idx, 12, 40, top + 24, ls=3, op=.7))
        b.append(T("j3", en, 20, 40, top + 58, ls=8))
        b.append(T("jp", jp, 15, 40, top + 82, ls=5, op=.8))
        if r:
            b.append(hline(40, W - 40, top - 12, .08))
        for i, (label, ic) in enumerate(items):
            tx = 250 + i * 124
            b.append(f'<rect x="{tx + .5}" y="{top + .5}" width="111" height="111" fill="none" stroke="{CREAM}" stroke-opacity=".14"/>')
            b.append(icon(ic, tx + 56, top + 44, 40, CREAM, .95))
            b.append(T("mono", label.upper(), 12, tx + 56, top + 94, "middle", 2, .9))
    return svg(W, H, "".join(b), "", "Tech stack. Languages: C++, Python, TypeScript, JavaScript, SQL. Tools: React, FastAPI, Node.js, Tailwind CSS, Vite. Platform: Git, Vercel, Render, Linux.")


# ------------------------------------------------------------------ projects
def _eye():
    return (f'<circle r="58" fill="none" stroke="{CREAM}" stroke-opacity=".28" stroke-dasharray="1.5 7"/>'
            f'<g><animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 .08;1 1" keyTimes="0;.92;.96;1" dur="9s" repeatCount="indefinite"/>'
            f'<path d="M-42 0Q0 -30 42 0Q0 30 -42 0Z" fill="none" stroke="{CREAM}" stroke-opacity=".9" stroke-width="1.3"/>'
            f'<circle r="15" fill="none" stroke="url(#holo)" stroke-width="1.6"/><circle r="5.5" fill="{CREAM}"/></g>'
            f'<path d="M0 -70V-60M0 60V70M-70 0H-60M60 0H70" stroke="{CREAM}" stroke-opacity=".5"/>')


def _calc():
    dots = "".join(f'<circle cx="{-16 + c * 16}" cy="{-2 + r * 15}" r="2.6" fill="{CREAM}" fill-opacity=".9"/>' for r in range(4) for c in range(3))
    return (f'<circle r="58" fill="none" stroke="{CREAM}" stroke-opacity=".28" stroke-dasharray="1.5 7"/>'
            f'<rect x="-30" y="-42" width="60" height="84" rx="5" fill="none" stroke="{CREAM}" stroke-opacity=".9" stroke-width="1.3"/>'
            f'<rect x="-22" y="-34" width="44" height="18" rx="2" fill="none" stroke="url(#holo)" stroke-width="1.3"/>'
            f'<path d="M-15 -25H-3M9 -25H16" stroke="{CREAM}" stroke-opacity=".85"/>' + dots)


def _globe():
    R = 42
    lat = "".join(f"M{-math.sqrt(R * R - y * y):.1f} {y}H{math.sqrt(R * R - y * y):.1f}" for y in (-28, -14, 0, 14, 28))
    mer = "".join(f'<ellipse rx="{R}" ry="{R}" fill="none" stroke="{CREAM}" stroke-opacity=".5"><animate attributeName="rx" values="{R};1;{R}" dur="30s" begin="-{k * 10}s" repeatCount="indefinite"/></ellipse>' for k in range(3))
    return (f'<circle r="58" fill="none" stroke="{CREAM}" stroke-opacity=".28" stroke-dasharray="1.5 7"/>'
            f'<circle r="{R}" fill="none" stroke="{CREAM}" stroke-opacity=".9" stroke-width="1.3"/>'
            f'<path d="{lat}" stroke="{CREAM}" stroke-opacity=".35" fill="none"/>{mer}'
            f'<circle cx="16" cy="-14" r="3" fill="{TEAL}"/><path d="M-70 0H-60M60 0H70M0 -70V-60M0 60V70" stroke="{CREAM}" stroke-opacity=".5"/>')


def quest_card(idx, title, subtitle_jp, status_en, status_jp, scol, desc, bullets, tags, emblem):
    W, x0 = 900, 232
    maxw = W - x0 - 44
    t = []
    t.append(T("mono", f"PROJECT {idx}  /  作品", 12, x0, 52, ls=4, op=.75))
    ts = fit("j3", title.upper(), 38, 340, 13)
    t.append(T("j3", title.upper(), ts, x0 - 2, 106, ls=13))
    t.append(T("jp", subtitle_jp, 17, x0, 138, ls=4, op=.88))
    jw, ew = width("jp", status_jp, 13, 3), width("mono", status_en, 11.5, 3)
    stw = jw + ew + 62
    px = W - 40 - stw
    t.append(f'<rect x="{px:.0f}" y="34" width="{stw:.0f}" height="28" fill="none" stroke="{scol}" stroke-opacity=".7"/><circle cx="{px + 15:.0f}" cy="48" r="3" fill="{scol}"/>'
             + T("jp", status_jp, 13, px + 28, 53, ls=3, fill=scol) + T("mono", status_en, 11.5, px + 40 + jw, 53, ls=3, op=.95, fill=scol))
    t.append(hline(x0, W - 40, 158, .14))
    d, n = para("j4", desc, 19, x0, 192, maxw, 29, CREAM)
    t.append(f'<g fill-opacity=".92">{d}</g>')
    y = 192 + n * 29 + 6
    for bl in bullets:
        d, k = para("j4", bl, 17, x0 + 22, y, maxw - 22, 25, CREAM)
        t.append(f'<rect x="{x0 + 2}" y="{y - 10}" width="6" height="6" fill="none" stroke="{TEAL}"/><g fill-opacity=".82">{d}</g>')
        y += k * 25 + 7
    y += 12
    cx = x0
    for tag in tags:
        cw = width("mono", tag, 11.5, 2) + 26
        if cx + cw > W - 40:
            cx, y = x0, y + 34
        t.append(f'<rect x="{cx:.0f}" y="{y:.0f}" width="{cw:.0f}" height="26" fill="none" stroke="{CREAM}" stroke-opacity=".34"/>' + T("mono", tag, 11.5, cx + cw / 2, y + 17.5, "middle", 2, .9))
        cx += cw + 8
    H = int(y + 26 + 36)
    body = (card(W, H) + f'<circle cx="108" cy="{H / 2:.0f}" r="92" fill="url(#halo)"/>' + f'<g transform="translate(108 {H / 2:.0f})">{emblem}</g>'
            + vline(200, 44, H - 44, .12) + "".join(t))
    return svg(W, H, body, "", f"{title}: {desc}")


def quest_godiglobe():
    return quest_card("01", "GodiGlobe", "世界のニュースを地球儀で", "LIVE", "公開中", TEAL,
                      "A full-stack news explorer that maps global headlines onto an interactive 3D globe. Click a country, or drill into states and provinces, to read cached, deduplicated articles.",
                      ["WebGL globe with country polygons, state boundaries and labelled major nations",
                       "Smart caching: stale articles refresh in the background after two hours",
                       "Articles are keyed by URL, so the same story never appears twice"],
                      ["REACT", "VITE", "TAILWIND", "FASTAPI", "SQLALCHEMY", "SQLITE"], _globe())


def quest_aicalc():
    return quest_card("02", "AICalc", "手書きで解く、AI電卓", "LIVE", "公開中", TEAL,
                      "Draw math, physics and chemistry problems on a canvas and receive AI-solved answers rendered in LaTeX. Powered by Gemini 2.5 Flash.",
                      ["Freehand drawing, movable text boxes and step-by-step explanations",
                       "Rotates across N API keys on rate limits and retries on network errors",
                       "Cuts API cost by skipping blank canvases and compressing images to 768px"],
                      ["REACT", "TYPESCRIPT", "FASTAPI", "GEMINI 2.5 FLASH", "LATEX"], _calc())


def quest_argus():
    return quest_card("03", "Argus", "コードを読み解くAIの相棒", "IN DEVELOPMENT", "開発中", "#f5d68a",
                      "An AI-powered codebase companion that helps developers understand and navigate code. A full-stack build with a backend, a frontend and a Docker Compose setup, currently in development.",
                      [], ["AI COMPANION", "FULL STACK", "DOCKER COMPOSE", "GITHUB ACTIONS"], _eye())


# ------------------------------------------------------------ achievements
def feats():
    W, H = 900, 322
    data = [("2026", "Goldman Sachs India Hackathon", "Advanced to the Interview Round", "面接選考へ進出"),
            ("2025", "Google Agentic AI Day Hackathon", "Invited On-site · BIEC Bengaluru", "現地招待"),
            ("2025 · 26", "Tic Tech Toe Hackathon", "On Campus · DAU", "学内大会")]
    b = [card(W, H), ptitle("ACHIEVEMENTS", "実績", W)]
    for i, (yr, ev, res, jp) in enumerate(data):
        x = 40 + i * 288
        if i:
            b.append(vline(x - 22, 92, H - 36, .1))
        b.append(f'<rect x="{x}" y="92" width="18" height="2" fill="url(#holo)"/>')
        b.append(T("j2", yr, fit("j2", yr, 60, 232, 2), x - 2, 158, ls=2))
        y = 194
        for ln in wrap("j4", ev.upper(), 15, 232, 2.2):
            b.append(T("j4", ln, 15, x, y, ls=2.2))
            y += 22
        d, k = para("j3", res, 18, x, y + 6, 232, 25, CREAM)
        b.append(f'<g fill-opacity=".88">{d}</g>')
        y = H - 38
        b.append(f'<rect x="{x}" y="{y - 11}" width="6" height="6" fill="none" stroke="{TEAL}"/>' + T("jp", jp, 14, x + 16, y - 4, ls=3, op=.8))
    return svg(W, H, "".join(b), "", "Achievements: Goldman Sachs India Hackathon 2026 (interview round), Google Agentic AI Day Hackathon 2025 (invited on-site, BIEC Bengaluru), Tic Tech Toe Hackathon 2025 and 2026 (on campus, DAU)")


# ----------------------------------------------------------------- buttons
def _bicon(kind, cx, cy):
    g = f'fill="none" stroke="{CREAM}" stroke-opacity=".95" stroke-width="1.5" stroke-linejoin="round"'
    if kind == "github":
        return icon("github", cx, cy, 20, CREAM, .95)
    if kind == "mail":
        return f'<g transform="translate({cx} {cy})" {g}><rect x="-10" y="-7" width="20" height="14" rx="1.5"/><path d="M-10 -6L0 2L10 -6"/></g>'
    if kind == "in":
        return T("j3", "in", 19, cx, cy + 6, "middle", 0, .95)
    return f'<g transform="translate({cx} {cy})" {g}><circle r="10"/><path d="M-10 0H10M0 -10Q-6 0 0 10M0 -10Q6 0 0 10" stroke-width="1.2"/></g>'


def button(label, jp, kind, w=270):
    H = 58
    b = [f'<rect x=".5" y=".5" width="{w - 1}" height="{H - 1}" fill="{PANEL}" stroke="{CREAM}" stroke-opacity=".3"/>',
         f'<rect width="3" height="{H}" fill="{TEAL}" fill-opacity=".9"/>',
         _bicon(kind, 34, H / 2), vline(60, 12, H - 12, .16),
         T("j4", label, fit("j4", label, 15, w - 124, 4), 78, 26, ls=4), T("jp", jp, 12.5, 78, 46, ls=3, op=.75),
         f'<path d="M{w - 38} {H / 2}H{w - 18}M{w - 26} {H / 2 - 6}L{w - 18} {H / 2}L{w - 26} {H / 2 + 6}" fill="none" stroke="{CREAM}" stroke-opacity=".9"/>']
    return svg(w, H, "".join(b), "", label)


# ------------------------------------------------------------------ footer
def _pagoda(cx, base, s=1.0):
    g = [f'<g transform="translate({cx} {base}) scale({s})" fill="{INK}" stroke="{CREAM}" stroke-opacity=".62" stroke-width="1" stroke-linejoin="round">',
         '<rect x="-48" y="-7" width="96" height="7"/><rect x="-40" y="-14" width="80" height="7"/>']
    y = -14
    for i in range(5):
        hw, bw = 36 - 4.5 * i, (36 - 4.5 * i) * .6
        g.append(f'<rect x="{-bw:.1f}" y="{y - 15}" width="{2 * bw:.1f}" height="15"/>')
        y -= 15
        g.append(f'<path d="M{-hw - 9:.1f} {y - 5}Q{-hw + 2:.1f} {y} {-hw + 10:.1f} {y}H{hw - 10:.1f}Q{hw - 2:.1f} {y} {hw + 9:.1f} {y - 5}Q{hw - 6:.1f} {y - 7} {hw - 14:.1f} {y - 14}H{-hw + 14:.1f}Q{-hw + 6:.1f} {y - 7} {-hw - 9:.1f} {y - 5}Z"/>')
        y -= 14
    g.append(f'<path d="M0 {y}V{y - 34}" fill="none"/><path d="M-5 {y - 10}H5M-4 {y - 18}H4M-3 {y - 26}H3" fill="none"/></g>')
    return "".join(g)


def _tower(cx, base, s=1.0):
    half = lambda y: 36 - 30 * (-y) / 132
    g = [f'<g transform="translate({cx} {base}) scale({s})" fill="none" stroke="{CREAM}" stroke-opacity=".62" stroke-width="1" stroke-linejoin="round"><path d="M-36 0L-6 -132M36 0L6 -132"/>']
    lv = [0, -26, -52, -80, -108, -132]
    for a, c in zip(lv, lv[1:]):
        g.append(f'<path d="M{-half(a):.1f} {a}L{half(c):.1f} {c}M{half(a):.1f} {a}L{-half(c):.1f} {c}M{-half(c):.1f} {c}H{half(c):.1f}" stroke-opacity=".35"/>')
    g.append(f'<rect x="{-half(-56) - 6:.1f}" y="-60" width="{2 * half(-56) + 12:.1f}" height="7" fill="{INK}"/><rect x="{-half(-104) - 4:.1f}" y="-107" width="{2 * half(-104) + 8:.1f}" height="5" fill="{INK}"/><path d="M0 -132V-196"/></g>')
    return "".join(g)


def footer():
    W, H = 900, 330
    HZ = 186
    rng = random.Random(2)
    N = 8
    yf = lambda i: HZ + (H - HZ + 30) * (i / N) ** 2.0
    defs = (f'<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CREAM}"/><stop offset=".5" stop-color="{PINK}"/><stop offset="1" stop-color="{LILAC}"/></linearGradient>'
            f'<mask id="stripes"><rect width="{W}" height="{H}" fill="#fff"/>'
            + "".join(f'<rect x="0" y="{HZ - 58 + k * 10 + k * k * .5:.1f}" width="{W}" height="{1 + k * .55:.1f}" fill="#000"/>' for k in range(1, 8))
            + f'</mask><clipPath id="above"><rect width="{W}" height="{HZ}"/></clipPath>'
            f'<radialGradient id="scrim"><stop offset="0" stop-color="{INK}" stop-opacity=".9"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient>')
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>',
         aurora([(220, 120, 260, 100, TEAL, .08, 20, 28), (680, 110, 280, 100, PINK, .08, 24, 30)]),
         stars(rng, 40, W, HZ - 60),
         f'<circle cx="450" cy="{HZ - 14}" r="200" fill="url(#halo)"/>',
         f'<g clip-path="url(#above)" mask="url(#stripes)"><circle cx="450" cy="{HZ - 10}" r="66" fill="url(#sun)" fill-opacity=".95"/></g>']
    x, wins = -10, []
    while x < W + 10:
        w = rng.uniform(24, 50)
        h = rng.uniform(20, 78) * (.3 + .95 * abs(x + w / 2 - 450) / 450) + 10
        b.append(f'<rect x="{x:.0f}" y="{HZ - h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{INK}" fill-opacity=".96" stroke="{CREAM}" stroke-opacity=".34" stroke-width=".8"/>')
        for wy in range(int(HZ - h + 8), HZ - 4, 8):
            for wx in range(int(x + 5), int(x + w - 4), 7):
                if rng.random() < .26:
                    wins.append(f"M{wx} {wy}h2v2h-2Z")
        x += w + rng.uniform(0, 4)
    b.append(f'<path d="{"".join(wins)}" fill="{CREAM}" fill-opacity=".4"/>')
    b += [_pagoda(150, HZ, .8), _tower(748, HZ, .86)]
    b.append(f'<circle cx="150" cy="{HZ - 188 * .8 + 4:.0f}" r="2.2" fill="{PINK}"><animate attributeName="opacity" values="1;.25;1" dur="3.2s" repeatCount="indefinite"/></circle>')
    b.append(f'<circle cx="748" cy="{HZ - 199 * .86:.0f}" r="2.4" fill="{PINK}"><animate attributeName="opacity" values="1;.25;1" dur="2.6s" repeatCount="indefinite"/></circle>')
    b.append(f'<path d="{"".join(f"M450 {HZ}L{450 + j * 112} {H + 30}" for j in range(-12, 13))}" stroke="{CREAM}" stroke-opacity=".26" stroke-width=".8" fill="none"/>')
    for i in range(1, N + 1):
        b.append(f'<rect x="0" y="{yf(i):.1f}" width="{W}" height="1" fill="{CREAM}" fill-opacity="{.08 + .4 * i / N:.2f}"/>')
    b.append(hline(0, W, HZ, .55))
    b += [f'<ellipse cx="450" cy="268" rx="400" ry="70" fill="url(#scrim)"/><ellipse cx="450" cy="268" rx="300" ry="50" fill="url(#scrim)"/>',
          T("jp", "ご訪問ありがとうございます", 25, 450, 252, "middle", 10, .98),
          T("j3", "THANK YOU FOR VISITING", 13, 450, 280, "middle", 12, .85),
          T("mono", "© 2026 ARYAN RANAVAT  ·  DA-IICT", 11.5, 450, 304, "middle", 4, .65),
          ticks(12, 12, W - 24, H - 24, 14, .5)]
    return svg(W, H, "".join(b), defs, "Thank you for visiting.")
