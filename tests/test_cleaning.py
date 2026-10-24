"""Unit tests cho module làm sạch dữ liệu (src/data/cleaning.py).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer
"""

import numpy as np
import pandas as pd
import pytest

from src.data.cleaning import (
    clean_price_column,
    clean_year_column,
    clean_mileage_column,
    clean_categorical_columns,
    extract_engine_specs,
    extract_capacity_specs,
    engineer_features,
    clean_dataset,
    LUXURY_BRANDS,
)


@pytest.fixture
def synthetic_sample_df() -> pd.DataFrame:
    """Fixture tạo DataFrame tổng hợp phục vụ kiểm thử."""
    return pd.DataFrame({
        "Mã tin": ["T101", "T102", "T103", "T104", "T105"],
        "Giá": ["500 Triệu", "1 Tỷ 200 Triệu", "Giá liên hệ", "12 Triệu", "50 Tỷ"],
        "Năm sản xuất": [2018, "2020", "invalid", 2012, 2022],
        "Số Km đã đi": ["45,000 Km", "0 Km", "100.000 km", "1,500,000 Km", None],
        "Hãng": ["Toyota", "Mercedes Benz", "BMW", "Kia", "Hyundai"],
        "Grade": ["Vios", "C200", "320i", "Morning", "Accent"],
        "Hộp số": ["Tự động", "Số tay", "-", "Số hỗn hợp", "Tự động"],
        "Xuất xứ": ["Lắp ráp trong nước", "Nhập khẩu", "Trong nước", "Nhập khẩu", "Lắp ráp trong nước"],
        "Dòng xe": ["Sedan", "Sedan", "Sedan", "Hatchback", "Sedan"],
        "Tình trạng": ["Xe đã dùng", "Xe mới", "Xe đã dùng", "Xe đã dùng", "Xe mới"],
        "Động cơ": ["Xăng\t1.5 L", "Xăng\t2.0 L", "Dầu\t2.0 L", "Điện", "Hybrid\t1.8 L"],
        "Số chỗ ngồi": ["5 chỗ", "5", "5 chỗ", "4 chỗ", "5 chỗ"],
        "Số cửa": ["4 cửa", "4", "4 cửa", "5 cửa", "4 cửa"],
        "URL": ["https://bonbanh.com/1", "https://bonbanh.com/2", "https://bonbanh.com/3", "https://bonbanh.com/4", "https://bonbanh.com/5"],
        "Mô tả": ["Xe đẹp", "Showroom", "Xe lướt", "Cần bán", "Xe mới 100%"],
    })


def test_clean_price_column_valid_and_missing(synthetic_sample_df):
    """Kiểm tra parse giá, đảm bảo không thay missing target thành 0 và không mutate dữ liệu gốc."""
    df_original = synthetic_sample_df.copy()
    result = clean_price_column(synthetic_sample_df)

    # Dữ liệu gốc không bị thay đổi
    pd.testing.assert_frame_equal(synthetic_sample_df, df_original)

    # Kiểm tra giá trị chuyển đổi
    assert result.loc[0, "price_vnd"] == 500_000_000.0
    assert result.loc[1, "price_vnd"] == 1_200_000_000.0
    assert pd.isna(result.loc[2, "price_vnd"])  # 'Giá liên hệ' phải là NaN, KHÔNG ĐƯỢC LÀ 0
    assert result.loc[2, "price_vnd"] != 0.0
    assert result.loc[3, "price_vnd"] == 12_000_000.0
    assert result.loc[4, "price_vnd"] == 50_000_000_000.0


def test_clean_year_column_handles_numeric_and_invalid(synthetic_sample_df):
    """Kiểm tra chuyển đổi năm sang numeric có kiểm soát."""
    result = clean_year_column(synthetic_sample_df)
    assert result.loc[0, "year"] == 2018.0
    assert result.loc[1, "year"] == 2020.0
    assert pd.isna(result.loc[2, "year"])  # 'invalid' thành NaN
    assert result.loc[3, "year"] == 2012.0
    assert result.loc[4, "year"] == 2022.0


def test_clean_mileage_column_preserves_zero_and_flags_overflow(synthetic_sample_df):
    """Kiểm tra ODO = 0 được giữ nguyên, overflow > 1M thành NaN."""
    result = clean_mileage_column(synthetic_sample_df)
    assert result.loc[0, "mileage_km"] == 45_000.0
    assert result.loc[1, "mileage_km"] == 0.0  # ODO = 0 giữ nguyên
    assert result.loc[2, "mileage_km"] == 100_000.0
    assert pd.isna(result.loc[3, "mileage_km"])  # 1,500,000 km là sentinel/overflow -> NaN
    assert pd.isna(result.loc[4, "mileage_km"])  # None -> NaN


