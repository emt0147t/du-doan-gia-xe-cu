# Báo Cáo Kiểm Định Độc Lập Mã Nguồn & Cổng Sẵn Sàng Dữ Liệu (Phase 1.5 Independent Code Review & Data Readiness Gate)

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 1.5 — Independent Code Review & Data Readiness Gate
- **Thời gian thực hiện**: 18/10/2026, 15:43:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Người thực hiện**: Senior Python Engineer, Data Engineer & ML Reviewer
- **Môi trường thực thi**: Windows 11, Python `3.11.9`, pytest `9.1.1`

---

## A. Test Execution (Thực Thi Kiểm Thử Độc Lập)

Quá trình kiểm thử được thực hiện qua hai vòng:
1. **Vòng 1 (Baseline Verification)**: Kiểm tra lại toàn bộ test suite sẵn có từ Phase 1 để đối chứng con số 32/32 tests.
2. **Vòng 2 (Post-Fix Verification)**: Chạy lại test suite mở rộng sau khi vá các lỗi logic tiềm ẩn và bổ sung các ca kiểm thử biên (edge cases).

### Lệnh thực thi:
```powershell
$env:PYTHONIOENCODING="utf-8"
pytest -v --tb=short
```

### Kết quả đo lường thực tế (Vòng 2 sau khi sửa lỗi và bổ sung test):
- **Tổng số ca kiểm thử**: **36 test functions** (bao gồm fixture JSON chứa 37 ca kiểm thử giá và 8 ca kiểm thử bản ghi xe).
- **Passed**: **36 (100%)**
- **Failed**: **0**
- **Skipped**: **0**
- **Thời gian chạy**: **0.11 giây**

