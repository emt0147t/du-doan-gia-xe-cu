"""
Module parse giá tiếng Việt sang số nguyên VND (Vietnamese Price Parser).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Engineer & ML Mentor

Module này cung cấp hàm chuẩn hóa chuỗi giá rao bán tiếng Việt sang số nguyên VND.
Được thiết kế độc lập, chỉ sử dụng Python Standard Library, phục vụ kiểm thử ngoại tuyến (Offline Readiness).
"""

import re
from typing import Optional


def _clean_raw_string(raw: Optional[str]) -> Optional[str]:
    """
    Chuẩn hóa chuỗi đầu vào: loại bỏ khoảng trắng thừa đầu/cuối và thu gọn khoảng trắng giữa.
    Trả về None nếu chuỗi rỗng hoặc chỉ toàn khoảng trắng.
    """
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    # Thu gọn khoảng trắng liên tiếp (bao gồm non-breaking spaces)
    return re.sub(r"\s+", " ", s)


def _is_non_price_indicator(s: str) -> bool:
    """
    Kiểm tra xem chuỗi có chứa các từ khóa biểu thị không có mức giá cụ thể hay không.
    (Ví dụ: 'thỏa thuận', 'liên hệ', 'thương lượng', 'call', 'inbox').
    """
    lower = s.lower()
    indicators = [
        "thỏa thuận", "thoa thuan", "thương lượng", "thuong luong",
        "liên hệ", "lien he", "lh", "call", "inbox", "đang cập nhật",
        "dang cap nhat", "chưa có", "chua co", "liên lac", "lien lac"
    ]
    return any(ind in lower for ind in indicators)


def _parse_full_digits_format(s: str) -> Optional[int]:
    """
    Xử lý các chuỗi giá viết đầy đủ bằng chữ số, có hoặc không có dấu phân cách hàng nghìn
    và hậu tố đơn vị tiền tệ.
    
    Hỗ trợ:
      - Số nguyên thuần: '850000000'
      - Dấu chấm phân cách hàng nghìn (chuẩn Việt Nam): '900.000.000 đồng', '900.000.000'
      - Dấu phẩy phân cách hàng nghìn (chuẩn quốc tế): '900,000,000 vnd'
      - Dấu chấm nghìn kết hợp dấu phẩy thập phân: '900.000.000,00'
    """
    cleaned = s.lower().strip()
    
    # Kiểm tra số âm
    if cleaned.startswith("-"):
        return None

    # Phát hiện ngoại tệ (USD, EUR, $, v.v.) -> Không phải VND, từ chối
    if re.search(r"(\$|usd|eur|jpy|cny|đô|do\b)", cleaned):
        return None

    # Lược bỏ hậu tố tiền tệ hợp lệ ở cuối chuỗi (đồng, vnđ,...)
    cleaned = re.sub(r"\s*(?:đồng|dong|vnđ|vnd|đ)$", "", cleaned).strip()

    # Trường hợp 1: Chuỗi số nguyên thuần túy (không dấu phân cách)
    if re.fullmatch(r"\d+", cleaned):
        try:
            val = int(cleaned)
            return val if val > 0 else None
        except ValueError:
            return None

    # Trường hợp 2: Dấu chấm phân cách hàng nghìn chuẩn Việt Nam (vd: 900.000.000)
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", cleaned):
        try:
            val = int(cleaned.replace(".", ""))
            return val if val > 0 else None
        except ValueError:
            return None

    # Trường hợp 3: Dấu phẩy phân cách hàng nghìn chuẩn quốc tế (vd: 900,000,000)
    if re.fullmatch(r"\d{1,3}(?:,\d{3})+", cleaned):
        try:
            val = int(cleaned.replace(",", ""))
            return val if val > 0 else None
        except ValueError:
            return None

    # Trường hợp 4: Có phần thập phân lẻ (vd: 900.000.000,50 hoặc 900,000,000.50)
    m_dec_vn = re.fullmatch(r"(\d{1,3}(?:\.\d{3})+),(\d+)", cleaned)
    if m_dec_vn:
        try:
            int_val = int(m_dec_vn.group(1).replace(".", ""))
            dec_val = float("0." + m_dec_vn.group(2))
            val = int(round(int_val + dec_val))
            return val if val > 0 else None
        except ValueError:
            return None

    m_dec_en = re.fullmatch(r"(\d{1,3}(?:,\d{3})+)\.(\d+)", cleaned)
    if m_dec_en:
        try:
            int_val = int(m_dec_en.group(1).replace(",", ""))
            dec_val = float("0." + m_dec_en.group(2))
            val = int(round(int_val + dec_val))
            return val if val > 0 else None
        except ValueError:
            return None

    return None


