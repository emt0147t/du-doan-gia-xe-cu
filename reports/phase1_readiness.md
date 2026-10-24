# Báo Cáo Mức Độ Sẵn Sàng Giai Đoạn 1 (Phase 1 Readiness Report)

- **Dự án**: Dự đoán giá rao bán ô tô đã qua sử dụng tại Việt Nam (Used Car Price Prediction in Vietnam)
- **Giai đoạn**: Phase 1 — Offline Data Pilot & Price Parser (Đã kiểm định lại tại Phase 1.5)
- **Thời gian lập báo cáo**: 18/10/2026, 15:43:00 (Múi giờ: Asia/Ho_Chi_Minh)
- **Tác giả**: Senior Data Engineer, Data Scientist & Python Mentor

---

## 1. Các Module Đã Triển Khai (Implemented Modules)

Trong Phase 1 và 1.5, toàn bộ các thành phần mã nguồn cốt lõi đã được xây dựng, kiểm định độc lập và đặt tại thư mục [src/data/](file:///d:/ai-club-end-training/src/data):

| Tên Module / File | Vai trò và chức năng chính | Trạng thái kỹ thuật |
| :--- | :--- | :--- |
| [src/data/__init__.py](file:///d:/ai-club-end-training/src/data/__init__.py) | Khởi tạo Python package cho tầng dữ liệu | Hoàn thành |
| [src/data/price_parser.py](file:///d:/ai-club-end-training/src/data/price_parser.py) | Chuyển đổi an toàn chuỗi giá tiếng Việt sang số nguyên VND dương (`parse_vietnamese_price_to_vnd`). Nhận diện chính xác dấu phân cách hàng nghìn trước "triệu" (vd: `1.250 triệu` $\rightarrow$ `1.250.000.000`), bóc tách từ đơn vị (tỷ, triệu), số viết đủ, loại bỏ ngoại tệ và tin không có giá. | Hoàn thành (Không dùng thư viện ngoài) |
| [src/data/validation.py](file:///d:/ai-club-end-training/src/data/validation.py) | Định nghĩa hợp đồng kiểm định chất lượng dữ liệu (`ValidationConfig`, `validate_car_record`, `check_duplicate_listings`). Xử lý an toàn `NaN`, `Inf`, `Bool`, case-insensitivity danh mục và deduplication an toàn khi thiếu ID. | Hoàn thành (Data Quality Contract) |
| [tests/fixtures/synthetic_price_cases.json](file:///d:/ai-club-end-training/tests/fixtures/synthetic_price_cases.json) | Fixture JSON chứa 37 ca kiểm thử giá tổng hợp được dán nhãn `is_synthetic: true`. | Hoàn thành |
| [tests/fixtures/synthetic_car_records.json](file:///d:/ai-club-end-training/tests/fixtures/synthetic_car_records.json) | Fixture JSON chứa 8 ca bản ghi ô tô tổng hợp phục vụ kiểm thử validation contract. | Hoàn thành |

---

## 2. Kết Quả Kiểm Thử Thực Tế (Unit Test Results)

Toàn bộ test suite được thực thi bằng công cụ **pytest** (phiên bản `9.1.1`) trên môi trường Python `3.11.9`:

```powershell
$env:PYTHONIOENCODING="utf-8"; pytest -v --tb=short
```

### Kết quả chi tiết:
- **Tổng số ca kiểm thử**: **36 ca kiểm thử**
- **Trạng thái**: **36 PASSED (100%), 0 FAILED, 0 SKIPPED**
- **Thời gian thực thi**: **0.11 giây**

| File kiểm thử | Số ca test | Danh sách kiểm thử chi tiết | Kết quả |
| :--- | :---: | :--- | :---: |
| [tests/test_price_parser.py](file:///d:/ai-club-end-training/tests/test_price_parser.py) | 17 | - Triệu cơ bản, viết tắt (`tr`), không dấu cách<br>- Dấu phân cách hàng nghìn trước triệu (`1.250 triệu` $\rightarrow$ 1,25 tỷ)<br>- Tỷ cơ bản, vần `tỉ`, không dấu cách<br>- Số thập phân dấu phẩy Việt Nam (`1,2 tỷ`) & dấu chấm (`1.25 tỷ`)<br>- Kết hợp Tỷ và Triệu (`1 tỷ 200 triệu`, `1 tỉ 169 triệu`)<br>- Viết đủ số (`900.000.000 đồng`, `850000000`)<br>- Khoảng trắng & chữ hoa/thường (` 899 Triệu `)<br>- Giá trị `None`, rỗng `""`, khoảng trắng<br>- Từ khóa phi giá trị (`Liên hệ`, `Thỏa thuận`)<br>- Chuỗi sai cú pháp (`abc triệu`, `1.2.3 tỷ`)<br>- Chuỗi khoảng giá mơ hồ (`800 triệu đến 900 triệu`)<br>- Từ chối ngoại tệ (`50.000 USD`, `$`, `EUR`)<br>- Biên: Giá âm (`-500 triệu`), giá bằng 0 (`0 đồng`)<br>- Biên: Số cực lớn (`500 tỷ`)<br>- Tính bất biến & nhất quán (Idempotence)<br>- Tự động đối soát từ fixture JSON (37 sub-cases) | **17/17 PASSED** |
| [tests/test_validation.py](file:///d:/ai-club-end-training/tests/test_validation.py) | 19 | - Kiểm tra `validate_price` (hợp lệ, thiếu, NaN, Inf, bool, ngoài phạm vi)<br>- Kiểm tra `validate_year` (hợp lệ, thiếu, NaN, xe quá cũ, năm tương lai)<br>- Kiểm tra `validate_mileage` (hợp lệ, NaN missing được chấp nhận, số âm, Inf, vượt trần)<br>- Kiểm tra `validate_identifier` (hợp lệ, missing, rỗng, 'None')<br>- Kiểm tra `validate_categorical_field` (hợp lệ, NaN missing được chấp nhận, case-insensitivity, sai danh mục)<br>- Kiểm tra `validate_car_record` (bản ghi đầy đủ, bản ghi thiếu trường tùy chọn/NaN vẫn hợp lệ, bản ghi lỗi nghiêm trọng)<br>- Kiểm tra `check_duplicate_listings` (lọc tách trùng ID; không gộp ID None; không gộp xe cùng specs khác ID)<br>- Tự động kiểm thử qua fixture tổng hợp 8 bản ghi | **19/19 PASSED** |

---

## 3. Các Quy Tắc Parse Đã Được Hỗ Trợ (Supported Parsing Rules)

1. **Chuẩn hóa đại lượng tiền tệ Việt Nam**:
   - $1 \text{ triệu} = 1.000.000$ VND.
   - $1 \text{ tỷ} / 1 \text{ tỉ} = 1.000.000.000$ VND.
2. **Quy chuẩn số thập phân & phân cách hàng nghìn**:
   - Dấu phẩy tiếng Việt: `"1,2 tỷ"` $\rightarrow 1.2 \times 10^9 = 1.200.000.000$ VND.
   - Dấu chấm số học: `"1.25 tỷ"` $\rightarrow 1.25 \times 10^9 = 1.250.000.000$ VND.
   - Dấu chấm phân cách hàng nghìn trước triệu: `"1.250 triệu"` $\rightarrow 1250 \times 10^6 = 1.250.000.000$ VND.
3. **Cấu trúc hỗn hợp hai thành phần**:
   - Bóc tách độc lập phần tỷ và phần triệu: `"1 tỷ 200 triệu"` $\rightarrow 1.000.000.000 + 200.000.000 = 1.200.000.000$ VND.
4. **Viết đủ số nguyên (Full Digits)**:
   - Tự động nhận diện và bóc tách dấu chấm hàng nghìn chuẩn Việt Nam (`"900.000.000 đồng"`) hoặc dấu phẩy chuẩn quốc tế (`"900,000,000 vnd"`).
5. **Cơ chế phòng thủ (Defensive Rejection)**:
   - Bất kỳ chuỗi nào biểu thị không có giá cụ thể (`"Thỏa thuận"`, `"Liên hệ"`, `"Thương lượng"`, `"Call"`) hoặc chuỗi rỗng đều trả về `None`.
   - Các giá trị không hợp lý về mặt kinh tế đối với giá ô tô rao bán (giá $\le 0$) hoặc ngoại tệ (USD, EUR, $) đều bị từ chối và trả về `None`.

---

## 4. Các Trường Hợp Chưa Hỗ Trợ Hoặc Còn Mơ Hồ (Unsupported & Ambiguous Cases)

1. **Khoảng giá (Price Ranges)**:
   - Các chuỗi dạng `"800 triệu - 900 triệu"`, `"800 đến 900 triệu"` hoặc `"khoảng 1 tỷ"` trả về `None`.
2. **Cách nói tắt dân gian thiếu đơn vị thành phần thứ hai**:
   - Ví dụ: `"1 tỷ 5"` (trong văn nói có thể là 1 tỷ 500 triệu, nhưng về cú pháp không có chữ "trăm" hay "triệu", dễ bị nhầm thành 1 tỷ 5 triệu hoặc lỗi gõ phím cho 15 tỷ) trả về `None`.
3. **Giới hạn của kiểu trả về `int | None`**:
   - API trả về `int | None` giúp code gọi đơn giản, nhưng làm mất thông tin phân loại nguyên nhân thất bại (không biết là tin 'Thỏa thuận', chuỗi rỗng hay cú pháp lỗi). Điều này đã được ghi rõ trong docstring.

---

## 5. Giới Hạn Của Dữ Liệu Tổng Hợp Dùng Trong Kiểm Thử (Synthetic Data Limitations)

- Các tệp fixture [synthetic_price_cases.json](file:///d:/ai-club-end-training/tests/fixtures/synthetic_price_cases.json) và [synthetic_car_records.json](file:///d:/ai-club-end-training/tests/fixtures/synthetic_car_records.json) được tạo lập thuần túy cho mục đích kiểm thử phần mềm (Software Unit Testing).
- **Tuyệt đối không mang tính đại diện thống kê** cho phân phối thực tế của thị trường xe cũ Việt Nam:
  - Tỷ lệ các trường hợp lỗi trong fixture (~50%) cao hơn nhiều so với thực tế nhằm kiểm tra năng lực phòng thủ của code.
  - Không thể dùng dữ liệu fixture này để thực hiện EDA, vẽ biểu đồ phân phối hay rút ra bất kỳ nhận định kinh tế nào về thị trường ô tô.

---

## 6. Những Việc Còn Chờ Xác Minh & Chấp Thuận (Pending Approvals & Verification)

1. **Quyền truy cập nguồn dữ liệu**:
   - Tệp nháp [docs/permission_request_draft.md](file:///d:/ai-club-end-training/docs/permission_request_draft.md) đã hoàn thành nhưng **chưa được gửi đi**.
   - Cần thảo luận với Mentor xem nên gửi thư chính thức tới Oto.com.vn hay ưu tiên sử dụng tập dữ liệu dự phòng được cấp phép sẵn (ví dụ Kaggle Vietnam Automobile Dataset).
2. **Quy mô và biến động của nguồn dữ liệu**:
   - Con số 5.267 tin đăng chỉ là ghi nhận tại thời điểm khảo sát ban đầu (18/10/2026), chưa được đo đạc lại.
3. **Phê duyệt các ngưỡng đề xuất (`PROPOSED_THRESHOLD`)**:
   - Các ngưỡng tại [docs/data_pilot_plan.md](file:///d:/ai-club-end-training/docs/data_pilot_plan.md) (tỷ lệ parse > 95%, tỷ lệ ODO > 80%, trần giá 50 tỷ, sàn giá 30 triệu) cần được Mentor chính thức thông qua.

---

## 7. Đánh Giá Khả Năng Chuyển Sang Giai Đoạn Pilot Thực Tế

- **Về mặt kỹ thuật nội bộ (Code Readiness)**: **ĐẠT 100% (READY)**. Bộ parser giá, module validation, unit test suite (36 tests) và deduplication logic đã sẵn sàng xử lý dữ liệu ngay khi có nguồn cấp.
- **Về mặt pháp lý & đạo đức dữ liệu (Access Readiness)**: **CHƯA SẴN SÀNG (PENDING AUTHORIZATION)**. Dự án giữ nguyên trạng thái `AUTOMATED_COLLECTION_PENDING_PERMISSION_CLARIFICATION`, kiên quyết không gửi HTTP request live cho đến khi có sự cho phép rõ ràng.
