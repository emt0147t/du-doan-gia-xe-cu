"""Unit tests cho module src/data/load_dataset.py (100% Offline Testing)."""

from pathlib import Path

import pandas as pd
import pytest

from src.data.load_dataset import (
    compute_sha256,
    load_raw_dataset,
    map_raw_to_project_schema,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
SYNTHETIC_CSV = FIXTURES_DIR / "synthetic_raw_dataset.csv"


def test_compute_sha256_existing_file() -> None:
    """Kiểm tra tính mã băm SHA-256 trên tệp fixture tổng hợp."""
    sha = compute_sha256(SYNTHETIC_CSV)
    assert isinstance(sha, str)
    assert len(sha) == 64  # SHA-256 hex string có đúng 64 ký tự
    assert sha == compute_sha256(SYNTHETIC_CSV)  # Tính bất biến (idempotent)


def test_compute_sha256_missing_file() -> None:
    """Kiểm tra báo lỗi FileNotFoundError khi tệp không tồn tại."""
    with pytest.raises(FileNotFoundError):
        compute_sha256(FIXTURES_DIR / "non_existent_file.csv")


def test_load_raw_dataset_success() -> None:
    """Kiểm tra nạp tệp CSV tổng hợp thành công và trả về DataFrame hợp lệ."""
    df = load_raw_dataset(SYNTHETIC_CSV)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 7
    assert "listing_id" in df.columns
    assert "price_raw" in df.columns
    assert "brand_raw" in df.columns


def test_load_raw_dataset_with_required_columns() -> None:
    """Kiểm tra xác thực các cột bắt buộc thành công."""
    req_cols = ["listing_id", "price_raw", "year_raw"]
    df = load_raw_dataset(SYNTHETIC_CSV, required_columns=req_cols)
    assert not df.empty
    assert all(col in df.columns for col in req_cols)


def test_load_raw_dataset_missing_required_columns() -> None:
    """Kiểm tra báo lỗi ValueError khi thiếu cột bắt buộc trong schema."""
    req_cols = ["listing_id", "non_existent_column_xyz"]
    with pytest.raises(ValueError, match="thiếu các cột bắt buộc"):
        load_raw_dataset(SYNTHETIC_CSV, required_columns=req_cols)


def test_load_raw_dataset_non_existent_file() -> None:
    """Kiểm tra báo lỗi FileNotFoundError khi đường dẫn tệp sai."""
    with pytest.raises(FileNotFoundError):
        load_raw_dataset(FIXTURES_DIR / "ghost_file.csv")


def test_load_raw_dataset_empty_file(tmp_path: Path) -> None:
    """Kiểm tra báo lỗi ValueError khi tệp rỗng 0 bytes."""
    empty_file = tmp_path / "empty.csv"
    empty_file.touch()
    with pytest.raises(ValueError, match="Tệp dữ liệu rỗng"):
        load_raw_dataset(empty_file)


def test_map_raw_to_project_schema() -> None:
    """Kiểm tra ánh xạ các cột thô sang cột chuẩn của dự án."""
    df = load_raw_dataset(SYNTHETIC_CSV)
    mapping = {
        "price_raw": "price_vnd_raw",
        "brand_raw": "brand",
        "model_raw": "model",
        "year_raw": "year",
    }
    df_mapped = map_raw_to_project_schema(df, mapping)
    assert "brand" in df_mapped.columns
    assert "model" in df_mapped.columns
    assert "year" in df_mapped.columns
    assert "price_vnd_raw" in df_mapped.columns
    # Cột không nằm trong mapping giữ nguyên tên
    assert "listing_id" in df_mapped.columns


def test_verify_staged_dataset_checksum_if_present() -> None:
    """Kiểm tra mã băm SHA-256 của tập dữ liệu external staged (nếu có trên đĩa)."""
    staged_csv = Path(__file__).resolve().parent.parent / "data" / "raw" / "external" / "mquaan_car_price" / "car_sell_processed.csv"
    checksum_file = Path(f"{staged_csv}.sha256")

    if not staged_csv.is_file() or not checksum_file.is_file():
        pytest.skip("Staged dataset chưa hiện diện trên máy cục bộ.")

    expected_sha = checksum_file.read_text(encoding="utf-8").strip().split()[0]
    actual_sha = compute_sha256(staged_csv)
    assert actual_sha == expected_sha
    assert len(actual_sha) == 64

