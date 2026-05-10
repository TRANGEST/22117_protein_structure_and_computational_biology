import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from parse_results import get_stability_ddg, get_binding_ddg, classify

VARIANTS = ["K47E", "R149G", "D206H", "V242L", "T261S", "S281P", "R291W", "Q364E"]
OUTPUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "figure_groupBar.png",
)


def bar_color(ddg):
    if ddg is None:
        return "#cccccc"
    if ddg > 1.0:
        return "#e74c3c"
    if ddg < -1.0:
        return "#2ecc71"
    return "#95a5a6"


if __name__ == "__main__":
    stability = get_stability_ddg()
    binding = get_binding_ddg()

    ddg_s = [stability[v] for v in VARIANTS]
    ddg_b = [binding[v] for v in VARIANTS]

    x = np.arange(len(VARIANTS))
    w = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))

    for i, val in enumerate(ddg_s):
        ax.bar(
            x[i] - w / 2, val, w, color=bar_color(val), edgecolor="black", linewidth=0.6
        )

    for i, val in enumerate(ddg_b):
        ax.bar(
            x[i] + w / 2,
            val if val is not None else 0,
            w,
            color=bar_color(val),
            edgecolor="black",
            linewidth=0.6,
            alpha=0.6 if val is None else 1.0,
        )

    ax.axhline(y=1.0, color="black", linestyle="--", linewidth=0.9)
    ax.axhline(y=-1.0, color="black", linestyle="--", linewidth=0.9)
    ax.axhline(y=0.0, color="black", linestyle="-", linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels(VARIANTS, rotation=30, ha="right", fontsize=11)
    ax.set_ylabel("ΔΔG (kcal/mol)", fontsize=12)
    ax.set_title(
        "Effect of NT5C2 variants on stability and binding free energy", fontsize=13
    )

    red_patch = mpatches.Patch(color="#e74c3c", label="Destabilizing (>+1)")
    grey_patch = mpatches.Patch(color="#95a5a6", label="Neutral (−1 to +1)")
    green_patch = mpatches.Patch(color="#2ecc71", label="Stabilizing (<−1)")
    stab_patch = mpatches.Patch(color="black", label="Left bar = Stability")
    bind_patch = mpatches.Patch(color="black", alpha=0.5, label="Right bar = Binding")
    ax.legend(
        handles=[red_patch, grey_patch, green_patch, stab_patch, bind_patch],
        fontsize=9,
        loc="upper right",
    )

    plt.tight_layout()
    plt.savefig(OUTPUT, dpi=300)
    print(f"Saved: {OUTPUT}")
    plt.show()
