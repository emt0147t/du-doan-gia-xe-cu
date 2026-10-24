"""
Module kiểm định dữ liệu ô tô cục bộ (Local Data Validation Contract).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Engineer & ML Mentor

Module này định nghĩa hợp đồng kiểm định chất lượng dữ liệu (Data Quality Contract)
cho từng bản ghi và tập dữ liệu xe ô tô, hoạt động hoàn toàn ngoại tuyến (offline).
Tuân thủ Data Dictionary: Phân biệt rõ dữ liệu không hợp lệ (Invalid) với dữ liệu
hợp lệ nhưng thiếu trường tùy chọn (Missing Optional Fields).
"""

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass(frozen=True)
class ValidationConfig:
    """
    Cấu hình các ngưỡng kiểm định dữ liệu nghiệp vụ có thể tùy biến.
    Tất cả các ngưỡng đều là PROPOSED_THRESHOLD phục vụ thảo luận và kiểm thử.
    """
    # Ngưỡng giá niêm yết (price_vnd)
    min_price_vnd: int = 30_000_000          # 30 triệu VND (ngưỡng sàn xe ô tô cũ giá rẻ)
    max_price_vnd: int = 50_000_000_000      # 50 tỷ VND (ngưỡng trần cho xe siêu sang)

    # Ngưỡng năm sản xuất (year)
    min_year: int = 2010                     # Xe không quá 16 năm tuổi
    max_year: int = 2026                     # Không vượt quá năm hiện tại

    # Ngưỡng số kilomet đã đi (mileage_km)
    min_mileage_km: float = 0.0              # ODO không âm
    max_mileage_km: float = 1_000_000.0      # 1 triệu km

    # Tập danh mục cho phép (Allowed Categorical Sets)
    allowed_transmissions: Set[str] = field(default_factory=lambda: {
        "Số tự động", "Số sàn"
    })
    allowed_fuel_types: Set[str] = field(default_factory=lambda: {
        "Máy xăng", "Máy dầu", "Hybrid", "Điện"
    })
    allowed_origins: Set[str] = field(default_factory=lambda: {
        "Trong nước", "Nhập khẩu"
    })
    allowed_body_types: Set[str] = field(default_factory=lambda: {
        "Sedan", "SUV", "MPV", "Hatchback", "Bán tải", "Crossover", "Coupe", "Convertible"
    })


