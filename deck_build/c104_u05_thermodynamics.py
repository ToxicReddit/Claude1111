import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import Card, write_tsv, summarize

TAG_COURSE = "chem104"
UNIT = "thermodynamics"
cards = []

def add(front, back, sub, kind):
    cards.append(Card(front, back, f"{TAG_COURSE} {UNIT}::{sub} {kind}"))

# ---------- CONCEPT ----------
add("Define entropy (S), and give an intuitive description of what it measures.",
    "Entropy is a thermodynamic state function that measures the number of accessible microstates (ways to arrange energy/matter) of a system — informally, a measure of dispersal of energy and disorder/randomness. Higher entropy corresponds to more possible microstates (more disorder/dispersal); lower entropy corresponds to fewer accessible microstates (more order).",
    "entropy_basics", "concept")

add("State the second law of thermodynamics.",
    "For any spontaneous process, the total entropy of the universe (system + surroundings) increases: deltaS_universe = deltaS_system + deltaS_surroundings > 0. (At equilibrium, deltaS_universe = 0; it can never be negative for a real, spontaneous process.)",
    "entropy_basics", "concept")

add("List three general factors that increase the entropy of a system (give qualitative predictions of deltaS sign).",
    "1) Increasing temperature (more thermal motion/microstates).<br>2) Phase change solid -> liquid -> gas (increasing disorder/freedom of motion; gases have by far the highest entropy).<br>3) Increasing the number of gas particles/moles in a reaction, or dissolving a solid into solution (more possible arrangements/positions).",
    "entropy_basics", "concept")

add("Why does entropy generally increase when a solid or liquid dissolves into solution, or when the number of moles of gas increases in a reaction?",
    "Both processes increase the number of ways the system's particles/energy can be arranged (increase in accessible microstates). Dissolving disperses particles throughout the solvent (more possible positions than in the fixed lattice of a solid); increasing gas moles gives more independently moving, freely dispersing particles occupying more possible positions/momenta, both of which raise the system's entropy.",
    "entropy_basics", "concept")

add("Define Gibbs free energy (G), and give the equation relating deltaG, deltaH, and deltaS.",
    "Gibbs free energy combines enthalpy and entropy into one property that determines spontaneity at constant temperature and pressure. Equation: deltaG = deltaH - T*deltaS, where T must be in Kelvin.",
    "gibbs_free_energy", "concept")

add("What does the sign of deltaG indicate about a process's spontaneity?",
    "deltaG < 0: spontaneous (favorable) in the forward direction as written.<br>deltaG > 0: nonspontaneous in the forward direction (spontaneous in reverse).<br>deltaG = 0: system is at equilibrium (no net driving force in either direction).",
    "gibbs_free_energy", "concept")

add("Complete the table of spontaneity based on the signs of deltaH and deltaS: (a) deltaH<0, deltaS>0; (b) deltaH>0, deltaS<0; (c) deltaH<0, deltaS<0; (d) deltaH>0, deltaS>0.",
    "(a) deltaH<0, deltaS>0: deltaG always negative -> spontaneous at ALL temperatures.<br>(b) deltaH>0, deltaS<0: deltaG always positive -> NEVER spontaneous (nonspontaneous at all T).<br>(c) deltaH<0, deltaS<0: spontaneous only at LOW temperature (favorable enthalpy must outweigh the T*deltaS penalty).<br>(d) deltaH>0, deltaS>0: spontaneous only at HIGH temperature (favorable entropy term must outweigh unfavorable enthalpy).",
    "gibbs_free_energy", "concept")

add("Why can a reaction with a positive (unfavorable) deltaH still be spontaneous at high enough temperature?",
    "If deltaS is also positive (favorable), the term -T*deltaS becomes increasingly negative as T increases. At sufficiently high T, this large negative -T*deltaS term can outweigh the positive deltaH, making the overall deltaG = deltaH - T*deltaS negative (spontaneous), even though the process absorbs heat.",
    "gibbs_free_energy", "concept")

add("Give the equation relating standard Gibbs free energy (deltaG°) to the equilibrium constant K.",
    "deltaG° = -RT ln(K), where R = 8.314 J/(mol*K), T is absolute temperature (K). Equivalently, K = e^(-deltaG°/RT). This shows deltaG° and K are directly linked: a very negative deltaG° corresponds to a very large K (products strongly favored), and vice versa.",
    "deltaG_and_K", "concept")

