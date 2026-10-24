"""Tạo bộ phân chia tập dữ liệu theo nhóm độc lập (Group-Aware Split v1).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & Independent ML Evaluation Reviewer

Nguyên tắc:
- Sử dụng StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=42)
- Toàn bộ các bản ghi trong cùng một `record_group_id` nằm trọn vẹn trong 1 tập duy nhất.
- Tỷ lệ: Train 80% (8 folds), Val 10% (1 fold), Test 10% (1 fold).
- Tuyệt đối không ghi đè lên thư mục data/processed/splits/.
- Lưu tại data/processed/splits_grouped_v1/.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from src.data.duplicate_groups import classify_duplicate_candidates

SPLIT_DIR = Path("data/processed/splits_grouped_v1")
SPLIT_DIR.mkdir(parents=True, exist_ok=True)


def compute_file_sha256(filepath: Path | str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()


def main():
    print("=" * 80)
    print("TẠO BỘ CHIA TẬP GROUP-AWARE SPLIT V1 (STRATIFIED GROUP SPLITTING)")
    print("=" * 80)

    raw_clean_path = Path("data/processed/cars_clean_phase5.csv")
    df = pd.read_csv(raw_clean_path)
    print(f"Dữ liệu gốc Cohort A: {len(df):,} dòng.")

    # 1. Phân loại và gán record_group_id
    df_grouped = classify_duplicate_candidates(df)
    n_groups = df_grouped["record_group_id"].nunique()
    print(f"Tổng số nhóm (record_group_id): {n_groups:,}")

    # 2. Tạo 10 phân vị giá cho stratification
    df_grouped["price_bin"] = pd.qcut(df_grouped["price_vnd"], q=10, labels=False, duplicates="drop")

    # 3. Phân chia bằng StratifiedGroupKFold
    sgkf = StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=42)
    folds = list(sgkf.split(df_grouped, df_grouped["price_bin"], df_grouped["record_group_id"]))

    train_idx = np.concatenate([folds[i][1] for i in range(8)])
    val_idx = folds[8][1]
    test_idx = folds[9][1]

    train_df = df_grouped.iloc[train_idx].copy().reset_index(drop=True)
    val_df = df_grouped.iloc[val_idx].copy().reset_index(drop=True)
    test_df = df_grouped.iloc[test_idx].copy().reset_index(drop=True)

    print(f"\nQuy mô các tập sau khi chia nhóm:")
    print(f"  Train: {len(train_df):,} dòng ({len(train_df)/len(df)*100:.2f}%) | Groups: {train_df['record_group_id'].nunique():,}")
    print(f"  Val:   {len(val_df):,} dòng ({len(val_df)/len(df)*100:.2f}%)   | Groups: {val_df['record_group_id'].nunique():,}")
    print(f"  Test:  {len(test_df):,} dòng ({len(test_df)/len(df)*100:.2f}%)   | Groups: {test_df['record_group_id'].nunique():,}")

    # 4. Kiểm tra toàn vẹn không trùng lặp group
    s_tr = set(train_df["record_group_id"])
    s_va = set(val_df["record_group_id"])
    s_te = set(test_df["record_group_id"])

    assert len(s_tr & s_va) == 0, "LỖI: Phát hiện trùng record_group_id giữa Train và Val!"
    assert len(s_tr & s_te) == 0, "LỖI: Phát hiện trùng record_group_id giữa Train và Test!"
    assert len(s_va & s_te) == 0, "LỖI: Phát hiện trùng record_group_id giữa Val và Test!"
    print("-> XÁC NHẬN: 100% group_id hoàn toàn rời rạc giữa Train, Val và Test (0% overlap).")

    # 5. Lưu trữ tệp split
    train_path = SPLIT_DIR / "train.csv"
    val_path = SPLIT_DIR / "val.csv"
    test_path = SPLIT_DIR / "test.csv"
    train_ids_path = SPLIT_DIR / "train_ids.csv"
    val_ids_path = SPLIT_DIR / "val_ids.csv"
    test_ids_path = SPLIT_DIR / "test_ids.csv"

    train_df.to_csv(train_path, index=False, encoding="utf-8")
    val_df.to_csv(val_path, index=False, encoding="utf-8")
    test_df.to_csv(test_path, index=False, encoding="utf-8")

    train_df[["listing_id", "record_group_id"]].to_csv(train_ids_path, index=False, encoding="utf-8")
    val_df[["listing_id", "record_group_id"]].to_csv(val_ids_path, index=False, encoding="utf-8")
    test_df[["listing_id", "record_group_id"]].to_csv(test_ids_path, index=False, encoding="utf-8")

    # Tính toán SHA256
    train_hash = compute_file_sha256(train_path)
    val_hash = compute_file_sha256(val_path)
    test_hash = compute_file_sha256(test_path)

    # 6. Tạo metadata
    metadata = {
        "split_version": "splits_grouped_v1",
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "strategy": "StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=42)",
        "grouping_method": "src.data.duplicate_groups.classify_duplicate_candidates (Grouping HIGH_CONFIDENCE_DUPLICATE by desc_fingerprint + brand + model + year)",
        "target_variable": "price_vnd (Stratified across 10 quantiles)",
        "random_seed": 42,
        "total_rows": len(df),
        "total_groups": n_groups,
        "splits": {
            "train": {
                "file": str(train_path),
                "rows": len(train_df),
                "pct": round(len(train_df) / len(df) * 100, 2),
                "groups": train_df["record_group_id"].nunique(),
                "price_median_vnd": float(train_df["price_vnd"].median()),
                "price_mean_vnd": float(train_df["price_vnd"].mean()),
                "price_std_vnd": float(train_df["price_vnd"].std()),
                "sha256": train_hash,
            },
            "val": {
                "file": str(val_path),
                "rows": len(val_df),
                "pct": round(len(val_df) / len(df) * 100, 2),
                "groups": val_df["record_group_id"].nunique(),
                "price_median_vnd": float(val_df["price_vnd"].median()),
                "price_mean_vnd": float(val_df["price_vnd"].mean()),
                "price_std_vnd": float(val_df["price_vnd"].std()),
                "sha256": val_hash,
            },
            "test": {
                "file": str(test_path),
                "rows": len(test_df),
                "pct": round(len(test_df) / len(df) * 100, 2),
                "groups": test_df["record_group_id"].nunique(),
                "price_median_vnd": float(test_df["price_vnd"].median()),
                "price_mean_vnd": float(test_df["price_vnd"].mean()),
                "price_std_vnd": float(test_df["price_vnd"].std()),
                "sha256": test_hash,
            },
        },
        "known_limitations": [
            "Không thể gom nhóm các xe khác nhau của cùng 1 người bán do bảng seller.csv bị loại bỏ nhằm bảo vệ PII.",
            "Không có số khung xe (VIN) trên website Bonbanh để xác thực xe vật lý duy nhất.",
            "Các xe mới tại showroom (SIMILAR_SPEC_ONLY) và xe cũ trùng 5 thông số nhưng khác mô tả (POSSIBLE_DUPLICATE) không bị gộp nhằm tránh dương tính giả.",
        ],
    }

    meta_path = SPLIT_DIR / "split_grouped_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\nĐã lưu metadata kiểm toán: {meta_path}")
    print("HOÀN THÀNH TẠO BỘ CHIA TẬP GROUP-AWARE SPLIT V1.")


if __name__ == "__main__":
    main()
