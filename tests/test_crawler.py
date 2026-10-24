"""Unit tests cho module src/data/crawler.py (100% Offline Testing)."""

from pathlib import Path

from src.data.crawler import (
    CrawlerConfig,
    PilotCrawler,
    extract_listing_card,
    extract_page_listings,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
HTML_FIXTURE = FIXTURES_DIR / "sample_listing_page.html"


def test_extract_page_listings_count() -> None:
    """Kiểm tra trích xuất đúng 3 thẻ tin đăng từ HTML fixture."""
    html_content = HTML_FIXTURE.read_text(encoding="utf-8")
    listings = extract_page_listings(html_content)
    assert len(listings) == 3


def test_extract_record_details() -> None:
    """Kiểm tra độ chính xác của các trường metadata kỹ thuật trích xuất được."""
    html_content = HTML_FIXTURE.read_text(encoding="utf-8")
    listings = extract_page_listings(html_content)

    rec1 = listings[0]
    assert rec1["listing_id"] == "23442555"
    assert rec1["brand_raw"] == "Mercedes-Benz"
    assert rec1["model_raw"] == "C200"
    assert rec1["year_raw"] == 2021
    assert rec1["price_raw"] == "899 triệu"
    assert "49.000" in rec1["mileage_raw"]
    assert rec1["location_raw"] == "Hà Nội"

    rec2 = listings[1]
    assert rec2["listing_id"] == "23444950"
    assert rec2["brand_raw"] == "Kia"
    assert rec2["model_raw"] == "Carnival"
    assert rec2["year_raw"] == 2022
    assert rec2["price_raw"] == "1 tỷ 250 triệu"
    assert rec2["location_raw"] == "Tp.HCM"

    rec3 = listings[2]
    assert rec3["listing_id"] == "23444973"
    assert rec3["price_raw"] == "Thỏa thuận"


def test_pii_scrubbing_strictly_enforced() -> None:
    """Kiểm tra nghiêm ngặt: Tuyệt đối không trích xuất số điện thoại người bán vào dữ liệu."""
    html_content = HTML_FIXTURE.read_text(encoding="utf-8")
    listings = extract_page_listings(html_content)

    phone_numbers_in_fixture = ["0987654321", "0912345678", "0909090909"]
    for rec in listings:
        for val in rec.values():
            if val is not None:
                val_str = str(val)
                for phone in phone_numbers_in_fixture:
                    assert phone not in val_str, f"Phát hiện rò rỉ PII ({phone}) trong bản ghi: {rec}"


def test_pii_scrubbing_in_title_text() -> None:
    """Kiểm tra cơ chế phòng vệ chiều sâu: Khử số điện thoại nếu người bán cố tình đưa vào tiêu đề."""
    malicious_html = (
        '<div class="item-car" data-autoid="99999">'
        '<a class="title" href="/xe-99999">Bán xe Vios chính chủ liên hệ 0988123456 gấp</a>'
        '<p class="price">400 triệu</p>'
        '</div>'
    )
    listings = extract_page_listings(malicious_html)
    assert len(listings) == 1
    assert "0988123456" not in listings[0]["title"]
    assert "[REDACTED_PHONE]" in listings[0]["title"]



def test_extract_empty_or_malformed_html() -> None:
    """Kiểm tra xử lý an toàn chuỗi HTML rỗng hoặc không có thẻ item-car."""
    assert extract_page_listings("") == []
    assert extract_page_listings("<div>Không có tin đăng xe</div>") == []


def test_pilot_crawler_gate_dry_run() -> None:
    """Kiểm tra Crawler Gate: Chặn hoàn toàn các cuộc gọi live khi dry_run=True."""
    config = CrawlerConfig(dry_run=True)
    crawler = PilotCrawler(config=config)
    result = crawler.run_pilot()

    assert result["status"] == "STOPPED_BY_CRAWLER_GATE"
    assert result["requests_made"] == 0
    assert result["records_count"] == 0