@dataclass
class ValidationResult:
    """Kết quả kiểm định một bản ghi dữ liệu."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def _is_missing_value(val: Any) -> bool:
    """
    Kiểm tra xem một giá trị có phải là missing hay không.
    Nhận diện: None, chuỗi rỗng / toàn khoảng trắng, float('nan') (chuẩn Pandas/NumPy).
    Không coi 0 hoặc False là missing.
    """
    if val is None:
        return True
    if isinstance(val, float) and math.isnan(val):
        return True
    if isinstance(val, str) and not val.strip():
        return True
    return False


def validate_price(price_vnd: Any, config: ValidationConfig) -> Tuple[bool, Optional[str]]:
    """
    Kiểm tra biến mục tiêu price_vnd:
      - Phải tồn tại (không được None hoặc NaN).
      - Không được là kiểu bool.
      - Phải là số nguyên hoặc float tương đương nguyên (vd: 899000000.0 từ Pandas).
      - Phải nằm trong khoảng [min_price_vnd, max_price_vnd].
    """
    if _is_missing_value(price_vnd):
        return False, "MISSING_TARGET_PRICE: Biến mục tiêu price_vnd không được để trống."
    if isinstance(price_vnd, bool):
        return False, "INVALID_TARGET_TYPE: price_vnd không được là kiểu bool."
    if isinstance(price_vnd, float):
        if math.isinf(price_vnd):
            return False, "NON_FINITE_TARGET_PRICE: price_vnd không được là Infinity."
        if not price_vnd.is_integer():
            return False, f"INVALID_TARGET_TYPE: price_vnd phải là số nguyên, nhận được số thập phân {price_vnd}."
        val = int(price_vnd)
    elif isinstance(price_vnd, int):
        val = price_vnd
    else:
        return False, f"INVALID_TARGET_TYPE: price_vnd phải là kiểu int, nhận được {type(price_vnd).__name__}."

    if val < config.min_price_vnd or val > config.max_price_vnd:
        return False, (
            f"TARGET_OUT_OF_BOUNDS: price_vnd={val:,} nằm ngoài phạm vi cho phép "
            f"[{config.min_price_vnd:,}, {config.max_price_vnd:,}] VND."
        )
    return True, None


def validate_year(year: Any, config: ValidationConfig) -> Tuple[bool, Optional[str]]:
    """
    Kiểm tra năm sản xuất:
      - Phải tồn tại (trường bắt buộc, không được None/NaN).
      - Phải là số nguyên hoặc float nguyên nằm trong [min_year, max_year].
    """
    if _is_missing_value(year):
        return False, "MISSING_YEAR: Năm sản xuất không được để trống."
    if isinstance(year, bool):
        return False, "INVALID_YEAR_TYPE: year không được là kiểu bool."
    if isinstance(year, float):
        if math.isinf(year) or not year.is_integer():
            return False, f"INVALID_YEAR_TYPE: year phải là số nguyên, nhận được {year}."
        val = int(year)
    elif isinstance(year, int):
        val = year
    else:
        return False, f"INVALID_YEAR_TYPE: year phải là kiểu int, nhận được {type(year).__name__}."

    if val < config.min_year or val > config.max_year:
        return False, (
            f"YEAR_OUT_OF_BOUNDS: year={val} nằm ngoài phạm vi cho phép "
            f"[{config.min_year}, {config.max_year}]."
        )
    return True, None


def validate_mileage(mileage_km: Any, config: ValidationConfig) -> Tuple[bool, Optional[str]]:
    """
    Kiểm tra số kilomet đã đi (mileage_km):
      - Là trường TÙY CHỌN (Optional): None hoặc NaN là hợp lệ (không gây lỗi bản ghi).
      - Không được là kiểu bool hoặc chuỗi số.
      - Phải là số hữu hạn không âm và <= max_mileage_km.
    """
    if _is_missing_value(mileage_km):
        return True, None  # Trường tùy chọn hợp lệ khi missing
    if isinstance(mileage_km, bool) or not isinstance(mileage_km, (int, float)):
        return False, f"INVALID_MILEAGE_TYPE: mileage_km phải là số, nhận được {type(mileage_km).__name__}."
    if math.isinf(mileage_km):
        return False, "NON_FINITE_MILEAGE: mileage_km không được là Infinity."
    if mileage_km < config.min_mileage_km:
        return False, f"NEGATIVE_MILEAGE: mileage_km={mileage_km} không được là số âm."
    if mileage_km > config.max_mileage_km:
        return False, f"MILEAGE_EXCEEDS_MAX: mileage_km={mileage_km:,} vượt quá ngưỡng tối đa {config.max_mileage_km:,} km."
    return True, None


def validate_identifier(listing_id: Any) -> Tuple[bool, Optional[str]]:
    """
    Kiểm tra mã định danh tin đăng (listing_id):
      - Phải tồn tại và không được rỗng / 'nan' / 'null' để hỗ trợ deduplication.
    """
    if _is_missing_value(listing_id):
        return False, "MISSING_LISTING_ID: listing_id không được để trống."
    s_id = str(listing_id).strip()
    if not s_id or s_id.lower() in ("none", "null", "nan"):
        return False, "MISSING_LISTING_ID: listing_id không được là chuỗi rỗng hoặc giá trị null."
    return True, None


def validate_categorical_field(
    val: Any,
    field_name: str,
    allowed_values: Set[str]
) -> Tuple[bool, Optional[str]]:
    """
    Kiểm tra trường phân loại (Categorical):
      - Là trường tùy chọn: None hoặc NaN được chấp nhận (không gây lỗi).
      - Nếu có giá trị chuỗi: So khớp không phân biệt chữ hoa/chữ thường với allowed_values.
    """
    if _is_missing_value(val):
        return True, None
    s_val = str(val).strip()
    lookup = {v.strip().lower(): v for v in allowed_values}
    if s_val.lower() not in lookup:
        return False, (
            f"INVALID_{field_name.upper()}_CATEGORY: Giá trị '{s_val}' không thuộc "
            f"danh mục cho phép: {sorted(list(allowed_values))}."
        )
    return True, None


def validate_car_record(
    record: Dict[str, Any],
    config: Optional[ValidationConfig] = None
) -> ValidationResult:
    """
    Kiểm định toàn diện một bản ghi xe ô tô theo Data Quality Contract.

    Quy tắc phân loại:
      - ERRORS (Gây invalid): Thiếu target, target sai phạm vi, năm sai phạm vi,
        mileage âm, thiếu listing_id, hoặc trường category sai danh mục chuẩn.
      - WARNINGS (Không gây invalid): Thiếu các trường tùy chọn như mileage_km,
        fuel_type, transmission, origin, body_type, hoặc seats.

    Parameters:
      record (dict): Dictionary chứa các trường của một tin đăng.
      config (ValidationConfig, optional): Cấu hình ngưỡng kiểm tra.

    Returns:
      ValidationResult: Đối tượng chứa is_valid, danh sách errors và warnings.
    """
    if config is None:
        config = ValidationConfig()

    errors: List[str] = []
    warnings: List[str] = []

    # 1. Kiểm tra khóa định danh (bắt buộc để chống trùng)
    ok_id, err_id = validate_identifier(record.get("listing_id"))
    if not ok_id and err_id:
        errors.append(err_id)

    # 2. Kiểm tra biến mục tiêu price_vnd (bắt buộc cho Supervised Learning)
    ok_price, err_price = validate_price(record.get("price_vnd"), config)
    if not ok_price and err_price:
        errors.append(err_price)

    # 3. Kiểm tra các trường bắt buộc cơ bản: brand, model, year
    brand = record.get("brand")
    if _is_missing_value(brand):
        errors.append("MISSING_BRAND: Hãng xe (brand) không được để trống.")

    model = record.get("model")
    if _is_missing_value(model):
        errors.append("MISSING_MODEL: Dòng xe (model) không được để trống.")

    ok_year, err_year = validate_year(record.get("year"), config)
    if not ok_year and err_year:
        errors.append(err_year)

    # 4. Kiểm tra số ODO (tùy chọn nhưng nếu có phải hợp lệ)
    ok_odo, err_odo = validate_mileage(record.get("mileage_km"), config)
    if not ok_odo and err_odo:
        errors.append(err_odo)
    elif _is_missing_value(record.get("mileage_km")):
        warnings.append("OPTIONAL_FIELD_MISSING: mileage_km bị thiếu (cần xử lý Imputation ở Phase 6).")

    # 5. Kiểm tra các trường phân loại (tùy chọn)
    cat_checks = [
        ("transmission", config.allowed_transmissions),
        ("fuel_type", config.allowed_fuel_types),
        ("origin", config.allowed_origins),
        ("body_type", config.allowed_body_types),
    ]
    for fname, allowed_set in cat_checks:
        val = record.get(fname)
        ok_cat, err_cat = validate_categorical_field(val, fname, allowed_set)
        if not ok_cat and err_cat:
            errors.append(err_cat)
        elif _is_missing_value(val):
            warnings.append(f"OPTIONAL_FIELD_MISSING: {fname} bị thiếu.")

    # 6. Kiểm tra trường số chỗ ngồi (seats - Provisional)
    seats = record.get("seats")
    if not _is_missing_value(seats):
        if (
            isinstance(seats, bool)
            or not isinstance(seats, (int, float))
            or math.isinf(seats)
            or not float(seats).is_integer()
            or int(seats) < 2
            or int(seats) > 16
        ):
            errors.append(f"INVALID_SEATS_VALUE: seats={seats} không hợp lệ (cho phép từ 2 đến 16 chỗ).")
    else:
        warnings.append("PROVISIONAL_FIELD_MISSING: seats không có trong bảng thông số chuẩn.")

    is_valid = len(errors) == 0
    return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)


def check_duplicate_listings(records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Phát hiện các bản ghi trùng lặp trong tập dữ liệu dựa trên mã định danh kỹ thuật (listing_id).
    
    Quy tắc an toàn:
      - Các bản ghi thiếu listing_id hợp lệ sẽ KHÔNG được gộp chung là trùng lặp với nhau,
        mà được giữ lại trong unique_records (để hàm validate_car_record bắt lỗi thiếu ID).
      - Hai xe khác nhau có cùng thông số (brand, model, year, price) nhưng có listing_id
        khác nhau tuyệt đối KHÔNG bị kết luận là trùng lặp.

    Returns:
      (unique_records, duplicate_records): Danh sách các bản ghi duy nhất và các bản ghi bị trùng.
    """
    seen_ids: Set[str] = set()
    unique_records: List[Dict[str, Any]] = []
    duplicate_records: List[Dict[str, Any]] = []

    for r in records:
        raw_id = r.get("listing_id")
        if _is_missing_value(raw_id):
            # Không có ID hợp lệ -> Không deduplicate, giữ lại
            unique_records.append(r)
            continue

        lid = str(raw_id).strip()
        if lid.lower() in ("none", "null", "nan"):
            unique_records.append(r)
            continue

        if lid in seen_ids:
            duplicate_records.append(r)
        else:
            seen_ids.add(lid)
            unique_records.append(r)

    return unique_records, duplicate_records
