import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from helpers import Card, write_tsv, summarize

TAG_COURSE = "chem102"
UNIT = "molecular_geometry"
cards = []

def add(front, back, sub, kind):
    cards.append(Card(front, back, f"{TAG_COURSE} {UNIT}::{sub} {kind}"))

# ---------- CONCEPT ----------
add("What is the core idea behind VSEPR theory?",
    "Valence Shell Electron Pair Repulsion theory states that electron groups (bonding pairs and lone pairs) around a central atom arrange themselves as far apart as possible to minimize electrostatic repulsion, which determines the molecule's geometry.",
    "vsepr", "concept")

add("List the electron-group geometries for 2, 3, 4, 5, and 6 electron groups around a central atom.",
    "2 groups: linear (180 deg).<br>3 groups: trigonal planar (120 deg).<br>4 groups: tetrahedral (109.5 deg).<br>5 groups: trigonal bipyramidal (90/120/180 deg).<br>6 groups: octahedral (90 deg).",
    "vsepr", "concept")

add("Why does a lone pair compress bond angles more than a bonding pair does (e.g., water's H-O-H angle is 104.5 deg, less than the tetrahedral 109.5 deg)?",
    "A lone pair is held only by the central atom's nucleus and occupies more space (is 'fatter') than a bonding pair, which is shared and pulled between two nuclei. This means lone pair-bonding pair repulsion is stronger than bonding pair-bonding pair repulsion, pushing the bonding pairs closer together and compressing the bond angle below the ideal geometric value.",
    "vsepr", "concept")

add("Distinguish 'electron-group geometry' from 'molecular geometry.' Use NH3 as an example.",
    "Electron-group geometry describes the arrangement of all electron groups (bonds + lone pairs), while molecular geometry describes only the arrangement of the atoms (ignoring lone pairs, though they still influence the shape). For NH3: electron-group geometry is tetrahedral (3 bonds + 1 lone pair = 4 groups), but molecular geometry is trigonal pyramidal (only the 3 N-H bonds define the observed atomic shape).",
    "vsepr", "concept")

add("What is hybridization, and why is it invoked to explain molecular bonding?",
    "Hybridization is the mixing of atomic orbitals (s, p, d) on a central atom to form a new set of equivalent hybrid orbitals suited to the observed molecular geometry. It's invoked because pure atomic s and p orbitals alone often can't explain the observed bond angles (e.g., pure p orbitals at 90 deg don't match a tetrahedral 109.5 deg carbon).",
    "hybridization", "concept")

add("Match hybridization to number of electron groups: sp, sp2, sp3, sp3d, sp3d2.",
    "sp: 2 electron groups (linear). sp2: 3 electron groups (trigonal planar). sp3: 4 electron groups (tetrahedral). sp3d: 5 electron groups (trigonal bipyramidal). sp3d2: 6 electron groups (octahedral).",
    "hybridization", "concept")

add("What is the difference between a sigma bond and a pi bond?",
    "A sigma bond forms from head-on (end-to-end) orbital overlap along the bond axis, allowing free rotation; it is the first bond in any single, double, or triple bond. A pi bond forms from sideways overlap of parallel unhybridized p orbitals above/below the bond axis, restricting rotation; double bonds have 1 pi bond, triple bonds have 2 pi bonds.",
    "hybridization", "concept")

add("Why can't atoms freely rotate around a double bond, but they can around a single bond?",
    "A double bond contains a pi bond formed by sideways overlap of parallel p orbitals. Rotating one end of the molecule would misalign these p orbitals and break the pi bond's overlap, which costs a large amount of energy. A single (sigma-only) bond has cylindrically symmetric end-to-end overlap along the bond axis, so rotation doesn't disrupt orbital overlap and costs very little energy.",
    "hybridization", "concept")

add("What determines whether a molecule is polar overall, given that it may contain polar bonds?",
    "Overall molecular polarity depends on both (1) the presence of polar bonds (bond dipoles from electronegativity differences) and (2) the molecular geometry/symmetry. If bond dipoles are arranged symmetrically, they can cancel (vector sum = 0), making the molecule nonpolar overall even if individual bonds are polar. If the arrangement is asymmetric (including from lone pairs), the dipoles do not cancel and the molecule is polar.",
    "polarity", "concept")

add("Why is CO2 a nonpolar molecule even though each C=O bond is significantly polar?",
    "CO2 is linear (180 deg) with two identical, oppositely-directed C=O bond dipoles. Because the geometry is symmetric and the two bond dipoles are equal in magnitude and point in exactly opposite directions, their vector sum is zero — the bond dipoles cancel, making the overall molecule nonpolar despite having polar bonds.",
    "polarity", "concept")

# ---------- MISCONCEPTIONS ----------
add("Misconception check: Does a molecule with only nonpolar bonds (identical atoms bonded) always have zero net dipole, and is that the only way to get a nonpolar molecule?",
    "Identical-atom bonds (like O2 or N2) are indeed nonpolar, but symmetric arrangement of polar bonds can ALSO cancel to give an overall nonpolar molecule (e.g., CO2, CCl4) even though every individual bond is polar. So molecular nonpolarity can arise either from nonpolar bonds or from symmetric cancellation of polar bond dipoles — not only from having zero individual bond polarity.",
    "polarity", "concept")

