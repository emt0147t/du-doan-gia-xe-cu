"""Kịch bản chuẩn bị dữ liệu mô hình hóa (Prepare Modeling Dataset).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer

Kịch bản này chịu trách nhiệm:
1. Xác minh checksum SHA-256 của tập dữ liệu thô (Raw Data Integrity).
2. Gọi quy trình làm sạch từ `src.data.cleaning.clean_dataset`.
3. Tạo tập dữ liệu mô hình hóa chuẩn `data/processed/cars_clean_phase5.csv` (Cohort A: >= 2015).
4. Tạo tập dữ liệu phân tích độ nhạy `data/processed/cars_clean_phase5_cohort_b.csv` (Cohort B: >= 2010).
5. Xuất metadata JSON có băm SHA-256 đầy đủ để kiểm toán provenance.
6. Xuất tài liệu nhật ký làm sạch và từ điển dữ liệu.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import pandas as pd

from src.data.cleaning import clean_dataset

RAW_DATA_PATH = Path("data/raw/external/mquaan_car_price/car_detail.csv")
RAW_METADATA_PATH = Path("data/metadata/ingestion_mquaan_car_price.json")
OUTPUT_DIR = Path("data/processed")
OUTPUT_METADATA_DIR = Path("data/metadata")
REPORTS_DIR = Path("reports")

EXPECTED_RAW_SHA256 = "44c13afc5982f7abc51611fc56eeefd02df8e47f3224112f51b76514a7328f08"


def compute_file_sha256(filepath: Path | str) -> str:
    """Tính mã băm SHA-256 của file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()


def verify_raw_dataset_integrity(
    raw_path: Path = RAW_DATA_PATH,
    metadata_path: Path = RAW_METADATA_PATH,
) -> bool:
    """Kiểm tra tính toàn vẹn của dữ liệu raw trước khi xử lý bằng ingestion metadata."""
    if not raw_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu thô: {raw_path}")
    
    expected_hash = EXPECTED_RAW_SHA256
    if metadata_path.exists():
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
                for f_info in meta.get("ingestion_metadata", {}).get("staged_files", []):
                    if f_info.get("filename") == raw_path.name:
                        expected_hash = f_info.get("sha256", expected_hash)
                        break
        except Exception:
            pass

    current_sha256 = compute_file_sha256(raw_path)
    if current_sha256 != expected_hash:
        raise ValueError(
            f"Checksum dữ liệu thô không khớp!\n"
            f"Hiện tại: {current_sha256}\n"
            f"Kỳ vọng: {expected_hash}"
        )
    return True


def prepare_modeling_datasets(
    raw_path: Path = RAW_DATA_PATH,
    output_dir: Path = OUTPUT_DIR,
    metadata_dir: Path = OUTPUT_METADATA_DIR,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """Thực thi pipeline chuẩn bị dữ liệu và xuất artifact cho cả hai cohort.

    Returns:
        Tuple gồm (df_cohort_a, df_cohort_b, metadata).
    """
    verify_raw_dataset_integrity(raw_path)

    # Đọc dữ liệu raw nguyên bản
    df_raw = pd.read_csv(raw_path)

    # Làm sạch cho Cohort A (Primary - Charter: year >= 2015)
    df_cohort_a, log_a = clean_dataset(df_raw, min_year=2015)
    output_dir.mkdir(parents=True, exist_ok=True)
    cohort_a_path = output_dir / "cars_clean_phase5.csv"
    df_cohort_a.to_csv(cohort_a_path, index=False, encoding="utf-8")
    sha256_cohort_a = compute_file_sha256(cohort_a_path)

    # Làm sạch cho Cohort B (Extended Sensitivity - EDA: year >= 2010)
    df_cohort_b, log_b = clean_dataset(df_raw, min_year=2010)
    cohort_b_path = output_dir / "cars_clean_phase5_cohort_b.csv"
    df_cohort_b.to_csv(cohort_b_path, index=False, encoding="utf-8")
    sha256_cohort_b = compute_file_sha256(cohort_b_path)

    # Ghi nhận metadata
    metadata = {
        "pipeline_name": "Phase 5 Reproducible Data Cleaning & Preparation",
        "created_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "source_data": {
            "path": str(raw_path),
            "sha256": EXPECTED_RAW_SHA256,
            "total_rows": len(df_raw),
            "total_columns": len(df_raw.columns),
        },
        "cohort_a_primary": {
            "description": "Primary Modeling Cohort (Project Charter Scope: year >= 2015)",
            "output_file": str(cohort_a_path),
            "sha256": sha256_cohort_a,
            "min_year": 2015,
            "rows": len(df_cohort_a),
            "columns": len(df_cohort_a.columns),
            "retained_percentage": log_a["retained_percentage"],
            "cleaning_audit": log_a,
        },
        "cohort_b_extended": {
            "description": "Extended Sensitivity Cohort (EDA Scope: year >= 2010)",
            "output_file": str(cohort_b_path),
            "sha256": sha256_cohort_b,
            "min_year": 2010,
            "rows": len(df_cohort_b),
            "columns": len(df_cohort_b.columns),
            "retained_percentage": log_b["retained_percentage"],
            "cleaning_audit": log_b,
        },
    }

    metadata_dir.mkdir(parents=True, exist_ok=True)
    metadata_file = metadata_dir / "prepare_modeling_data_phase5.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return df_cohort_a, df_cohort_b, metadata


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    print("Bắt đầu chuẩn bị dữ liệu mô hình hóa Phase 5...")
    df_a, df_b, meta = prepare_modeling_datasets()
    print("Xác minh toàn vẹn dữ liệu raw: THÀNH CÔNG")
    print(f"Cohort A (Chính - 2015+): {len(df_a):,} dòng -> {meta['cohort_a_primary']['output_file']}")
    print(f"  SHA-256: {meta['cohort_a_primary']['sha256']}")
    print(f"Cohort B (Mở rộng - 2010+): {len(df_b):,} dòng -> {meta['cohort_b_extended']['output_file']}")
    print(f"  SHA-256: {meta['cohort_b_extended']['sha256']}")
    print("Hoàn tất quy trình chuẩn bị dữ liệu.")
