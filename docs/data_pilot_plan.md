# Kế Hoạch Thử Nghiệm Thu Thập & Chuẩn Bị Dữ Liệu (Data Pilot & Ingestion Specification)

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Phiên bản kế hoạch**: 3.1 (Hiệu chỉnh điều kiện kích hoạt độc lập và chuẩn hóa chất lượng dữ liệu tại Phase 2.1)
- **Trạng thái thực thi hiện tại**: **Giai đoạn 1 Ngoại tuyến (ĐÃ HOÀN TẤT) / Dự án đang chờ quyết định định hướng từ Mentor trước khi kích hoạt Giai đoạn 2**
- **Tài liệu liên quan**: [Data Source Audit](file:///d:/ai-club-end-training/docs/data_source_audit.md), [Data Dictionary](file:///d:/ai-club-end-training/docs/data_dictionary.md), [Permission Request Draft](file:///d:/ai-club-end-training/docs/permission_request_draft.md), [Mentor Decision Brief](file:///d:/ai-club-end-training/docs/mentor_data_source_decision.md)

---

## 1. Tổng Quan Kiến Trúc Kế Hoạch Hai Giai Đoạn

Kế hoạch chuẩn bị dữ liệu tuân thủ nghiêm ngặt tính an toàn kỹ thuật và đạo đức nghiên cứu, bao gồm hai giai đoạn:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  STAGE 1: OFFLINE READINESS (Sẵn Sàng Ngoại Tuyến)                          │
│  - Xây dựng Price Parser & 17 Unit Tests (src/data/price_parser.py)         │
│  - Định nghĩa Data Validation Contract & 19 Unit Tests (src/data/valid...)  │
│  - Xây dựng Fixtures tổng hợp kiểm thử độc lập (tests/fixtures/)            │
│  - Phát hiện và khắc phục 3 lỗi logic nghiệp vụ tiềm ẩn                     │
│  ==> ĐÃ HOÀN THÀNH 100% VỚI 36/36 TESTS PASSED (100% OFFLINE)               │
│  *Lưu ý: 36 unit tests kiểm tra logic code; chất lượng dữ liệu thật là      │
│   NOT MEASURED vì chưa có dữ liệu thật được phép sử dụng.                   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                Chờ 5 quyết định định hướng chính thức từ Mentor
                                       │
         ┌─────────────────────────────┴─────────────────────────────┐
         ▼                                                           ▼
┌──────────────────────────────────┐        ┌──────────────────────────────────┐
│ BRANCH A: AUTHORIZED COLLECTION  │        │ BRANCH B: APPROVED PUBLIC DATASET│
│ (Thu thập Web có cấp phép)       │        │ (Khai thác Dataset Mở Được Duyệt)│
│ - 4 điều kiện kích hoạt độc lập  │        │ - Mentor chấp thuận thay thế crawl│
│ - Mẫu pilot quy mô 30-50 tin     │        │ - Kiểm tra SHA-256 checksum      │
│ - Khử PII tuyệt đối              │        │ - Đối chiếu schema & audit missing│
│ - Đánh giá Parser & Validation   │        │ - Độc lập kiểm định chất lượng   │
└──────────────────────────────────┘        └──────────────────────────────────┘
```

---

## 2. Giai Đoạn 1: Sẵn Sàng Ngoại Tuyến (Stage 1 — Offline Readiness [ĐÃ HOÀN TẤT])

Tất cả các thành phần cốt lõi của Stage 1 đã được cài đặt và kiểm định độc lập trong workspace:
1. **Module Parse Giá Tiếng Việt** ([src/data/price_parser.py](file:///d:/ai-club-end-training/src/data/price_parser.py)):
   - Hỗ trợ đơn vị Triệu, Tỷ, kết hợp Tỷ-Triệu, số nguyên đầy đủ.
   - Xử lý đúng cấu trúc dấu phân cách hàng nghìn (khắc phục BUG-01: `1.250 triệu` $\rightarrow$ `1.250.000.000 VND`).
   - Loại trừ rõ ràng ngoại tệ (`USD`, `EUR`, `$`) và giá thỏa thuận (`None`).
2. **Hợp Đồng Kiểm Định Dữ Liệu Cục Bộ** ([src/data/validation.py](file:///d:/ai-club-end-training/src/data/validation.py)):
   - Khắc phục BUG-02: Không gom cụm các bản ghi thiếu `listing_id` thành trùng lặp.
   - Khắc phục BUG-03: Xử lý an toàn `float('nan')`, `float('inf')`, `bool` và khoảng trắng.
3. **Bộ Kiểm Thử Độc Lập** ([tests/](file:///d:/ai-club-end-training/tests/)):
   - Đạt **36/36 tests passed** (100% Pass) trong thời gian 0.06 giây.
   - 100% assertions thực chất, nạp fixture tổng hợp từ tệp JSON.
   - **Xác nhận**: Unit tests chỉ xác minh tính đúng đắn của logic code xử lý dữ liệu. Toàn bộ các chỉ số chất lượng dữ liệu thực tế (tỷ lệ missing, tỷ lệ lỗi parse thực tế, tỷ lệ trùng lặp thực tế, độ phân tán của giá) hiện ở trạng thái **`NOT MEASURED`** cho tới khi có dữ liệu thật được phép tiếp cận.

---

## 3. Giai Đoạn 2 — Đặc Tả Phân Nhánh Triển Khai (Stage 2 Specification)

> [!WARNING]
> **Quy định an toàn tuyệt đối**:
> Hiện tại chưa có nhánh nào được kích hoạt. Không thực hiện HTTP request live, không chạy crawler và không tải dataset khi chưa có chỉ thị từ Mentor.

### 3.1. Nhánh A — Thu Thập Dữ Liệu Website Có Cấp Phép (Branch A — Authorized Website Collection)

#### 1. Bốn điều kiện cần độc lập trước khi bắt đầu (Pre-conditions):
Nhánh A chỉ được kích hoạt khi thỏa mãn đồng thời cả 4 điều kiện, không điều kiện nào được thay thế cho nhau:
1. **Chấp thuận sư phạm từ Mentor**: Mentor đồng ý rằng phương thức thu thập và quy mô thử nghiệm phù hợp với mục tiêu đào tạo của CLB.
2. **Điều kiện sử dụng nguồn**: Điều khoản sử dụng của website cho phép trích xuất hoặc không cấm đoán.
3. **Chấp thuận của đơn vị sở hữu dữ liệu**: Có văn bản / email chấp thuận chính thức từ Công ty Cổ phần Nextgen Việt Nam (hoặc đơn vị vận hành tương ứng). *(Sự chấp thuận của Mentor không thay thế được quyền sở hữu trí tuệ của doanh nghiệp).*
4. **Đáp ứng tiêu chuẩn kỹ thuật an toàn & bảo vệ dữ liệu**:
   - Khai báo User-Agent học thuật minh bạch kèm thông tin liên hệ.
   - Áp dụng độ trễ tối thiểu `time.sleep(3.0)` giữa các request, chạy đơn luồng (single thread).
   - Bộ lọc khử PII hoạt động trước khi lưu trữ bản ghi thô.

#### 2. Quy mô mẫu thử nghiệm (Pilot Sample Size):
- **Cỡ mẫu**: Thu thập giới hạn từ **30 đến 50 bản ghi** đầu tiên bằng phương pháp lấy mẫu bước nhảy (jump-paging across categories).
- **Mục đích**: Đo lường thực tế tỷ lệ thành công của parser giá, kiểm tra sự ổn định của selector DOM, và phát hiện các trường hợp biên trên dữ liệu sống mà không gây tải cho máy chủ nguồn.

#### 3. Schema đầu ra & Phân loại trường (Output Schema):
Mỗi bản ghi được lưu trữ dưới định dạng JSON Lines (`jsonl`) với cấu trúc:
- **Trường bắt buộc (Mandatory - Thiếu sẽ làm bản ghi INVALID)**:
  - `listing_id` (string): Khóa định danh kỹ thuật trích xuất từ `data-autoid`.
  - `price_vnd` (int): Giá rao bán sau khi parse bằng `price_parser.py` (30 triệu $\le$ price $\le$ 50 tỷ VND).
  - `brand` (string): Hãng sản xuất xe (Toyota, Mazda, Kia, Honda, Ford, Mercedes-Benz...).
  - `model` (string): Dòng xe (Vios, CX-5, Morning, City, Ranger, C200...).
  - `year` (int): Năm sản xuất (2010 $\le$ year $\le$ 2026).
- **Trường tùy chọn (Optional - Thiếu sẽ ghi nhận WARNING nhưng bản ghi vẫn VALID)**:
  - `mileage_km` (float | null): Số km đã đi (0 $\le$ mileage $\le$ 1.000.000 km).
  - `transmission` (string | null): Hộp số (`Số tự động`, `Số sàn`).
  - `fuel_type` (string | null): Nhiên liệu (`Máy xăng`, `Máy dầu`, `Hybrid`, `Điện`).
  - `origin` (string | null): Xuất xứ (`Trong nước`, `Nhập khẩu`).
  - `body_type` (string | null): Kiểu dáng (`Sedan`, `SUV`, `MPV`, `Hatchback`...).
  - `location_province` (string | null): Tỉnh / thành phố nơi bán.
  - `seats` (int | null): Số chỗ ngồi (trường suy diễn / dự phòng).
- **Trường kiểm toán hệ thống (System Metadata)**:
  - `source_url` (string): URL tin đăng để đối chứng.
  - `crawl_date` (string): Thời điểm thu thập chuẩn ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`).

