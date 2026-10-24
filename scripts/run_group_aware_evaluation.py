"""Huấn luyện và đánh giá mô hình trên bộ chia tập Group-Aware (Task E).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & Independent ML Evaluation Reviewer
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pandas as pd

from src.models.experiment_config import ExperimentConfig
from src.models.train import run_single_experiment

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = Path("reports/model_experiments/phase6_2_grouped")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("=" * 80)
    print("CHẠY ĐÁNH GIÁ ĐỘ BỀN GROUP-AWARE ROBUSTNESS EVALUATION (PHASE 6.2)")
    print("=" * 80)

    train_path = Path("data/processed/splits_grouped_v1/train.csv")
    val_path = Path("data/processed/splits_grouped_v1/val.csv")
    test_path = Path("data/processed/splits_grouped_v1/test.csv")

    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)

    print(f"Dữ liệu Group-Aware Train: {len(train_df):,} dòng.")
    print(f"Dữ liệu Group-Aware Val:   {len(val_df):,} dòng.")
    print(f"Dữ liệu Group-Aware Test:  {len(test_df):,} dòng.\n")

    # Danh sách các cấu hình đóng băng
    frozen_configs = [
        ExperimentConfig(
            name="Baseline_Dummy_Median",
            model_type="dummy_median",
            target_type="raw",
            preprocessor_type="tree",
            description="Baseline dự đoán trung vị tập Train",
        ),
        ExperimentConfig(
            name="Baseline_Dummy_Mean",
            model_type="dummy_mean",
            target_type="raw",
            preprocessor_type="tree",
            description="Baseline dự đoán trung bình tập Train",
        ),
        ExperimentConfig(
            name="Tree_RandomForest_Tuned_LogTarget",
            model_type="random_forest",
            hyperparameters={"n_estimators": 150, "max_depth": 24, "min_samples_leaf": 1},
            target_type="log",
            preprocessor_type="tree",
            description="Champion Random Forest đã đóng băng siêu tham số từ Phase 6",
        ),
    ]

    eval_records = []
    test_preds_dict = {
        "actual_price_vnd": test_df["price_vnd"].values,
    }
    if "listing_id" in test_df.columns:
        test_preds_dict["listing_id"] = test_df["listing_id"].values
    if "record_group_id" in test_df.columns:
        test_preds_dict["record_group_id"] = test_df["record_group_id"].values

    for cfg in frozen_configs:
        print(f"\n--> [1/2] Đánh giá trên Group-Aware Validation: [{cfg.name}]...")
        val_rec, _, _ = run_single_experiment(cfg, train_df, val_df)
        print(f"    Val MAE: {val_rec['mae']:,.0f} VND | Val R2: {val_rec['r2']:.4f} | MdAPE: {val_rec['mdape']}%")

        print(f"--> [2/2] Đánh giá trên Group-Aware Test: [{cfg.name}]...")
        test_rec, test_preds, _ = run_single_experiment(cfg, train_df, test_df)
        print(f"    Test MAE: {test_rec['mae']:,.0f} VND | Test RMSE: {test_rec['rmse']:,.0f} | Test R2: {test_rec['r2']:.4f} | MdAPE: {test_rec['mdape']}%")

        test_preds_dict[cfg.name] = test_preds

        combined_record = {
            "model_name": cfg.name,
            "target_type": cfg.target_type,
            # Validation metrics
            "val_mae": val_rec["mae"],
            "val_rmse": val_rec["rmse"],
            "val_r2": val_rec["r2"],
            "val_mape": val_rec["mape"],
            "val_mdape": val_rec["mdape"],
            # Test metrics
            "test_mae": test_rec["mae"],
            "test_rmse": test_rec["rmse"],
            "test_r2": test_rec["r2"],
            "test_mape": test_rec["mape"],
            "test_mdape": test_rec["mdape"],
            "fit_time_seconds": test_rec["fit_time_seconds"],
        }
        eval_records.append(combined_record)

    df_eval = pd.DataFrame(eval_records)
    df_preds = pd.DataFrame(test_preds_dict)

    res_csv = OUTPUT_DIR / "evaluation_results.csv"
    preds_csv = OUTPUT_DIR / "test_predictions.csv"
    df_eval.to_csv(res_csv, index=False, encoding="utf-8")
    df_preds.to_csv(preds_csv, index=False, encoding="utf-8")

    meta = {
        "evaluation_phase": "Phase 6.2 - Group-Aware Robustness Evaluation",
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "train_split": str(train_path),
        "val_split": str(val_path),
        "test_split": str(test_path),
        "evaluation_results": str(res_csv),
        "test_predictions": str(preds_csv),
        "champion_performance": {
            "val_mae_vnd": float(df_eval.loc[df_eval["model_name"] == "Tree_RandomForest_Tuned_LogTarget", "val_mae"].iloc[0]),
            "val_r2": float(df_eval.loc[df_eval["model_name"] == "Tree_RandomForest_Tuned_LogTarget", "val_r2"].iloc[0]),
            "val_mdape_pct": float(df_eval.loc[df_eval["model_name"] == "Tree_RandomForest_Tuned_LogTarget", "val_mdape"].iloc[0]),
            "test_mae_vnd": float(df_eval.loc[df_eval["model_name"] == "Tree_RandomForest_Tuned_LogTarget", "test_mae"].iloc[0]),
            "test_r2": float(df_eval.loc[df_eval["model_name"] == "Tree_RandomForest_Tuned_LogTarget", "test_r2"].iloc[0]),
            "test_mdape_pct": float(df_eval.loc[df_eval["model_name"] == "Tree_RandomForest_Tuned_LogTarget", "test_mdape"].iloc[0]),
        },
    }

    meta_json = OUTPUT_DIR / "experiment_metadata.json"
    with open(meta_json, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("BẢNG KẾT QUẢ ĐÁNH GIÁ ĐỘ BỀN GROUP-AWARE (SUMMARY TABLE)")
    print("=" * 80)
    print(df_eval[["model_name", "val_mae", "val_r2", "val_mdape", "test_mae", "test_r2", "test_mdape"]].to_string(index=False))

    print(f"\nĐã lưu kết quả tại: {res_csv}")
    print(f"Đã lưu dự đoán tại: {preds_csv}")
    print(f"Đã lưu metadata tại: {meta_json}")


if __name__ == "__main__":
    main()
