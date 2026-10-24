"""
Unit tests cho module kiểm định dữ liệu (tests/test_validation.py).

Dự án: Used Car Price Prediction in Vietnam
Sử dụng: Pytest

Kiểm thử toàn diện các hàm validation đơn lẻ, hàm kiểm tra bản ghi tổng thể,
phát hiện trùng lặp, xử lý các trường hợp đặc biệt của Python (NaN, Inf, Bool)
và xác minh qua fixture tổng hợp JSON.
"""

import json
import math
from pathlib import Path
import pytest

from src.data.validation import (
    ValidationConfig,
    validate_price,
    validate_year,
    validate_mileage,
    validate_identifier,
    validate_categorical_field,
    validate_car_record,
    check_duplicate_listings,
)


@pytest.fixture
def default_config():
    return ValidationConfig()


# ---------------------------------------------------------------------------
# 1. Kiểm thử validate_price (Bao gồm NaN, Inf, Float nguyên)
# ---------------------------------------------------------------------------
def test_validate_price_valid(default_config):
    ok, err = validate_price(899_000_000, default_config)
    assert ok is True
    assert err is None

    # Hỗ trợ float nguyên từ Pandas (vd: 899000000.0)
    ok_f, err_f = validate_price(899_000_000.0, default_config)
    assert ok_f is True
    assert err_f is None


def test_validate_price_missing_and_nan(default_config):
    ok, err = validate_price(None, default_config)
    assert ok is False
    assert "MISSING_TARGET_PRICE" in err

    # float('nan') phải được nhận diện là missing target
    ok_nan, err_nan = validate_price(float("nan"), default_config)
    assert ok_nan is False
    assert "MISSING_TARGET_PRICE" in err_nan


def test_validate_price_invalid_type_and_non_finite(default_config):
    # Chuỗi số không được xem là int
    ok, err = validate_price("899000000", default_config)
    assert ok is False
    assert "INVALID_TARGET_TYPE" in err

    # bool là subclass của int trong Python nhưng bị từ chối
    ok, err = validate_price(True, default_config)
    assert ok is False
    assert "INVALID_TARGET_TYPE" in err

    # float không nguyên
    ok, err = validate_price(899.5, default_config)
    assert ok is False
    assert "INVALID_TARGET_TYPE" in err

    # Infinity
    ok_inf, err_inf = validate_price(float("inf"), default_config)
    assert ok_inf is False
    assert "NON_FINITE_TARGET_PRICE" in err_inf


def test_validate_price_out_of_bounds(default_config):
    # Dưới ngưỡng sàn 30 triệu
    ok, err = validate_price(10_000_000, default_config)
    assert ok is False
    assert "TARGET_OUT_OF_BOUNDS" in err

    # Vượt ngưỡng trần 50 tỷ
    ok, err = validate_price(60_000_000_000, default_config)
    assert ok is False
    assert "TARGET_OUT_OF_BOUNDS" in err


# ---------------------------------------------------------------------------
# 2. Kiểm thử validate_year
# ---------------------------------------------------------------------------
def test_validate_year_valid(default_config):
    ok, err = validate_year(2021, default_config)
    assert ok is True
    assert err is None

    # Float nguyên từ Pandas (vd: 2021.0)
    ok_f, err_f = validate_year(2021.0, default_config)
    assert ok_f is True
    assert err_f is None


def test_validate_year_missing_and_invalid(default_config):
    ok, err = validate_year(None, default_config)
    assert ok is False
    assert "MISSING_YEAR" in err

    ok_nan, err_nan = validate_year(float("nan"), default_config)
    assert ok_nan is False
    assert "MISSING_YEAR" in err_nan

    ok_b, err_b = validate_year(True, default_config)
    assert ok_b is False
    assert "INVALID_YEAR_TYPE" in err_b


def test_validate_year_out_of_bounds(default_config):
    # Quá cũ (trước 2010)
    ok, err = validate_year(2005, default_config)
    assert ok is False
    assert "YEAR_OUT_OF_BOUNDS" in err

    # Năm tương lai
    ok, err = validate_year(2035, default_config)
    assert ok is False
    assert "YEAR_OUT_OF_BOUNDS" in err


# ---------------------------------------------------------------------------
# 3. Kiểm thử validate_mileage (Trường tùy chọn, NaN, Inf)
# ---------------------------------------------------------------------------
def test_validate_mileage_valid(default_config):
    ok, err = validate_mileage(45000.0, default_config)
    assert ok is True
    assert err is None

    # ODO = 0 (xe mới lăn bánh) là hợp lệ
    ok, err = validate_mileage(0, default_config)
    assert ok is True
    assert err is None


