import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import Card, write_tsv, summarize

TAG_COURSE = "chem102"
UNIT = "quantum_theory"

cards = []

def add(front, back, sub, kind):
    cards.append(Card(front, back, f"{TAG_COURSE} {UNIT}::{sub} {kind}"))

# ---------- CONCEPT ----------
add("What is the equation relating a photon's energy to its frequency, and what does each symbol mean?",
    "E = h*nu, where E = photon energy (J), h = Planck's constant (6.626 x 10^-34 J*s), and nu = frequency (Hz, s^-1).",
    "photon_energy", "concept")

add("What is the equation relating wavelength and frequency of light, and what does each symbol mean?",
    "c = lambda*nu, where c = speed of light (3.00 x 10^8 m/s), lambda = wavelength (m), and nu = frequency (Hz).",
    "photon_energy", "concept")

add("How do photon energy and wavelength relate to each other qualitatively?",
    "They are inversely related: shorter wavelength means higher frequency means higher energy per photon. Long-wavelength light (like radio waves) is low energy; short-wavelength light (like UV or X-rays) is high energy.",
    "photon_energy", "concept")

add("What did Bohr's model propose about electrons in a hydrogen atom?",
    "Electrons exist in specific, quantized circular orbits (energy levels, n = 1, 2, 3...) around the nucleus. Electrons in a given orbit have a fixed energy; they can jump between orbits by absorbing or emitting a photon whose energy exactly matches the energy difference between levels.",
    "bohr_model", "concept")

add("Why do atoms produce line spectra (discrete lines) rather than a continuous rainbow of colors when they emit light?",
    "Because electron energy levels are quantized, only specific energy differences (and thus specific photon frequencies/wavelengths) are allowed when an electron falls from a higher to a lower level. Since only certain transitions are possible, only certain wavelengths of light appear, producing discrete lines instead of a continuum.",
    "bohr_model", "concept")

add("List the four quantum numbers and what each one describes.",
    "n (principal): energy level/shell size, n = 1, 2, 3...<br>l (angular momentum): subshell shape (0=s, 1=p, 2=d, 3=f), ranges 0 to n-1.<br>m_l (magnetic): orientation of the orbital, ranges -l to +l.<br>m_s (spin): electron spin, +1/2 or -1/2.",
    "quantum_numbers", "concept")

add("What are the allowed values of l and m_l when n = 3?",
    "l can be 0, 1, or 2 (since l ranges 0 to n-1 = 2), corresponding to 3s, 3p, 3d subshells. For each l, m_l ranges from -l to +l: l=0 gives m_l=0 (1 orbital); l=1 gives m_l=-1,0,1 (3 orbitals); l=2 gives m_l=-2,-1,0,1,2 (5 orbitals).",
    "quantum_numbers", "concept")

add("State the Pauli exclusion principle.",
    "No two electrons in the same atom can have the identical set of all four quantum numbers. Practically, this means each orbital (defined by n, l, m_l) can hold at most 2 electrons, and those two must have opposite spins (+1/2 and -1/2).",
    "pauli_exclusion", "concept")

add("State Hund's rule.",
    "When filling degenerate orbitals (orbitals of equal energy, e.g. the three 2p orbitals), electrons fill each orbital singly, with parallel spins, before any orbital gets a second electron.",
    "hunds_rule", "concept")

add("State the Aufbau principle.",
    "Electrons fill atomic orbitals starting from the lowest available energy level and proceeding to higher energy levels, following the order given by the (n + l) rule (e.g., 1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p...).",
    "aufbau_principle", "concept")

add("Why does the 4s orbital fill before the 3d orbital, even though n=3 is 'lower' than n=4?",
    "Orbital filling order depends on overall energy, not just principal quantum number n. Due to shielding and penetration effects, the 4s orbital is lower in energy than 3d for atoms being built up (Aufbau order), so 4s fills first even though 3d has a smaller n.",
    "aufbau_principle", "concept")

add("Write the full ground-state electron configuration for chlorine (Z=17).",
    "1s^2 2s^2 2p^6 3s^2 3p^5 (total electrons = 2+2+6+2+5 = 17).",
    "electron_configuration", "concept")

add("What is the noble gas (condensed) electron configuration notation, and how do you write it for potassium (Z=19)?",
    "It abbreviates the filled inner shells using the preceding noble gas symbol in brackets, then lists only the remaining electrons. For K (Z=19): [Ar] 4s^1, since Ar (Z=18) accounts for the first 18 electrons.",
    "electron_configuration", "concept")

add("Why are chromium (Cr) and copper (Cu) common exceptions to the standard Aufbau filling order?",
    "A half-filled (d^5) or completely filled (d^10) d subshell has extra stability from favorable electron exchange energy. So instead of [Ar] 4s^2 3d^4, chromium is [Ar] 4s^1 3d^5 (half-filled d), and instead of [Ar] 4s^2 3d^9, copper is [Ar] 4s^1 3d^10 (filled d) — one 4s electron shifts into the 3d subshell to gain this stability.",
    "electron_configuration", "concept")

# ---------- MISCONCEPTIONS ----------
add("Misconception check: Does a higher-energy electron orbit farther from the nucleus mean it moves in a fixed, well-defined circular path like a planet?",
    "No — that classical picture is the Bohr model, which works only for describing hydrogen's energy levels approximately. The modern quantum mechanical model describes orbitals as probability distributions (regions of space where an electron is likely to be found), not fixed paths or orbits.",
    "bohr_model", "concept")