| Test Module | Số hàm test | Trạng thái | Đánh giá tính thực chất của Assertion |
| :--- | :---: | :---: | :--- |
| [tests/test_price_parser.py](file:///D:/ai-club-end-training/tests/test_price_parser.py) | 17 | **PASSED** | 100% test có `assert result == expected` hoặc `assert result is None`. Không có test rỗng. Fixture `synthetic_price_cases.json` được nạp thực tế qua `json.load()` và assert từng ca. |
| [tests/test_validation.py](file:///D:/ai-club-end-training/tests/test_validation.py) | 19 | **PASSED** | Kiểm tra rõ ràng các giá trị boolean `is_valid` và chuỗi mã lỗi trong `errors` / `warnings`. Fixture `synthetic_car_records.json` được assert đối chiếu từng mã lỗi. |

---

## B. Findings (Các Vấn Đề Phát Hiện Qua Quá Trình Review)

Qua việc kiểm tra sâu từng dòng code và chạy các ca kiểm thử nghịch đảo (adversarial testing), đã phát hiện **3 vấn đề kỹ thuật nghiêm trọng**:

### 1. [BUG-01 | Nghiêm trọng] Hiểu sai dấu chấm phân cách hàng nghìn thành dấu thập phân trước đơn vị "triệu"
- **Vị trí**: [src/data/price_parser.py](file:///D:/ai-club-end-training/src/data/price_parser.py) (hàm `_parse_word_units_format`).
- **Hiện tượng**:
  - Khi người bán hoặc salon tại Việt Nam đăng giá dạng `"1.250 triệu"`, `"1.050 triệu"` hoặc `"1,250 triệu"` (nghĩa là 1.250 triệu = 1 tỷ 250 triệu VND), regex cũ `r"^(\d+(?:[.,]\d+)?)\s*(?:triệu|tr)$"` coi `.250` là số thập phân `1.25` triệu.
  - Kết quả trả về là `1.250.000 VND` (1,25 triệu đồng) thay vì `1.250.000.000 VND` (1,25 tỷ đồng).
  - **Mức độ ảnh hưởng**: Sai lệch **1.000 lần** (1000x error). Đây là lỗi âm thầm tạo ra giá trị sai nhưng vẫn hợp lệ về kiểu dữ liệu (`int`), có nguy cơ làm hỏng toàn bộ phân phối target trong mô hình hồi quy.

### 2. [BUG-02 | Trung bình] Trùng lặp sai lầm các bản ghi thiếu `listing_id` trong deduplication
- **Vị trí**: [src/data/validation.py](file:///D:/ai-club-end-training/src/data/validation.py) (hàm `check_duplicate_listings`).
- **Hiện tượng**:
  - Lệnh cũ `str(r.get("listing_id", "")).strip()` biến giá trị `None` thành chuỗi `"None"`.
  - Khi có hai bản ghi khác nhau cùng thiếu `listing_id` (`{"listing_id": None, "brand": "Toyota"}` và `{"listing_id": None, "brand": "Kia"}`), bản ghi thứ hai bị coi là trùng lặp với bản ghi thứ nhất (`"None" in seen_ids`).
  - **Mức độ ảnh hưởng**: Hai chiếc xe hoàn toàn khác nhau bị xóa nhầm thành trùng lặp chỉ vì cùng thiếu khóa kỹ thuật.

### 3. [BUG-03 | Trung bình] `float('nan')` và `float('inf')` vượt qua kiểm tra hoặc gây lỗi sai danh mục
- **Vị trí**: [src/data/validation.py](file:///D:/ai-club-end-training/src/data/validation.py) (hàm `validate_mileage` và `validate_categorical_field`).
- **Hiện tượng**:
  - Trong Python, `float('nan') < 0` là `False`, và `float('nan') > 1_000_000` cũng là `False`. Do đó, nếu một bản ghi từ Pandas truyền `mileage_km = float('nan')`, `validate_mileage` trước đây trả về `(True, None)` nhưng không được nhận diện là missing trong warnings.
  - Ngược lại, trong `validate_categorical_field`, `str(float('nan'))` trở thành chuỗi `"nan"`, khiến hàm báo lỗi sai danh mục (`INVALID_TRANSMISSION_CATEGORY: 'nan' không thuộc danh mục`) thay vì xem đó là một trường tùy chọn bị thiếu.

---

## C. Fixes (Các Chỉnh Sửa Đã Thực Hiện Có Căn Cứ)

### 1. Khắc phục BUG-01 trong [src/data/price_parser.py](file:///D:/ai-club-end-training/src/data/price_parser.py):
- Xây dựng hàm helper chuyên biệt [`_parse_numeric_value_before_unit(s_num: str, unit: str)`](file:///D:/ai-club-end-training/src/data/price_parser.py#L112-L157):
  - Nhận diện đúng cấu trúc dấu phân cách hàng nghìn `^\d{1,3}[.,]\d{3}$` trước đơn vị "triệu" (vd: `1.250 triệu` $\rightarrow$ `1250 triệu` $\rightarrow$ `1.250.000.000 VND`).
  - Phân biệt với số thập phân thông thường có 1–2 chữ số lẻ (vd: `850.5 triệu` $\rightarrow$ `850.500.000 VND`).
  - Bổ sung cơ chế loại trừ ngoại tệ rõ ràng (`USD`, `EUR`, `$`).

### 2. Khắc phục BUG-02 và BUG-03 trong [src/data/validation.py](file:///D:/ai-club-end-training/src/data/validation.py):
- Xây dựng hàm chuẩn hóa missing [`_is_missing_value(val: Any) -> bool`](file:///D:/ai-club-end-training/src/data/validation.py#L58-L70) nhận diện an toàn `None`, `math.isnan(val)` và chuỗi rỗng.
- Cập nhật [`validate_price`](file:///D:/ai-club-end-training/src/data/validation.py#L72-L101) và [`validate_year`](file:///D:/ai-club-end-training/src/data/validation.py#L103-L129): Bắt chặt các trường hợp `bool`, `float('nan')`, `float('inf')` và hỗ trợ số nguyên dạng float từ Pandas (`899000000.0`).
- Cập nhật [`validate_categorical_field`](file:///D:/ai-club-end-training/src/data/validation.py#L158-L177): Bỏ qua an toàn khi gặp `NaN`, hỗ trợ so khớp không phân biệt chữ hoa/thường (`case-insensitive`).
- Cập nhật [`check_duplicate_listings`](file:///D:/ai-club-end-training/src/data/validation.py#L243-L277): Tuyệt đối không gộp các bản ghi thiếu `listing_id` thành duplicate; chỉ deduplicate khi có `listing_id` hợp lệ trùng nhau.

### 3. Cập nhật Test Suites & Fixtures:
- Bổ sung 4 hàm kiểm thử mới trong [tests/test_price_parser.py](file:///D:/ai-club-end-training/tests/test_price_parser.py) và [tests/test_validation.py](file:///D:/ai-club-end-training/tests/test_validation.py).
- Bổ sung các ca kiểm thử tương ứng trong fixture [tests/fixtures/synthetic_price_cases.json](file:///D:/ai-club-end-training/tests/fixtures/synthetic_price_cases.json).

---

## D. Remaining Risks (Các Rủi Ro Kỹ Thuật Còn Lại)

1. **Khoảng giá không cố định (Price Ranges)**:
   - Các tin đăng ghi `"Từ 800 - 900 triệu"` hoặc `"khoảng 1 tỷ"` hiện tại được parser trả về `None` (chấp nhận mất tin để bảo đảm tính chính xác của nhãn học máy).
2. **Cách viết tắt dân gian thiếu đơn vị thứ hai**:
   - Dạng `"1 tỷ 5"` (thiếu chữ "trăm" hoặc "triệu") vẫn bị từ chối để tránh đoán sai giữa 1,5 tỷ và 1,005 tỷ.
3. **Mã định danh `listing_id` có thể bị thay đổi nếu tin đăng được làm mới (re-posted)**:
   - Nếu cùng một người bán xóa tin cũ và tạo tin mới cho cùng một chiếc xe, website có thể sinh `listing_id` mới. Kiểm tra trùng lặp thuần túy bằng `listing_id` sẽ không bắt được trường hợp này. Bước Feature Engineering / Cleaning ở Phase 6 sẽ cần thêm thuật toán fuzzy matching theo thông số xe.

---

## E. Source Readiness & Data Gate (Kiểm Định Sẵn Sàng Nguồn Dữ Liệu)

Trạng thái chính thức: **`AUTOMATED_COLLECTION_PENDING_PERMISSION_CLARIFICATION`**

### Bảng Kiểm Tra Bằng Chứng Còn Thiếu Trước Khi Được Cấp Phép Pilot Thực Tế:

| Tiêu chí bằng chứng | Hiện trạng | Còn thiếu gì để mở cổng Pilot? |
| :--- | :---: | :--- |
| **Cơ sở pháp lý / Cho phép từ đơn vị sở hữu** | Chưa có | Cần phản hồi chính thức từ Công ty Cổ phần Nextgen Việt Nam (dựa trên [docs/permission_request_draft.md](file:///D:/ai-club-end-training/docs/permission_request_draft.md)) hoặc quyết định phê duyệt bằng văn bản từ Mentor. |
| **Bảo vệ dữ liệu cá nhân (PII)** | Đã thiết kế | Cần chạy kiểm thử dry-run đảm bảo không một byte nào của trường số điện thoại hay tên người bán lọt vào raw data. |
| **Độ ổn định kỹ thuật của website** | Đã khảo sát 2 trang mẫu | Cần xác minh website có dựng WAF/Cloudflare Turnstile chặn IP trường học hay không khi gửi liên tiếp 10 request có delay. |
| **Tính nhất quán của trường `seats`** | `UNVERIFIED` | Cần quyết định của nhóm và Mentor về việc loại bỏ trường này khỏi baseline model hay sử dụng bảng đối chiếu (lookup dictionary) theo dòng xe. |

---

## F. Đánh Giá Tập Dữ Liệu Mở Dự Phòng (Secondary Backup Open Dataset)

Trong trường hợp không nhận được phản hồi chấp thuận từ Oto.com.vn, dự án đã khảo sát tập dữ liệu mở dự phòng trên Kaggle để không làm gián đoạn tiến độ huấn luyện mô hình:

- **Tên dataset**: [Vietnam Automobile Dataset](https://www.kaggle.com/datasets/quocvinhduong/vietnam-automobile-dataset)
- **Tác giả / Người đăng tải**: Quốc Vinh Dương (User Kaggle: `quocvinhduong`)
- **Quốc gia & Phạm vi**: Thị trường ô tô tại Việt Nam (dữ liệu các dòng xe, giá niêm yết, năm sản xuất, thông số kỹ thuật).
- **Quy mô**: Tệp `data.csv`, dung lượng khoảng ~5 MB, hơn 5.000 bản ghi.
- **Nguồn gốc dữ liệu ban đầu**: Tác giả thu thập bằng Scrapy từ các website mua bán xe tại Việt Nam.
- **Giấy phép thực tế**: Trên Kaggle được gán giấy phép cộng đồng mở (Unknown / Open Database), **tuy nhiên** vì dữ liệu gốc bắt nguồn từ việc trích xuất các sàn thương mại, giấy phép này không đại diện cho quyền thương mại hóa.
- **Đánh giá mức độ phù hợp**:
  - **KHÔNG THAY THẾ** được yêu cầu tự thu thập và xây dựng crawler trong đồ án nếu Mentor yêu cầu sinh viên phải tự trải nghiệm end-to-end data pipeline.
  - **RẤT PHÙ HỢP LÀM PHƯƠNG ÁN DỰ PHÒNG (BACKUP DATASET)**: Cho phép chuyển ngay sang Phase 4 (EDA) và Phase 5 (Modeling) nếu việc xin cấp phép crawl từ Oto.com.vn bị từ chối hoặc kéo dài quá hạn chót của khóa đào tạo.

---

## G. Acceptance Checklist

| Tiêu chí nghiệm thu (Acceptance Criteria) | Trạng thái | Minh chứng thực tế trong workspace |
| :--- | :---: | :--- |
| Đã đọc implementation thực tế | **PASS** | Đọc và phân tích toàn bộ `price_parser.py`, `validation.py`, `data_dictionary.md`. |
| Toàn bộ test suite đã được chạy lại | **PASS** | Chạy thực tế pytest: **36/36 tests passed** trong 0.11s. |
| Các test có assertion thực chất | **PASS** | Tất cả test đều assert cụ thể giá trị đầu ra và mã lỗi, không có test rỗng. |
| Parser đã được review các trường hợp biên | **PASS** | Phát hiện và vá triệt để BUG-01 (1.250 triệu), bổ sung test ngoại tệ và tính bất biến. |
| Validation đã được kiểm tra missing, kiểu dữ liệu, duplicate | **PASS** | Khắc phục BUG-02 (dedup `None` ID) và BUG-03 (xử lý an toàn `NaN`, `Inf`, `Bool`). |
| Các lỗi quan trọng phát hiện được đã được sửa | **PASS** | Cả 3 lỗi tiềm ẩn đã được sửa trực tiếp trong code nguồn. |
| Test mới được thêm cho các lỗi đã sửa | **PASS** | Bổ sung 4 hàm test mới bao quát các lỗi vừa khắc phục. |
| Tài liệu và implementation nhất quán | **PASS** | Cập nhật đồng bộ `price_parser.py`, `validation.py`, `synthetic_price_cases.json`, `reports/phase1_readiness.md`. |
| Không thực hiện network request tới website | **PASS** | Toàn bộ kiểm thử thực hiện 100% offline. |
| Không có dữ liệu giả được xem là dữ liệu thật | **PASS** | Tất cả fixture nằm trong `tests/fixtures/` với nhãn `is_synthetic: true`. Thư mục `data/raw/` không chứa dữ liệu giả. |
| Không có thay đổi Git không liên quan | **PASS** | Không chỉnh sửa file ngoài phạm vi. |
| Chưa commit thay đổi | **PASS** | Kiểm tra `git status`: Toàn bộ thay đổi nằm ở working tree, chưa commit tự động. |
| Báo cáo ghi trung thực trạng thái từng tiêu chí | **PASS** | Ghi nhận chi tiết, phân biệt rõ lỗi code và rủi ro thiết kế. |
