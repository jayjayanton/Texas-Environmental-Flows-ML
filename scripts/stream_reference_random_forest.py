#!/usr/bin/env python3
"""Classify reference/non-reference streams using a leakage-safe Random Forest."""
import argparse
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

EXCLUDE = ["Area", "Falcone_Non_Falcone", "Ref_Non_Ref", "Gage ID",
           "Ref_Non_Ref_Binary", "lat", "lon", "NID Storage Summary"]

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--train", type=Path, required=True, help="Labeled training CSV")
    p.add_argument("--predict", type=Path, help="Optional new stream CSV")
    p.add_argument("--output-dir", type=Path, default=Path("outputs/random_forest"))
    p.add_argument("--target", default="Ref_Non_Ref_Binary")
    p.add_argument("--test-size", type=float, default=0.3)
    p.add_argument("--trees", type=int, default=100)
    args = p.parse_args()
    df = pd.read_csv(args.train)
    if args.target not in df:
        p.error(f"Missing target column: {args.target}")
    y = pd.to_numeric(df[args.target], errors="raise")
    if y.isna().any() or not set(y.unique()).issubset({0, 1}) or y.nunique() != 2:
        p.error("Target must contain both binary classes 0 and 1, without missing values")
    feature_cols = [c for c in df.columns if c not in set(EXCLUDE + [args.target])]
    numeric = df[feature_cols].select_dtypes(include="number").columns.tolist()
    if not numeric:
        p.error("No numeric predictors found")
    X = df[numeric].replace([np.inf, -np.inf], np.nan)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=3, stratify=y)
    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),
        ("forest", RandomForestClassifier(n_estimators=args.trees, random_state=30,
                                          class_weight="balanced", n_jobs=-1))
    ])
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)
    probability = pipeline.predict_proba(X_test)[:, 1]
    report = {"accuracy": float(accuracy_score(y_test, pred)),
              "roc_auc": float(roc_auc_score(y_test, probability)),
              "classification_report": classification_report(y_test, pred, output_dict=True),
              "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
              "n_train": len(X_train), "n_test": len(X_test),
              "predictors": numeric}
    min_class = int(y_train.value_counts().min())
    if min_class >= 2:
        folds = min(5, min_class)
        cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=3)
        report["cv_f1_mean"] = float(cross_val_score(
            pipeline, X_train, y_train, cv=cv, scoring="f1").mean())
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "evaluation.json").write_text(json.dumps(report, indent=2))
    pd.DataFrame({"feature": numeric,
                  "importance": pipeline.named_steps["forest"].feature_importances_}
                 ).sort_values("importance", ascending=False).to_csv(
                     args.output_dir / "feature_importance.csv", index=False)
    if args.predict:
        incoming = pd.read_csv(args.predict)
        absent = [c for c in numeric if c not in incoming]
        if absent:
            p.error(f"Prediction CSV missing predictors: {absent}")
        xp = incoming[numeric].apply(pd.to_numeric, errors="coerce").replace([np.inf, -np.inf], np.nan)
        incoming["RF_predicted_class"] = pipeline.predict(xp)
        incoming["RF_probability_class_1"] = pipeline.predict_proba(xp)[:, 1]
        incoming.to_csv(args.output_dir / "stream_predictions.csv", index=False)
    print(json.dumps({"accuracy": report["accuracy"], "roc_auc": report["roc_auc"],
                      "output_dir": str(args.output_dir)}, indent=2))

if __name__ == "__main__":
    main()
