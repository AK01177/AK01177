"""
aes.py - toolkit for the minimal, futuristic, Japanese-typographic SVG theme.

All lettering is converted to vector outlines (fontTools), so nothing depends on
fonts installed on the viewer's device. Fonts live in scripts/fonts (SIL OFL):
Jost, JetBrains Mono, and a subset of Zen Kaku Gothic New for the Japanese text.
"""
import base64
import json
import math
import os
import random

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))

FONT_FILES = {
    "j2": "jost-latin-200-normal.woff",       # ultra-light display
    "j3": "jost-latin-300-normal.woff",
    "j4": "jost-latin-400-normal.woff",       # body
    "mono": "jetbrains-mono-latin-400-normal.woff",
    "jp": "ZenKakuGothicNew-Light.subset.ttf",
    "jpm": "ZenKakuGothicNew-Medium.subset.ttf",
}
FALLBACK = {"j2": ["jp"], "j3": ["jp"], "j4": ["jpm"], "mono": ["jp"], "jp": [], "jpm": []}
_FONTS = {}


def _font(key):
    if key not in _FONTS:
        f = TTFont(os.path.join(HERE, "fonts", FONT_FILES[key]))
        _FONTS[key] = (f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm)
    return _FONTS[key]


def _n(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def _lookup(fk, ch):
    for k in [fk] + FALLBACK[fk]:
        gs, cm, upm = _font(k)
        g = cm.get(ord(ch))
        if g:
            return k, g
    gs, cm, upm = _font(fk)
    return fk, cm.get(32) or next(iter(gs.keys()))


def width(fk, text, size, ls=0.0):
    if not text:
        return 0.0
    w = 0.0
    for c in text:
        k, g = _lookup(fk, c)
        gs, _, upm = _font(k)
        w += gs[g].width * size / upm + ls
    return w - ls


_REG = {}


def _flat(fill):
    return not fill.startswith("url(")


def txt(fk, text, size, x, y, fill, anchor="start", ls=0.0, extra=""):
    """Lettering as vectors; y is the baseline. Flat colours share glyph outlines via <use>."""
    w = width(fk, text, size, ls)
    cx = x - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
    if _flat(fill):
        uses = []
        for ch in text:
            k, g = _lookup(fk, ch)
            gs, _, upm = _font(k)
            s = size / upm
            gid = f"{k}{ord(ch):x}"
            if gid not in _REG:
                p = SVGPathPen(gs, ntos=lambda v: str(int(round(v))))
                gs[g].draw(p)
                _REG[gid] = p.getCommands()
            if _REG[gid]:
                uses.append(f'<use href="#{gid}" transform="translate({_n(cx)} {_n(y)}) scale({s:.4f} {-s:.4f})"/>')
            cx += gs[g].width * s + ls
        return f'<g fill="{fill}" {extra}>{"".join(uses)}</g>' if uses else ""
    pen = SVGPathPen(_font(fk)[0], ntos=_n)
    for ch in text:
        k, g = _lookup(fk, ch)
        gs, _, upm = _font(k)
        s = size / upm
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        cx += gs[g].width * s + ls
    d = pen.getCommands()
    return f'<path d="{d}" fill="{fill}" {extra}/>' if d else ""


def vtxt(fk, text, size, x, y, fill, step=1.4, extra=""):
    """Japanese-style vertical writing: one character per row, centred on x."""
    return "".join(txt(fk, ch, size, x, y + i * size * step, fill, "middle", 0, extra) for i, ch in enumerate(text))


def rtxt(fk, text, size, x, y, fill, angle=90, anchor="start", ls=0.0, extra=""):
    return f'<g transform="rotate({angle} {x} {y})">{txt(fk, text, size, x, y, fill, anchor, ls, extra)}</g>'


def wrap(fk, text, size, maxw, ls=0.0):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if cur and width(fk, trial, size, ls) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def para(fk, text, size, x, y, maxw, lh, fill, anchor="start", ls=0.0):
    lines = wrap(fk, text, size, maxw, ls)
    return "".join(txt(fk, ln, size, x, y + i * lh, fill, anchor, ls) for i, ln in enumerate(lines)), len(lines)


def fit(fk, text, size, maxw, ls=0.0):
    w = width(fk, text, size, ls)
    return size if w <= maxw else size * maxw / w


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


ICONS = json.load(open(os.path.join(HERE, "icons.json")))

# ------------------------------------------------------------------ palette
INK = "#06080e"
PANEL = "#0a0d14"
CREAM = "#fbf0c8"
TEAL = "#9fe6dc"
LILAC = "#b9b3f5"
PINK = "#f5c0dc"
CHAR = "#2f2c2b"     # warm charcoal from the portrait

COMMON = f"""
<linearGradient id="holo" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="520" y2="0" spreadMethod="repeat">
  <stop offset="0" stop-color="{CREAM}"/><stop offset=".25" stop-color="{TEAL}"/><stop offset=".5" stop-color="{LILAC}"/>
  <stop offset=".75" stop-color="{PINK}"/><stop offset="1" stop-color="{CREAM}"/>
  <animate attributeName="x1" values="0;520" dur="11s" repeatCount="indefinite"/>
  <animate attributeName="x2" values="520;1040" dur="11s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="trav" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{TEAL}" stop-opacity="0"/><stop offset=".55" stop-color="{CREAM}"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="fadeR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CREAM}" stop-opacity=".5"/><stop offset="1" stop-color="{CREAM}" stop-opacity="0"/></linearGradient>
<linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CREAM}" stop-opacity="0"/><stop offset="1" stop-color="{CREAM}" stop-opacity=".5"/></linearGradient>
<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CREAM}" stop-opacity="0"/><stop offset=".5" stop-color="{CREAM}" stop-opacity=".09"/><stop offset="1" stop-color="{CREAM}" stop-opacity="0"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="{CREAM}" stop-opacity=".16"/><stop offset="1" stop-color="{CREAM}" stop-opacity="0"/></radialGradient>
<radialGradient id="aurT"><stop offset="0" stop-color="#9fe6dc"/><stop offset=".5" stop-color="#9fe6dc" stop-opacity=".45"/><stop offset="1" stop-color="#9fe6dc" stop-opacity="0"/></radialGradient>
<radialGradient id="aurP"><stop offset="0" stop-color="#f5c0dc"/><stop offset=".5" stop-color="#f5c0dc" stop-opacity=".45"/><stop offset="1" stop-color="#f5c0dc" stop-opacity="0"/></radialGradient>
<radialGradient id="aurL"><stop offset="0" stop-color="#b9b3f5"/><stop offset=".5" stop-color="#b9b3f5" stop-opacity=".45"/><stop offset="1" stop-color="#b9b3f5" stop-opacity="0"/></radialGradient>
<filter id="b24" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="24"/></filter>
<filter id="b40" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="40"/></filter>
<linearGradient id="bgpanel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1017"/><stop offset="1" stop-color="#080a10"/></linearGradient>
"""


def svg(w, h, body, defs="", title=""):
    glyphs = "".join(f'<path id="{i}" d="{d}"/>' for i, d in _REG.items())
    _REG.clear()
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
        f"<defs>{COMMON}{defs}{glyphs}</defs>{body}</svg>"
    )


