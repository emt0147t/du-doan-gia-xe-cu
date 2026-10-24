"""Module tiếp nhận và nạp tập dữ liệu ô tô ngoại tuyến (Offline Dataset Ingestion).

Module này cung cấp các tiện ích đọc, kiểm tra tính toàn vẹn (SHA-256)
và ánh xạ schema cho các tập dữ liệu bảng (CSV) mà không phụ thuộc vào kết nối mạng.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import pandas as pd


def compute_sha256(file_path: Path | str) -> str:
    """Tính toán mã băm SHA-256 của tệp để kiểm tra tính toàn vẹn và bất biến.

    Args:
        file_path: Đường dẫn tới tệp cần tính hash.

    Returns:
        Chuỗi hex biểu diễn mã băm SHA-256.

    Raises:
        FileNotFoundError: Nếu tệp không tồn tại.
    """
    path = Path(file_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Không tìm thấy tệp để tính SHA-256: {path}")

    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_raw_dataset(
    file_path: Path | str,
    required_columns: list[str] | None = None,
    encoding: str = "utf-8",
) -> pd.DataFrame:
    """Đọc tệp dữ liệu bảng thô từ đĩa, kiểm tra định dạng và các cột bắt buộc.

    Hàm này chỉ đọc ngoại tuyến từ tệp cục bộ, tuyệt đối không tải dữ liệu từ internet.

    Args:
        file_path: Đường dẫn tới tệp CSV.
        required_columns: Danh sách các cột bắt buộc phải có trong tệp.
        encoding: Mã hóa ký tự (mặc định 'utf-8').

    Returns:
        DataFrame chứa dữ liệu thô đọc từ tệp.

    Raises:
        FileNotFoundError: Nếu tệp không tồn tại.
        ValueError: Nếu tệp rỗng hoặc thiếu các cột bắt buộc.
    """
    path = Path(file_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Tệp dữ liệu không tồn tại: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"Tệp dữ liệu rỗng (0 bytes): {path}")

    try:
        df = pd.read_csv(path, encoding=encoding)
    except Exception as e:
        raise ValueError(f"Không thể đọc tệp CSV {path}: {e}") from e

    if df.empty:
        raise ValueError(f"Tệp CSV không chứa bản ghi dữ liệu nào: {path}")

    if required_columns:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(
                f"Tệp CSV thiếu các cột bắt buộc theo schema: {missing_cols}. "
                f"Các cột hiện có: {list(df.columns)}"
            )

    return df


def map_raw_to_project_schema(
    df_raw: pd.DataFrame,
    column_mapping: dict[str, str],
) -> pd.DataFrame:
    """Ánh xạ các cột từ dữ liệu thô sang tên cột chuẩn mực của dự án.

    Args:
        df_raw: DataFrame dữ liệu thô gốc.
        column_mapping: Từ điển ánh xạ từ {tên_cột_thô: tên_cột_chuẩn_dự_án}.

    Returns:
        DataFrame mới chứa các cột đã được đổi tên theo schema dự án.
    """
    df_mapped = df_raw.copy()
    valid_mapping = {
        src: dst for src, dst in column_mapping.items() if src in df_mapped.columns
    }
    return df_mapped.rename(columns=valid_mapping)
