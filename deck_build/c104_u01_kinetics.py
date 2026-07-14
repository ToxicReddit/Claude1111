import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import Card, write_tsv, summarize

TAG_COURSE = "chem104"
UNIT = "kinetics"
cards = []

def add(front, back, sub, kind):
    cards.append(Card(front, back, f"{TAG_COURSE} {UNIT}::{sub} {kind}"))

# ---------- CONCEPT ----------
add("Define reaction rate, and give the general expression relating it to concentration change over time.",
    "Reaction rate is the change in concentration of a reactant or product per unit time. General form: rate = -(1/a)(d[A]/dt) = (1/c)(d[C]/dt) for aA -> cC, where the negative sign for reactants reflects their decreasing concentration, and dividing by stoichiometric coefficients gives a single consistent rate value.",
    "rate_basics", "concept")

add("What is a rate law, and what do 'm' and 'n' represent in rate = k[A]^m[B]^n?",
    "A rate law expresses reaction rate as a function of reactant concentrations. k is the rate constant (specific to the reaction and temperature). m and n are the reaction orders with respect to A and B respectively — they must be determined EXPERIMENTALLY and are not necessarily equal to the stoichiometric coefficients in the balanced equation.",
    "rate_laws", "concept")

add("Why can't reaction orders (m, n in the rate law) simply be read off from the balanced chemical equation's coefficients?",
    "Reaction order reflects the actual molecular-level mechanism (how many of each species participate in the rate-determining step), which is often different from the overall stoichiometry of the net balanced equation (which just reflects mass balance for the overall reaction, not the rate-determining elementary step). Only for a reaction that occurs in a single elementary step do coefficients equal reaction orders; for multi-step mechanisms, orders must be found from experimental rate data.",
    "rate_laws", "concept")

add("Give the integrated rate law and half-life formula for a zero-order reaction.",
    "Integrated rate law: [A] = -kt + [A]0 (linear in [A] vs t, slope = -k).<br>Half-life: t_(1/2) = [A]0 / (2k) — half-life DEPENDS on initial concentration.",
    "integrated_rate_laws", "concept")

add("Give the integrated rate law and half-life formula for a first-order reaction.",
    "Integrated rate law: ln[A] = -kt + ln[A]0 (linear in ln[A] vs t, slope = -k).<br>Half-life: t_(1/2) = ln(2)/k = 0.693/k — half-life is CONSTANT, independent of initial concentration.",
    "integrated_rate_laws", "concept")

add("Give the integrated rate law and half-life formula for a second-order reaction.",
    "Integrated rate law: 1/[A] = kt + 1/[A]0 (linear in 1/[A] vs t, slope = +k).<br>Half-life: t_(1/2) = 1/(k[A]0) — half-life depends on initial concentration (increases as [A]0 decreases, opposite trend from zero-order).",
    "integrated_rate_laws", "concept")

add("How can you determine reaction order graphically from concentration-vs-time data?",
    "Plot [A] vs t, ln[A] vs t, and 1/[A] vs t. Whichever plot is LINEAR (straight line) indicates the reaction order: linear [A] vs t = zero order; linear ln[A] vs t = first order; linear 1/[A] vs t = second order. The slope of the correct linear plot also gives the rate constant k (with appropriate sign).",
    "integrated_rate_laws", "concept")

add("State the Arrhenius equation and define every variable.",
    "k = A * e^(-Ea/RT), where k = rate constant, A = frequency/pre-exponential factor (collision frequency and orientation factor), Ea = activation energy (J/mol), R = gas constant (8.314 J/(mol*K)), and T = absolute temperature (K).",
    "arrhenius_equation", "concept")

add("Why does increasing temperature increase the rate constant k, according to collision theory and the Arrhenius equation?",
    "Increasing temperature increases the average kinetic energy of molecules, so a larger fraction of collisions have enough energy to exceed the activation energy (Ea) barrier. In the Arrhenius equation, higher T makes the exponent -Ea/RT less negative, making e^(-Ea/RT) larger, so k increases. This does NOT change Ea or the mechanism — it changes how many molecules have sufficient energy to react.",
    "arrhenius_equation", "concept")