# --------------------------------------------------------------- primitives
def hline(x1, x2, y, op=.22, col=CREAM, h=1):
    return f'<rect x="{x1}" y="{_n(y - h / 2)}" width="{_n(x2 - x1)}" height="{h}" fill="{col}" fill-opacity="{op}"/>'


def vline(x, y1, y2, op=.22, col=CREAM, w=1):
    return f'<rect x="{_n(x - w / 2)}" y="{y1}" width="{w}" height="{_n(y2 - y1)}" fill="{col}" fill-opacity="{op}"/>'


def ticks(x, y, w, h, l=10, op=.75, col=CREAM, sw=1):
    return (f'<path d="M{x} {y + l}V{y}H{x + l}M{x + w - l} {y}H{x + w}V{y + l}M{x + w} {y + h - l}V{y + h}H{x + w - l}M{x + l} {y + h}H{x}V{y + h - l}" '
            f'fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{sw}"/>')


def frame(w, h, r=0, op=.16):
    return f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{r}" fill="url(#bgpanel)" stroke="{CREAM}" stroke-opacity="{op}"/>'


def plus(cx, cy, s=4, op=.6):
    return f'<path d="M{cx - s} {cy}H{cx + s}M{cx} {cy - s}V{cy + s}" stroke="{CREAM}" stroke-opacity="{op}" stroke-width="1" fill="none"/>'


def blink_dot(cx, cy, r=3, col=TEAL, dur=1.8):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"><animate attributeName="opacity" values="1;.2;1" dur="{dur}s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-opacity=".6"><animate attributeName="r" values="{r};{r * 3.2:.1f}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values=".6;0" dur="{dur}s" repeatCount="indefinite"/></circle>')


def traveler(x0, x1, y, w=140, dur=5.0, begin=0.0, h=1.4):
    return (f'<rect x="{x0 - w}" y="{_n(y - h / 2)}" width="{w}" height="{h}" fill="url(#trav)">'
            f'<animate attributeName="x" values="{x0 - w};{x1}" dur="{dur}s" begin="-{begin:.1f}s" repeatCount="indefinite"/></rect>')


def scan(w, h, dur=9.0, band=90, op=1):
    return (f'<rect width="{w}" height="{band}" fill="url(#scanG)" opacity="{op}">'
            f'<animate attributeName="y" values="{-band};{h}" dur="{dur}s" repeatCount="indefinite"/></rect>')


def tunnel(ow, oh, iw, ih, n=7, m=6, cx=0, cy=0):
    """Wireframe box seen from inside (the grid cube from the portrait) as one path."""
    d = []
    for k in range(n + 1):
        t = k / n
        w, h = ow * (iw / ow) ** t, oh * (ih / oh) ** t
        d.append(f"M{_n(cx - w / 2)} {_n(cy - h / 2)}H{_n(cx + w / 2)}V{_n(cy + h / 2)}H{_n(cx - w / 2)}Z")
    for i in range(m + 1):
        f = i / m
        for (ax, ay, bx, by, cx2, cy2, dx, dy) in (
            (-ow / 2, -oh / 2, ow / 2, -oh / 2, -iw / 2, -ih / 2, iw / 2, -ih / 2),   # top
            (-ow / 2, oh / 2, ow / 2, oh / 2, -iw / 2, ih / 2, iw / 2, ih / 2),       # bottom
            (-ow / 2, -oh / 2, -ow / 2, oh / 2, -iw / 2, -ih / 2, -iw / 2, ih / 2),   # left
            (ow / 2, -oh / 2, ow / 2, oh / 2, iw / 2, -ih / 2, iw / 2, ih / 2),       # right
        ):
            d.append(f"M{_n(cx + ax + (bx - ax) * f)} {_n(cy + ay + (by - ay) * f)}L{_n(cx + cx2 + (dx - cx2) * f)} {_n(cy + cy2 + (dy - cy2) * f)}")
    return "".join(d)


def cube(cx, cy, s, op=.7, dur=8):
    o = s * .34
    d = (f"M{cx - s / 2} {cy - s / 2}h{s}v{s}h{-s}Z"
         f"M{cx - s / 2 + o} {cy - s / 2 - o}h{s}v{s}h{-s}Z"
         f"M{cx - s / 2} {cy - s / 2}l{o} {-o}M{cx + s / 2} {cy - s / 2}l{o} {-o}"
         f"M{cx + s / 2} {cy + s / 2}l{o} {-o}M{cx - s / 2} {cy + s / 2}l{o} {-o}")
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="{dur}s" repeatCount="indefinite" '
            f'calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
            f'<path d="{d}" fill="none" stroke="url(#holo)" stroke-width="1.2" stroke-linejoin="round" stroke-opacity="{op}"/></g>')


