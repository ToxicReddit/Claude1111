"""Curated film catalog for the watch guide.

Each niche is registered with N(category, subcategory, niche, sources, note, films).
`films` is a block of lines, one film per line, in recommended viewing order:

    *Title | Year | Director     -> Tier 1 "Start Here"
     Title | Year | Director     -> Tier 2 "Core"
    +Title | Year | Director     -> Tier 3 "Deep Cut"

A film may appear in any number of niches; the builder de-duplicates it into
one Master row while keeping every bucket it belongs to.
"""

NICHES = []


def N(category, subcategory, niche, sources, note, films):
    rows = []
    for raw in films.strip().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        tier = 2
        if line[0] == "*":
            tier, line = 1, line[1:].strip()
        elif line[0] == "+":
            tier, line = 3, line[1:].strip()
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 3:
            raise ValueError(f"Bad film line in {niche!r}: {raw!r}")
        title, year, director = parts
        rows.append((title, int(year), director, tier))
    NICHES.append(dict(category=category, subcategory=subcategory, niche=niche,
                       sources=sources, note=note, films=rows))


from . import c01_foundations, c02_history, c03_world, c04_genres  # noqa: E402,F401
from . import c05_auteurs, c06_theory, c07_themes, c08_niches  # noqa: E402,F401
from . import c09_canons, c10_bridges  # noqa: E402,F401