add("Misconception check: Is molecular geometry (the shape you'd draw/observe) the same thing as electron-group (electron-domain) geometry whenever there are lone pairs present?",
    "No — they differ whenever lone pairs are present. Electron-group geometry accounts for all electron groups (bonds + lone pairs); molecular geometry describes only the positions of the actual atoms. For example, water has tetrahedral electron-group geometry but bent molecular geometry, because 2 of the 4 electron groups are lone pairs that are not 'seen' in the atom-based molecular shape.",
    "vsepr", "concept")

# ---------- APPLIED ----------
add("Predict the electron-group geometry, molecular geometry, hybridization, and polarity of SF4 (sulfur tetrafluoride).",
    "Step 1 - count electron groups on S: 4 bonding pairs (to F) + 1 lone pair = 5 groups.<br>Step 2 - electron-group geometry: trigonal bipyramidal (5 groups).<br>Step 3 - molecular geometry: with 1 lone pair in an equatorial position (minimizing 90 deg lone pair repulsions), the shape is 'seesaw'.<br>Step 4 - hybridization: sp3d (5 groups).<br>Step 5 - polarity: the lone pair creates an asymmetric charge distribution, so the bond dipoles do not cancel -> SF4 is polar.<br>Answer: electron-group geometry trigonal bipyramidal, molecular geometry seesaw, sp3d hybridization, polar.",
    "vsepr", "applied")

add("Determine the molecular geometry and bond angle around the central atom in BF3, and state whether it is polar.",
    "Step 1 - count electron groups on B: 3 bonding pairs, 0 lone pairs = 3 groups.<br>Step 2 - electron-group geometry = molecular geometry here (no lone pairs): trigonal planar, ~120 deg bond angles.<br>Step 3 - hybridization: sp2.<br>Step 4 - polarity: 3 identical, symmetric B-F bond dipoles at 120 deg to each other cancel exactly (vector sum = 0) -> BF3 is nonpolar overall, despite each B-F bond being quite polar.<br>Answer: trigonal planar, ~120 deg, nonpolar (bond dipoles cancel by symmetry).",
    "polarity", "applied")

add("For the molecule XeF4, determine the number of electron groups, electron-group geometry, and molecular geometry.",
    "Total valence electrons around Xe: Xe has 8 valence e-, contributes 4 bonds to 4 F (using 4 electrons) leaving 4 electrons = 2 lone pairs on Xe. Total electron groups on Xe = 4 bonding + 2 lone pair = 6 groups.<br>Electron-group geometry (6 groups): octahedral.<br>Molecular geometry: with 2 lone pairs placed opposite each other (180 deg apart, minimizing repulsion), the 4 F atoms form a square planar molecular geometry.<br>Answer: 6 electron groups, octahedral electron-group geometry, square planar molecular geometry, sp3d2 hybridization.",
    "vsepr", "applied")

add("Trap: A student says NH3 and BF3 should have the same molecular geometry because both have a central atom bonded to 3 other atoms. Explain why this is wrong.",
    "Counting only the bonded atoms ignores lone pairs, which is the key error. BF3's B has 3 bonding pairs and 0 lone pairs (3 total electron groups) giving trigonal planar geometry. NH3's N has 3 bonding pairs PLUS 1 lone pair (4 total electron groups), giving tetrahedral electron-group geometry but trigonal PYRAMIDAL molecular geometry (not planar) because the lone pair pushes the N-H bonds down and compresses the H-N-H angle to ~107 deg (versus BF3's ~120 deg). You must count lone pairs, not just bonded atoms, to determine geometry correctly.",
    "vsepr", "applied")

add("Choosing the right approach: Is SO2 polar or nonpolar? Walk through the correct method rather than guessing from the formula alone.",
    "Don't just compare to CO2 by formula similarity — analyze S's actual electron groups. S in SO2 has 2 bonding groups (to each O, counting each double bond as one electron group) plus 1 lone pair = 3 total electron groups, giving trigonal planar electron-group geometry but BENT molecular geometry (~119 deg), analogous to ozone. Because of the bent shape, the two S=O bond dipoles do NOT point in exactly opposite directions, so they do not cancel. SO2 is polar — unlike the linear, nonpolar CO2, even though both have an 'AX2' formula pattern, the lone pair on S changes everything.",
    "polarity", "applied")

add("A molecule has a central atom with sp3d2 hybridization and 2 lone pairs positioned opposite each other. What is the resulting molecular geometry, and give an example molecule.",
    "sp3d2 hybridization corresponds to an octahedral electron-group geometry (6 groups total). Removing 2 lone pairs (placed at opposite/axial positions to minimize repulsion) from the 6 positions leaves 4 bonding positions in a plane -> square planar molecular geometry.<br>Answer: square planar; example: XeF4.",
    "hybridization", "applied")

path = os.path.join(os.path.dirname(__file__), "..", "outputs", "CHEM102_unit05_molecular_geometry.txt")
n = write_tsv(cards, path)
print(f"Wrote {n} cards to {path}")
print(summarize(cards))
