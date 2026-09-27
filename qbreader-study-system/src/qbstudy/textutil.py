"""Deterministic text helpers: HTML stripping, normalization, stemming,
clue-sentence splitting, and answerline parsing. No AI involved."""
from __future__ import annotations

import hashlib
import html
import json
import re
import unicodedata
from dataclasses import dataclass, field

STOPWORDS = frozenset("""
a about above after again against all also although am an and any are as at be
because been before being below between both but by can could did do does doing
down during each either few for from further had has have having he her here hers
herself him himself his how i if in into is it its itself just many may me might
more most much must my myself neither no nor not now of off on once one only or
other our ours ourselves out over own same she should so some such than that the
their theirs them themselves then there these they this those through to too under
until up upon very was we were what when where which while who whom whose why will
with within without would yet you your yours yourself yourselves
""".split())

# Quizbowl boilerplate that says nothing about the subject.
QB_BOILERPLATE = frozenset("""
points point name identify give ftp ten fifteen twenty title man woman person
figure thing entity work works author country city
""".split())

HEDGE_WORDS = ("may ", "might ", "possibly", "probably", "suggest", "suggests", "suggested",
               "appears to", "appear to", "likely", "reportedly", "allegedly", "is thought",
               "are thought", "is believed", "hypothes", "uncertain", "unclear", "disputed",
               "controversial", "preliminary", "in mice", "in vitro", "could ")

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_NON_WORD_RE = re.compile(r"[^0-9a-z]+")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def strip_html(text: str | None) -> str:
    if not text:
        return ""
    return _WS_RE.sub(" ", html.unescape(_TAG_RE.sub("", text))).strip()


def fold_diacritics(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def normalize(text: str | None) -> str:
    """Lowercase, remove diacritics and punctuation, collapse whitespace."""
    if not text:
        return ""
    t = fold_diacritics(text).lower().replace("’", "'").replace("'s ", " ")
    t = _NON_WORD_RE.sub(" ", t)
    return _WS_RE.sub(" ", t).strip()


def normalize_ws(text: str | None) -> str:
    """Whitespace/quote normalization only (used for verbatim grounding checks)."""
    if not text:
        return ""
    t = fold_diacritics(text)
    t = (t.replace("‘", "'").replace("’", "'").replace("“", '"')
         .replace("”", '"').replace("—", "-").replace("–", "-"))
    return _WS_RE.sub(" ", t).strip().lower()


def stem(word: str) -> str:
    """Tiny suffix stripper; consistent rather than linguistically perfect."""
    w = word
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 4 and w.endswith("sses"):
        return w[:-2]
    for suffix, minlen in (("ing", 6), ("ed", 5), ("ly", 5), ("es", 5), ("s", 4)):
        if len(w) >= minlen and w.endswith(suffix) and not w.endswith("ss"):
            return w[: -len(suffix)]
    return w


def tokens(text: str | None) -> list[str]:
    return normalize(text).split()


def content_stems(text: str | None, extra_stop: set[str] | None = None) -> list[str]:
    """Stemmed content words (stopwords and quizbowl boilerplate removed)."""
    out = []
    stop = STOPWORDS | QB_BOILERPLATE | (extra_stop or set())
    for tok in tokens(text):
        if tok in stop or (len(tok) < 3 and not tok.isdigit()):
            continue
        out.append(stem(tok))
    return out


def bigrams(seq: list[str]) -> set[tuple[str, str]]:
    return {(seq[i], seq[i + 1]) for i in range(len(seq) - 1)}


def detect_hedges(text: str) -> list[str]:
    low = " " + normalize_ws(text) + " "
    return sorted({h.strip() for h in HEDGE_WORDS if h in low})


# ------------------------------------------------------------ sentence split
_ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "st", "mt", "ft", "jr", "sr", "vs", "etc", "no", "vol", "ch",
    "fig", "gen", "col", "lt", "sgt", "capt", "gov", "sen", "rep", "rev", "prof", "ca", "c",
    "approx", "dept", "inc", "ltd", "co", "corp", "e.g", "i.e", "u.s", "u.k", "a.d", "b.c",
    "op", "pp", "p", "ed", "eds", "trans", "al", "jan", "feb", "mar", "apr", "aug", "sept",
    "sep", "oct", "nov", "dec",
}
_SENT_END_RE = re.compile(r'([.!?]["”\')\]]*)\s+(?=["“(\[]?[A-Z0-9])')
GIVEAWAY_RE = re.compile(r"\b(for (10|ten|15|fifteen|20|twenty) points|ftp)\b", re.IGNORECASE)


