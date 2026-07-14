import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import Card, write_tsv, summarize

TAG_COURSE = "chem102"
UNIT = "equilibrium_intro"
cards = []

def add(front, back, sub, kind):
    cards.append(Card(front, back, f"{TAG_COURSE} {UNIT}::{sub} {kind}"))

# ---------- CONCEPT ----------
add("What does it mean for a reaction to be 'at equilibrium'?",
    "The forward and reverse reaction rates are equal, so the concentrations of reactants and products no longer change over time (macroscopically constant), even though both reactions continue to occur microscopically — this is why it's called a dynamic equilibrium.",
    "equilibrium_basics", "concept")

add("Write the general equilibrium constant expression for the reaction aA + bB <-> cC + dD.",
    "K = [C]^c [D]^d / ([A]^a [B]^b), where brackets denote equilibrium molar concentrations and the exponents are the stoichiometric coefficients from the balanced equation.",
    "K_expressions", "concept")

add("What is the rule for including or excluding pure solids and pure liquids in an equilibrium expression?",
    "Pure solids and pure liquids (including the solvent in dilute solution, and water) are omitted from the K expression, because their concentration (activity) is effectively constant and equal to 1 by convention — they don't change as the reaction proceeds toward equilibrium.",
    "K_expressions", "concept")

add("What does it mean when K >> 1 versus K << 1?",
    "K >> 1 (large K) means at equilibrium, products are strongly favored (mostly products present). K << 1 (small K) means reactants are strongly favored (mostly reactants present, reaction barely proceeds forward).",
    "K_expressions", "concept")

add("Define the reaction quotient Q, and how it differs from K.",
    "Q has the same mathematical form as K (same expression, same exponents) but is calculated using the CURRENT (non-equilibrium, i.e., initial or any instantaneous) concentrations, whereas K uses concentrations specifically AT equilibrium. Comparing Q to K tells you which direction the reaction must shift to reach equilibrium.",
    "Q_vs_K", "concept")

add("Explain the three possible outcomes when comparing Q to K.",
    "If Q < K: not enough products yet, reaction shifts FORWARD (toward products) to reach equilibrium.<br>If Q > K: too many products already, reaction shifts REVERSE (toward reactants) to reach equilibrium.<br>If Q = K: the system is already at equilibrium, no net shift occurs.",
    "Q_vs_K", "concept")

add("What is an ICE table, and what does each row represent?",
    "An ICE table organizes an equilibrium calculation with three rows: Initial concentrations (before reaction proceeds), Change (how much each species' concentration changes, using +/-x scaled by stoichiometric coefficients), and Equilibrium (initial +/- change, the final concentrations used in the K expression).",
    "ICE_tables", "concept")

add("State Le Chatelier's Principle.",
    "If a system at equilibrium is disturbed (by a change in concentration, pressure/volume, or temperature), the system shifts in the direction that partially counteracts the disturbance, establishing a new equilibrium.",
    "le_chateliers_principle", "concept")

add("According to Le Chatelier's Principle, how does adding more reactant, and how does removing product, each affect the equilibrium position?",
    "Adding more reactant: shifts equilibrium FORWARD (toward products), consuming some of the added reactant.<br>Removing product: shifts equilibrium FORWARD (toward products) as well, since the system tries to replace the removed product.<br>Both changes push the reaction toward making more product to partially counteract the disturbance.",
    "le_chateliers_principle", "concept")

add("Why does changing temperature (unlike changing concentration or pressure) actually change the VALUE of K, not just the equilibrium position?",
    "Temperature changes affect the underlying thermodynamics of the reaction (via the relationship between K and Gibbs free energy, deltaG° = -RT ln K), effectively altering how favorable the forward vs reverse reaction is at a fundamental level. Concentration and pressure changes only shift the position (the specific concentrations at the new equilibrium) without changing K itself, because K is a constant only at a given, fixed temperature.",
    "le_chateliers_principle", "concept")

# ---------- MISCONCEPTIONS ----------
add("Misconception check: At equilibrium, are the concentrations of reactants and products necessarily equal to each other?",
    "No — equilibrium means the RATES of the forward and reverse reactions are equal, not that the concentrations themselves are equal. Concentrations at equilibrium can be very different (e.g., mostly products if K is large, or mostly reactants if K is small); what stays constant is that they no longer change over time.",
    "equilibrium_basics", "concept")

add("Misconception check: If you add a catalyst to a reaction at equilibrium, does the equilibrium position (the value of K, or the ratio of products to reactants) change?",
    "No — a catalyst speeds up BOTH the forward and reverse reactions equally, helping the system reach equilibrium faster, but it does not change the equilibrium position or the value of K. The same final equilibrium concentrations are reached either way, just faster with a catalyst.",
    "le_chateliers_principle", "concept")

