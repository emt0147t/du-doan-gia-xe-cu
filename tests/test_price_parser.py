"""
Unit tests cho module parse giá tiếng Việt (tests/test_price_parser.py).

Dự án: Used Car Price Prediction in Vietnam
Sử dụng: Pytest / Unittest

Kiểm thử toàn diện các dạng giá, các trường hợp biên, giá trị thiếu và chuỗi mơ hồ
dựa trên tập fixture tổng hợp và các ca kiểm thử trực tiếp.
"""

import json
from pathlib import Path
import pytest

from src.data.price_parser import parse_vietnamese_price_to_vnd


# ---------------------------------------------------------------------------
# 1. Kiểm thử các ca giá đơn vị Triệu
# ---------------------------------------------------------------------------
def test_parse_million_basic():
    assert parse_vietnamese_price_to_vnd("899 triệu") == 899_000_000
    assert parse_vietnamese_price_to_vnd("850 triệu đồng") == 850_000_000
    assert parse_vietnamese_price_to_vnd("550tr") == 550_000_000
    assert parse_vietnamese_price_to_vnd("350.5 triệu") == 350_500_000
    assert parse_vietnamese_price_to_vnd("899triệu") == 899_000_000


def test_thousand_separator_before_million():
    # Trường hợp quan trọng: '1.250 triệu' = 1 tỷ 250 triệu = 1.250.000.000 VND
    # Tránh bug hiểu nhầm dấu chấm nghìn thành dấu thập phân
    assert parse_vietnamese_price_to_vnd("1.250 triệu") == 1_250_000_000
    assert parse_vietnamese_price_to_vnd("1.050 triệu") == 1_050_000_000
    assert parse_vietnamese_price_to_vnd("2.100 triệu") == 2_100_000_000
    assert parse_vietnamese_price_to_vnd("1,250 triệu") == 1_250_000_000
    assert parse_vietnamese_price_to_vnd("1250 triệu") == 1_250_000_000


# ---------------------------------------------------------------------------
# 2. Kiểm thử các ca giá đơn vị Tỷ
# ---------------------------------------------------------------------------
def test_parse_billion_basic():
    assert parse_vietnamese_price_to_vnd("2 tỷ") == 2_000_000_000
    assert parse_vietnamese_price_to_vnd("3 tỉ") == 3_000_000_000
    assert parse_vietnamese_price_to_vnd("1.5tỷ") == 1_500_000_000
    assert parse_vietnamese_price_to_vnd("2 tỉ đồng") == 2_000_000_000


# ---------------------------------------------------------------------------
# 3. Kiểm thử số thập phân (dấu phẩy tiếng Việt và dấu chấm)
# ---------------------------------------------------------------------------
def test_parse_decimals():
    # Chuẩn dấu phẩy tiếng Việt: 1,2 tỷ = 1 tỷ 200 triệu
    assert parse_vietnamese_price_to_vnd("1,2 tỷ") == 1_200_000_000
    assert parse_vietnamese_price_to_vnd("2,5 tỉ") == 2_500_000_000
    # Chuẩn dấu chấm: 1.25 tỷ = 1 tỷ 250 triệu
    assert parse_vietnamese_price_to_vnd("1.25 tỷ") == 1_250_000_000
    assert parse_vietnamese_price_to_vnd("3.14 tỷ") == 3_140_000_000


# ---------------------------------------------------------------------------
# 4. Kiểm thử dạng kết hợp Tỷ và Triệu
# ---------------------------------------------------------------------------
def test_parse_combined_billion_million():
    assert parse_vietnamese_price_to_vnd("1 tỷ 200 triệu") == 1_200_000_000
    assert parse_vietnamese_price_to_vnd("1 tỉ 169 triệu") == 1_169_000_000
    assert parse_vietnamese_price_to_vnd("2 tỷ 50 tr") == 2_050_000_000
    assert parse_vietnamese_price_to_vnd("3 tỉ 400 triệu đồng") == 3_400_000_000
    assert parse_vietnamese_price_to_vnd("1 tỷ 050 triệu") == 1_050_000_000


