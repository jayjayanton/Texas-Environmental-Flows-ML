#!/usr/bin/env python3
"""Multi-output decision-tree depth sweep by Texas ecoregion and HIT metric."""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor

ID_COLUMNS = {"COMID", "year", "huc4", "region"}

def load_data(path: Path, r_object: str) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"Input file not found: {path}")
    suffix = path.suffix.lower()
    if suffix == ".rdata":
        import pyreadr
        objects = pyreadr.read_r(str(path))
        if r_object not in objects:
            raise KeyError(f"R object {r_object!r} missing; available: {list(objects)}")
        return objects[r_object]
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError("Use .RData, .csv, or .xlsx input")

def names(value: str | None) -> list[str] | None:
    return [x.strip() for x in value.split(",") if x.strip()] if value else None

def run(df: pd.DataFrame, metric_count: int, max_depth: int,
        metrics: list[str] | None, responses: list[str] | None) -> pd.DataFrame:
    if "region" not in df.columns:
        raise ValueError("Input must contain a 'region' column")
    candidates = [c for c in df.columns if c not in ID_COLUMNS]
    if metrics is None:
        if len(candidates) <= metric_count:
            raise ValueError("Not enough columns for metric-count plus fish responses")
        metrics = candidates[:metric_count]
    if responses is None:
        responses = [c for c in candidates if c not in metrics]
    missing = [c for c in metrics + responses if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    if not metrics or not responses or set(metrics) & set(responses):
        raise ValueError("Select distinct, nonempty metric and response columns")
    results = []
    for region, group in df.groupby("region", dropna=True, sort=True):
        y_all = group[responses].apply(pd.to_numeric, errors="coerce")
        for metric in metrics:
            x_all = pd.to_numeric(group[metric], errors="coerce")
            valid = x_all.notna() & np.isfinite(x_all) & y_all.notna().all(axis=1) & np.isfinite(y_all).all(axis=1)
            x = x_all.loc[valid].to_numpy().reshape(-1, 1)
            y = y_all.loc[valid].to_numpy()
            if len(x) < 2:
                continue
            for depth in range(1, max_depth + 1):
                model = DecisionTreeRegressor(max_depth=depth, random_state=42)
                model.fit(x, y)
                results.append({"Ecoregion": str(region), "Metric": metric,
                                "Depth": depth, "R2_train": float(model.score(x, y)),
                                "ActualTreeDepth": int(model.get_depth()), "N": len(x)})
                if model.get_depth() < depth:
                    break
    return pd.DataFrame(results, columns=["Ecoregion", "Metric", "Depth", "R2_train", "ActualTreeDepth", "N"])

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--r-object", default="ivern")
    p.add_argument("--output-dir", type=Path, default=Path("outputs"))
    p.add_argument("--metric-count", type=int, default=130)
    p.add_argument("--max-depth", type=int, default=40)
    p.add_argument("--metric-columns", help="Comma-separated HIT predictor column names")
    p.add_argument("--response-columns", help="Comma-separated fish response column names")
    args = p.parse_args()
    if args.metric_count < 1 or args.max_depth < 1:
        p.error("--metric-count and --max-depth must be positive")
    df = load_data(args.input, args.r_object)
    result = run(df, args.metric_count, args.max_depth, names(args.metric_columns), names(args.response_columns))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = args.output_dir / "metric_runs.csv"
    result.to_csv(target, index=False)
    print(f"Wrote {len(result)} rows to {target}")

if __name__ == "__main__":
    main()
