"""Unit tests cho module phân chia tập dữ liệu (src/data/split_data.py).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from src.data.split_data import (
    split_dataset,
    save_splits,
    load_splits,
)


@pytest.fixture
def mock_dataset_for_split() -> pd.DataFrame:
    """Fixture tạo tập dữ liệu 100 dòng có phân phối giá rộng để kiểm thử split."""
    np.random.seed(42)
    n = 100
    prices = np.random.exponential(scale=500_000_000, size=n) + 200_000_000
    return pd.DataFrame({
        "listing_id": [f"ID_{i:04d}" for i in range(n)],
        "price_vnd": prices,
        "year": np.random.randint(2015, 2024, size=n),
        "mileage_km": np.random.randint(0, 100000, size=n),
        "brand": np.random.choice(["Toyota", "Hyundai", "Mercedes-Benz", "Ford"], size=n),
    })


def test_split_proportions_and_counts(mock_dataset_for_split):
    """Kiểm tra tỷ lệ phân chia 80/10/10 trên tập 100 dòng."""
    df_train, df_val, df_test, meta = split_dataset(
        mock_dataset_for_split,
        train_ratio=0.8,
        val_ratio=0.1,
        test_ratio=0.1,
        random_state=42,
    )

    assert len(df_train) == 80
    assert len(df_val) == 10
    assert len(df_test) == 10
    assert meta["percentages"]["train"] == 80.0
    assert meta["percentages"]["validation"] == 10.0
    assert meta["percentages"]["test"] == 10.0


def test_split_strict_disjointness_no_overlap(mock_dataset_for_split):
    """Kiểm tra tính rời rạc 100%: Tuyệt đối không trùng lặp listing_id giữa Train, Val, Test."""
    df_train, df_val, df_test, meta = split_dataset(mock_dataset_for_split, random_state=42)

    train_ids = set(df_train["listing_id"])
    val_ids = set(df_val["listing_id"])
    test_ids = set(df_test["listing_id"])

    assert len(train_ids.intersection(val_ids)) == 0
    assert len(train_ids.intersection(test_ids)) == 0
    assert len(val_ids.intersection(test_ids)) == 0
    assert meta["leakage_verification"]["is_strictly_disjoint"] is True


def test_split_reproducibility_with_seed(mock_dataset_for_split):
    """Kiểm tra tính tái lập: Cùng random_state=42 phải sinh ra tập chia giống nhau 100%."""
    tr1, val1, te1, _ = split_dataset(mock_dataset_for_split, random_state=42)
    tr2, val2, te2, _ = split_dataset(mock_dataset_for_split, random_state=42)

    pd.testing.assert_frame_equal(tr1, tr2)
    pd.testing.assert_frame_equal(val1, val2)
    pd.testing.assert_frame_equal(te1, te2)

    # Đổi seed phải sinh ra tập khác
    tr3, _, _, _ = split_dataset(mock_dataset_for_split, random_state=123)
    assert not tr1["listing_id"].equals(tr3["listing_id"])


def test_split_invalid_ratios_raise_error(mock_dataset_for_split):
    """Kiểm tra báo lỗi khi tổng tỷ lệ không bằng 1.0."""
    with pytest.raises(ValueError, match="Tổng tỷ lệ các tập phải bằng 1.0"):
        split_dataset(mock_dataset_for_split, train_ratio=0.7, val_ratio=0.1, test_ratio=0.1)


def test_save_and_load_splits(tmp_path, mock_dataset_for_split):
    """Kiểm tra lưu trữ và đọc lại các tập chia từ đĩa."""
    df_train, df_val, df_test, meta = split_dataset(mock_dataset_for_split, random_state=42)

    output_dir = tmp_path / "splits_test"
    saved_info = save_splits(df_train, df_val, df_test, meta, output_dir=output_dir)

    assert (output_dir / "train.csv").exists()
    assert (output_dir / "val.csv").exists()
    assert (output_dir / "test.csv").exists()
    assert (output_dir / "split_metadata.json").exists()
    assert (output_dir / "train_ids.csv").exists()

    # Tải lại bằng load_splits
    loaded_train, loaded_val, loaded_test = load_splits(splits_dir=output_dir)
    assert len(loaded_train) == 80
    assert len(loaded_val) == 10
    assert len(loaded_test) == 10
    pd.testing.assert_series_equal(loaded_train["listing_id"], df_train["listing_id"].reset_index(drop=True))