add("Misconception check: When writing electron configurations, do electrons fill orbitals strictly in order of increasing n (all of n=3 before any of n=4)?",
    "No — filling follows increasing (n+l) energy order (Aufbau), not strict n order. For example, 4s (n+l = 4) fills before 3d (n+l = 5), so 4s electrons are added before 3d electrons even though n=3 < n=4.",
    "aufbau_principle", "concept")

add("Misconception check: Do all three 2p orbitals get fully paired up (2 electrons each) before moving to the next orbital, per Hund's rule?",
    "No — Hund's rule says the opposite: electrons occupy each degenerate orbital singly first (with parallel spin) before any orbital receives a second electron. For example, with 3 electrons in 2p, each of the three 2p orbitals gets one electron, rather than pairing two electrons in one orbital while leaving another empty.",
    "hunds_rule", "concept")

# ---------- APPLIED ----------
add("Calculate the energy of a photon with wavelength 500 nm.",
    "Step 1: find frequency using c = lambda*nu -> nu = c/lambda = (3.00x10^8 m/s)/(500x10^-9 m) = 6.00x10^14 Hz.<br>Step 2: use E = h*nu = (6.626x10^-34 J*s)(6.00x10^14 Hz) = 3.98x10^-19 J.<br>Answer: E ~ 3.98 x 10^-19 J per photon.",
    "photon_energy", "applied")

add("A laser emits photons with energy 4.42 x 10^-19 J. What is the wavelength of this light, in nm?",
    "Step 1: find frequency from E = h*nu -> nu = E/h = (4.42x10^-19 J)/(6.626x10^-34 J*s) = 6.67x10^14 Hz.<br>Step 2: find wavelength from c = lambda*nu -> lambda = c/nu = (3.00x10^8 m/s)/(6.67x10^14 Hz) = 4.50x10^-7 m = 450 nm.<br>Answer: 450 nm (blue-violet visible light).",
    "photon_energy", "applied")

add("Write the full and condensed (noble gas core) electron configurations for iron, Fe (Z=26).",
    "Fill in Aufbau order: 1s^2 2s^2 2p^6 3s^2 3p^6 4s^2 3d^6 (2+2+6+2+6+2+6=26).<br>Condensed: [Ar] 4s^2 3d^6.<br>Answer: full form 1s^2 2s^2 2p^6 3s^2 3p^6 4s^2 3d^6; condensed [Ar]4s^2 3d^6.",
    "electron_configuration", "applied")

add("Give a complete, valid set of four quantum numbers for the last electron added when building up phosphorus (Z=15).",
    "P's configuration is 1s^2 2s^2 2p^6 3s^2 3p^3. The 3p subshell has 3 electrons, and by Hund's rule they occupy the three 3p orbitals singly with parallel spin before pairing. So the last (3rd) electron added: n=3, l=1 (p), m_l can be -1, 0, or +1 (whichever was still empty — commonly written as m_l = +1 for the third one added), m_s = +1/2 (parallel to the first two).<br>Answer: n=3, l=1, m_l=+1, m_s=+1/2 (one valid answer; m_l could be listed as -1,0,+1 depending on the electron being tracked, but m_s must be +1/2 for all three per Hund's rule).",
    "quantum_numbers", "applied")

add("Trap: A student writes the electron configuration of Cr (Z=24) as [Ar] 4s^2 3d^4, following the standard Aufbau filling order table. Is this correct? Explain.",
    "This is incorrect. Chromium is an Aufbau exception: because a half-filled d subshell (d^5) is unusually stable, one electron shifts from 4s into 3d. The correct configuration is [Ar] 4s^1 3d^5, not [Ar] 4s^2 3d^4. This exception must be memorized — it is not predicted by the standard filling-order chart alone.",
    "electron_configuration", "applied")

add("Trap: A student calculates photon energy using E = h*nu but plugs in wavelength (500 nm) directly for nu without converting to frequency. What is wrong, and what is the correct result?",
    "The error is skipping the c = lambda*nu conversion — h*nu requires frequency (in Hz), not wavelength. Plugging wavelength directly gives a nonsensical, wildly wrong energy value. Correct approach: first nu = c/lambda = (3.00x10^8)/(500x10^-9) = 6.00x10^14 Hz, then E = h*nu = (6.626x10^-34)(6.00x10^14) = 3.98x10^-19 J. Always convert wavelength to frequency (or use E = hc/lambda directly) before computing energy.",
    "photon_energy", "applied")

add("Choosing the right approach: For n = 4, how many total orbitals and how many total electrons can this shell hold?",
    "Total orbitals in shell n = n^2 = 16 orbitals (from l=0,1,2,3 giving 1+3+5+7=16 orbitals). Each orbital holds 2 electrons (Pauli exclusion), so total electron capacity = 2n^2 = 2(16) = 32 electrons.<br>Answer: 16 orbitals, 32 electrons maximum.",
    "quantum_numbers", "applied")

path = os.path.join(os.path.dirname(__file__), "..", "outputs", "CHEM102_unit02_quantum_theory.txt")
n = write_tsv(cards, path)
print(f"Wrote {n} cards to {path}")
print(summarize(cards))