add("What does it mean if deltaG° = 0 for a reaction, in terms of K?",
    "If deltaG° = 0, then K = e^(0) = 1, meaning that under STANDARD conditions, the reaction is already essentially at its equilibrium point (products and reactants present in comparable, thermodynamically balanced amounts) — neither strongly favored.",
    "deltaG_and_K", "concept")

add("Distinguish deltaG (nonstandard) from deltaG° (standard), and give the equation relating them via Q.",
    "deltaG° is calculated under standard conditions (1 M concentrations, 1 atm pressure, specified temperature, usually 25 deg C). deltaG is the free energy change under ACTUAL, non-standard (real, current) conditions. Relationship: deltaG = deltaG° + RT ln(Q), where Q is the reaction quotient calculated from actual (current) concentrations/pressures.",
    "deltaG_and_Q", "concept")

add("Why does a reaction with deltaG° > 0 (nonspontaneous under standard conditions) potentially still proceed spontaneously under certain non-standard conditions?",
    "Spontaneity under real conditions is governed by deltaG (not deltaG°): deltaG = deltaG° + RT ln(Q). If the actual reaction quotient Q is sufficiently small (far below K, e.g., very low product concentrations or very high reactant concentrations), the RT ln(Q) term can be very negative, making the overall deltaG negative (spontaneous) even if deltaG° itself is positive. This is why reactions can be 'pushed' by manipulating concentrations away from standard conditions.",
    "deltaG_and_Q", "concept")

add("Give the equation relating deltaG° to the standard cell potential E° for an electrochemical process, and define the variables.",
    "deltaG° = -nFE°, where n = moles of electrons transferred in the balanced redox reaction, F = Faraday's constant (96,485 C/mol e-), and E° = standard cell potential (V). This links thermodynamics (deltaG°) directly to electrochemistry (E°).",
    "deltaG_and_E", "concept")

add("If a redox reaction has a positive standard cell potential E°, what does this imply about deltaG° and K?",
    "A positive E° (spontaneous redox reaction as written) corresponds to a NEGATIVE deltaG° (since deltaG°=-nFE°, and n, F are always positive, so positive E° gives negative deltaG°), which in turn corresponds to K > 1 (products favored at equilibrium), consistent with deltaG°=-RTlnK.",
    "deltaG_and_E", "concept")

# ---------- MISCONCEPTIONS ----------
add("Misconception check: Does a spontaneous process always happen quickly, or release energy (be exothermic)?",
    "No — 'spontaneous' in thermodynamics means the process is thermodynamically favorable (deltaG<0) and will occur without continuous outside energy input, given enough TIME — it says nothing about the RATE (a kinetics property, separate from thermodynamics). Also, spontaneous processes can be endothermic if driven by a sufficiently large positive deltaS (e.g., dissolving ammonium nitrate in water is spontaneous and endothermic — the classic 'cold pack' reaction).",
    "gibbs_free_energy", "concept")

add("Misconception check: Does the entropy of the SYSTEM alone determine whether a process is spontaneous?",
    "No — the second law requires TOTAL entropy of the universe (system + surroundings) to increase for a spontaneous process; the system's own entropy can actually decrease in a spontaneous process (e.g., water freezing, deltaS_system<0) as long as the surroundings' entropy increases by an even larger amount (heat released to surroundings during freezing increases surroundings' entropy more than enough to compensate). Gibbs free energy (deltaG = deltaH - TdeltaS_system) conveniently folds this surroundings entropy contribution (via deltaH) into a single system-based criterion, which is why it works using only system-based quantities.",
    "entropy_basics", "concept")

add("Misconception check: Does deltaG° = -RTlnK mean deltaG (not deltaG°) is always zero at equilibrium?",
    "The correct statement is: deltaG (the actual/nonstandard free energy) equals ZERO once a reaction reaches equilibrium (Q=K), not deltaG°, which is typically a fixed nonzero standard-state value. deltaG° is a constant for a given reaction/temperature representing the standard-state free energy difference between pure products and pure reactants; it is deltaG (which depends on Q via deltaG=deltaG°+RTlnQ) that becomes exactly zero specifically when the system reaches equilibrium (Q=K).",
    "deltaG_and_K", "concept")

