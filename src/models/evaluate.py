"""Module tính toán các chỉ số đánh giá mô hình hồi quy (Model Evaluation Metrics).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer
"""

from __future__ import annotations

from typing import Dict
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def inverse_log_transform(y_pred_log: np.ndarray | pd.Series) -> np.ndarray:
    """Nghịch đảo biến đổi logarit exp(y) về giá trị tiền VND thực tế.

    Bảo đảm các giá trị không âm và hữu hạn.
    """
    y_pred_arr = np.asarray(y_pred_log, dtype="float64")
    # Giới hạn cận trên để tránh tràn số float64 exp(>700)
    y_pred_arr = np.clip(y_pred_arr, a_min=0.0, a_max=30.0)
    y_inv = np.exp(y_pred_arr)
    # Clip cận dưới tại mức giá sàn thực tế (30 triệu VND)
    y_inv = np.clip(y_inv, a_min=30_000_000.0, a_max=100_000_000_000.0)
    return y_inv


def compute_regression_metrics(
    y_true: np.ndarray | pd.Series,
    y_pred: np.ndarray | pd.Series,
) -> Dict[str, float]:
    """Tính toán toàn diện các chỉ số đánh giá hồi quy theo đơn vị VND thực tế.

    Args:
        y_true: Nhãn thực tế (đơn vị VND).
        y_pred: Nhãn dự đoán từ mô hình (đơn vị VND).

    Returns:
        Dict gồm các chỉ số: MAE, RMSE, R2, MAPE, MdAPE.
    """
    y_t = np.asarray(y_true, dtype="float64")
    y_p = np.asarray(y_pred, dtype="float64")

    # Kiểm tra an toàn: Không chứa NaN hoặc Inf
    if np.isnan(y_p).any() or np.isinf(y_p).any():
        raise ValueError("Dự đoán của mô hình chứa giá trị NaN hoặc không hữu hạn (Inf).")

    # Đảm bảo không có dự đoán âm đối với giá xe
    y_p_clipped = np.clip(y_p, a_min=0.0, a_max=None)

    mae = float(mean_absolute_error(y_t, y_p_clipped))
    rmse = float(np.sqrt(mean_squared_error(y_t, y_p_clipped)))
    r2 = float(r2_score(y_t, y_p_clipped))

    # Tỷ lệ sai số phần trăm tuyệt đối (Percentage Error)
    # Tránh chia cho 0 bằng cách lọc mẫu dương
    valid_mask = y_t > 0
    if valid_mask.sum() > 0:
        ape = np.abs((y_t[valid_mask] - y_p_clipped[valid_mask]) / y_t[valid_mask]) * 100.0
        mape = float(np.mean(ape))
        mdape = float(np.median(ape))
    else:
        mape = np.nan
        mdape = np.nan

    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2": round(r2, 4),
        "mape": round(mape, 2),
        "mdape": round(mdape, 2),
    }


def compute_residual_dataframe(
    y_true: np.ndarray | pd.Series,
    y_pred: np.ndarray | pd.Series,
    listing_ids: pd.Series | None = None,
) -> pd.DataFrame:
    """Tạo bảng phân tích phần dư phục vụ trực quan hóa sai số."""
    y_t = np.asarray(y_true, dtype="float64")
    y_p = np.asarray(y_pred, dtype="float64")

    residual = y_t - y_p
    abs_error = np.abs(residual)
    pct_error = (abs_error / np.where(y_t > 0, y_t, 1.0)) * 100.0

    df_res = pd.DataFrame({
        "actual_price_vnd": y_t,
        "predicted_price_vnd": y_p,
        "residual_vnd": residual,
        "absolute_error_vnd": abs_error,
        "percentage_error": pct_error,
    })

    if listing_ids is not None:
        df_res.insert(0, "listing_id", listing_ids.reset_index(drop=True))

    return df_res
