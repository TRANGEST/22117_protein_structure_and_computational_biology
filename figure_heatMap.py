import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from parse_results import get_stability_ddg, get_binding_ddg

OUTPUT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "figure_heatMap.png",
)

VARIANTS = ["K47E", "R149G", "D206H", "V242L", "T261S", "S281P", "R291W", "Q364E"]

AM_SCORES = {
    "K47E": 0.5146,
    "R149G": 0.9943,
    "D206H": 0.9967,
    "V242L": 0.4422,
    "T261S": 0.0656,
    "S281P": 0.9345,
    "R291W": 0.6197,
    "Q364E": 0.4790,
}

DEMASK_SCORES = {
    "K47E": -0.30,
    "R149G": -0.34,
    "D206H": -0.33,
    "V242L": -0.10,
    "T261S": -0.02,
    "S281P": -0.32,
    "R291W": -0.31,
    "Q364E": -0.18,
}

if __name__ == "__main__":
    stability = get_stability_ddg()
    binding = get_binding_ddg()

    data = {
        "AlphaMissense": [AM_SCORES[v] for v in VARIANTS],
        "DeMask": [abs(DEMASK_SCORES[v]) for v in VARIANTS],
        "DDG stability": [stability[v] for v in VARIANTS],
        "DDG binding": [binding[v] for v in VARIANTS],
    }
    df = pd.DataFrame(data, index=VARIANTS)

    fig, axes = plt.subplots(1, 4, figsize=(12, 6))
    fig.suptitle("NT5C2 variant summary — all analyses", fontsize=14, fontweight="bold")

    configs = [
        ("AlphaMissense", "Reds", 0.0, 1.0, "Score (0→1)"),
        ("DeMask", "Reds", 0.0, 0.4, "|Score| (0→0.4)"),
        ("DDG stability", "RdYlGn_r", -2.0, 5.0, "kcal/mol"),
        ("DDG binding", "RdYlGn_r", -2.0, 5.0, "kcal/mol"),
    ]

    for ax, (col, cmap, vmin, vmax, unit) in zip(axes, configs):
        values = df[[col]].values
        im = ax.imshow(values, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")

        for i, v in enumerate(values.flatten()):
            label = f"{v:.2f}" if not np.isnan(v) else "N/A"
            ax.text(
                0, i, label, ha="center", va="center", fontsize=9, fontweight="bold"
            )

        ax.set_xticks([0])
        ax.set_xticklabels([col], rotation=30, ha="right", fontsize=10)
        ax.set_yticks(range(len(VARIANTS)))
        ax.set_yticklabels(VARIANTS if ax == axes[0] else [], fontsize=10)
        plt.colorbar(im, ax=ax, shrink=0.6, label=unit)

    plt.tight_layout()
    plt.savefig(OUTPUT, dpi=300)
    print(f"Saved: {OUTPUT}")
    plt.show()