# ---------------------------------------------------------------------------
# 5. Kiểm thử dạng ghi đủ số chữ số (Full digits)
# ---------------------------------------------------------------------------
def test_parse_full_digits():
    assert parse_vietnamese_price_to_vnd("900.000.000 đồng") == 900_000_000
    assert parse_vietnamese_price_to_vnd("900.000.000") == 900_000_000
    assert parse_vietnamese_price_to_vnd("900,000,000 vnd") == 900_000_000
    assert parse_vietnamese_price_to_vnd("850000000") == 850_000_000


# ---------------------------------------------------------------------------
# 6. Kiểm thử khoảng trắng và chữ hoa/thường (Casing & Whitespace)
# ---------------------------------------------------------------------------
def test_parse_casing_and_whitespace():
    assert parse_vietnamese_price_to_vnd(" 899 Triệu ") == 899_000_000
    assert parse_vietnamese_price_to_vnd("  1,2   TỶ   ") == 1_200_000_000
    assert parse_vietnamese_price_to_vnd("\t1 Tỉ 200 TRIỆU\n") == 1_200_000_000


# ---------------------------------------------------------------------------
# 7. Kiểm thử giá trị rỗng hoặc None
# ---------------------------------------------------------------------------
def test_parse_none_and_empty():
    assert parse_vietnamese_price_to_vnd(None) is None
    assert parse_vietnamese_price_to_vnd("") is None
    assert parse_vietnamese_price_to_vnd("   ") is None
    assert parse_vietnamese_price_to_vnd("\t\n") is None


# ---------------------------------------------------------------------------
# 8. Kiểm thử chuỗi không biểu thị giá cụ thể (Thỏa thuận / Liên hệ)
# ---------------------------------------------------------------------------
def test_parse_non_price_indicators():
    assert parse_vietnamese_price_to_vnd("Liên hệ") is None
    assert parse_vietnamese_price_to_vnd("Thỏa thuận") is None
    assert parse_vietnamese_price_to_vnd("Giá thỏa thuận") is None
    assert parse_vietnamese_price_to_vnd("LH 0909123456") is None
    assert parse_vietnamese_price_to_vnd("Thương lượng trực tiếp") is None
    assert parse_vietnamese_price_to_vnd("Inbox để biết giá") is None


# ---------------------------------------------------------------------------
# 9. Kiểm thử chuỗi sai cú pháp hoặc lẫn chữ lạ (Malformed)
# ---------------------------------------------------------------------------
def test_parse_malformed_strings():
    assert parse_vietnamese_price_to_vnd("abc triệu") is None
    assert parse_vietnamese_price_to_vnd("1.2.3 tỷ") is None
    assert parse_vietnamese_price_to_vnd("tỷ triệu") is None
    assert parse_vietnamese_price_to_vnd("$$$") is None


# ---------------------------------------------------------------------------
# 10. Kiểm thử chuỗi mơ hồ (Ambiguous ranges / approximations)
# ---------------------------------------------------------------------------
def test_parse_ambiguous_strings():
    # Không được tự ý đoán trung bình cộng khi gặp khoảng giá
    assert parse_vietnamese_price_to_vnd("800 triệu đến 900 triệu") is None
    assert parse_vietnamese_price_to_vnd("khoảng 1 tỷ") is None
    assert parse_vietnamese_price_to_vnd("1 tỷ / 2 tỷ") is None
    assert parse_vietnamese_price_to_vnd("1 tỷ - 1.2 tỷ") is None
    assert parse_vietnamese_price_to_vnd("1 tỷ 200 triệu 50 triệu") is None
    assert parse_vietnamese_price_to_vnd("200 triệu 1 tỷ") is None  # Thứ tự bất thường


