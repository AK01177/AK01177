"""
Subset Zen Kaku Gothic New (Japanese) to just the characters used in these scripts.

  python scripts/make_fonts.py

Run it again after adding new Japanese text to any script. The full fonts are
downloaded once into scripts/fonts_src (not committed) from the Google Fonts repo.
"""
import os
import urllib.request

from fontTools import subset

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(HERE, "fonts_src"), os.path.join(HERE, "fonts")
BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/zenkakugothicnew/"
WEIGHTS = {"Light": "ZenKakuGothicNew-Light", "Medium": "ZenKakuGothicNew-Medium"}


def used_chars():
    chars = set()
    for name in os.listdir(HERE):
        if name.endswith(".py"):
            with open(os.path.join(HERE, name), encoding="utf-8") as f:
                chars |= {c for c in f.read() if ord(c) >= 0x3000}
    chars |= {chr(i) for i in range(32, 127)} | set("…·—°©")
    return sorted(chars)


def main():
    os.makedirs(SRC, exist_ok=True)
    chars = used_chars()
    print(f"{len(chars)} characters")
    for _, stem in WEIGHTS.items():
        src = os.path.join(SRC, stem + ".ttf")
        if not os.path.exists(src):
            urllib.request.urlretrieve(BASE + stem + ".ttf", src)
        opts = subset.Options()
        opts.layout_features = []
        opts.notdef_outline = True
        opts.name_IDs = [1, 2]
        font = subset.load_font(src, opts)
        sub = subset.Subsetter(opts)
        sub.populate(text="".join(chars))
        sub.subset(font)
        out = os.path.join(OUT, stem + ".subset.ttf")
        subset.save_font(font, out, opts)
        print(out, round(os.path.getsize(out) / 1024, 1), "KB")


if __name__ == "__main__":
    main()
