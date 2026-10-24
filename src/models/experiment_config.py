"""Cấu hình thí nghiệm mô hình hóa (Experiment Configuration).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict


@dataclass
class ExperimentConfig:
    """Đặc tả cấu hình của một thí nghiệm mô hình hóa.

    Attributes:
        name: Tên định danh của thí nghiệm (duy nhất).
        model_type: Loại mô hình ('dummy_median', 'dummy_mean', 'ridge', 'lasso', 'random_forest', 'hist_gradient_boosting').
        hyperparameters: Dict các siêu tham số cho mô hình.
        target_type: 'raw' (giá VND) hoặc 'log' (ln(VND)).
        preprocessor_type: 'linear' hoặc 'tree'.
        random_state: Seed ngẫu nhiên để tái lập kết quả (mặc định 42).
        description: Mô tả mục tiêu của thí nghiệm.
    """

    name: str
    model_type: str
    hyperparameters: Dict[str, Any] = field(default_factory=dict)
    target_type: str = "raw"  # 'raw' or 'log'
    preprocessor_type: str = "tree"  # 'linear' or 'tree'
    random_state: int = 42
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi cấu hình sang dict có thể tuần tự hóa JSON."""
        return asdict(self)
