"""Tính toán và vẽ biểu đồ tầm quan trọng của đặc trưng (Feature Importance).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer
"""

from __future__ import annotations

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.models.experiment_config import ExperimentConfig
from src.models.train import build_full_pipeline, extract_features_and_target

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

FIGURES_DIR = Path("reports/figures/phase6")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("Bắt đầu tính toán Feature Importance...")
    train_df = pd.read_csv("data/processed/splits/train.csv")
    X_train, y_train = extract_features_and_target(train_df)
    y_train_log = np.log(y_train.values.astype("float64"))

    cfg = ExperimentConfig(
        name="Tree_RandomForest_Tuned_LogTarget",
        model_type="random_forest",
        hyperparameters={"n_estimators": 150, "max_depth": 24, "min_samples_leaf": 1},
        target_type="log",
        preprocessor_type="tree",
    )
    pipe = build_full_pipeline(cfg)
    pipe.fit(X_train, y_train_log)

    prep = pipe.named_steps["preprocessor"]
    rf = pipe.named_steps["model"]

    feat_names = prep.get_feature_names_out()
    importances = rf.feature_importances_

    # Gộp theo tên đặc trưng gốc
    orig_features = {}
    known_features = [
        "is_luxury_brand",
        "engine_displacement_l",
        "car_age",
        "year",
        "mileage_km",
        "is_zero_mileage",
        "seats",
        "doors",
        "brand",
        "model",
        "condition",
        "transmission",
        "origin",
        "body_type",
        "fuel_type",
    ]

    for name, imp in zip(feat_names, importances):
        matched = False
        for orig in known_features:
            if name.startswith(f"num__{orig}") or name.startswith(f"cat__{orig}"):
                orig_features[orig] = orig_features.get(orig, 0.0) + imp
                matched = True
                break
        if not matched:
            clean_p = name.split("__")[1].split("_")[0]
            orig_features[clean_p] = orig_features.get(clean_p, 0.0) + imp

    s_orig = pd.Series(orig_features).sort_values(ascending=False)

    # Top 15 đặc trưng chi tiết sau One-Hot
    clean_encoded_names = [n.replace("num__", "").replace("cat__", "") for n in feat_names]
    s_encoded = pd.Series(importances, index=clean_encoded_names).sort_values(ascending=False).head(15)

    print("Aggregated Feature Importance:\n", s_orig)
    print("\nTop 15 Encoded Features:\n", s_encoded)

    # Vẽ biểu đồ
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    sns.barplot(x=s_orig.values, y=s_orig.index, ax=axes[0], palette="Blues_r")
    axes[0].set_title("Tầm quan trọng gộp theo Nhóm đặc trưng gốc", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Tỷ trọng quan trọng tương đối (Mean Decrease in Impurity / Variance Reduction)", fontsize=10)

    sns.barplot(x=s_encoded.values, y=s_encoded.index, ax=axes[1], palette="Reds_r")
    axes[1].set_title("Top 15 Đặc trưng chi tiết (One-Hot Encoded)", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Tỷ trọng quan trọng tương đối", fontsize=10)

    plt.tight_layout()
    out_fig = FIGURES_DIR / "feature_importance.png"
    plt.savefig(out_fig, dpi=300)
    plt.close()
    print(f"Đã lưu biểu đồ: {out_fig}")


if __name__ == "__main__":
    main()
