import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import Card, write_tsv, summarize

TAG_COURSE = "chem102"
UNIT = "periodic_trends"
cards = []

def add(front, back, sub, kind):
    cards.append(Card(front, back, f"{TAG_COURSE} {UNIT}::{sub} {kind}"))

# ---------- CONCEPT ----------
add("Define effective nuclear charge (Z_eff).",
    "The net positive charge experienced by an electron in an atom, after accounting for the shielding (repulsion) of other electrons between it and the nucleus. Approximately Z_eff = Z - S, where Z is the actual nuclear charge and S is the shielding constant from inner/core electrons.",
    "effective_nuclear_charge", "concept")

add("How does effective nuclear charge change across a period (left to right) and why?",
    "Z_eff increases across a period. Each step right adds a proton (increasing Z) and an electron to the same outer shell; electrons in the same shell shield each other poorly, so the shielding barely increases while nuclear charge does — the net pull on outer electrons grows.",
    "effective_nuclear_charge", "concept")

add("Define atomic radius and describe its trend across a period and down a group.",
    "Atomic radius is (roughly) half the distance between nuclei of two bonded/touching identical atoms. It decreases across a period (left to right) due to increasing Z_eff pulling electrons in closer. It increases down a group because each row adds a new outer shell (higher n), which is farther from the nucleus and outweighs the increased nuclear charge.",
    "atomic_radius", "concept")

add("Why does atomic radius decrease across a period even though more electrons are being added?",
    "The added electrons go into the same principal shell (same n), so they don't shield each other well from the also-increasing nuclear charge. The rising effective nuclear charge pulls all outer electrons closer to the nucleus, shrinking the radius despite the higher electron count.",
    "atomic_radius", "concept")

add("How does ionic radius compare to atomic radius for cations and anions?",
    "Cations (formed by losing electrons) are smaller than their parent atom, because removing electrons reduces electron-electron repulsion and often removes an entire outer shell. Anions (formed by gaining electrons) are larger than their parent atom, because added electrons increase electron-electron repulsion and the same nuclear charge now pulls on more electrons (lower effective pull per electron).",
    "ionic_radius", "concept")

add("Define ionization energy (IE) and describe its trend across a period and down a group.",
    "Ionization energy is the energy required to remove an electron from a gaseous atom or ion. It increases across a period (higher Z_eff holds electrons more tightly) and decreases down a group (outer electrons are farther from the nucleus and more shielded, so easier to remove).",
    "ionization_energy", "concept")

add("Why is there often a small dip in ionization energy between group 2 and group 13 (e.g., Be to B), and between group 15 and 16 (e.g., N to O)?",
    "Be-to-B: removing an electron from B takes it from a higher-energy p orbital (less stable, slightly shielded by the filled s subshell) rather than the more stable, fully filled 2s2 of Be — so B's IE is slightly lower despite higher Z.<br>N-to-O: N has a stable half-filled p^3 configuration (extra stability from Hund's rule/exchange energy); removing an electron from O's p^4 relieves electron-electron repulsion from a paired orbital, making it easier than expected, so O's first IE is slightly lower than N's.",
    "ionization_energy", "concept")

add("Why does the second ionization energy (IE2) jump dramatically for group 1 metals but not as much for group 2 metals?",
    "Group 1 metals lose their single valence electron easily (low IE1), but removing a second electron means breaking into the next full, lower-energy noble-gas-like core shell — this requires far more energy, causing a huge jump in IE2. Group 2 metals still have a second valence electron available in the same outer shell, so their IE2 is only moderately higher than IE1 (a big jump only appears at IE3 for group 2).",
    "ionization_energy", "concept")

add("Define electron affinity and describe its general periodic trend.",
    "Electron affinity is the energy change when an electron is added to a gaseous atom (usually released, so often reported as negative/exothermic for a favorable addition). It generally becomes more negative (more favorable/exothermic) across a period, and less negative (less favorable) down a group, mirroring the ionization energy trend, though with more exceptions (e.g., noble gases and group 2 have near-zero or unfavorable electron affinities).",
    "electron_affinity", "concept")

add("Why do noble gases have electron affinities close to zero or even positive (unfavorable)?",
    "Noble gases already have a completely filled valence shell (stable octet). Adding an extra electron would force it into a new, higher-energy shell far from the nucleus with poor shielding benefit, which is energetically unfavorable rather than stabilizing.",
    "electron_affinity", "concept")

