"""Module điều phối huấn luyện và theo dõi thí nghiệm (Experiment Runner & Model Training).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, Ridge
from sklearn.pipeline import Pipeline

from src.data.preprocessing import (
    build_linear_preprocessor,
    build_tree_preprocessor,
    extract_features_and_target,
)
from src.models.evaluate import compute_regression_metrics, inverse_log_transform
from src.models.experiment_config import ExperimentConfig

EXPERIMENT_RESULTS_DIR = Path("reports/model_experiments")


def build_estimator(
    model_type: str,
    hyperparameters: Dict[str, Any] | None = None,
    random_state: int = 42,
) -> BaseEstimator:
    """Khởi tạo estimator dựa trên loại mô hình và siêu tham số."""
    params = hyperparameters.copy() if hyperparameters is not None else {}

    if model_type == "dummy_median":
        return DummyRegressor(strategy="median")
    elif model_type == "dummy_mean":
        return DummyRegressor(strategy="mean")
    elif model_type == "ridge":
        return Ridge(random_state=random_state, **params)
    elif model_type == "lasso":
        if "max_iter" not in params:
            params["max_iter"] = 3000
        return Lasso(random_state=random_state, **params)
    elif model_type == "random_forest":
        if "n_jobs" not in params:
            params["n_jobs"] = -1
        return RandomForestRegressor(random_state=random_state, **params)
    elif model_type == "hist_gradient_boosting":
        return HistGradientBoostingRegressor(random_state=random_state, **params)
    else:
        raise ValueError(f"Loại mô hình không được hỗ trợ: '{model_type}'")


def build_full_pipeline(config: ExperimentConfig) -> Pipeline:
    """Xây dựng Pipeline scikit-learn tích hợp ColumnTransformer và Estimator."""
    if config.preprocessor_type == "linear":
        preprocessor = build_linear_preprocessor()
    elif config.preprocessor_type == "tree":
        preprocessor = build_tree_preprocessor()
    else:
        raise ValueError(f"Loại preprocessor không hợp lệ: '{config.preprocessor_type}'")

    estimator = build_estimator(
        model_type=config.model_type,
        hyperparameters=config.hyperparameters,
        random_state=config.random_state,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", estimator),
        ]
    )
    return pipeline


def run_single_experiment(
    config: ExperimentConfig,
    train_df: pd.DataFrame,
    eval_df: pd.DataFrame,
    target_col: str = "price_vnd",
) -> Tuple[Dict[str, Any], np.ndarray, Pipeline]:
    """Huấn luyện một thí nghiệm trên tập Train và đánh giá trên tập Eval (Validation hoặc Test).

    Args:
        config: Cấu hình thí nghiệm.
        train_df: DataFrame tập huấn luyện.
        eval_df: DataFrame tập đánh giá.
        target_col: Cột mục tiêu gốc (mặc định 'price_vnd').

    Returns:
        Tuple gồm (metrics_dict, predictions_vnd, fitted_pipeline).
    """
    # 1. Trích xuất đặc trưng và mục tiêu (đảm bảo không rò rỉ target/identifiers)
    X_train, y_train_raw = extract_features_and_target(train_df, target_col=target_col)
    X_eval, y_eval_raw = extract_features_and_target(eval_df, target_col=target_col)

    # 2. Xử lý target cho huấn luyện (Raw hay Log)
    if config.target_type == "log":
        y_train_fit = np.log(y_train_raw.values.astype("float64"))
    elif config.target_type == "raw":
        y_train_fit = y_train_raw.values.astype("float64")
    else:
        raise ValueError(f"target_type không hợp lệ: '{config.target_type}'")

    # 3. Khởi tạo pipeline và đo thời gian huấn luyện
    pipeline = build_full_pipeline(config)

    t0_fit = time.time()
    pipeline.fit(X_train, y_train_fit)
    fit_time = round(time.time() - t0_fit, 3)

    # 4. Dự đoán và đo thời gian suy luận
    t0_pred = time.time()
    raw_preds = pipeline.predict(X_eval)
    predict_time = round(time.time() - t0_pred, 3)

    # 5. Nghịch đảo về thang đo VND nếu mô hình học trên không gian Log
    if config.target_type == "log":
        y_pred_vnd = inverse_log_transform(raw_preds)
    else:
        y_pred_vnd = np.clip(raw_preds, a_min=0.0, a_max=None)

    # 6. Tính toán các chỉ số đánh giá theo VND thực tế
    metrics = compute_regression_metrics(y_eval_raw.values, y_pred_vnd)

    # Bổ sung thông tin quản trị thí nghiệm
    experiment_record = {
        "experiment_name": config.name,
        "model_type": config.model_type,
        "target_type": config.target_type,
        "preprocessor_type": config.preprocessor_type,
        "hyperparameters": json.dumps(config.hyperparameters),
        "fit_time_seconds": fit_time,
        "predict_time_seconds": predict_time,
        **metrics,
    }

    return experiment_record, y_pred_vnd, pipeline


def run_experiment_suite(
    configs: List[ExperimentConfig],
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    output_dir: Path = EXPERIMENT_RESULTS_DIR,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """Chạy toàn bộ danh sách các thí nghiệm mô hình hóa và lưu artifact.

    Returns:
        Tuple gồm (df_results, df_val_predictions, metadata).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    results_list: List[Dict[str, Any]] = []
    val_preds_dict: Dict[str, np.ndarray] = {
        "actual_price_vnd": val_df["price_vnd"].values,
    }
    if "listing_id" in val_df.columns:
        val_preds_dict["listing_id"] = val_df["listing_id"].values

    fitted_pipelines: Dict[str, Pipeline] = {}

    for cfg in configs:
        print(f"--> Đang thực thi thí nghiệm: [{cfg.name}] ({cfg.model_type}, target={cfg.target_type})...")
        rec, preds, pipe = run_single_experiment(cfg, train_df, val_df)
        results_list.append(rec)
        val_preds_dict[cfg.name] = preds
        fitted_pipelines[cfg.name] = pipe
        print(f"    Xong trong {rec['fit_time_seconds']}s | Val MAE: {rec['mae']:,.0f} VND | R2: {rec['r2']:.4f}")

    df_results = pd.DataFrame(results_list)
    # Sắp xếp theo MAE tăng dần (mô hình tốt nhất đứng đầu)
    df_results = df_results.sort_values(by="mae", ascending=True).reset_index(drop=True)

    df_val_preds = pd.DataFrame(val_preds_dict)

    # Lưu kết quả
    results_csv = output_dir / "experiment_results.csv"
    val_preds_csv = output_dir / "validation_predictions.csv"
    df_results.to_csv(results_csv, index=False, encoding="utf-8")
    df_val_preds.to_csv(val_preds_csv, index=False, encoding="utf-8")

    meta = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "total_experiments": len(configs),
        "best_model_by_mae": df_results.iloc[0]["experiment_name"],
        "best_val_mae": float(df_results.iloc[0]["mae"]),
        "best_val_r2": float(df_results.iloc[0]["r2"]),
        "results_table": str(results_csv),
        "predictions_table": str(val_preds_csv),
    }

    meta_json = output_dir / "experiment_metadata.json"
    with open(meta_json, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    return df_results, df_val_preds, meta
