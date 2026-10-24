"""Phân chia tập dữ liệu Huấn luyện / Kiểm tra (Train / Validation / Test Splits).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer

Module này thực hiện phân chia tập dữ liệu theo tỷ lệ 80% Train / 10% Validation / 10% Test:
- Đảm bảo tính tái lập 100% thông qua `random_state=42`.
- Phân tầng theo phân vị giá (Stratified by Target Quantiles) nhằm bảo đảm phân phối giá
  ở cả 3 tập đều đồng nhất (bao gồm cả phân khúc xe sang và xe phổ thông).
- Kiểm tra tính độc lập (Disjointness) giữa các tập (0% trùng lặp listing_id).
- Lưu trữ danh sách listing_ids và file dữ liệu chia tập vào `data/processed/splits/`.
- Xuất split_metadata.json đầy đủ checksum SHA-256 để phục vụ kiểm toán.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

DEFAULT_DATA_PATH = Path("data/processed/cars_clean_phase5.csv")
DEFAULT_SPLITS_DIR = Path("data/processed/splits")


def compute_sha256(filepath: Path | str) -> str:
    """Tính mã băm SHA-256 của file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()


def split_dataset(
    df: pd.DataFrame,
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    test_ratio: float = 0.1,
    random_state: int = 42,
    stratify_target_col: str | None = "price_vnd",
    n_stratify_bins: int = 10,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """Phân chia tập dữ liệu thành 3 tập Train / Validation / Test độc lập.

    Args:
        df: DataFrame dữ liệu đã làm sạch.
        train_ratio: Tỷ lệ tập huấn luyện (mặc định 0.8 = 80%).
        val_ratio: Tỷ lệ tập kiểm định (mặc định 0.1 = 10%).
        test_ratio: Tỷ lệ tập kiểm thử (mặc định 0.1 = 10%).
        random_state: Seed ngẫu nhiên cố định (mặc định 42).
        stratify_target_col: Tên cột mục tiêu dùng để phân tầng theo phân vị (hoặc None nếu random).
        n_stratify_bins: Số lượng bins phân tầng giá (mặc định 10 phân vị - deciles).

    Returns:
        Tuple gồm (df_train, df_val, df_test, metadata).
    """
    total_ratio = train_ratio + val_ratio + test_ratio
    if not np.isclose(total_ratio, 1.0):
        raise ValueError(f"Tổng tỷ lệ các tập phải bằng 1.0, hiện tại là: {total_ratio}")

    n_total = len(df)
    if n_total == 0:
        raise ValueError("DataFrame rỗng, không thể chia tập.")

    # Xác định nhãn phân tầng
    stratify_labels = None
    stratify_method = "Simple Random Split"
    if stratify_target_col and stratify_target_col in df.columns:
        valid_prices = df[stratify_target_col].dropna()
        if len(valid_prices) == len(df) and len(df) >= n_stratify_bins:
            try:
                # Phân vị giá làm các giỏ phân tầng
                stratify_labels = pd.qcut(df[stratify_target_col], q=n_stratify_bins, labels=False, duplicates="drop")
                stratify_method = f"Target Quantile Stratification ({n_stratify_bins} bins on {stratify_target_col})"
            except ValueError:
                stratify_labels = None

    # Bước 1: Tách Train vs Temp (Val + Test)
    temp_ratio = val_ratio + test_ratio
    df_train, df_temp = train_test_split(
        df,
        test_size=temp_ratio,
        random_state=random_state,
        stratify=stratify_labels,
    )

    # Bước 2: Tách Temp thành Validation và Test
    # Tỷ lệ tương đối giữa val và test trong temp
    val_rel_ratio = val_ratio / temp_ratio
    temp_stratify = None
    if stratify_labels is not None:
        temp_stratify = stratify_labels.loc[df_temp.index]

    df_val, df_test = train_test_split(
        df_temp,
        test_size=(1.0 - val_rel_ratio),
        random_state=random_state,
        stratify=temp_stratify,
    )

    # Kiểm tra tính rời rạc (Disjointness) theo listing_id hoặc index
    train_ids = set(df_train["listing_id"]) if "listing_id" in df_train.columns else set(df_train.index)
    val_ids = set(df_val["listing_id"]) if "listing_id" in df_val.columns else set(df_val.index)
    test_ids = set(df_test["listing_id"]) if "listing_id" in df_test.columns else set(df_test.index)

    overlap_train_val = train_ids.intersection(val_ids)
    overlap_train_test = train_ids.intersection(test_ids)
    overlap_val_test = val_ids.intersection(test_ids)

    if overlap_train_val or overlap_train_test or overlap_val_test:
        raise ValueError(
            f"Phát hiện trùng lặp ID giữa các tập!\n"
            f"Train-Val: {len(overlap_train_val)}, "
            f"Train-Test: {len(overlap_train_test)}, "
            f"Val-Test: {len(overlap_val_test)}"
        )

    metadata: Dict[str, Any] = {
        "split_design": "Train / Validation / Test 80-10-10 Split",
        "random_state": random_state,
        "split_ratios": {
            "train": train_ratio,
            "validation": val_ratio,
            "test": test_ratio,
        },
        "stratification_method": stratify_method,
        "sample_counts": {
            "total": n_total,
            "train": len(df_train),
            "validation": len(df_val),
            "test": len(df_test),
        },
        "percentages": {
            "train": round((len(df_train) / n_total) * 100, 2),
            "validation": round((len(df_val) / n_total) * 100, 2),
            "test": round((len(df_test) / n_total) * 100, 2),
        },
        "target_distribution_comparison": {
            "train_median_price": float(df_train["price_vnd"].median()) if "price_vnd" in df_train.columns else None,
            "val_median_price": float(df_val["price_vnd"].median()) if "price_vnd" in df_val.columns else None,
            "test_median_price": float(df_test["price_vnd"].median()) if "price_vnd" in df_test.columns else None,
        },
        "leakage_verification": {
            "train_val_overlap_count": 0,
            "train_test_overlap_count": 0,
            "val_test_overlap_count": 0,
            "is_strictly_disjoint": True,
        },
    }

    return df_train, df_val, df_test, metadata


def save_splits(
    df_train: pd.DataFrame,
    df_val: pd.DataFrame,
    df_test: pd.DataFrame,
    metadata: Dict[str, Any],
    output_dir: Path = DEFAULT_SPLITS_DIR,
) -> Dict[str, str]:
    """Lưu trữ các tập dữ liệu, danh sách ID và metadata JSON vào thư mục splits.

    Returns:
        Dict chứa đường dẫn và checksum SHA-256 của các file đã lưu.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    files_info: Dict[str, str] = {}

    # Lưu file CSV đầy đủ từng tập
    train_path = output_dir / "train.csv"
    val_path = output_dir / "val.csv"
    test_path = output_dir / "test.csv"

    df_train.to_csv(train_path, index=False, encoding="utf-8")
    df_val.to_csv(val_path, index=False, encoding="utf-8")
    df_test.to_csv(test_path, index=False, encoding="utf-8")

    files_info["train_csv"] = str(train_path)
    files_info["train_sha256"] = compute_sha256(train_path)
    files_info["val_csv"] = str(val_path)
    files_info["val_sha256"] = compute_sha256(val_path)
    files_info["test_csv"] = str(test_path)
    files_info["test_sha256"] = compute_sha256(test_path)

    # Lưu riêng danh sách listing_ids
    if "listing_id" in df_train.columns:
        train_ids_path = output_dir / "train_ids.csv"
        val_ids_path = output_dir / "val_ids.csv"
        test_ids_path = output_dir / "test_ids.csv"

        df_train[["listing_id"]].to_csv(train_ids_path, index=False, encoding="utf-8")
        df_val[["listing_id"]].to_csv(val_ids_path, index=False, encoding="utf-8")
        df_test[["listing_id"]].to_csv(test_ids_path, index=False, encoding="utf-8")

        files_info["train_ids_sha256"] = compute_sha256(train_ids_path)
        files_info["val_ids_sha256"] = compute_sha256(val_ids_path)
        files_info["test_ids_sha256"] = compute_sha256(test_ids_path)

    # Cập nhật thông tin file vào metadata và lưu metadata JSON
    metadata["saved_files"] = files_info
    meta_path = output_dir / "split_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return files_info


def load_splits(
    splits_dir: Path = DEFAULT_SPLITS_DIR,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Tải lại các tập Train, Validation, Test từ thư mục splits."""
    train_path = splits_dir / "train.csv"
    val_path = splits_dir / "val.csv"
    test_path = splits_dir / "test.csv"

    if not (train_path.exists() and val_path.exists() and test_path.exists()):
        raise FileNotFoundError(f"Không tìm thấy các file splits tại: {splits_dir}")

    df_train = pd.read_csv(train_path)
    df_val = pd.read_csv(val_path)
    df_test = pd.read_csv(test_path)

    return df_train, df_val, df_test


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    print(f"Bắt đầu phân chia tập dữ liệu từ: {DEFAULT_DATA_PATH}")
    if not DEFAULT_DATA_PATH.exists():
        print(f"Lỗi: Không tìm thấy {DEFAULT_DATA_PATH}. Vui lòng chạy prepare_modeling_data trước.")
        sys.exit(1)

    df_clean = pd.read_csv(DEFAULT_DATA_PATH)
    print(f"Dữ liệu nạp thành công: {len(df_clean):,} dòng.")

    train_df, val_df, test_df, meta = split_dataset(df_clean)
    print("Phân chia hoàn tất:")
    print(f"  Train: {len(train_df):,} dòng ({meta['percentages']['train']}%) - Median: {meta['target_distribution_comparison']['train_median_price']:,.0f} VND")
    print(f"  Val:   {len(val_df):,} dòng ({meta['percentages']['validation']}%) - Median: {meta['target_distribution_comparison']['val_median_price']:,.0f} VND")
    print(f"  Test:  {len(test_df):,} dòng ({meta['percentages']['test']}%) - Median: {meta['target_distribution_comparison']['test_median_price']:,.0f} VND")

    saved = save_splits(train_df, val_df, test_df, meta)
    print(f"Đã lưu các tập và metadata vào: {DEFAULT_SPLITS_DIR}")
    print(f"  Train SHA-256: {saved['train_sha256']}")
    print(f"  Val SHA-256:   {saved['val_sha256']}")
    print(f"  Test SHA-256:  {saved['test_sha256']}")