add("What is the two-point (linearized) form of the Arrhenius equation used to find Ea from rate constants at two temperatures?",
    "ln(k2/k1) = -(Ea/R)(1/T2 - 1/T1), or equivalently ln(k1/k2) = (Ea/R)(1/T2-1/T1). This lets you solve for Ea if k is known at two different temperatures T1 and T2, without needing to know A.",
    "arrhenius_equation", "concept")

add("What is a reaction mechanism, and what is an elementary step?",
    "A reaction mechanism is the sequence of elementary steps (simple, single-molecular-event reactions) that together add up to the overall balanced reaction. Each elementary step's rate law CAN be written directly from its stoichiometry (unlike the overall reaction), because it represents an actual single molecular collision/event.",
    "mechanisms", "concept")

add("What is the rate-determining step, and how does it relate to the overall rate law of a multi-step mechanism?",
    "The rate-determining step (RDS) is the SLOWEST elementary step in a mechanism, which acts as a bottleneck controlling the overall reaction rate. The overall experimental rate law typically matches the rate law of the rate-determining step (adjusted for any fast pre-equilibrium steps before it using the steady-state or pre-equilibrium approximation).",
    "mechanisms", "concept")

add("What is a catalyst, and how does it increase reaction rate without being consumed?",
    "A catalyst provides an alternative reaction pathway (mechanism) with a LOWER activation energy than the uncatalyzed pathway. It participates in the reaction (e.g., binding a reactant, forming an intermediate) but is regenerated by the end of the reaction, so it is not permanently consumed and does not appear in the overall balanced equation.",
    "catalysis", "concept")

add("Distinguish homogeneous catalysis from heterogeneous catalysis, and from an enzyme's role as a biological catalyst.",
    "Homogeneous catalysis: catalyst is in the same phase as the reactants (e.g., dissolved in the same solution). Heterogeneous catalysis: catalyst is in a different phase (commonly a solid catalyst with gas or liquid-phase reactants, reaction occurring at the catalyst's surface, e.g., catalytic converters). Enzymes are biological catalysts (usually proteins) that dramatically lower Ea for specific biochemical reactions via a specific active site, functioning similarly in principle to other catalysts (lowering Ea, not consumed) but with high substrate specificity.",
    "catalysis", "concept")

# ---------- MISCONCEPTIONS ----------
add("Misconception check: Does doubling the concentration of a reactant always double the reaction rate?",
    "Only if the reaction is FIRST ORDER with respect to that reactant. If zero order in that reactant, rate is unaffected by its concentration; if second order, doubling concentration quadruples the rate (since rate depends on [A]^2). The effect of concentration on rate depends entirely on the experimentally determined reaction order, not a universal doubling rule.",
    "rate_laws", "concept")

add("Misconception check: Does a catalyst change the value of Keq (the equilibrium constant) for a reaction, since it speeds things up?",
    "No — a catalyst speeds up both the forward AND reverse reactions equally by lowering Ea for both directions via the same alternate pathway, so the equilibrium position (and K) is unaffected. It only helps the system reach the same equilibrium state faster (a kinetics effect), not a thermodynamics effect.",
    "catalysis", "concept")

add("Misconception check: Is the half-life of a reaction always a fixed, constant value regardless of reaction order?",
    "No — half-life behavior depends on order. Only FIRST-ORDER reactions have a constant half-life independent of concentration (t_1/2 = 0.693/k). Zero-order half-life DECREASES as concentration decreases (t_1/2 = [A]0/2k, proportional to [A]0), and second-order half-life INCREASES as concentration decreases (t_1/2 = 1/(k[A]0), inversely proportional to [A]0).",
    "integrated_rate_laws", "concept")

# ---------- APPLIED ----------
add("For the reaction 2A + B -> C, doubling [A] (with [B] constant) quadruples the rate; doubling [B] (with [A] constant) has no effect on rate. Determine the rate law.",
    "Doubling [A] quadruples rate: 2^m = 4 -> m = 2 (second order in A).<br>Doubling [B] has no effect: 2^n = 1 -> n = 0 (zero order in B).<br>Answer: rate = k[A]^2[B]^0 = k[A]^2. Overall reaction order = 2 (second order overall).",
    "rate_laws", "applied")

