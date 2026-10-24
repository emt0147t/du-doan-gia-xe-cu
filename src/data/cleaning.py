"""Module làm sạch dữ liệu và trích xuất đặc trưng (Data Cleaning & Feature Engineering).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer

Module này cung cấp các hàm xử lý dữ liệu bảng độc lập, có thể kiểm thử (testable),
áp dụng các quy tắc làm sạch đã được chuẩn hóa tại docs/eda_findings_and_cleaning_policy.md.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Tuple
import numpy as np
import pandas as pd

from src.data.price_parser import parse_vietnamese_price_to_vnd

# Danh sách các thương hiệu xe sang (Luxury Brands) phổ biến tại thị trường Việt Nam
LUXURY_BRANDS: set[str] = {
    "Mercedes-Benz", "BMW", "Lexus", "Audi", "Porsche",
    "Land Rover", "Volvo", "Bentley", "Rolls-Royce", "Jaguar", "Maserati"
}


def clean_price_column(df: pd.DataFrame, source_col: str = "Giá", target_col: str = "price_vnd") -> pd.DataFrame:
    """Bóc tách chuỗi giá tiếng Việt sang số nguyên VND.
    
    Bảo toàn 100% cột giá gốc ban đầu, không thay thế giá thiếu bằng 0.

    Args:
        df: DataFrame đầu vào chứa cột giá gốc.
        source_col: Tên cột giá gốc.
        target_col: Tên cột giá sau khi chuẩn hóa.

    Returns:
        DataFrame mới chứa cột `target_col`.
    """
    df_out = df.copy()
    if source_col not in df_out.columns:
        df_out[target_col] = np.nan
        return df_out

    parsed_values = []
    for val in df_out[source_col]:
        parsed = parse_vietnamese_price_to_vnd(val)
        parsed_values.append(parsed if parsed is not None else np.nan)

    df_out[target_col] = pd.Series(parsed_values, index=df_out.index, dtype="float64")
    return df_out


def clean_year_column(df: pd.DataFrame, source_col: str = "Năm sản xuất", target_col: str = "year") -> pd.DataFrame:
    """Chuyển đổi năm sản xuất sang kiểu số nguyên có kiểm soát.

    Args:
        df: DataFrame đầu vào.
        source_col: Cột năm sản xuất gốc.
        target_col: Cột năm chuẩn hóa.

    Returns:
        DataFrame mới chứa cột `target_col`.
    """
    df_out = df.copy()
    if source_col in df_out.columns:
        df_out[target_col] = pd.to_numeric(df_out[source_col], errors="coerce")
    else:
        df_out[target_col] = np.nan
    return df_out


def clean_mileage_column(df: pd.DataFrame, source_col: str = "Số Km đã đi", target_col: str = "mileage_km") -> pd.DataFrame:
    """Chuẩn hóa số kilomet đã đi (ODO).

    Loại bỏ đơn vị 'Km', dấu phẩy, dấu chấm phân cách hàng nghìn.
    Các giá trị tràn số lính canh (>= 1,000,000 km) được gán thành NaN để xử lý an toàn.
    Giữ nguyên giá trị 0 km để phân tích riêng qua cờ nhị phân `is_zero_mileage`.

    Args:
        df: DataFrame đầu vào.
        source_col: Tên cột ODO thô.
        target_col: Tên cột ODO chuẩn hóa.

    Returns:
        DataFrame mới chứa cột `target_col`.
    """
    df_out = df.copy()
    if source_col not in df_out.columns:
        df_out[target_col] = np.nan
        return df_out

    def _parse_km(val: Any) -> float:
        if pd.isna(val):
            return np.nan
        s = str(val).replace("Km", "").replace("km", "").replace(",", "").replace(".", "").strip()
        try:
            km = float(s)
            # Giá trị âm hoặc quá 1 triệu km coi là không hợp lệ / lỗi nhập liệu
            if km < 0 or km > 1_000_000:
                return np.nan
            return km
        except (ValueError, TypeError):
            return np.nan

    df_out[target_col] = df_out[source_col].apply(_parse_km)
    return df_out


def clean_categorical_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Chuẩn hóa các biến danh mục (trim khoảng trắng, đồng nhất tên thương hiệu).

    - Chuẩn hóa 'Mercedes Benz' thành 'Mercedes-Benz'.
    - Lọc các ký tự dị biệt trong hộp số ('-' hoặc 'Số hỗn hợp' chuyển thành NaN).
    - Chuẩn hóa xuất xứ ('Lắp ráp trong nước' -> 'Trong nước', 'Nhập khẩu' -> 'Nhập khẩu').
    """
    df_out = df.copy()

    # Chuẩn hóa Mã tin thành listing_id
    if "Mã tin" in df_out.columns:
        df_out["listing_id"] = df_out["Mã tin"].astype(str).str.strip()
    elif "listing_id" in df_out.columns:
        df_out["listing_id"] = df_out["listing_id"].astype(str).str.strip()

    # Chuẩn hóa URL
    if "URL" in df_out.columns:
        df_out["url"] = df_out["URL"].astype(str).str.strip()

    # Chuẩn hóa Brand
    if "Hãng" in df_out.columns:
        df_out["brand"] = (
            df_out["Hãng"]
            .astype(str)
            .str.strip()
            .replace({"Mercedes Benz": "Mercedes-Benz"})
        )
    elif "brand" in df_out.columns:
        df_out["brand"] = df_out["brand"].astype(str).str.strip().replace({"Mercedes Benz": "Mercedes-Benz"})

    # Chuẩn hóa Model / Trim
    if "Grade" in df_out.columns:
        df_out["model"] = df_out["Grade"].astype(str).str.strip()

    # Chuẩn hóa Hộp số
    if "Hộp số" in df_out.columns:
        raw_trans = df_out["Hộp số"].astype(str).str.strip()
        df_out["transmission"] = raw_trans.replace({"-": np.nan, "Số hỗn hợp": np.nan, "nan": np.nan})
    elif "transmission" in df_out.columns:
        raw_trans = df_out["transmission"].astype(str).str.strip()
        df_out["transmission"] = raw_trans.replace({"-": np.nan, "Số hỗn hợp": np.nan, "nan": np.nan})

    # Chuẩn hóa Xuất xứ
    if "Xuất xứ" in df_out.columns:
        raw_orig = df_out["Xuất xứ"].astype(str).str.strip()
        df_out["origin"] = raw_orig.replace({"Lắp ráp trong nước": "Trong nước", "nan": np.nan})

    # Chuẩn hóa Tình trạng
    if "Tình trạng" in df_out.columns:
        df_out["condition"] = df_out["Tình trạng"].astype(str).str.strip()

    # Chuẩn hóa Kiểu dáng
    if "Dòng xe" in df_out.columns:
        df_out["body_type"] = df_out["Dòng xe"].astype(str).str.strip()

    return df_out


