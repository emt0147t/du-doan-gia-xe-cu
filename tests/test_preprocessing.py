"""Unit tests cho module tiền xử lý dữ liệu (src/data/preprocessing.py).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer
"""

import numpy as np
import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer

from src.data.preprocessing import (
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    TARGET_COLUMN,
    TARGET_LOG_COLUMN,
    EXCLUDED_LEAKAGE_COLUMNS,
    get_feature_names,
    extract_features_and_target,
    build_linear_preprocessor,
    build_tree_preprocessor,
)


@pytest.fixture
def clean_mock_df() -> pd.DataFrame:
    """Fixture tạo DataFrame sạch hoàn chỉnh phục vụ kiểm thử preprocessor."""
    return pd.DataFrame({
        "listing_id": ["ID1", "ID2", "ID3", "ID4", "ID5"],
        "url": ["https://bonbanh.com/1", "https://bonbanh.com/2", "https://bonbanh.com/3", "https://bonbanh.com/4", "https://bonbanh.com/5"],
        "Mã tin": ["ID1", "ID2", "ID3", "ID4", "ID5"],
        "Giá": ["500 Triệu", "700 Triệu", "1 Tỷ", "1.5 Tỷ", "2 Tỷ"],
        "Mô tả": ["Xe tốt", "Chính chủ", "Bao test", "Giá thương lượng", "Salon uy tín"],
        "Tên xe": ["Toyota Vios 2018", "Hyundai Accent 2020", "Mazda CX5 2019", "Ford Ranger 2021", "Mercedes C200 2022"],
        # Numeric features
        "year": [2018.0, 2020.0, 2019.0, 2021.0, 2022.0],
        "car_age": [6.0, 4.0, 5.0, 3.0, 2.0],
        "mileage_km": [45000.0, 0.0, 30000.0, 15000.0, np.nan],
        "is_zero_mileage": [0, 1, 0, 0, 0],
        "engine_displacement_l": [1.5, 1.4, 2.0, 2.2, np.nan],
        "seats": [5.0, 5.0, 5.0, 5.0, 5.0],
        "doors": [4.0, 4.0, 5.0, 4.0, 4.0],
        "is_luxury_brand": [0, 0, 0, 0, 1],
        # Categorical features
        "brand": ["Toyota", "Hyundai", "Mazda", "Ford", "Mercedes-Benz"],
        "model": ["Vios", "Accent", "CX-5", "Ranger", "C200"],
        "condition": ["Xe đã dùng", "Xe mới", "Xe đã dùng", "Xe đã dùng", "Xe mới"],
        "transmission": ["Số tay", "Tự động", "Tự động", "Tự động", "Tự động"],
        "origin": ["Trong nước", "Trong nước", "Trong nước", "Nhập khẩu", "Trong nước"],
        "body_type": ["Sedan", "Sedan", "SUV", "Bán tải / Pickup", "Sedan"],
        "fuel_type": ["Xăng", "Xăng", "Xăng", "Dầu", "Xăng"],
        # Targets
        "price_vnd": [500_000_000.0, 700_000_000.0, 1_000_000_000.0, 1_500_000_000.0, 2_000_000_000.0],
        "log_price": np.log([500_000_000.0, 700_000_000.0, 1_000_000_000.0, 1_500_000_000.0, 2_000_000_000.0]),
    })


def test_feature_names_lists():
    """Kiểm tra danh sách features định lượng và định danh có định nghĩa đúng."""
    num_cols, cat_cols = get_feature_names()
    assert len(num_cols) == 8
    assert len(cat_cols) == 7
    assert set(num_cols) == set(NUMERIC_FEATURES)
    assert set(cat_cols) == set(CATEGORICAL_FEATURES)


def test_extract_features_and_target_leakage_safety(clean_mock_df):
    """Kiểm tra trích xuất X và y: X không chứa bất kỳ cột leakage nào."""
    X, y = extract_features_and_target(clean_mock_df, target_col="price_vnd")

    # Kiểm tra kích thước
    assert X.shape == (5, 15)  # 8 num + 7 cat
    assert len(y) == 5

    # Đảm bảo không có cột leakage nào trong X
    for col in EXCLUDED_LEAKAGE_COLUMNS:
        assert col not in X.columns, f"Cột rò rỉ '{col}' không được phép có trong X!"

    # Kiểm tra target
    assert y.iloc[0] == 500_000_000.0


def test_extract_log_target(clean_mock_df):
    """Kiểm tra trích xuất log_price làm target."""
    X, y_log = extract_features_and_target(clean_mock_df, use_log_target=True)
    assert np.isclose(y_log.iloc[0], np.log(500_000_000.0))


def test_build_linear_preprocessor_is_unfitted():
    """Kiểm tra preprocessor trả về instance chưa được fit."""
    preprocessor = build_linear_preprocessor()
    assert isinstance(preprocessor, ColumnTransformer)
    assert not hasattr(preprocessor, "transformers_")


def test_build_tree_preprocessor_is_unfitted():
    """Kiểm tra tree preprocessor trả về instance chưa được fit."""
    preprocessor = build_tree_preprocessor()
    assert isinstance(preprocessor, ColumnTransformer)
    assert not hasattr(preprocessor, "transformers_")


def test_preprocessor_fit_on_train_transforms_test_with_unseen_categories(clean_mock_df):
    """Kiểm tra an toàn rò rỉ: Fit trên train, transform trên test chứa nhãn danh mục mới (unseen)."""
    X_train = clean_mock_df.iloc[:3][NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()
    X_test = clean_mock_df.iloc[3:][NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()

    # Thêm hãng xe chưa từng xuất hiện trong train (unseen category)
    X_test.loc[3, "brand"] = "Ferrari"
    X_test.loc[4, "model"] = "F8 Tributo"

    preprocessor = build_linear_preprocessor()

    # Fit CHỈ trên train
    preprocessor.fit(X_train)
    assert hasattr(preprocessor, "transformers_")

    # Transform trên train
    train_trans = preprocessor.transform(X_train)
    assert train_trans.shape[0] == 3

    # Transform trên test KHÔNG ĐƯỢC BÁO LỖI do unseen category (nhờ handle_unknown='ignore')
    test_trans = preprocessor.transform(X_test)
    assert test_trans.shape[0] == 2
    assert not np.isnan(test_trans).any()


def test_tree_preprocessor_does_not_scale(clean_mock_df):
    """Kiểm tra tree preprocessor không sử dụng StandardScaler."""
    preprocessor = build_tree_preprocessor()
    num_step = preprocessor.transformers[0][1]
    step_names = [name for name, _ in num_step.steps]
    assert "scaler" not in step_names
    assert "imputer" in step_names