def barcode(seed, x, y, w, h, op=.55):
    rng = random.Random(seed)
    cur, out = x, []
    while cur < x + w - 3:
        bw = rng.choice([1, 1, 2, 3])
        out.append(f"M{cur} {y}h{bw}v{h}h{-bw}Z")
        cur += bw + rng.choice([2, 3, 3, 5])
    return f'<path d="{"".join(out)}" fill="{CREAM}" fill-opacity="{op}"/>'


def dust(rng, n, w, h, y0=0):
    out = []
    for _ in range(n):
        x, y = rng.uniform(0, w), rng.uniform(y0, h)
        dur, b = rng.uniform(9, 20), rng.uniform(0, 15)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rng.uniform(.6, 1.5):.1f}" fill="{CREAM}" opacity="0">'
                   f'<animate attributeName="cy" values="{y:.0f};{y - rng.uniform(40, 110):.0f}" dur="{dur:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="0;.55;0" dur="{dur:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def icon(name, cx, cy, size, fill=CREAM, op=1):
    d = ICONS.get(name)
    if not d:
        return ""
    s = size / 24
    return f'<path transform="translate({_n(cx - size / 2)} {_n(cy - size / 2)}) scale({s:.3f})" d="{d}" fill="{fill}" fill-opacity="{op}"/>'


def data_uri(path, mime="image/png"):
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


# ------------------------------------------------------- graphic extras
KANA = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン未来開発設計学習創造光"


def pathd(fk, text, size, x, y, anchor="start", ls=0.0):
    w = width(fk, text, size, ls)
    cx = x - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
    pen = SVGPathPen(_font(fk)[0], ntos=_n)
    for ch in text:
        k, g = _lookup(fk, ch)
        gs, _, upm = _font(k)
        s = size / upm
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        cx += gs[g].width * s + ls
    return pen.getCommands()


