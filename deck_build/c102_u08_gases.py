import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import Card, write_tsv, summarize

TAG_COURSE = "chem102"
UNIT = "gases"
cards = []

def add(front, back, sub, kind):
    cards.append(Card(front, back, f"{TAG_COURSE} {UNIT}::{sub} {kind}"))

# ---------- CONCEPT ----------
add("State the ideal gas law and define every variable with typical units.",
    "PV = nRT, where P = pressure (atm), V = volume (L), n = moles of gas (mol), R = ideal gas constant (0.08206 L*atm/(mol*K)), and T = temperature in KELVIN (K).",
    "ideal_gas_law", "concept")

add("State Boyle's Law, Charles's Law, and Gay-Lussac's Law, noting what is held constant in each.",
    "Boyle's Law: P1V1 = P2V2 (constant n, T) — pressure and volume are inversely related.<br>Charles's Law: V1/T1 = V2/T2 (constant n, P) — volume and temperature are directly related.<br>Gay-Lussac's Law: P1/T1 = P2/T2 (constant n, V) — pressure and temperature are directly related.",
    "gas_laws", "concept")

add("What is the combined gas law, and when is it useful?",
    "P1V1/T1 = P2V2/T2 (constant n). It's useful when both pressure, volume, and temperature all change for a fixed amount of gas, combining Boyle's, Charles's, and Gay-Lussac's laws into one equation.",
    "gas_laws", "concept")

add("Why must temperature always be converted to Kelvin before using it in any gas law calculation?",
    "Gas law relationships (like V proportional to T, or P proportional to T) are proportionalities that only hold true relative to absolute zero (0 K), where a gas's volume/pressure would theoretically reach zero. Celsius has an arbitrary zero point (freezing point of water), so a proportional relationship like V1/T1 = V2/T2 would give nonsensical results (including division by zero or negative volumes) if Celsius were used instead of Kelvin.",
    "gas_laws", "concept")

add("State Dalton's Law of partial pressures, and give its formula.",
    "The total pressure of a mixture of non-reacting gases equals the sum of the partial pressures each gas would exert if it alone occupied the same container. Formula: P_total = P1 + P2 + P3 + ...",
    "partial_pressures", "concept")

add("What is mole fraction, and how does it relate to partial pressure?",
    "Mole fraction (chi) is the ratio of moles of one component to the total moles of all components in a mixture: chi_A = n_A / n_total. Partial pressure relates to mole fraction by P_A = chi_A x P_total.",
    "partial_pressures", "concept")

add("List the key postulates of the Kinetic Molecular Theory (KMT) of gases.",
    "1) Gas particles are in constant, random motion.<br>2) Gas particle volume is negligible compared to the container volume (particles are treated as point masses).<br>3) There are no attractive or repulsive forces between gas particles (collisions are perfectly elastic).<br>4) Average kinetic energy is directly proportional to absolute temperature (in Kelvin), and is the same for all gases at a given temperature.",
    "kinetic_molecular_theory", "concept")

add("State Graham's Law of effusion, and what it predicts about lighter vs heavier gases.",
    "Rate1/Rate2 = sqrt(M2/M1), where M is molar mass. Lighter gases (smaller M) effuse/diffuse faster than heavier gases, because at a given temperature all gases have the same average kinetic energy, so lower-mass particles must move faster to compensate.",
    "effusion_diffusion", "concept")

add("Under what conditions do real gases deviate most from ideal gas behavior, and why?",
    "Real gases deviate most at high pressure and low temperature. At high pressure, gas particles are pushed close together, so their actual (nonzero) volume becomes significant relative to the container volume (violating the KMT assumption of negligible particle volume). At low temperature, particles move slower, giving intermolecular attractive forces enough time/opportunity to matter (violating the 'no attractive forces' assumption), pulling particles together and reducing the pressure/volume compared to ideal predictions.",
    "real_gases", "concept")

# ---------- MISCONCEPTIONS ----------
add("Misconception check: At the same temperature, do heavier gas molecules have more kinetic energy than lighter gas molecules?",
    "No — according to KMT, average KINETIC ENERGY depends only on temperature (in Kelvin), not molar mass; at a given temperature, all gases (regardless of mass) have the same average kinetic energy. What differs is SPEED: since KE = (1/2)mv^2, a lighter molecule must move faster than a heavier one to have the same average kinetic energy.",
    "kinetic_molecular_theory", "concept")

add("Misconception check: Does increasing the temperature of a gas at constant volume increase the pressure because the molecules 'get bigger' or 'take up more space'?",
    "No — molecule size does not change with temperature. Increasing temperature increases the average kinetic energy (speed) of gas molecules, causing them to collide with the container walls more frequently and with greater force per collision, which increases pressure (Gay-Lussac's Law) — this is a change in collision frequency/force, not molecular size.",
    "gas_laws", "concept")

