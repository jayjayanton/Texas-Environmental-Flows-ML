#!/usr/bin/env python3
"""Summarize multi-output tree depth sweep and plot ecoregion curves."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, default=Path("outputs/analysis"))
    args = p.parse_args()
    if not args.input.is_file():
        p.error(f"Input does not exist: {args.input}")
    df = pd.read_csv(args.input)
    needed = {"Ecoregion", "Metric", "Depth", "R2_train"}
    if not needed.issubset(df.columns):
        p.error(f"Missing columns: {sorted(needed - set(df.columns))}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary = df.groupby(["Ecoregion", "Depth"], as_index=False)["R2_train"].mean()
    summary.rename(columns={"R2_train": "MeanTrainR2"}, inplace=True)
    summary.to_csv(args.output_dir / "mean_r2_by_depth.csv", index=False)
    rows = []
    fig, ax = plt.subplots(figsize=(10, 6))
    for region, group in summary.groupby("Ecoregion", sort=True):
        group = group.sort_values("Depth")
        depths = group["Depth"].to_numpy(dtype=float)
        scores = group["MeanTrainR2"].to_numpy(dtype=float)
        ax.plot(depths, scores, marker=".", label=str(region))
        if len(depths) >= 4:
            d2 = np.gradient(np.gradient(scores, depths), depths)
            crossings = np.flatnonzero(np.diff(np.sign(d2)) != 0)
            for index in crossings:
                rows.append({"Ecoregion": region, "CandidateDepth": int(depths[index + 1]),
                             "Note": "discrete second-derivative sign change"})
    pd.DataFrame(rows, columns=["Ecoregion", "CandidateDepth", "Note"]).to_csv(
        args.output_dir / "candidate_inflections.csv", index=False)
    ax.set(xlabel="Maximum tree depth", ylabel="Mean in-sample multi-output R²",
           title="HIT metric decision-tree depth sweep")
    ax.legend(loc="best", fontsize="small", ncol=2)
    fig.tight_layout()
    fig.savefig(args.output_dir / "depth_curves.png", dpi=180)
    plt.close(fig)
    print(f"Saved summaries and figure to {args.output_dir}")

if __name__ == "__main__":
    main()
