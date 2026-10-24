"""Kịch bản kiểm toán độc lập Phase 5 (Independent Audit of Phase 5).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Reviewer
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Set
import numpy as np
import pandas as pd

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

RAW_DETAIL_PATH = Path("data/raw/external/mquaan_car_price/car_detail.csv")
RAW_PROCESSED_PATH = Path("data/raw/external/mquaan_car_price/car_sell_processed.csv")
RAW_METADATA_PATH = Path("data/metadata/ingestion_mquaan_car_price.json")
PHASE4_CLEAN_PATH = Path("data/processed/cars_clean_phase4.csv")
PHASE5_COHORT_A_PATH = Path("data/processed/cars_clean_phase5.csv")
PHASE5_COHORT_B_PATH = Path("data/processed/cars_clean_phase5_cohort_b.csv")
SPLITS_DIR = Path("data/processed/splits")


def compute_sha256(filepath: Path | str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()


def audit_raw_integrity():
    print("=" * 80)
    print("1. KIỂM TOÁN TÍNH TOÀN VẸN DỮ LIỆU THÔ (RAW INTEGRITY)")
    print("=" * 80)
    with open(RAW_METADATA_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)

    for item in meta["ingestion_metadata"]["staged_files"]:
        fn = item["filename"]
        fp = Path("data/raw/external/mquaan_car_price") / fn
        if fp.exists():
            actual_sha = compute_sha256(fp)
            match = (actual_sha == item["sha256"])
            print(f"File: {fn:<25} | Bytes: {fp.stat().st_size:<10} | Match: {match}")
            if not match:
                print(f"  Expected: {item['sha256']}")
                print(f"  Actual:   {actual_sha}")
        else:
            print(f"File: {fn:<25} | KHÔNG TỒN TẠI!")


def audit_row_counts_and_filters():
    print("\n" + "=" * 80)
    print("2. ĐỘC LẬP TÁI TÍNH TOÁN SỐ LƯỢNG HÀNG VÀ CÁC BƯỚC LỌC")
    print("=" * 80)
    df_raw = pd.read_csv(RAW_DETAIL_PATH)
    n_raw = len(df_raw)
    print(f"Tổng số hàng raw ban đầu: {n_raw:,}")

    # A. Parse giá độc lập bằng logic cơ bản
    # Regex parse giá tiếng Việt
    def _parse_vnd(val):
        if pd.isna(val):
            return np.nan
        s = str(val).strip().lower()
        if "liên hệ" in s or "thỏa thuận" in s or "call" in s or not s:
            return np.nan
        # Pattern X tỷ Y triệu
        ty_m = re.search(r"(\d+(?:[.,]\d+)?)\s*tỷ", s)
        tr_m = re.search(r"(\d+(?:[.,]\d+)?)\s*triệu", s)
        vnd = 0.0
        found = False
        if ty_m:
            vnd += float(ty_m.group(1).replace(",", ".")) * 1e9
            found = True
        if tr_m:
            vnd += float(tr_m.group(1).replace(",", ".")) * 1e6
            found = True
        if found:
            return vnd
        # Thử parse số thuần
        s_clean = s.replace(".", "").replace(",", "").replace(" ", "").replace("vnd", "").replace("đ", "")
        if s_clean.isdigit():
            return float(s_clean)
        return np.nan

    parsed_prices = df_raw["Giá"].apply(_parse_vnd)
    n_valid_price = parsed_prices.notna().sum()
    n_missing_price = parsed_prices.isna().sum()
    print(f"Số giá parse thành công: {n_valid_price:,} ({n_valid_price/n_raw*100:.2f}%)")
    print(f"Số giá thiếu/liên hệ:      {n_missing_price:,} ({n_missing_price/n_raw*100:.2f}%)")

    # Target bounds
    p_under_30m = (parsed_prices < 30_000_000).sum()
    p_over_50b = (parsed_prices > 50_000_000_000).sum()
    p_valid_range = ((parsed_prices >= 30_000_000) & (parsed_prices <= 50_000_000_000)).sum()
    print(f"Số giá < 30 triệu VND:     {p_under_30m:,}")
    print(f"Số giá > 50 tỷ VND:        {p_over_50b:,}")
    print(f"Số giá trong [30M, 50B]:   {p_valid_range:,}")

    # B. Năm sản xuất
    years = pd.to_numeric(df_raw["Năm sản xuất"], errors="coerce")
    n_missing_year = years.isna().sum()
    print(f"\nSố dòng thiếu Năm sản xuất: {n_missing_year:,}")
    print(f"Phạm vi năm: min={years.min():.0f}, max={years.max():.0f}")

    # C. Phân bố theo năm
    y_ge_2015 = (years >= 2015).sum()
    y_ge_2010 = (years >= 2010).sum()
    y_2010_2014 = ((years >= 2010) & (years < 2015)).sum()
    y_lt_2010 = (years < 2010).sum()
    print(f"Số xe có năm >= 2015 (Cohort A raw): {y_ge_2015:,}")
    print(f"Số xe có năm >= 2010 (Cohort B raw): {y_ge_2010:,}")
    print(f"Số xe năm 2010 - 2014:               {y_2010_2014:,}")
    print(f"Số xe năm < 2010:                    {y_lt_2010:,}")

    # D. Hộp số (Transmission)
    trans = df_raw["Hộp số"].astype(str).str.strip()
    print(f"\nPhân phối Hộp số trên toàn bộ raw data:")
    print(trans.value_counts(dropna=False))

    # E. Số km (Mileage)
    def _parse_km(val):
        if pd.isna(val):
            return np.nan
        s = str(val).lower().replace("km", "").replace(",", "").replace(".", "").strip()
        try:
            return float(s)
        except:
            return np.nan

    km = df_raw["Số Km đã đi"].apply(_parse_km)
    km_zero = (km == 0).sum()
    km_gt_1m = (km > 1_000_000).sum()
    km_na = km.isna().sum()
    print(f"\nSố xe có ODO = 0:          {km_zero:,}")
    print(f"Số xe có ODO > 1,000,000:  {km_gt_1m:,}")
    print(f"Số xe có ODO khuyết/NaN:   {km_na:,}")

    return df_raw, parsed_prices, years, trans, km


def audit_cohort_b_discrepancy(df_raw, parsed_prices, years, trans, km):
    print("\n" + "=" * 80)
    print("3. ĐIỀU TRA CHÊNH LỆCH 70 BẢN GHI COHORT B (PHASE 4: 27,229 vs PHASE 5: 27,299)")
    print("=" * 80)

    # Đọc Phase 4 clean
    df_p4 = pd.read_csv(PHASE4_CLEAN_PATH)
    p4_cohort_b = df_p4[df_p4["year"] >= 2010]
    n_p4_b = len(p4_cohort_b)
    print(f"Số dòng Phase 4 có year >= 2010: {n_p4_b:,}")

    # Đọc Phase 5 cohort b
    df_p5_b = pd.read_csv(PHASE5_COHORT_B_PATH)
    n_p5_b = len(df_p5_b)
    print(f"Số dòng Phase 5 Cohort B clean:  {n_p5_b:,}")
    print(f"Chênh lệch thực tế: {n_p5_b - n_p4_b} dòng.")

    # Tìm các listing_id có trong Phase 5 Cohort B nhưng không có trong Phase 4 (hoặc ngược lại)
    # Lưu ý: Mã tin trong df_raw / df_p4
    id_col_p4 = "Mã tin" if "Mã tin" in df_p4.columns else "listing_id"
    id_col_p5 = "listing_id" if "listing_id" in df_p5_b.columns else "Mã tin"

    p4_ids = set(p4_cohort_b[id_col_p4].astype(str))
    p5_ids = set(df_p5_b[id_col_p5].astype(str))

    in_p5_not_p4 = p5_ids - p4_ids
    in_p4_not_p5 = p4_ids - p5_ids

    print(f"Số ID có trong Phase 5 Cohort B nhưng KHÔNG có trong Phase 4 (year>=2010): {len(in_p5_not_p4)}")
    print(f"Số ID có trong Phase 4 (year>=2010) nhưng KHÔNG có trong Phase 5 Cohort B: {len(in_p4_not_p5)}")

    if in_p5_not_p4:
        # Lấy thông tin các dòng này từ df_raw
        diff_raw = df_raw[df_raw["Mã tin"].astype(str).isin(in_p5_not_p4)]
        print("\nThông tin các dòng xuất hiện trong Phase 5 nhưng bị loại ở Phase 4:")
        print(f"Số lượng: {len(diff_raw)}")
        print("Phân phối năm:")
        print(diff_raw["Năm sản xuất"].value_counts())
        print("Phân phối Tình trạng:")
        print(diff_raw["Tình trạng"].value_counts())
        print("Phân phối Hộp số:")
        print(diff_raw["Hộp số"].value_counts())
        print("Mẫu 5 dòng đầu tiên:")
        for idx, r in diff_raw.head(5).iterrows():
            print(f"  Mã tin: {r['Mã tin']} | Năm: {r['Năm sản xuất']} | Giá: {r['Giá']} | Km: {r['Số Km đã đi']} | Hộp số: {r['Hộp số']}")


def audit_splits_and_leakage():
    print("\n" + "=" * 80)
    print("4. KIỂM TOÁN SPLITS VÀ NGUY CƠ RÒ RỈ NEAR-DUPLICATES")
    print("=" * 80)
    train_df = pd.read_csv(SPLITS_DIR / "train.csv")
    val_df = pd.read_csv(SPLITS_DIR / "val.csv")
    test_df = pd.read_csv(SPLITS_DIR / "test.csv")

    with open(SPLITS_DIR / "split_metadata.json", "r", encoding="utf-8") as f:
        meta_split = json.load(f)

    print(f"Train rows: {len(train_df):,} (meta: {meta_split['sample_counts']['train']:,})")
    print(f"Val rows:   {len(val_df):,} (meta: {meta_split['sample_counts']['validation']:,})")
    print(f"Test rows:  {len(test_df):,} (meta: {meta_split['sample_counts']['test']:,})")

    # Kiểm tra checksum các file split
    for split_name in ["train", "val", "test"]:
        csv_file = SPLITS_DIR / f"{split_name}.csv"
        actual_hash = compute_sha256(csv_file)
        expected_hash = meta_split["saved_files"].get(f"{split_name}_sha256")
        print(f"{split_name}.csv checksum match: {actual_hash == expected_hash} ({actual_hash[:16]}...)")

    # Near duplicate check across splits
    def make_spec_key(df):
        return df["brand"].astype(str) + "||" + df["model"].astype(str) + "||" + df["year"].astype(str) + "||" + df["mileage_km"].astype(str) + "||" + df["price_vnd"].astype(str)

    train_k = set(make_spec_key(train_df))
    val_k = set(make_spec_key(val_df))
    test_k = set(make_spec_key(test_df))

    print(f"\nSpec tuple overlap Train-Val:  {len(train_k & val_k)}")
    print(f"Spec tuple overlap Train-Test: {len(train_k & test_k)}")
    print(f"Spec tuple overlap Val-Test:   {len(val_k & test_k)}")

    # Kiểm tra xem bao nhiêu overlap là Xe mới / ODO = 0
    overlap_tv = train_k & val_k
    val_overlap = val_df[make_spec_key(val_df).isin(overlap_tv)]
    print(f"Trong {len(val_overlap)} dòng Val trùng spec với Train:")
    print(f"  Xe mới (condition='Xe mới'): { (val_overlap['condition'] == 'Xe mới').sum()} ({ (val_overlap['condition'] == 'Xe mới').sum() / len(val_overlap)*100:.1f}%)")
    print(f"  ODO = 0 (is_zero_mileage=1): { (val_overlap['is_zero_mileage'] == 1).sum()} ({ (val_overlap['is_zero_mileage'] == 1).sum() / len(val_overlap)*100:.1f}%)")
    print(f"  Xe đã dùng có ODO > 0:       { ((val_overlap['condition'] != 'Xe mới') & (val_overlap['is_zero_mileage'] == 0)).sum()}")


def audit_transmission_details():
    print("\n" + "=" * 80)
    print("5. CHI TIẾT KIỂM TOÁN HỘP SỐ (TRANSMISSION AUDIT)")
    print("=" * 80)
    df_raw = pd.read_csv(RAW_DETAIL_PATH)
    odd_trans = df_raw[df_raw["Hộp số"].isin(["-", "Số hỗn hợp"])].copy()
    print(f"Tổng số bản ghi hộp số bất thường: {len(odd_trans)}")

    for idx, r in odd_trans.iterrows():
        print(f"ID: {r['Mã tin']:<8} | Năm: {str(r['Năm sản xuất']):<5} | Hãng: {str(r['Hãng']):<12} | Model: {str(r['Grade']):<15} | Hộp số: {r['Hộp số']:<12} | Giá: {str(r['Giá']):<15} | Động cơ: {str(r['Động cơ'])}")

    print("\nPhân tích bản chất:")
    print("1. Giá trị '-': 15 bản ghi. Trên portal Bonbanh.com, dấu '-' xuất hiện khi người đăng tin không chọn trường hộp số (bỏ trống trường bắt buộc). Đây là Missing/Unknown value.")
    print("2. Giá trị 'Số hỗn hợp': 2 bản ghi. Trong tiếng Việt và thuật ngữ kỹ thuật ô tô, một số dòng xe hybrid/plugin hoặc e-CVT được salon gọi là 'Số hỗn hợp' (hỗn hợp giữa mô tơ điện và hộp số hành tinh / vô cấp) hoặc do hệ thống form của sàn giao dịch.")


if __name__ == "__main__":
    audit_raw_integrity()
    df_raw, p_prices, years, trans, km = audit_row_counts_and_filters()
    audit_cohort_b_discrepancy(df_raw, p_prices, years, trans, km)
    audit_splits_and_leakage()
    audit_transmission_details()