#### 4. Quy tắc bảo vệ quyền riêng tư & Khử PII (PII Scrubbing Rules):
- Tuyệt đối không đọc và không trích xuất các thuộc tính/thẻ chứa số điện thoại người bán (`data-phone`, `.seller-phone`, v.v.).
- Tuyệt đối không trích xuất tên cá nhân người bán (`.seller-name`, `.contact-name`).
- Tuyệt đối không lưu giữ nội dung văn bản tự do của người bán nếu chưa qua bộ lọc regex số điện thoại và email.

#### 5. Điều kiện dừng pilot ngay lập tức (Pilot Stop Conditions):
- Máy chủ nguồn trả về mã HTTP `403 Forbidden`, `429 Too Many Requests` hoặc trang chuyển hướng xác thực CAPTCHA / Cloudflare Turnstile.
- Tỷ lệ tin "Giá thỏa thuận" vượt quá **25%** tổng mẫu pilot.
- Tỷ lệ bóc tách giá thất bại trên các tin có giá cụ thể vượt quá **5%**.

---

### 3.2. Nhánh B — Khai Thác Dataset Mở Được Duyệt (Branch B — Approved Public Dataset)

#### 1. Điều kiện kích hoạt:
- Mentor phê duyệt bằng văn bản cho phép sử dụng dataset mở có sẵn (như Vietnam Automobile Dataset trên Kaggle) để thay thế hoàn toàn hoặc bổ trợ cho khâu thu thập dữ liệu.

