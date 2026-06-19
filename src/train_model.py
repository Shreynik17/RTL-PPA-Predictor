#!/usr/bin/env python3
"""
train_model.py
Trains ML models to predict synthesis cost (cell count, logic depth)
from RTL features. Evaluates on held-out designs and saves plots.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib
matplotlib.use("Agg")                 # save plots to file, don't open a window
import matplotlib.pyplot as plt
import os

DATA = "data/dataset_swept.csv"

# features the model is allowed to look at
FEATURES = ["width", "loc", "n_inputs", "n_outputs", "max_width",
            "n_assign", "n_always", "n_case", "is_sequential",
            "n_operators", "width_x_ops"]

TARGETS = ["cell_count", "logic_depth"]


def evaluate(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)                  # learn from training data
    preds = model.predict(X_test)                # predict on unseen test data
    mae = mean_absolute_error(y_test, preds)
    r2  = r2_score(y_test, preds)
    print(f"   {name:18s} MAE={mae:7.2f}   R2={r2:6.3f}")
    return preds, mae, r2


def main():
    df = pd.read_csv(DATA)
    print(f"Loaded {len(df)} samples, {len(FEATURES)} features.\n")

    X = df[FEATURES]
    os.makedirs("results", exist_ok=True)

    for target in TARGETS:
        y = df[target]
        # hold back 25% of designs the model never sees during training
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42
        )

        print(f"=== Predicting {target} ===")
        # two models: a simple baseline and a stronger one
        lin = LinearRegression()
        rf  = RandomForestRegressor(n_estimators=200, random_state=42)

        evaluate("LinearRegression", lin, X_train, X_test, y_train, y_test)
        rf_preds, _, _ = evaluate("RandomForest", rf, X_train, X_test, y_train, y_test)

        # plot predicted vs actual for the random forest
        plt.figure(figsize=(5, 5))
        plt.scatter(y_test, rf_preds, c="#4299e1", s=60, edgecolors="k")
        lims = [0, max(y_test.max(), rf_preds.max()) * 1.1]
        plt.plot(lims, lims, "r--", label="perfect prediction")
        plt.xlabel(f"actual {target}")
        plt.ylabel(f"predicted {target}")
        plt.title(f"RandomForest: {target}")
        plt.legend()
        plt.tight_layout()
        out = f"results/pred_{target}.png"
        plt.savefig(out, dpi=120)
        print(f"   saved plot -> {out}\n")

    # which features mattered most (using cell_count model)
    rf_full = RandomForestRegressor(n_estimators=200, random_state=42)
    rf_full.fit(X, df["cell_count"])
    importances = sorted(zip(FEATURES, rf_full.feature_importances_),
                         key=lambda t: t[1], reverse=True)
    print("Feature importance for cell_count:")
    for feat, imp in importances:
        print(f"   {feat:16s} {imp:.3f}")


if __name__ == "__main__":
    main()
