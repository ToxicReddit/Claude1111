import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import Card, write_tsv, summarize

TAG_COURSE = "chem102"
UNIT = "atomic_structure"

cards = []

def add(front, back, sub, kind):
    cards.append(Card(front, back, f"{TAG_COURSE} {UNIT}::{sub} {kind}"))

# ---------- CONCEPT CARDS ----------
add("What are Dalton's four postulates of atomic theory?",
    "1) All matter is made of indivisible atoms.<br>2) All atoms of a given element are identical in mass and properties.<br>3) Atoms combine in small whole-number ratios to form compounds.<br>4) Chemical reactions rearrange atoms but do not create, destroy, or convert them into other atoms.",
    "dalton_model", "concept")

add("What did J.J. Thomson's cathode ray tube experiment reveal, and what model resulted?",
    "It showed that atoms contain small, negatively charged particles (electrons) with a very large charge-to-mass ratio. This led to the 'plum pudding' model: a diffuse positive charge with electrons embedded in it.",
    "thomson_model", "concept")

add("What did Rutherford's gold foil experiment show, and why was the result surprising?",
    "Most alpha particles passed straight through the foil, but a small fraction deflected at large angles (some almost backward). This was surprising under the plum-pudding model, which predicted only small deflections. It implied that positive charge and most of the mass are concentrated in a tiny, dense nucleus, with the atom being mostly empty space.",
    "rutherford_model", "concept")

add("Define atomic number (Z) and mass number (A).",
    "Atomic number (Z) = number of protons in the nucleus (defines the element). Mass number (A) = number of protons + neutrons (total nucleons) in a specific atom/isotope.",
    "isotopes", "concept")

add("What are isotopes?",
    "Atoms of the same element (same number of protons, same Z) that have different numbers of neutrons, and therefore different mass numbers (A).",
    "isotopes", "concept")

add("How is the number of neutrons calculated from A and Z?",
    "Neutrons = A - Z (mass number minus atomic number).",
    "isotopes", "concept")

add("What does the notation ^A_Z X (e.g., 13/6 C) tell you?",
    "X is the element symbol; the subscript Z is the atomic number (protons); the superscript A is the mass number (protons + neutrons). For 13/6 C: 6 protons, 13 - 6 = 7 neutrons.",
    "isotopes", "concept")

add("What is average atomic mass, and why is it usually not a whole number?",
    "It is the weighted average of the masses of all naturally occurring isotopes of an element, weighted by their relative natural abundances. It is not a whole number because it blends multiple isotope masses (each close to whole numbers) in proportions that are almost never round.",
    "average_atomic_mass", "concept")

add("Why do the masses of individual isotopes (like carbon-12, carbon-13) come out to nearly whole numbers, but the periodic table mass for carbon is 12.011?",
    "Each isotope's mass is close to a whole number because it is dominated by the integer number of protons and neutrons (each contributing ~1 amu). The periodic table value (12.011) is the natural abundance-weighted average across all isotopes, so it reflects a mixture rather than one nuclide's mass.",
    "average_atomic_mass", "concept")

add("What is the difference between an atom and an ion in terms of subatomic particles?",
    "An atom is electrically neutral: number of electrons equals number of protons. An ion has an imbalance: a cation has fewer electrons than protons (net positive charge), and an anion has more electrons than protons (net negative charge). Protons (and thus identity/Z) do not change.",
    "ions", "concept")

add("Why does losing or gaining electrons not change what element an atom is, but losing or gaining protons does?",
    "Element identity is defined solely by the number of protons (Z). Electrons can be gained or lost relatively easily (forming ions) without altering the nucleus. Changing the number of protons would change Z, which by definition converts the atom into a different element (this only happens in nuclear reactions, not ordinary chemistry).",
    "ions", "concept")

add("What are the charge and approximate mass (in amu) of a proton, neutron, and electron?",
    "Proton: charge +1, mass ~1 amu. Neutron: charge 0, mass ~1 amu. Electron: charge -1, mass ~1/1836 amu (negligible compared to nucleons).",
    "subatomic_particles", "concept")

# ---------- MISCONCEPTIONS ----------
add("Misconception check: Does a higher mass number always mean a 'heavier version' with different chemical properties?",
    "No — isotopes of the same element have essentially identical chemical properties because chemistry is governed by electron configuration (determined by Z, the number of protons/electrons), not by the number of neutrons. Extra neutrons change mass and nuclear stability (and can matter for physical properties like diffusion rate or radioactivity) but not the chemical bonding behavior.",
    "isotopes", "concept")

