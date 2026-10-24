"""Kiểm toán độc lập Phase 6 (Independent Model Audit & Metric Reassessment).

Mục đích:
1. Đối soát toàn diện các con số trong experiment_results.csv, final_test_results.csv.
2. Phân tích nguyên nhân sâu xa vì sao Test metrics tốt hơn Validation metrics.
3. Đo lường phân phối giá, xe siêu sang, ngoại lai giữa Train, Val và Test.
4. Kiểm tra Permutation Importance đối chiếu với Tree MDI Importance.
5. Đo lường tác động của group leakage (showroom / cross-posting).
"""

import sys
from pathlib import Path
import json

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
import joblib

from src.models.evaluate import compute_regression_metrics, inverse_log_transform
from src.data.preprocessing import extract_features_and_target, NUMERIC_FEATURES, CATEGORICAL_FEATURES

def audit_datasets_and_distributions():
    print("=" * 80)
    print("1. ĐỐI SOÁT PHÂN PHỐI & ĐẶC TÍNH DATA SPLITS (TRAIN, VAL, TEST)")
    print("=" * 80)
    
    train = pd.read_csv("data/processed/splits/train.csv")
    val = pd.read_csv("data/processed/splits/val.csv")
    test = pd.read_csv("data/processed/splits/test.csv")
    
    print(f"Số lượng dòng: Train = {len(train):,}, Val = {len(val):,}, Test = {len(test):,}")
    
    for name, df in [("Train", train), ("Val", val), ("Test", test)]:
        p = df["price_vnd"]
        print(f"\n--- Phân phối giá {name} ---")
        print(f"  Mean:      {p.mean():,.0f} VND")
        print(f"  Median:    {p.median():,.0f} VND")
        print(f"  Std:       {p.std():,.0f} VND")
        print(f"  Min:       {p.min():,.0f} VND")
        print(f"  Max:       {p.max():,.0f} VND")
        print(f"  P90:       {p.quantile(0.90):,.0f} VND")
        print(f"  P95:       {p.quantile(0.95):,.0f} VND")
        print(f"  P99:       {p.quantile(0.99):,.0f} VND")
        print(f"  Skewness:  {p.skew():.2f}")
        
        # Đếm số xe siêu sang (>5 tỷ, >10 tỷ)
        c_5b = (p > 5_000_000_000).sum()
        c_10b = (p > 10_000_000_000).sum()
        c_lux = df["is_luxury_brand"].sum()
        print(f"  Số xe > 5 tỷ:  {c_5b} ({c_5b/len(df)*100:.2f}%)")
        print(f"  Số xe > 10 tỷ: {c_10b} ({c_10b/len(df)*100:.2f}%)")
        print(f"  Tỷ lệ xe sang: {c_lux} ({c_lux/len(df)*100:.2f}%)")

def audit_predictions_and_metrics():
    print("\n" + "=" * 80)
    print("2. ĐỐI SOÁT TÁI LẬP METRICS TỪ TỆP PREDICTIONS ĐÃ LƯU")
    print("=" * 80)
    
    val_preds_df = pd.read_csv("reports/model_experiments/validation_predictions.csv")
    test_preds_df = pd.read_csv("reports/model_experiments/final_test_predictions.csv")
    
    # 1. Validation metrics cho champion
    champ_col = "Tree_RandomForest_Tuned_LogTarget"
    y_val_true = val_preds_df["actual_price_vnd"].values
    y_val_pred = val_preds_df[champ_col].values
    val_metrics = compute_regression_metrics(y_val_true, y_val_pred)
    print("Recomputed Validation Metrics for Champion:")
    print(val_metrics)
    
    # 2. Test metrics cho champion
    champ_test_col = "Tree_RandomForest_Tuned_LogTarget (CHAMPION)"
    y_test_true = test_preds_df["actual_price_vnd"].values
    y_test_pred = test_preds_df[champ_test_col].values
    test_metrics = compute_regression_metrics(y_test_true, y_test_pred)
    print("\nRecomputed Test Metrics for Champion:")
    print(test_metrics)
    
    # 3. Phân rã sai số theo phân khúc giá để tìm nguồn gốc chênh lệch Val vs Test
    print("\n--- PHÂN RÃ MAE THEO PHÂN KHÚC GIÁ GIỮA VAL VÀ TEST ---")
    bins = [0, 500_000_000, 1_000_000_000, 2_000_000_000, 5_000_000_000, float("inf")]
    labels = ["<500M", "500M-1B", "1B-2B", "2B-5B", ">5B"]
    
    val_preds_df["price_bin"] = pd.cut(val_preds_df["actual_price_vnd"], bins=bins, labels=labels)
    test_preds_df["price_bin"] = pd.cut(test_preds_df["actual_price_vnd"], bins=bins, labels=labels)
    
    val_preds_df["err_champ"] = np.abs(val_preds_df["actual_price_vnd"] - val_preds_df[champ_col])
    test_preds_df["err_champ"] = np.abs(test_preds_df["actual_price_vnd"] - test_preds_df[champ_test_col])
    
    print("\n[VALIDATION] Thống kê sai số theo phân khúc:")
    val_grp = val_preds_df.groupby("price_bin", observed=True).agg(
        count=("err_champ", "count"),
        mae=("err_champ", "mean"),
        max_err=("err_champ", "max"),
        sum_err=("err_champ", "sum")
    )
    val_grp["pct_total_err"] = val_grp["sum_err"] / val_preds_df["err_champ"].sum() * 100
    print(val_grp)
    
    print("\n[TEST] Thống kê sai số theo phân khúc:")
    test_grp = test_preds_df.groupby("price_bin", observed=True).agg(
        count=("err_champ", "count"),
        mae=("err_champ", "mean"),
        max_err=("err_champ", "max"),
        sum_err=("err_champ", "sum")
    )
    test_grp["pct_total_err"] = test_grp["sum_err"] / test_preds_df["err_champ"].sum() * 100
    print(test_grp)

    # Xem các mẫu sai số lớn nhất trên Validation và Test
    print("\nTop 5 sai số lớn nhất trên Validation:")
    top_val_err = val_preds_df.sort_values(by="err_champ", ascending=False).head(5)
    for _, r in top_val_err.iterrows():
        print(f"  Actual: {r['actual_price_vnd']:,.0f} | Pred: {r[champ_col]:,.0f} | Error: {r['err_champ']:,.0f}")
        
    print("\nTop 5 sai số lớn nhất trên Test:")
    top_test_err = test_preds_df.sort_values(by="err_champ", ascending=False).head(5)
    for _, r in top_test_err.iterrows():
        print(f"  Actual: {r['actual_price_vnd']:,.0f} | Pred: {r[champ_test_col]:,.0f} | Error: {r['err_champ']:,.0f}")

