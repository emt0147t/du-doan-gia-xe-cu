"""Kiểm toán chuyên sâu Trùng lặp và Rò rỉ dữ liệu (Deep Duplicate & Cross-Posting Audit).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Reviewer
"""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

RAW_PATH = Path("data/raw/external/mquaan_car_price/car_detail.csv")
TRAIN_PATH = Path("data/processed/splits/train.csv")
VAL_PATH = Path("data/processed/splits/val.csv")
TEST_PATH = Path("data/processed/splits/test.csv")


def main():
    print("=" * 80)
    print("KIỂM TOÁN CHUYÊN SÂU TRÙNG LẶP & CROSS-POSTING")
    print("=" * 80)

    df_raw = pd.read_csv(RAW_PATH)
    n_raw = len(df_raw)

    # 1. Exact full-row duplicates
    n_exact_dup = df_raw.duplicated().sum()
    print(f"1. Trùng lặp hoàn toàn 100% tất cả các cột: {n_exact_dup} dòng (0.00%)")

    # 2. Duplicate listing_id
    n_id_dup = df_raw["Mã tin"].duplicated().sum()
    print(f"2. Trùng lặp theo Mã tin (listing_id):       {n_id_dup} dòng (0.00%)")

    # 3. Duplicate spec tuples (brand, Grade, Năm sản xuất, Số Km đã đi, Giá)
    spec_cols = ["Hãng", "Grade", "Năm sản xuất", "Số Km đã đi", "Giá"]
    dup_specs_mask = df_raw.duplicated(subset=spec_cols, keep=False)
    n_dup_specs = dup_specs_mask.sum()
    n_spec_groups = df_raw[dup_specs_mask].groupby(spec_cols).ngroups
    print(f"3. Trùng lặp theo 5 thông số xe:             {n_dup_specs:,} dòng ({n_dup_specs/n_raw*100:.2f}%) trong {n_spec_groups:,} cụm")

    # Phân tích bản chất các ca trùng thông số
    dup_specs_df = df_raw[dup_specs_mask]
    n_new_cars = (dup_specs_df["Tình trạng"].str.strip() == "Xe mới").sum()
    n_zero_km = (dup_specs_df["Số Km đã đi"].str.strip() == "0 Km").sum()
    n_used_with_km = ((dup_specs_df["Tình trạng"].str.strip() != "Xe mới") & (dup_specs_df["Số Km đã đi"].str.strip() != "0 Km")).sum()
    print(f"   - Xe mới tại Showroom:                   {n_new_cars:,} dòng ({n_new_cars/n_dup_specs*100:.1f}%)")
    print(f"   - ODO = 0 Km:                            {n_zero_km:,} dòng ({n_zero_km/n_dup_specs*100:.1f}%)")
    print(f"   - Xe cũ có ODO > 0 trùng cả thông số:    {n_used_with_km:,} dòng ({n_used_with_km/n_dup_specs*100:.1f}%)")

    # 4. Duplicate descriptions (cross-posting)
    desc_clean = df_raw["Mô tả"].dropna().astype(str).str.strip()
    long_desc_mask = desc_clean.str.len() > 30
    desc_dup_mask = desc_clean[long_desc_mask].duplicated(keep=False)
    n_desc_dup = desc_dup_mask.sum()
    n_desc_groups = desc_clean[long_desc_mask][desc_dup_mask].groupby(desc_clean).ngroups
    print(f"4. Trùng lặp theo Mô tả tin đăng (>30 ký tự): {n_desc_dup:,} dòng ({n_desc_dup/n_raw*100:.2f}%) trong {n_desc_groups:,} cụm")

    # 5. Kiểm toán rò rỉ giữa các splits
    print("\n" + "=" * 80)
    print("5. ĐỐI CHIẾU RÒ RỈ GIỮA TRAIN / VALIDATION / TEST")
    print("=" * 80)
    train_df = pd.read_csv(TRAIN_PATH)
    val_df = pd.read_csv(VAL_PATH)
    test_df = pd.read_csv(TEST_PATH)

    # A. listing_id overlap
    s_tr = set(train_df["listing_id"])
    s_va = set(val_df["listing_id"])
    s_te = set(test_df["listing_id"])
    print(f"A. Trùng lặp listing_id:")
    print(f"   Train & Val:  {len(s_tr & s_va)}")
    print(f"   Train & Test: {len(s_tr & s_te)}")
    print(f"   Val & Test:   {len(s_va & s_te)}")

    # B. Long description overlap
    tr_desc = set(train_df["Mô tả"].dropna().str.strip().loc[lambda s: s.str.len() > 50])
    va_desc = set(val_df["Mô tả"].dropna().str.strip().loc[lambda s: s.str.len() > 50])
    te_desc = set(test_df["Mô tả"].dropna().str.strip().loc[lambda s: s.str.len() > 50])

    print(f"\nB. Trùng lặp Mô tả dài (>50 ký tự - Cross-posting thật sự):")
    print(f"   Train & Val:  {len(tr_desc & va_desc)} cụm mô tả")
    print(f"   Train & Test: {len(tr_desc & te_desc)} cụm mô tả")
    print(f"   Val & Test:   {len(va_desc & te_desc)} cụm mô tả")

    # Bao nhiêu dòng val/test bị ảnh hưởng bởi trùng mô tả?
    val_desc_leaked = val_df[val_df["Mô tả"].dropna().str.strip().isin(tr_desc & va_desc)]
    test_desc_leaked = test_df[test_df["Mô tả"].dropna().str.strip().isin(tr_desc & te_desc)]
    print(f"   -> Số dòng Val có mô tả xuất hiện trong Train:  {len(val_desc_leaked):,} / {len(val_df):,} ({len(val_desc_leaked)/len(val_df)*100:.2f}%)")
    print(f"   -> Số dòng Test có mô tả xuất hiện trong Train: {len(test_desc_leaked):,} / {len(test_df):,} ({len(test_desc_leaked)/len(test_df)*100:.2f}%)")

    # C. Trùng lặp thông số kỹ thuật (Spec tuple)
    def make_k(df):
        return set(zip(df["brand"], df["model"], df["year"], df["mileage_km"], df["price_vnd"]))

    k_tr = make_k(train_df)
    k_va = make_k(val_df)
    k_te = make_k(test_df)

    print(f"\nC. Trùng lặp bộ thông số (brand, model, year, ODO, price):")
    print(f"   Train & Val:  {len(k_tr & k_va)} bộ thông số")
    print(f"   Train & Test: {len(k_tr & k_te)} bộ thông số")
    print(f"   Val & Test:   {len(k_va & k_te)} bộ thông số")

    # Phân loại trong số các dòng Val/Test trùng spec:
    val_spec_leaked = val_df[val_df.apply(lambda r: (r["brand"], r["model"], r["year"], r["mileage_km"], r["price_vnd"]) in (k_tr & k_va), axis=1)]
    test_spec_leaked = test_df[test_df.apply(lambda r: (r["brand"], r["model"], r["year"], r["mileage_km"], r["price_vnd"]) in (k_tr & k_te), axis=1)]

    print(f"\n   -> Số dòng Val trùng spec với Train:  {len(val_spec_leaked):,} / {len(val_df):,} ({len(val_spec_leaked)/len(val_df)*100:.2f}%)")
    print(f"      + Xe mới tại showroom (ODO=0):     {(val_spec_leaked['is_zero_mileage']==1).sum():,} ({ (val_spec_leaked['is_zero_mileage']==1).sum()/len(val_spec_leaked)*100:.1f}%)")
    print(f"      + Xe cũ có ODO > 0:                {(val_spec_leaked['is_zero_mileage']==0).sum():,} ({ (val_spec_leaked['is_zero_mileage']==0).sum()/len(val_spec_leaked)*100:.1f}%)")

    print(f"\n   -> Số dòng Test trùng spec với Train: {len(test_spec_leaked):,} / {len(test_df):,} ({len(test_spec_leaked)/len(test_df)*100:.2f}%)")
    print(f"      + Xe mới tại showroom (ODO=0):     {(test_spec_leaked['is_zero_mileage']==1).sum():,} ({ (test_spec_leaked['is_zero_mileage']==1).sum()/len(test_spec_leaked)*100:.1f}%)")
    print(f"      + Xe cũ có ODO > 0:                {(test_spec_leaked['is_zero_mileage']==0).sum():,} ({ (test_spec_leaked['is_zero_mileage']==0).sum()/len(test_spec_leaked)*100:.1f}%)")


if __name__ == "__main__":
    main()