def test_validate_mileage_missing_is_allowed(default_config):
    # Trường tùy chọn: missing None hoặc float('nan') đều hợp lệ
    ok, err = validate_mileage(None, default_config)
    assert ok is True
    assert err is None

    ok_nan, err_nan = validate_mileage(float("nan"), default_config)
    assert ok_nan is True
    assert err_nan is None


def test_validate_mileage_invalid_values(default_config):
    # Số âm
    ok, err = validate_mileage(-1000.0, default_config)
    assert ok is False
    assert "NEGATIVE_MILEAGE" in err

    # Vượt ngưỡng tối đa 1 triệu km
    ok, err = validate_mileage(2_000_000.0, default_config)
    assert ok is False
    assert "MILEAGE_EXCEEDS_MAX" in err

    # Chuỗi số bị từ chối
    ok, err = validate_mileage("45000", default_config)
    assert ok is False
    assert "INVALID_MILEAGE_TYPE" in err

    # Bool bị từ chối
    ok, err = validate_mileage(True, default_config)
    assert ok is False
    assert "INVALID_MILEAGE_TYPE" in err

    # Infinity bị từ chối
    ok_inf, err_inf = validate_mileage(float("inf"), default_config)
    assert ok_inf is False
    assert "NON_FINITE_MILEAGE" in err_inf


# ---------------------------------------------------------------------------
# 4. Kiểm thử validate_identifier
# ---------------------------------------------------------------------------
def test_validate_identifier():
    ok, err = validate_identifier("23442555")
    assert ok is True
    assert err is None

    ok, err = validate_identifier(23442555)
    assert ok is True
    assert err is None

    ok, err = validate_identifier(None)
    assert ok is False
    assert "MISSING_LISTING_ID" in err

    ok, err = validate_identifier("   ")
    assert ok is False
    assert "MISSING_LISTING_ID" in err

    ok, err = validate_identifier("None")
    assert ok is False
    assert "MISSING_LISTING_ID" in err


# ---------------------------------------------------------------------------
# 5. Kiểm thử validate_categorical_field (Case-insensitivity & NaN safety)
# ---------------------------------------------------------------------------
def test_validate_categorical_field():
    allowed = {"Số tự động", "Số sàn"}
    # Khớp chính xác
    ok, err = validate_categorical_field("Số tự động", "transmission", allowed)
    assert ok is True
    assert err is None

    # Khớp không phân biệt chữ hoa/thường
    ok_lower, err_lower = validate_categorical_field("số tự động", "transmission", allowed)
    assert ok_lower is True
    assert err_lower is None

    ok_upper, err_upper = validate_categorical_field("SỐ SÀN", "transmission", allowed)
    assert ok_upper is True
    assert err_upper is None

    # Missing None hoặc float('nan') là hợp lệ (trường tùy chọn)
    ok, err = validate_categorical_field(None, "transmission", allowed)
    assert ok is True
    assert err is None

    ok_nan, err_nan = validate_categorical_field(float("nan"), "transmission", allowed)
    assert ok_nan is True
    assert err_nan is None

    # Giá trị không nằm trong danh mục
    ok, err = validate_categorical_field("Tự động 8 cấp", "transmission", allowed)
    assert ok is False
    assert "INVALID_TRANSMISSION_CATEGORY" in err


# ---------------------------------------------------------------------------
# 6. Kiểm thử validate_car_record & Phân biệt Lỗi vs Cảnh báo
# ---------------------------------------------------------------------------
def test_validate_car_record_complete_valid(default_config):
    record = {
        "listing_id": "test_001",
        "price_vnd": 899_000_000,
        "brand": "Mercedes-Benz",
        "model": "C200",
        "year": 2021,
        "mileage_km": 49000.0,
        "fuel_type": "Máy xăng",
        "transmission": "Số tự động",
        "location_province": "Hà Nội",
        "body_type": "Sedan",
        "origin": "Nhập khẩu",
        "seats": 5
    }
    result = validate_car_record(record, default_config)
    assert result.is_valid is True
    assert len(result.errors) == 0


