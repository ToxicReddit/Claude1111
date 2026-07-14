"""Shared helper for building Anki tab-separated import files.

Each unit script builds a list of Card tuples and calls write_tsv() to emit
a .txt file into outputs/. Anki's tab-separated importer splits strictly on
the tab character, so the only hard requirement is that no field contains a
literal tab or newline. We convert internal newlines to <br> and strip any
stray tabs defensively.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class Card:
    front: str
    back: str
    tags: str  # space-separated tag string, e.g. "chem102::atomic_structure concept"


def _clean(field: str) -> str:
    field = field.replace("\t", "    ")
    field = field.replace("\r\n", "\n").replace("\r", "\n")
    field = field.replace("\n", "<br>")
    return field.strip()


def write_tsv(cards: List[Card], filepath: str, header: bool = True) -> int:
    lines = []
    if header:
        lines.append("#separator:tab")
        lines.append("#html:true")
        lines.append("#tags column:3")
    for c in cards:
        front = _clean(c.front)
        back = _clean(c.back)
        tags = c.tags.strip()
        lines.append(f"{front}\t{back}\t{tags}")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(cards)


def summarize(cards: List[Card]):
    concept = sum(1 for c in cards if "concept" in c.tags.split())
    applied = sum(1 for c in cards if "applied" in c.tags.split())
    return {"total": len(cards), "concept": concept, "applied": applied}
