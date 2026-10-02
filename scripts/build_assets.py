"""Regenerate every SVG in ../assets  (python scripts/build_assets.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dynamic_assets as dyn
import static_assets as st

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{name:24s}{len(content) / 1024:7.1f} KB")


if __name__ == "__main__":
    write("header.svg", st.header())
    write("divider.svg", st.divider())
    for slug, idx, en, jp in [("about", "01", "About", "自己紹介"), ("stack", "02", "Stack", "技術"),
                              ("projects", "03", "Projects", "作品"), ("achievements", "04", "Achievements", "実績"),
                              ("stats", "05", "Stats", "統計"), ("contact", "06", "Contact", "連絡")]:
        write(f"h-{slug}.svg", st.section_header(idx, en, jp))
    write("about.svg", st.about())
    write("stack.svg", st.stack())
    write("project-godiglobe.svg", st.quest_godiglobe())
    write("project-aicalc.svg", st.quest_aicalc())
    write("project-argus.svg", st.quest_argus())
    write("achievements.svg", st.feats())
    write("btn-repo.svg", st.button("REPOSITORY", "リポジトリ", "github", 250))
    write("btn-demo.svg", st.button("LIVE DEMO", "デモを見る", "play", 250))
    write("btn-email.svg", st.button("EMAIL", "メールを送る", "mail", 270))
    write("btn-linkedin.svg", st.button("LINKEDIN", "つながる", "in", 270))
    write("btn-github.svg", st.button("GITHUB", "コードを見る", "github", 270))
    write("footer.svg", st.footer())
    # living files: only seeded when missing (the workflow owns them afterwards)
    seed = {"total": 738, "cur": 7, "cur_range": "SEP 23 – SEP 29", "longest": 7,
            "longest_range": "JUN 14 – JUN 20, 2025", "since_label": "SINCE DEC 2024"}
    for name, fn, data in [("ledger-stats.svg", dyn.stats, seed), ("ledger-langs.svg", dyn.langs, {}), ("ledger-activity.svg", dyn.heatmap, {}), ("ledger-recent.svg", dyn.recent, {})]:
        if not os.path.exists(os.path.join(OUT, name)):
            write(name, fn(data))