add("A first-order reaction has a rate constant k = 0.0347 s^-1. Calculate its half-life.",
    "t_1/2 = 0.693/k = 0.693/0.0347 s^-1 = 19.97 s.<br>Answer: t_1/2 ~ 20.0 s.",
    "integrated_rate_laws", "applied")

add("A first-order reaction starts with [A]0 = 0.500 M and has k = 0.0250 min^-1. Find [A] after 45.0 minutes.",
    "Use ln[A] = -kt + ln[A]0.<br>ln[A] = -(0.0250 min^-1)(45.0 min) + ln(0.500) = -1.125 + (-0.693) = -1.818.<br>[A] = e^(-1.818) = 0.1624 M.<br>Answer: [A] ~ 0.162 M after 45.0 minutes.",
    "integrated_rate_laws", "applied")

add("A reaction has k=0.0125 M^-1s^-1 at 300 K and Ea=75.0 kJ/mol. Find k at 350 K.",
    "Use the two-point Arrhenius equation: ln(k2/k1) = -(Ea/R)(1/T2 - 1/T1).<br>ln(k2/0.0125) = -(75000 J/mol / 8.314 J/mol*K)(1/350 - 1/300)<br>= -(9021.9)(0.002857 - 0.003333) = -(9021.9)(-0.000476) = 4.296.<br>k2/0.0125 = e^4.296 = 73.4.<br>k2 = 0.0125 x 73.4 = 0.918 M^-1s^-1.<br>Answer: k2 ~ 0.918 M^-1 s^-1 at 350 K (much faster, as expected with higher T).",
    "arrhenius_equation", "applied")

add("A proposed mechanism for 2NO(g)+O2(g)->2NO2(g) is: Step 1 (fast, reversible): 2NO <-> N2O2; Step 2 (slow): N2O2+O2 -> 2NO2. Determine the overall rate law implied by this mechanism.",
    "Since step 2 is the rate-determining (slow) step, its elementary rate law is rate = k2[N2O2][O2]. But N2O2 is a reactive intermediate — not a reactant we can measure directly — so we must substitute using the fast pre-equilibrium in step 1: K1 = [N2O2]/[NO]^2, so [N2O2] = K1[NO]^2.<br>Substituting: rate = k2*K1*[NO]^2*[O2] = k_obs[NO]^2[O2], where k_obs = k2*K1.<br>Answer: rate = k[NO]^2[O2] (second order in NO, first order in O2, third order overall) — matching the experimentally observed rate law for this classic reaction.",
    "mechanisms", "applied")

add("Trap: A student is given the rate law rate=k[NO]^2[O2] for 2NO(g)+O2(g)->2NO2(g) and assumes this must be a single-step (termolecular) elementary reaction because the rate law 'matches' the stoichiometric coefficients (2 and 1). Explain the flaw in this reasoning.",
    "The flaw is assuming a matching rate law and stoichiometry PROVES a single-step mechanism — it does not. A rate law matching overall stoichiometry is consistent with (but does not prove) a single elementary step; it is equally consistent with certain multi-step mechanisms (like the fast pre-equilibrium mechanism shown in another card) that happen to produce the same overall rate law after algebraic substitution. True termolecular (three-body) elementary collisions are actually quite rare because the odds of three particles colliding simultaneously with correct orientation and energy are low. Additional evidence (e.g., detection of intermediates, more detailed kinetic studies) is needed to establish the true mechanism, not just matching orders.",
    "mechanisms", "applied")

add("Choosing the right approach: A student has concentration-vs-time data for a reactant and doesn't know the reaction order. Describe how they should determine the order and find k, without assuming order from the reaction's coefficients.",
    "Plot the data three ways: [A] vs t, ln[A] vs t, and 1/[A] vs t. Whichever gives a straight line (best linear fit, high R^2) reveals the true order: linear [A] vs t means zero order (k = -slope); linear ln[A] vs t means first order (k = -slope); linear 1/[A] vs t means second order (k = +slope). This graphical method uses experimental data directly and does not rely on (and should never simply assume) the balanced equation's stoichiometric coefficients, since order must be determined empirically.",
    "integrated_rate_laws", "applied")

path = os.path.join(os.path.dirname(__file__), "..", "outputs", "CHEM104_unit01_kinetics.txt")
n = write_tsv(cards, path)
print(f"Wrote {n} cards to {path}")
print(summarize(cards))