def split_sentences(text: str) -> list[str]:
    """Split quizbowl text into clue sentences, protecting common
    abbreviations and single-letter initials (e.g. "J. P. Morgan")."""
    text = _WS_RE.sub(" ", text or "").strip()
    if not text:
        return []
    pieces: list[str] = []
    start = 0
    for m in _SENT_END_RE.finditer(text):
        end = m.end(1)
        candidate = text[start:end]
        last_word = re.search(r"([A-Za-z.]+)[.!?][\"”')\]]*$", candidate)
        if last_word:
            lw = last_word.group(1).lower().rstrip(".")
            if lw in _ABBREVIATIONS or (len(lw) == 1 and lw.isalpha()):
                continue
        pieces.append(candidate.strip())
        start = m.end()
    tail = text[start:].strip()
    if tail:
        pieces.append(tail)
    return [p for p in pieces if p]


def is_giveaway(sentence: str) -> bool:
    return bool(GIVEAWAY_RE.search(sentence))


# ---------------------------------------------------------- answerline parse
@dataclass
class Answerline:
    main: str
    alternates: list[str] = field(default_factory=list)
    prompts: list[str] = field(default_factory=list)
    rejects: list[str] = field(default_factory=list)

    @property
    def all_accepted(self) -> list[str]:
        seen, out = set(), []
        for a in [self.main, *self.alternates]:
            n = normalize(a)
            if n and n not in seen:
                seen.add(n)
                out.append(a)
        return out


_BRACKET_RE = re.compile(r"[\[(](.*?)[\])]")
_CLAUSE_SPLIT_RE = re.compile(r"\s*;\s*")
_OR_SPLIT_RE = re.compile(r"\s*,?\s+\bor\b\s+|\s*,\s*")


def _clean_alt(s: str) -> str:
    s = re.sub(r"\b(accept|also accept|or|until|before|after)\b.*?:\s*", "", s, flags=re.I)
    s = re.sub(r"^\s*(or|accept|also accept|anything that mentions|word forms of)\b\s*", "", s, flags=re.I)
    s = s.strip(" .,:;\"'")
    return s


def parse_answerline(answer: str | None) -> Answerline:
    """Parse a QBReader answerline such as
    'Jay Gould [or Jason Gould; prompt on Gould; do not accept "Fisk"]'."""
    text = strip_html(answer)
    if not text:
        return Answerline(main="")
    main = _BRACKET_RE.split(text)[0].strip(" .,;:")
    line = Answerline(main=main or text)
    for inner in _BRACKET_RE.findall(text):
        for clause in _CLAUSE_SPLIT_RE.split(inner):
            c = clause.strip()
            low = c.lower()
            if not c:
                continue
            if low.startswith(("do not accept", "don't accept", "reject", "do not prompt",
                               "antiprompt", "anti-prompt")):
                target = line.rejects
                c = re.sub(r"^(do not accept|don't accept|reject|do not prompt on|antiprompt on|"
                           r"anti-prompt on)\b( or prompt on)?\s*", "", c, flags=re.I)
            elif low.startswith("prompt"):
                target = line.prompts
                c = re.sub(r"^prompt on\s*", "", c, flags=re.I)
            elif low.startswith(("or ", "accept", "also accept")) or target_is_plain(low):
                target = line.alternates
            else:
                continue
            for alt in _OR_SPLIT_RE.split(c):
                alt = _clean_alt(alt)
                if alt and len(alt) < 120:
                    target.append(alt)
    return line


def target_is_plain(low: str) -> bool:
    # e.g. "[Jason Gould]" with no leading keyword: treat as an alternate name
    return not re.match(r"^(prompt|do not|don't|reject|antiprompt|anti-prompt|note|until|after|"
                        r"before|if|when|since|moderator|read)\b", low)
