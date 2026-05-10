# Structural and Computational Analysis of Disease-Associated Variants in NT5C2 
**Course 22117 — Protein Structure and Computational Biology**
**Group 6**

---

## Overview

This project analyses nine missense variants of the human cytosolic 5'-nucleotidase II (NT5C2) using computational structural biology methods. NT5C2 is a purine nucleotide phosphatase involved in maintaining intracellular nucleotide pools. Loss-of-function variants are associated with hereditary spastic paraplegia (SPG45), while gain-of-function variants confer thiopurine resistance in relapsed acute lymphoblastic leukemia (ALL).

---

## Protein

| Property | Detail |
|----------|--------|
| Name | Cytosolic purine 5'-nucleotidase II |
| Gene | NT5C2 |
| UniProt | P49902 |
| Structure | PDB 2JC9 (X-ray, 1.50 Å) |
| Assembly | Homodimer |
| Cofactor | Mg²⁺ (coordinated by Asp52, Asp54, Asp351) |
| Substrates | IMP, GMP |
| Coverage | Residues 3–488 of 561 |

---

## Variants Analysed

| Variant | Position | RSA (%) | Burial | Disease Context |
|---------|----------|---------|--------|-----------------|
| K47E | 47 | 50.2 | Exposed | SPG45 (LOF) |
| R149G | 149 | 25.2 | Partially buried | SPG45 (LOF) |
| D206H | 206 | 43.2 | Partially buried | SPG45 (LOF) |
| V242L | 242 | 50.4 | Exposed | Uncertain |
| T261S | 261 | 52.5 | Exposed | Uncertain |
| S281P | 281 | 38.0 | Partially buried | SPG45 (LOF) |
| R291W | 291 | 60.7 | Exposed | ALL (GOF) |
| Q364E | 364 | 34.0 | Partially buried | Uncertain |

H522Y was excluded as position 522 lies outside the 2JC9 coverage (residues 3–488).

---

## Project Structure

The project follows the MAVISp framework and consists of four parts:

### 1 — Variant Selection and Pathogenicity Prediction
Nine variants were selected from ClinVar and UniProt. Pathogenicity was assessed using AlphaMissense (score 0–1, pathogenic > 0.564) and evolutionary conservation was evaluated using DeMask (negative score = damaging).

### 2 — Structure Selection and Preparation
PDBMiner was used to identify and rank available structures. 2JC9 was selected based on resolution (1.50 Å), R-free (0.186), zero Ramachandran outliers, and full coverage of the catalytic domain. The AlphaFold model (AF-P49902-F1-v6) was used for full-length visualisation and structural alignment (RMSD = 0.775 Å).

### 3 — Stability Analysis
Folding free energy changes (ΔΔG_stability) were calculated using MutateX/FoldX on 2JC9. Relative solvent accessibility (RSA) was computed using NACCESS.

### 4 — Local Interaction and Binding Analysis
Binding free energy changes (ΔΔG_binding) at the homodimer interface were calculated using MutateX/FoldX with the AnalyseComplex protocol on the 2JC9 biological assembly. Local contacts were analysed in PyMOL at a 4.5 Å cutoff.

---

## Classification Thresholds

```
ΔΔG > +1.0 kcal/mol  →  destabilizing
ΔΔG  -1.0 to +1.0    →  neutral
ΔΔG < -1.0 kcal/mol  →  stabilizing
```

Applied to both stability and binding free energy values.

---

## Tools Used

| Task | Tools |
|------|-------|
| Variant selection | ClinVar, UniProt, MAVISp |
| Pathogenicity | AlphaMissense, DeMask |
| Structure selection | PDBMiner, RCSB PDB, AlphaFold DB |
| Visualisation | PyMOL |
| Stability ΔΔG | MutateX, FoldX (BuildModel) |
| Binding ΔΔG | MutateX, FoldX (AnalyseComplex) |
| Solvent accessibility | NACCESS |

---

## Code and Figures

### Requirements

Python 3.8 or higher. Install dependencies:

```bash
pip install -r requirements.txt
```

### How to Run

```bash
python parse_results.py     # summary table of stability & binding
python figure_groupBar.py   # grouped bar chart
python figure_heatMap.py    # integrative summary heatmap
```
### PyMOL Sessions

The following PyMOL session files (.pse) can be opened directly in PyMOL to reproduce the figures.

**figure1_alignment.pse** — Structural alignment of AF-P49902-F1-v6 onto 2JC9.
Open in PyMOL to view the alignment with 2JC9 (gray), AlphaFold core (orange), and C-terminal region (magenta).

Commands used to generate this session:

```pymol
reinitialize
fetch 2JC9, async=0
load AF.pdb
align AF, 2JC9
hide everything
show cartoon
color gray70, 2JC9
color tv_orange, AF
select AF_cterminal, AF and resi 401-561
color magenta, AF_cterminal
bg_color white
set ray_opaque_background, on
orient all
```

**figur2_plddt.pse** — AlphaFold model coloured by pLDDT confidence score.
Open in PyMOL to view confidence map from red (low) to blue (high).

Commands used to generate this session:

```pymol
reinitialize
load AF.pdb
spectrum b, red_yellow_cyan_blue, AF
bg_color white
set ray_opaque_background, on
orient AF
```

### Structure Preparation

**2JC9_clean.pdb** — Cleaned structure used for stability calculations.
Water molecules, glycerol, sulfate ions, and adenosine removed. Magnesium ion retained.

```pymol
fetch 2JC9, async=0
remove resn HOH
remove resn GOL
remove resn SO4
remove resn ADN
save 2JC9_clean.pdb
```

### Folder Structure

```
nt5c2/
├── parse_results.py
├── figure_groupBar.py
├── figure_heatMap.py
├── figur2_plddt.pse
├── figure1_alignment.pse
├── 2JC9_clean.pdb
├── AF.pdb
├── requirements.txt
├── README.md
└── data/
    ├── stability/
    │   ├── energies.csv      # ΔΔG stability
    │   └── 2JC9_clean.rsa    # RSA values
    └── binding/
        └── energies.csv      # ΔΔG binding
```

---

## Server

All calculations were performed on DTU pupil2 server:
```
pupil2.healthtech.dtu.dk
/home/projects/22117_protein_structure/projects/group6/
```

---

## Team

| Member | Task |
|--------|------|
| Humaira Fatima Amin (s235423) | Variant selection and pathogenicity |
| Aisha Osman Ali (s250697) | Structure selection and preparation |
| Sabah Khan (s180383) | Stability analysis |
| Trang Nguyen (s250150) | Local interaction and binding analysis |
