"""Module thu thập dữ liệu web và bóc tách thông tin xe ô tô (Web Crawler & Parser Architecture).

Module này được thiết kế theo kiến trúc phân tách độc lập (Separation of Concerns):
1. Tầng bóc tách dữ liệu DOM (HTML Parsing): Hoàn toàn không phụ thuộc mạng, có thể kiểm thử ngoại tuyến 100%.
2. Tầng kết nối mạng (HTTP Transport): Có cơ chế kiểm soát tốc độ (Pacing), giới hạn số lượng tin,
   bảo vệ PII (tuyệt đối không lấy SĐT/tên người bán), và chốt an toàn (Crawler Gate) dừng ngay khi bị chặn.
"""

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class CrawlerConfig:
    """Cấu hình các tham số vận hành của Crawler phục vụ giai đoạn Pilot."""

    base_url: str = "https://oto.com.vn/mua-ban-xe-cu"
    request_delay_seconds: float = 3.0
    timeout_seconds: int = 15
    max_pages: int = 3
    max_records: int = 50
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AI-Club-Research-Bot/1.0 (+academic-pilot@ai-club.edu.vn)"
    )
    # Crawler Gate: Mặc định dry_run=True để ngăn chặn việc gửi request live khi chưa được phép
    dry_run: bool = True
    stop_on_challenge: bool = True


def extract_listing_card(card_soup: Any) -> dict[str, Any] | None:
    """Bóc tách thông tin kỹ thuật của một chiếc xe từ thẻ HTML chứa tin đăng.

    Hàm này là pure function, hoàn toàn không phụ thuộc mạng.
    Tuyệt đối không trích xuất các thuộc tính PII (data-phone, seller-phone, tên người bán).

    Args:
        card_soup: Đối tượng BeautifulSoup của thẻ `<div class="item-car">`.

    Returns:
        Dictionary chứa các trường thô trích xuất được, hoặc None nếu không hợp lệ.
    """
    if not card_soup:
        return None

    # 1. Trích xuất listing_id từ thuộc tính data-autoid
    listing_id = card_soup.get("data-autoid")
    if not listing_id:
        # Dự phòng trích xuất từ link href có dạng aidxc<ID>
        link_tag = card_soup.find("a", href=True)
        if link_tag:
            match = re.search(r"aidx[a-z](\d+)", link_tag["href"])
            if match:
                listing_id = match.group(1)

    if not listing_id:
        return None

    listing_id = str(listing_id).strip()

    # 2. Trích xuất metadata từ thuộc tính data-call (JSON nhúng sẵn) nếu có
    data_call_raw = card_soup.get("data-call")
    data_call: dict[str, Any] = {}
    if data_call_raw:
        try:
            data_call = json.loads(data_call_raw)
        except (json.JSONDecodeError, TypeError):
            data_call = {}

    # 3. Trích xuất giá thô từ thẻ p.price hoặc span.price
    raw_price = None
    price_tag = card_soup.find(class_="price")
    if price_tag:
        raw_price = price_tag.get_text(strip=True)

    # 4. Trích xuất tiêu đề và URL
    title = None
    source_url = None
    title_tag = card_soup.find(["h3", "h2", "a"], class_="title")
    if not title_tag:
        title_tag = card_soup.find("a", href=True)
    if title_tag:
        raw_title = title_tag.get_text(strip=True)
        # Phòng thủ chiều sâu: Làm sạch số điện thoại có thể bị người bán chèn vào tiêu đề tự do
        title = re.sub(r"(?:\+84|0)[35789]\d{8}", "[REDACTED_PHONE]", raw_title)
        href = title_tag.get("href")
        if href:
            source_url = href if href.startswith("http") else f"https://oto.com.vn{href}"

    # 5. Trích xuất danh sách tags (Năm, ODO, Hộp số, Nhiên liệu)
    tags = []
    tag_list = card_soup.find("ul", class_="tag-list")
    if tag_list:
        for li in tag_list.find_all("li"):
            text = li.get_text(strip=True)
            if text:
                tags.append(text)

    # Phân loại thông tin từ tags
    year = data_call.get("year")
    mileage_raw = None
    transmission_raw = None
    fuel_raw = None

    for t in tags:
        if re.match(r"^\d{4}$", t) and not year:
            year = int(t)
        elif "km" in t.lower():
            mileage_raw = t
        elif any(k in t.lower() for k in ["tự động", "số sàn", "at", "mt"]):
            transmission_raw = t
        elif any(k in t.lower() for k in ["xăng", "dầu", "hybrid", "điện"]):
            fuel_raw = t

    # 6. Địa điểm người bán (Tỉnh/Thành phố)
    location_raw = None
    loc_tag = card_soup.find(class_="seller-location")
    if loc_tag:
        location_raw = loc_tag.get_text(strip=True)

    # 7. Hãng, dòng xe, xuất xứ, kiểu dáng
    brand = data_call.get("brand")
    model = data_call.get("model")
    origin = data_call.get("origin")
    body_type = data_call.get("body")

    return {
        "listing_id": listing_id,
        "title": title,
        "price_raw": raw_price,
        "brand_raw": brand,
        "model_raw": model,
        "year_raw": year,
        "mileage_raw": mileage_raw,
        "transmission_raw": transmission_raw,
        "fuel_raw": fuel_raw,
        "location_raw": location_raw,
        "origin_raw": origin,
        "body_raw": body_type,
        "seats_raw": None,  # Không có trong thẻ chuẩn; giữ None
        "source_url": source_url,
    }