#### 2. Quy trình kiểm tra nguồn gốc & Tính toàn vẹn:
- Lập biên bản thẩm định nguồn gốc: Ghi rõ giấy phép hiển thị trên Kaggle (MIT) và thực tế quyền phát hành dữ liệu nguồn là **`UNVERIFIED`** do nguồn gốc xuất phát từ web-scraping bên thứ 3.
- Sử dụng dataset giới hạn trong phạm vi học tập phi thương mại tại CLB.
- **Tạo mã băm kiểm tra (SHA-256 Checksum)** cho tệp `data.csv` ngay khi tải về để cố định phiên bản dữ liệu.
- Viết script kiểm tra schema độc lập: Đo lường chính xác số dòng, số cột, kiểu dữ liệu thực tế (không dùng số liệu giả định).

#### 3. Đo lường chất lượng dữ liệu thực tế:
- Đưa 100% dữ liệu qua [src/data/validation.py](file:///d:/ai-club-end-training/src/data/validation.py).
- Đo lường và báo cáo thực tế: Tỷ lệ missing từng cột, tỷ lệ outliers (giá, năm, ODO), tỷ lệ trùng lặp.

---

## 4. Bảng Tiêu Chí Quyết Định Pilot (Pilot Go / No-Go Decision Matrix)

| Tiêu chí | Ngưỡng đạt yêu cầu (PROPOSED_THRESHOLD) | Hành động khi không đạt |
| :--- | :--- | :--- |
| **Quyền truy cập & Pháp lý (Branch A)** | Thỏa mãn đồng thời cả 4 điều kiện độc lập tại Mục 3.1.1 (bao gồm văn bản chấp thuận của chủ sở hữu) | DỪNG (NO-GO) Branch A; thảo luận cùng Mentor về Branch B. |
| **Phê duyệt của Mentor (Branch B)** | Mentor phê duyệt bằng văn bản cho phép sử dụng dataset mở | DỪNG (NO-GO) Branch B; quay lại tìm nguồn được phép crawl. |
| **Tính toàn vẹn biến mục tiêu (`price_vnd`)** | Tỷ lệ parse thành công > 95% trên các tin có giá cụ thể trong mẫu pilot | Tạm dừng; cập nhật regex trong `price_parser.py` và kiểm thử lại. |
| **Độ đầy đủ biến cốt lõi (`brand`, `model`, `year`)** | Tỷ lệ missing = 0% trên các bản ghi hợp lệ | Điều chỉnh bộ lọc DOM selector; loại bỏ các bản ghi khuyết tật. |
| **Tỷ lệ thiếu biến tùy chọn (`mileage_km`)** | Tỷ lệ missing $\le$ 20% trên mẫu pilot | Ghi nhận Warning; chuẩn bị kỹ thuật Imputation ở Phase 4/5. |
| **Tính ổn định của server (Branch A)** | Không gặp mã lỗi 403, 429 hay thử thách CAPTCHA | Tăng delay từ 3.0s lên 5.0s; nếu vẫn bị chặn thì dừng pilot vĩnh viễn. |
| **Tính xác thực của dataset mở (Branch B)** | Checksum SHA-256 khớp chuẩn, schema chứa đủ các đặc trưng cốt lõi | Từ chối sử dụng dataset; tìm kiếm nguồn thay thế khác. |

---

## 5. Tạo Tác Đầu Ra Dự Kiến Của Giai Đoạn Pilot (Expected Deliverables)

Sau khi được Mentor phê chuẩn nhánh triển khai:
1. `data/raw/pilot_sample.jsonl` (cho Branch A quy mô 30–50 tin) hoặc `data/raw/vietnam_automobile_dataset.csv` kèm tệp `checksum.sha256` (cho Branch B).
2. `reports/pilot_quality_summary.md`: Báo cáo đánh giá chất lượng thực nghiệm, phân phối dữ liệu thực tế và quyết định mở rộng toàn quy mô.