def audit_feature_importance_and_permutation():
    print("\n" + "=" * 80)
    print("3. KIỂM TOÁN TẦM QUAN TRỌNG ĐẶC TRƯNG & PERMUTATION IMPORTANCE")
    print("=" * 80)
    
    model = joblib.load("models/champion_random_forest.joblib")
    val_df = pd.read_csv("data/processed/splits/val.csv")
    X_val, y_val = extract_features_and_target(val_df)
    y_val_log = np.log(y_val.values.astype("float64"))
    
    # Tính permutation importance trên 500 mẫu của validation (để nhanh và độc lập)
    print("Đang tính Permutation Importance trên Validation set (subsample 500 mẫu, n_repeats=5)...")
    np.random.seed(42)
    sample_idx = np.random.choice(len(X_val), size=min(500, len(X_val)), replace=False)
    X_val_sub = X_val.iloc[sample_idx]
    y_val_log_sub = y_val_log[sample_idx]
    
    perm_res = permutation_importance(
        model, X_val_sub, y_val_log_sub, n_repeats=5, random_state=42, n_jobs=-1, scoring="neg_mean_squared_error"
    )
    
    perm_df = pd.DataFrame({
        "feature": X_val.columns,
        "importance_mean": perm_res.importances_mean,
        "importance_std": perm_res.importances_std,
    }).sort_values(by="importance_mean", ascending=False)
    
    print("\nPermutation Feature Importance on Validation (MSE degradation):")
    print(perm_df.to_string(index=False))

def audit_leakage_groups():
    print("\n" + "=" * 80)
    print("4. KIỂM TOÁN RÒ RỈ DỮ LIỆU THEO CỤM GROUP ID")
    print("=" * 80)
    
    # Đọc dataset clean
    cars_df = pd.read_csv("data/processed/cars_clean_phase5.csv")
    train = pd.read_csv("data/processed/splits/train.csv")
    val = pd.read_csv("data/processed/splits/val.csv")
    test = pd.read_csv("data/processed/splits/test.csv")
    
    # Tạo Group ID từ cấu hình thông số kỹ thuật xe chi tiết
    # Group: brand + model + year + transmission + engine_displacement_l + fuel_type + body_type + origin
    group_cols = ["brand", "model", "year", "transmission", "engine_displacement_l", "fuel_type", "body_type", "origin"]
    for df in [train, val, test]:
        df["spec_group_id"] = df[group_cols].fillna("missing").astype(str).apply(lambda r: "_".join(r.values), axis=1)
        
    train_groups = set(train["spec_group_id"])
    val_groups = set(val["spec_group_id"])
    test_groups = set(test["spec_group_id"])
    
    val_in_train = val["spec_group_id"].isin(train_groups)
    test_in_train = test["spec_group_id"].isin(train_groups)
    
    print(f"Số lượng spec groups độc lập trong Train: {len(train_groups):,}")
    print(f"Tỷ lệ dòng trong Val thuộc group đã có trong Train: {val_in_train.sum()} / {len(val)} ({val_in_train.mean()*100:.2f}%)")
    print(f"Tỷ lệ dòng trong Test thuộc group đã có trong Train: {test_in_train.sum()} / {len(test)} ({test_in_train.mean()*100:.2f}%)")
    
    # Kiểm tra sai số của mô hình trên các xe thuộc group đã thấy vs chưa từng thấy
    test_preds_df = pd.read_csv("reports/model_experiments/final_test_predictions.csv")
    test_preds_df["in_train_group"] = test_in_train.values
    test_preds_df["err"] = np.abs(test_preds_df["actual_price_vnd"] - test_preds_df["Tree_RandomForest_Tuned_LogTarget (CHAMPION)"])
    
    print("\nSo sánh sai số Test trên nhóm thông số đã gặp trong Train vs chưa từng gặp:")
    grp_perf = test_preds_df.groupby("in_train_group").agg(
        count=("err", "count"),
        mae=("err", "mean"),
        median_ape=("actual_price_vnd", lambda s: np.median(test_preds_df.loc[s.index, "err"] / s * 100))
    )
    print(grp_perf)

if __name__ == "__main__":
    audit_datasets_and_distributions()
    audit_predictions_and_metrics()
    audit_feature_importance_and_permutation()
    audit_leakage_groups()