def extract_page_listings(html_content: str) -> list[dict[str, Any]]:
    """Phân tích cú pháp toàn bộ tài liệu HTML và trích xuất danh sách các xe.

    Args:
        html_content: Chuỗi mã nguồn HTML của trang danh sách.

    Returns:
        Danh sách các dictionary đại diện cho từng tin đăng (đã lọc PII).
    """
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, "html.parser")
    # Tìm tất cả các thẻ tin đăng theo cấu trúc item-car
    card_elements = soup.find_all("div", class_=lambda c: c and "item-car" in c)
    if not card_elements:
        # Dự phòng tìm theo class tương tự
        card_elements = soup.find_all(attrs={"data-autoid": True})

    listings: list[dict[str, Any]] = []
    for el in card_elements:
        record = extract_listing_card(el)
        if record:
            listings.append(record)

    return listings


class PilotCrawler:
    """Trình thu thập dữ liệu thử nghiệm có kiểm soát với đầy đủ chốt an toàn."""

    def __init__(self, config: CrawlerConfig | None = None) -> None:
        self.config = config or CrawlerConfig()
        self.session: Any = None
        self.requests_made = 0
        self.errors_count = 0
        self.records_extracted: list[dict[str, Any]] = []

    def run_pilot(self) -> dict[str, Any]:
        """Thực thi chu trình thu thập pilot có kiểm soát.

        Nếu self.config.dry_run = True, hàm sẽ dừng ngay lập tức và từ chối gửi request mạng.
        """
        if self.config.dry_run:
            logger.info(
                "Crawler Gate đang ở trạng thái ACTIVE (dry_run=True). "
                "Tuyệt đối không gửi HTTP request live khi chưa được cấp phép."
            )
            return {
                "status": "STOPPED_BY_CRAWLER_GATE",
                "reason": "dry_run is True. Live network collection requires explicit authorization.",
                "requests_made": 0,
                "records_count": 0,
            }

        # Nếu dry_run=False, logic thu thập thực tế chỉ chạy khi được unlatch
        # (Để đảm bảo an toàn, logic này không được gọi tự động trong Phase 3)
        return {
            "status": "UNLATCHED_NOT_PERMITTED_IN_PHASE_3",
            "requests_made": 0,
            "records_count": 0,
        }