def _parse_numeric_value_before_unit(s_num: str, unit: str) -> Optional[float]:
    """
    Bóc tách số học đứng trước từ chỉ đơn vị (tỷ hoặc triệu), nhận diện chính xác
    ranh giới giữa dấu chấm thập phân và dấu phân cách hàng nghìn.
    
    Quy tắc:
      - Với đơn vị 'tỷ' / 'tỉ': Dấu chấm hoặc phẩy luôn là dấu thập phân
        (vd: 1.25 tỷ = 1 tỷ 250 triệu, 1,2 tỷ = 1 tỷ 200 triệu).
      - Với đơn vị 'triệu' / 'tr':
        + Nếu có 1 hoặc nhiều dấu phân cách theo sau bởi đúng 3 chữ số (vd: '1.250', '1.050', '1,250'):
          Đây là dấu phân cách hàng nghìn (1.250 triệu = 1.250.000.000 VND).
        + Nếu có 1 hoặc 2 chữ số thập phân (vd: '850.5', '850,5'):
          Đây là số thập phân (850.5 triệu = 850.500.000 VND).
    """
    s = s_num.strip()
    if unit in ("tỷ", "tỉ"):
        # Không cho phép chuỗi lẫn nhiều dấu phân cách (như 1.2.3)
        if s.count(".") + s.count(",") > 1:
            return None
        s_norm = s.replace(",", ".")
        try:
            return float(s_norm)
        except ValueError:
            return None

    elif unit in ("triệu", "tr"):
        # Trường hợp A: Dấu phân cách hàng nghìn chuẩn 3 chữ số (vd: 1.250, 1.050, 2.300 hoặc 1,250)
        if re.fullmatch(r"^\d{1,3}[.,]\d{3}$", s):
            clean_digits = re.sub(r"[.,]", "", s)
            return float(clean_digits)

        # Trường hợp B: Nhiều cụm phân cách hàng nghìn (vd: 1.000.000 triệu)
        if re.fullmatch(r"^\d{1,3}(?:\.\d{3})+$", s) or re.fullmatch(r"^\d{1,3}(?:,\d{3})+$", s):
            clean_digits = re.sub(r"[.,]", "", s)
            return float(clean_digits)

        # Trường hợp C: Số thập phân thông thường (vd: 850.5, 850,5, 850.25)
        if s.count(".") + s.count(",") > 1:
            return None
        s_norm = s.replace(",", ".")
        try:
            return float(s_norm)
        except ValueError:
            return None

    return None


def _parse_word_units_format(s: str) -> Optional[int]:
    """
    Xử lý các chuỗi giá sử dụng từ chỉ đơn vị (tỷ / tỉ, triệu / tr).
    
    Hỗ trợ:
      - Chỉ có triệu: '899 triệu', '850 triệu đồng', '899tr', '850.5 triệu', '1.250 triệu'
      - Chỉ có tỷ: '1,2 tỷ', '1.25 tỷ', '2 tỷ', '3 tỉ', '1.2 tỉ'
      - Kết hợp tỷ và triệu: '1 tỷ 200 triệu', '1 tỉ 169 triệu', '2 tỷ 50 tr'
    """
    cleaned = s.lower().strip()

    # Kiểm tra số âm
    if cleaned.startswith("-"):
        return None

    # Phát hiện ngoại tệ
    if re.search(r"(\$|usd|eur|jpy|cny|đô|do\b)", cleaned):
        return None

    # Lược bỏ hậu tố tiền tệ dư thừa ở cuối (đồng, vnđ,...)
    cleaned = re.sub(r"\s*(?:đồng|dong|vnđ|vnd|đ)$", "", cleaned).strip()

    # Loại bỏ các từ chỉ khoảng giá hoặc từ liên kết mơ hồ (không đoán giá)
    ambiguous_keywords = ["đến", "den", "tới", "toi", "khoảng", "khoang", "/", "hoặc", "hoac", "-"]
    if any(k in cleaned for k in ambiguous_keywords):
        return None

    # Khớp dạng 1: Kết hợp cả Tỷ và Triệu (vd: '1 tỷ 200 triệu', '1 tỉ 169 triệu', '1,5 tỷ 200 triệu')
    comb_pattern = r"^(\d+(?:[.,]\d+)?)\s*(?:tỷ|tỉ)\s+(\d+(?:[.,]\d+)?)\s*(?:triệu|tr)$"
    m_comb = re.fullmatch(comb_pattern, cleaned)
    if m_comb:
        val_ty = _parse_numeric_value_before_unit(m_comb.group(1), "tỷ")
        val_tr = _parse_numeric_value_before_unit(m_comb.group(2), "triệu")
        if val_ty is None or val_tr is None or val_ty < 0 or val_tr < 0:
            return None
        # Thành phần triệu trong chuỗi kết hợp phải < 1000 triệu (nếu >= 1000 triệu là sai ngữ pháp)
        if val_tr >= 1000:
            return None
        total = int(round(val_ty * 1_000_000_000 + val_tr * 1_000_000))
        return total if total > 0 else None

    # Khớp dạng 2: Chỉ có đơn vị Tỷ (vd: '1,2 tỷ', '1.25 tỷ', '2 tỷ', '3 tỉ', '1.2 tỉ đồng')
    billion_pattern = r"^(\d+(?:[.,]\d+)?)\s*(?:tỷ|tỉ)$"
    m_ty = re.fullmatch(billion_pattern, cleaned)
    if m_ty:
        val_ty = _parse_numeric_value_before_unit(m_ty.group(1), "tỷ")
        if val_ty is None or val_ty <= 0:
            return None
        return int(round(val_ty * 1_000_000_000))

    # Khớp dạng 3: Chỉ có đơn vị Triệu (vd: '899 triệu', '850 triệu đồng', '899tr', '850.5 triệu', '1.250 triệu')
    million_pattern = r"^(\d+(?:[.,]\d+)?)\s*(?:triệu|tr)$"
    m_tr = re.fullmatch(million_pattern, cleaned)
    if m_tr:
        val_tr = _parse_numeric_value_before_unit(m_tr.group(1), "triệu")
        if val_tr is None or val_tr <= 0:
            return None
        return int(round(val_tr * 1_000_000))

    return None