def test_clean_categorical_columns_normalization(synthetic_sample_df):
    """Kiểm tra chuẩn hóa chuỗi phân loại, mapping listing_id và loại ký tự dị biệt."""
    result = clean_categorical_columns(synthetic_sample_df)

    # Mapping listing_id và url
    assert result.loc[0, "listing_id"] == "T101"
    assert result.loc[0, "url"] == "https://bonbanh.com/1"

    # Chuẩn hóa brand
    assert result.loc[1, "brand"] == "Mercedes-Benz"  # 'Mercedes Benz' -> 'Mercedes-Benz'

    # Lọc hộp số dị biệt
    assert result.loc[0, "transmission"] == "Tự động"
    assert result.loc[1, "transmission"] == "Số tay"
    assert pd.isna(result.loc[2, "transmission"])  # '-' -> NaN
    assert pd.isna(result.loc[3, "transmission"])  # 'Số hỗn hợp' -> NaN

    # Chuẩn hóa xuất xứ
    assert result.loc[0, "origin"] == "Trong nước"
    assert result.loc[1, "origin"] == "Nhập khẩu"


def test_extract_engine_and_capacity_specs(synthetic_sample_df):
    """Kiểm tra trích xuất nhiên liệu, dung tích động cơ, số chỗ ngồi và số cửa."""
    res_eng = extract_engine_specs(synthetic_sample_df)
    assert res_eng.loc[0, "fuel_type"] == "Xăng"
    assert res_eng.loc[0, "engine_displacement_l"] == 1.5
    assert res_eng.loc[2, "fuel_type"] == "Dầu"
    assert res_eng.loc[2, "engine_displacement_l"] == 2.0
    assert res_eng.loc[3, "fuel_type"] == "Điện"
    assert pd.isna(res_eng.loc[3, "engine_displacement_l"])
    assert res_eng.loc[4, "fuel_type"] == "Hybrid"
    assert res_eng.loc[4, "engine_displacement_l"] == 1.8

    res_cap = extract_capacity_specs(synthetic_sample_df)
    assert res_cap.loc[0, "seats"] == 5.0
    assert res_cap.loc[0, "doors"] == 4.0
    assert res_cap.loc[3, "seats"] == 4.0
    assert res_cap.loc[3, "doors"] == 5.0


def test_engineer_features_correctness():
    """Kiểm tra tạo các đặc trưng phái sinh: car_age, is_zero_mileage, is_luxury_brand, log_price."""
    df_test = pd.DataFrame({
        "year": [2020, 2024, 2015],
        "mileage_km": [0.0, 50000.0, 0.0],
        "brand": ["Mercedes-Benz", "Toyota", "Porsche"],
        "price_vnd": [1_000_000_000.0, 500_000_000.0, 4_000_000_000.0],
    })

    result = engineer_features(df_test, reference_year=2024)

    # car_age
    assert result.loc[0, "car_age"] == 4.0
    assert result.loc[1, "car_age"] == 0.0
    assert result.loc[2, "car_age"] == 9.0

    # is_zero_mileage
    assert result.loc[0, "is_zero_mileage"] == 1
    assert result.loc[1, "is_zero_mileage"] == 0
    assert result.loc[2, "is_zero_mileage"] == 1

    # is_luxury_brand
    assert result.loc[0, "is_luxury_brand"] == 1
    assert result.loc[1, "is_luxury_brand"] == 0
    assert result.loc[2, "is_luxury_brand"] == 1

    # log_price
    assert np.isclose(result.loc[0, "log_price"], np.log(1_000_000_000.0))
    assert np.isclose(result.loc[1, "log_price"], np.log(500_000_000.0))


def test_clean_dataset_end_to_end_pipeline(synthetic_sample_df):
    """Kiểm tra pipeline clean_dataset với các tiêu chí lọc và ghi audit_log."""
    df_clean, audit = clean_dataset(
        synthetic_sample_df,
        min_year=2015,
        min_price=30_000_000,
        max_price=50_000_000_000,
    )

    assert audit["initial_row_count"] == 5
    assert audit["min_year_scope"] == 2015

    # T103 bị loại do Giá liên hệ (target khuyết)
    # T104 bị loại do Năm 2012 (< 2015) và Hộp số 'Số hỗn hợp'
    # Các bản ghi hợp lệ: T101 (2018), T102 (2020), T105 (2022)
    assert len(df_clean) == 3
    assert set(df_clean["listing_id"]) == {"T101", "T102", "T105"}
    assert df_clean["price_vnd"].min() >= 30_000_000
    assert df_clean["year"].min() >= 2015
