"""Unit tests cho module phát hiện và gom nhóm bản ghi trùng lặp (tests/test_duplicate_groups.py).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & Independent ML Evaluation Reviewer
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.data.duplicate_groups import (
    classify_duplicate_candidates,
    compute_text_fingerprint,
    normalize_vietnamese_text,
)
from src.data.preprocessing import extract_features_and_target, NUMERIC_FEATURES, CATEGORICAL_FEATURES


def test_normalize_vietnamese_text_pii_scrubbing():
    """Kiểm tra hàm chuẩn hóa khử sạch số điện thoại cá nhân (PII) và ký tự thừa."""
    raw_text = "Xe đẹp chính chủ, liên hệ: 0912345678 hoặc 0987.654.321! Giá 450tr."
    norm_text = normalize_vietnamese_text(raw_text)

    # Không được chứa số điện thoại
    assert "0912345678" not in norm_text
    assert "0987654321" not in norm_text
    # Không còn chữ số hay dấu chấm câu
    assert not any(char.isdigit() for char in norm_text)
    assert "." not in norm_text
    assert "!" not in norm_text
    assert "xe đẹp chính chủ" in norm_text


def test_compute_text_fingerprint():
    """Kiểm tra tạo mã băm fingerprint khi văn bản >= 50 ký tự."""
    short_text = "Bán xe Vios cũ"
    assert compute_text_fingerprint(short_text, min_len=50) == ""

    long_text = "Xe gia đình sử dụng giữ gìn cẩn thận không đâm đụng ngập nước bảo dưỡng hãng định kỳ đầy đủ tiện nghi"
    fp = compute_text_fingerprint(long_text, min_len=50)
    assert len(fp) == 16
    assert isinstance(fp, str)

    # Đảm bảo tính bất biến (Idempotent)
    assert compute_text_fingerprint(long_text, min_len=50) == fp


def test_classify_duplicate_candidates_categories():
    """Kiểm tra phân loại chính xác 4 cấp độ tin cậy trùng lặp."""
    # Tạo DataFrame tổng hợp nhỏ
    sample_data = pd.DataFrame([
        # Cặp 1: Cùng mô tả dài + cùng brand + cùng model + cùng year -> HIGH_CONFIDENCE
        {
            "listing_id": "ID_01",
            "brand": "Toyota",
            "model": "Vios",
            "year": 2020.0,
            "mileage_km": 40000.0,
            "price_vnd": 450_000_000.0,
            "condition": "Xe đã dùng",
            "Mô tả": "Xe chính chủ đi lại cẩn thận cam kết không đâm đụng không ngập nước bảo dưỡng đầy đủ tại hãng",
        },
        {
            "listing_id": "ID_02",
            "brand": "Toyota",
            "model": "Vios",
            "year": 2020.0,
            "mileage_km": 40000.0,
            "price_vnd": 450_000_000.0,
            "condition": "Xe đã dùng",
            "Mô tả": "Xe chính chủ đi lại cẩn thận cam kết không đâm đụng không ngập nước bảo dưỡng đầy đủ tại hãng",
        },
        # Ca 2: Xe cũ ODO > 0 trùng 5 specs nhưng mô tả khác -> POSSIBLE_DUPLICATE
        {
            "listing_id": "ID_03",
            "brand": "Hyundai",
            "model": "Accent",
            "year": 2021.0,
            "mileage_km": 30000.0,
            "price_vnd": 480_000_000.0,
            "condition": "Xe đã dùng",
            "Mô tả": "Xe lướt chạy gia đình",
        },
        {
            "listing_id": "ID_04",
            "brand": "Hyundai",
            "model": "Accent",
            "year": 2021.0,
            "mileage_km": 30000.0,
            "price_vnd": 480_000_000.0,
            "condition": "Xe đã dùng",
            "Mô tả": "Màu trắng nguyên bản",
        },
        # Ca 3: Xe mới showroom ODO = 0 trùng 5 specs -> SIMILAR_SPEC_ONLY
        {
            "listing_id": "ID_05",
            "brand": "Kia",
            "model": "Morning",
            "year": 2023.0,
            "mileage_km": 0.0,
            "price_vnd": 389_000_000.0,
            "condition": "Xe mới",
            "Mô tả": "Xe giao ngay đủ màu",
        },
        {
            "listing_id": "ID_06",
            "brand": "Kia",
            "model": "Morning",
            "year": 2023.0,
            "mileage_km": 0.0,
            "price_vnd": 389_000_000.0,
            "condition": "Xe mới",
            "Mô tả": "Ưu đãi giá tốt trong tháng",
        },
        # Ca 4: Xe độc lập -> UNRELATED_OR_UNRESOLVED
        {
            "listing_id": "ID_07",
            "brand": "Mazda",
            "model": "CX-5",
            "year": 2022.0,
            "mileage_km": 15000.0,
            "price_vnd": 790_000_000.0,
            "condition": "Xe đã dùng",
            "Mô tả": "Bản Premium 2.0 rất mới",
        },
    ])

    res_df = classify_duplicate_candidates(sample_data)

    # ID_01 và ID_02 phải là HIGH_CONFIDENCE và có cùng record_group_id
    assert res_df.loc[res_df["listing_id"] == "ID_01", "duplicate_category"].iloc[0] == "HIGH_CONFIDENCE_DUPLICATE"
    assert res_df.loc[res_df["listing_id"] == "ID_02", "duplicate_category"].iloc[0] == "HIGH_CONFIDENCE_DUPLICATE"
    assert (
        res_df.loc[res_df["listing_id"] == "ID_01", "record_group_id"].iloc[0]
        == res_df.loc[res_df["listing_id"] == "ID_02", "record_group_id"].iloc[0]
    )

    # ID_03 và ID_04 phải là POSSIBLE_DUPLICATE và KHÔNG được gộp chung record_group_id
    assert res_df.loc[res_df["listing_id"] == "ID_03", "duplicate_category"].iloc[0] == "POSSIBLE_DUPLICATE"
    assert res_df.loc[res_df["listing_id"] == "ID_04", "duplicate_category"].iloc[0] == "POSSIBLE_DUPLICATE"
    assert (
        res_df.loc[res_df["listing_id"] == "ID_03", "record_group_id"].iloc[0]
        != res_df.loc[res_df["listing_id"] == "ID_04", "record_group_id"].iloc[0]
    )

    # ID_05 và ID_06 phải là SIMILAR_SPEC_ONLY và KHÔNG được gộp chung
    assert res_df.loc[res_df["listing_id"] == "ID_05", "duplicate_category"].iloc[0] == "SIMILAR_SPEC_ONLY"
    assert res_df.loc[res_df["listing_id"] == "ID_06", "duplicate_category"].iloc[0] == "SIMILAR_SPEC_ONLY"
    assert (
        res_df.loc[res_df["listing_id"] == "ID_05", "record_group_id"].iloc[0]
        != res_df.loc[res_df["listing_id"] == "ID_06", "record_group_id"].iloc[0]
    )

    # ID_07 phải là UNRELATED
    assert res_df.loc[res_df["listing_id"] == "ID_07", "duplicate_category"].iloc[0] == "UNRELATED_OR_UNRESOLVED"


def test_group_aware_split_disjointness():
    """Kiểm tra tính rời rạc 100% của tập chia group_aware_v1."""
    split_dir = Path("data/processed/splits_grouped_v1")
    if not (split_dir / "train.csv").exists():
        pytest.skip("Chưa tạo splits_grouped_v1")

    train_df = pd.read_csv(split_dir / "train.csv")
    val_df = pd.read_csv(split_dir / "val.csv")
    test_df = pd.read_csv(split_dir / "test.csv")

    s_tr = set(train_df["record_group_id"])
    s_va = set(val_df["record_group_id"])
    s_te = set(test_df["record_group_id"])

    # Không trùng lặp bất kỳ record_group_id nào
    assert len(s_tr & s_va) == 0
    assert len(s_tr & s_te) == 0
    assert len(s_va & s_te) == 0


def test_record_group_id_not_in_feature_matrix():
    """Đảm bảo cột record_group_id và các cột audit không bị rò rỉ vào ma trận đặc trưng X."""
    split_dir = Path("data/processed/splits_grouped_v1")
    if not (split_dir / "train.csv").exists():
        pytest.skip("Chưa tạo splits_grouped_v1")

    train_df = pd.read_csv(split_dir / "train.csv")
    X, y = extract_features_and_target(train_df)

    assert "record_group_id" not in X.columns
    assert "duplicate_category" not in X.columns
    assert "desc_fingerprint" not in X.columns
    assert "Mô tả" not in X.columns
    assert "Tên xe" not in X.columns
    assert len(X.columns) == len(NUMERIC_FEATURES) + len(CATEGORICAL_FEATURES)


def test_split_grouped_metadata_no_pii():
    """Kiểm tra file metadata của split không chứa số điện thoại hoặc văn bản mô tả."""
    meta_path = Path("data/processed/splits_grouped_v1/split_grouped_metadata.json")
    if not meta_path.exists():
        pytest.skip("Chưa có split_grouped_metadata.json")

    with open(meta_path, "r", encoding="utf-8") as f:
        meta_str = f.read()

    # Kiểm tra không chứa chuỗi số điện thoại 10 chữ số
    import re
    phones = re.findall(r"\b0[35789]\d{8}\b", meta_str)
    assert len(phones) == 0
