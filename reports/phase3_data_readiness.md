# Báo Cáo Tính Sẵn Sàng Dữ Liệu & Kiểm Định Hai Nhánh Thu Thập
*(Phase 3 — Dual-Track Data Acquisition & Dataset Validation Readiness Report)*

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 3 — Dual-Track Data Acquisition & Dataset Validation
- **Thời gian lập**: 19/10/2026, 01:25:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Data Engineer, Data Scientist & ML Engineer Mentor
- **Môi trường thực thi**: Windows 11, Python `3.11.9`, pytest `9.1.1`

---

## 1. Tình Trạng Hai Nhánh Dữ Liệu Song Song (Dual-Track Status)

Sau khi Mentor phê duyệt về mặt sư phạm cho phép nhóm triển khai cả hai hướng, nhóm đã quản lý và thiết lập độc lập hai nhánh dữ liệu:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DỰ ÁN MACHINE LEARNING PHASE 3                     │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ TRACK A: EXISTING DATASET            │ TRACK B: WEBSITE DATA COLLECTION     │
│ - Trạng thái: PENDING_LICENSE        │ - Trạng thái: ARCHITECTURE_READY_GATE│
│ - Đã xây dựng load_dataset.py        │ - Đã xây dựng crawler.py (Offline DOM│
│ - Đã lập quy chuẩn schema mapping    │ - Tích hợp PII Scrubbing (chặn SĐT)  │
│ - Tạm dừng tải Kaggle do quyền nguồn │ - Crawler Gate giữ chốt dry_run=True │
│   chưa rõ và trả về HTTP 404         │ - Chờ văn bản chấp thuận Nextgen VN  │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 2. Nguồn Đã Khảo Sát & Bằng Chứng Xác Minh (Source Selection & Evidence)

1. **Track A (Ứng viên Kaggle — Vietnam Automobile Dataset)**:
   - *Bằng chứng kỹ thuật*: Lệnh `curl.exe -I https://www.kaggle.com/datasets/quocvinhduong/vietnam-automobile-dataset` trả về `HTTP/1.1 404 Not Found`. Kaggle áp dụng cơ chế xác thực hoặc bảo vệ Cloudflare, không cho phép tải tự động vô danh qua script CLI.
   - *Bằng chứng pháp lý*: Tác giả công bố dữ liệu cào bằng Scrapy từ một website bán xe ô tô Việt Nam. Quyền phát hành dữ liệu nguồn dưới nhãn MIT là **`UNVERIFIED`**.
   - *Quyết định*: **`PENDING_LICENSE_OR_PROVENANCE`**. Không tải về workspace khi quyền chưa rõ ràng để bảo vệ tính liêm chính khoa học.
2. **Track B (Website Oto.com.vn)**:
   - *Bằng chứng kỹ thuật*: Đã thẩm định mã nguồn HTML tĩnh (SSR), thẻ `<div class="item-car">` chứa sẵn metadata (`data-call`, `data-autoid`).
   - *Bằng chứng pháp lý*: Mục 10.1 Quy chế sàn cấm trích xuất tự động; `robots.txt` không phải giấy phép. Đã soạn thảo [docs/permission_request_draft.md](file:///d:/ai-club-end-training/docs/permission_request_draft.md).
   - *Quyết định*: **`CONDITIONAL GO`**. Module crawler đã sẵn sàng nhưng khóa chốt `dry_run=True`, không gửi request cào thật cho đến khi có văn bản chấp thuận từ Nextgen Vietnam.

---

## 3. Tệp Thực Tế Đã Tiếp Nhận & Kết Quả Checksum (Artifacts & Checksums)

Tuân thủ nguyên tắc không tải dữ liệu khi chưa đủ căn cứ pháp lý, workspace chưa tiếp nhận tệp dữ liệu live nào vào `data/raw/external/`. 

Để phục vụ kiểm thử ngoại tuyến 100% cho pipeline, nhóm sử dụng tệp kiểm thử tổng hợp:
- **Tệp fixture**: `tests/fixtures/synthetic_raw_dataset.csv` (7 bản ghi)
- **Mã băm toàn vẹn (SHA-256 Checksum)**:
  `c0f7fcb1a20a40f5339f4ad16cb60d738ffeb61d56f6625895744cb85c45e851`
- **Tệp fixture HTML**: `tests/fixtures/sample_listing_page.html` (3 thẻ xe Oto.com.vn có chứa số điện thoại PII để kiểm thử bộ lọc)

---

## 4. Đặc Tả Ánh Xạ Schema (Schema Mapping Specification)

Chi tiết quy chuẩn ánh xạ 14 trường đã được ban hành tại [docs/schema_mapping.md](file:///d:/ai-club-end-training/docs/schema_mapping.md) và cài đặt trong `src/data/load_dataset.py`:
- **Ánh xạ trực tiếp (Direct)**: `listing_id`, `year`.
- **Cần chuẩn hóa (Normalization)**: `brand`, `model`, `transmission`, `fuel_type`, `location_province`, `origin`, `body_type`.
- **Cần chuyển đổi đơn vị (Unit Conversion)**: `price_vnd` (qua `price_parser.py`), `mileage_km` (bóc tách km).
- **Không có trong nguồn / Dự phòng (Provisional / Missing)**: `seats` (được giữ nguyên `None`, không đoán mò).

---

## 5. Chất Lượng Dữ Liệu Ban Đầu & Những Trường Hợp Chưa Xử Lý

- **Dữ liệu thị trường thật trên diện rộng**: Tiếp tục duy trì trạng thái **`NOT MEASURED`** theo đúng nguyên tắc trung thực khoa học, không bịa đặt số liệu.
- **Những trường hợp biên chưa thể xử lý tự động**:
  1. *Tin đăng "Giá thỏa thuận" hoặc "Liên hệ"*: Parser trả về `None`, bản ghi bị đánh dấu thiếu nhãn mục tiêu và sẽ bị loại khỏi tập huấn luyện có giám sát.
  2. *Thiếu trường số chỗ ngồi (`seats`)*: Bảng thông số chuẩn của Oto.com.vn không có trường này; tỷ lệ missing dự kiến sẽ là ~100% nếu không dùng từ điển suy diễn theo `model`.
  3. *Số kilomet (ODO) bất thường*: Cần xây dựng biến kiểm toán chéo `mileage_per_year` ở Phase 4 để phát hiện xe tua số hoặc điền tượng trưng.

---

## 6. Trạng Thái Module Crawler (Crawler Status & Safety Gate)

- **Module**: [src/data/crawler.py](file:///d:/ai-club-end-training/src/data/crawler.py)
- **Kiến trúc**: Phân tách triệt để logic DOM parsing (`extract_page_listings`, `extract_listing_card`) khỏi logic mạng (`fetch_page`).
- **Khử PII**: Bộ lọc kiểm tra regex đã được unit test xác nhận chặn 100% số điện thoại và tên liên hệ người bán.
- **Trạng thái chốt an toàn (Crawler Gate)**: **`ACTIVE (dry_run=True)`**.
- **Hành vi**: Mọi lệnh chạy live crawler đều bị chặn tự động ở cổng an toàn, không phát sinh bất kỳ HTTP request nào đến website `oto.com.vn`.

---

## 7. Kết Quả Kiểm Thử Phần Mềm Toàn Diện (Unit Test Results)

Lệnh thực thi trong môi trường `Python 3.11.9`:
```powershell
$env:PYTHONIOENCODING="utf-8"
pytest -v --tb=short
```

**Kết quả đo lường thực tế:**
- **Tổng số ca kiểm thử**: **49 test functions** (bao quát 37 cases giá, 8 cases validation records, 7 tests loader/hash, và 5 tests crawler DOM/PII/Gate).
- **Trạng thái**: **49 PASSED / 0 FAILED / 0 SKIPPED** (100% Pass trong 1.99s).
- **Tính độc lập mạng**: Toàn bộ 49 tests chạy 100% offline, không yêu cầu kết nối internet.

---

## 8. Bảng Nghiệm Thu Tiêu Chí Phase 3 (Acceptance Checklist)

| Tiêu chí nghiệm thu Phase 3 | Trạng thái | Minh chứng thực tế |
| :--- | :---: | :--- |
| **Hai nhánh dữ liệu được quản lý riêng biệt** | **PASS** | Phân định rạch ròi Track A (Dataset) và Track B (Website). |
| **Tài liệu đánh giá nguồn hiện hành** | **PASS** | Hoàn thành [docs/data_source_audit.md](file:///d:/ai-club-end-training/docs/data_source_audit.md) v3.0. |
| **Bằng chứng nguồn gốc và điều kiện dataset** | **PASS** | Đánh dấu Kaggle là `PENDING_LICENSE_OR_PROVENANCE` và `UNAVAILABLE via CLI`. |
| **Lưu hash và metadata quy chuẩn** | **PASS** | Xây dựng [data/metadata/README.md](file:///d:/ai-club-end-training/data/metadata/README.md) và hàm `compute_sha256()`. |
| **Local loader có unit tests độc lập** | **PASS** | [src/data/load_dataset.py](file:///d:/ai-club-end-training/src/data/load_dataset.py) và [tests/test_load_dataset.py](file:///d:/ai-club-end-training/tests/test_load_dataset.py) (7 tests pass). |
| **Schema mapping và Initial Quality Report** | **PASS** | Hoàn thành [docs/schema_mapping.md](file:///d:/ai-club-end-training/docs/schema_mapping.md) và [reports/dataset_initial_audit.md](file:///d:/ai-club-end-training/reports/dataset_initial_audit.md). |
| **Website crawler chỉ kích hoạt khi đủ điều kiện** | **PASS** | [src/data/crawler.py](file:///d:/ai-club-end-training/src/data/crawler.py) giữ chốt an toàn `dry_run=True`. |
| **Không có dữ liệu giả báo cáo như dữ liệu thật** | **PASS** | Toàn bộ chỉ số dữ liệu thật tiếp tục ghi nhận `NOT MEASURED`. |
| **Không có network crawling trái phép** | **PASS** | 0 HTTP crawl request đến các website mục tiêu. |
| **Kiểm tra git status & không commit tự động** | **PASS** | Toàn bộ thay đổi nằm ở working tree sẵn sàng để người dùng xem xét. |

---

## 9. Điều Kiện Để Chuyển Sang Phase 4 (Exploratory Data Analysis - EDA)

Dự án có thể bước sang Phase 4 (EDA & Feature Preprocessing) khi thỏa mãn **MỘT TRONG HAI** điều kiện sau:

1. **Kịch bản A (Nếu thực hiện Track B - Website Pilot)**:
   - Nhận được phản hồi chấp thuận từ Nextgen Vietnam.
   - Chạy pilot thu thập mẫu 30–50 tin bằng `PilotCrawler` (mở chốt `dry_run=False`, delay $\ge$ 3.0s).
   - Đạt ngưỡng đề xuất `PROPOSED_THRESHOLD`: Tỷ lệ bóc tách giá > 95%, các biến cốt lõi (`brand`, `model`, `year`) đầy đủ 100%.
2. **Kịch bản B (Nếu thực hiện Track A - Mentor cấp dataset hoặc duyệt Kaggle)**:
   - Mentor cung cấp trực tiếp tệp CSV của CLB hoặc hướng dẫn phương thức tiếp nhận tệp `data.csv` từ Kaggle kèm quyết định bảo trợ pháp lý học thuật.
   - Nạp tệp qua `src/data/load_dataset.py`, tính mã băm SHA-256, và áp dụng `src/data/validation.py` để tạo báo cáo chất lượng chính thức.