def parse_vietnamese_price_to_vnd(raw_price: Optional[str]) -> Optional[int]:
    """
    Chuyển đổi chuỗi giá rao bán tiếng Việt sang số nguyên VND (đồng).

    Quy ước nghiệp vụ:
      - 1 triệu = 1.000.000 VND
      - 1 tỷ / 1 tỉ = 1.000.000.000 VND
      - Hỗ trợ số thập phân tiếng Việt dùng dấu phẩy (vd: '1,2 tỷ' -> 1.200.000.000)
      - Hỗ trợ số thập phân dùng dấu chấm (vd: '1.25 tỷ' -> 1.250.000.000)
      - Hỗ trợ phân cách hàng nghìn trước triệu (vd: '1.250 triệu' -> 1.250.000.000)
      - Hỗ trợ dạng kết hợp (vd: '1 tỷ 200 triệu' -> 1.200.000.000)
      - Hỗ trợ viết đủ số có dấu chấm/phẩy ngăn cách hàng nghìn (vd: '900.000.000 đồng' -> 900.000.000)
      - Giá trị âm hoặc bằng 0 bị từ chối và trả về None.
      - Chuỗi không có giá cụ thể (vd: 'Liên hệ', 'Thỏa thuận') trả về None.
      - Chuỗi ngoại tệ (USD, EUR, $) bị từ chối và trả về None.
      - Chuỗi mơ hồ, sai định dạng hoặc lẫn nhiều khoảng giá trả về None (không suy diễn đoán mò).

    Giới hạn kỹ thuật (Known Limitations):
      Hàm trả về kiểu `int | None`. Điều này đồng nghĩa với việc người gọi không thể phân biệt
      nguyên nhân thất bại (do chuỗi rỗng, do là tin 'Thỏa thuận', do sai cú pháp hay do số âm).
      Đối với đường ống Machine Learning, tất cả các trường hợp trả về None đều đại diện cho
      'Không có giá trị mục tiêu hợp lệ để huấn luyện có giám sát'.

    Parameters:
      raw_price (str | None): Chuỗi giá thô nhận từ tin đăng.

    Returns:
      int | None: Số nguyên VND dương nếu parse thành công; ngược lại trả về None.
    """
    cleaned = _clean_raw_string(raw_price)
    if cleaned is None:
        return None

    # Phát hiện các tin không có mức giá cụ thể
    if _is_non_price_indicator(cleaned):
        return None

    # 1. Thử nghiệm parse theo dạng từ chỉ đơn vị (tỷ, triệu)
    val_word = _parse_word_units_format(cleaned)
    if val_word is not None:
        return val_word

    # 2. Thử nghiệm parse theo dạng số viết đầy đủ (digits)
    val_digit = _parse_full_digits_format(cleaned)
    if val_digit is not None:
        return val_digit

    # Không khớp với bất kỳ mẫu hợp lệ nào
    return None


# Alias for backward compatibility and clean notebook access
parse_price_vnd = parse_vietnamese_price_to_vnd
