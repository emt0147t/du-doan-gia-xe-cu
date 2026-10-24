"""Unit tests cho hệ thống huấn luyện và đánh giá mô hình học máy (src/models/).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer
"""

import json
from pathlib import Path
from typing import Tuple
import numpy as np
import pandas as pd
import pytest

from src.models.evaluate import (
    compute_regression_metrics,
    compute_residual_dataframe,
    inverse_log_transform,
)
from src.models.experiment_config import ExperimentConfig
from src.models.train import (
    build_estimator,
    build_full_pipeline,
    run_single_experiment,
)


@pytest.fixture
def mock_modeling_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Tạo bộ fixture giả lập nhỏ gọn để kiểm thử pipeline huấn luyện."""
    np.random.seed(42)
    n_train, n_val = 60, 20

    def _make_df(n):
        prices = np.random.uniform(300_000_000, 2_000_000_000, size=n)
        return pd.DataFrame({
            "listing_id": [f"ID_{i:03d}" for i in range(n)],
            "url": [f"https://bonbanh.com/{i}" for i in range(n)],
            "Mã tin": [f"ID_{i:03d}" for i in range(n)],
            "Giá": [f"{p/1e6:.0f} Triệu" for p in prices],
            "Mô tả": ["Xe đẹp chính chủ" for _ in range(n)],
            "Tên xe": ["Xe lướt" for _ in range(n)],
            # Numerics
            "year": np.random.randint(2015, 2024, size=n).astype("float64"),
            "car_age": np.random.randint(1, 10, size=n).astype("float64"),
            "mileage_km": np.random.uniform(0, 100_000, size=n),
            "is_zero_mileage": np.random.choice([0, 1], size=n),
            "engine_displacement_l": np.random.choice([1.5, 2.0, 2.5], size=n),
            "seats": np.random.choice([5.0, 7.0], size=n),
            "doors": [4.0] * n,
            "is_luxury_brand": np.random.choice([0, 1], size=n),
            # Categoricals
            "brand": np.random.choice(["Toyota", "Hyundai", "Mercedes-Benz"], size=n),
            "model": np.random.choice(["Vios", "Accent", "C200"], size=n),
            "condition": np.random.choice(["Xe đã dùng", "Xe mới"], size=n),
            "transmission": np.random.choice(["Tự động", "Số tay"], size=n),
            "origin": np.random.choice(["Trong nước", "Nhập khẩu"], size=n),
            "body_type": np.random.choice(["Sedan", "SUV"], size=n),
            "fuel_type": np.random.choice(["Xăng", "Dầu"], size=n),
            # Target
            "price_vnd": prices,
            "log_price": np.log(prices),
        })

    return _make_df(n_train), _make_df(n_val)


def test_experiment_config_serialization():
    """Kiểm tra tuần tự hóa ExperimentConfig sang Dict."""
    cfg = ExperimentConfig(
        name="test_exp",
        model_type="ridge",
        hyperparameters={"alpha": 1.0},
        target_type="log",
        preprocessor_type="linear",
    )
    d = cfg.to_dict()
    assert d["name"] == "test_exp"
    assert d["model_type"] == "ridge"
    assert d["target_type"] == "log"
    assert d["hyperparameters"]["alpha"] == 1.0


def test_inverse_log_transform_bounds():
    """Kiểm tra hàm nghịch đảo logarit exp(y) tuân thủ biên giá trị an toàn."""
    y_log = np.array([np.log(500_000_000.0), np.log(1_000_000_000.0), 0.0, 50.0])
    y_inv = inverse_log_transform(y_log)

    assert np.isclose(y_inv[0], 500_000_000.0)
    assert np.isclose(y_inv[1], 1_000_000_000.0)
    assert y_inv[2] >= 30_000_000.0  # Giới hạn cận dưới
    assert y_inv[3] <= 100_000_000_000.0  # Giới hạn cận trên
    assert not np.isnan(y_inv).any()


def test_compute_regression_metrics_accuracy():
    """Kiểm tra độ chính xác của hàm tính toán chỉ số MAE, RMSE, R2, MAPE."""
    y_true = np.array([100.0, 200.0, 300.0])
    y_pred = np.array([110.0, 190.0, 310.0])  # Sai số tuyệt đối 10 ở mỗi mẫu

    metrics = compute_regression_metrics(y_true, y_pred)
    assert metrics["mae"] == 10.0
    assert metrics["rmse"] == 10.0
    assert metrics["r2"] > 0.95
    assert np.isclose(metrics["mdape"], 5.0, atol=1.5)


def test_compute_residual_dataframe():
    """Kiểm tra tạo bảng phân tích phần dư."""
    y_true = np.array([500.0, 1000.0])
    y_pred = np.array([450.0, 1100.0])
    ids = pd.Series(["A1", "A2"])

    df_res = compute_residual_dataframe(y_true, y_pred, listing_ids=ids)
    assert len(df_res) == 2
    assert "listing_id" in df_res.columns
    assert df_res.loc[0, "residual_vnd"] == 50.0
    assert df_res.loc[1, "residual_vnd"] == -100.0


def test_build_estimator_supported_types():
    """Kiểm tra khởi tạo đúng class estimator."""
    assert build_estimator("dummy_median").__class__.__name__ == "DummyRegressor"
    assert build_estimator("dummy_mean").__class__.__name__ == "DummyRegressor"
    assert build_estimator("ridge").__class__.__name__ == "Ridge"
    assert build_estimator("lasso").__class__.__name__ == "Lasso"
    assert build_estimator("random_forest").__class__.__name__ == "RandomForestRegressor"
    assert build_estimator("hist_gradient_boosting").__class__.__name__ == "HistGradientBoostingRegressor"

    with pytest.raises(ValueError, match="Loại mô hình không được hỗ trợ"):
        build_estimator("unsupported_model")


def test_run_single_experiment_end_to_end(mock_modeling_data):
    """Kiểm tra luồng huấn luyện thí nghiệm hoàn chỉnh (Fit trên Train, Predict trên Val)."""
    train_df, val_df = mock_modeling_data

    cfg = ExperimentConfig(
        name="test_rf_small",
        model_type="random_forest",
        hyperparameters={"n_estimators": 10, "max_depth": 5},
        target_type="log",
        preprocessor_type="tree",
        random_state=42,
    )

    rec, preds, pipe = run_single_experiment(cfg, train_df, val_df)
    assert rec["experiment_name"] == "test_rf_small"
    assert len(preds) == len(val_df)
    assert rec["mae"] > 0
    assert rec["r2"] is not None
    assert rec["fit_time_seconds"] >= 0


def test_reproducibility_with_fixed_seed(mock_modeling_data):
    """Kiểm tra tính tái lập 100%: Cùng random_state sinh ra cùng kết quả dự đoán."""
    train_df, val_df = mock_modeling_data

    cfg1 = ExperimentConfig("rf_run1", "random_forest", {"n_estimators": 15, "max_depth": 5}, target_type="raw", random_state=42)
    cfg2 = ExperimentConfig("rf_run2", "random_forest", {"n_estimators": 15, "max_depth": 5}, target_type="raw", random_state=42)

    _, preds1, _ = run_single_experiment(cfg1, train_df, val_df)
    _, preds2, _ = run_single_experiment(cfg2, train_df, val_df)

    np.testing.assert_array_almost_equal(preds1, preds2)
