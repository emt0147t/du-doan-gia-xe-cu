"""Unit tests cho module suy luận mô hình dự đoán giá xe (tests/test_predict.py).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.models.predict import (
    format_vnd_price,
    load_champion_model,
    predict_car_price,
    prepare_car_features,
)


def test_format_vnd_price():
    """Kiểm tra định dạng tiền tệ tiếng Việt."""
    assert format_vnd_price(450_000_000) == "450 Triệu VNĐ (450,000,000 đ)"
    assert format_vnd_price(1_250_000_000) == "1 Tỷ 250 Triệu VNĐ (1,250,000,000 đ)"
    assert format_vnd_price(2_000_000_000) == "2 Tỷ VNĐ (2,000,000,000 đ)"
    assert format_vnd_price(-100) == "N/A"
    assert format_vnd_price(np.nan) == "N/A"


def test_prepare_car_features_derivation():
    """Kiểm tra việc tự động suy luận đặc trưng (car_age, is_zero_mileage, is_luxury_brand)."""
    raw_dict = {
        "brand": "Mercedes-Benz",
        "model": "C200",
        "year": 2021,
        "mileage_km": 0,
        "transmission": "Tự động",
        "engine_displacement_l": 1.5,
        "fuel_type": "Xăng",
        "origin": "Trong nước",
        "body_type": "Sedan",
        "condition": "Xe mới",
        "seats": 5.0,
        "doors": 4.0,
    }

    df_prepared = prepare_car_features(raw_dict)

    assert len(df_prepared) == 1
    assert df_prepared["car_age"].iloc[0] == 3.0  # 2024 - 2021
    assert df_prepared["is_zero_mileage"].iloc[0] == 1.0
    assert df_prepared["is_luxury_brand"].iloc[0] == 1.0


def test_prepare_car_features_mass_market():
    """Kiểm tra đặc trưng với xe phổ thông có ODO > 0."""
    raw_dict = {
        "brand": "Toyota",
        "model": "Vios",
        "year": 2019,
        "mileage_km": 60000,
    }

    df_prepared = prepare_car_features(raw_dict)

    assert df_prepared["car_age"].iloc[0] == 5.0
    assert df_prepared["is_zero_mileage"].iloc[0] == 0.0
    assert df_prepared["is_luxury_brand"].iloc[0] == 0.0
    # Các trường thiếu phải là NaN hoặc chuẩn hóa
    assert pd.isna(df_prepared["engine_displacement_l"].iloc[0])


def test_predict_car_price_integration():
    """Kiểm thử tích hợp dự đoán với Champion Model artifact nếu tồn tại."""
    model_path = Path("models/champion_random_forest.joblib")
    if not model_path.exists():
        pytest.skip("Chưa có tệp artifact models/champion_random_forest.joblib")

    model = load_champion_model(model_path)

    sample_car = {
        "brand": "Toyota",
        "model": "Vios",
        "year": 2020,
        "mileage_km": 40000,
        "transmission": "Tự động",
        "engine_displacement_l": 1.5,
        "fuel_type": "Xăng",
        "origin": "Trong nước",
        "body_type": "Sedan",
        "condition": "Xe đã dùng",
        "seats": 5.0,
        "doors": 4.0,
    }

    result = predict_car_price(sample_car, model=model)

    assert isinstance(result, dict)
    assert "predicted_price_vnd" in result
    assert "formatted_price" in result
    assert 200_000_000 <= result["predicted_price_vnd"] <= 800_000_000
    assert "VNĐ" in result["formatted_price"]