def test_validate_car_record_optional_missing_is_still_valid(default_config):
    # Bản ghi chỉ có các trường bắt buộc, thiếu mileage_km, seats, fuel_type,... (bao gồm cả NaN)
    record = {
        "listing_id": "test_002",
        "price_vnd": 450_000_000,
        "brand": "Toyota",
        "model": "Vios",
        "year": 2019,
        "mileage_km": float("nan"),
        "transmission": float("nan"),
        "seats": float("nan")
    }
    result = validate_car_record(record, default_config)
    assert result.is_valid is True
    assert len(result.errors) == 0
    assert len(result.warnings) > 0
    assert any("mileage_km bị thiếu" in w for w in result.warnings)
    assert any("seats không có trong bảng thông số chuẩn" in w for w in result.warnings)


def test_validate_car_record_fatal_errors(default_config):
    # Thiếu target
    rec1 = {"listing_id": "001", "brand": "Kia", "model": "Morning", "year": 2020}
    res1 = validate_car_record(rec1, default_config)
    assert res1.is_valid is False
    assert any("MISSING_TARGET_PRICE" in e for e in res1.errors)

    # ODO âm
    rec2 = {
        "listing_id": "002",
        "price_vnd": 300_000_000,
        "brand": "Kia",
        "model": "Morning",
        "year": 2020,
        "mileage_km": -5000.0
    }
    res2 = validate_car_record(rec2, default_config)
    assert res2.is_valid is False
    assert any("NEGATIVE_MILEAGE" in e for e in res2.errors)


# ---------------------------------------------------------------------------
# 7. Kiểm thử check_duplicate_listings (Safe Deduplication Rules)
# ---------------------------------------------------------------------------
def test_check_duplicate_listings():
    records = [
        {"listing_id": "ID_001", "brand": "Toyota", "price_vnd": 500_000_000},
        {"listing_id": "ID_002", "brand": "Honda", "price_vnd": 600_000_000},
        {"listing_id": "ID_001", "brand": "Toyota", "price_vnd": 500_000_000},  # Trùng thật
        {"listing_id": "ID_003", "brand": "Mazda", "price_vnd": 700_000_000},
    ]
    unique, dupes = check_duplicate_listings(records)
    assert len(unique) == 3
    assert len(dupes) == 1
    assert dupes[0]["listing_id"] == "ID_001"


def test_check_duplicate_listings_none_ids_not_collapsed():
    # Hai bản ghi cùng thiếu listing_id (None) KHÔNG được gộp thành duplicate của nhau!
    records = [
        {"listing_id": None, "brand": "Toyota", "price_vnd": 500_000_000},
        {"listing_id": None, "brand": "Kia", "price_vnd": 400_000_000},
        {"listing_id": "", "brand": "Mazda", "price_vnd": 600_000_000},
    ]
    unique, dupes = check_duplicate_listings(records)
    assert len(unique) == 3
    assert len(dupes) == 0


def test_different_listings_same_specs_not_duplicate():
    # Hai xe khác nhau có cùng thông số nhưng khác listing_id KHÔNG bị coi là duplicate
    records = [
        {"listing_id": "CAR_A", "brand": "Toyota", "model": "Vios", "year": 2020, "price_vnd": 450_000_000},
        {"listing_id": "CAR_B", "brand": "Toyota", "model": "Vios", "year": 2020, "price_vnd": 450_000_000},
    ]
    unique, dupes = check_duplicate_listings(records)
    assert len(unique) == 2
    assert len(dupes) == 0


# ---------------------------------------------------------------------------
# 8. Kiểm thử từ Fixture JSON tổng hợp (synthetic_car_records.json)
# ---------------------------------------------------------------------------
def test_validation_against_synthetic_fixture(default_config):
    fixture_path = Path(__file__).parent / "fixtures" / "synthetic_car_records.json"
    assert fixture_path.exists()

    with open(fixture_path, "r", encoding="utf-8") as f:
        fixture = json.load(f)

    assert fixture.get("_metadata", {}).get("is_synthetic") is True

    for case in fixture.get("records", []):
        cid = case["case_id"]
        data = case["data"]
        expected_valid = case["expected_valid"]
        expected_reasons = case["expected_reasons"]

        result = validate_car_record(data, default_config)
        assert result.is_valid == expected_valid, (
            f"Case '{cid}' mismatch on is_valid: got {result.is_valid}, expected {expected_valid}. "
            f"Errors: {result.errors}"
        )

        for reason in expected_reasons:
            assert any(reason in err for err in result.errors), (
                f"Case '{cid}' did not find expected error reason '{reason}' in {result.errors}"
            )