def otxt(fk, text, size, x, y, stroke, anchor="start", ls=0.0, sw=1.0, op=1.0, extra=""):
    """Outlined (hollow) lettering."""
    d = pathd(fk, text, size, x, y, anchor, ls)
    return (f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-opacity="{op}" stroke-linejoin="round" {extra}/>' if d else "")


def glitch(gid, fk, text, size, x, y, anchor="start", ls=0.0, period=7.0, begin=0.0, fill=CREAM, spread=3.6):
    """Cream lettering with a rare teal/pink chromatic-aberration burst."""
    d = pathd(fk, text, size, x, y, anchor, ls)
    kt = "0;.9;.915;.93;.945;.96;1"
    out = [f'<path id="{gid}" d="{d}" fill="{fill}"/>']
    for col, dx, dy in ((TEAL, -spread, .8), (PINK, spread, -.8)):
        out.append(
            f'<use href="#{gid}" fill="{col}" opacity="0" style="mix-blend-mode:screen">'
            f'<animate attributeName="opacity" values="0;0;.9;0;.6;0;0" keyTimes="{kt}" dur="{period}s" begin="-{begin}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;{dx} {dy};{-dx * .5} 0;{dx * .7} {dy};0 0;0 0" keyTimes="{kt}" dur="{period}s" begin="-{begin}s" repeatCount="indefinite"/></use>')
    return "".join(out)


def aurora(blobs):
    """Soft, slowly drifting holographic colour fields. blobs: (cx, cy, rx, ry, colour, opacity, drift, seconds)."""
    return "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{ {TEAL: 'aurT', PINK: 'aurP', LILAC: 'aurL'}[col] })" opacity="{min(1, op * 1.7):.2f}">'
        f'<animateTransform attributeName="transform" type="translate" values="{-dr} 0;{dr} {dr * .4:.0f};{-dr} 0" dur="{dur}s" repeatCount="indefinite" '
        f'calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/></ellipse>'
        for cx, cy, rx, ry, col, op, dr, dur in blobs)


def kana_rain(rng, xs, h, size=15, n=12, op=.15):
    """Slow columns of falling katakana / kanji, set vertically like tategaki."""
    step, out = 1.45, []
    for x in xs:
        s = "".join(rng.choice(KANA) for _ in range(n))
        dur, b = rng.uniform(18, 34), rng.uniform(0, 34)
        total = n * size * step
        col = vtxt("jp", s[:-1], size, 0, 0, CREAM, step, f'fill-opacity="{op}"')
        head = txt("jp", s[-1], size, 0, (n - 1) * size * step, TEAL, "middle", 0, 'fill-opacity=".6"')
        out.append(f'<g transform="translate({x} 0)"><g><animateTransform attributeName="transform" type="translate" values="0 {-total:.0f};0 {h + 20}" dur="{dur:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/>{col}{head}</g></g>')
    return "".join(out)


def arc(cx, cy, r, a0, a1):
    p = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    (x0, y0), (x1, y1) = p(a0), p(a1)
    return f"M{_n(x0)} {_n(y0)}A{r} {r} 0 {1 if (a1 - a0) % 360 > 180 else 0} 1 {_n(x1)} {_n(y1)}"


def equalizer(x, y, n=12, h=34, bw=3, gap=4, seed=3):
    rng = random.Random(seed)
    out = []
    for i in range(n):
        vals = ";".join(f"1 {rng.uniform(.12, 1):.2f}" for _ in range(6))
        vals += ";" + vals.split(";")[0]
        out.append(f'<g transform="translate({x + i * (bw + gap)} {y})"><rect x="0" y="{-h}" width="{bw}" height="{h}" fill="{CREAM}" fill-opacity=".7">'
                   f'<animateTransform attributeName="transform" type="scale" values="{vals}" dur="{rng.uniform(2.2, 4.4):.1f}s" repeatCount="indefinite"/></rect></g>')
    return "".join(out)


def stars(rng, n, w, h, y0=0):
    out = []
    for _ in range(n):
        x, y = rng.uniform(0, w), rng.uniform(y0, h)
        o, dur, b = rng.uniform(.25, .8), rng.uniform(2.5, 7), rng.uniform(0, 6)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rng.choice([.5, .7, .9, 1.2]):.1f}" fill="{CREAM}" opacity="{o:.2f}">'
                   f'<animate attributeName="opacity" values="{o:.2f};{o * .15:.2f};{o:.2f}" dur="{dur:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)
