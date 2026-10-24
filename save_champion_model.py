"""Lưu trữ artifact mô hình chiến thắng (Save Champion Model Artifact & Metadata).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

from src.models.experiment_config import ExperimentConfig
from src.models.train import build_full_pipeline, extract_features_and_target

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

MODELS_DIR = Path("models")
MODELS_DIR.mkdir(parents=True, exist_ok=True)


def compute_file_sha256(filepath: Path | str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()


def main():
    print("Bắt đầu huấn luyện và lưu trữ mô hình chiến thắng...")
    train_path = Path("data/processed/splits/train.csv")
    train_df = pd.read_csv(train_path)

    X_train, y_train = extract_features_and_target(train_df)
    y_train_log = np.log(y_train.values.astype("float64"))

    cfg = ExperimentConfig(
        name="Tree_RandomForest_Tuned_LogTarget",
        model_type="random_forest",
        hyperparameters={"n_estimators": 150, "max_depth": 24, "min_samples_leaf": 1},
        target_type="log",
        preprocessor_type="tree",
        description="Random Forest 150 trees tuned pipeline on log target",
    )

    pipeline = build_full_pipeline(cfg)
    pipeline.fit(X_train, y_train_log)

    model_file = MODELS_DIR / "champion_random_forest.joblib"
    joblib.dump(pipeline, model_file, compress=3)
    model_sha256 = compute_file_sha256(model_file)
    file_size_bytes = model_file.stat().st_size

    metadata = {
        "model_name": "Champion Random Forest Regressor (Tuned Log-Target)",
        "pipeline_structure": {
            "preprocessor": "ColumnTransformer (SimpleImputer + OneHotEncoder for Categorical; SimpleImputer for Numeric)",
            "estimator": "RandomForestRegressor(n_estimators=150, max_depth=24, min_samples_leaf=1, random_state=42, n_jobs=-1)",
        },
        "target_transformation": {
            "training_target": "log_price = ln(price_vnd)",
            "inference_inverse": "price_vnd = exp(pred_log), bounded [30M, 100B]",
        },
        "training_data": {
            "source": "data/processed/splits/train.csv",
            "samples": len(train_df),
            "features_in": list(X_train.columns),
            "total_features": len(X_train.columns),
        },
        "evaluation_summary": {
            "validation_mae_vnd": 142934537.0,
            "validation_r2": 0.8694,
            "validation_mdape_pct": 4.25,
            "final_test_mae_vnd": 111793581.0,
            "final_test_r2": 0.9448,
            "final_test_mdape_pct": 4.29,
        },
        "artifact_details": {
            "file_path": str(model_file),
            "file_size_bytes": file_size_bytes,
            "sha256": model_sha256,
            "serialized_with": f"joblib {joblib.__version__}",
        },
    }

    meta_file = MODELS_DIR / "champion_model_metadata.json"
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"Đã lưu mô hình: {model_file} ({file_size_bytes / 1e6:.1f} MB)")
    print(f"  SHA-256: {model_sha256}")
    print(f"Đã lưu metadata: {meta_file}")


if __name__ == "__main__":
    main()
