import os
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

ENERGIES_CSV = os.path.join(DATA, "stability/energies.csv")
BINDING_ENERGIES_CSV = os.path.join(DATA, "binding/energies.csv")
RSA_FILE = os.path.join(DATA, "stability/2JC9_clean.rsa")

VARIANTS = {
    "K47E": (47, "E"),
    "R149G": (149, "G"),
    "D206H": (206, "H"),
    "V242L": (242, "L"),
    "T261S": (261, "S"),
    "S281P": (281, "P"),
    "R291W": (291, "W"),
    "Q364E": (364, "E"),
}


def classify(ddg):
    if ddg > 1.0:
        return "destabilizing"
    if ddg < -1.0:
        return "stabilizing"
    return "neutral"


def get_stability_ddg():
    df = pd.read_csv(ENERGIES_CSV)
    results = {}
    for name, (resnum, mut_aa) in VARIANTS.items():
        row = df[df["Residue #"] == resnum].iloc[0]
        results[name] = float(row[mut_aa])
    return results


def get_binding_ddg():
    df = pd.read_csv(BINDING_ENERGIES_CSV)
    results = {}
    for name, (resnum, mut_aa) in VARIANTS.items():
        row = df[df["Residue #"] == resnum].iloc[0]
        results[name] = float(row[mut_aa])
    return results


def get_rsa_values():
    # Parse NACCESS .rsa output — column index 5 is All-atoms REL (%)
    target_resnums = {v[0] for v in VARIANTS.values()}
    rsa_map = {}
    with open(RSA_FILE) as f:
        for line in f:
            if not line.startswith("RES"):
                continue
            parts = line.split()
            try:
                resnum = int(parts[3])
                rel = float(parts[5])
                if resnum in target_resnums:
                    rsa_map[resnum] = rel
            except:
                pass
    return {name: rsa_map.get(resnum) for name, (resnum, _) in VARIANTS.items()}


if __name__ == "__main__":
    stability = get_stability_ddg()
    binding = get_binding_ddg()
    rsa = get_rsa_values()

    print(
        f"\n{'Variant':<10} {'DDG_stab':>12} {'Stab_class':<16} {'RSA%':>7} {'Burial':<20} {'DDG_bind':>12} {'Bind_class'}"
    )
    print("-" * 95)

    for name in VARIANTS:
        ddg_s = stability[name]
        ddg_b = binding[name]
        rsa_v = rsa[name]
        burial = (
            "exposed"
            if rsa_v > 50
            else ("partially buried" if rsa_v > 25 else "buried")
        )

        print(
            f"{name:<10} {ddg_s:>12.4f} {classify(ddg_s):<16} {rsa_v:>7.1f} {burial:<20} {ddg_b:>12.4f} {classify(ddg_b)}"
        )
