import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import Card, write_tsv, summarize

TAG_COURSE = "chem104"
UNIT = "intro_organic"
cards = []

def add(front, back, sub, kind):
    cards.append(Card(front, back, f"{TAG_COURSE} {UNIT}::{sub} {kind}"))

# ---------- CONCEPT ----------
add("What is a functional group, and why are they central to organic chemistry?",
    "A functional group is a specific arrangement of atoms within a molecule responsible for characteristic chemical reactions and properties. They are central because molecules with the same functional group tend to undergo similar reactions regardless of the rest of the (often large) carbon skeleton, letting chemists predict reactivity from a relatively small set of recognizable patterns.",
    "functional_groups", "concept")

add("Identify the functional group and general formula for: alcohol, aldehyde, ketone, carboxylic acid.",
    "Alcohol: -OH attached to a carbon chain (R-OH).<br>Aldehyde: carbonyl (C=O) at the END of a chain, bonded to at least one H (R-CHO).<br>Ketone: carbonyl (C=O) in the MIDDLE of a chain, bonded to two carbon groups (R-CO-R').<br>Carboxylic acid: -COOH, a carbonyl carbon also bonded to an -OH (R-COOH).",
    "functional_groups", "concept")

add("Identify the functional group and general formula for: amine, ester, ether.",
    "Amine: nitrogen bonded to one or more carbon groups (R-NH2, R2NH, or R3N), analogous to ammonia with H's replaced by carbon groups.<br>Ester: R-CO-O-R' (a carbonyl carbon bonded to an -O- that connects to another carbon group; commonly formed from a carboxylic acid + alcohol).<br>Ether: R-O-R' (an oxygen atom bonded to two separate carbon groups, no carbonyl).",
    "functional_groups", "concept")

add("What distinguishes an alkane, alkene, and alkyne (hydrocarbon classes)?",
    "Alkanes contain only single (sigma) C-C bonds (general formula CnH2n+2, 'saturated'). Alkenes contain at least one C=C double bond (general formula CnH2n for one double bond). Alkynes contain at least one C#C triple bond (general formula CnH2n-2 for one triple bond).",
    "hydrocarbon_nomenclature", "concept")

add("What do the prefixes meth-, eth-, prop-, but-, pent-, hex- indicate in IUPAC nomenclature?",
    "They indicate the number of carbon atoms in the main (longest continuous) chain: meth-=1, eth-=2, prop-=3, but-=4, pent-=5, hex-=6. These are combined with a suffix (-ane, -ene, -yne, -ol, etc.) to indicate both chain length and functional group/bonding type.",
    "hydrocarbon_nomenclature", "concept")

add("What do the suffixes -ane, -ene, -yne, -ol, -al, -one, -oic acid indicate in IUPAC nomenclature?",
    "-ane: all single bonds (alkane). -ene: contains a C=C double bond (alkene). -yne: contains a C#C triple bond (alkyne). -ol: contains an -OH (alcohol). -al: contains a terminal aldehyde (-CHO). -one: contains a ketone (internal C=O). -oic acid: contains a carboxylic acid (-COOH).",
    "hydrocarbon_nomenclature", "concept")

add("Why do carboxylic acids (R-COOH) act as weak Bronsted-Lowry acids, connecting this topic back to acid-base chemistry?",
    "The O-H bond in the -COOH group is polarized and made more acidic than a typical alcohol O-H because the resulting carboxylate anion (R-COO-) is stabilized by resonance — the negative charge is delocalized over both oxygen atoms rather than localized on just one, making the anion (conjugate base) unusually stable, which favors the forward (proton-donating) ionization compared to alcohols, where no such resonance stabilization exists in the resulting alkoxide anion.",
    "functional_groups", "concept")

add("At a basic level, what are the three main classes of biomolecules typically introduced (carbohydrates, proteins, and lipids), and their defining structural feature?",
    "Carbohydrates: built from monosaccharide (sugar) units, characterized by many -OH groups and a carbonyl (aldehyde or ketone) group (e.g., glucose). Proteins: polymers of amino acids linked by amide (peptide) bonds, each amino acid containing both an amine (-NH2) and a carboxylic acid (-COOH) group. Lipids: largely nonpolar, hydrocarbon-rich molecules (e.g., fatty acids, which are long hydrocarbon chains ending in a carboxylic acid group), generally insoluble in water due to their nonpolar character.",
    "intro_biomolecules", "concept")

# ---------- MISCONCEPTIONS ----------
add("Misconception check: Are an aldehyde and a ketone the same functional group, just written differently, since both contain a C=O (carbonyl)?",
    "No — while both contain a carbonyl (C=O), their POSITION differs: an aldehyde's carbonyl carbon is at the END of the chain (bonded to at least one hydrogen, R-CHO), while a ketone's carbonyl carbon is in the MIDDLE of the chain (bonded to two carbon-containing groups, R-CO-R', no H directly on the carbonyl carbon). This positional difference gives them distinct reactivity patterns and names (aldehydes are generally easier to oxidize further than ketones, for example).",
    "functional_groups", "concept")

