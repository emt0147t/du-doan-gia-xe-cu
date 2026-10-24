"""Phân tích độ nhạy trên Cohort B (Cohort B Sensitivity Analysis).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer

Mục tiêu:
1. Đánh giá mô hình Champion (được huấn luyện trên Cohort A: >= 2015) trực tiếp trên tập xe đời sâu (2010 - 2014).
2. Huấn luyện lại kiến trúc Champion trên toàn bộ Cohort B (2010 - 2023) với split 80/10/10 để so sánh phân phối và sai số.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd

from src.data.split_data import split_dataset
from src.models.evaluate import compute_regression_metrics, inverse_log_transform
from src.models.experiment_config import ExperimentConfig
from src.models.train import build_full_pipeline, extract_features_and_target, run_single_experiment

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = Path("reports/model_experiments")


def main():
    print("=" * 80)
    print("PHÂN TÍCH ĐỘ NHẠY COHORT B (NĂM SẢN XUẤT >= 2010)")
    print("=" * 80)

    # 1. Đọc dữ liệu Cohort B sạch
    cohort_b_path = Path("data/processed/cars_clean_phase5_cohort_b.csv")
    df_cohort_b = pd.read_csv(cohort_b_path)
    print(f"Tổng số bản ghi Cohort B: {len(df_cohort_b):,} dòng.")

    # 2. Phân lập tập xe đời sâu 2010 - 2014 (3,789 dòng)
    df_older_cars = df_cohort_b[df_cohort_b["year"] < 2015].copy()
    print(f"Số lượng xe đời sâu (2010 - 2014): {len(df_older_cars):,} dòng.")

    # 3. Thử nghiệm 1: Khả năng tổng quát hóa của Model Cohort A trên xe đời sâu
    train_a_df = pd.read_csv("data/processed/splits/train.csv")
    cfg_champion = ExperimentConfig(
        "Tree_RandomForest_Tuned_LogTarget",
        "random_forest",
        {"n_estimators": 150, "max_depth": 24, "min_samples_leaf": 1},
        target_type="log",
        preprocessor_type="tree",
    )

    print("\n--> Đang huấn luyện Champion Pipeline trên Cohort A Train (2015+)...")
    rec_older, preds_older, _ = run_single_experiment(cfg_champion, train_a_df, df_older_cars)
    print("Kết quả đánh giá Model Cohort A trên nhóm xe đời sâu 2010-2014:")
    print(f"  MAE:   {rec_older['mae']:,.0f} VND")
    print(f"  RMSE:  {rec_older['rmse']:,.0f} VND")
    print(f"  R2:    {rec_older['r2']:.4f}")
    print(f"  MdAPE: {rec_older['mdape']}%")

    # 4. Thử nghiệm 2: Huấn luyện và kiểm thử trực tiếp trên toàn bộ Cohort B (Split 80/10/10)
    print("\n--> Phân chia Cohort B thành Train/Val/Test 80/10/10 phân tầng theo giá...")
    b_train, b_val, b_test, b_meta = split_dataset(df_cohort_b, random_state=42)
    print(f"  Cohort B Train: {len(b_train):,} | Val: {len(b_val):,} | Test: {len(b_test):,}")

    rec_b_val, _, _ = run_single_experiment(cfg_champion, b_train, b_val)
    rec_b_test, _, _ = run_single_experiment(cfg_champion, b_train, b_test)

    print("\nKết quả huấn luyện trực tiếp trên Cohort B (Toàn diện 2010 - 2023):")
    print(f"  Validation MAE: {rec_b_val['mae']:,.0f} VND | R2: {rec_b_val['r2']:.4f} | MdAPE: {rec_b_val['mdape']}%")
    print(f"  Test MAE:       {rec_b_test['mae']:,.0f} VND | R2: {rec_b_test['r2']:.4f} | MdAPE: {rec_b_test['mdape']}%")

    # 5. Lưu kết quả phân tích độ nhạy
    sensitivity_report = {
        "cohort_a_champion_on_older_cars_2010_2014": {
            "sample_size": len(df_older_cars),
            "mae": rec_older["mae"],
            "rmse": rec_older["rmse"],
            "r2": rec_older["r2"],
            "mdape": rec_older["mdape"],
        },
        "retrained_on_cohort_b_full": {
            "total_size": len(df_cohort_b),
            "val_mae": rec_b_val["mae"],
            "val_r2": rec_b_val["r2"],
            "val_mdape": rec_b_val["mdape"],
            "test_mae": rec_b_test["mae"],
            "test_r2": rec_b_test["r2"],
            "test_mdape": rec_b_test["mdape"],
        },
    }

    out_json = OUTPUT_DIR / "cohort_b_sensitivity_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(sensitivity_report, f, indent=2, ensure_ascii=False)
    print(f"\nĐã lưu kết quả phân tích độ nhạy vào: {out_json}")


if __name__ == "__main__":
    main()
