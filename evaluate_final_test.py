"""Đánh giá cuối cùng trên tập Test độc lập (Final Test Set Evaluation).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer

Nguyên tắc:
- Được thực thi DUY NHẤT MỘT LẦN sau khi đã chốt mô hình chiến thắng trên tập Validation.
- Tuyệt đối không sử dụng kết quả test để tinh chỉnh ngược lại mô hình.
- So sánh mô hình chiến thắng với các baseline quy chuẩn trên cùng tập Test (2,351 dòng).
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

OUTPUT_DIR = Path("reports/model_experiments")


def main():
    print("=" * 80)
    print("FINAL TEST EVALUATION (ĐÁNH GIÁ ĐỘC LẬP TRÊN TẬP TEST - CHẠY 1 LẦN DUY NHẤT)")
    print("=" * 80)

    train_path = Path("data/processed/splits/train.csv")
    test_path = Path("data/processed/splits/test.csv")

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    print(f"Dữ liệu huấn luyện (Train): {len(train_df):,} dòng.")
    print(f"Dữ liệu kiểm thử (Test):     {len(test_df):,} dòng (Unseen Data).\n")

    # Danh sách mô hình đánh giá trên Test:
    # Mô hình vô địch được chọn trên Validation + các đại diện baseline/tuyến tính/boosting
    final_configs = [
        ExperimentConfig("Baseline_Dummy_Median", "dummy_median", target_type="raw", preprocessor_type="tree"),
        ExperimentConfig("Baseline_Dummy_Mean", "dummy_mean", target_type="raw", preprocessor_type="tree"),
        ExperimentConfig("Linear_Ridge_LogTarget", "ridge", {"alpha": 10.0}, target_type="log", preprocessor_type="linear"),
        ExperimentConfig("Tree_HistGBM_LogTarget", "hist_gradient_boosting", {"max_iter": 150, "learning_rate": 0.1, "max_leaf_nodes": 31}, target_type="log", preprocessor_type="tree"),
        ExperimentConfig("Tree_RandomForest_Tuned_LogTarget (CHAMPION)", "random_forest", {"n_estimators": 150, "max_depth": 24, "min_samples_leaf": 1}, target_type="log", preprocessor_type="tree"),
    ]

    results = []
    test_preds_dict = {
        "actual_price_vnd": test_df["price_vnd"].values,
    }
    if "listing_id" in test_df.columns:
        test_preds_dict["listing_id"] = test_df["listing_id"].values

    for cfg in final_configs:
        print(f"--> Đang đánh giá trên Test set: [{cfg.name}]...")
        rec, preds, _ = run_single_experiment(cfg, train_df, test_df)
        results.append(rec)
        test_preds_dict[cfg.name] = preds
        print(f"    Test MAE: {rec['mae']:,.0f} VND | Test RMSE: {rec['rmse']:,.0f} | Test R2: {rec['r2']:.4f} | MdAPE: {rec['mdape']}%")

    df_test_results = pd.DataFrame(results).sort_values(by="mae", ascending=True).reset_index(drop=True)
    df_test_preds = pd.DataFrame(test_preds_dict)

    out_csv = OUTPUT_DIR / "final_test_results.csv"
    out_preds = OUTPUT_DIR / "final_test_predictions.csv"
    df_test_results.to_csv(out_csv, index=False, encoding="utf-8")
    df_test_preds.to_csv(out_preds, index=False, encoding="utf-8")

    print("\n" + "=" * 80)
    print("BẢNG KẾT QUẢ CUỐI CÙNG TRÊN TẬP TEST (FINAL UNSEEN TEST SET)")
    print("=" * 80)
    display_cols = ["experiment_name", "mae", "rmse", "r2", "mape", "mdape", "fit_time_seconds"]
    print(df_test_results[display_cols].to_string(index=False))

    print(f"\nĐã lưu: {out_csv}")
    print(f"Đã lưu: {out_preds}")


if __name__ == "__main__":
    main()