def extract_engine_specs(df: pd.DataFrame, source_col: str = "Động cơ") -> pd.DataFrame:
    """Trích xuất loại nhiên liệu (fuel_type) và dung tích động cơ (displacement) từ chuỗi mô tả động cơ.

    Ví dụ: 'Xăng\\t1.5 L' -> fuel_type='Xăng', engine_displacement_l=1.5
    """
    df_out = df.copy()
    if source_col not in df_out.columns:
        if "fuel_type" not in df_out.columns:
            df_out["fuel_type"] = np.nan
        if "engine_displacement_l" not in df_out.columns:
            df_out["engine_displacement_l"] = np.nan
        return df_out

    def _get_fuel(val: Any) -> str:
        if pd.isna(val):
            return np.nan
        s = str(val).lower()
        if "xăng" in s or "petrol" in s:
            return "Xăng"
        if "dầu" in s or "diesel" in s:
            return "Dầu"
        if "điện" in s or "electric" in s:
            return "Điện"
        if "hybrid" in s:
            return "Hybrid"
        return "Khác"

    def _get_displacement(val: Any) -> float:
        if pd.isna(val):
            return np.nan
        s = str(val)
        parts = s.split("\t")
        for p in parts:
            p_clean = p.replace("L", "").replace("l", "").strip()
            try:
                disp = float(p_clean)
                if 0.5 <= disp <= 10.0:
                    return disp
            except ValueError:
                continue
        return np.nan

    df_out["fuel_type"] = df_out[source_col].apply(_get_fuel)
    df_out["engine_displacement_l"] = df_out[source_col].apply(_get_displacement)
    return df_out


def extract_capacity_specs(df: pd.DataFrame) -> pd.DataFrame:
    """Bóc tách số chỗ ngồi (seats) và số cửa (doors) thành số nguyên."""
    df_out = df.copy()

    if "Số chỗ ngồi" in df_out.columns:
        df_out["seats"] = df_out["Số chỗ ngồi"].astype(str).str.extract(r"(\d+)").astype("float64")
    elif "seats" not in df_out.columns:
        df_out["seats"] = np.nan

    if "Số cửa" in df_out.columns:
        df_out["doors"] = df_out["Số cửa"].astype(str).str.extract(r"(\d+)").astype("float64")
    elif "doors" not in df_out.columns:
        df_out["doors"] = np.nan

    return df_out