add("Misconception check: Is a carboxylic acid (R-COOH) as strong an acid as a typical strong mineral acid like HCl?",
    "No — carboxylic acids are WEAK acids (they only partially ionize in water, with typical Ka values around 10^-4 to 10^-5), unlike strong acids like HCl which ionize essentially completely. The resonance stabilization of the carboxylate anion makes carboxylic acids MORE acidic than simple alcohols, but still far weaker than strong mineral acids.",
    "functional_groups", "concept")

add("Misconception check: Does 'saturated' in the context of hydrocarbons (like saturated fats) refer to being saturated with water, similar to a saturated solution?",
    "No — in organic chemistry, 'saturated' refers to a carbon chain containing only single bonds (fully 'saturated' with hydrogen atoms, i.e., an alkane, the maximum possible number of H atoms for that number of carbons). This is an entirely different meaning from 'saturated' in the context of solutions (a solution holding the maximum dissolved solute at equilibrium) — the same word describes unrelated concepts in these two contexts.",
    "hydrocarbon_nomenclature", "concept")

# ---------- APPLIED ----------
add("Identify the functional group(s) present in the molecule CH3-CH2-COOH (propanoic acid), and classify the compound.",
    "The -COOH group at the end of the chain is a carboxylic acid functional group. The compound is a carboxylic acid (specifically propanoic acid, a 3-carbon carboxylic acid).<br>Answer: carboxylic acid functional group; the compound is propanoic acid, a weak organic acid.",
    "functional_groups", "applied")

add("Name the following compound using IUPAC rules: CH3-CH2-CH2-CH3 with a double bond between carbons 1 and 2 (CH2=CH-CH2-CH3).",
    "4 carbons in the main chain = 'but-' prefix. Contains one C=C double bond = '-ene' suffix. The double bond starts at carbon 1 (lowest possible locant, numbering from the end nearest the double bond).<br>Answer: 1-butene (or but-1-ene).",
    "hydrocarbon_nomenclature", "applied")

add("Trap: A student is asked to classify CH3-CO-CH3 (acetone) and calls it an aldehyde because it 'has a C=O group like formaldehyde.' Correct this classification.",
    "This is incorrect — simply having a C=O (carbonyl) is not enough to identify the specific functional group; POSITION matters. In CH3-CO-CH3, the carbonyl carbon is bonded to TWO carbon groups (both CH3 groups) with no H directly attached to the carbonyl carbon, placing the carbonyl in the MIDDLE of the molecule — this is the defining feature of a KETONE, not an aldehyde. An aldehyde would require the carbonyl carbon to be at the end of the chain with at least one H directly attached (like H-CHO in formaldehyde, or CH3-CHO in acetaldehyde). Acetone is correctly classified as a ketone.",
    "functional_groups", "applied")

add("A carboxylic acid (Ka=1.8x10^-5, similar to acetic acid) at 0.100 M is compared to a simple alcohol at the same concentration. Explain, using resonance, why the carboxylic acid solution has a measurably acidic pH while the alcohol solution is essentially neutral, even though both contain an O-H bond.",
    "When the carboxylic acid loses its O-H proton, the resulting carboxylate anion (R-COO-) has its negative charge delocalized (via resonance) equally over BOTH oxygen atoms of the former -COOH group, significantly stabilizing the anion and making the forward ionization (donating H+) favorable enough to measurably shift the equilibrium and produce a noticeably acidic pH (e.g., pH~2.9 for 0.100 M acetic acid, from the earlier acid-base ICE calculation method). In contrast, when a simple alcohol loses its O-H proton, the resulting alkoxide anion (R-O-) has no comparable resonance stabilization (the negative charge is localized on a single oxygen), making that ionization far less favorable (Ka roughly 10^-16 to 10^-18, vastly smaller) — so alcohols behave as such weak acids that their solutions are essentially neutral (indistinguishable from pure water) under typical conditions.",
    "functional_groups", "applied")

add("Choosing the right approach: You are given an unlabeled organic molecule and asked to identify its functional group(s) as a first step before predicting its reactivity. Outline the systematic approach rather than guessing.",
    "Do not guess based on overall molecule size or a superficial resemblance to a known compound. Instead: (1) scan the structure for any C=O (carbonyl) group, and if found, determine its position and neighboring atoms (end-of-chain with an H attached = aldehyde; between two carbons = ketone; attached to -OH = carboxylic acid; attached to -O-R = ester); (2) if no carbonyl, check for an isolated -OH group on a carbon chain = alcohol; (3) check for -O- between two carbon groups with no carbonyl = ether; (4) check for nitrogen bonded to carbon group(s) = amine; (5) check the carbon skeleton itself for double or triple C-C bonds if no heteroatom-based functional group is present (alkene/alkyne) versus all single bonds (alkane). Systematically checking for each functional group pattern (rather than pattern-matching to a memorized 'famous' molecule) ensures correct identification even for unfamiliar structures.",
    "functional_groups", "applied")

path = os.path.join(os.path.dirname(__file__), "..", "outputs", "CHEM104_unit07_intro_organic.txt")
n = write_tsv(cards, path)
print(f"Wrote {n} cards to {path}")
print(summarize(cards))