# ---------- MISCONCEPTIONS ----------
add("Misconception check: Does effective nuclear charge equal the full nuclear charge (total protons) felt by every electron?",
    "No — effective nuclear charge is the actual nuclear charge reduced by shielding from other electrons (Z_eff = Z - S). Outer/valence electrons feel a much smaller pull than the full proton count because inner-shell (core) electrons shield them substantially.",
    "effective_nuclear_charge", "concept")

add("Misconception check: Since atomic radius decreases across a period, does ionic radius also always decrease across a period for isoelectronic ions?",
    "Not simply 'across a period' — the better comparison is among isoelectronic species (same electron count). Among ions/atoms with the same number of electrons, radius decreases as nuclear charge (Z) increases, since more protons pull the same electron cloud in tighter. So going from an anion to a cation with the same electron count (e.g., O2- > F- > Ne > Na+ > Mg2+), radius shrinks as Z increases, not strictly by periodic position alone.",
    "ionic_radius", "concept")

add("Misconception check: Is ionization energy the same as electron affinity, just with opposite sign?",
    "No — they describe different processes. Ionization energy is the energy required to remove an electron from a neutral (or charged) species, always requiring energy input (endothermic). Electron affinity is the energy change when an electron is added to a neutral atom, which is often (but not always) exothermic. They are related in trend direction but are physically distinct processes on different species.",
    "ionization_energy", "concept")

# ---------- APPLIED ----------
add("Rank the following in order of increasing atomic radius: Cl, Na, Al, S (all period 3 elements).",
    "All are in period 3, so radius decreases left to right across the period as Z_eff increases: Na (group 1) > Al (group 13) > S (group 16) > Cl (group 17).<br>Answer, increasing radius: Cl < S < Al < Na.",
    "atomic_radius", "applied")

add("Rank the following isoelectronic species in order of increasing radius: Mg^2+, O^2-, F^-, Na^+.",
    "All have 10 electrons (isoelectronic with Ne). Compare nuclear charge Z: O(8) < F(9) < Na(11) < Mg(12). More protons pulling on the same 10 electrons means a smaller radius, so radius decreases as Z increases.<br>Answer, increasing radius: Mg^2+ < Na^+ < F^- < O^2-.",
    "ionic_radius", "applied")

add("Which has the larger first ionization energy: potassium (K) or calcium (Ca)? Explain using Z_eff.",
    "Ca has the larger IE1. Both are in period 4, and Ca is to the right of K, so Ca has a higher effective nuclear charge on its valence electrons (more protons, same shielding from the argon core), making its 4s electron more tightly held and harder to remove than K's single 4s electron.",
    "ionization_energy", "applied")

add("Trap: A student claims sulfur (S) must have a higher first ionization energy than phosphorus (P) because S is farther right on the periodic table and IE increases left to right. Evaluate this claim.",
    "This is actually a known exception, similar to N/O: P has a stable half-filled 3p^3 configuration, giving it extra stability and making its electron slightly harder to remove than expected. S has 3p^4 (one paired orbital), and removing an electron relieves electron-electron repulsion in that paired orbital, making S's first IE slightly LOWER than P's — the opposite of the naive left-to-right rule. The general trend (increasing left to right) has known exceptions at half-filled/filled subshell boundaries.",
    "ionization_energy", "applied")

add("Choosing the right approach: Without a data table, predict whether Br or I has a more exothermic (more negative) electron affinity, and justify using periodic trends.",
    "Br is above I in group 17 (Br is period 4, I is period 5). Electron affinity becomes less favorable (less negative) going down a group because the added electron goes farther from the nucleus with more shielding, gaining less stabilization. So Br should have a more negative (more exothermic/favorable) electron affinity than I.",
    "electron_affinity", "applied")

add("Trap: A student says 'fluorine should have the most negative electron affinity of any element since it's the most electronegative and almost at the top-right of the periodic table.' Explain why this is actually not quite true experimentally.",
    "Although fluorine is highly electronegative, its very small atomic size causes significant electron-electron repulsion when an extra electron is added to its already-compact 2p subshell, making its electron affinity slightly less negative than expected — in fact, chlorine (Cl) has a more negative (more favorable) electron affinity than fluorine, because Cl is larger and can accommodate the extra electron with less repulsion. This shows periodic trends are general guides, not absolute rules — small, top-row elements sometimes break the naive expectation.",
    "electron_affinity", "applied")

path = os.path.join(os.path.dirname(__file__), "..", "outputs", "CHEM102_unit03_periodic_trends.txt")
n = write_tsv(cards, path)
print(f"Wrote {n} cards to {path}")
print(summarize(cards))
