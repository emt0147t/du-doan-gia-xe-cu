"""Kịch bản thực thi bộ thí nghiệm mô hình hóa Phase 6.

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer
"""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd

from src.models.experiment_config import ExperimentConfig
from src.models.train import run_experiment_suite

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    print("=" * 80)
    print("PHASE 6: CHẠY BỘ THÍ NGHIỆM HUẤN LUYỆN VÀ ĐÁNH GIÁ MÔ HÌNH HỌC MÁY")
    print("=" * 80)

    train_path = Path("data/processed/splits/train.csv")
    val_path = Path("data/processed/splits/val.csv")

    if not (train_path.exists() and val_path.exists()):
        print("Lỗi: Không tìm thấy dữ liệu splits train.csv hoặc val.csv!")
        sys.exit(1)

    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    print(f"Dữ liệu huấn luyện (Train): {len(train_df):,} dòng.")
    print(f"Dữ liệu kiểm định (Val):   {len(val_df):,} dòng.\n")

    # Danh sách 9 cấu hình thí nghiệm đa dạng
    configs = [
        # 1. Baseline Models
        ExperimentConfig(
            name="Baseline_Dummy_Median",
            model_type="dummy_median",
            target_type="raw",
            preprocessor_type="tree",
            description="Dự đoán trung vị toàn bộ tập huấn luyện",
        ),
        ExperimentConfig(
            name="Baseline_Dummy_Mean",
            model_type="dummy_mean",
            target_type="raw",
            preprocessor_type="tree",
            description="Dự đoán trung bình toàn bộ tập huấn luyện",
        ),
        # 2. Linear Models (Ridge)
        ExperimentConfig(
            name="Linear_Ridge_RawTarget",
            model_type="ridge",
            hyperparameters={"alpha": 10.0},
            target_type="raw",
            preprocessor_type="linear",
            description="Hồi quy Ridge với giá thô VND",
        ),
        ExperimentConfig(
            name="Linear_Ridge_LogTarget",
            model_type="ridge",
            hyperparameters={"alpha": 10.0},
            target_type="log",
            preprocessor_type="linear",
            description="Hồi quy Ridge với log(VND)",
        ),
        # 3. Linear Model (Lasso)
        ExperimentConfig(
            name="Linear_Lasso_LogTarget",
            model_type="lasso",
            hyperparameters={"alpha": 0.001, "max_iter": 3000},
            target_type="log",
            preprocessor_type="linear",
            description="Hồi quy Lasso với log(VND)",
        ),
        # 4. Tree Ensembles (Random Forest)
        ExperimentConfig(
            name="Tree_RandomForest_RawTarget",
            model_type="random_forest",
            hyperparameters={"n_estimators": 100, "max_depth": 16, "min_samples_leaf": 2},
            target_type="raw",
            preprocessor_type="tree",
            description="Random Forest 100 cây trên giá thô VND",
        ),
        ExperimentConfig(
            name="Tree_RandomForest_LogTarget",
            model_type="random_forest",
            hyperparameters={"n_estimators": 100, "max_depth": 16, "min_samples_leaf": 2},
            target_type="log",
            preprocessor_type="tree",
            description="Random Forest 100 cây trên log(VND)",
        ),
        # 5. Gradient Boosting (HistGradientBoosting)
        ExperimentConfig(
            name="Tree_HistGBM_RawTarget",
            model_type="hist_gradient_boosting",
            hyperparameters={"max_iter": 150, "learning_rate": 0.1, "max_leaf_nodes": 31},
            target_type="raw",
            preprocessor_type="tree",
            description="HistGradientBoosting 150 cây trên giá thô VND",
        ),
        ExperimentConfig(
            name="Tree_HistGBM_LogTarget",
            model_type="hist_gradient_boosting",
            hyperparameters={"max_iter": 150, "learning_rate": 0.1, "max_leaf_nodes": 31},
            target_type="log",
            preprocessor_type="tree",
            description="HistGradientBoosting 150 cây trên log(VND)",
        ),
        # 6. Tuned Champion Model
        ExperimentConfig(
            name="Tree_RandomForest_Tuned_LogTarget",
            model_type="random_forest",
            hyperparameters={"n_estimators": 150, "max_depth": 24, "min_samples_leaf": 1},
            target_type="log",
            preprocessor_type="tree",
            description="Random Forest 150 cây tuned (depth 24, leaf 1) trên log(VND)",
        ),
    ]

    df_results, df_val_preds, meta = run_experiment_suite(configs, train_df, val_df)

    print("\n" + "=" * 80)
    print("BẢNG XẾP HẠNG KẾT QUẢ TRÊN TẬP VALIDATION (SẮP XẾP THEO MAE TĂNG DẦN)")
    print("=" * 80)
    display_cols = ["experiment_name", "target_type", "mae", "rmse", "r2", "mape", "mdape", "fit_time_seconds"]
    print(df_results[display_cols].to_string(index=False))

    print("\nThí nghiệm tốt nhất trên Validation Set:")
    print(f"  Mô hình: {meta['best_model_by_mae']}")
    print(f"  Validation MAE: {meta['best_val_mae']:,.0f} VND")
    print(f"  Validation R2:  {meta['best_val_r2']:.4f}")
    print(f"  Đã xuất bảng kết quả: {meta['results_table']}")
    print(f"  Đã xuất bảng dự đoán: {meta['predictions_table']}")


if __name__ == "__main__":
    main()
