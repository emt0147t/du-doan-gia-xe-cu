"""Pipeline tiền xử lý dữ liệu an toàn rò rỉ (Leakage-Safe Preprocessing Pipeline).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer

Module này sử dụng scikit-learn ColumnTransformer và Pipeline để đóng gói toàn bộ quy trình:
- Imputation các biến số bị thiếu (median + indicator).
- Scaling đặc trưng cho mô hình tuyến tính (StandardScaler).
- One-Hot Encoding cho các biến danh mục (handle_unknown='ignore').
- Tách biệt hoàn toàn việc khởi tạo kiến trúc pipeline với việc fit dữ liệu (chỉ fit trên Train).
"""

from __future__ import annotations

from typing import List, Tuple
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Danh sách chuẩn các đặc trưng định lượng
NUMERIC_FEATURES: List[str] = [
    "year",
    "car_age",
    "mileage_km",
    "is_zero_mileage",
    "engine_displacement_l",
    "seats",
    "doors",
    "is_luxury_brand",
]

# Danh sách chuẩn các đặc trưng phân loại
CATEGORICAL_FEATURES: List[str] = [
    "brand",
    "model",
    "condition",
    "transmission",
    "origin",
    "body_type",
    "fuel_type",
]

# Biến mục tiêu chuẩn
TARGET_COLUMN: str = "price_vnd"
TARGET_LOG_COLUMN: str = "log_price"

# Các cột gây rò rỉ thông tin hoặc PII tuyệt đối bị loại khỏi X
EXCLUDED_LEAKAGE_COLUMNS: List[str] = [
    "price_vnd",
    "log_price",
    "Giá",
    "listing_id",
    "Mã tin",
    "url",
    "URL",
    "Mô tả",
    "Tên xe",
]

# Aliases for convenience
LEAKAGE_COLUMNS: List[str] = EXCLUDED_LEAKAGE_COLUMNS
ALL_MODELING_FEATURES: List[str] = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def get_feature_names() -> Tuple[List[str], List[str]]:
    """Trả về danh sách các đặc trưng số và đặc trưng danh mục."""
    return list(NUMERIC_FEATURES), list(CATEGORICAL_FEATURES)


def extract_features_and_target(
    df: pd.DataFrame,
    target_col: str = TARGET_COLUMN,
    use_log_target: bool = False,
) -> Tuple[pd.DataFrame, pd.Series]:
    """Tách ma trận đặc trưng X và nhãn mục tiêu y từ tập dữ liệu sạch.

    Đảm bảo tuyệt đối không có cột leakage hay identifier nào nằm trong X.

    Args:
        df: DataFrame dữ liệu đã làm sạch.
        target_col: Tên cột mục tiêu ('price_vnd' hoặc 'log_price').
        use_log_target: Nếu True, tự động chuyển sang dùng `log_price`.

    Returns:
        Tuple (X, y) với X chỉ chứa NUMERIC_FEATURES + CATEGORICAL_FEATURES.
    """
    selected_target = TARGET_LOG_COLUMN if use_log_target else target_col

    if selected_target not in df.columns:
        raise KeyError(f"Cột mục tiêu '{selected_target}' không tồn tại trong dữ liệu đầu vào.")

    # Kiểm tra sự hiện diện của các features
    missing_num = [c for c in NUMERIC_FEATURES if c not in df.columns]
    missing_cat = [c for c in CATEGORICAL_FEATURES if c not in df.columns]

    if missing_num or missing_cat:
        raise KeyError(
            f"Dữ liệu thiếu các cột đặc trưng quy chuẩn:\n"
            f"Thiếu numeric: {missing_num}\n"
            f"Thiếu categorical: {missing_cat}"
        )

    # Trích xuất X chỉ với các đặc trưng được phép
    feature_cols = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    X = df[feature_cols].copy()
    y = df[selected_target].copy()

    # Kiểm tra an toàn: Tuyệt đối không chứa leakage trong X
    for col in EXCLUDED_LEAKAGE_COLUMNS:
        if col in X.columns:
            raise ValueError(f"Phát hiện rò rỉ dữ liệu nghiêm trọng: Cột '{col}' đang nằm trong ma trận X!")

    return X, y


def build_linear_preprocessor(
    numeric_features: List[str] | None = None,
    categorical_features: List[str] | None = None,
) -> ColumnTransformer:
    """Xây dựng preprocessor cho các mô hình tuyến tính (Linear / Ridge / Lasso / SGD).

    Quy trình:
    - Numeric: SimpleImputer(median, indicator=True) -> StandardScaler()
    - Categorical: SimpleImputer(missing) -> OneHotEncoder(handle_unknown='ignore')

    Returns:
        ColumnTransformer chưa qua fit (unfitted).
    """
    num_cols = numeric_features if numeric_features is not None else NUMERIC_FEATURES
    cat_cols = categorical_features if categorical_features is not None else CATEGORICAL_FEATURES

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median", add_indicator=True)),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols),
        ],
        remainder="drop",
    )

    return preprocessor


def build_tree_preprocessor(
    numeric_features: List[str] | None = None,
    categorical_features: List[str] | None = None,
) -> ColumnTransformer:
    """Xây dựng preprocessor cho các mô hình dạng cây (RandomForest, LightGBM, XGBoost).

    Quy trình:
    - Numeric: SimpleImputer(median, indicator=True) (Mô hình cây không cần scaling).
    - Categorical: SimpleImputer(missing) -> OneHotEncoder(handle_unknown='ignore').

    Returns:
        ColumnTransformer chưa qua fit (unfitted).
    """
    num_cols = numeric_features if numeric_features is not None else NUMERIC_FEATURES
    cat_cols = categorical_features if categorical_features is not None else CATEGORICAL_FEATURES

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median", add_indicator=True)),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols),
        ],
        remainder="drop",
    )

    return preprocessor