def engineer_features(df: pd.DataFrame, reference_year: int = 2024) -> pd.DataFrame:
    """Tạo các đặc trưng phái sinh có căn cứ nghiệp vụ vững chắc.

    Features được sinh:
    - `car_age`: Tuổi xe tính từ mốc cố định 2024 (thời điểm cào tập dữ liệu 2023-2024).
                 Tránh dùng năm động hiện tại để đảm bảo tính tái lập (reproducibility).
    - `is_zero_mileage`: Cờ nhị phân (1 nếu ODO == 0, 0 nếu ODO > 0).
    - `is_luxury_brand`: Cờ nhị phân (1 nếu thuộc danh mục xe sang, 0 nếu phổ thông).
    - `log_price`: Giá trị ln(price_vnd) phục vụ huấn luyện mô hình.
    """
    df_out = df.copy()

    # Tuổi xe
    if "year" in df_out.columns:
        df_out["car_age"] = reference_year - df_out["year"]
        # Bảo vệ cận âm nếu có xe đời tương lai
        df_out["car_age"] = df_out["car_age"].clip(lower=0)

    # Cờ nhị phân ODO = 0
    if "mileage_km" in df_out.columns:
        df_out["is_zero_mileage"] = (df_out["mileage_km"] == 0).astype("int64")

    # Cờ nhị phân xe sang
    if "brand" in df_out.columns:
        df_out["is_luxury_brand"] = df_out["brand"].isin(LUXURY_BRANDS).astype("int64")

    # Biến đổi Logarit nhãn mục tiêu
    if "price_vnd" in df_out.columns:
        # Chỉ lấy log cho giá trị dương hợp lệ
        valid_p = df_out["price_vnd"] > 0
        df_out["log_price"] = np.nan
        df_out.loc[valid_p, "log_price"] = np.log(df_out.loc[valid_p, "price_vnd"])

    return df_out


def clean_dataset(
    df_raw: pd.DataFrame,
    min_year: int = 2015,
    min_price: int = 30_000_000,
    max_price: int = 50_000_000_000,
    max_mileage: float = 1_000_000.0,
    reference_year: int = 2024,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Hàm điều phối toàn bộ quy trình làm sạch dữ liệu và ghi nhật ký kiểm toán.

    Args:
        df_raw: DataFrame dữ liệu thô nguyên bản (car_detail.csv).
        min_year: Năm sản xuất sàn (2015 cho Cohort A, 2010 cho Cohort B).
        min_price: Ngưỡng sàn giá VND (mặc định 30 triệu).
        max_price: Ngưỡng trần giá VND (mặc định 50 tỷ).
        max_mileage: Ngưỡng trần ODO km (mặc định 1 triệu km).
        reference_year: Năm tham chiếu tính tuổi xe.

    Returns:
        Tuple gồm (df_clean, cleaning_audit_log).
    """
    n_initial = len(df_raw)
    audit_log: Dict[str, Any] = {
        "initial_row_count": n_initial,
        "min_year_scope": min_year,
        "dropped_steps": {},
    }

    # Bước 1: Ánh xạ và chuyển đổi kiểu dữ liệu
    df_step = clean_price_column(df_raw)
    df_step = clean_year_column(df_step)
    df_step = clean_mileage_column(df_step)
    df_step = clean_categorical_columns(df_step)
    df_step = extract_engine_specs(df_step)
    df_step = extract_capacity_specs(df_step)
    df_step = engineer_features(df_step, reference_year=reference_year)

    # Bước 2: Lọc theo nhãn mục tiêu hợp lệ
    valid_price = df_step["price_vnd"].notna() & (df_step["price_vnd"] >= min_price) & (df_step["price_vnd"] <= max_price)
    dropped_price = (~valid_price).sum()
    audit_log["dropped_steps"]["invalid_or_out_of_bounds_target"] = int(dropped_price)
    df_filtered = df_step[valid_price].copy()

    # Bước 3: Lọc theo năm sản xuất (Scope)
    valid_year = df_filtered["year"].notna() & (df_filtered["year"] >= min_year)
    dropped_year = (~valid_year).sum()
    audit_log["dropped_steps"]["missing_or_out_of_scope_year"] = int(dropped_year)
    df_filtered = df_filtered[valid_year].copy()

    # Bước 4: Lọc hộp số dị biệt
    valid_trans = df_filtered["transmission"].notna()
    dropped_trans = (~valid_trans).sum()
    audit_log["dropped_steps"]["invalid_transmission"] = int(dropped_trans)
    df_filtered = df_filtered[valid_trans].copy()

    # Bước 5: Lọc ODO quá ngưỡng
    valid_mileage = df_filtered["mileage_km"].isna() | (df_filtered["mileage_km"] <= max_mileage)
    dropped_mileage = (~valid_mileage).sum()
    audit_log["dropped_steps"]["extreme_mileage_outliers"] = int(dropped_mileage)
    df_clean = df_filtered[valid_mileage].copy()

    audit_log["final_clean_row_count"] = len(df_clean)
    audit_log["retained_percentage"] = round((len(df_clean) / n_initial) * 100, 2)

    return df_clean, audit_log