# ---------------------------------------------------------------------------
# 11. Kiểm thử từ chối ngoại tệ (USD, EUR, $)
# ---------------------------------------------------------------------------
def test_reject_foreign_currency():
    assert parse_vietnamese_price_to_vnd("50.000 USD") is None
    assert parse_vietnamese_price_to_vnd("50000 usd") is None
    assert parse_vietnamese_price_to_vnd("50.000 $") is None
    assert parse_vietnamese_price_to_vnd("30.000 eur") is None


# ---------------------------------------------------------------------------
# 12. Kiểm thử các trường hợp biên (Boundary Cases: Âm, 0, Cực lớn)
# ---------------------------------------------------------------------------
def test_boundary_negative_prices():
    # Giá âm là phi logic đối với tin bán xe -> Trả về None
    assert parse_vietnamese_price_to_vnd("-500 triệu") is None
    assert parse_vietnamese_price_to_vnd("-100000000") is None
    assert parse_vietnamese_price_to_vnd("-1,2 tỷ") is None


def test_boundary_zero_prices():
    # Giá bằng 0 không phản ánh giá trị giao dịch -> Trả về None
    assert parse_vietnamese_price_to_vnd("0 đồng") is None
    assert parse_vietnamese_price_to_vnd("0") is None
    assert parse_vietnamese_price_to_vnd("0 triệu") is None
    assert parse_vietnamese_price_to_vnd("0 tỷ") is None


def test_boundary_extreme_large_prices():
    # Parser có khả năng bóc tách toán học số cực lớn,
    # nhưng tầng validation nghiệp vụ sau đó sẽ đánh giá tính hợp lệ của phân khúc xe.
    val = parse_vietnamese_price_to_vnd("500 tỷ")
    assert val == 500_000_000_000
    # Dạng dấu phân cách không nhất quán bị từ chối
    assert parse_vietnamese_price_to_vnd("1.200,300.400") is None


# ---------------------------------------------------------------------------
# 13. Kiểm thử tính bất biến và tính nhất quán (Property-based Invariants)
# ---------------------------------------------------------------------------
def test_idempotence_and_invariants():
    sample_inputs = ["899 triệu", "1,2 tỷ", "1.25 tỷ", "1.250 triệu", "1 tỷ 200 triệu", "900.000.000 đồng"]
    for inp in sample_inputs:
        res1 = parse_vietnamese_price_to_vnd(inp)
        res2 = parse_vietnamese_price_to_vnd(inp)
        res3 = parse_vietnamese_price_to_vnd(inp)
        assert res1 == res2 == res3, f"Parse results inconsistent across runs for '{inp}'"
        assert isinstance(res1, int), f"Parsed result is not int: {type(res1)}"
        assert res1 > 0, f"Parsed result is not positive: {res1}"


# ---------------------------------------------------------------------------
# 14. Kiểm thử tự động từ Fixture JSON tổng hợp
# ---------------------------------------------------------------------------
def test_fixture_cases():
    fixture_path = Path(__file__).parent / "fixtures" / "synthetic_price_cases.json"
    assert fixture_path.exists(), f"Fixture file not found: {fixture_path}"

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Đảm bảo fixture được gắn nhãn tổng hợp
    assert data.get("_metadata", {}).get("is_synthetic") is True

    # Kiểm tra tất cả ca hợp lệ
    for case in data.get("valid_cases", []):
        inp = case["input"]
        exp = case["expected"]
        result = parse_vietnamese_price_to_vnd(inp)
        assert result == exp, f"Failed on valid case '{inp}': got {result}, expected {exp}"

    # Kiểm tra tất cả ca không hợp lệ / None
    for case in data.get("invalid_or_none_cases", []):
        inp = case["input"]
        exp = case["expected"]
        result = parse_vietnamese_price_to_vnd(inp)
        assert result == exp, f"Failed on invalid case '{inp}': got {result}, expected {exp}"