add("Misconception check: Is 'STP' the same set of conditions in every textbook/context?",
    "Not always — the traditional STP definition is 0 deg C (273.15 K) and 1 atm, under which 1 mole of ideal gas occupies 22.4 L. However, IUPAC's more current standard uses 0 deg C and 100 kPa (0.987 atm), giving 22.7 L/mol. Always check which convention a given problem or course is using, since it affects molar volume calculations.",
    "ideal_gas_law", "concept")

# ---------- APPLIED ----------
add("A gas occupies 5.00 L at 1.20 atm and 298 K. What volume will it occupy at 2.40 atm and 350 K?",
    "Use the combined gas law: P1V1/T1 = P2V2/T2.<br>(1.20 atm)(5.00 L)/(298 K) = (2.40 atm)(V2)/(350 K).<br>Solve: V2 = [(1.20)(5.00)(350)] / [(298)(2.40)] = 2100/715.2 = 2.94 L.<br>Answer: V2 = 2.94 L.",
    "gas_laws", "applied")

add("Calculate the pressure exerted by 2.50 mol of an ideal gas in a 10.0 L container at 27 deg C.",
    "Convert T to Kelvin: 27 + 273 = 300 K.<br>Use PV = nRT -> P = nRT/V = (2.50 mol)(0.08206 L*atm/mol*K)(300 K)/(10.0 L) = 61.545/10.0 = 6.15 atm.<br>Answer: P = 6.15 atm.",
    "ideal_gas_law", "applied")

add("A gas mixture contains 2.0 mol N2, 3.0 mol O2, and 1.0 mol CO2 at a total pressure of 6.0 atm. Find the partial pressure of O2.",
    "Total moles = 2.0 + 3.0 + 1.0 = 6.0 mol.<br>Mole fraction of O2 = 3.0/6.0 = 0.50.<br>Partial pressure O2 = chi_O2 x P_total = 0.50 x 6.0 atm = 3.0 atm.<br>Answer: P(O2) = 3.0 atm.",
    "partial_pressures", "applied")

add("Compare the effusion rates of He (M=4.00 g/mol) and O2 (M=32.00 g/mol): how many times faster does He effuse than O2?",
    "Use Graham's Law: Rate(He)/Rate(O2) = sqrt(M(O2)/M(He)) = sqrt(32.00/4.00) = sqrt(8) = 2.83.<br>Answer: He effuses about 2.83 times faster than O2.",
    "effusion_diffusion", "applied")

add("Trap: A student uses PV=nRT with T = 25 (forgetting to convert from Celsius) to find moles of gas at P=1.00 atm, V=10.0 L. Identify the error and give the corrected calculation.",
    "The error is using 25 directly as if it were Kelvin, when 25 is actually in Celsius. Correct: T = 25 + 273 = 298 K.<br>n = PV/RT = (1.00 atm)(10.0 L) / [(0.08206 L*atm/mol*K)(298 K)] = 10.0/24.45 = 0.409 mol.<br>Using the uncorrected T=25 K would give a drastically wrong (much larger) mole value: n = 10.0/(0.08206x25) = 4.87 mol — nearly 12x too high. Always convert Celsius to Kelvin (add 273.15) before plugging into any gas law equation.",
    "ideal_gas_law", "applied")

add("Choosing the right approach: A rigid, sealed 5.0 L container holds gas at 2.00 atm and 300 K. If the container is heated to 450 K, what is the new pressure? Which law applies and why?",
    "Since the container is rigid and sealed, V and n are both constant — this calls for Gay-Lussac's Law (P1/T1 = P2/T2), not the full ideal gas law or combined gas law (which would be unnecessarily complex when V and n don't change).<br>P2 = P1 x (T2/T1) = 2.00 atm x (450/300) = 2.00 x 1.5 = 3.00 atm.<br>Answer: P2 = 3.00 atm. Recognizing which variables are held constant (here, V and n) is the key step in choosing the simplest correct gas law.",
    "gas_laws", "applied")

add("Trap: A student assumes real gas behavior always causes HIGHER measured pressure than the ideal gas law predicts, because 'real molecules take up space and push harder.' Evaluate and correct this reasoning.",
    "This reasoning is incomplete/incorrect in general. Real gas deviations arise from two competing effects with opposite directions: (1) finite molecular volume tends to make the real gas exert slightly HIGHER pressure than ideal at a given volume (less free space than assumed), while (2) intermolecular attractive forces tend to make real gas pressure LOWER than ideal (attractions pull molecules together and soften their wall collisions). At high pressure, the volume effect tends to dominate (P_real > P_ideal), but at moderate pressure/low temperature, attractive forces can dominate and make P_real < P_ideal. There isn't one universal direction — it depends on conditions, and both effects are captured together in the van der Waals equation's 'a' (attraction) and 'b' (volume) correction terms.",
    "real_gases", "applied")

path = os.path.join(os.path.dirname(__file__), "..", "outputs", "CHEM102_unit08_gases.txt")
n = write_tsv(cards, path)
print(f"Wrote {n} cards to {path}")
print(summarize(cards))
