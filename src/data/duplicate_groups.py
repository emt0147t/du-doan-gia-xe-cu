"""Module phát hiện và gom nhóm bản ghi trùng lặp có kiểm soát (Record Grouping & Deduplication).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & Independent ML Evaluation Reviewer

Module này cung cấp:
- Chuẩn hóa văn bản và tạo fingerprint (băm SHA-256 nội dung sau khi lọc bỏ PII).
- Phân loại ứng viên trùng lặp thành 4 cấp độ:
    1. HIGH_CONFIDENCE_DUPLICATE: Trùng văn bản mô tả dài (>=50 ký tự) cùng hãng, dòng xe và năm sản xuất.
    2. POSSIBLE_DUPLICATE: Xe cũ trùng 5 thông số nhưng mô tả khác biệt hoặc ngắn (không tự động gộp).
    3. SIMILAR_SPEC_ONLY: Xe mới showroom trùng thông số và giá niêm yết (không tự động gộp).
    4. UNRELATED_OR_UNRESOLVED: Tin đăng độc lập hoặc chia sẻ slogan mẫu giữa các hãng xe khác nhau.
- Tạo `record_group_id` cho dữ liệu bảng nhằm phục vụ Group-Aware Split (không làm feature dự đoán).
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd


def normalize_vietnamese_text(text: Any) -> str:
    """Chuẩn hóa văn bản tiếng Việt và khử hoàn toàn PII (SĐT, ký tự đặc biệt)."""
    if text is None or pd.isna(text) or not isinstance(text, str):
        return ""

    t = text.lower()
    # 1. Khử số điện thoại di động Việt Nam (10-11 số) để chặn PII
    t = re.sub(r"\b(0[35789]\d{8})\b", " ", t)
    t = re.sub(r"\b(0\d{9,10})\b", " ", t)
    t = re.sub(r"\b(\+84\d{9,10})\b", " ", t)

    # 2. Loại bỏ chữ số và ký tự dấu câu để loại bỏ giá/số lẻ ngẫu nhiên
    t = re.sub(r"[\d\.\,\-\:\/\(\)\+\*\_\"\'\`\!\?\;\#\@\$\%\^\&\=\~\\\|\[\]\{\}]", " ", t)

    # 3. Chuẩn hóa khoảng trắng
    t = re.sub(r"\s+", " ", t).strip()
    return t


def compute_text_fingerprint(text: Any, min_len: int = 50) -> str:
    """Tạo mã băm fingerprint SHA-256 (16 ký tự) cho đoạn văn bản có độ dài >= min_len."""
    norm_t = normalize_vietnamese_text(text)
    if len(norm_t) < min_len:
        return ""
    return hashlib.sha256(norm_t.encode("utf-8")).hexdigest()[:16]


def classify_duplicate_candidates(df: pd.DataFrame) -> pd.DataFrame:
    """Phân loại mọi bản ghi trong DataFrame thành 4 cấp độ tin cậy trùng lặp.

    Returns:
        DataFrame với 3 cột mới:
        - 'desc_fingerprint': Mã băm mô tả chuẩn hóa
        - 'duplicate_category': Một trong 4 phân loại
        - 'record_group_id': Định danh nhóm dùng cho split (chỉ gộp HIGH_CONFIDENCE_DUPLICATE)
    """
    df_out = df.copy()

    # 1. Tạo fingerprint mô tả
    desc_col = "Mô tả" if "Mô tả" in df_out.columns else None
    if desc_col is not None:
        df_out["desc_fingerprint"] = [compute_text_fingerprint(d, min_len=50) for d in df_out[desc_col]]
    else:
        df_out["desc_fingerprint"] = ""

    # Đảm bảo có các cột chuẩn đoán
    brand_col = "brand" if "brand" in df_out.columns else "Hãng"
    model_col = "model" if "model" in df_out.columns else "Grade"
    year_col = "year" if "year" in df_out.columns else "Năm sản xuất"
    mileage_col = "mileage_km" if "mileage_km" in df_out.columns else "Số Km đã đi"
    price_col = "price_vnd" if "price_vnd" in df_out.columns else "Giá"
    condition_col = "condition" if "condition" in df_out.columns else "Tình trạng"
    id_col = "listing_id" if "listing_id" in df_out.columns else "Mã tin"

    # Mặc định khởi tạo
    df_out["duplicate_category"] = "UNRELATED_OR_UNRESOLVED"
    df_out["record_group_id"] = [f"SINGLE_{row_id}" for row_id in df_out[id_col]]

    # 2. Nhận diện HIGH_CONFIDENCE_DUPLICATE
    # Điều kiện: Cùng desc_fingerprint (>=50 chars) + cùng brand + cùng model + cùng year có >= 2 tin
    has_fp = df_out["desc_fingerprint"] != ""
    grouped_hc = df_out[has_fp].groupby(["desc_fingerprint", brand_col, model_col, year_col])

    for (fp, b, m, y), idxs in grouped_hc.groups.items():
        if len(idxs) >= 2:
            group_key = f"GRP_HC_{fp[:8]}_{abs(hash((b, m, y))) % 100000:05d}"
            df_out.loc[idxs, "duplicate_category"] = "HIGH_CONFIDENCE_DUPLICATE"
            df_out.loc[idxs, "record_group_id"] = group_key

    # 3. Nhận diện SIMILAR_SPEC_ONLY (Xe mới Showroom trùng thông số)
    # Xe mới showroom (condition=='Xe mới' hoặc mileage_km==0) có >= 2 tin trùng 5 thông số
    # nhưng CHƯA được gộp vào HIGH_CONFIDENCE_DUPLICATE
    is_new = (df_out[condition_col].astype(str).str.strip() == "Xe mới") | (pd.to_numeric(df_out[mileage_col], errors="coerce") == 0)
    spec_cols_5 = [brand_col, model_col, year_col, mileage_col, price_col]

    grouped_new_spec = df_out[is_new].groupby(spec_cols_5)
    for _, idxs in grouped_new_spec.groups.items():
        if len(idxs) >= 2:
            # Chỉ gắn nhãn nếu chưa thuộc HIGH_CONFIDENCE
            mask_unresolved = df_out.loc[idxs, "duplicate_category"] == "UNRELATED_OR_UNRESOLVED"
            target_idxs = idxs[mask_unresolved]
            df_out.loc[target_idxs, "duplicate_category"] = "SIMILAR_SPEC_ONLY"
            # TUYỆT ĐỐI KHÔNG GỘP GROUP_ID CHO SIMILAR_SPEC_ONLY (Giữ SINGLE_id)

    # 4. Nhận diện POSSIBLE_DUPLICATE (Xe cũ trùng 5 thông số nhưng mô tả khác)
    # Xe cũ (condition != 'Xe mới' và mileage_km > 0) có >= 2 tin trùng 5 thông số
    is_used = (~is_new) & (pd.to_numeric(df_out[mileage_col], errors="coerce") > 0)
    grouped_used_spec = df_out[is_used].groupby(spec_cols_5)
    for _, idxs in grouped_used_spec.groups.items():
        if len(idxs) >= 2:
            mask_unresolved = df_out.loc[idxs, "duplicate_category"] == "UNRELATED_OR_UNRESOLVED"
            target_idxs = idxs[mask_unresolved]
            df_out.loc[target_idxs, "duplicate_category"] = "POSSIBLE_DUPLICATE"
            # TUYỆT ĐỐI KHÔNG GỘP GROUP_ID CHO POSSIBLE_DUPLICATE (Giữ SINGLE_id)

    return df_out


def audit_group_leakage_across_splits(
    df_with_groups: pd.DataFrame,
    train_ids: set,
    val_ids: set,
    test_ids: set,
    id_col: str = "listing_id",
) -> Dict[str, Any]:
    """Kiểm toán mức độ rò rỉ group_id và duplicate categories giữa các tập Train, Val và Test cũ."""
    df = df_with_groups.copy()
    id_series = df[id_col].astype(str)

    train_mask = id_series.isin(train_ids)
    val_mask = id_series.isin(val_ids)
    test_mask = id_series.isin(test_ids)

    df_train = df[train_mask]
    df_val = df[val_mask]
    df_test = df[test_mask]

    # Kiểm tra Group ID
    hc_train_groups = set(df_train[df_train["duplicate_category"] == "HIGH_CONFIDENCE_DUPLICATE"]["record_group_id"])
    hc_val_groups = set(df_val[df_val["duplicate_category"] == "HIGH_CONFIDENCE_DUPLICATE"]["record_group_id"])
    hc_test_groups = set(df_test[df_test["duplicate_category"] == "HIGH_CONFIDENCE_DUPLICATE"]["record_group_id"])

    val_hc_in_train = len(hc_val_groups & hc_train_groups)
    test_hc_in_train = len(hc_test_groups & hc_train_groups)
    val_test_hc = len(hc_val_groups & hc_test_groups)

    val_rows_leaked = df_val["record_group_id"].isin(hc_train_groups).sum()
    test_rows_leaked = df_test["record_group_id"].isin(hc_train_groups).sum()

    category_counts = df["duplicate_category"].value_counts().to_dict()

    return {
        "total_rows": len(df),
        "category_counts": category_counts,
        "high_confidence_groups_total": df[df["duplicate_category"] == "HIGH_CONFIDENCE_DUPLICATE"]["record_group_id"].nunique(),
        "old_split_leakage": {
            "val_groups_in_train": val_hc_in_train,
            "val_rows_affected": int(val_rows_leaked),
            "val_rows_pct": round(val_rows_leaked / len(df_val) * 100, 2) if len(df_val) > 0 else 0.0,
            "test_groups_in_train": test_hc_in_train,
            "test_rows_affected": int(test_rows_leaked),
            "test_rows_pct": round(test_rows_leaked / len(df_test) * 100, 2) if len(df_test) > 0 else 0.0,
            "val_test_shared_groups": val_test_hc,
        },
    }