add("Misconception check: If a reaction's K value is very large, does that mean the reaction happens instantaneously (fast)?",
    "No — K (equilibrium constant, thermodynamics) tells you the ratio of products to reactants once equilibrium is established; it says nothing about how FAST the system gets there (kinetics). A reaction can have a huge K (strongly favors products) yet be extremely slow to actually reach that equilibrium state without a catalyst.",
    "K_expressions", "concept")

# ---------- APPLIED ----------
add("Write the equilibrium expression for 2SO2(g) + O2(g) <-> 2SO3(g).",
    "K = [SO3]^2 / ([SO2]^2 [O2]^1).<br>Answer: K = [SO3]^2 / ([SO2]^2[O2]).",
    "K_expressions", "applied")

add("Write the equilibrium expression for the heterogeneous reaction CaCO3(s) <-> CaO(s) + CO2(g).",
    "Pure solids are omitted from the expression (CaCO3 and CaO are both solids).<br>Answer: K = [CO2] (only the gas-phase species appears).",
    "K_expressions", "applied")

add("For N2(g)+3H2(g)<->2NH3(g), Kc=0.500 at a given temperature. At a certain instant, [N2]=1.00 M, [H2]=1.00 M, [NH3]=2.00 M. Determine which direction the reaction will shift.",
    "Calculate Q: Q = [NH3]^2/([N2][H2]^3) = (2.00)^2/[(1.00)(1.00)^3] = 4.00/1.00 = 4.00.<br>Compare Q to K: Q(4.00) > K(0.500), so there is too much product relative to equilibrium.<br>Answer: the reaction shifts in REVERSE (toward reactants) to reach equilibrium.",
    "Q_vs_K", "applied")

add("For the reaction H2(g)+I2(g)<->2HI(g), Kc=54.0 at 425 deg C. If initial concentrations are [H2]=[I2]=0.200 M and [HI]=0, set up (but do not fully solve) the ICE table and equilibrium expression.",
    "ICE table:<br>Initial: [H2]=0.200, [I2]=0.200, [HI]=0.<br>Change: [H2]=-x, [I2]=-x, [HI]=+2x (matching 1:1:2 stoichiometry).<br>Equilibrium: [H2]=0.200-x, [I2]=0.200-x, [HI]=2x.<br>Equilibrium expression: Kc = (2x)^2/[(0.200-x)(0.200-x)] = 54.0.<br>This can be solved by taking the square root of both sides since both denominator terms are identical: 2x/(0.200-x) = sqrt(54.0) = 7.35, then solve for x algebraically.",
    "ICE_tables", "applied")

add("Trap: A student sets up the ICE table for 2NO2(g)<->N2O4(g) starting with initial [NO2]=0.400 M and writes the change row as -x for NO2 and +x for N2O4, ignoring stoichiometric coefficients. Identify and correct the error.",
    "The error is failing to scale the change by the stoichiometric coefficients — NO2 has a coefficient of 2, so its change must be -2x (not -x), while N2O4 (coefficient 1) correctly has change +x. Correct ICE table: Initial [NO2]=0.400, [N2O4]=0; Change [NO2]=-2x, [N2O4]=+x; Equilibrium [NO2]=0.400-2x, [N2O4]=x. Using -x instead of -2x for NO2 would systematically produce an incorrect equilibrium constant relationship and wrong final concentrations.",
    "ICE_tables", "applied")

add("Choosing the right approach: A sealed container at equilibrium contains N2(g)+3H2(g)<->2NH3(g). Predict the shift when (a) the container's volume is decreased (increasing pressure), and (b) argon gas is added at constant volume. Explain why these two are different.",
    "(a) Decreasing volume increases pressure and concentration of all gaseous species; Le Chatelier's principle says the system shifts toward the side with FEWER moles of gas to partially reduce the pressure increase. Left side has 1+3=4 moles gas, right side has 2 moles gas, so the equilibrium shifts FORWARD (toward NH3, the side with fewer gas moles).<br>(b) Adding an inert gas like argon at CONSTANT volume increases total pressure but does NOT change the partial pressures or concentrations of N2, H2, or NH3 (each species still occupies the same volume at the same concentration) — so there is NO shift in equilibrium position. The key distinction: shifting depends on changes to the concentrations/partial pressures of the actual reacting species, not on total pressure alone.",
    "le_chateliers_principle", "applied")

path = os.path.join(os.path.dirname(__file__), "..", "outputs", "CHEM102_unit10_equilibrium_intro.txt")
n = write_tsv(cards, path)
print(f"Wrote {n} cards to {path}")
print(summarize(cards))