# ---------- APPLIED ----------
add("A reaction has deltaH = -92.0 kJ and deltaS = -199 J/K at 298 K. Calculate deltaG and determine if it's spontaneous at this temperature.",
    "Convert deltaS to kJ/K: -199 J/K = -0.199 kJ/K.<br>deltaG = deltaH - TdeltaS = -92.0 kJ - (298 K)(-0.199 kJ/K) = -92.0 - (-59.30) = -92.0 + 59.30 = -32.7 kJ.<br>Answer: deltaG = -32.7 kJ, which is negative, so the reaction IS spontaneous at 298 K (favorable enthalpy outweighs the unfavorable entropy at this temperature).",
    "gibbs_free_energy", "applied")

add("For the reaction in the previous problem (deltaH=-92.0 kJ, deltaS=-199 J/K), calculate the temperature above which the reaction becomes nonspontaneous.",
    "At the crossover temperature, deltaG = 0: 0 = deltaH - TdeltaS -> T = deltaH/deltaS.<br>T = (-92,000 J) / (-199 J/K) = 462.3 K.<br>Answer: above T ~ 462 K, the reaction becomes nonspontaneous (since deltaS<0 makes the -TdeltaS term increasingly positive/unfavorable as T rises).",
    "gibbs_free_energy", "applied")

add("Calculate K at 298 K for a reaction with deltaG° = -10.0 kJ/mol.",
    "deltaG° = -RTlnK -> lnK = -deltaG°/(RT) = -(-10,000 J/mol)/[(8.314 J/mol*K)(298 K)] = 10,000/2477.6 = 4.036.<br>K = e^4.036 = 56.6.<br>Answer: K = 56.6 (K>1, consistent with the favorable/negative deltaG°).",
    "deltaG_and_K", "applied")

add("A reaction has deltaG° = +5.00 kJ/mol at 298 K. Actual concentrations give Q = 0.00100. Calculate deltaG under these actual conditions and determine spontaneity.",
    "deltaG = deltaG° + RTlnQ = 5000 J/mol + (8.314)(298)ln(0.00100) = 5000 + (2477.6)(-6.908) = 5000 + (-17,116) = -12,116 J/mol = -12.1 kJ/mol.<br>Answer: deltaG = -12.1 kJ/mol, which is NEGATIVE, so the reaction IS spontaneous under these actual (non-standard) conditions, even though deltaG° was positive (nonspontaneous under standard conditions) — the low Q (product-starved conditions) drives the reaction forward.",
    "deltaG_and_Q", "applied")

add("Trap: A student sees deltaS_system = -50 J/K (negative) for a reaction and immediately concludes the reaction cannot be spontaneous at any temperature. Evaluate this claim.",
    "This conclusion is premature — a negative deltaS_system does NOT by itself rule out spontaneity; it depends on deltaH as well. If deltaH is sufficiently negative (exothermic enough), deltaG = deltaH - TdeltaS can still be negative (spontaneous) at sufficiently LOW temperatures, since the -TdeltaS term (positive, since deltaS is negative) is small at low T and can be outweighed by a strongly negative deltaH. The reaction would only be nonspontaneous at ALL temperatures if BOTH deltaH>0 AND deltaS<0 (both terms unfavorable) — a negative deltaS alone, without checking deltaH, is insufficient to conclude anything about spontaneity in general.",
    "gibbs_free_energy", "applied")

add("Choosing the right approach: You need to determine if a reaction with deltaH°=+45.0 kJ and deltaS°=+125 J/K is spontaneous at both 25 deg C and 500 deg C. Walk through the correct process (don't just guess from the deltaH sign).",
    "Convert both temperatures to Kelvin: T1=298 K, T2=773 K. Convert deltaS to kJ/K: 0.125 kJ/K.<br>At T1=298K: deltaG=45.0-(298)(0.125)=45.0-37.25=+7.75 kJ (positive, NONspontaneous at 25 deg C).<br>At T2=773K: deltaG=45.0-(773)(0.125)=45.0-96.6=-51.6 kJ (negative, SPONTANEOUS at 500 deg C).<br>Answer: the reaction is nonspontaneous at 25 deg C but becomes spontaneous at 500 deg C — you must actually calculate deltaG at EACH specific temperature (since deltaH and deltaS have opposite-favorability signs here), rather than assuming the sign of deltaH alone determines spontaneity at every temperature.",
    "gibbs_free_energy", "applied")

path = os.path.join(os.path.dirname(__file__), "..", "outputs", "CHEM104_unit05_thermodynamics.txt")
n = write_tsv(cards, path)
print(f"Wrote {n} cards to {path}")
print(summarize(cards))