add("Misconception check: In Rutherford's model, is the nucleus a large fraction of the atom's volume?",
    "No — the nucleus is extremely small relative to the overall size of the atom (roughly 1/10,000th of the atom's radius) even though it holds almost all the mass. The atom is mostly empty space occupied by the much larger electron cloud.",
    "rutherford_model", "concept")

add("Misconception check: Is average atomic mass simply the average of a 'typical' isotope's protons and neutrons?",
    "No — it is a weighted average based on each isotope's actual natural abundance (percentage), not a simple average of all known isotopes. An isotope that makes up 99% of natural samples dominates the average far more than a rare 0.01% isotope.",
    "average_atomic_mass", "concept")

# ---------- APPLIED CARDS ----------
add("An atom of chlorine has 17 protons and 18 neutrons. Write its symbol in ^A_Z X notation and state A and Z.",
    "Z = 17 (protons, defines chlorine). A = protons + neutrons = 17 + 18 = 35. Symbol: 35/17 Cl (mass number 35, atomic number 17).",
    "isotopes", "applied")

add("How many protons, neutrons, and electrons are in the ion 56/26 Fe 3+?",
    "Z = 26, so protons = 26. Neutrons = A - Z = 56 - 26 = 30. The 3+ charge means 3 fewer electrons than protons: electrons = 26 - 3 = 23.<br>Answer: 26 protons, 30 neutrons, 23 electrons.",
    "ions", "applied")

add("Copper has two naturally occurring isotopes: Cu-63 (mass 62.930 amu, abundance 69.17%) and Cu-65 (mass 64.928 amu, abundance 30.83%). Calculate the average atomic mass of copper.",
    "Weighted average = (fractional abundance x mass) summed over isotopes.<br>Setup: (0.6917)(62.930 amu) + (0.3083)(64.928 amu)<br>= 43.531 amu + 20.019 amu<br>= 63.55 amu.<br>Answer: 63.55 amu, matching the periodic table value for Cu.",
    "average_atomic_mass", "applied")

add("Trap: Boron has isotopes B-10 (10.013 amu) and B-11 (11.009 amu), and boron's average atomic mass is 10.81 amu. A student assumes the two isotopes are equally abundant (50/50) and calculates (10.013+11.009)/2 = 10.51 amu, then reports 10.51 amu as boron's atomic mass. What went wrong, and what must be true instead?",
    "The error is assuming equal (50/50) abundance without being given that data. Average atomic mass is abundance-weighted, not a simple mean of isotope masses. Since the correct value (10.81) is closer to B-11's mass (11.009) than to B-10's mass (10.013), B-11 must be the more abundant isotope (in reality, about 80% B-11 and 20% B-10). Without abundance data, you cannot compute average atomic mass by simple averaging.",
    "average_atomic_mass", "applied")

add("A neutral atom has mass number 39 and 20 neutrons. Identify the element and give the number of protons and electrons.",
    "Protons = A - neutrons = 39 - 20 = 19. Z = 19 corresponds to potassium (K). Since the atom is neutral, electrons = protons = 19.<br>Answer: Potassium-39, 19 protons, 19 electrons, 20 neutrons.",
    "isotopes", "applied")

add("Choosing the right approach: You're told an ion has 34 protons, 45 neutrons, and 36 electrons. Determine the mass number, the charge, and identify the element.",
    "Mass number A = protons + neutrons = 34 + 45 = 79.<br>Charge = protons - electrons = 34 - 36 = -2 (2 extra electrons means net negative charge).<br>Z = 34 corresponds to selenium (Se).<br>Answer: 79/34 Se^2-, a selenide ion.",
    "ions", "applied")

add("Trap: A student sees the ion Cr^3+ and reasons 'chromium normally has 24 electrons, so losing 3 electrons must also remove 3 neutrons to keep the mass number the same, giving fewer neutrons.' Explain the error.",
    "Charge is determined only by the electron count relative to protons; forming an ion never changes the number of neutrons or protons in the nucleus. Cr^3+ has the same number of protons (24) and neutrons as neutral Cr — only electrons change (24 - 3 = 21 electrons). Mass number A depends on protons + neutrons, which are unaffected by ionization, so A stays the same.",
    "ions", "applied")

path = os.path.join(os.path.dirname(__file__), "..", "outputs", "CHEM102_unit01_atomic_structure.txt")
n = write_tsv(cards, path)
print(f"Wrote {n} cards to {path}")
print(summarize(cards))
